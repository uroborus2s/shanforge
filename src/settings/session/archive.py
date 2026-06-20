from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.ports import SessionAssemblyStorePort
from settings.session.artifact_store import InMemoryArtifactStore
from settings.session.store import InMemorySessionStore


def _to_iso_timestamp(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    if value is None:
        return None
    return str(value)


def _tokenize_query(query_text: str) -> tuple[str, ...]:
    return tuple(token for token in re.split(r"\s+", query_text.lower().strip()) if token)


def _truncate_around_matches(full_text: str, query: str, max_chars: int = 4000) -> str:
    if len(full_text) <= max_chars:
        return full_text

    text_lower = full_text.lower()
    query_lower = query.lower().strip()
    match_positions = [match.start() for match in re.finditer(re.escape(query_lower), text_lower)]

    if not match_positions:
        for term in _tokenize_query(query):
            match_positions.extend(match.start() for match in re.finditer(re.escape(term), text_lower))

    if not match_positions:
        return full_text[:max_chars] + "\n\n...[later conversation truncated]..."

    match_positions.sort()
    best_start = 0
    best_count = 0
    for candidate in match_positions:
        start = max(0, candidate - max_chars // 4)
        end = min(len(full_text), start + max_chars)
        if end - start < max_chars:
            start = max(0, len(full_text) - max_chars)
        count = sum(1 for position in match_positions if start <= position < end)
        if count > best_count:
            best_count = count
            best_start = start

    start = best_start
    end = min(len(full_text), start + max_chars)
    prefix = "...[earlier conversation truncated]...\n\n" if start > 0 else ""
    suffix = "\n\n...[later conversation truncated]..." if end < len(full_text) else ""
    return prefix + full_text[start:end] + suffix


@dataclass(slots=True)
class InMemorySessionArchiveProvider:
    """Structured-store adapter backed by the in-memory session and artifact stores."""

    session_store: InMemorySessionStore
    artifact_store: InMemoryArtifactStore
    assembly_store: SessionAssemblyStorePort | None = None

    def put_record(
        self,
        namespace: str,
        record_id: str,
        payload: Mapping[str, Any],
    ) -> None:
        raise NotImplementedError(f"Namespace is read-only: {namespace}:{record_id}")

    def get_record(self, namespace: str, record_id: str) -> Mapping[str, Any] | None:
        if namespace == "sessions":
            session = self.session_store.load_session(record_id)
            return self._session_to_record(session) if session is not None else None
        if namespace == "session_transcripts":
            session = self.session_store.load_session(record_id)
            if session is None:
                return None
            return {
                "session_id": record_id,
                "events": self._events_to_records(record_id),
            }
        if namespace == "artifacts":
            for record in self._artifact_records():
                if record["artifact_id"] == record_id:
                    return record
        return None

    def query_records(
        self,
        namespace: str,
        filters: Mapping[str, Any] | None = None,
        limit: int = 100,
    ) -> tuple[Mapping[str, Any], ...]:
        filters = dict(filters or {})
        if namespace == "sessions":
            records = self._session_records()
        elif namespace == "session_events":
            records = self._event_records()
        elif namespace == "artifacts":
            records = self._artifact_records()
        else:
            return ()

        filtered = [record for record in records if self._matches_filters(record, filters)]
        if namespace == "sessions":
            filtered.sort(key=lambda item: (item.get("created_at") or "", item["session_id"]), reverse=True)
        return tuple(filtered[: max(limit, 0)])

    def _session_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for session_id in sorted(self.session_store.sessions):
            session = self.session_store.load_session(session_id)
            if session is None:
                continue
            record = self._session_to_record(session)
            if record is not None:
                records.append(record)
        return records

    def _event_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for session_id in sorted(self.session_store.sessions):
            records.extend(self._events_to_records(session_id))
        return records

    def _artifact_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for session_id in sorted(self.artifact_store.session_artifact_ids):
            for artifact in self.artifact_store.list_artifacts(session_id):
                records.append(
                    {
                        "artifact_id": artifact.id,
                        "session_id": session_id,
                        "kind": artifact.kind,
                        "summary": artifact.summary,
                        "uri": artifact.uri,
                        "created_at": _to_iso_timestamp(artifact.created_at),
                    }
                )
        return records

    def _session_to_record(self, session: Any) -> dict[str, Any] | None:
        if session is None:
            return None
        transcript_preview = self._render_session_text(session.id, max_chars=400)
        profile_id = session.context.get("profile_id")
        created_at = self._session_created_at(session.id)
        return {
            "session_id": session.id,
            "summary": session.user_input,
            "profile_id": str(profile_id) if profile_id is not None else None,
            "workspace_root": session.context.get("workspace_root"),
            "parent_session_id": session.context.get("parent_session_id"),
            "created_at": created_at,
            "preview": transcript_preview,
            "search_text": self._render_session_text(session.id),
            "assembly_manifest": self._resolve_assembly_manifest(session),
        }

    def _events_to_records(self, session_id: str) -> list[dict[str, Any]]:
        events = self.session_store.list_events(session_id)
        return [
            {
                "event_id": event.id,
                "session_id": session_id,
                "type": event.type,
                "summary": event.summary,
                "payload": dict(event.payload),
                "created_at": _to_iso_timestamp(event.created_at),
            }
            for event in events
        ]

    def _session_created_at(self, session_id: str) -> str | None:
        events = self.session_store.list_events(session_id)
        if events:
            return _to_iso_timestamp(events[0].created_at)
        artifacts = self.artifact_store.list_artifacts(session_id)
        if artifacts:
            return _to_iso_timestamp(artifacts[0].created_at)
        session = self.session_store.load_session(session_id)
        if session is None:
            return None
        created_at = session.context.get("created_at")
        return _to_iso_timestamp(created_at)

    def _render_session_text(self, session_id: str, max_chars: int | None = None) -> str:
        session = self.session_store.load_session(session_id)
        if session is None:
            return ""

        parts = [f"[USER]: {session.user_input}"]
        for event in self.session_store.list_events(session_id):
            payload_text = json.dumps(event.payload, ensure_ascii=True, sort_keys=True)
            parts.append(f"[{event.type.upper()}]: {event.summary}\n{payload_text}")
        for artifact in self.artifact_store.list_artifacts(session_id):
            parts.append(f"[ARTIFACT:{artifact.kind}]: {artifact.summary}\n{artifact.uri}")

        text = "\n\n".join(parts)
        if max_chars is not None and len(text) > max_chars:
            return text[:max_chars]
        return text

    def _matches_filters(self, record: Mapping[str, Any], filters: Mapping[str, Any]) -> bool:
        for key, expected in filters.items():
            if expected is None:
                continue
            value = record.get(key)
            if isinstance(expected, (list, tuple, set)):
                if value not in expected:
                    return False
            elif value != expected:
                return False
        return True

    def _serialize_assembly_manifest(self, payload: Any) -> Mapping[str, Any] | None:
        if payload is None:
            return None
        if isinstance(payload, SessionAssemblyManifest):
            return payload.to_mapping()
        if isinstance(payload, Mapping):
            return dict(payload)
        return None

    def _resolve_assembly_manifest(self, session: Any) -> Mapping[str, Any] | None:
        if self.assembly_store is not None:
            manifest = self.assembly_store.get(session.id)
            if manifest is not None:
                return manifest.to_mapping()
        return self._serialize_assembly_manifest(session.context.get("assembly_manifest"))


@dataclass(slots=True)
class InMemorySearchIndexProvider:
    """Simple token-based search adapter over structured session records."""

    archive_store: InMemorySessionArchiveProvider

    def search(
        self,
        namespace: str,
        query_text: str,
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]:
        tokens = _tokenize_query(query_text)
        if not tokens:
            return self.archive_store.query_records(namespace, filters=filters, limit=limit)

        records = self.archive_store.query_records(namespace, filters=filters, limit=max(limit * 10, 50))
        scored_records: list[dict[str, Any]] = []
        for raw_record in records:
            record = dict(raw_record)
            haystack = str(record.get("search_text") or record.get("summary") or "").lower()
            score = sum(haystack.count(token) for token in tokens)
            if score <= 0:
                continue
            if "search_text" in record and namespace == "sessions":
                record["preview"] = _truncate_around_matches(record["search_text"], query_text, max_chars=800)
            record["score"] = float(score)
            scored_records.append(record)

        scored_records.sort(key=lambda item: (item["score"], item.get("created_at") or ""), reverse=True)
        return tuple(scored_records[: max(limit, 0)])


@dataclass(slots=True)
class EmptyVectorIndexProvider:
    """Placeholder vector index until embeddings land in the settings layer."""

    def query(
        self,
        namespace: str,
        vector: tuple[float, ...],
        limit: int = 20,
        filters: Mapping[str, Any] | None = None,
    ) -> tuple[Mapping[str, Any], ...]:
        return ()
