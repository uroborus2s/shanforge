package httptransport

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func NewRouter(logger *logrus.Logger) *gin.Engine {
	router := gin.New()
	router.Use(requestContext(logger), recovery(logger))
	router.GET("/live", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	})
	return router
}

func requestContext(logger *logrus.Logger) gin.HandlerFunc {
	return func(c *gin.Context) {
		started := time.Now()
		requestID := c.GetHeader("X-Request-ID")
		if requestID == "" {
			var value [16]byte
			if _, err := rand.Read(value[:]); err != nil {
				logger.WithError(err).Error("generate request ID")
				c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": "internal_error"})
				return
			}
			requestID = hex.EncodeToString(value[:])
		}
		if !validRequestID(requestID) {
			logger.WithFields(logrus.Fields{
				"method": c.Request.Method,
				"path":   c.Request.URL.Path,
				"status": http.StatusBadRequest,
				"reason": "invalid_request_id",
			}).Warn("HTTP request rejected")
			c.AbortWithStatusJSON(http.StatusBadRequest, gin.H{"error": "invalid_request_id"})
			return
		}
		c.Header("X-Request-ID", requestID)
		c.Set("logger", logger.WithField("request_id", requestID))

		c.Next()
		logger.WithFields(logrus.Fields{
			"request_id": requestID,
			"method":     c.Request.Method,
			"path":       c.Request.URL.Path,
			"status":     c.Writer.Status(),
			"latency_ms": time.Since(started).Milliseconds(),
		}).Info("HTTP request completed")
	}
}

func recovery(logger *logrus.Logger) gin.HandlerFunc {
	return gin.CustomRecoveryWithWriter(io.Discard, func(c *gin.Context, recovered any) {
		entry := logger.WithField("panic_type", fmt.Sprintf("%T", recovered))
		if requestLogger, ok := c.Get("logger"); ok {
			if typed, valid := requestLogger.(*logrus.Entry); valid {
				entry = typed.WithField("panic_type", fmt.Sprintf("%T", recovered))
			}
		}
		entry.Error("HTTP request panic recovered")
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{"error": "internal_error"})
	})
}

func validRequestID(value string) bool {
	if value == "" || len(value) > 128 {
		return false
	}
	for _, char := range value {
		if (char >= 'a' && char <= 'z') || (char >= 'A' && char <= 'Z') ||
			(char >= '0' && char <= '9') || char == '-' || char == '_' || char == '.' {
			continue
		}
		return false
	}
	return true
}
