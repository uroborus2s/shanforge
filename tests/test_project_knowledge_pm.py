from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from settings.project_knowledge.pm_projection import ProjectManagementProjector
from settings.project_knowledge.schema import create_schema

ROOT = Path(__file__).resolve().parents[1]
FIELD_MAP = (
    ROOT / ".factory/workitems/FLOW-CONTRACT-001/drafts/"
    "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
)


def connection() -> sqlite3.Connection:
    database = sqlite3.connect(":memory:")
    database.execute("PRAGMA foreign_keys=ON")
    create_schema(database)
    return database


def base_snapshot() -> dict[str, object]:
    return {
        "schema_id": "ProjectProgressSnapshot/v2",
        "project_id": "shanforge",
        "project": {
            "name": "Shanforge",
            "code": {"$state": "not_applicable"},
            "manager": None,
        },
        "sections": {
            "members": {
                "rows": [
                    {
                        "member_id": "uroborus",
                        "name": "Uroborus",
                        "project_role": "Owner",
                    }
                ]
            },
            "wbs": {"rows": []},
            "schedule": {"rows": []},
            "risks": {"rows": []},
            "communication": {"rows": []},
            "meetings": {"rows": []},
            "status_reports": {"rows": []},
            "changes": {"rows": []},
        },
    }


def test_projector_covers_137_fields_and_preserves_four_value_states() -> None:
    database = connection()
    result = ProjectManagementProjector(FIELD_MAP).project(
        base_snapshot(),
        database,
        generation_id="g1",
        source_manifest_sha256="a" * 64,
    )
    assert result.field_count == 137
    assert result.row_model_count == 13
    assert set(result.value_state_counts) == {
        "known",
        "unknown",
        "not_registered",
        "not_applicable",
    }
    row = database.execute(
        "SELECT project_name,field_values_json FROM pm_project_profile WHERE project_id='shanforge'"
    ).fetchone()
    assert row[0] == "Shanforge"
    values = json.loads(row[1])
    assert values["common.project_name"]["state"] == "known"
    assert values["common.project_name"]["label"] == "项目名称"
    assert values["common.project_manager"]["state"] == "unknown"
    assert values["common.prepared_by"]["state"] == "not_registered"
    assert values["common.project_code"]["state"] == "not_applicable"
    assert values["common.project_code"]["value"] is None

    party = database.execute(
        "SELECT party_kind,display_name,role_name,department,responsibility "
        "FROM pm_party WHERE party_id='pm-party:member:uroborus'"
    ).fetchone()
    assert party == ("member", "Uroborus", "Owner", None, None)


