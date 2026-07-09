from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / "skills" / "spring-boot-development-standards" / "SKILL.md"


def read_skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_spring_boot_development_standards_skill_exists_and_triggers_on_stack() -> None:
    content = read_skill()
    frontmatter = content.split("---", 2)[1]

    assert "name: spring-boot-development-standards" in frontmatter
    assert "Spring Boot / Java 项目的技术开发规范" in frontmatter
    assert "Bug 根因调查仍由 systematic-debugging 接管" in frontmatter
    assert "controller      HTTP 入站" in content
    assert "application     用例编排" in content
    assert "domain          领域对象" in content
    assert "infrastructure  Repository" in content


def test_spring_boot_development_standards_applies_ponytail_rules() -> None:
    content = read_skill()

    for phrase in (
        "Ponytail 约束",
        "项目里是否已有工具方法、基类、配置或模式；先查再写",
        "禁止为了分段而写只被引用一次的 helper 方法",
        "禁止每个类都写自己的 `parse`、`format`、`convert`、`isEmpty`、`buildXxx` 等工具方法",
        "只要出现相同功能工具函数，就提升到最近公共 owner",
        "禁止把默认值、空对象、吞异常、重试、宽松解析或 fallback 当作 Bug 修复",
        "修 Bug 必须先找到直接原因、根源原因和证据",
        "禁止超过 3 层核心业务嵌套",
        "不简化输入校验、认证鉴权、事务一致性、数据完整性、错误处理和审计日志",
    ):
        assert phrase in content


def test_spring_boot_development_standards_allows_real_java_polymorphism_only() -> None:
    content = read_skill()

    for phrase in (
        "有真实可替换算法时，用策略模式",
        "有多个创建分支且调用方不该知道细节时，用工厂",
        "有领域事件或跨边界通知时，用观察者 / Spring event",
        "有类型差异行为时，用多态和动态绑定",
        "只有一个实现、一个调用方或没有变化轴时，不新增接口、抽象类或工厂",
        "模式引入后必须减少条件分支、重复代码或错误边界；否则删掉",
        "- skill: spring-boot-development-standards",
        "- status: ready_for_review | blocked | needs_user_input",
    ):
        assert phrase in content
