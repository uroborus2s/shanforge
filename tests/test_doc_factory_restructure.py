from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]

DELETED_PATHS = (
    "docs/04-project-development/02-discovery/brainstorm-record.md",
    "docs/04-project-development/02-discovery/input.md",
    "docs/04-project-development/03-requirements/memory-system-business-requirements.md",
    "docs/04-project-development/03-requirements/process-workflow-contract-requirements.md",
    "docs/04-project-development/04-design/action-registry-and-autonomy-policy.md",
    "docs/04-project-development/04-design/architecture-layer-code-mapping.md",
    "docs/04-project-development/04-design/assets/v2-architecture-pages/index.md",
    "docs/04-project-development/04-design/backend-design.md",
    "docs/04-project-development/04-design/basic-capability-layer-design.md",
    "docs/04-project-development/04-design/core-subsystems.md",
    "docs/04-project-development/04-design/database-design.md",
    "docs/04-project-development/04-design/deployment-architecture.md",
    "docs/04-project-development/04-design/design-assets/writer-room-simulator.html",
    "docs/04-project-development/04-design/evaluation-summary-and-approval-reporting.md",
    "docs/04-project-development/04-design/frontend-adapters-and-multi-agent-coordination.md",
    "docs/04-project-development/04-design/memory-governance-design.md",
    "docs/04-project-development/04-design/skill-evolution-mechanism.md",
    "docs/04-project-development/04-design/source-docs-standard-upgrade-analysis.md",
    "docs/04-project-development/04-design/ux-ui-design.md",
    "docs/04-project-development/04-design/writer-room-simulator-design.md",
    "docs/04-project-development/05-development-process/memory-governance-implementation-plan.md",
    "docs/04-project-development/05-development-process/process-workflow-contract-implementation-plan.md",
    "docs/04-project-development/05-development-process/project-management-control-plane.md",
    "docs/04-project-development/05-development-process/software-development-process.md",
    "docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md",
    "docs/04-project-development/09-evolution/agent-motivation-autonomy-integration.md",
    "docs/04-project-development/09-evolution/retrospective.md",
    "docs/04-project-development/09-evolution/skill-evolution-plan.md",
    ".factory/design-assets.json",
    ".factory/process",
    ".factory/memory/history",
    ".factory/pm/generated",
)

ENTRYPOINTS = (
    "docs/index.md",
    "docs/05-design/index.md",
    "docs/document-index.md",
    ".factory/memory/doc-map.md",
    ".factory/project.json",
)


def read(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def walk_values(value: Any) -> list[Any]:
    if isinstance(value, dict):
        values: list[Any] = []
        for item in value.values():
            values.extend(walk_values(item))
        return values
    if isinstance(value, list):
        values = []
        for item in value:
            values.extend(walk_values(item))
        return values
    return [value]


def test_task_execution_contract_is_registered() -> None:
    docs_index = read("docs/index.md")
    design_index = read("docs/05-design/index.md")
    document_index = read("docs/document-index.md")
    doc_map = read(".factory/memory/doc-map.md")

    path = "05-design/workflow-execution-design.md"
    assert "05-design/index.md" in docs_index
    assert "./workflow-execution-design.md" in design_index
    assert f"docs/{path}" in document_index
    assert f"docs/{path}` -> `.factory/memory/tasks.summary.md`" in doc_map


def test_task_execution_contract_defines_six_task_types_and_gates() -> None:
    contract = read("docs/05-design/workflow-execution-design.md")
    architecture_pages = read("docs/05-design/system-architecture.md")

    for phrase in (
        "任务分解",
        "系统总设计",
        "模块设计",
        "UI 设计",
        "开发",
        "测试",
        "ready_for_review",
        "Review 不能替代 verification",
        "Verification 不能替代 human confirmation",
        ".factory/workitems/<WORKITEM-ID>/",
    ):
        assert phrase in contract

    assert "| 版本 | 修改内容 | 日期 | 修改人 | 审核 | 批准 |" in contract
    assert "| `0.1.0` | 初版，固化六类任务执行方式" in contract
    assert "| 项目负责人 |" in contract
    assert "| 项目负责人 |" in architecture_pages
    assert "Codex" not in contract
    assert "Codex" not in architecture_pages


def test_destructive_migration_removed_old_assets_and_structures() -> None:
    for path in DELETED_PATHS:
        assert not (REPO_ROOT / path).exists(), path


def test_current_entrypoints_do_not_reference_deleted_paths() -> None:
    for entrypoint in ENTRYPOINTS:
        content = read(entrypoint)
        for deleted_path in DELETED_PATHS:
            path_without_docs = deleted_path.removeprefix("docs/")
            assert deleted_path not in content
            assert path_without_docs not in content


def test_factory_readme_declares_destructive_boundaries() -> None:
    readme = read(".factory/README.md")

    for phrase in (
        "正式产品事实仍以 `docs/` 为人类可审计来源",
        "破坏性迁移规则",
        "只保留最新正式资产和正式内容",
        ".factory/workitems/",
        "执行审计事实",
        "不批量删除",
        "正式文档版本历史不得署名为 `Codex`",
    ):
        assert phrase in readme

    assert "优先采用非破坏性方式" not in readme


def test_design_asset_markdown_index_is_outside_assets() -> None:
    docs_index = read("docs/index.md")
    design_index = read("docs/05-design/index.md")
    document_index = read("docs/document-index.md")
    doc_map = read(".factory/memory/doc-map.md")

    new_path = "05-design/system-architecture.md"
    old_path = "docs/04-project-development/04-design/assets/v2-architecture-pages/index.md"

    assert "05-design/index.md" in docs_index
    assert "./system-architecture.md" in design_index
    assert f"docs/{new_path}" in document_index
    assert any(
        f"docs/{new_path}" in line and ".factory/memory/architecture.summary.md" in line
        for line in doc_map.splitlines()
    )
    assert not (REPO_ROOT / old_path).exists()


def test_formal_signatures_do_not_attribute_work_to_codex() -> None:
    formal_docs = (
        "docs/05-design/solution-overview.md",
        "docs/05-design/workflow-execution-design.md",
        "docs/06-delivery/test-plan.md",
        "docs/05-design/system-architecture.md",
    )
    forbidden = ("**负责人：** Codex", "**执行人：** Codex", "| Codex |")

    for path in formal_docs:
        content = read(path)
        for phrase in forbidden:
            assert phrase not in content


def test_current_factory_config_uses_project_owner_not_codex_signature() -> None:
    for path in (
        ".factory/project.json",
        ".factory/tech-profile.json",
        ".factory/multi-agent-board.json",
    ):
        data = json.loads(read(path))
        assert "Codex" not in walk_values(data)


def test_current_workitem_has_standard_artifacts() -> None:
    base = REPO_ROOT / ".factory/workitems/DOC-FACTORY-RESTRUCTURE-001"
    for relative in (
        "brief.md",
        "plan.md",
        "task-briefs/TASK-001-destructive-full-doc-migration.md",
        "evidence/TASK-001-verification.md",
        "reports/TASK-001-implementer-report.md",
        "reviews/TASK-001-review-input.md",
        "ledger.jsonl",
    ):
        assert (base / relative).is_file()

    assert not (base / "task-briefs/TASK-001-doc-factory-contract.md").exists()

    ledger = base / "ledger.jsonl"
    events = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    passed = [event for event in events if event.get("status") == "passed"]
    assert passed
    assert passed[-1]["next_required_action"] == "independent_review"
    assert {event["actor"] for event in events} == {"用户授权代执行"}
    assert passed[-1]["task"] == "TASK-001-destructive-full-doc-migration"
