from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "java-developer"
OLD_SKILL = REPO_ROOT / "skills" / "spring-boot-development-standards" / "SKILL.md"


def read(path: str) -> str:
    return (SKILL_ROOT / path).read_text(encoding="utf-8")


def test_java_developer_replaces_long_spring_boot_skill_name() -> None:
    content = read("SKILL.md")
    frontmatter = content.split("---", 2)[1]

    assert not OLD_SKILL.exists()
    assert "name: java-developer" in frontmatter
    assert "Java / Spring Boot 工程开发 skill" in frontmatter
    assert "spring-boot-development-standards" not in content
    assert "- skill: java-developer" in content


def test_java_developer_main_entry_routes_by_stage_and_mode() -> None:
    content = read("SKILL.md")
    engineering = read("references/engineering-standards.md")

    for phrase in (
        "先判断当前阶段和工作方式",
        "references/engineering-standards.md",
        "需求 / 澄清",
        "技术设计",
        "Bug 修复",
        "重构",
        "代码评审",
        "工程规范",
        "Java 开发不是只看代码规范",
        "工作方式区分",
        "质量门",
    ):
        assert phrase in content or phrase in engineering


def test_java_developer_moves_code_and_document_standards_to_references() -> None:
    content = read("SKILL.md")
    code = read("references/code-standards.md")
    docs = read("references/documentation-standards.md")

    assert "references/code-standards.md" in content
    assert "references/documentation-standards.md" in content

    for phrase in (
        "Ponytail 约束",
        "禁止为了分段而写只被引用一次的 helper 方法",
        "禁止每个类都写自己的 `parse`、`format`、`convert`、`isEmpty`、`buildXxx` 等工具方法",
        "只要出现相同功能工具函数，就提升到最近公共 owner",
        "禁止把默认值、空对象、吞异常、重试、宽松解析或 fallback 当作 Bug 修复",
        "修 Bug 必须先找到直接原因、根源原因和证据",
        "禁止超过 3 层核心业务嵌套",
        "有真实可替换算法时，用策略模式",
        "有多个创建分支且调用方不该知道细节时，用工厂",
        "有领域事件或跨边界通知时，用观察者 / Spring event",
        "有类型差异行为时，用多态和动态绑定",
    ):
        assert phrase in code

    for phrase in (
        "Java 开发文档规范",
        "README",
        "API 说明",
        "开发说明",
        "变更记录",
        "Bug 修复文档必须写根因和验证",
        "文档 Review Checklist",
    ):
        assert phrase in docs