def test_projector_populates_typed_filter_sort_and_join_columns() -> None:
    snapshot = base_snapshot()
    snapshot["project"]["manager"] = "uroborus"  # type: ignore[index]
    snapshot["sections"]["schedule"]["rows"] = [  # type: ignore[index]
        {
            "record_id": "S-1",
            "name": "交付知识站点",
            "owner": "uroborus",
            "planned_start": "2026-07-20",
            "planned_finish": "2026-07-24",
            "actual_start": "2026-07-21",
            "variance_workdays": 1,
        }
    ]
    snapshot["sections"]["risks"]["rows"] = [  # type: ignore[index]
        {
            "risk_id": "R-1",
            "description": "索引可能过期",
            "probability": 0.2,
            "impact": "medium",
            "level": "medium",
            "response": "每次快照先检查来源",
            "owner": "uroborus",
            "status": "open",
        }
    ]
    snapshot["sections"]["communication"]["rows"] = [  # type: ignore[index]
        {
            "record_id": "C-1",
            "stakeholder": "uroborus",
            "required_information": "当前进度",
            "frequency": "weekly",
            "method": "会话",
            "owner": "uroborus",
            "next_at": "2026-07-29T09:00:00Z",
        }
    ]
    snapshot["sections"]["meetings"]["rows"] = [  # type: ignore[index]
        {
            "meeting_id": "M-1",
            "name": "项目复核",
            "convener": "uroborus",
            "date": "2026-07-22",
            "resolutions": ["关闭评审问题"],
            "actions": [
                {
                    "action_id": "A-1",
                    "description": "修复类型列",
                    "owner": "uroborus",
                    "due_at": "2026-07-22",
                    "status": "done",
                }
            ],
        }
    ]
    snapshot["sections"]["status_reports"]["rows"] = [  # type: ignore[index]
        {
            "report_id": "SR-1",
            "overall": "on_plan",
            "period": {"start": "2026-07-20", "end": "2026-07-22"},
            "current_deliverables": ["SQLite", "HTML"],
            "next_plan": ["复核"],
            "current_issues": ["性能"],
        }
    ]
    snapshot["sections"]["summary"] = {  # type: ignore[index]
        "project_id": "shanforge",
        "planned_results": "建立项目知识索引",
        "actual_results": "已生成只读站点",
        "time_variance": "无",
        "cost_variance": "不适用",
        "lessons": "派生缓存不进 Git",
        "actual_finish": "2026-07-22",
    }

    database = connection()
    ProjectManagementProjector(FIELD_MAP).project(
        snapshot,
        database,
        generation_id="g1",
        source_manifest_sha256="a" * 64,
    )

    profile = database.execute(
        "SELECT project_name,manager_party_id FROM pm_project_profile"
    ).fetchone()
    assert profile == ("Shanforge", "pm-party:member:uroborus")
    schedule = database.execute(
        "SELECT plan_kind,title,owner_party_id,planned_start,planned_end,actual_start,"
        "schedule_variance FROM pm_work_plan WHERE plan_item_id='pm-work-plan:schedule:S-1'"
    ).fetchone()
    assert schedule == (
        "schedule",
        "交付知识站点",
        "pm-party:member:uroborus",
        "2026-07-20",
        "2026-07-24",
        "2026-07-21",
        1.0,
    )
    risk = database.execute(
        "SELECT description,probability,impact,risk_level,owner_party_id,response_strategy,"
        "risk_status FROM pm_risk"
    ).fetchone()
    assert risk == (
        "索引可能过期",
        0.2,
        "medium",
        "medium",
        "pm-party:member:uroborus",
        "每次快照先检查来源",
        "open",
    )
    action = database.execute(
        "SELECT meeting_id,title,owner_party_id,due_at,action_status FROM pm_action_item"
    ).fetchone()
    assert action == (
        "pm-meeting:M-1",
        "修复类型列",
        "pm-party:member:uroborus",
        "2026-07-22",
        "done",
    )
    report = database.execute(
        "SELECT period_start,period_end,overall_status,highlights,next_steps,help_needed "
        "FROM pm_status_report"
    ).fetchone()
    assert report == (
        "2026-07-20",
        "2026-07-22",
        "on_plan",
        '["SQLite","HTML"]',
        '["复核"]',
        '["性能"]',
    )
    summary = database.execute(
        "SELECT scope_result,schedule_result,cost_result,delivery_result,lessons_learned,closed_at "
        "FROM pm_project_summary"
    ).fetchone()
    assert summary == (
        "建立项目知识索引",
        "无",
        "不适用",
        "已生成只读站点",
        "派生缓存不进 Git",
        "2026-07-22",
    )


def test_projector_rejects_duplicate_keys_missing_parent_and_invalid_types() -> None:
    projector = ProjectManagementProjector(FIELD_MAP)
    duplicate = base_snapshot()
    duplicate["sections"]["members"]["rows"].append(  # type: ignore[index]
        {"member_id": "uroborus", "name": "Duplicate"}
    )
    with pytest.raises(ValueError, match="target key collision"):
        projector.project(
            duplicate,
            connection(),
            generation_id="g1",
            source_manifest_sha256="a" * 64,
        )

    missing_parent = base_snapshot()
    missing_parent["sections"]["meetings"]["rows"] = [  # type: ignore[index]
        {"name": "Meeting", "actions": [{"action_id": "A-1", "description": "Do"}]}
    ]
    with pytest.raises(ValueError, match="required"):
        projector.project(
            missing_parent,
            connection(),
            generation_id="g1",
            source_manifest_sha256="a" * 64,
        )

    invalid_type = base_snapshot()
    invalid_type["project"]["name"] = 42  # type: ignore[index]
    with pytest.raises(ValueError, match="common.project_name"):
        projector.project(
            invalid_type,
            connection(),
            generation_id="g1",
            source_manifest_sha256="a" * 64,
        )


def test_projector_is_deterministic_and_does_not_create_history_rows() -> None:
    database = connection()
    projector = ProjectManagementProjector(FIELD_MAP)
    first = projector.project(
        base_snapshot(), database, generation_id="g1", source_manifest_sha256="a" * 64
    )
    second = projector.project(
        base_snapshot(), database, generation_id="g1", source_manifest_sha256="a" * 64
    )
    assert first.projection_sha256 == second.projection_sha256
    assert database.execute("SELECT COUNT(*) FROM pm_project_profile").fetchone()[0] == 1
