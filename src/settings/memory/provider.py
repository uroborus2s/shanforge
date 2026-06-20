from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Mapping
from urllib.parse import urlparse

from domain.memory.assembly_models import MemoryProviderBinding
from domain.memory.models import (
    DistillationResult,
    MemoryLifecycleApplyResult,
    MemoryStatus,
    RecallQuery,
)
from domain.memory.ports import MemoryProviderPort
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import SessionEvent
from settings.memory.remote_http_metadata import (
    RemoteHttpMetadataResolver,
    RemoteHttpRequestGovernance,
)
from settings.shared.jsonl import JsonlStore, parse_datetime
from settings.workspace.secret_catalog import LocalSecretCatalogProvider


@dataclass(slots=True)
class NullMemoryProvider(MemoryProviderPort):
    """Default no-op provider that preserves local-first memory behavior."""

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        return None

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        return ""

    def sync_turn(
        self,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None:
        return None

    def on_session_end(
        self,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None:
        return None

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None:
        return None

    def on_delegation(self, digest: SubAgentDigest) -> None:
        return None

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "null",
        }


@dataclass(slots=True)
class InMemoryAugmentationMemoryProvider(MemoryProviderPort):
    """In-memory external provider stub used for local governance tests."""

    default_recall_block: str = "Remember the external memory guidance."
    initialized_bindings: dict[str, MemoryProviderBinding] = field(default_factory=dict)
    synced_events: dict[str, tuple[tuple[str, ...], ...]] = field(default_factory=dict)
    ended_sessions: dict[str, DistillationResult] = field(default_factory=dict)
    lifecycle_apply_results: dict[str, tuple[MemoryLifecycleApplyResult, ...]] = field(
        default_factory=dict
    )
    delegated_digests: dict[str, tuple[SubAgentDigest, ...]] = field(default_factory=dict)

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        self.initialized_bindings[session_id] = binding

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        binding = self.initialized_bindings.get(session_id)
        if binding is None:
            return self.default_recall_block
        recall_block = binding.metadata.get("recall_block")
        return str(recall_block or self.default_recall_block)

    def sync_turn(
        self,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None:
        existing = list(self.synced_events.get(session_id, ()))
        existing.append(tuple(event.id for event in latest_events))
        self.synced_events[session_id] = tuple(existing)

    def on_session_end(
        self,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None:
        self.ended_sessions[session_id] = distillation_result

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None:
        existing = list(self.lifecycle_apply_results.get(session_id, ()))
        existing.append(apply_result)
        self.lifecycle_apply_results[session_id] = tuple(existing)

    def on_delegation(self, digest: SubAgentDigest) -> None:
        existing = list(self.delegated_digests.get(digest.parent_session_id, ()))
        existing.append(digest)
        self.delegated_digests[digest.parent_session_id] = tuple(existing)

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
        }


@dataclass(slots=True, frozen=True)
class _ProviderSnapshotRecord:
    id: str
    session_id: str
    record_id: str
    app_id: str | None
    workflow_id: str | None
    title: str
    body: str
    confidence: float
    created_at: datetime


@dataclass(slots=True, frozen=True)
class _ProviderTurnRecord:
    id: str
    session_id: str
    event_ids: tuple[str, ...]
    summaries: tuple[str, ...]
    created_at: datetime


@dataclass(slots=True, frozen=True)
class _ProviderDigestRecord:
    id: str
    parent_session_id: str
    child_session_id: str
    summary: str
    created_at: datetime


@dataclass(slots=True, frozen=True)
class _PrefetchHit:
    id: str
    source_kind: str
    title: str
    snippet: str
    score: float
    provenance: dict[str, Any] = field(default_factory=dict)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _tokenize_text(payload: str | None) -> tuple[str, ...]:
    return tuple(token for token in re.findall(r"[a-z0-9]+", str(payload or "").lower()))


def _score_text(query_tokens: tuple[str, ...], payload: str | None) -> float:
    if not query_tokens:
        return 0.0
    candidate_tokens = set(_tokenize_text(payload))
    if not candidate_tokens:
        return 0.0
    overlap = sum(1 for token in dict.fromkeys(query_tokens) if token in candidate_tokens)
    return overlap / max(len(dict.fromkeys(query_tokens)), 1)


def _prefetch_query_terms(
    query: RecallQuery,
    *,
    max_terms: int = 12,
) -> tuple[str, ...]:
    return _tokenize_text(query.query_text or f"{query.app_id} {query.workflow_id}")[:max_terms]


def _build_prefetch_budget_trace(
    *,
    query: RecallQuery,
    provider_limit: int | None,
    candidate_hit_count: int,
    selected_hit_count: int,
    selected_hit_ids: tuple[str, ...] = (),
    selection_strategy: str,
    rank_trace_count: int,
) -> dict[str, Any]:
    return {
        "requested_limit": query.limit,
        "provider_limit": provider_limit,
        "query_text_present": bool(str(query.query_text or "").strip()),
        "candidate_hit_count": candidate_hit_count,
        "selected_hit_count": selected_hit_count,
        "selected_hit_ids": selected_hit_ids,
        "selection_strategy": selection_strategy,
        "rank_trace_count": rank_trace_count,
        "rank_trace_truncated": rank_trace_count < candidate_hit_count,
    }


def _build_prefetch_rank_trace(
    hits: tuple[_PrefetchHit, ...],
    *,
    selected_hit_count: int,
    selected_reason: str,
    overflow_reason: str,
    max_entries: int = 12,
) -> tuple[dict[str, Any], ...]:
    capped_hits = hits[:max_entries]
    selected_limit = min(max(selected_hit_count, 0), len(hits))
    trace: list[dict[str, Any]] = []
    for rank_position, hit in enumerate(capped_hits):
        selected = rank_position < selected_limit
        trace.append(
            {
                "rank_position": rank_position,
                "hit_id": hit.id,
                "source_kind": hit.source_kind,
                "selected": selected,
                "selection_reason": selected_reason if selected else overflow_reason,
                "score": hit.score,
            }
        )
    return tuple(trace)


def _compact_mapping(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        str(key): value
        for key, value in payload.items()
        if value not in (None, "", (), {})
    }


def _build_prefetch_hit_provenance(
    hits: tuple[_PrefetchHit, ...],
    *,
    max_entries: int = 12,
) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "hit_id": hit.id,
            "source_kind": hit.source_kind,
            **_compact_mapping(dict(hit.provenance)),
        }
        for hit in hits[:max_entries]
    )


