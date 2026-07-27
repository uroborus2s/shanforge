package httptransport

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func TestRecoveryDoesNotLogPanicValue(t *testing.T) {
	const secret = "secret-panic-sentinel"
	var output bytes.Buffer
	logger := logrus.New()
	logger.SetOutput(&output)
	logger.SetFormatter(&logrus.JSONFormatter{})

	router := NewRouter(logger)
	router.GET("/panic", func(_ *gin.Context) { panic(secret) })

	request := httptest.NewRequest(http.MethodGet, "/panic", nil)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)

	if response.Code != http.StatusInternalServerError {
		t.Fatalf("expected 500, got %d", response.Code)
	}
	if strings.Contains(output.String(), secret) {
		t.Fatalf("panic value leaked: %s", output.String())
	}
	if !strings.Contains(output.String(), "panic_type") {
		t.Fatalf("structured panic type missing: %s", output.String())
	}
}

func TestInvalidRequestIDIsRejected(t *testing.T) {
	const invalidRequestID = "invalid request id with spaces"
	var output bytes.Buffer
	logger := logrus.New()
	logger.SetOutput(&output)
	logger.SetFormatter(&logrus.JSONFormatter{})
	router := NewRouter(logger)

	request := httptest.NewRequest(http.MethodGet, "/live", nil)
	request.Header.Set("X-Request-ID", invalidRequestID)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, request)

	if response.Code != http.StatusBadRequest {
		t.Fatalf("expected 400, got %d", response.Code)
	}
	if !strings.Contains(response.Body.String(), "invalid_request_id") {
		t.Fatalf("expected stable error code, got %s", response.Body.String())
	}
	logOutput := output.String()
	for _, field := range []string{
		`"msg":"HTTP request rejected"`,
		`"method":"GET"`,
		`"path":"/live"`,
		`"status":400`,
		`"reason":"invalid_request_id"`,
	} {
		if !strings.Contains(logOutput, field) {
			t.Fatalf("rejection log missing %s: %s", field, logOutput)
		}
	}
	if strings.Contains(logOutput, invalidRequestID) {
		t.Fatalf("invalid request ID leaked to logs: %s", logOutput)
	}
	if strings.Count(logOutput, "\n") != 1 {
		t.Fatalf("expected one rejection log, got %s", logOutput)
	}
}
