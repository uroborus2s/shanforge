package config

import (
	"strings"
	"testing"
)

func TestDecodeRemoteRejectsUnknownFields(t *testing.T) {
	_, err := decodeRemote([]byte(`{"http_address":":8080","unknown":true}`))
	if err == nil || !strings.Contains(err.Error(), "unknown field") {
		t.Fatalf("expected unknown field error, got %v", err)
	}
}

func TestConfigValidateRejectsInvalidValues(t *testing.T) {
	tests := []Config{
		{HTTPAddress: "8080", DatabaseDSN: "dsn", LogLevel: "info"},
		{HTTPAddress: ":70000", DatabaseDSN: "dsn", LogLevel: "info"},
		{HTTPAddress: ":8080", DatabaseDSN: "dsn", LogLevel: "verbose"},
		{HTTPAddress: ":8080", DatabaseDSN: "", LogLevel: "info"},
	}
	for _, cfg := range tests {
		if err := cfg.Validate(); err == nil {
			t.Fatalf("expected validation error for %#v", cfg)
		}
	}
}

func TestBootstrapOverridesTakePrecedenceOverRemote(t *testing.T) {
	bootstrap := Bootstrap{
		HTTPAddressOverride: ":9090",
		LogLevelOverride:    "debug",
	}
	cfg := Config{HTTPAddress: ":8080", DatabaseDSN: "dsn", LogLevel: "info"}
	remote := remoteConfig{HTTPAddress: ":8181", LogLevel: "warn"}
	cfg = mergeConfig(cfg, remote, bootstrap)

	if cfg.HTTPAddress != ":9090" || cfg.LogLevel != "debug" {
		t.Fatalf("bootstrap overrides lost: %#v", cfg)
	}
}
