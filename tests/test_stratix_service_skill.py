from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stratix-service"
OLD_SKILL_ROOT = REPO_ROOT / "skills" / "stratix-nodejs-backend"
CHECKER = REPO_ROOT / "skills/stratix-service/scripts/check_compatibility.py"


def write_fake_pnpm(path: Path, marker: Path, exit_code: int = 0) -> None:
    path.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\n' \"$*\" >> {marker}\n"
        f"exit {exit_code}\n",
        encoding="utf-8",
    )
    path.chmod(0o755)


def read_skill_file(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_skill_is_renamed_and_uses_current_toolchain() -> None:
    content = read_skill_file("SKILL.md")
    cli = read_skill_file("references/cli-workflow.md")
    frontmatter = content.split("---", 2)[1]

    assert not OLD_SKILL_ROOT.exists()
    assert "name: stratix-service" in frontmatter
    assert "stratix-nodejs-backend" not in content
    assert "npm view" not in cli
    assert "dist-tags" not in cli
    assert "业务项目直接遵循本规范，无需读取框架源码" in content
    assert "由本 skill 维护者更新规范" in content
    assert "create-stratix" in content
    assert "不使用旧单包 `@stratix/cli`" in cli


def test_cli_workflow_covers_project_end_to_end_development() -> None:
    content = read_skill_file("references/cli-workflow.md")

    for phrase in (
        "create-stratix app api demo-api",
        "create-stratix plugin data @demo/data-plugin",
        "stratix add preset database",
        "stratix generate business-repository workflow-execution",
        "stratix build-manifest --output .stratix/production-manifest.json",
        "stratix release gate --dry-run --manifest .stratix/production-manifest.json",
        "stratix openapi generate",
        "CLI 只从进程环境读取 key",
        "不接受 `--key`",
        "发布结论必须来自当前目标版本的新鲜执行",
    ):
        assert phrase in content

    assert "## 框架仓库" not in content


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
        "生产环境不允许 Core 回退到内置开发 key",
        "64 位 hex",
        "标准 base64",
        "同一次启动不会再回头解密",
        "required('STRATIX_ENCRYPTION_KEY')",
        "isTest()",
    ):
        assert phrase in content

    assert ' --key "$STRATIX_ENCRYPTION_KEY"' not in content


def test_generated_apps_must_use_encrypted_sensitive_config() -> None:
    skill = read_skill_file("SKILL.md")
    environment = read_skill_file("references/environment-config.md")
    application = read_skill_file("references/application-development.md")
    references = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((SKILL_ROOT / "references").glob("*.md"))
    )

    for phrase in (
        "敏感业务配置只从函数参数 `sensitiveConfig` 映射",
        "业务类不自行解密",
        "CLI 不接受 `--key`",
        "任一必需验证失败",
    ):
        assert phrase in skill

    for phrase in (
        "Forge 使用 STRATIX_ENCRYPTION_KEY 加密",
        "普通 `.env` 只保留启动所需进程变量",
        "server",
        "database",
    ):
        assert phrase in environment

    assert "sensitiveConfig.database" in application
    assert "process.env.DB_" not in references
    assert "process.env.REDIS_" not in references
    assert "process.env.PORT" not in references
    assert "process.env.WPS_APP_SECRET" not in references


def test_cli_upgrade_guard_requires_live_capability_probe() -> None:
    content = "\n".join(
        (
            read_skill_file("SKILL.md"),
            read_skill_file("references/cli-workflow.md"),
        )
    )

    for phrase in (
        "先查目标项目实际版本",
        "pnpm exec stratix --help",
        "pnpm exec stratix list templates",
        "pnpm exec stratix list presets",
        "不要假设这些包版本相同",
        "只选择真实需要的 template/preset",
    ):
        assert phrase in content

    assert "stratix config generate-key --length 32 --format base64" in content


