from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stratix-service"


def read(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_skill_requires_source_backed_application_guide() -> None:
    skill = read("SKILL.md")
    sources = read("references/source-locations.md")

    assert "references/application-development.md" in skill
    assert "/Users/uroborus/NodeProject/wps/obsync-root" in sources
    for source in (
        "packages/create/src/template/generated-files.ts",
        "packages/forge/templates/resources/module",
        "packages/core/src/utils/environment/env.ts",
        "packages/database/src/config/base-repository.ts",
        "docs/03-developer-guide/应用后端开发/database-crud.md",
        "docs/03-developer-guide/应用后端开发/from-crud-to-modules.md",
    ):
        assert source in sources


def test_application_guide_has_current_stratix_config_template() -> None:
    guide = read("references/application-development.md")

    for phrase in (
        "src/stratix.config.ts",
        "fileURLToPath(new URL('.', import.meta.url))",
        "import databasePlugin from '@stratix/database'",
        "sensitiveConfig.database",
        "autoLoad: {}",
        "rootDir: sourceRoot",
        "routing: { enabled: true }",
    ):
        assert phrase in guide

    assert "applicationAutoDI" not in guide


def test_environment_guide_explains_key_and_test_mode_access() -> None:
    environment = read("references/environment-config.md")

    for phrase in (
        "required('STRATIX_ENCRYPTION_KEY')",
        "isTest()",
        "from '@stratix/core/environment'",
        "64 位 hex",
        "标准 base64",
        "不要通过命令行参数传密钥",
    ):
        assert phrase in environment

    assert ' --key "$STRATIX_ENCRYPTION_KEY"' not in environment


def test_application_guide_explains_generated_module_configuration() -> None:
    guide = read("references/application-development.md")

    for phrase in (
        "module.yaml",
        "不是运行时配置入口",
        "createModuleFixture",
        "fixture.manifest",
        "stratix doctor modules",
        "stratix graph modules --format mermaid",
        ".stratix/project.json",
    ):
        assert phrase in guide


def test_application_guide_traces_api_to_kysely_without_layer_leaks() -> None:
    guide = read("references/application-development.md")

    for phrase in (
        "@Get('/users',",
        "UserController",
        "@Service()",
        "UserService",
        "@Repository()",
        "UserRepository",
        "DatabaseConnectionProvider",
        "super({ database })",
        "this.query(async (db)",
        ".selectFrom(this.tableName)",
        "isLeft(result)",
        "return result.right",
    ):
        assert phrase in guide

    assert "Service 直接注入 `DatabaseConnectionProvider`" not in guide


def test_references_reject_removed_or_stale_configuration_contracts() -> None:
    references = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((SKILL_ROOT / "references").glob("*.md"))
    )

    assert "applicationAutoDI" not in references
    assert "--key \"$STRATIX_ENCRYPTION_KEY\"" not in references
    assert "core 运行时直接把 key 字符串作为字节使用" not in references
