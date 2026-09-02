from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/writing-plans/scripts/validate_task_graph.py"


def test_task_graph_accepts_valid_dependencies_and_rejects_invalid_ones(tmp_path: Path) -> None:
    cases = {
        "valid": ("TASK-A|owner-a|none\nTASK-B|owner-b|TASK-A", 0),
        "diamond": (
            "TASK-A|owner-a|TASK-B,TASK-C\nTASK-B|owner-b|TASK-D\n"
            "TASK-C|owner-c|TASK-D\nTASK-D|owner-d|none",
            0,
        ),
        "missing-owner": ("TASK-A||none", 1),
        "unknown": ("TASK-A|owner-a|TASK-MISSING", 1),
        "self": ("TASK-A|owner-a|TASK-A", 1),
        "cycle": ("TASK-A|owner-a|TASK-B\nTASK-B|owner-b|TASK-A", 1),
    }
    for name, (tasks, expected_returncode) in cases.items():
        path = tmp_path / f"{name}.md"
        path.write_text(
            "\n".join(
                f"- task_card_id: {task}\n- owner: {owner}\n- depends_on: {depends_on}"
                for task, owner, depends_on in (line.split("|") for line in tasks.splitlines())
            ),
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(path)], text=True, capture_output=True
        )
        assert result.returncode == expected_returncode, result.stdout


def test_task_graph_rejects_duplicate_task_card_contract_mismatches(tmp_path: Path) -> None:
    plan = tmp_path / "plan.md"
    brief = tmp_path / "brief.md"
    plan.write_text(
        "- task_card_id: TASK-A\n- owner: owner-a\n- depends_on: TASK-B\n"
        "- task_card_id: TASK-B\n- owner: owner-b\n- depends_on: none\n",
        encoding="utf-8",
    )
    for name, text in {
        "owner": "- task_card_id: TASK-A\n- owner: owner-other\n- depends_on: TASK-B\n",
        "depends": "- task_card_id: TASK-A\n- owner: owner-a\n- depends_on: none\n",
    }.items():
        brief.write_text(text, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(plan), str(brief)], text=True, capture_output=True
        )
        assert result.returncode == 1, f"{name}: {result.stdout}"


def test_task_graph_accepts_rendered_plan_and_task_card_templates(tmp_path: Path) -> None:
    replacements = {
        "<WORKITEM-ID>": "WI-GRAPH",
        "<TASK-CARD-ID>": "WI-GRAPH-T01",
        "<WBS-ID>": "WBS-GRAPH-01",
        "<owner>": "graph-owner",
        "<TASK-CARD-ID,... | none>": "none",
    }
    paths = []
    for name in ("workitem-plan-template.md", "task-brief-template.md"):
        text = (ROOT / "skills/writing-plans/references" / name).read_text(encoding="utf-8")
        for source, target in replacements.items():
            text = text.replace(source, target)
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout
