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
    assert "@stratix/create@1.1.0" in content
    assert "@stratix/forge@1.1.0" in content
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


def test_openai_metadata_points_to_new_skill_name() -> None:
    content = read_skill_file("agents/openai.yaml")

    assert 'display_name: "Stratix Service"' in content
    assert "Use $stratix-service" in content
    assert "$stratix-nodejs-backend" not in content
    assert "do not use the removed tasks preset" in content