def test_cli_creation_requires_a_verified_local_creator_and_fails_closed() -> None:
    content = read_skill_file("references/cli-workflow.md")

    for phrase in (
        "显式/已安装 CLI 和相关包版本",
        "`@stratix/create`: `1.1.2`",
        "未知或不兼容立即 `blocked`",
        "`detected`、`required`、`difference`",
        "未执行命令",
        "唯一 `next_required_action`",
        "不自动安装或升级",
        "不运行未固定版本的远端创建器",
        "已验证兼容的本地 `create-stratix`",
    ):
        assert phrase in content

    assert "npx create-stratix" not in content
    assert "npm view" not in content
    assert content.index("仅在上述创建门通过后") < content.index(
        "create-stratix list templates"
    )


def test_service_version_gate_fails_closed_without_a_compatible_package_matrix() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "## 版本兼容门",
        "`package.json`、lockfile 和已安装 `node_modules/@stratix/*/package.json`",
        "不能假设各包同版",
        "仅当每个相关包与本 skill 的支持矩阵兼容时",
        "未知或不匹配时，立即 `blocked`",
        "每个相关包的 `detected`、`required`、`difference`",
        "未执行命令",
        "唯一 `next_required_action`",
        "不自动安装或升级",
    ):
        assert phrase in content


def test_service_boundary_defers_admin_web_pages_to_admin_web_skill() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "Stratix `app web-admin`、`admin-page`、`admin-crud` 的前端页面",
        "交给 `stratix-admin-web`",
        "- work_item: <WORKITEM-ID or none>",
        "- ledger_event: <event id or none>",
    ):
        assert phrase in content

    assert "stratix generate admin-page user" not in content
    assert "stratix generate admin-crud user" not in content


def test_default_api_examples_use_minimal_testing_preset() -> None:
    combined = "\n".join(
        read_skill_file(path)
        for path in ("SKILL.md", "references/cli-workflow.md", "references/scaffolds.md")
    )

    assert "create-stratix app api demo-api --preset testing --no-install" in combined
    assert "app api demo-api --preset database,testing" not in combined


def test_implementation_uses_bundled_normative_contracts() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "规范入口",
        "application development",
        "业务项目直接遵循本 skill 的规范",
        "不要求业务项目读取 Stratix 框架源码",
        "repository -> service -> controller",
        "BaseRepository.query()",
    ):
        assert phrase in content

    assert "source-locations.md" not in content


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
        "真实 start",
        "runtime injection",
        "全部新鲜通过",
        "任一必需验证失败",
    ):
        assert phrase in content


def test_skill_applies_ponytail_minimalism_to_service_design() -> None:
    content = read_skill_file("SKILL.md")

    for phrase in (
        "最小实现",
        "只有 1–3 个简单资源时，不创建模块层或额外 domain abstraction",
        "领域规则有真实复用或复杂不变量时",
        "不新增 manager、factory、registry 或包装层",
        "不简化输入校验、敏感配置、数据一致性、错误处理和发布门",
    ):
        assert phrase in content


def test_openai_metadata_points_to_new_skill_name() -> None:
    content = read_skill_file("agents/openai.yaml")

    assert 'display_name: "Stratix Service"' in content
    assert "Use $stratix-service" in content
    assert "$stratix-nodejs-backend" not in content
    for phrase in (
        "bundled Stratix contracts",
        "config",
        "module",
        "three-layer",
        "Kysely",
    ):
        assert phrase in content


def test_version_gate_smoke_runs_real_cli_after_lock_compatibility() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        packages = {
            "@stratix/core": "1.1.2",
            "@stratix/forge": "1.1.4",
            "@stratix/create": "1.1.2",
            "@stratix/database": "1.1.1",
            "@stratix/testing": "1.0.0-beta.1",
        }
        (project / "package.json").write_text(
            json.dumps({"dependencies": packages}), encoding="utf-8"
        )
        (project / "pnpm-lock.yaml").write_text(
            "\n".join(f"  {name}@{version}: {{}}" for name, version in packages.items()),
            encoding="utf-8",
        )
        marker = project / "pnpm.calls"
        bin_dir = project / "bin"
        bin_dir.mkdir()
        write_fake_pnpm(bin_dir / "pnpm", marker)
        compatible = subprocess.run(
            [sys.executable, str(CHECKER), str(project)],
            text=True,
            capture_output=True,
            env={"PATH": str(bin_dir)},
        )
        assert compatible.returncode == 0, compatible.stdout
        assert marker.read_text(encoding="utf-8").splitlines() == [
            "exec stratix --help",
            "exec stratix doctor",
        ]


def test_version_gate_rejects_lock_mismatch_without_running_smoke() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        packages = {
            "@stratix/core": "1.1.2",
            "@stratix/forge": "1.1.4",
            "@stratix/create": "1.1.2",
            "@stratix/database": "1.1.1",
            "@stratix/testing": "1.0.0-beta.1",
        }
        (project / "package.json").write_text(
            json.dumps({"dependencies": packages}), encoding="utf-8"
        )
        (project / "pnpm-lock.yaml").write_text(
            "\n".join(
                f"  {name}@{'1.1.3' if name == '@stratix/core' else version}: {{}}"
                for name, version in packages.items()
            ),
            encoding="utf-8",
        )
        marker = project / "pnpm.calls"
        bin_dir = project / "bin"
        bin_dir.mkdir()
        write_fake_pnpm(bin_dir / "pnpm", marker)
        incompatible = subprocess.run(
            [sys.executable, str(CHECKER), str(project)],
            text=True,
            capture_output=True,
            env={"PATH": str(bin_dir)},
        )
        assert incompatible.returncode == 1
        assert "lock" in incompatible.stdout
        assert not marker.exists()


def test_cli_smoke_failure_fails_closed() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        packages = {
            "@stratix/core": "1.1.2",
            "@stratix/forge": "1.1.4",
            "@stratix/create": "1.1.2",
            "@stratix/database": "1.1.1",
            "@stratix/testing": "1.0.0-beta.1",
        }
        (project / "package.json").write_text(
            json.dumps({"dependencies": packages}), encoding="utf-8"
        )
        (project / "pnpm-lock.yaml").write_text(
            "\n".join(f"  {name}@{version}: {{}}" for name, version in packages.items()),
            encoding="utf-8",
        )
        marker = project / "pnpm.calls"
        bin_dir = project / "bin"
        bin_dir.mkdir()
        write_fake_pnpm(bin_dir / "pnpm", marker, exit_code=1)
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(project)],
            text=True,
            capture_output=True,
            env={"PATH": str(bin_dir)},
        )
        assert result.returncode == 1
        assert marker.read_text(encoding="utf-8").splitlines() == ["exec stratix --help"]


def test_version_gate_rejects_incompatible_package_fixture() -> None:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory)
        packages = {
            "@stratix/core": "1.1.2",
            "@stratix/forge": "1.1.4",
            "@stratix/create": "1.1.2",
            "@stratix/database": "1.1.1",
            "@stratix/testing": "1.0.0-beta.1",
        }
        (project / "package.json").write_text(
            json.dumps({"dependencies": packages}), encoding="utf-8"
        )
        (project / "pnpm-lock.yaml").write_text(
            "\n".join(f"  {name}@{version}: {{}}" for name, version in packages.items()),
            encoding="utf-8",
        )
        packages["@stratix/core"] = "1.1.3"
        (project / "package.json").write_text(
            json.dumps({"dependencies": packages}), encoding="utf-8"
        )
        incompatible = subprocess.run(
            [sys.executable, str(CHECKER), str(project)], text=True, capture_output=True
        )
        assert incompatible.returncode == 1
        assert "@stratix/core" in incompatible.stdout


def test_version_gate_rejects_non_object_dependency_map_without_traceback(tmp_path: Path) -> None:
    (tmp_path / "package.json").write_text(json.dumps({"dependencies": []}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(CHECKER), str(tmp_path)], text=True, capture_output=True
    )

    assert result.returncode == 1
    assert "dependencies must be an object" in result.stdout
    assert "Traceback" not in result.stderr
