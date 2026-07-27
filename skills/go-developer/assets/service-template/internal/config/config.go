package config

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"os"
	"strconv"
	"strings"
	"time"

	consul "github.com/hashicorp/consul/api"
)

type Config struct {
	HTTPAddress string
	DatabaseDSN string
	LogLevel    string
}

type Bootstrap struct {
	ConsulAddress       string
	ConsulToken         string
	ConsulKey           string
	HTTPAddressOverride string
	LogLevelOverride    string
	DatabaseDSN         string
}

type remoteConfig struct {
	HTTPAddress string `json:"http_address"`
	LogLevel    string `json:"log_level"`
}

func LoadBootstrap() (Bootstrap, error) {
	bootstrap := Bootstrap{
		ConsulAddress:       os.Getenv("CONSUL_HTTP_ADDR"),
		ConsulToken:         os.Getenv("CONSUL_HTTP_TOKEN"),
		ConsulKey:           os.Getenv("CONSUL_KV_KEY"),
		HTTPAddressOverride: os.Getenv("HTTP_ADDRESS"),
		LogLevelOverride:    os.Getenv("LOG_LEVEL"),
		DatabaseDSN:         os.Getenv("DATABASE_DSN"),
	}
	if bootstrap.ConsulKey == "" {
		return Bootstrap{}, errors.New("CONSUL_KV_KEY is required")
	}
	if bootstrap.DatabaseDSN == "" {
		return Bootstrap{}, errors.New("DATABASE_DSN is required")
	}
	return bootstrap, nil
}

func Load(ctx context.Context, bootstrap Bootstrap) (Config, error) {
	cfg := Config{
		HTTPAddress: ":8080",
		DatabaseDSN: bootstrap.DatabaseDSN,
		LogLevel:    "info",
	}

	clientConfig := consul.DefaultConfig()
	if bootstrap.ConsulAddress != "" {
		clientConfig.Address = bootstrap.ConsulAddress
	}
	clientConfig.Token = bootstrap.ConsulToken
	client, err := consul.NewClient(clientConfig)
	if err != nil {
		return Config{}, fmt.Errorf("create Consul client: %w", err)
	}

	queryCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	pair, _, err := client.KV().Get(bootstrap.ConsulKey, (&consul.QueryOptions{}).WithContext(queryCtx))
	if err != nil {
		return Config{}, fmt.Errorf("read Consul key %q: %w", bootstrap.ConsulKey, err)
	}
	if pair == nil {
		return Config{}, fmt.Errorf("required Consul key %q does not exist", bootstrap.ConsulKey)
	}

	remote, err := decodeRemote(pair.Value)
	if err != nil {
		return Config{}, fmt.Errorf("decode Consul key %q: %w", bootstrap.ConsulKey, err)
	}
	cfg = mergeConfig(cfg, remote, bootstrap)
	if err := cfg.Validate(); err != nil {
		return Config{}, err
	}
	return cfg, nil
}

func mergeConfig(cfg Config, remote remoteConfig, bootstrap Bootstrap) Config {
	if remote.HTTPAddress != "" {
		cfg.HTTPAddress = remote.HTTPAddress
	}
	if remote.LogLevel != "" {
		cfg.LogLevel = remote.LogLevel
	}
	if bootstrap.HTTPAddressOverride != "" {
		cfg.HTTPAddress = bootstrap.HTTPAddressOverride
	}
	if bootstrap.LogLevelOverride != "" {
		cfg.LogLevel = bootstrap.LogLevelOverride
	}
	return cfg
}

func decodeRemote(value []byte) (remoteConfig, error) {
	decoder := json.NewDecoder(bytes.NewReader(value))
	decoder.DisallowUnknownFields()

	var remote remoteConfig
	if err := decoder.Decode(&remote); err != nil {
		return remoteConfig{}, err
	}
	if err := decoder.Decode(&struct{}{}); !errors.Is(err, io.EOF) {
		return remoteConfig{}, errors.New("remote config must contain exactly one JSON object")
	}
	return remote, nil
}

func (c Config) Validate() error {
	_, portText, err := net.SplitHostPort(c.HTTPAddress)
	if err != nil {
		return fmt.Errorf("validate HTTP address: %w", err)
	}
	port, err := strconv.Atoi(portText)
	if err != nil || port < 1 || port > 65535 {
		return fmt.Errorf("validate HTTP address: invalid port %q", portText)
	}

	switch strings.ToLower(c.LogLevel) {
	case "trace", "debug", "info", "warn", "error", "fatal", "panic":
	default:
		return fmt.Errorf("validate log level: unsupported value %q", c.LogLevel)
	}
	if c.DatabaseDSN == "" {
		return errors.New("DATABASE_DSN is required")
	}
	return nil
}
