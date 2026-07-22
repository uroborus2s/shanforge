from __future__ import annotations

import hashlib
import io
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from access.project_cli import run
from application.project_knowledge.sync_service import (
    PROJECT_STATE_SYNC_TRANSITIONS,
    ProjectStateSyncRequest,
    SyncEvent,
    SyncState,
)
from settings.project_knowledge.sync_store import SQLiteProjectStateSyncStore
from settings.project_knowledge.sync_worker import ProjectStateSyncWorker

NOW = datetime(2026, 7, 22, 8, 0, tzinfo=UTC)


def _request(head: str, *, authorized: bool = False) -> ProjectStateSyncRequest:
    return ProjectStateSyncRequest.create(
        fact_high_watermark=head,
        source_scope="project",
        authorization_profile="local-owner",
        generator_version="ProjectSiteRenderer/v2",
        commit_authorized=authorized,
        requested_at=NOW,
    )


def test_transition_model_exactly_matches_the_50_approved_contract_rows() -> None:
    contract_path = Path(
        ".factory/workitems/FLOW-CONTRACT-001/drafts/"
        "REQ-CHANGE-PROJECT-KNOWLEDGE-001.contract.R009.json"
    )
    approved = json.loads(contract_path.read_text(encoding="utf-8"))["system_task"]
    expected = {
        (row["from"], row["event"], row["to"], row["precondition"])
        for row in approved["transitions"]
    }
    actual = {
        (row.from_state.value, row.event.value, row.to_state.value, row.precondition)
        for row in PROJECT_STATE_SYNC_TRANSITIONS
    }
    assert len(actual) == 50
    assert actual == expected


def test_queue_is_independent_idempotent_superseding_and_fenced(tmp_path: Path) -> None:
    frozen = [
        Path("src/domain/system_tasks/models.py"),
        Path("src/settings/system_tasks/sqlite_store.py"),
    ]
    before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in frozen}
    store = SQLiteProjectStateSyncStore(tmp_path / "project-state-sync.sqlite3")

    first = store.enqueue(_request("head-1"), now=NOW)
    duplicate = store.enqueue(_request("head-1"), now=NOW)
    second = store.enqueue(_request("head-2"), now=NOW + timedelta(seconds=1))

    assert duplicate.job_id == first.job_id
    assert duplicate.coalesced is True
    assert store.get(first.job_id).state is SyncState.SUPERSEDED
    assert store.get(second.job_id).state is SyncState.QUEUED

    claim = store.claim(worker_id="worker-a", now=NOW + timedelta(seconds=2), lease_seconds=30)
    assert claim is not None and claim.job_id == second.job_id
    assert claim.fencing_token == 1
    with pytest.raises(PermissionError, match="fencing"):
        store.apply_event(
            second.job_id,
            SyncEvent.STAGE_SUCCEEDED,
            worker_id="worker-a",
            fencing_token=claim.fencing_token + 1,
            now=NOW + timedelta(seconds=3),
        )
    assert store.get(second.job_id).state is SyncState.RUNNING

    with store.connect() as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert "system_tasks" not in tables
    assert before == {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in frozen}


def test_retry_budget_is_bounded_at_five_attempts(tmp_path: Path) -> None:
    store = SQLiteProjectStateSyncStore(tmp_path / "queue.sqlite3")
    receipt = store.enqueue(_request("head-retry"), now=NOW)
    for attempt in range(1, 6):
        claim = store.claim(
            worker_id="worker-a",
            now=NOW + timedelta(minutes=attempt),
            lease_seconds=30,
        )
        assert claim is not None and claim.attempt == attempt
        store.apply_event(
            receipt.job_id,
            SyncEvent.TRANSIENT_FAILURE,
            worker_id="worker-a",
            fencing_token=claim.fencing_token,
            now=NOW + timedelta(minutes=attempt, seconds=1),
        )
        state = store.schedule_retry(
            receipt.job_id,
            now=NOW + timedelta(minutes=attempt, seconds=2),
        )
        assert state is (SyncState.QUEUED if attempt < 5 else SyncState.NEEDS_ATTENTION)


class _Stages:
    def __init__(self) -> None:
        self.commits = 0

    def project(self, request: ProjectStateSyncRequest) -> None:
        del request

    def update_memory(self, request: ProjectStateSyncRequest) -> None:
        del request

    def publish_html(self, request: ProjectStateSyncRequest) -> None:
        del request

    def has_maintenance_diff(self, request: ProjectStateSyncRequest) -> bool:
        del request
        return True

    def commit_maintenance(self, request: ProjectStateSyncRequest) -> None:
        del request
        self.commits += 1

    def integrate(self, request: ProjectStateSyncRequest) -> bool:
        del request
        return True

    def receipt_matches(self, request: ProjectStateSyncRequest) -> bool:
        del request
        return True


def test_worker_closes_commit_not_authorized_as_success_without_committing(tmp_path: Path) -> None:
    store = SQLiteProjectStateSyncStore(tmp_path / "queue.sqlite3")
    queued = store.enqueue(_request("head-worker", authorized=False), now=NOW)
    stages = _Stages()
    result = ProjectStateSyncWorker(store, stages).run_once(
        worker_id="isolated-worker",
        now=NOW + timedelta(seconds=1),
    )
    assert result is not None
    assert store.get(queued.job_id).state is SyncState.DONE
    assert stages.commits == 0
    assert SyncState.COMMIT_NOT_AUTHORIZED in result.visited_states


class _FakeApplication:
    def execute(self, command: str, **arguments: object) -> dict[str, object]:
        return {"command": command, **arguments}


def test_cli_sync_enqueue_returns_immediately_with_stable_arguments() -> None:
    stdout = io.StringIO()
    assert (
        run(
            [
                "project",
                "sync",
                "enqueue",
                "--head",
                "abc123",
                "--scope",
                "project",
                "--json",
            ],
            _FakeApplication(),
            stdout=stdout,
            stderr=io.StringIO(),
        )
        == 0
    )
    receipt = json.loads(stdout.getvalue())
    assert receipt["command"] == "sync.enqueue"
    assert receipt["data"] == {
        "command": "sync.enqueue",
        "head": "abc123",
        "scope": "project",
    }