def _build_contract_trace(
    contract_metadata: dict[str, Any],
    *,
    response_contract: str | None = None,
    response_contract_source: str | None = None,
    response_keys: tuple[str, ...] = (),
    response_validation_error: str | None = None,
) -> dict[str, Any]:
    return _compact_mapping(
        {
            "bridge_kind": contract_metadata.get("bridge_kind"),
            "provider_kind": contract_metadata.get("provider_kind"),
            "storage_kind": contract_metadata.get("storage_kind"),
            "retrieval_kind": contract_metadata.get("retrieval_kind"),
            "contract_ready": contract_metadata.get("contract_ready"),
            "response_contract": response_contract,
            "response_contract_source": response_contract_source,
            "response_keys": response_keys,
            "response_validation_error": response_validation_error,
        }
    )


def _build_access_trace(
    *,
    access_kind: str,
    access_ref: str,
    attempt_count: int = 1,
    auth_kind: str = "none",
    request_header_names: tuple[str, ...] = (),
    signature_key_id: str | None = None,
    signature_key_selection_source: str | None = None,
    bearer_token_id: str | None = None,
    bearer_token_selection_source: str | None = None,
    secret_catalog_source_path: str | None = None,
    timeout_seconds: float | None = None,
    max_retries: int | None = None,
    retry_status_codes: tuple[int, ...] = (),
    retry_backoff_seconds: float | None = None,
    status_code: int | None = None,
) -> dict[str, Any]:
    return _compact_mapping(
        {
            "access_kind": access_kind,
            "access_ref": access_ref,
            "attempt_count": attempt_count,
            "auth_kind": auth_kind,
            "request_header_names": request_header_names,
            "signature_key_id": signature_key_id,
            "signature_key_selection_source": signature_key_selection_source,
            "bearer_token_id": bearer_token_id,
            "bearer_token_selection_source": bearer_token_selection_source,
            "secret_catalog_source_path": secret_catalog_source_path,
            "timeout_seconds": timeout_seconds,
            "max_retries": max_retries,
            "retry_status_codes": retry_status_codes,
            "retry_backoff_seconds": retry_backoff_seconds,
            "status_code": status_code,
        }
    )


def _build_writeback_trace(
    *,
    supported: bool,
    configured: bool,
    session_writable: bool,
    reports: dict[str, Any],
) -> dict[str, Any]:
    trace = {
        "supported": supported,
        "configured": configured,
        "session_writable": session_writable,
        "enabled": configured and session_writable,
        "detail_reports": dict(reports),
    }
    successes = _summarize_writeback_reports(reports, "success")
    if successes:
        trace["successes"] = successes
    failure_policies = _summarize_writeback_reports(reports, "failure_policy")
    if failure_policies:
        trace["failure_policies"] = failure_policies
    response_oks = _summarize_writeback_reports(reports, "response_ok")
    if response_oks:
        trace["response_oks"] = response_oks
    response_statuses = _summarize_writeback_reports(reports, "response_status")
    if response_statuses:
        trace["response_statuses"] = response_statuses
    response_messages = _summarize_writeback_reports(reports, "response_message")
    if response_messages:
        trace["response_messages"] = response_messages
    response_report_ids = _summarize_writeback_reports(reports, "response_report_id")
    if response_report_ids:
        trace["response_report_ids"] = response_report_ids
    response_validation_errors = _summarize_writeback_reports(
        reports,
        "response_validation_error",
    )
    if response_validation_errors:
        trace["response_validation_errors"] = response_validation_errors
    return trace


def _summarize_writeback_reports(
    reports: Mapping[str, Any],
    field: str,
) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for request_kind, report in reports.items():
        if not isinstance(report, Mapping):
            continue
        value = report.get(field)
        if value not in (None, "", (), {}):
            values[str(request_kind)] = value
    return values


def _deserialize_snapshot_record(payload: dict[str, Any]) -> _ProviderSnapshotRecord:
    return _ProviderSnapshotRecord(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        record_id=str(payload["record_id"]),
        app_id=str(payload.get("app_id") or "") or None,
        workflow_id=str(payload.get("workflow_id") or "") or None,
        title=str(payload["title"]),
        body=str(payload["body"]),
        confidence=float(payload.get("confidence", 0.0)),
        created_at=parse_datetime(str(payload["created_at"])),
    )


def _deserialize_turn_record(payload: dict[str, Any]) -> _ProviderTurnRecord:
    return _ProviderTurnRecord(
        id=str(payload["id"]),
        session_id=str(payload["session_id"]),
        event_ids=tuple(str(item) for item in payload.get("event_ids", ())),
        summaries=tuple(str(item) for item in payload.get("summaries", ())),
        created_at=parse_datetime(str(payload["created_at"])),
    )


