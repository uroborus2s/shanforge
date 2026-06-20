from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from domain.session.assembly_models import SessionAssemblyManifest
from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.data_access import (
    SearchIndexProviderPort,
    StructuredStoreProviderPort,
    VectorIndexProviderPort,
)
from runtime.session_search.models import SessionArchiveHit, SessionTranscriptSlice


@dataclass(slots=True)
class SessionSearchService:
    """Self-owned scaffold for archive search and replay explanations."""

    structured_store: StructuredStoreProviderPort | None = None
    search_index: SearchIndexProviderPort | None = None
    vector_index: VectorIndexProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="session_search",
            name="Session Search",
            summary=(
                "Searches archived sessions, loads transcript slices, and "
                "explains session assembly."
            ),
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="session_search.search_archive",
                    method_name="search_session_archive",
                    summary="Search archived sessions.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="session_search.load_slice",
                    method_name="load_session_slice",
                    summary="Load one transcript slice.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="session_search.explain_assembly",
                    method_name="explain_session_assembly",
                    summary="Explain session assembly sources.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="session_search.search_artifacts",
                    method_name="search_session_artifacts",
                    summary="Search archived session artifacts.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("structured_store", required=False),
                CapabilityProviderDependency("search_index", required=False),
                CapabilityProviderDependency("vector_index", required=False),
            ),
        )

    def search_session_archive(
        self,
        query: str,
        profile_id: str | None,
        limit: int,
        context: CapabilityInvocationContext,
    ) -> tuple[SessionArchiveHit, ...]:
        capped_limit = max(1, min(limit, 10))
        filters: dict[str, Any] = {}
        if profile_id is not None:
            filters["profile_id"] = profile_id

        if not query.strip():
            records = self._structured_query("sessions", filters=filters, limit=capped_limit + 5)
            records = self._exclude_current_lineage(records, context.session_id)
            return tuple(self._archive_hit_from_record(record) for record in records[:capped_limit])

        records = self._search_records("sessions", query, capped_limit + 5, filters=filters)
        records = self._exclude_current_lineage(records, context.session_id)
        return tuple(self._archive_hit_from_record(record) for record in records[:capped_limit])

    def load_session_slice(
        self,
        session_id: str,
        cursor: str | None,
        limit: int,
        context: CapabilityInvocationContext,
    ) -> SessionTranscriptSlice:
        del context
        capped_limit = max(1, min(limit, 200))
        offset = int(cursor or "0")
        records = self._structured_query(
            "session_events",
            filters={"session_id": session_id},
            limit=max(offset + capped_limit + 1, capped_limit + 1),
        )
        window = records[offset : offset + capped_limit]
        next_cursor = str(offset + capped_limit) if offset + capped_limit < len(records) else None
        return SessionTranscriptSlice(
            session_id=session_id,
            cursor=next_cursor,
            events=tuple(dict(record) for record in window),
            metadata={
                "offset": offset,
                "limit": capped_limit,
                "total_events": len(records),
            },
        )

    def explain_session_assembly(
        self,
        session_id: str,
        context: CapabilityInvocationContext,
    ) -> SessionAssemblyManifest:
        del context
        session_record = self._structured_get("sessions", session_id)
        if session_record is None:
            raise KeyError(f"Unknown session: {session_id}")

        event_records = self._structured_query(
            "session_events",
            filters={"session_id": session_id},
            limit=500,
        )
        artifact_records = self._structured_query(
            "artifacts",
            filters={"session_id": session_id},
            limit=500,
        )
        sources = []
        if session_record.get("profile_id"):
            sources.append("profile")
        if session_record.get("workspace_root"):
            sources.append("workspace")
        if event_records:
            sources.append("events")
        if artifact_records:
            sources.append("artifacts")
        if session_record.get("parent_session_id"):
            sources.append("parent_session")

        manifest_payload = session_record.get("assembly_manifest")
        if isinstance(manifest_payload, dict):
            manifest = SessionAssemblyManifest.from_mapping(manifest_payload)
            metadata = dict(manifest.metadata)
            metadata.update(
                {
                    "event_count": len(event_records),
                    "artifact_count": len(artifact_records),
                    "preview": session_record.get("preview"),
                }
            )
            return SessionAssemblyManifest(
                session_id=manifest.session_id,
                profile_id=manifest.profile_id,
                workspace_root=manifest.workspace_root,
                rule_bundle=manifest.rule_bundle,
                active_skills=manifest.active_skills,
                recall_scope_filters=manifest.recall_scope_filters,
                recalled_memory_ids=manifest.recalled_memory_ids,
                child_session_ids=manifest.child_session_ids,
                child_digests=manifest.child_digests,
                memory_provider_binding=manifest.memory_provider_binding,
                selected_model=manifest.selected_model,
                model_bindings=manifest.model_bindings,
                backend_bindings=manifest.backend_bindings,
                provider_bindings=manifest.provider_bindings,
                sources=manifest.sources,
                metadata=metadata,
            )

        return SessionAssemblyManifest(
            session_id=session_id,
            profile_id=str(session_record.get("profile_id") or "") or None,
            workspace_root=str(session_record.get("workspace_root") or "") or None,
            sources=tuple(sources),
            metadata={
                "event_count": len(event_records),
                "artifact_count": len(artifact_records),
                "preview": session_record.get("preview"),
            },
        )

    def get_session_summary(self, session_id: str) -> str | None:
        session_record = self._structured_get("sessions", session_id)
        if session_record is None:
            return None
        summary = str(session_record.get("preview") or session_record.get("summary") or "").strip()
        return summary or None

    def search_session_artifacts(
        self,
        filters: dict[str, object] | None,
        context: CapabilityInvocationContext,
    ) -> tuple[SessionArchiveHit, ...]:
        del context
        normalized_filters = dict(filters or {})
        query = str(normalized_filters.pop("query", "") or "")
        limit = int(normalized_filters.pop("limit", 10) or 10)

        if query:
            records = self._search_records("artifacts", query, limit, filters=normalized_filters)
        else:
            records = self._structured_query("artifacts", filters=normalized_filters, limit=limit)
        return tuple(self._artifact_hit_from_record(record) for record in records[:limit])

    def _structured_query(
        self,
        namespace: str,
        filters: dict[str, object] | None,
        limit: int,
    ) -> list[dict[str, object]]:
        if self.structured_store is None:
            return []
        return [
            dict(item)
            for item in self.structured_store.query_records(namespace, filters, limit)
        ]

    def _structured_get(self, namespace: str, record_id: str) -> dict[str, object] | None:
        if self.structured_store is None:
            return None
        record = self.structured_store.get_record(namespace, record_id)
        return dict(record) if record is not None else None

    def _search_records(
        self,
        namespace: str,
        query: str,
        limit: int,
        filters: dict[str, object] | None,
    ) -> list[dict[str, object]]:
        if self.search_index is not None:
            return [
                dict(item)
                for item in self.search_index.search(namespace, query, limit, filters)
            ]

        records = self._structured_query(namespace, filters=filters, limit=max(limit * 5, 50))
        tokens = tuple(token for token in query.lower().split() if token)
        matched: list[dict[str, object]] = []
        for record in records:
            text = str(record.get("search_text") or record.get("summary") or "").lower()
            score = sum(text.count(token) for token in tokens)
            if score <= 0:
                continue
            record["score"] = float(score)
            matched.append(record)
        matched.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        return matched[:limit]

    def _exclude_current_lineage(
        self,
        records: list[dict[str, object]],
        current_session_id: str,
    ) -> list[dict[str, object]]:
        current_root = self._resolve_parent_session(current_session_id)
        filtered = []
        seen_session_ids: set[str] = set()
        for record in records:
            session_id = str(record.get("session_id") or "")
            if not session_id:
                continue
            resolved_session_id = self._resolve_parent_session(session_id)
            if current_root and resolved_session_id == current_root:
                continue
            if resolved_session_id in seen_session_ids:
                continue
            if resolved_session_id != session_id:
                record = dict(record)
                record["session_id"] = resolved_session_id
            filtered.append(record)
            seen_session_ids.add(resolved_session_id)
        return filtered

    def _resolve_parent_session(self, session_id: str | None) -> str | None:
        if not session_id:
            return None
        visited: set[str] = set()
        current = session_id
        while current and current not in visited:
            visited.add(current)
            record = self._structured_get("sessions", current)
            if record is None:
                break
            parent = str(record.get("parent_session_id") or "") or None
            if parent is None:
                break
            current = parent
        return current or session_id

    def _archive_hit_from_record(self, record: dict[str, object]) -> SessionArchiveHit:
        return SessionArchiveHit(
            session_id=str(record.get("session_id") or ""),
            summary=str(record.get("preview") or record.get("summary") or ""),
            profile_id=str(record.get("profile_id") or "") or None,
            score=float(record["score"]) if "score" in record else None,
            created_at=str(record.get("created_at") or "") or None,
            metadata={
                "parent_session_id": record.get("parent_session_id"),
                "workspace_root": record.get("workspace_root"),
            },
        )

    def _artifact_hit_from_record(self, record: dict[str, object]) -> SessionArchiveHit:
        return SessionArchiveHit(
            session_id=str(record.get("session_id") or ""),
            summary=str(record.get("summary") or ""),
            score=float(record["score"]) if "score" in record else None,
            created_at=str(record.get("created_at") or "") or None,
            metadata={
                "artifact_id": record.get("artifact_id"),
                "kind": record.get("kind"),
                "uri": record.get("uri"),
            },
        )
