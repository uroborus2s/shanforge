from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "stratix-admin-web"


def read_skill() -> str:
    return (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")


def test_frontmatter_and_registry_are_explicit() -> None:
    content = read_skill()
    frontmatter = content.split("---", 2)[1]

    assert "name: stratix-admin-web" in frontmatter
    assert "Stratix 管理后台前端开发规范" in frontmatter
    assert "web-admin" in frontmatter
    assert "admin CRUD" in frontmatter

    defaults = json.loads((REPO_ROOT / "config/software-factory.defaults.json").read_text())
    project = json.loads((REPO_ROOT / ".factory/project.json").read_text())
    for payload in (defaults, project):
        skills = {item["name"]: item for item in payload["shared_skills"]}
        assert skills["stratix-admin-web"]["path"] == "skills/stratix-admin-web/SKILL.md"


def test_development_order_requires_component_inventory_before_pages() -> None:
    content = read_skill()

    for phrase in (
        "先总结相似组件，再开发公共组件，再开发每个页面和页面逻辑",
        "梳理页面清单",
        "梳理组件清单",
        "先实现已确认会被两个以上页面复用的公共组件",
        "再逐页实现页面结构",
    ):
        assert phrase in content


def test_reuse_rules_include_ponytail_constraints() -> None:
    content = read_skill()

    for phrase in (
        "两个不同页面出现相同 UI 和交互契约时，提升到公共 UI 组件",
        "不写万能表格",
        "万能表单",
        "重复真实出现两次再抽",
        "不新增 UI 框架",
        "原生 HTML、CSS、浏览器能力和项目已有依赖优先",
        "只有一个页面使用",
        "抽出来会产生大量 boolean props",
    ):
        assert phrase in content


def test_stratix_web_admin_cli_and_security_boundaries_are_present() -> None:
    content = read_skill()

    for phrase in (
        "create-stratix app web-admin demo-admin --preset admin-mock,testing --no-install",
        "stratix generate admin-page user",
        "stratix generate admin-crud user",
        "`admin-mock` 只用于本地开发和测试",
        "前端不得写入密钥",
        "STRATIX_SENSITIVE_CONFIG",
    ):
        assert phrase in content


def test_output_contract_and_blocked_semantics_are_present() -> None:
    content = read_skill()

    for phrase in (
        "工作结果：",
        "- work_item: <WORKITEM-ID or none>",
        "- skill: stratix-admin-web",
        "- status: ready_for_review | blocked | needs_user_input",
        "页面清单和组件清单",
        "哪些重复 UI 被提升",
        "- ledger_event: <event id or none>",
        "`blocked` 用于缺页面清单",
        "`needs_user_input` 用于必须由用户决定后台信息架构",
    ):
        assert phrase in content


def test_admin_web_version_gate_fails_closed_before_generation() -> None:
    content = read_skill()

    for phrase in (
        "## 版本兼容门",
        "项目/生成器/CLI 版本与能力",
        "`package.json`、lockfile 和已安装包元数据",
        "`create-stratix --help`",
        "`pnpm exec stratix --help`",
        "未知或不兼容时，立即 `blocked`",
        "`detected`、`required`、`difference`",
        "未执行的生成命令",
        "唯一 `next_required_action`",
        "不自动安装或升级",
    ):
        assert phrase in content
