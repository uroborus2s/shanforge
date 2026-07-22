"""Bounded read queries over the current SQLite projection."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sqlite3
from collections import deque
from contextlib import closing
from pathlib import Path
from typing import Any


class StoreQueryError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _fts_expression(query: str) -> str:
    tokens = re.findall(r"[\w\-\u4e00-\u9fff]+", query, flags=re.UNICODE)
    if not tokens:
        raise StoreQueryError("QUERY_EMPTY", "query has no searchable terms")
    return " AND ".join(f'"{token}"' for token in tokens)


class SQLiteKnowledgeQueryStore:
    def __init__(self, database_path: Path, project_root: Path) -> None:
        self._path = database_path
        self._root = project_root.resolve()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def check(self) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            integrity = str(connection.execute("PRAGMA integrity_check").fetchone()[0])
            current = connection.execute(
                "SELECT generation_id,source_root_sha256,as_of FROM pk_generation "
                "WHERE status='current'"
            ).fetchone()
            source_count = int(
                connection.execute("SELECT COUNT(*) FROM pk_source WHERE enabled=1").fetchone()[0]
            )
        if integrity != "ok":
            raise StoreQueryError("INDEX_CORRUPT", integrity)
        return {
            "integrity": integrity,
            "generation": None if current is None else dict(current),
            "source_count": source_count,
        }

    def resolve_alias(self, entity_id: str) -> str:
        current = entity_id
        visited: set[str] = set()
        with closing(self._connect()) as connection:
            for _ in range(8):
                if current in visited:
                    raise StoreQueryError("ALIAS_CYCLE", f"alias cycle detected at {current}")
                visited.add(current)
                row = connection.execute(
                    "SELECT canonical_entity_id FROM pk_entity_alias WHERE alias_entity_id=?",
                    (current,),
                ).fetchone()
                if row is None:
                    return current
                current = str(row[0])
        raise StoreQueryError("ALIAS_DEPTH_EXCEEDED", "alias chain exceeds 8 hops")

    def find(self, query: str, *, limit: int) -> list[dict[str, Any]]:
        expression = _fts_expression(query)
        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        with closing(self._connect()) as connection:
            exact = connection.execute(
                """
                SELECT entity_id,entity_kind,display_name,summary
                  FROM pk_entity WHERE entity_id=?
                """,
                (query,),
            ).fetchone()
            if exact is not None:
                item = dict(exact)
                item["confidence"] = 1.0
                results.append(item)
                seen.add(str(exact["entity_id"]))
            for table, confidence in (("pk_search_fts", 0.9), ("pk_search_tri", 0.7)):
                try:
                    rows = connection.execute(
                        f"""
                        SELECT e.entity_id,n.entity_kind,e.title AS display_name,e.summary,
                               bm25({table}) AS rank
                          FROM {table} f
                          JOIN pk_search_entry e ON e.rowid=f.rowid
                          JOIN pk_entity n ON n.entity_id=e.entity_id
                         WHERE {table} MATCH ?
                         ORDER BY rank
                         LIMIT ?
                        """,
                        (expression, limit),
                    ).fetchall()
                except sqlite3.OperationalError:
                    rows = []
                for row in rows:
                    entity_id = str(row["entity_id"])
                    if entity_id in seen:
                        continue
                    item = dict(row)
                    item.pop("rank", None)
                    item["confidence"] = confidence
                    results.append(item)
                    seen.add(entity_id)
                    if len(results) >= limit:
                        return results
            like = f"%{query}%"
            rows = connection.execute(
                """
                SELECT entity_id,entity_kind,display_name,summary
                  FROM pk_entity
                 WHERE display_name LIKE ? OR entity_id LIKE ?
                 ORDER BY display_name
                 LIMIT ?
                """,
                (like, like, limit),
            ).fetchall()
            for row in rows:
                entity_id = str(row["entity_id"])
                if entity_id in seen:
                    continue
                item = dict(row)
                item["confidence"] = 0.5
                results.append(item)
                seen.add(entity_id)
                if len(results) >= limit:
                    break
        return results

    def entity(self, entity_id: str) -> dict[str, Any] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                """
                SELECT entity_id,entity_kind,display_name,summary,lifecycle_status,
                       primary_artifact_id,semantic_sha256
                  FROM pk_entity WHERE entity_id=?
                """,
                (entity_id,),
            ).fetchone()
        return None if row is None else dict(row)

    def locators(self, entity_id: str, *, limit: int) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT l.locator_id,l.locator_kind,l.selector_json,l.validation_state,
                       l.source_id,s.relative_path,st.size_bytes,
                       el.locator_role,el.confidence,el.is_primary
                  FROM pk_entity_locator el
                  JOIN pk_locator l ON l.locator_id=el.locator_id
                  JOIN pk_source s ON s.source_id=l.source_id
                  LEFT JOIN pk_source_state st ON st.source_id=s.source_id
                 WHERE el.entity_id=?
                 ORDER BY el.is_primary DESC,el.confidence DESC,el.locator_role,l.locator_id
                 LIMIT ?
                """,
                (entity_id, limit),
            ).fetchall()
        items: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["selector"] = json.loads(str(item.pop("selector_json")))
            estimated = item["selector"].get("estimated_bytes")
            if isinstance(estimated, int) and estimated >= 0:
                item["size_bytes"] = min(int(item["size_bytes"] or 0), estimated)
            items.append(item)
        return items

    def direct_edges(self, entity_id: str, *, limit: int = 20) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT edge_id,from_entity_id,to_entity_id,relation_type,source_id,
                       strength,confidence,evidence_locator_id
                  FROM pk_edge
                 WHERE from_entity_id=? OR to_entity_id=?
                 ORDER BY relation_type,from_entity_id,to_entity_id,source_id
                 LIMIT ?
                """,
                (entity_id, entity_id, limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def trace(
        self,
        entity_id: str,
        *,
        depth: int,
        node_limit: int = 100,
        edge_limit: int = 200,
    ) -> dict[str, Any]:
        pending: deque[tuple[str, int]] = deque([(entity_id, 0)])
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, Any]] = []
        seen_edges: set[str] = set()
        while pending and len(nodes) < node_limit and len(edges) < edge_limit:
            current, current_depth = pending.popleft()
            if current in nodes:
                continue
            entity = self.entity(current)
            if entity is None:
                continue
            nodes[current] = entity
            if current_depth >= depth:
                continue
            for edge in self.direct_edges(current, limit=edge_limit):
                edge_id = str(edge["edge_id"])
                if edge_id not in seen_edges:
                    edges.append(edge)
                    seen_edges.add(edge_id)
                neighbour = (
                    str(edge["to_entity_id"])
                    if edge["from_entity_id"] == current
                    else str(edge["from_entity_id"])
                )
                if neighbour not in nodes:
                    pending.append((neighbour, current_depth + 1))
        return {
            "nodes": list(nodes.values()),
            "edges": edges[:edge_limit],
            "truncated": bool(pending) or len(edges) >= edge_limit,
        }

    def context_plan(
        self,
        entity_id: str,
        *,
        max_files: int,
        max_bytes: int,
    ) -> dict[str, Any]:
        locators = self.locators(entity_id, limit=32)
        files: list[dict[str, Any]] = []
        seen_paths: set[str] = set()
        total_bytes = 0
        for locator in locators:
            relative_path = str(locator["relative_path"])
            if relative_path in seen_paths:
                continue
            size_bytes = int(locator["size_bytes"] or 0)
            if len(files) >= max_files or total_bytes + size_bytes > max_bytes:
                continue
            self._validate_locator(locator)
            files.append(
                {
                    "relative_path": relative_path,
                    "locator_id": locator["locator_id"],
                    "locator_kind": locator["locator_kind"],
                    "selector": locator["selector"],
                    "size_bytes": size_bytes,
                    "locator_role": locator["locator_role"],
                }
            )
            seen_paths.add(relative_path)
            total_bytes += size_bytes
        if locators and not files:
            raise StoreQueryError("CONTEXT_BUDGET_EXHAUSTED", "no locator fits the context budget")
        return {"files": files, "total_bytes": total_bytes, "body_read": False}

    def _safe_source_path(self, relative_path: str) -> Path:
        path = (self._root / relative_path).resolve()
        if not path.is_relative_to(self._root) or not path.is_file():
            raise StoreQueryError("LOCATOR_NOT_FOUND", "locator source is unavailable")
        return path

    def _validate_locator(self, locator: dict[str, Any]) -> None:
        path = self._safe_source_path(str(locator["relative_path"]))
        selector = locator["selector"]
        kind = str(locator["locator_kind"])
        matches = 0
        if kind == "markdown_section":
            text = path.read_text(encoding="utf-8")
            section_id = str(selector["section_id"])
            blocks = _markdown_section_blocks(text, section_id)
            matches = len(blocks)
            expected_hash = selector.get("block_sha256")
            if matches == 1 and isinstance(expected_hash, str):
                actual_hash = hashlib.sha256(blocks[0].encode("utf-8")).hexdigest()
                matches = 1 if actual_hash == expected_hash else 0
        elif kind == "python_symbol":
            tree = ast.parse(path.read_text(encoding="utf-8"))
            qualified = str(selector["qualified_name"])
            matches = _python_symbol_matches(tree, qualified, str(selector["symbol_kind"]))
        elif kind == "json_pointer":
            value: Any = json.loads(path.read_text(encoding="utf-8"))
            try:
                _resolve_json_pointer(value, str(selector["pointer"]))
                matches = 1
            except KeyError, IndexError, TypeError, ValueError:
                matches = 0
        else:
            matches = 1 if locator["validation_state"] == "valid" else 0
        if matches == 0:
            raise StoreQueryError("LOCATOR_NOT_FOUND", "locator did not match the current source")
        if matches > 1:
            raise StoreQueryError(
                "LOCATOR_AMBIGUOUS", "locator matched the current source more than once"
            )


def _heading_slug(title: str) -> str:
    return re.sub(r"[^\w\-\u4e00-\u9fff]+", "-", title.strip().lower()).strip("-")


def _markdown_section_blocks(text: str, requested_section_id: str) -> list[str]:
    lines = text.splitlines()
    raw: list[tuple[str, int]] = []
    pending: str | None = None
    heading_counts: dict[str, int] = {}
    for index, line in enumerate(lines):
        marker = re.fullmatch(r"<!--\s*sf:section-id=([^\s]+)\s*-->", line.strip())
        if marker:
            pending = marker.group(1)
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if heading is None:
            continue
        if pending is not None:
            section_id = pending
        else:
            slug = _heading_slug(heading.group(1))
            heading_counts[slug] = heading_counts.get(slug, 0) + 1
            occurrence = heading_counts[slug]
            section_id = f"heading:{slug}" if occurrence == 1 else f"heading:{slug}~{occurrence}"
        raw.append((section_id, index))
        pending = None
    blocks: list[str] = []
    for position, (section_id, start) in enumerate(raw):
        if section_id != requested_section_id:
            continue
        end = raw[position + 1][1] if position + 1 < len(raw) else len(lines)
        blocks.append("\n".join(lines[start:end]))
    return blocks


def _python_symbol_matches(tree: ast.AST, qualified_name: str, symbol_kind: str) -> int:
    matches = 0

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack: list[str] = []

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            nonlocal matches
            name = ".".join([*self.stack, node.name])
            if name == qualified_name and symbol_kind == "class":
                matches += 1
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            nonlocal matches
            name = ".".join([*self.stack, node.name])
            if name == qualified_name and symbol_kind == "function":
                matches += 1
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            nonlocal matches
            name = ".".join([*self.stack, node.name])
            if name == qualified_name and symbol_kind == "async_function":
                matches += 1
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

    Visitor().visit(tree)
    return matches


def _resolve_json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ValueError("invalid JSON pointer")
    current = value
    for raw_token in pointer[1:].split("/"):
        token = raw_token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        elif isinstance(current, dict):
            current = current[token]
        else:
            raise TypeError("JSON pointer descends through a scalar")
    return current
