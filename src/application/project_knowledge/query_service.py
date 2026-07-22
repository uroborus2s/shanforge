"""Bounded query and command use cases."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol


class QueryFailure(RuntimeError):
    def __init__(self, code: str, message: str, *, exit_code: int = 4) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code


class QueryStorePort(Protocol):
    def check(self) -> dict[str, Any]: ...

    def resolve_alias(self, entity_id: str) -> str: ...

    def find(self, query: str, *, limit: int) -> list[dict[str, Any]]: ...

    def entity(self, entity_id: str) -> dict[str, Any] | None: ...

    def locators(self, entity_id: str, *, limit: int) -> list[dict[str, Any]]: ...

    def direct_edges(self, entity_id: str, *, limit: int = 20) -> list[dict[str, Any]]: ...

    def trace(
        self, entity_id: str, *, depth: int, node_limit: int = 100, edge_limit: int = 200
    ) -> dict[str, Any]: ...

    def context_plan(self, entity_id: str, *, max_files: int, max_bytes: int) -> dict[str, Any]: ...


class ProjectKnowledgeQueryService:
    def __init__(self, store: QueryStorePort) -> None:
        self._store = store

    def _canonical(self, entity_id: str) -> str:
        try:
            canonical = self._store.resolve_alias(entity_id)
        except RuntimeError as error:
            code = str(getattr(error, "code", "QUERY_FAILED"))
            raise QueryFailure(code, str(error)) from error
        if self._store.entity(canonical) is None:
            raise QueryFailure("ENTITY_NOT_FOUND", f"entity {entity_id!r} was not found")
        return canonical

    def find(self, query: str) -> dict[str, Any]:
        try:
            items = self._store.find(query, limit=20)
        except RuntimeError as error:
            code = str(getattr(error, "code", "QUERY_FAILED"))
            raise QueryFailure(code, str(error), exit_code=2) from error
        return {"query": query, "items": items, "count": len(items)}

    def show(self, entity_id: str) -> dict[str, Any]:
        canonical = self._canonical(entity_id)
        entity = self._store.entity(canonical)
        assert entity is not None
        return {
            "requested_id": entity_id,
            "canonical_id": canonical,
            "entity": entity,
            "locators": self._store.locators(canonical, limit=8),
            "edges": self._store.direct_edges(canonical, limit=20),
        }

    def trace(self, entity_id: str, *, depth: int = 2) -> dict[str, Any]:
        if depth < 0 or depth > 8:
            raise QueryFailure("INVALID_DEPTH", "trace depth must be between 0 and 8", exit_code=2)
        canonical = self._canonical(entity_id)
        return self._store.trace(canonical, depth=depth)

    def context(
        self,
        entity_id: str,
        *,
        max_files: int = 4,
        max_bytes: int = 32 * 1024,
    ) -> dict[str, Any]:
        if max_files < 1 or max_files > 16 or max_bytes < 1 or max_bytes > 1024 * 1024:
            raise QueryFailure(
                "INVALID_CONTEXT_BUDGET", "context budget is outside limits", exit_code=2
            )
        canonical = self._canonical(entity_id)
        try:
            plan = self._store.context_plan(canonical, max_files=max_files, max_bytes=max_bytes)
        except RuntimeError as error:
            code = str(getattr(error, "code", "QUERY_FAILED"))
            raise QueryFailure(code, str(error)) from error
        plan["entity_id"] = canonical
        return plan


class ProjectKnowledgeCommandService:
    def __init__(
        self,
        query_service: ProjectKnowledgeQueryService,
        *,
        check_index: Callable[[], dict[str, Any]],
        refresh_index: Callable[[], dict[str, Any]],
        rebuild_index: Callable[[], dict[str, Any]],
        enqueue_sync: Callable[[str, str], dict[str, Any]] | None = None,
        sync_head: Callable[[str], dict[str, Any]] | None = None,
        snapshot: Callable[..., dict[str, Any]] | None = None,
        maintain: Callable[[bool], dict[str, Any]] | None = None,
    ) -> None:
        self._query = query_service
        self._check_index = check_index
        self._refresh_index = refresh_index
        self._rebuild_index = rebuild_index
        self._enqueue_sync = enqueue_sync
        self._sync_head = sync_head
        self._snapshot = snapshot
        self._maintain = maintain

    def execute(self, command: str, **arguments: Any) -> dict[str, Any]:
        if command == "find":
            return self._query.find(str(arguments["query"]))
        if command == "show":
            return self._query.show(str(arguments["entity_id"]))
        if command == "trace":
            return self._query.trace(str(arguments["entity_id"]), depth=int(arguments["depth"]))
        if command == "context":
            return self._query.context(
                str(arguments["entity_id"]),
                max_files=int(arguments["max_files"]),
                max_bytes=int(arguments["max_bytes"]),
            )
        if command == "index.check":
            return self._check_index()
        if command == "index.refresh":
            return self._refresh_index()
        if command == "index.rebuild":
            return self._rebuild_index()
        if command == "sync.enqueue" and self._enqueue_sync is not None:
            return self._enqueue_sync(str(arguments["head"]), str(arguments["scope"]))
        if command == "sync.head" and self._sync_head is not None:
            return self._sync_head(str(arguments["scope"]))
        if command == "snapshot" and self._snapshot is not None:
            return self._snapshot(**arguments)
        if command == "maintain" and self._maintain is not None:
            return self._maintain(bool(arguments["apply"]))
        raise QueryFailure("INVALID_INPUT", f"unsupported command {command!r}", exit_code=2)