def _deserialize_digest_record(payload: dict[str, Any]) -> _ProviderDigestRecord:
    return _ProviderDigestRecord(
        id=str(payload["id"]),
        parent_session_id=str(payload["parent_session_id"]),
        child_session_id=str(payload["child_session_id"]),
        summary=str(payload["summary"]),
        created_at=parse_datetime(str(payload["created_at"])),
    )


class _JsonlProviderStore(JsonlStore):
    def __init__(self, root: str | Path, filename: str) -> None:
        super().__init__(root=root, filename=filename)


@dataclass(slots=True)
class JsonlAugmentationMemoryProvider(MemoryProviderPort):
    """Durable external memory provider backed by provider-owned JSONL state."""

    root: str | Path
    default_recall_block: str = "Remember the external memory guidance."
    max_prefetch_entries: int = 4
    initialized_bindings: dict[str, MemoryProviderBinding] = field(default_factory=dict)
    last_prefetch_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    _snapshot_store: _JsonlProviderStore | None = field(init=False, default=None, repr=False)
    _turn_store: _JsonlProviderStore | None = field(init=False, default=None, repr=False)
    _digest_store: _JsonlProviderStore | None = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self.root = Path(self.root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self._snapshot_store = _JsonlProviderStore(self.root, "memory-provider-snapshots.jsonl")
        self._turn_store = _JsonlProviderStore(self.root, "memory-provider-turns.jsonl")
        self._digest_store = _JsonlProviderStore(self.root, "memory-provider-digests.jsonl")

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        self.initialized_bindings[session_id] = binding

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        binding = self.initialized_bindings.get(session_id)
        recall_parts: list[str] = []
        if binding is not None:
            configured = str(binding.metadata.get("recall_block") or "").strip()
            if configured:
                recall_parts.append(configured)
        elif self.default_recall_block:
            recall_parts.append(self.default_recall_block)
        snapshots = self._snapshot_store.read_all(_deserialize_snapshot_record)
        matching = [
            record
            for record in snapshots
            if (
                record.app_id in {None, query.app_id}
                or record.workflow_id in {None, query.workflow_id}
            )
        ]
        matching.sort(key=lambda record: (-record.confidence, record.created_at, record.id))
        query_terms = _prefetch_query_terms(query)
        all_hits = tuple(
            _PrefetchHit(
                id=record.id,
                source_kind="snapshot",
                title=record.title,
                snippet=record.body,
                score=record.confidence,
                provenance=_compact_mapping(
                    {
                        "origin_kind": "provider_snapshot",
                        "session_id": record.session_id,
                        "record_id": record.record_id,
                        "app_id": record.app_id,
                        "workflow_id": record.workflow_id,
                    }
                ),
            )
            for record in matching
        )
        selected = matching[: self.max_prefetch_entries]
        selected_hits = all_hits[: self.max_prefetch_entries]
        rank_trace = _build_prefetch_rank_trace(
            all_hits,
            selected_hit_count=len(selected_hits),
            selected_reason="provider_window",
            overflow_reason="provider_overflow",
        )
        contract_trace = _build_contract_trace(self.contract_metadata())
        access_trace = _build_access_trace(
            access_kind="state_root",
            access_ref=str(self.root),
        )
        writeback_trace = _build_writeback_trace(
            supported=True,
            configured=True,
            session_writable=bool(binding and binding.writable),
            reports={},
        )
        self.last_prefetch_reports[session_id] = {
            "hit_count": len(selected),
            "hit_ids": tuple(record.id for record in selected),
            "query_text_present": bool(str(query.query_text or "").strip()),
            "query_terms": query_terms,
            "source_breakdown": {"snapshot": len(selected)} if selected else {},
            "result_truncated": len(matching) > self.max_prefetch_entries,
            "budget_trace": _build_prefetch_budget_trace(
                query=query,
                provider_limit=self.max_prefetch_entries,
                candidate_hit_count=len(all_hits),
                selected_hit_count=len(selected_hits),
                selected_hit_ids=tuple(hit.id for hit in selected_hits),
                selection_strategy="provider_window_confidence_recency",
                rank_trace_count=len(rank_trace),
            ),
            "rank_trace": rank_trace,
            "hit_provenance": _build_prefetch_hit_provenance(all_hits),
            "contract_trace": contract_trace,
            "access_trace": access_trace,
            "writeback_trace": writeback_trace,
        }
        if matching:
            recall_parts.append("Durable provider snapshots:")
            recall_parts.extend(
                f"- {record.title}: {record.body}"
                for record in selected
            )
        return "\n".join(part for part in recall_parts if part).strip()

    def sync_turn(
        self,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None:
        if not latest_events:
            return
        record = _ProviderTurnRecord(
            id=f"{session_id}:{len(latest_events)}:{latest_events[-1].id}",
            session_id=session_id,
            event_ids=tuple(event.id for event in latest_events),
            summaries=tuple(event.summary for event in latest_events),
            created_at=_utcnow(),
        )
        self._turn_store.replace_or_append(record.id, _serialize_dataclass(record))

    def on_session_end(
        self,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None:
        for record in distillation_result.promoted_records:
            snapshot = _ProviderSnapshotRecord(
                id=f"{session_id}:{record.id}",
                session_id=session_id,
                record_id=record.id,
                app_id=str(record.metadata.get("app_id") or "") or None,
                workflow_id=str(record.metadata.get("workflow_id") or "") or None,
                title=record.title,
                body=record.body,
                confidence=record.confidence,
                created_at=_utcnow(),
            )
            self._snapshot_store.replace_or_append(snapshot.id, _serialize_dataclass(snapshot))

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None:
        records_by_id = {record.id: record for record in apply_result.updated_records}
        if not records_by_id:
            return
        snapshots = self._snapshot_store.read_all(_deserialize_snapshot_record)
        existing_snapshot_ids = {
            snapshot.record_id: snapshot.id
            for snapshot in snapshots
            if snapshot.record_id in records_by_id
        }
        for record_id, record in records_by_id.items():
            snapshot_id = existing_snapshot_ids.get(record_id, f"{session_id}:{record_id}")
            if record.status is MemoryStatus.ACCEPTED:
                snapshot = _ProviderSnapshotRecord(
                    id=snapshot_id,
                    session_id=session_id,
                    record_id=record.id,
                    app_id=str(record.metadata.get("app_id") or "") or None,
                    workflow_id=str(record.metadata.get("workflow_id") or "") or None,
                    title=record.title,
                    body=record.body,
                    confidence=record.confidence,
                    created_at=_utcnow(),
                )
                self._snapshot_store.replace_or_append(
                    snapshot.id,
                    _serialize_dataclass(snapshot),
                )
            elif record_id in existing_snapshot_ids:
                self._snapshot_store.remove(existing_snapshot_ids[record_id])

    def on_delegation(self, digest: SubAgentDigest) -> None:
        record = _ProviderDigestRecord(
            id=f"{digest.parent_session_id}:{digest.child_session_id}",
            parent_session_id=digest.parent_session_id,
            child_session_id=digest.child_session_id,
            summary=digest.summary,
            created_at=_utcnow(),
        )
        self._digest_store.replace_or_append(record.id, _serialize_dataclass(record))

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "storage_kind": "jsonl",
            "retrieval_kind": "snapshot",
            "state_root": str(self.root),
        }

    def prefetch_diagnostics(self, session_id: str) -> dict[str, Any]:
        return dict(self.last_prefetch_reports.get(session_id, {}))


@dataclass(slots=True)
class JsonlVectorAugmentationMemoryProvider(JsonlAugmentationMemoryProvider):
    """Durable provider that ranks provider-owned snapshots/turns/digests by query overlap."""

    max_query_terms: int = 12

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        binding = self.initialized_bindings.get(session_id)
        recall_parts: list[str] = []
        if binding is not None:
            configured = str(binding.metadata.get("recall_block") or "").strip()
            if configured:
                recall_parts.append(configured)
        elif self.default_recall_block:
            recall_parts.append(self.default_recall_block)

        query_tokens = _prefetch_query_terms(query, max_terms=self.max_query_terms)
        all_hits = self._collect_hits(query, query_tokens)
        hits = all_hits[: self.max_prefetch_entries]
        rank_trace = _build_prefetch_rank_trace(
            all_hits,
            selected_hit_count=len(hits),
            selected_reason="provider_window",
            overflow_reason="provider_overflow",
        )
        contract_trace = _build_contract_trace(self.contract_metadata())
        access_trace = _build_access_trace(
            access_kind="state_root",
            access_ref=str(self.root),
        )
        writeback_trace = _build_writeback_trace(
            supported=True,
            configured=True,
            session_writable=bool(binding and binding.writable),
            reports={},
        )
        self.last_prefetch_reports[session_id] = {
            "hit_count": len(hits),
            "hit_ids": tuple(hit.id for hit in hits),
            "query_text_present": bool(str(query.query_text or "").strip()),
            "query_terms": query_tokens,
            "source_breakdown": self._source_breakdown(hits),
            "result_truncated": len(all_hits) > self.max_prefetch_entries,
            "budget_trace": _build_prefetch_budget_trace(
                query=query,
                provider_limit=self.max_prefetch_entries,
                candidate_hit_count=len(all_hits),
                selected_hit_count=len(hits),
                selected_hit_ids=tuple(hit.id for hit in hits),
                selection_strategy="provider_window_query_overlap",
                rank_trace_count=len(rank_trace),
            ),
            "rank_trace": rank_trace,
            "hit_provenance": _build_prefetch_hit_provenance(all_hits),
            "contract_trace": contract_trace,
            "access_trace": access_trace,
            "writeback_trace": writeback_trace,
        }
        if hits:
            recall_parts.append("Vector augmentation hits:")
            recall_parts.extend(
                f"- [{hit.source_kind}] {hit.title}: {hit.snippet}"
                for hit in hits[: self.max_prefetch_entries]
            )
        return "\n".join(part for part in recall_parts if part).strip()

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "local",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "storage_kind": "jsonl",
            "retrieval_kind": "vector",
            "state_root": str(self.root),
        }

    def _collect_hits(
        self,
        query: RecallQuery,
        query_tokens: tuple[str, ...],
    ) -> tuple[_PrefetchHit, ...]:
        hits: list[_PrefetchHit] = []
        snapshots = self._snapshot_store.read_all(_deserialize_snapshot_record)
        for record in snapshots:
            if not (
                record.app_id in {None, query.app_id}
                or record.workflow_id in {None, query.workflow_id}
            ):
                continue
            score = _score_text(query_tokens, f"{record.title}\n{record.body}") + record.confidence
            if query_tokens and score <= record.confidence:
                continue
            hits.append(
                _PrefetchHit(
                    id=record.id,
                    source_kind="snapshot",
                    title=record.title,
                    snippet=record.body,
                    score=score,
                    provenance=_compact_mapping(
                        {
                            "origin_kind": "provider_snapshot",
                            "session_id": record.session_id,
                            "record_id": record.record_id,
                            "app_id": record.app_id,
                            "workflow_id": record.workflow_id,
                        }
                    ),
                )
            )
        turns = self._turn_store.read_all(_deserialize_turn_record)
        for record in turns:
            snippet = " ".join(record.summaries)
            score = _score_text(query_tokens, snippet)
            if query_tokens and score <= 0:
                continue
            hits.append(
                _PrefetchHit(
                    id=record.id,
                    source_kind="turn",
                    title=f"Session {record.session_id} turns",
                    snippet=snippet,
                    score=score,
                    provenance=_compact_mapping(
                        {
                            "origin_kind": "provider_turn",
                            "session_id": record.session_id,
                            "event_ids": record.event_ids,
                        }
                    ),
                )
            )
        digests = self._digest_store.read_all(_deserialize_digest_record)
        for record in digests:
            score = _score_text(query_tokens, record.summary)
            if query_tokens and score <= 0:
                continue
            hits.append(
                _PrefetchHit(
                    id=record.id,
                    source_kind="delegation",
                    title=f"Child digest {record.child_session_id}",
                    snippet=record.summary,
                    score=score,
                    provenance=_compact_mapping(
                        {
                            "origin_kind": "provider_delegation_digest",
                            "parent_session_id": record.parent_session_id,
                            "child_session_id": record.child_session_id,
                        }
                    ),
                )
            )
        hits.sort(key=lambda hit: (-hit.score, hit.source_kind, hit.id))
        return tuple(hits)

    @staticmethod
    def _source_breakdown(hits: tuple[_PrefetchHit, ...]) -> dict[str, int]:
        breakdown: dict[str, int] = {}
        for hit in hits:
            breakdown[hit.source_kind] = breakdown.get(hit.source_kind, 0) + 1
        return breakdown


@dataclass(slots=True)
class RemoteAugmentationMemoryProvider(MemoryProviderPort):
    """Remote external provider bridge backed by the settings-layer HTTP client."""

    PREFETCH_RESPONSE_CONTRACT: ClassVar[str] = "remote_memory_prefetch_v1"
    WRITEBACK_RESPONSE_CONTRACT: ClassVar[str] = "remote_memory_writeback_ack_v1"

    http_client: Any
    default_endpoint_url: str | None = None
    default_sync_endpoint_url: str | None = None
    default_session_end_endpoint_url: str | None = None
    default_lifecycle_apply_endpoint_url: str | None = None
    default_delegation_endpoint_url: str | None = None
    default_recall_block: str = ""
    secret_catalog_provider: LocalSecretCatalogProvider = field(
        default_factory=LocalSecretCatalogProvider
    )
    metadata_resolver: RemoteHttpMetadataResolver = field(
        default_factory=RemoteHttpMetadataResolver
    )
    initialized_bindings: dict[str, MemoryProviderBinding] = field(default_factory=dict)
    last_prefetch_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    last_writeback_reports: dict[str, dict[str, Any]] = field(default_factory=dict)

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        self.initialized_bindings[session_id] = binding
        self.last_writeback_reports.setdefault(session_id, {})

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        binding = self.initialized_bindings.get(session_id)
        recall_parts: list[str] = []
        metadata = binding.metadata if binding is not None else {}
        query_terms = _prefetch_query_terms(query)
        governance = self.metadata_resolver.resolve_prefetch_governance(
            metadata,
            default_endpoint_url=self.default_endpoint_url,
            default_contract=self.PREFETCH_RESPONSE_CONTRACT,
            secret_catalog_provider=self.secret_catalog_provider,
        )
        endpoint_url = governance.endpoint_url
        validation_mode = governance.response_validation_mode
        validation_errors: tuple[str, ...] = ()
        hits: tuple[_PrefetchHit, ...] = ()
        if binding is not None:
            configured = str(binding.metadata.get("recall_block") or "").strip()
            if configured:
                recall_parts.append(configured)
        elif self.default_recall_block:
            recall_parts.append(self.default_recall_block)

        response: dict[str, Any] = {}
        if endpoint_url:
            payload = self.http_client.request(
                "GET",
                endpoint_url,
                payload={
                    "session_id": query.session_id,
                    "app_id": query.app_id,
                    "workflow_id": query.workflow_id,
                    "query_text": query.query_text,
                    "limit": query.limit,
                },
                options=governance.request_options,
            )
            response = dict(payload)
            remote_block, hits, validation_errors = self._normalize_prefetch_response(
                response,
                validation_mode=validation_mode,
            )
            if remote_block:
                recall_parts.append(remote_block)
        transport_report = self._transport_report()
        response_summary = self._summarize_prefetch_response(
            response,
            contract_id=governance.response_contract,
            contract_source=governance.response_contract_source,
        )
        rank_trace = _build_prefetch_rank_trace(
            hits,
            selected_hit_count=len(hits),
            selected_reason="remote_response_order",
            overflow_reason="remote_response_overflow",
        )
        request_header_names = tuple(
            str(name) for name in transport_report.get("request_header_names", ())
        )
        response_validation_error = (
            "; ".join(validation_errors)
            if validation_errors and validation_mode == "record"
            else None
        )
        writeback_enabled = self.metadata_resolver.writeback_enabled(
            metadata,
            default_sync_endpoint_url=self.default_sync_endpoint_url,
            default_session_end_endpoint_url=self.default_session_end_endpoint_url,
            default_lifecycle_apply_endpoint_url=self.default_lifecycle_apply_endpoint_url,
            default_delegation_endpoint_url=self.default_delegation_endpoint_url,
        )
        writeback_reports = dict(self.last_writeback_reports.get(session_id, {}))
        contract_trace = _build_contract_trace(
            self.contract_metadata(),
            response_contract=str(response_summary.get("response_contract") or "") or None,
            response_contract_source=str(response_summary.get("response_contract_source") or "")
            or None,
            response_keys=tuple(str(key) for key in response_summary.get("response_keys", ())),
            response_validation_error=response_validation_error,
        )
        access_trace = _build_access_trace(
            access_kind="endpoint_url",
            access_ref=endpoint_url,
            attempt_count=int(transport_report.get("attempt_count", 1) or 1),
            auth_kind=str(transport_report.get("auth_kind") or "none"),
            request_header_names=request_header_names,
            signature_key_id=str(transport_report.get("signature_key_id") or "") or None,
            signature_key_selection_source=(
                str(transport_report.get("signature_key_selection_source") or "") or None
            ),
            bearer_token_id=str(transport_report.get("bearer_token_id") or "") or None,
            bearer_token_selection_source=(
                str(transport_report.get("bearer_token_selection_source") or "") or None
            ),
            secret_catalog_source_path=(
                str(transport_report.get("secret_catalog_source_path") or "") or None
            ),
            timeout_seconds=(
                float(transport_report["timeout_seconds"])
                if transport_report.get("timeout_seconds") is not None
                else None
            ),
            max_retries=(
                int(transport_report["max_retries"])
                if transport_report.get("max_retries") is not None
                else None
            ),
            retry_status_codes=tuple(
                int(code) for code in transport_report.get("retry_status_codes", ())
            ),
            retry_backoff_seconds=(
                float(transport_report["retry_backoff_seconds"])
                if transport_report.get("retry_backoff_seconds") is not None
                else None
            ),
            status_code=(
                int(transport_report["status_code"])
                if transport_report.get("status_code") is not None
                else None
            ),
        )
        writeback_trace = _build_writeback_trace(
            supported=True,
            configured=bool(writeback_enabled),
            session_writable=bool(binding and binding.writable),
            reports=writeback_reports,
        )
        self.last_prefetch_reports[session_id] = {
            "hit_count": len(hits),
            "hit_ids": tuple(hit.id for hit in hits),
            "query_text_present": bool(str(query.query_text or "").strip()),
            "query_terms": query_terms,
            "source_breakdown": self._source_breakdown(hits),
            "result_truncated": False,
            "budget_trace": _build_prefetch_budget_trace(
                query=query,
                provider_limit=None,
                candidate_hit_count=len(hits),
                selected_hit_count=len(hits),
                selected_hit_ids=tuple(hit.id for hit in hits),
                selection_strategy="remote_response_order",
                rank_trace_count=len(rank_trace),
            ),
            "rank_trace": rank_trace,
            "hit_provenance": _build_prefetch_hit_provenance(hits),
            "signature_key_id": transport_report.get("signature_key_id"),
            "signature_key_selection_source": transport_report.get(
                "signature_key_selection_source"
            ),
            "bearer_token_id": transport_report.get("bearer_token_id"),
            "bearer_token_selection_source": transport_report.get(
                "bearer_token_selection_source"
            ),
            "secret_catalog_source_path": transport_report.get("secret_catalog_source_path"),
            "timeout_seconds": transport_report.get("timeout_seconds"),
            "max_retries": transport_report.get("max_retries"),
            "retry_status_codes": transport_report.get("retry_status_codes"),
            "retry_backoff_seconds": transport_report.get("retry_backoff_seconds"),
            "contract_trace": contract_trace,
            "access_trace": access_trace,
            "writeback_trace": writeback_trace,
        }
        if response_validation_error is not None:
            self.last_prefetch_reports[session_id]["response_validation_error"] = (
                response_validation_error
            )
        if hits:
            recall_parts.append("Remote augmentation hits:")
            recall_parts.extend(
                f"- [{hit.source_kind}] {hit.title}: {hit.snippet}"
                for hit in hits
            )
        return "\n".join(part for part in recall_parts if part).strip()

    def sync_turn(
        self,
        session_id: str,
        latest_events: tuple[SessionEvent, ...],
    ) -> None:
        if not latest_events:
            return None
        binding = self.initialized_bindings.get(session_id)
        governance = self.metadata_resolver.resolve_writeback_governance(
            binding.metadata if binding is not None else {},
            request_kind="sync",
            default_endpoint_url=self.default_sync_endpoint_url,
            default_contract=self.WRITEBACK_RESPONSE_CONTRACT,
            secret_catalog_provider=self.secret_catalog_provider,
        )
        if not governance.endpoint_url:
            return None
        self._perform_writeback(
            session_id=session_id,
            governance=governance,
            payload={
                "session_id": session_id,
                "events": [
                    {
                        "id": event.id,
                        "type": event.type,
                        "summary": event.summary,
                        "payload": dict(event.payload),
                    }
                    for event in latest_events
                ],
            },
        )
        return None

    def on_session_end(
        self,
        session_id: str,
        distillation_result: DistillationResult,
    ) -> None:
        binding = self.initialized_bindings.get(session_id)
        governance = self.metadata_resolver.resolve_writeback_governance(
            binding.metadata if binding is not None else {},
            request_kind="session_end",
            default_endpoint_url=self.default_session_end_endpoint_url,
            default_contract=self.WRITEBACK_RESPONSE_CONTRACT,
            secret_catalog_provider=self.secret_catalog_provider,
        )
        if not governance.endpoint_url:
            return None
        self._perform_writeback(
            session_id=session_id,
            governance=governance,
            payload={
                "session_id": session_id,
                "promoted_records": [
                    {
                        "id": record.id,
                        "title": record.title,
                        "scope": str(record.scope),
                        "confidence": record.confidence,
                    }
                    for record in distillation_result.promoted_records
                ],
                "promotion_decisions": [
                    {
                        "candidate_id": decision.candidate_id,
                        "status": str(decision.status),
                        "reason": decision.reason,
                    }
                    for decision in distillation_result.promotion_decisions
                ],
                "candidate_count": len(distillation_result.candidates),
            },
        )
        return None

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: MemoryLifecycleApplyResult,
    ) -> None:
        binding = self.initialized_bindings.get(session_id)
        governance = self.metadata_resolver.resolve_writeback_governance(
            binding.metadata if binding is not None else {},
            request_kind="lifecycle_apply",
            default_endpoint_url=self.default_lifecycle_apply_endpoint_url,
            default_contract=self.WRITEBACK_RESPONSE_CONTRACT,
            secret_catalog_provider=self.secret_catalog_provider,
        )
        if not governance.endpoint_url:
            return None
        self._perform_writeback(
            session_id=session_id,
            governance=governance,
            payload={
                "session_id": session_id,
                "actor": apply_result.actor,
                "selected_record_ids": list(apply_result.selected_record_ids),
                "applied_record_ids": list(apply_result.applied_record_ids),
                "skipped_record_ids": list(apply_result.skipped_record_ids),
                "updated_records": [
                    {
                        "id": record.id,
                        "title": record.title,
                        "scope": str(record.scope),
                        "status": str(record.status),
                        "confidence": record.confidence,
                    }
                    for record in apply_result.updated_records
                ],
                "evaluations": [
                    {
                        "record_id": evaluation.record_id,
                        "current_status": str(evaluation.current_status),
                        "effective_status": str(evaluation.effective_status),
                        "reason": evaluation.reason,
                        "hidden": evaluation.hidden,
                        "allowed": evaluation.allowed,
                    }
                    for evaluation in apply_result.evaluations
                ],
                "queue_filter": (
                    {
                        "actionable_only": apply_result.queue_filter.actionable_only,
                        "include_hidden": apply_result.queue_filter.include_hidden,
                        "reasons": list(apply_result.queue_filter.reasons),
                        "effective_statuses": [
                            str(status) for status in apply_result.queue_filter.effective_statuses
                        ],
                        "current_statuses": [
                            str(status) for status in apply_result.queue_filter.current_statuses
                        ],
                        "limit": apply_result.queue_filter.limit,
                    }
                    if apply_result.queue_filter is not None
                    else None
                ),
            },
        )
        return None

    def on_delegation(self, digest: SubAgentDigest) -> None:
        binding = self.initialized_bindings.get(digest.parent_session_id)
        governance = self.metadata_resolver.resolve_writeback_governance(
            binding.metadata if binding is not None else {},
            request_kind="delegation",
            default_endpoint_url=self.default_delegation_endpoint_url,
            default_contract=self.WRITEBACK_RESPONSE_CONTRACT,
            secret_catalog_provider=self.secret_catalog_provider,
        )
        if not governance.endpoint_url:
            return None
        self._perform_writeback(
            session_id=digest.parent_session_id,
            governance=governance,
            payload={
                "parent_session_id": digest.parent_session_id,
                "child_session_id": digest.child_session_id,
                "summary": digest.summary,
                "responsibility_scope": list(digest.responsibility_scope),
                "evidence_refs": list(digest.evidence_refs),
                "metadata": dict(digest.metadata),
            },
        )
        return None

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "remote",
            "contract_ready": True,
            "provider_kind": "augmentation",
            "retrieval_kind": "remote_http",
            "writeback_supported": True,
        }

    def prefetch_diagnostics(self, session_id: str) -> dict[str, Any]:
        return dict(self.last_prefetch_reports.get(session_id, {}))

    def _normalize_prefetch_response(
        self,
        payload: dict[str, Any],
        *,
        validation_mode: str,
    ) -> tuple[str, tuple[_PrefetchHit, ...], tuple[str, ...]]:
        errors: list[str] = []
        remote_block = self._normalize_remote_block(
            payload.get("recall_block"),
            validation_mode=validation_mode,
            errors=errors,
        )
        hits = self._normalize_hits(
            payload.get("hits", ()),
            validation_mode=validation_mode,
            errors=errors,
        )
        if errors and validation_mode == "raise":
            raise ValueError("; ".join(errors))
        return remote_block, hits, tuple(errors)

    @staticmethod
    def _normalize_remote_block(
        payload: object,
        *,
        validation_mode: str,
        errors: list[str],
    ) -> str:
        if payload is None or payload == "":
            return ""
        if isinstance(payload, str):
            return payload.strip()
        if validation_mode != "ignore":
            errors.append("recall_block must be a string")
            return ""
        return str(payload).strip()

    @staticmethod
    def _normalize_hits(
        payload: object,
        *,
        validation_mode: str,
        errors: list[str],
    ) -> tuple[_PrefetchHit, ...]:
        if payload is None or payload == "":
            return ()
        if not isinstance(payload, (list, tuple)):
            if validation_mode != "ignore":
                errors.append("hits must be a list of objects")
            return ()
        hits: list[_PrefetchHit] = []
        for index, item in enumerate(payload):
            if not isinstance(item, dict):
                if validation_mode != "ignore":
                    errors.append(f"hits[{index}] must be an object")
                continue
            try:
                score = float(item.get("score", 0.0) or 0.0)
            except (TypeError, ValueError):
                if validation_mode != "ignore":
                    errors.append(f"hits[{index}].score must be numeric")
                score = 0.0
            hits.append(
                _PrefetchHit(
                    id=str(item.get("id") or item.get("record_id") or ""),
                    source_kind=str(item.get("source_kind") or "remote"),
                    title=str(item.get("title") or "Remote hit"),
                    snippet=str(item.get("body") or item.get("snippet") or ""),
                    score=score,
                    provenance=_compact_mapping(
                        {
                            "origin_kind": "remote_response",
                            "response_position": index,
                            "record_id": str(item.get("record_id") or "") or None,
                            "session_id": str(item.get("session_id") or "") or None,
                            "source_ref": str(item.get("source_ref") or "") or None,
                        }
                    ),
                )
            )
        return tuple(hits)

    @staticmethod
    def _source_breakdown(hits: tuple[_PrefetchHit, ...]) -> dict[str, int]:
        breakdown: dict[str, int] = {}
        for hit in hits:
            breakdown[hit.source_kind] = breakdown.get(hit.source_kind, 0) + 1
        return breakdown

    @staticmethod
    def _summarize_prefetch_response(
        payload: object,
        *,
        contract_id: str,
        contract_source: str,
    ) -> dict[str, Any]:
        summary: dict[str, Any] = {
            "response_contract": contract_id,
            "response_contract_source": contract_source,
        }
        if isinstance(payload, dict):
            summary["response_keys"] = tuple(sorted(str(key) for key in payload))
        return summary

    def _perform_writeback(
        self,
        *,
        session_id: str,
        governance: RemoteHttpRequestGovernance,
        payload: dict[str, Any],
    ) -> None:
        endpoint_url = governance.endpoint_url
        if endpoint_url is None:
            return
        failure_policy = governance.failure_policy or "raise"
        validation_mode = governance.response_validation_mode
        try:
            response = self.http_client.request(
                "POST",
                endpoint_url,
                payload=payload,
                options=governance.request_options,
            )
            validation_error = self._validate_writeback_response(
                response,
                validation_mode=validation_mode,
            )
            self._record_writeback_report(
                session_id,
                governance.request_kind,
                endpoint_url,
                failure_policy=failure_policy,
                success_override=False if validation_error is not None else None,
                response_validation_error=validation_error,
                response_summary=self._summarize_writeback_response(
                    response,
                    request_kind=governance.request_kind,
                    contract_id=governance.response_contract,
                    contract_source=governance.response_contract_source,
                ),
            )
        except Exception as exc:
            self._record_writeback_report(
                session_id,
                governance.request_kind,
                endpoint_url,
                failure_policy=failure_policy,
                success_override=False,
                error=str(exc),
                response_summary={
                    "request_kind": governance.request_kind,
                    "response_contract": governance.response_contract,
                    "response_contract_source": governance.response_contract_source,
                },
            )
            if validation_mode == "raise" or failure_policy not in {"ignore", "record"}:
                raise

    @staticmethod
    def _validate_writeback_response(
        payload: object,
        *,
        validation_mode: str,
    ) -> str | None:
        if validation_mode == "ignore":
            return None
        if not isinstance(payload, dict):
            error = "writeback response must be an object"
        elif payload.get("ok") is not True:
            error = "writeback response ok must be true"
        else:
            return None
        if validation_mode == "raise":
            raise ValueError(error)
        return error

    @staticmethod
    def _summarize_writeback_response(
        payload: object,
        *,
        request_kind: str,
        contract_id: str,
        contract_source: str,
    ) -> dict[str, Any]:
        summary: dict[str, Any] = {
            "request_kind": request_kind,
            "response_contract": contract_id,
            "response_contract_source": contract_source,
        }
        if not isinstance(payload, dict):
            return summary
        summary["response_keys"] = tuple(sorted(str(key) for key in payload))
        if "ok" in payload:
            summary["response_ok"] = payload.get("ok") is True
        status = str(payload.get("status") or "").strip()
        if status:
            summary["response_status"] = status
        message = str(payload.get("message") or payload.get("error") or "").strip()
        if message:
            summary["response_message"] = message
        report_id = str(payload.get("report_id") or payload.get("ack_id") or "").strip()
        if report_id:
            summary["response_report_id"] = report_id
        return summary

    def _transport_report(self) -> dict[str, Any]:
        last_request_report = getattr(self.http_client, "last_request_report", None)
        if not callable(last_request_report):
            return {}
        payload = last_request_report()
        if not isinstance(payload, dict):
            return {}
        return dict(payload)

    def _record_writeback_report(
        self,
        session_id: str,
        request_kind: str,
        endpoint_url: str,
        *,
        failure_policy: str,
        success_override: bool | None = None,
        error: str | None = None,
        response_validation_error: str | None = None,
        response_summary: dict[str, Any] | None = None,
    ) -> None:
        transport_report = self._transport_report()
        report = {
            "path": urlparse(endpoint_url).path or endpoint_url,
            **transport_report,
            "failure_policy": failure_policy,
        }
        if response_summary:
            report.update(response_summary)
        if success_override is not None:
            report["success"] = success_override
        if error is not None:
            report["error"] = error
        if response_validation_error is not None:
            report["response_validation_error"] = response_validation_error
        self.last_writeback_reports.setdefault(session_id, {})[request_kind] = report
        if session_id in self.last_prefetch_reports:
            writeback_trace = self.last_prefetch_reports[session_id].get("writeback_trace")
            if isinstance(writeback_trace, dict):
                refreshed_trace = dict(writeback_trace)
                refreshed_trace["detail_reports"] = dict(
                    self.last_writeback_reports[session_id]
                )
                refreshed_trace.pop("reports", None)
                self.last_prefetch_reports[session_id]["writeback_trace"] = refreshed_trace


def _serialize_dataclass(record: object) -> dict[str, Any]:
    if hasattr(record, "__dataclass_fields__"):
        from settings.shared.jsonl import serialize_record

        return serialize_record(record)
    raise TypeError(f"Unsupported record type: {type(record)!r}")
