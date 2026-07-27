from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stratix-service"


def read(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_skill_bundles_norms_without_runtime_source_reading() -> None:
    skill = read("SKILL.md")
    runtime_paths = [
        SKILL_ROOT / "SKILL.md",
        *(
            path
            for root in ("agents", "references")
            for path in (SKILL_ROOT / root).rglob("*")
            if path.is_file()
        ),
    ]
    runtime_material = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in sorted(runtime_paths)
    )

    forbidden_patterns = (
        r"/Users/",
        r"packages/(?:create|core|forge|database|testing)/(?:src|templates)/",
        r"docs/03-developer-guide/",
    )
    forbidden_instructions = (
        "先读 [source locations",
        "再按任务回源",
        "回源对应源码",
        "处理其他版本时重新核对对应源码",
        "以目标版本的源码与类型为准",
    )

    assert all(re.search(pattern, runtime_material) is None for pattern in forbidden_patterns)
    assert all(instruction not in runtime_material for instruction in forbidden_instructions)
    assert any(path.name == "application-development.md" for path in runtime_paths)

    assert "references/application-development.md" in skill
    assert "业务项目直接遵循本 skill 的规范" in skill
    for package_version in (
        "@stratix/core@1.1.2",
        "@stratix/forge@1.1.4",
        "@stratix/create@1.1.2",
        "@stratix/database@1.1.1",
        "@stratix/testing@1.0.0-beta.1",
    ):
        assert package_version in skill

    for maintenance_detail in (
        "项目化执行时",
        "工作 Skill 回写契约",
        "框架源码只在维护本 skill",
        "work item evidence",
    ):
        assert maintenance_detail not in skill

    assert "references/source-locations.md" not in skill
    assert not (SKILL_ROOT / "references" / "source-locations.md").exists()


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
    assert '--key "$STRATIX_ENCRYPTION_KEY"' not in references
    assert "core 运行时直接把 key 字符串作为字节使用" not in references
