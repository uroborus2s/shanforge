"""Independent durable SQLite queue for project-state synchronization."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

from application.project_knowledge.sync_service import (
    LEASED_STATES,
    TRANSITION_BY_STATE_EVENT,
    ProjectStateSyncRequest,
    SyncClaim,
    SyncEnqueueReceipt,
    SyncEvent,
    SyncJob,
    SyncState,
)


def _time(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _request(value: str) -> ProjectStateSyncRequest:
    return ProjectStateSyncRequest(**json.loads(value))


class SQLiteProjectStateSyncStore:
    MAX_ATTEMPTS = 5

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS sync_jobs (
                    job_id TEXT PRIMARY KEY,
                    idempotency_key TEXT NOT NULL UNIQUE,
                    coalesce_scope TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    state TEXT NOT NULL,
                    attempt INTEGER NOT NULL DEFAULT 0 CHECK(attempt BETWEEN 0 AND 5),
                    available_at TEXT NOT NULL,
                    lease_owner TEXT,
                    lease_until TEXT,
                    fencing_token INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS sync_jobs_dispatch
                    ON sync_jobs(state, available_at, created_at);
                CREATE INDEX IF NOT EXISTS sync_jobs_scope
                    ON sync_jobs(coalesce_scope, state);
                CREATE TABLE IF NOT EXISTS sync_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT NOT NULL REFERENCES sync_jobs(job_id),
                    from_state TEXT NOT NULL,
                    event TEXT NOT NULL,
                    to_state TEXT NOT NULL,
                    occurred_at TEXT NOT NULL,
                    fencing_token INTEGER
                );
                CREATE TABLE IF NOT EXISTS sync_meta (
                    singleton INTEGER PRIMARY KEY CHECK(singleton = 1),
                    next_fencing_token INTEGER NOT NULL
                );
                INSERT OR IGNORE INTO sync_meta(singleton, next_fencing_token) VALUES(1, 1);
                """
            )

    def enqueue(self, request: ProjectStateSyncRequest, *, now: datetime) -> SyncEnqueueReceipt:
        current_time = _time(now)
        coalesce_scope = json.dumps(
            [request.source_scope, request.authorization_profile, request.generator_version],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        job_id = f"pss-{request.idempotency_key[:24]}"
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT job_id, state FROM sync_jobs WHERE idempotency_key = ?",
                (request.idempotency_key,),
            ).fetchone()
            if existing is not None:
                return SyncEnqueueReceipt(
                    "ProjectStateSyncEnqueueReceipt/v1",
                    str(existing["job_id"]),
                    SyncState(str(existing["state"])),
                    True,
                )
            older = connection.execute(
                """
                SELECT job_id, state FROM sync_jobs
                WHERE coalesce_scope = ? AND state IN ('queued', 'retryable_failed')
                ORDER BY created_at
                """,
                (coalesce_scope,),
            ).fetchall()
            for row in older:
                self._transition_in_connection(
                    connection,
                    str(row["job_id"]),
                    SyncEvent.INPUT_SUPERSEDED,
                    now=current_time,
                )
            connection.execute(
                """
                INSERT INTO sync_jobs(
                    job_id, idempotency_key, coalesce_scope, request_json, state,
                    available_at, created_at, updated_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    request.idempotency_key,
                    coalesce_scope,
                    request.to_json(),
                    SyncState.QUEUED.value,
                    current_time,
                    current_time,
                    current_time,
                ),
            )
        return SyncEnqueueReceipt(
            "ProjectStateSyncEnqueueReceipt/v1", job_id, SyncState.QUEUED, False
        )

    def claim(self, *, worker_id: str, now: datetime, lease_seconds: int) -> SyncClaim | None:
        if not worker_id or lease_seconds <= 0:
            raise ValueError("worker_id and positive lease_seconds are required")
        current_time = _time(now)
        lease_until = _time(now + timedelta(seconds=lease_seconds))
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT * FROM sync_jobs
                WHERE state = 'queued' AND available_at <= ? AND attempt < ?
                ORDER BY created_at, job_id LIMIT 1
                """,
                (current_time, self.MAX_ATTEMPTS),
            ).fetchone()
            if row is None:
                return None
            token_row = connection.execute(
                "SELECT next_fencing_token FROM sync_meta WHERE singleton = 1"
            ).fetchone()
            assert token_row is not None
            token = int(token_row[0])
            connection.execute(
                "UPDATE sync_meta SET next_fencing_token = ? WHERE singleton = 1",
                (token + 1,),
            )
            attempt = int(row["attempt"]) + 1
            connection.execute(
                """
                UPDATE sync_jobs SET attempt = ?, lease_owner = ?, lease_until = ?,
                    fencing_token = ?, updated_at = ? WHERE job_id = ?
                """,
                (attempt, worker_id, lease_until, token, current_time, row["job_id"]),
            )
            self._transition_in_connection(
                connection,
                str(row["job_id"]),
                SyncEvent.DISPATCHED,
                now=current_time,
                fencing_token=token,
            )
            return SyncClaim(str(row["job_id"]), _request(str(row["request_json"])), attempt, token)

    def apply_event(
        self,
        job_id: str,
        event: SyncEvent,
        *,
        now: datetime,
        worker_id: str | None = None,
        fencing_token: int | None = None,
    ) -> SyncState:
        current_time = _time(now)
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT * FROM sync_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            if row is None:
                raise KeyError(job_id)
            state = SyncState(str(row["state"]))
            if state in LEASED_STATES:
                if (
                    worker_id != row["lease_owner"]
                    or fencing_token != int(row["fencing_token"])
                    or row["lease_until"] is None
                    or str(row["lease_until"]) < current_time
                ):
                    raise PermissionError("lease or fencing token does not match")
            return self._transition_in_connection(
                connection,
                job_id,
                event,
                now=current_time,
                fencing_token=fencing_token,
            )

    def schedule_retry(self, job_id: str, *, now: datetime) -> SyncState:
        current_time = _time(now)
        with self.connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT state, attempt FROM sync_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
            if row is None:
                raise KeyError(job_id)
            if SyncState(str(row["state"])) is not SyncState.RETRYABLE_FAILED:
                raise ValueError("job is not retryable_failed")
            event = (
                SyncEvent.RETRY_BUDGET_AVAILABLE
                if int(row["attempt"]) < self.MAX_ATTEMPTS
                else SyncEvent.RETRY_BUDGET_EXHAUSTED
            )
            return self._transition_in_connection(connection, job_id, event, now=current_time)

    def get(self, job_id: str) -> SyncJob:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM sync_jobs WHERE job_id = ?", (job_id,)
            ).fetchone()
        if row is None:
            raise KeyError(job_id)
        return SyncJob(
            job_id=str(row["job_id"]),
            request=_request(str(row["request_json"])),
            state=SyncState(str(row["state"])),
            attempt=int(row["attempt"]),
            fencing_token=int(row["fencing_token"]),
        )

    def event_states(self, job_id: str) -> tuple[SyncState, ...]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT to_state FROM sync_events WHERE job_id = ? ORDER BY event_id",
                (job_id,),
            ).fetchall()
        return tuple(SyncState(str(row[0])) for row in rows)

    @staticmethod
    def _transition_in_connection(
        connection: sqlite3.Connection,
        job_id: str,
        event: SyncEvent,
        *,
        now: str,
        fencing_token: int | None = None,
    ) -> SyncState:
        row = connection.execute(
            "SELECT state FROM sync_jobs WHERE job_id = ?", (job_id,)
        ).fetchone()
        if row is None:
            raise KeyError(job_id)
        from_state = SyncState(str(row["state"]))
        transition = TRANSITION_BY_STATE_EVENT.get((from_state, event))
        if transition is None:
            raise ValueError(f"undeclared sync transition: {from_state.value}/{event.value}")
        clear_lease = transition.to_state not in LEASED_STATES
        connection.execute(
            """
            UPDATE sync_jobs SET state = ?, updated_at = ?,
                lease_owner = CASE WHEN ? THEN NULL ELSE lease_owner END,
                lease_until = CASE WHEN ? THEN NULL ELSE lease_until END
            WHERE job_id = ?
            """,
            (transition.to_state.value, now, clear_lease, clear_lease, job_id),
        )
        connection.execute(
            """
            INSERT INTO sync_events(job_id, from_state, event, to_state, occurred_at, fencing_token)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                from_state.value,
                event.value,
                transition.to_state.value,
                now,
                fencing_token,
            ),
        )
        return transition.to_state
