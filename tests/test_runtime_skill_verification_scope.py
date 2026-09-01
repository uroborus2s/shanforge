from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_python_verification_scope_is_risk_based_and_reports_full_suite_omissions() -> None:
    content = (REPO_ROOT / "skills/python-uv-project/SKILL.md").read_text(encoding="utf-8")

    for phrase in (
        "普通低、中风险改动",
        "受影响范围的 `pytest`",
        "受影响文件或目录的 Ruff",
        "涉及类型边界时运行必要的 `mypy`",
        "批次、里程碑、高风险、发布或项目既有 Gate 明确要求时",
        "完整 `pytest`、Ruff、mypy",
        "已运行范围",
        "未运行的全量项及原因",
        "定向通过不得表述为全量通过",
    ):
        assert phrase in content
