package main

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/sirupsen/logrus"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"{{MODULE_PATH}}/internal/config"
	httptransport "{{MODULE_PATH}}/internal/transport/http"
)

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	bootstrap, err := config.LoadBootstrap()
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "load bootstrap configuration: %v\n", err)
		os.Exit(1)
	}
	initialLogLevel := bootstrap.LogLevelOverride
	if initialLogLevel == "" {
		initialLogLevel = "info"
	}
	level, err := logrus.ParseLevel(initialLogLevel)
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "parse initial log level: %v\n", err)
		os.Exit(1)
	}
	logger := logrus.New()
	logger.SetOutput(os.Stdout)
	logger.SetFormatter(&logrus.JSONFormatter{})
	logger.SetLevel(level)
	if err := run(ctx, bootstrap, logger); err != nil {
		logger.WithError(err).Error("service failed")
		os.Exit(1)
	}
}

// run owns resources that must close before main may call os.Exit.
func run(ctx context.Context, bootstrap config.Bootstrap, logger *logrus.Logger) (resultErr error) {
	cfg, err := config.Load(ctx, bootstrap)
	if err != nil {
		return fmt.Errorf("load remote configuration: %w", err)
	}
	level, err := logrus.ParseLevel(cfg.LogLevel)
	if err != nil {
		return fmt.Errorf("parse log level: %w", err)
	}
	logger.SetLevel(level)

	db, err := gorm.Open(postgres.Open(cfg.DatabaseDSN), &gorm.Config{})
	if err != nil {
		return fmt.Errorf("open database: %w", err)
	}
	sqlDB, err := db.DB()
	if err != nil {
		return fmt.Errorf("access database pool: %w", err)
	}
	sqlDB.SetMaxOpenConns(20)
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetConnMaxLifetime(30 * time.Minute)

	pingCtx, cancelPing := context.WithTimeout(ctx, 5*time.Second)
	err = sqlDB.PingContext(pingCtx)
	cancelPing()
	if err != nil {
		_ = sqlDB.Close()
		return fmt.Errorf("ping database: %w", err)
	}
	defer func() {
		if err := sqlDB.Close(); err != nil {
			resultErr = errors.Join(resultErr, fmt.Errorf("close database: %w", err))
		}
	}()
	logger.Info("database connection ready")

	server := &http.Server{
		Addr:              cfg.HTTPAddress,
		Handler:           httptransport.NewRouter(logger),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       15 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       60 * time.Second,
	}
	logger.WithField("address", cfg.HTTPAddress).Info("HTTP server starting")
	serverErr := make(chan error, 1)
	go func() {
		serverErr <- server.ListenAndServe()
	}()

	select {
	case err := <-serverErr:
		if errors.Is(err, http.ErrServerClosed) {
			return nil
		}
		return fmt.Errorf("serve HTTP: %w", err)
	case <-ctx.Done():
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer cancel()
		if err := server.Shutdown(shutdownCtx); err != nil {
			return fmt.Errorf("shutdown HTTP server: %w", err)
		}
		return nil
	}
}
