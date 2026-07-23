"""Transactional SQLite projection for current project knowledge."""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections.abc import Mapping
from contextlib import closing
from pathlib import Path
from typing import Any

from domain.project_knowledge.models import SourceDefinition, canonical_json, stable_id
from settings.project_knowledge.schema import create_schema


class SQLiteIndexBusyError(RuntimeError):
    """The current database could not enter the exclusive rebuild switch window."""


_RELATION_TYPES = {
    "CONTAINS": ("declared_or_structural", 1, "Parent contains child"),
    "SATISFIES": ("declared", 0, "Design or delivery satisfies a requirement"),
    "IMPLEMENTS": ("declared", 0, "Implementation realizes a design or requirement"),
    "VERIFIES": ("declared", 0, "Test or evidence verifies a target"),
    "BLOCKS": ("declared", 0, "Source blocks target"),
    "SUPERSEDES": ("declared", 0, "Source supersedes target"),
    "DEPENDS_ON": ("declared", 1, "Source depends on target"),
    "EVIDENCES": ("declared", 0, "Source provides evidence for target"),
    "RELEASES": ("declared", 0, "Source releases target"),
    "MENTIONS": ("weak_only", 0, "Source text mentions target"),
}


def _trusted_json(value: Any) -> str:
    """Serialize extractor-validated internal values without a second tree walk."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )


class SQLiteProjectKnowledgeIndex:
    def __init__(self, database_path: Path) -> None:
        self._path = database_path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.is_file() or self._path.stat().st_size == 0:
            with closing(self._connect()) as connection:
                create_schema(connection)
                connection.commit()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = NORMAL")
        connection.execute("PRAGMA temp_store = MEMORY")
        connection.execute("PRAGMA cache_size = -32768")
        return connection

    @staticmethod
    def prepare_single_file_for_atomic_replace(database_path: Path) -> None:
        """Checkpoint WAL and leave a validated, self-contained DELETE-mode file."""

        connection = sqlite3.connect(database_path, timeout=0.2, isolation_level=None)
        try:
            checkpoint = connection.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchone()
            if checkpoint is not None and int(checkpoint[0]) != 0:
                raise SQLiteIndexBusyError("database has an active reader or writer")
            integrity = str(connection.execute("PRAGMA integrity_check").fetchone()[0])
            if integrity != "ok":
                raise sqlite3.DatabaseError(f"database integrity check failed: {integrity}")
            try:
                mode = str(connection.execute("PRAGMA journal_mode=DELETE").fetchone()[0])
            except sqlite3.OperationalError as error:
                if "locked" in str(error).lower() or "busy" in str(error).lower():
                    raise SQLiteIndexBusyError(
                        "database journal mode is locked by another connection"
                    ) from error
                raise
            if mode.lower() != "delete":
                raise SQLiteIndexBusyError(
                    f"database did not enter single-file journal mode: {mode}"
                )
        finally:
            connection.close()
        for suffix in ("-wal", "-shm"):
            sidecar = Path(f"{database_path}{suffix}")
            if not sidecar.exists():
                continue
            if sidecar.stat().st_size != 0:
                raise sqlite3.DatabaseError(
                    f"database sidecar remained non-empty after checkpoint: {sidecar.name}"
                )
            sidecar.unlink()

    def current_generation_id(self) -> str | None:
        current = self.current_generation()
        return None if current is None else str(current["generation_id"])

    def current_generation(self) -> dict[str, str] | None:
        with closing(self._connect()) as connection:
            row = connection.execute(
                "SELECT generation_id,source_root_sha256,COALESCE(git_commit,'') AS git_commit "
                "FROM pk_generation WHERE status='current'"
            ).fetchone()
        return None if row is None else dict(row)

    def source_contributions(self) -> dict[str, dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT gs.source_id,gs.content_sha256,gs.contribution_sha256,
                       gs.contribution_json,
                       st.size_bytes,st.mtime_ns
                  FROM pk_generation g
                  JOIN pk_generation_source gs ON gs.generation_id=g.generation_id
                  JOIN pk_source s ON s.source_id=gs.source_id
                  JOIN pk_source_state st ON st.source_id=gs.source_id
                 WHERE g.status='current'
                """
            ).fetchall()
        result: dict[str, dict[str, Any]] = {}
        for row in rows:
            contribution = json.loads(str(row["contribution_json"]))
            result[str(row["source_id"])] = {
                "content_sha256": str(row["content_sha256"]),
                "contribution": contribution,
                "contribution_json": str(row["contribution_json"]),
                "contribution_sha256": str(row["contribution_sha256"]),
                "extractor_id": str(contribution["extractor_id"]),
                "registry_version": str(contribution["registry_version"]),
                "size_bytes": int(row["size_bytes"]),
                "mtime_ns": int(row["mtime_ns"]),
            }
        return result

    def update_source_stats(self, stats: Mapping[str, tuple[int, int]]) -> None:
        with closing(self._connect()) as connection:
            connection.executemany(
                "UPDATE pk_source_state SET size_bytes=?,mtime_ns=? WHERE source_id=?",
                [(size, mtime, source_id) for source_id, (size, mtime) in stats.items()],
            )
            connection.commit()

    @staticmethod
    def _merge_entities(
        contributions: Mapping[str, dict[str, Any]],
    ) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
        candidates: dict[str, list[tuple[int, str, dict[str, Any]]]] = {}
        for source_id, contribution in contributions.items():
            rank = int(contribution["authority_rank"])
            for raw_entity in contribution.get("entities", []):
                entity = dict(raw_entity)
                candidates.setdefault(str(entity["entity_id"]), []).append(
                    (rank, source_id, entity)
                )
        merged: dict[str, dict[str, Any]] = {}
        owners: dict[str, str] = {}
        for entity_id, options in candidates.items():
            definitions = [option for option in options if bool(option[2].get("definition"))]
            if not definitions:
                continue
            highest = max(option[0] for option in definitions)
            winners = [option for option in definitions if option[0] == highest]
            semantic_hashes = {str(option[2]["semantic_sha256"]) for option in winners}
            if len(semantic_hashes) > 1:
                raise ValueError(f"conflicting definitions for entity {entity_id}")
            winner = sorted(winners, key=lambda option: option[1])[0]
            merged[entity_id] = winner[2]
            owners[entity_id] = winner[1]
        return merged, owners

    def publish(
        self,
        *,
        sources: tuple[SourceDefinition, ...],
        contributions: Mapping[str, dict[str, Any]],
        content_hashes: Mapping[str, str],
        stats: Mapping[str, tuple[int, int]],
        as_of: str,
        git_commit: str | None,
        contribution_jsons: Mapping[str, str] | None = None,
        contribution_hashes: Mapping[str, str] | None = None,
        changed_source_ids: frozenset[str] | None = None,
        previous_changed_contributions: Mapping[str, dict[str, Any]] | None = None,
    ) -> dict[str, str]:
        if contribution_jsons is None:
            contribution_jsons = {
                source_id: canonical_json(contribution)
                for source_id, contribution in contributions.items()
            }
        if contribution_hashes is None:
            contribution_hashes = {
                source_id: hashlib.sha256(serialized.encode("utf-8")).hexdigest()
                for source_id, serialized in contribution_jsons.items()
            }
        contribution_rows: list[tuple[str, str, str]] = []
        root_rows: list[list[str]] = []
        for source_id in sorted(contributions):
            serialized = contribution_jsons[source_id]
            contribution_sha = contribution_hashes[source_id]
            contribution_rows.append((source_id, contribution_sha, serialized))
            root_rows.append([source_id, content_hashes[source_id], contribution_sha])
        source_root = hashlib.sha256(canonical_json(root_rows).encode("utf-8")).hexdigest()
        generation_id = stable_id("generation", [source_root, as_of, git_commit])
        merged, entity_owners = self._merge_entities(contributions)
        facts_high_watermark = sum(
            len(contribution.get("events", [])) for contribution in contributions.values()
        )
        source_by_id = {source.source_id: source for source in sources}
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            previous_row = connection.execute(
                "SELECT generation_id,COALESCE(git_commit,'') FROM pk_generation "
                "WHERE status='current'"
            ).fetchone()
            previous = None if previous_row is None else str(previous_row[0])
            previous_git_commit = None if previous_row is None else str(previous_row[1])
            if previous is not None:
                self._prune_superseded_generations(connection, keep_generation_id=previous)
            connection.execute(
                """
                INSERT INTO pk_generation(
                    generation_id,parent_generation_id,status,source_root_sha256,
                    facts_high_watermark,git_commit,as_of,schema_version,created_at
                ) VALUES (?,?,?,?,?,?,?,?,?)
                """,
                (
                    generation_id,
                    previous,
                    "building",
                    source_root,
                    facts_high_watermark,
                    git_commit,
                    as_of,
                    1,
                    as_of,
                ),
            )
            current_ids = set(source_by_id)
            connection.executemany(
                """
                INSERT INTO pk_source(
                    source_id,registry_source_id,kind,relative_path,extractor_id,
                    registry_version,authority_rank,access_class,enabled,config_json
                ) VALUES (?,?,?,?,?,?,?,?,1,?)
                ON CONFLICT(source_id) DO UPDATE SET
                    registry_source_id=excluded.registry_source_id,
                    kind=excluded.kind,relative_path=excluded.relative_path,
                    extractor_id=excluded.extractor_id,
                    registry_version=excluded.registry_version,
                    authority_rank=excluded.authority_rank,
                    access_class=excluded.access_class,enabled=1,config_json=excluded.config_json
                """,
                [
                    (
                        source.source_id,
                        source.registry_source_id,
                        source.kind,
                        source.relative_path,
                        source.extractor_id,
                        source.registry_version,
                        source.authority_rank,
                        source.access_class.value,
                        _trusted_json(source.config),
                    )
                    for source in sources
                ],
            )
            connection.executemany(
                """
                INSERT INTO pk_source_state(
                    source_id,content_sha256,size_bytes,mtime_ns,parse_status,last_generation_id
                ) VALUES (?,?,?,?,?,?)
                ON CONFLICT(source_id) DO UPDATE SET
                    content_sha256=excluded.content_sha256,size_bytes=excluded.size_bytes,
                    mtime_ns=excluded.mtime_ns,parse_status=excluded.parse_status,
                    last_generation_id=excluded.last_generation_id,error_digest=NULL
                """,
                [
                    (
                        source.source_id,
                        content_hashes[source.source_id],
                        stats[source.source_id][0],
                        stats[source.source_id][1],
                        "parsed",
                        generation_id,
                    )
                    for source in sources
                ],
            )
            old_ids = {
                str(row[0])
                for row in connection.execute("SELECT source_id FROM pk_source WHERE enabled=1")
            }
            connection.executemany(
                "UPDATE pk_source SET enabled=0 WHERE source_id=?",
                [(removed,) for removed in old_ids - current_ids],
            )
            reused_source_ids: set[str] = set()
            if previous is not None and changed_source_ids is not None:
                reused_source_ids = set(source_by_id) - set(changed_source_ids)
                if reused_source_ids:
                    placeholders = ",".join("?" for _ in reused_source_ids)
                    connection.execute(
                        "INSERT INTO pk_generation_source("
                        "generation_id,source_id,content_sha256,contribution_sha256,"
                        "contribution_json,parse_status) "
                        "SELECT ?,source_id,content_sha256,contribution_sha256,"
                        "contribution_json,'parsed' FROM pk_generation_source "
                        f"WHERE generation_id=? AND source_id IN ({placeholders})",
                        (generation_id, previous, *sorted(reused_source_ids)),
                    )
            connection.executemany(
                """
                INSERT INTO pk_generation_source(
                    generation_id,source_id,content_sha256,contribution_sha256,
                    contribution_json,parse_status
                ) VALUES (?,?,?,?,?,'parsed')
                """,
                [
                    (
                        generation_id,
                        source_id,
                        content_hashes[source_id],
                        contribution_sha,
                        serialized,
                    )
                    for source_id, contribution_sha, serialized in contribution_rows
                    if source_id not in reused_source_ids
                ],
            )
            changed = set(changed_source_ids or ())
            incremental_source_id = next(iter(changed)) if len(changed) == 1 else None
            previous_contribution = (
                None
                if incremental_source_id is None or previous_changed_contributions is None
                else previous_changed_contributions.get(incremental_source_id)
            )
            can_patch = (
                previous is not None
                and incremental_source_id is not None
                and previous_contribution is not None
                and previous_git_commit == (git_commit or "")
                and self._can_patch_source_projection(
                    connection,
                    incremental_source_id,
                    previous_contribution,
                    contributions[incremental_source_id],
                    entity_owners,
                )
            )
            if can_patch:
                assert incremental_source_id is not None
                assert previous_contribution is not None
                self._patch_source_projection(
                    connection,
                    source_id=incremental_source_id,
                    previous_contribution=previous_contribution,
                    contribution=contributions[incremental_source_id],
                    all_entities=merged,
                    entity_owners=entity_owners,
                    generation_id=generation_id,
                    git_commit=git_commit,
                    facts_high_watermark=facts_high_watermark,
                )
            else:
                self._replace_current_projection(
                    connection,
                    contributions,
                    merged,
                    entity_owners,
                    generation_id,
                    git_commit=git_commit,
                    facts_high_watermark=facts_high_watermark,
                )
            if previous is not None:
                connection.execute(
                    "UPDATE pk_generation SET status='previous' WHERE generation_id=?", (previous,)
                )
            connection.execute(
                "UPDATE pk_generation SET status='current',published_at=? WHERE generation_id=?",
                (as_of, generation_id),
            )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()
        return {"generation_id": generation_id, "source_root_sha256": source_root}

    @staticmethod
    def _prune_superseded_generations(
        connection: sqlite3.Connection,
        *,
        keep_generation_id: str,
    ) -> None:
        """Keep exactly the recovery generation before publishing its successor."""

        stale = [
            str(row[0])
            for row in connection.execute(
                "SELECT generation_id FROM pk_generation WHERE generation_id<>?",
                (keep_generation_id,),
            )
        ]
        if not stale:
            return
        placeholders = ",".join("?" for _ in stale)
        for table in ("pk_render_view", "pk_cache_entry", "pk_diagnostic"):
            connection.execute(
                f"DELETE FROM {table} WHERE generation_id IN ({placeholders})",
                stale,
            )
        connection.execute(
            f"DELETE FROM pk_generation_source WHERE generation_id IN ({placeholders})",
            stale,
        )
        connection.execute(
            f"UPDATE pk_document_revision SET observed_generation_id=NULL "
            f"WHERE observed_generation_id IN ({placeholders})",
            stale,
        )
        connection.execute(
            f"UPDATE pk_source_state SET last_generation_id=NULL "
            f"WHERE last_generation_id IN ({placeholders})",
            stale,
        )
        connection.execute(
            f"UPDATE pk_meta SET updated_generation_id=? "
            f"WHERE updated_generation_id IN ({placeholders})",
            (keep_generation_id, *stale),
        )
        connection.execute(
            f"UPDATE pk_diagnostic SET generation_id=? WHERE generation_id IN ({placeholders})",
            (keep_generation_id, *stale),
        )
        connection.execute(
            "UPDATE pk_generation SET parent_generation_id=NULL WHERE generation_id=?",
            (keep_generation_id,),
        )
        connection.execute(
            f"DELETE FROM pk_generation WHERE generation_id IN ({placeholders})",
            stale,
        )

    @staticmethod
    def _can_patch_source_projection(
        connection: sqlite3.Connection,
        source_id: str,
        previous: Mapping[str, Any],
        current: Mapping[str, Any],
        entity_owners: Mapping[str, str],
    ) -> bool:
        """Use the narrow incremental path only for an existing isolated code file."""

        if not isinstance(previous.get("code_file"), dict) or not isinstance(
            current.get("code_file"), dict
        ):
            return False
        if any(
            contribution.get(key)
            for contribution in (previous, current)
            for key in ("aliases", "document", "sections", "relations")
        ):
            return False
        previous_entities = {
            str(entity["entity_id"])
            for entity in previous.get("entities", [])
            if bool(entity.get("definition"))
        }
        current_entities = {
            str(entity["entity_id"])
            for entity in current.get("entities", [])
            if bool(entity.get("definition"))
        }
        if not previous_entities or not current_entities:
            return False
        if any(entity_owners.get(entity_id) != source_id for entity_id in current_entities):
            return False
        owned = {
            str(row[0])
            for row in connection.execute(
                "SELECT e.entity_id FROM pk_entity e JOIN pk_artifact a "
                "ON a.artifact_id=e.primary_artifact_id "
                "WHERE a.source_id=? AND e.entity_kind<>'module'",
                (source_id,),
            )
        }
        if owned != previous_entities:
            return False
        old_artifact_id = str(dict(previous["artifact"])["artifact_id"])
        if connection.execute(
            "SELECT 1 FROM pk_entity WHERE entity_kind='module' AND primary_artifact_id=?",
            (old_artifact_id,),
        ).fetchone():
            return False
        affected = previous_entities | current_entities
        placeholders = ",".join("?" for _ in affected)
        ordered = sorted(affected)
        if connection.execute(
            "SELECT 1 FROM pk_edge WHERE "
            f"from_entity_id IN ({placeholders}) OR to_entity_id IN ({placeholders}) LIMIT 1",
            (*ordered, *ordered),
        ).fetchone():
            return False
        if connection.execute(
            "SELECT 1 FROM pk_test WHERE "
            f"code_symbol_id IN ({placeholders}) OR last_evidence_entity_id IN ({placeholders}) "
            "LIMIT 1",
            (*ordered, *ordered),
        ).fetchone():
            return False
        for table, column in (
            ("pk_entity_alias", "canonical_entity_id"),
            ("pk_memory_checkpoint", "entity_id"),
            ("pk_diagnostic", "entity_id"),
        ):
            if connection.execute(
                f"SELECT 1 FROM {table} WHERE {column} IN ({placeholders}) LIMIT 1",
                ordered,
            ).fetchone():
                return False
        locator_ids = [
            str(row[0])
            for row in connection.execute(
                "SELECT locator_id FROM pk_locator WHERE source_id=?", (source_id,)
            )
        ]
        if locator_ids:
            locator_placeholders = ",".join("?" for _ in locator_ids)
            for table, column in (
                ("pk_edge", "evidence_locator_id"),
                ("pk_work_item", "ledger_locator_id"),
                ("pk_diagnostic", "locator_id"),
            ):
                if connection.execute(
                    f"SELECT 1 FROM {table} WHERE {column} IN ({locator_placeholders}) LIMIT 1",
                    locator_ids,
                ).fetchone():
                    return False
            if connection.execute(
                "SELECT 1 FROM pk_entity_locator WHERE "
                f"locator_id IN ({locator_placeholders}) "
                f"AND entity_id NOT IN ({placeholders}) LIMIT 1",
                (*locator_ids, *ordered),
            ).fetchone():
                return False
        return True

    @staticmethod
    def _patch_source_projection(
        connection: sqlite3.Connection,
        *,
        source_id: str,
        previous_contribution: Mapping[str, Any],
        contribution: Mapping[str, Any],
        all_entities: Mapping[str, dict[str, Any]],
        entity_owners: Mapping[str, str],
        generation_id: str,
        git_commit: str | None,
        facts_high_watermark: int,
    ) -> None:
        previous_entity_ids = {
            str(entity["entity_id"])
            for entity in previous_contribution.get("entities", [])
            if bool(entity.get("definition"))
        }
        current_entity_ids = {
            str(entity["entity_id"])
            for entity in contribution.get("entities", [])
            if bool(entity.get("definition"))
            and entity_owners.get(str(entity["entity_id"])) == source_id
        }
        affected_entity_ids = previous_entity_ids | current_entity_ids
        placeholders = ",".join("?" for _ in affected_entity_ids)
        ordered_ids = sorted(affected_entity_ids)

        search_rows = connection.execute(
            "SELECT se.rowid,se.search_id,se.title,se.summary,se.tags FROM pk_search_entry se "
            f"WHERE se.entity_id IN ({placeholders})",
            ordered_ids,
        ).fetchall()
        for table in ("pk_search_fts", "pk_search_tri"):
            connection.executemany(
                f"INSERT INTO {table}({table},rowid,search_id,title,summary,tags) "
                "VALUES('delete',?,?,?,?,?)",
                [tuple(row) for row in search_rows],
            )
        connection.execute(f"DELETE FROM pk_test WHERE entity_id IN ({placeholders})", ordered_ids)
        connection.execute(
            f"DELETE FROM pk_code_symbol WHERE entity_id IN ({placeholders})", ordered_ids
        )
        connection.execute(
            f"DELETE FROM pk_code_file WHERE entity_id IN ({placeholders})", ordered_ids
        )
        connection.execute(
            f"DELETE FROM pk_search_entry WHERE entity_id IN ({placeholders})", ordered_ids
        )
        locator_ids = [
            str(row[0])
            for row in connection.execute(
                "SELECT locator_id FROM pk_locator WHERE source_id=?", (source_id,)
            )
        ]
        if locator_ids:
            locator_placeholders = ",".join("?" for _ in locator_ids)
            connection.execute(
                f"DELETE FROM pk_entity_locator WHERE locator_id IN ({locator_placeholders})",
                locator_ids,
            )
        connection.execute("DELETE FROM pk_locator WHERE source_id=?", (source_id,))
        connection.execute("DELETE FROM pk_diagnostic WHERE source_id=?", (source_id,))
        connection.execute(
            f"DELETE FROM pk_entity WHERE entity_id IN ({placeholders})", ordered_ids
        )
        old_artifact_id = str(dict(previous_contribution["artifact"])["artifact_id"])
        connection.execute("DELETE FROM pk_artifact WHERE artifact_id=?", (old_artifact_id,))

        artifact = dict(contribution["artifact"])
        connection.execute(
            "INSERT INTO pk_artifact(artifact_id,source_id,artifact_kind,relative_path,"
            "content_sha256,semantic_sha256,access_class,revision_ref) VALUES (?,?,?,?,?,?,?,?)",
            (
                artifact["artifact_id"],
                source_id,
                artifact["artifact_kind"],
                artifact["relative_path"],
                artifact["content_sha256"],
                artifact["semantic_sha256"],
                artifact["access_class"],
                git_commit,
            ),
        )
        connection.executemany(
            "INSERT INTO pk_entity(entity_id,entity_kind,display_name,summary,lifecycle_status,"
            "primary_artifact_id,semantic_sha256,detail_json) VALUES (?,?,?,?,?,?,?,?)",
            [
                (
                    entity_id,
                    all_entities[entity_id]["entity_kind"],
                    all_entities[entity_id]["display_name"],
                    all_entities[entity_id].get("summary"),
                    all_entities[entity_id]["lifecycle_status"],
                    artifact["artifact_id"],
                    all_entities[entity_id]["semantic_sha256"],
                    _trusted_json(all_entities[entity_id].get("details", {})),
                )
                for entity_id in sorted(current_entity_ids)
            ],
        )

        locator_rows: list[tuple[Any, ...]] = []
        entity_locator_rows: list[tuple[Any, ...]] = []
        primary_roles: set[tuple[str, str]] = set()
        for raw_locator in contribution.get("locators", []):
            locator = dict(raw_locator)
            selector_json = _trusted_json(locator["selector"])
            entity_id = str(locator["entity_id"])
            role = str(locator["locator_role"])
            primary_key = (entity_id, role)
            is_primary = primary_key not in primary_roles
            primary_roles.add(primary_key)
            locator_rows.append(
                (
                    locator["locator_id"],
                    locator["locator_kind"],
                    selector_json,
                    hashlib.sha256(selector_json.encode("utf-8")).hexdigest(),
                    source_id,
                )
            )
            entity_locator_rows.append(
                (entity_id, locator["locator_id"], role, 1.0, 1 if is_primary else 0)
            )
        connection.executemany(
            "INSERT INTO pk_locator(locator_id,locator_kind,selector_json,selector_sha256,"
            "source_id,validation_state) VALUES (?,?,?,?,?,'valid')",
            locator_rows,
        )
        connection.executemany(
            "INSERT INTO pk_entity_locator("
            "entity_id,locator_id,locator_role,confidence,is_primary) "
            "VALUES (?,?,?,?,?)",
            entity_locator_rows,
        )

        projected_search_rows: list[tuple[Any, ...]] = []
        for entity_id in current_entity_ids:
            candidates = [
                dict(raw)
                for raw in contribution.get("search", [])
                if str(raw["entity_id"]) == entity_id
            ]
            if not candidates:
                continue
            search = sorted(
                candidates,
                key=lambda item: (
                    -len(str(item.get("summary", ""))),
                    str(item.get("title", "")),
                    str(item.get("tags", "")),
                ),
            )[0]
            projected_search_rows.append(
                (
                    stable_id("search", entity_id),
                    entity_id,
                    search["title"],
                    search["summary"],
                    search["tags"],
                    artifact["access_class"],
                    hashlib.sha256(
                        _trusted_json([search["title"], search["summary"], search["tags"]]).encode(
                            "utf-8"
                        )
                    ).hexdigest(),
                )
            )
        connection.executemany(
            "INSERT INTO pk_search_entry(search_id,entity_id,title,summary,tags,access_class,"
            "content_sha256) VALUES (?,?,?,?,?,?,?)",
            projected_search_rows,
        )
        inserted_search_rows = [
            (int(rowid), search_id, title, summary, tags)
            for rowid, search_id, title, summary, tags in connection.execute(
                "SELECT rowid,search_id,title,summary,tags FROM pk_search_entry "
                f"WHERE entity_id IN ({placeholders})",
                ordered_ids,
            )
        ]
        connection.executemany(
            "INSERT INTO pk_search_fts(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
            inserted_search_rows,
        )
        connection.executemany(
            "INSERT INTO pk_search_tri(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
            inserted_search_rows,
        )

        raw_file = dict(contribution["code_file"])
        connection.execute(
            "INSERT INTO pk_code_file(code_file_id,entity_id,artifact_id,module_id,language,"
            "import_name) VALUES (?,?,?,?,?,?)",
            (
                raw_file["code_file_id"],
                raw_file["entity_id"],
                raw_file["artifact_id"],
                SQLiteProjectKnowledgeIndex._module_id_for_path(str(artifact["relative_path"])),
                raw_file["language"],
                raw_file["import_name"],
            ),
        )
        symbol_rows = [
            (
                symbol["symbol_id"],
                symbol["entity_id"],
                raw_file["code_file_id"],
                symbol["symbol_kind"],
                symbol["qualified_name"],
                symbol["signature_text"],
                symbol["visibility"],
                symbol["semantic_sha256"],
            )
            for symbol in map(dict, contribution.get("symbols", []))
            if str(symbol["entity_id"]) in current_entity_ids
        ]
        connection.executemany(
            "INSERT INTO pk_code_symbol(symbol_id,entity_id,code_file_id,symbol_kind,"
            "qualified_name,signature_text,visibility,semantic_sha256) VALUES (?,?,?,?,?,?,?,?)",
            symbol_rows,
        )
        if str(raw_file["import_name"]).startswith("tests."):
            connection.executemany(
                "INSERT INTO pk_test(test_id,entity_id,code_symbol_id,framework,test_kind,"
                "test_status,last_evidence_entity_id) VALUES (?,?,?,?,?,'indexed',NULL)",
                [
                    (symbol_id, entity_id, symbol_id, "pytest", "automated")
                    for symbol_id, entity_id, _, _, qualified_name, _, _, _ in symbol_rows
                    if str(qualified_name).rsplit(".", 1)[-1].startswith("test_")
                ],
            )
        connection.executemany(
            "INSERT INTO pk_diagnostic(diagnostic_id,generation_id,source_id,entity_id,severity,"
            "code,safe_message,locator_id,diagnostic_status) "
            "VALUES (?,?,?,NULL,?,?,?,NULL,'open')",
            [
                (
                    stable_id(
                        "diagnostic",
                        [
                            source_id,
                            position,
                            diagnostic.get("code"),
                            diagnostic.get("safe_message"),
                        ],
                    ),
                    generation_id,
                    source_id,
                    diagnostic["severity"],
                    diagnostic["code"],
                    diagnostic["safe_message"],
                )
                for position, diagnostic in enumerate(
                    map(dict, contribution.get("diagnostics", []))
                )
            ],
        )
        connection.execute(
            "UPDATE pk_document_revision SET observed_generation_id=?", (generation_id,)
        )
        connection.execute("UPDATE pk_diagnostic SET generation_id=?", (generation_id,))
        meta_payload = {
            "generation_id": generation_id,
            "facts_high_watermark": facts_high_watermark,
            "git_commit": git_commit,
        }
        value_json = _trusted_json(meta_payload)
        connection.execute(
            "INSERT INTO pk_meta(meta_key,value_json,value_sha256,updated_generation_id) "
            "VALUES('current_generation',?,?,?) ON CONFLICT(meta_key) DO UPDATE SET "
            "value_json=excluded.value_json,value_sha256=excluded.value_sha256,"
            "updated_generation_id=excluded.updated_generation_id",
            (
                value_json,
                hashlib.sha256(value_json.encode("utf-8")).hexdigest(),
                generation_id,
            ),
        )
        connection.execute("UPDATE pk_meta SET updated_generation_id=?", (generation_id,))

    @staticmethod
    def _replace_current_projection(
        connection: sqlite3.Connection,
        contributions: Mapping[str, dict[str, Any]],
        entities: Mapping[str, dict[str, Any]],
        entity_owners: Mapping[str, str],
        generation_id: str,
        *,
        git_commit: str | None,
        facts_high_watermark: int,
    ) -> None:
        connection.execute("INSERT INTO pk_search_fts(pk_search_fts) VALUES('delete-all')")
        connection.execute("INSERT INTO pk_search_tri(pk_search_tri) VALUES('delete-all')")
        for table in (
            "pk_edge",
            "pk_entity_locator",
            "pk_entity_alias",
            "pk_acceptance_criterion",
            "pk_requirement",
            "pk_work_item",
            "pk_test",
            "pk_document_revision",
            "pk_memory_checkpoint",
            "pk_document_section",
            "pk_document",
            "pk_code_symbol",
            "pk_code_file",
            "pk_module",
            "pk_search_entry",
            "pk_diagnostic",
            "pk_locator",
            "pk_entity",
            "pk_artifact",
        ):
            connection.execute(f"DELETE FROM {table}")
        connection.executemany(
            """
            INSERT INTO pk_artifact(
                artifact_id,source_id,artifact_kind,relative_path,content_sha256,
                semantic_sha256,access_class,revision_ref
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            [
                (
                    artifact["artifact_id"],
                    source_id,
                    artifact["artifact_kind"],
                    artifact["relative_path"],
                    artifact["content_sha256"],
                    artifact["semantic_sha256"],
                    artifact["access_class"],
                    git_commit,
                )
                for source_id, contribution in contributions.items()
                for artifact in [dict(contribution["artifact"])]
            ],
        )
        connection.executemany(
            """
            INSERT INTO pk_entity(
                entity_id,entity_kind,display_name,summary,lifecycle_status,
                primary_artifact_id,semantic_sha256,detail_json
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            [
                (
                    entity_id,
                    entity["entity_kind"],
                    entity["display_name"],
                    entity.get("summary"),
                    entity["lifecycle_status"],
                    dict(contributions[entity_owners[entity_id]]["artifact"])["artifact_id"],
                    entity["semantic_sha256"],
                    _trusted_json(entity.get("details", {})),
                )
                for entity_id, entity in entities.items()
            ],
        )
        alias_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            for raw_alias in contribution.get("aliases", []):
                alias = dict(raw_alias)
                canonical_id = str(alias["canonical_entity_id"])
                if canonical_id not in entities:
                    raise ValueError(f"alias canonical entity is missing: {canonical_id}")
                alias_rows.append(
                    (
                        alias["alias_entity_id"],
                        canonical_id,
                        alias["reason"],
                        source_id,
                        generation_id,
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_entity_alias(
                alias_entity_id,canonical_entity_id,reason,source_id,created_generation_id
            ) VALUES (?,?,?,?,?)
            """,
            alias_rows,
        )
        primary_roles: set[tuple[str, str]] = set()
        locator_rows: list[tuple[Any, ...]] = []
        entity_locator_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            for raw_locator in contribution.get("locators", []):
                locator = dict(raw_locator)
                selector_json = _trusted_json(locator["selector"])
                entity_id = str(locator["entity_id"])
                locator_role = str(locator["locator_role"])
                primary_key = (entity_id, locator_role)
                is_primary = (
                    entity_owners.get(entity_id) == source_id and primary_key not in primary_roles
                )
                if is_primary:
                    primary_roles.add(primary_key)
                locator_rows.append(
                    (
                        locator["locator_id"],
                        locator["locator_kind"],
                        selector_json,
                        hashlib.sha256(selector_json.encode("utf-8")).hexdigest(),
                        source_id,
                    )
                )
                entity_locator_rows.append(
                    (
                        entity_id,
                        locator["locator_id"],
                        locator_role,
                        1.0,
                        1 if is_primary else 0,
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_locator(
                locator_id,locator_kind,selector_json,selector_sha256,source_id,
                validation_state
            ) VALUES (?,?,?,?,?,'valid')
            ON CONFLICT(locator_kind,selector_sha256) DO UPDATE SET
                validation_state='valid'
            """,
            locator_rows,
        )
        connection.executemany(
            """
            INSERT INTO pk_entity_locator(
                entity_id,locator_id,locator_role,confidence,is_primary
            ) VALUES (?,?,?,?,?)
            ON CONFLICT(entity_id,locator_id,locator_role) DO UPDATE SET
                confidence=MAX(confidence,excluded.confidence),
                is_primary=MAX(is_primary,excluded.is_primary)
            """,
            entity_locator_rows,
        )
        search_rows: list[tuple[Any, ...]] = []
        for entity_id, owner in entity_owners.items():
            contribution = contributions[owner]
            search_candidates = [
                dict(raw) for raw in contribution.get("search", []) if raw["entity_id"] == entity_id
            ]
            if search_candidates:
                search = sorted(
                    search_candidates,
                    key=lambda item: (
                        -len(str(item.get("summary", ""))),
                        str(item.get("title", "")),
                        str(item.get("tags", "")),
                    ),
                )[0]
                search_id = stable_id("search", entity_id)
                content_hash = hashlib.sha256(
                    _trusted_json([search["title"], search["summary"], search["tags"]]).encode(
                        "utf-8"
                    )
                ).hexdigest()
                access_class = dict(contribution["artifact"])["access_class"]
                search_rows.append(
                    (
                        search_id,
                        entity_id,
                        search["title"],
                        search["summary"],
                        search["tags"],
                        access_class,
                        content_hash,
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_search_entry(
                search_id,entity_id,title,summary,tags,access_class,content_sha256
            ) VALUES (?,?,?,?,?,?,?)
            """,
            search_rows,
        )
        search_rowids = {
            str(search_id): int(rowid)
            for rowid, search_id in connection.execute(
                "SELECT rowid,search_id FROM pk_search_entry"
            )
        }
        search_fts_rows = [
            (search_rowids[str(search_id)], search_id, title, summary, tags)
            for search_id, _, title, summary, tags, _, _ in search_rows
        ]
        connection.executemany(
            "INSERT INTO pk_search_fts(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
            search_fts_rows,
        )
        connection.executemany(
            "INSERT INTO pk_search_tri(rowid,search_id,title,summary,tags) VALUES (?,?,?,?,?)",
            search_fts_rows,
        )
        documents: set[str] = set()
        document_rows: list[tuple[Any, ...]] = []
        sections: dict[str, tuple[int, str, dict[str, Any]]] = {}
        for source_id, contribution in contributions.items():
            raw_document = contribution.get("document")
            if isinstance(raw_document, dict):
                entity_id = str(raw_document["entity_id"])
                if entity_owners.get(entity_id) == source_id:
                    document_rows.append(
                        (
                            raw_document["document_id"],
                            entity_id,
                            raw_document["artifact_id"],
                            raw_document["title"],
                            raw_document.get("chinese_name"),
                            raw_document.get("audience"),
                            raw_document.get("owner"),
                            raw_document.get("doc_status", "active"),
                            raw_document.get("doc_version"),
                        )
                    )
                    documents.add(str(raw_document["document_id"]))
            rank = int(contribution["authority_rank"])
            for raw_section in contribution.get("sections", []):
                section = dict(raw_section)
                key = str(section["section_key"])
                existing = sections.get(key)
                if existing is None or (rank, source_id) > (existing[0], existing[1]):
                    sections[key] = (rank, source_id, section)
        connection.executemany(
            """
            INSERT INTO pk_document(
                document_id,entity_id,artifact_id,title,chinese_name,audience,
                owner,doc_status,doc_version
            ) VALUES (?,?,?,?,?,?,?,?,?)
            """,
            document_rows,
        )
        pending = dict(sections)
        while pending:
            progressed = False
            section_rows: list[tuple[Any, ...]] = []
            completed_keys: list[str] = []
            for key, (_, source_id, section) in list(pending.items()):
                if section["document_id"] not in documents:
                    del pending[key]
                    continue
                parent = section.get("parent_section_key")
                if parent is not None and parent in pending:
                    continue
                section_rows.append(
                    (
                        key,
                        section["document_id"],
                        section["section_id"],
                        section["entity_id"],
                        parent,
                        source_id,
                        section["display_title"],
                        section["display_order"],
                        section["block_sha256"],
                        section["safe_excerpt"],
                    )
                )
                completed_keys.append(key)
                progressed = True
            if not progressed:
                raise ValueError("document section parent cycle or missing parent")
            connection.executemany(
                """
                INSERT INTO pk_document_section(
                    section_key,document_id,section_id,entity_id,parent_section_key,
                    source_id,display_title,display_order,block_sha256,safe_excerpt
                ) VALUES (?,?,?,?,?,?,?,?,?,?)
                """,
                section_rows,
            )
            for key in completed_keys:
                del pending[key]
        if git_commit:
            connection.execute(
                """
                INSERT INTO pk_document_revision(
                    document_id,git_commit,blob_sha256,content_sha256,doc_version,
                    observed_generation_id
                )
                SELECT d.document_id,?,a.content_sha256,a.content_sha256,d.doc_version,?
                  FROM pk_document d JOIN pk_artifact a ON a.artifact_id=d.artifact_id
                """,
                (git_commit, generation_id),
            )
        project_id = next(
            (
                str(contribution["project_id"])
                for contribution in contributions.values()
                if contribution.get("project_id")
            ),
            "project",
        )
        memory_candidates = sorted(
            (
                (source_id, contribution)
                for source_id, contribution in contributions.items()
                if contribution.get("registry_source_id") == "SRC-MEMORY"
                and isinstance(contribution.get("document"), dict)
            ),
            key=lambda item: (
                not str(dict(item[1]["artifact"])["relative_path"]).endswith("/agent-session.md"),
                str(dict(item[1]["artifact"])["relative_path"]),
            ),
        )
        connection.executemany(
            """
            INSERT INTO pk_memory_checkpoint(
                checkpoint_id,entity_id,project_id,task_id,gate_id,facts_high_watermark,
                schema_id,size_bytes,content_sha256,is_current
            ) VALUES (?,?,?,NULL,NULL,?,'ProjectMemoryCheckpoint/v1',?,?,?)
            """,
            [
                (
                    stable_id("memory-checkpoint", [source_id, generation_id]),
                    dict(contribution["document"])["entity_id"],
                    project_id,
                    facts_high_watermark,
                    int(contribution.get("size_bytes", 0)),
                    dict(contribution["artifact"])["content_sha256"],
                    1 if position == 0 else 0,
                )
                for position, (source_id, contribution) in enumerate(memory_candidates)
            ],
        )
        module_sources: dict[str, tuple[str, dict[str, Any], dict[str, Any]]] = {}
        for source_id, contribution in contributions.items():
            raw_file = contribution.get("code_file")
            if not isinstance(raw_file, dict):
                continue
            artifact = dict(contribution["artifact"])
            match = re.match(
                r"^src/(access|application|domain|runtime|settings)(?:/|$)",
                str(artifact["relative_path"]),
            )
            if match and match.group(1) not in module_sources:
                module_sources[match.group(1)] = (source_id, dict(raw_file), artifact)
        module_entity_rows: list[tuple[Any, ...]] = []
        module_rows: list[tuple[Any, ...]] = []
        for layer_name, (_, raw_file, artifact) in sorted(module_sources.items()):
            module_id = f"module:{layer_name}"
            boundary_sha256 = hashlib.sha256(
                _trusted_json([layer_name, f"src/{layer_name}"]).encode("utf-8")
            ).hexdigest()
            module_entity_rows.append(
                (
                    module_id,
                    "module",
                    layer_name,
                    f"src/{layer_name} 分层模块",
                    "active",
                    raw_file["artifact_id"],
                    boundary_sha256,
                    _trusted_json({"root_path": f"src/{layer_name}"}),
                )
            )
            module_rows.append(
                (module_id, module_id, layer_name, f"src/{layer_name}", boundary_sha256)
            )
        connection.executemany(
            """
            INSERT INTO pk_entity(
                entity_id,entity_kind,display_name,summary,lifecycle_status,
                primary_artifact_id,semantic_sha256,detail_json
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            module_entity_rows,
        )
        connection.executemany(
            """
            INSERT INTO pk_module(
                module_id,entity_id,layer_name,root_path,owner,boundary_sha256
            ) VALUES (?,?,?,?,NULL,?)
            """,
            module_rows,
        )
        code_file_rows: list[tuple[Any, ...]] = []
        code_symbol_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            raw_file = contribution.get("code_file")
            if (
                not isinstance(raw_file, dict)
                or entity_owners.get(str(raw_file["entity_id"])) != source_id
            ):
                continue
            code_file_rows.append(
                (
                    raw_file["code_file_id"],
                    raw_file["entity_id"],
                    raw_file["artifact_id"],
                    SQLiteProjectKnowledgeIndex._module_id_for_path(
                        str(dict(contribution["artifact"])["relative_path"])
                    ),
                    raw_file["language"],
                    raw_file["import_name"],
                )
            )
            for raw_symbol in contribution.get("symbols", []):
                symbol = dict(raw_symbol)
                if entity_owners.get(str(symbol["entity_id"])) != source_id:
                    continue
                code_symbol_rows.append(
                    (
                        symbol["symbol_id"],
                        symbol["entity_id"],
                        raw_file["code_file_id"],
                        symbol["symbol_kind"],
                        symbol["qualified_name"],
                        symbol["signature_text"],
                        symbol["visibility"],
                        symbol["semantic_sha256"],
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_code_file(
                code_file_id,entity_id,artifact_id,module_id,language,import_name
            ) VALUES (?,?,?,?,?,?)
            """,
            code_file_rows,
        )
        connection.executemany(
            """
            INSERT INTO pk_code_symbol(
                symbol_id,entity_id,code_file_id,symbol_kind,qualified_name,
                signature_text,visibility,semantic_sha256
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            code_symbol_rows,
        )
        meta_payloads = {
            "current_generation": {
                "generation_id": generation_id,
                "facts_high_watermark": facts_high_watermark,
                "git_commit": git_commit,
            },
            "projection_contract": {
                "logical_table_count": 39,
                "schema_version": 1,
            },
        }
        for meta_key, payload in meta_payloads.items():
            value_json = _trusted_json(payload)
            connection.execute(
                """
                INSERT INTO pk_meta(meta_key,value_json,value_sha256,updated_generation_id)
                VALUES (?,?,?,?)
                ON CONFLICT(meta_key) DO UPDATE SET
                    value_json=excluded.value_json,
                    value_sha256=excluded.value_sha256,
                    updated_generation_id=excluded.updated_generation_id
                """,
                (
                    meta_key,
                    value_json,
                    hashlib.sha256(value_json.encode("utf-8")).hexdigest(),
                    generation_id,
                ),
            )

        requirement_ids: set[str] = set()
        requirement_rows: list[tuple[Any, ...]] = []
        for entity_id, entity in entities.items():
            if entity["entity_kind"] not in {"requirement", "non_functional_requirement"}:
                continue
            requirement_rows.append(
                (
                    entity_id,
                    entity_id,
                    entity.get("priority"),
                    entity["lifecycle_status"],
                )
            )
            requirement_ids.add(entity_id)
        connection.executemany(
            """
            INSERT INTO pk_requirement(
                requirement_id,entity_id,priority,requirement_status,owner,source_section_key
            ) VALUES (?,?,?,?,NULL,NULL)
            """,
            requirement_rows,
        )
        acceptance_rows: list[tuple[Any, ...]] = []
        for entity_id, entity in entities.items():
            if entity["entity_kind"] != "acceptance_criterion" or "-AC-" not in entity_id:
                continue
            requirement_id, order_text = entity_id.rsplit("-AC-", 1)
            if requirement_id not in requirement_ids:
                raise ValueError(
                    f"acceptance criterion {entity_id} has missing requirement {requirement_id}"
                )
            try:
                display_order = int(order_text)
            except ValueError:
                display_order = 0
            acceptance_rows.append(
                (
                    entity_id,
                    entity_id,
                    requirement_id,
                    display_order,
                    entity["display_name"],
                    entity["lifecycle_status"],
                )
            )
        connection.executemany(
            """
            INSERT INTO pk_acceptance_criterion(
                acceptance_id,entity_id,requirement_id,display_order,statement,
                criterion_status
            ) VALUES (?,?,?,?,?,?)
            """,
            acceptance_rows,
        )
        primary_locators = {
            str(entity_id): str(locator_id)
            for entity_id, locator_id in connection.execute(
                """
                SELECT entity_id,locator_id FROM pk_entity_locator
                 WHERE locator_role='definition' AND is_primary=1
                """
            )
        }
        work_item_rows: list[tuple[Any, ...]] = []
        for entity_id, entity in entities.items():
            if entity["entity_kind"] != "work_item":
                continue
            display_name = str(entity["display_name"])
            task_kind = display_name.split("-", 1)[0].lower() if "-" in display_name else "task"
            work_item_rows.append(
                (
                    entity_id,
                    entity_id,
                    task_kind,
                    entity["lifecycle_status"],
                    primary_locators.get(entity_id),
                )
            )
        connection.executemany(
            """
            INSERT INTO pk_work_item(
                work_item_id,entity_id,parent_work_item_id,task_kind,task_status,
                completion_level,ledger_locator_id
            ) VALUES (?,?,NULL,?,?,NULL,?)
            """,
            work_item_rows,
        )
        test_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            raw_file = contribution.get("code_file")
            if not isinstance(raw_file, dict) or not str(raw_file["import_name"]).startswith(
                "tests."
            ):
                continue
            for raw_symbol in contribution.get("symbols", []):
                symbol = dict(raw_symbol)
                leaf = str(symbol["qualified_name"]).rsplit(".", 1)[-1]
                if not leaf.startswith("test_") or symbol["entity_id"] not in entities:
                    continue
                test_rows.append(
                    (
                        symbol["symbol_id"],
                        symbol["entity_id"],
                        symbol["symbol_id"],
                        "pytest",
                        "automated",
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_test(
                test_id,entity_id,code_symbol_id,framework,test_kind,test_status,
                last_evidence_entity_id
            ) VALUES (?,?,?,?,?,'indexed',NULL)
            """,
            test_rows,
        )

        connection.executemany(
            """
            INSERT INTO pk_relation_type(
                relation_type,inverse_type,strength_policy,is_transitive,description
            ) VALUES (?,NULL,?,?,?)
            ON CONFLICT(relation_type) DO UPDATE SET
                strength_policy=excluded.strength_policy,
                is_transitive=excluded.is_transitive,
                description=excluded.description
            """,
            [
                (relation_type, policy, transitive, description)
                for relation_type, (policy, transitive, description) in _RELATION_TYPES.items()
            ],
        )
        edge_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            for raw_relation in contribution.get("relations", []):
                relation = dict(raw_relation)
                from_entity = str(relation["from_entity_id"])
                to_entity = str(relation["to_entity_id"])
                missing = sorted({from_entity, to_entity} - entities.keys())
                if missing:
                    raise ValueError(f"missing relation endpoint: {', '.join(missing)}")
                relation_type = str(relation["relation_type"])
                if relation_type not in _RELATION_TYPES:
                    raise ValueError(f"unsupported relation type: {relation_type}")
                strength = str(relation["strength"])
                if relation_type == "MENTIONS" and strength != "weak":
                    raise ValueError("MENTIONS relations must be weak")
                evidence_locator_id = relation.get("evidence_locator_id")
                semantic = hashlib.sha256(
                    _trusted_json(
                        [
                            from_entity,
                            to_entity,
                            relation_type,
                            source_id,
                            strength,
                            relation["confidence"],
                            evidence_locator_id,
                        ]
                    ).encode("utf-8")
                ).hexdigest()
                edge_rows.append(
                    (
                        stable_id(
                            "edge",
                            [
                                from_entity,
                                to_entity,
                                relation_type,
                                source_id,
                                evidence_locator_id,
                            ],
                        ),
                        from_entity,
                        to_entity,
                        relation_type,
                        source_id,
                        strength,
                        float(relation["confidence"]),
                        evidence_locator_id,
                        semantic,
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_edge(
                edge_id,from_entity_id,to_entity_id,relation_type,source_id,
                strength,confidence,evidence_locator_id,semantic_sha256
            ) VALUES (?,?,?,?,?,?,?,?,?)
            """,
            edge_rows,
        )
        diagnostic_rows: list[tuple[Any, ...]] = []
        for source_id, contribution in contributions.items():
            for position, raw_diagnostic in enumerate(contribution.get("diagnostics", [])):
                diagnostic = dict(raw_diagnostic)
                diagnostic_rows.append(
                    (
                        stable_id(
                            "diagnostic",
                            [
                                source_id,
                                position,
                                diagnostic.get("code"),
                                diagnostic.get("safe_message"),
                            ],
                        ),
                        generation_id,
                        source_id,
                        diagnostic["severity"],
                        diagnostic["code"],
                        diagnostic["safe_message"],
                    )
                )
        connection.executemany(
            """
            INSERT INTO pk_diagnostic(
                diagnostic_id,generation_id,source_id,entity_id,severity,code,
                safe_message,locator_id,diagnostic_status
            ) VALUES (?,?,?,NULL,?,?,?,NULL,'open')
            """,
            diagnostic_rows,
        )

    @staticmethod
    def _module_id_for_path(relative_path: str) -> str | None:
        match = re.match(r"^src/(access|application|domain|runtime|settings)(?:/|$)", relative_path)
        return None if match is None else f"module:{match.group(1)}"
