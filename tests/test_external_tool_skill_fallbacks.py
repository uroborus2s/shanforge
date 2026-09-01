from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read_skill(name: str) -> str:
    return (REPO_ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")


def test_art_asset_pipeline_does_not_require_missing_chroma_key_script() -> None:
    skill = read_skill("art-asset-pipeline")

    assert "`remove_chroma_key.py` 在本仓库中不存在" in skill
    assert "需要透明背景时，先确认" in skill
    assert "透明背景是交付必需项而能力不可用" in skill
    assert "tools/" not in skill
    assert "运行 `remove_chroma_key.py`" not in skill


def test_browser_control_probes_before_showing_cli_commands() -> None:
    skill = read_skill("browser-control")

    for phrase in (
        "能力探测",
        "browser-use CLI",
        "Codex Browser",
        "Codex Chrome",
        "Computer Use",
        "用户明确要求 `browser-use`",
        "不得改用其他工具",
        "所有入口均不可用",
        "仅在 `browser-use` CLI 已确认可用后",
    ):
        assert phrase in skill


def test_document_skills_fail_closed_when_no_real_entrypoint_exists() -> None:
    for name in ("docx", "pdf", "xlsx"):
        skill = read_skill(name)

        for phrase in (
            "能力探测",
            "仓内脚本",
            "已安装依赖",
            "当前会话专用工具",
            "missing_capability",
            "next_required_action",
            "已探测",
            "未执行",
        ):
            assert phrase in skill, (name, phrase)
