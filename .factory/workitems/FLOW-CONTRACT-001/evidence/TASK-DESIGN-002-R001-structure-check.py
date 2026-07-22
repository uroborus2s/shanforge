from __future__ import annotations

import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORK_ITEM = ROOT / ".factory/workitems/FLOW-CONTRACT-001"
CONTRACT = WORK_ITEM / "drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json"
PM_MAP = WORK_ITEM / "drafts/REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
DESIGN = WORK_ITEM / "drafts/DESIGN-PROJECT-KNOWLEDGE-001.R001.md"
PLAN = WORK_ITEM / "plans/TASK-IMPLEMENT-003-P001.md"
LEDGER = WORK_ITEM / "ledger.jsonl"


def read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


def main() -> None:
    contract = read_json(CONTRACT)
    pm_map = read_json(PM_MAP)
    design = DESIGN.read_text(encoding="utf-8")
    plan = PLAN.read_text(encoding="utf-8")

    requirements = contract["requirements"]
    nfrs = contract["nfrs"]
    assert isinstance(requirements, list) and len(requirements) == 16
    assert isinstance(nfrs, list) and len(nfrs) == 11
    acceptance_count = sum(len(item["acceptance_criteria"]) for item in requirements)
    assert acceptance_count == 64

    sqlite_schema = contract["sqlite_schema"]
    assert isinstance(sqlite_schema, dict)
    core_tables = sqlite_schema["knowledge_core_tables"]
    pm_tables = sqlite_schema["pm_projection_tables"]
    assert isinstance(core_tables, list) and len(core_tables) == 29
    assert isinstance(pm_tables, list) and len(pm_tables) == 10
    assert all(f"`{table}`" in design for table in core_tables + pm_tables)

    mappings = pm_map["mappings"]
    row_models = pm_map["row_models"]
    assert isinstance(mappings, list) and len(mappings) == 137
    assert len({item["field_id"] for item in mappings}) == 137
    assert isinstance(row_models, dict) and len(row_models) == 13
    assert row_models["project_summary"]["primary_key"] == ["summary_id"]
    base_keys = {
        "field_id",
        "source_snapshot_path",
        "source_type",
        "row_model",
        "target_kind",
        "value_owner",
        "history_policy",
        "target_key_formula",
        "source_nullable",
    }
    for mapping in mappings:
        assert base_keys <= set(mapping)
        if mapping["target_kind"] == "sqlite_projection":
            assert {"target_table", "target_column"} <= set(mapping)
        else:
            assert {"target_dto", "target_field"} <= set(mapping)

    design_markers = (
        "`source_section_key -> pk_document_section.section_key`",
        '"mdsec:" + sha256(JCS([document_id, section_id]))',
        "`summary_id PK`",
        "contribution_json",
        "ProjectStateSyncQueuePort",
        "project-state-sync.sqlite3",
        "project sync enqueue --head H --scope SCOPE",
        "documents/<id>.html",
        "quality/<id>.html",
        "versions/<id>.html",
        "project-management/<module>/<id>.html",
        "os.replace(current.next, current)",
        "10,000 Artifact",
        "零未处理 violation",
        "T05 不删除任何 legacy source",
    )
    assert all(marker in design for marker in design_markers)
    assert "section_key=<document_id>:<section_id>" not in design
    plan_markers = (
        "ProjectStateSyncQueuePort",
        "project-state-sync.sqlite3",
        "project sync enqueue --head H --scope SCOPE",
        "不依赖冻结 system-task ports",
        "T05 只在",
        "10k single-source",
        "ordinary sync",
        "known|unknown|not_registered|not_applicable",
    )
    assert all(marker in plan for marker in plan_markers)

    for placeholder in (
        "<功能名称>",
        "<WORKITEM-ID>",
        "exact/path",
        "后续实现",
        "补充测试",
        "适当错误处理",
    ):
        assert placeholder not in design
        assert placeholder not in plan

    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE VIRTUAL TABLE f USING fts5(x)")
    connection.execute("CREATE VIRTUAL TABLE t USING fts5(x, tokenize='trigram')")
    connection.close()

    for line_number, line in enumerate(LEDGER.read_text(encoding="utf-8").splitlines(), 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as error:
            raise AssertionError(f"invalid ledger JSON at line {line_number}") from error

    print("requirements=16 acceptance=64 nfr=11")
    print("schema=29+10 fts=2")
    print("pm_fields=137 unique row_models=13 summary_pk=summary_id")
    print("review_fix_markers=all_present placeholders=0 jsonl=valid sqlite_fts=ok")


if __name__ == "__main__":
    main()
