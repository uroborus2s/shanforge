from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "go-developer"


def read(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_frontmatter_has_precise_go_stack_trigger() -> None:
    content = read("SKILL.md")
    frontmatter = content.split("---", 2)[1]

    assert "name: go-developer" in frontmatter
    for phrase in (
        "Go / Golang 后端工程开发 skill",
        "Gin",
        "GORM",
        "Logrus",
        "Consul",
        "非 Go 项目",
        "组合栈",
        "仅命中其中单个库",
    ):
        assert phrase in frontmatter


def test_main_entry_defines_boundaries_workflow_and_status() -> None:
    content = read("SKILL.md")

    for phrase in (
        "已有项目若采用其他框架或库，先遵守项目事实",
        "Gin + Zap",
        "GORM-only",
        "GORM 是数据访问工具，不是物理数据库",
        "Logrus 官方处于 maintenance mode",
        "gin.New()",
        "context.Context",
        "禁止服务启动时无条件 `AutoMigrate`",
        "Consul KV 不存放数据库密码",
        "signal-aware graceful shutdown",
        "needs_user_input",
        "ready_for_review",
        "- skill: go-developer",
    ):
        assert phrase in content


def test_verification_scope_is_risk_based_and_reports_full_suite_omissions() -> None:
    content = read("SKILL.md")

    for phrase in (
        "普通低、中风险改动",
        "仅对实际改动的 Go 文件运行 `gofmt`",
        "受影响包的 `go test`",
        "按风险和改动需要运行受影响包 `go vet`",
        "批次、里程碑、高风险、发布或项目既有 Gate 明确要求时",
        "`go test ./...`",
        "已运行范围",
        "未运行的全量项及原因",
        "定向通过不得表述为全量通过",
    ):
        assert phrase in content


def test_references_cover_go_engineering_and_fixed_stack_risks() -> None:
    engineering = read("references/engineering-standards.md")
    simplicity = read("references/simplicity-and-design.md")
    stack = read("references/stack-contract.md")
    sources = read("references/source-evaluation.md")

    for phrase in (
        "go.mod",
        "cmd/<service>/",
        "internal/",
        "context.Context",
        "errors.Is/As",
        "httptest",
        "go test -race ./...",
        "硬上限 3 层",
        "单一真实实现默认使用具体类型",
    ):
        assert phrase in engineering

    for phrase in (
        "Ponytail",
        "标准库",
        "只调用一次的私有函数或方法",
        "main -> run",
        "硬上限为 3 层",
        "不允许作者自行豁免硬上限",
        "函数 literal、callback、事务闭包和 goroutine",
        "前四项均无法满足",
        "Go 没有类继承",
        "Strategy",
        "至少两个真实算法",
        "Functional Options",
        "禁止推测性回退与兼容扩张",
        "dual-read",
        "失败后再试另一个地址",
        "未知字段与非法值必须失败",
    ):
        assert phrase in simplicity

    for phrase in (
        "ShouldBindJSON",
        "*gin.Context",
        "*logrus.Logger",
        "maintenance mode",
        "db.WithContext(ctx)",
        "db.Transaction",
        "SkipDefaultTransaction",
        "物理数据库选型",
        "github.com/hashicorp/consul/api",
        "last-known-good",
        "Consul KV 是配置和元数据 KV，不是业务数据库",
    ):
        assert phrase in stack

    for phrase in (
        "samber/cc-skills-golang",
        "2.5k stars",
        "没有 Gin 或 GORM 专用 skill",
        "Melkeydev/go-blueprint",
        "evrone/go-clean-template",
        "默认 Functional Options",
        "Go 不提供传统 class inheritance",
        "Logrus 官方明确处于 maintenance mode",
    ):
        assert phrase in sources


def test_service_template_is_minimal_pinned_and_composable() -> None:
    expected = {
        "go.mod.tmpl",
        "cmd/server/main.go",
        "internal/config/config.go",
        "internal/config/config_test.go",
        "internal/transport/http/router.go",
        "internal/transport/http/router_test.go",
    }
    template_root = SKILL_ROOT / "assets" / "service-template"
    actual = {
        str(path.relative_to(template_root)) for path in template_root.rglob("*") if path.is_file()
    }
    assert actual == expected

    module = read("assets/service-template/go.mod.tmpl")
    assert "@latest" not in module
    for dependency in (
        "github.com/gin-gonic/gin",
        "github.com/hashicorp/consul/api",
        "github.com/sirupsen/logrus",
        "gorm.io/driver/postgres",
        "gorm.io/gorm",
    ):
        assert dependency in module

    main = read("assets/service-template/cmd/server/main.go")
    router = read("assets/service-template/internal/transport/http/router.go")
    config = read("assets/service-template/internal/config/config.go")

    assert "signal.NotifyContext" in main
    assert "server.Shutdown" in main
    assert "func execute(" not in main
    assert "func serve(" not in main
    assert "gorm.Open" in main
    assert "PingContext" in main
    assert "SetMaxOpenConns" in main
    assert "gin.New()" in router
    assert "gin.Default()" not in router
    assert "gin.CustomRecoveryWithWriter(io.Discard" in router
    assert "CONSUL_HTTP_TOKEN" in config
    assert "DATABASE_DSN" in config
    assert "DisallowUnknownFields" in config
    assert "cfg.Validate()" in config
    assert "mergeConfig(cfg, remote, bootstrap)" in config
    assert 'WithField("panic", recovered)' not in router
    assert "panic(err)" not in main
    assert "os.Exit(1)" in main
    assert 'return fmt.Errorf("serve HTTP: %w", err)' in main
    assert 'logger.WithError(err).Error("service failed")' in main
    assert "_ = sqlDB.Close()" in main
    assert "fallback-" not in router
    assert "sync/atomic" not in router
    assert "http.StatusBadRequest" in router
    assert '"invalid_request_id"' in router
    assert 'case "trace", "debug", "info", "warn", "error"' in config
    assert '"warning"' not in config

    router_test = read("assets/service-template/internal/transport/http/router_test.go")
    config_test = read("assets/service-template/internal/config/config_test.go")
    assert "TestRecoveryDoesNotLogPanicValue" in router_test
    assert "TestInvalidRequestIDIsRejected" in router_test
    assert "TestDecodeRemoteRejectsUnknownFields" in config_test
    assert "TestConfigValidateRejectsInvalidValues" in config_test
    assert "TestBootstrapOverridesTakePrecedenceOverRemote" in config_test


def test_template_usage_requires_rendering_and_explicit_database_decision() -> None:
    usage = read("references/template-usage.md")

    for phrase in (
        "{{MODULE_PATH}}",
        "{{GO_VERSION}}",
        "不要在未验证时使用浮动 `latest`",
        "若物理数据库不是 PostgreSQL",
        "不提供认证、授权、业务模型、repository、迁移工具或部署文件",
        "不为一次调用建立包装 package",
    ):
        assert phrase in usage
