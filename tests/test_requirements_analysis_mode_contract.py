from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def test_requirements_analysis_is_mandatory_but_its_artifact_is_conditional() -> None:
    skill = read("skills/requirements-engineering/SKILL.md")
    prd_template = read("skills/requirements-engineering/references/prd-template.md")
    document_skill = read("skills/document-templates/SKILL.md")
    catalog = read("skills/document-templates/references/document-catalog.md")
    structure = read("skills/document-templates/references/repository-structure.md")
    gates = read("skills/document-templates/references/traceability-and-gates.md")
    standalone_template = read(
        "skills/document-templates/assets/templates/02-requirements/requirements-analysis.md"
    )

    for phrase in (
        "analysis_mode = embedded | standalone",
        "analysis_locator",
        "分析内容始终必做",
        "跨域",
        "高风险",
        "依赖复杂",
        "独立评审",
    ):
        assert phrase in skill

    assert "## 需求分析" in prd_template
    assert "analysis_mode: embedded" in prd_template
    assert "analysis_locator:" in prd_template
    assert "analysis_mode: standalone" in standalone_template
    assert "analysis_locator:" in standalone_template

    assert "分析内容必备，独立文件条件生成" in document_skill
    assert "| `requirements-analysis.md` | 条件 |" in catalog
    assert "requirements-analysis.md  # 条件" in structure
    assert "analysis_mode" in gates
    assert "analysis_locator" in gates
    assert "Gate 校验内容和定位" in gates
    assert "分析内容覆盖依赖、可行性、风险以及对设计和测试的影响" in gates
    assert "不再无条件要求 `requirements-analysis.md`" in gates
