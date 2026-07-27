# 服务模板使用说明

模板位于 `assets/service-template/`，用于新项目的最小起点。已有项目沿用自己的目录和依赖管理。

## 模板内容

```text
service-template/
├── go.mod.tmpl
├── cmd/server/main.go
└── internal/
    ├── config/config.go
    ├── config/config_test.go
    ├── transport/http/router.go
    └── transport/http/router_test.go
```

## 渲染变量

| 变量 | 含义 | 示例 |
|---|---|---|
| `{{MODULE_PATH}}` | Go module path | `example.com/orders` |
| `{{GO_VERSION}}` | 已验证 Go 版本 | `1.26.1` |
| `{{GIN_VERSION}}` | Gin 固定版本 | `v1.12.0` |
| `{{LOGRUS_VERSION}}` | Logrus 固定版本 | `v1.9.4` |
| `{{GORM_VERSION}}` | GORM 固定版本 | `v1.31.2` |
| `{{GORM_POSTGRES_VERSION}}` | PostgreSQL driver 固定版本 | `v1.6.0` |
| `{{CONSUL_API_VERSION}}` | Consul API client 固定版本 | `v1.34.4` |

版本只是 2026-07-13 的验证快照。创建项目时应核对部署支持、官方发布和依赖兼容性，明确写入 `go.mod` 并提交 `go.sum`；不要在未验证时使用浮动 `latest`。

## 使用步骤

1. 复制模板到新项目。
2. 替换所有变量，确认没有残留 `{{...}}`。
3. 若物理数据库不是 PostgreSQL，替换 driver、DSN 和相应集成测试。
4. 运行 `go mod tidy`，审查 `go.mod` 和 `go.sum`。
5. 补业务 API、repository、迁移和配置 schema。
6. 运行 `gofmt`、`go vet ./...`、`go test ./...`。

模板只提供 composition、配置、日志、数据库和 HTTP 骨架，不提供认证、授权、业务模型、repository、迁移工具或部署文件；这些必须来自项目需求。日志和数据库装配保留在唯一入口，不为一次调用建立包装 package；`run` 只承担必须在 `os.Exit` 前关闭资源的进程生命周期边界。
