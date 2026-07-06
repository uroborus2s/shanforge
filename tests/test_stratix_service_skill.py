from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stratix-service"
OLD_SKILL_ROOT = REPO_ROOT / "skills" / "stratix-nodejs-backend"


def read_skill_file(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_skill_is_renamed_and_uses_current_toolchain() -> None:
    content = read_skill_file("SKILL.md")
    frontmatter = content.split("---", 2)[1]

    assert not OLD_SKILL_ROOT.exists()
    assert "name: stratix-service" in frontmatter
    assert "stratix-nodejs-backend" not in content
    assert "npm view @stratix/create dist-tags --json" in content
    assert "npm view @stratix/forge dist-tags --json" in content
    assert "项目实际安装版本" in content
    assert "create-stratix" in content
    assert "不再推荐旧的单包 `@stratix/cli`" in content
    assert "@stratix/cli@1.1.0" not in content


def test_cli_workflow_covers_obsync_root_and_end_to_end_development() -> None:
    content = read_skill_file("references/cli-workflow.md")

    for phrase in (
        "/Users/uroborus/NodeProject/wps/obsync-root",
        "pnpm run quality:release",
        "create-stratix app api demo-api",
        "create-stratix plugin data @demo/data-plugin",
        "stratix add preset database",
        "stratix generate business-repository workflow-execution",
        "stratix build-manifest --output .stratix/production-manifest.json",
        "stratix release gate --dry-run --manifest .stratix/production-manifest.json",
        "stratix openapi generate",
        "2026-07-05 历史兼容注记",
        "历史失败，不是永久结论",
        "2026-07-06 latest 复测",
        "@stratix/create@1.1.1",
        "@stratix/forge@1.1.3",
        "stratix.generated.js",
        "Found sensitive configuration environment variable",
    ):
        assert phrase in content


def test_plugin_selection_rejects_removed_tasks_preset() -> None:
    content = read_skill_file("references/ecosystem-map.md")

    for phrase in (
        "`@stratix/create`",
        "`@stratix/forge`",
        "`database`",
        "`redis`",
        "`queue`",
        "`ossp`",
        "`was-v7`",
        "`testing`",
        "`devtools`",
        "当前新项目不使用 `@stratix/tasks` preset",
    ):
        assert phrase in content


def test_sensitive_config_rules_are_explicit() -> None:
    content = read_skill_file("references/environment-config.md")

    for phrase in (
        "STRATIX_SENSITIVE_CONFIG",
        "STRATIX_ENCRYPTION_KEY",
        "生产环境不要依赖默认加密 key",
        "使用 32 字节原始字符串",
        "它不会在同一次调用中从 `.env.sensitive` 读出变量后再回头解密",
        "stratix config encrypt sensitive.prod.json --key",
        "stratix config decrypt \"$STRATIX_SENSITIVE_CONFIG\" --key",
    ):
        assert phrase in content


def test_generated_apps_must_use_encrypted_sensitive_config() -> None:
    skill = read_skill_file("SKILL.md")
    environment = read_skill_file("references/environment-config.md")
    scaffold = read_skill_file("references/scaffolds.md")
    references = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((SKILL_ROOT / "references").glob("*.md"))
    )

    for phrase in (
        "新生成应用的配置默认全部来自 `sensitiveConfig`",
        "不得用 `DB_HOST`、`REDIS_HOST`、`WPS_APP_SECRET`",
        "配置安全门",
        "不能完成加密、解密和注入验证时，结论只能是 blocked",
    ):
        assert phrase in skill

    for phrase in (
        "所有应用配置先写入 JSON，再加密成 `STRATIX_SENSITIVE_CONFIG`",
        "普通 `.env` 不承载应用配置",
        "server",
        "database",
        "redis",
    ):
        assert phrase in environment

    assert "process.env.DB_" not in scaffold
    assert "process.env.REDIS_" not in scaffold
    assert "process.env.HOST" not in scaffold
    assert "process.env.PORT" not in scaffold
    assert "const appConfig = sensitiveConfig.app" in scaffold

    for forbidden in (
        "DB_HOST",
        "DB_PORT",
        "DB_USERNAME",
        "REDIS_HOST",
        "WPS_APP_SECRET",
        "OSSP_SECRET_KEY",
        "UPSTREAM_URL",
        "配置文件可通过 `process.env` 读取",
    ):
        assert forbidden not in references


def test_cli_upgrade_guard_requires_live_capability_probe() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "如果 `create-stratix list` 或 `stratix list` 失败",
        "先查 npm dist-tags",
        "再查项目实际安装版本",
        "项目内优先使用 `pnpm exec stratix`",
        "先用 `--help` 或 npm 包版本确认新命令",
        "不得猜测 template、preset 或插件名",
        "只选择业务明确需要的插件",
    ):
        assert phrase in content

    assert "stratix config generate-key --length 32 --format hex" not in content


def test_default_api_examples_use_minimal_testing_preset() -> None:
    combined = "\n".join(
        read_skill_file(path)
        for path in ("SKILL.md", "references/cli-workflow.md", "references/scaffolds.md")
    )

    assert "create-stratix app api my-api --preset testing --no-install" in combined
    assert "create-stratix app api demo-api --preset testing --no-install" in combined
    assert "app api demo-api --preset database,testing" not in combined
    assert "app api my-api --preset database,testing" not in combined


def test_production_testing_requires_official_control_project() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "官方对照项目",
        "同一命令矩阵",
        "官方 latest 模板",
        "工具链或模板问题",
        "只有 skill 生成项目失败",
        "process.env.PORT",
        "sensitiveConfig",
        "全部新鲜通过",
    ):
        assert phrase in content


def test_latest_production_report_is_current_not_stale() -> None:
    content = read_skill_file("reports/production-readiness-report-2026-07-06.md")

    for phrase in (
        "Status: `blocked`",
        "@stratix/create@1.1.1",
        "@stratix/forge@1.1.3",
        "pnpm build",
        "release gate",
        "sensitiveConfig.server",
        "STRATIX_SENSITIVE_CONFIG",
        "stratix.generated.js",
        ".stratix/project.json",
    ):
        assert phrase in content


def test_production_gate_requires_start_and_runtime_injection() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "stratix start",
        "runtime injection",
        "全部新鲜通过",
        "才能声明生成应用可上线",
    ):
        assert phrase in content


def test_skill_applies_ponytail_minimalism_to_service_design() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "Ponytail 约束",
        "不为“以后可能”新增 preset、插件、配置、manager、helper、factory 或接口",
        "已有 controller / service / repository / BaseRepository / business-repository",
        "能靠数据库约束、Stratix 配置校验、Fastify schema 或 TypeScript 类型解决",
        "不简化安全边界、输入校验、数据一致性、敏感配置、错误处理和生产交付 gate",
        "不新增中间层",
    ):
        assert phrase in content


def test_openai_metadata_points_to_new_skill_name() -> None:
    content = read_skill_file("agents/openai.yaml")

    assert 'display_name: "Stratix Service"' in content
    assert "Use $stratix-service" in content
    assert "$stratix-nodejs-backend" not in content
    assert "do not use the removed tasks preset" in content
    for phrase in (
        "npm dist-tags",
        "project's installed @stratix/create",
        "--help",
        "list templates",
        "list presets",
        "STRATIX_SENSITIVE_CONFIG",
        "fresh doctor, test, build, manifest, release gate, openapi, start, "
        "decrypt, and runtime injection",
        "runtime injection cannot be verified",
        "blocked",
    ):
        assert phrase in content
