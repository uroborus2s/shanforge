"""Composition root and executable entry for deterministic project knowledge."""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from contextlib import closing
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from access.project_cli import run
from application.project_knowledge.index_service import ProjectKnowledgeIndexService
from application.project_knowledge.query_service import (
    ProjectKnowledgeCommandService,
    ProjectKnowledgeQueryService,
    QueryFailure,
)
from application.project_knowledge.site_service import ProjectSiteService
from application.project_knowledge.sync_service import ProjectStateSyncRequest
from runtime.project_knowledge.extractors import default_extractors
from runtime.project_knowledge.site_renderer import RENDERER_VERSION, ProjectSiteRenderer
from settings.project_knowledge.maintenance import (
    CacheRegistration,
    ProjectKnowledgeMaintenance,
)
from settings.project_knowledge.pm_projection import (
    ProjectManagementProjector,
    SQLiteSiteDataStore,
)
from settings.project_knowledge.query_store import SQLiteKnowledgeQueryStore
from settings.project_knowledge.site_publisher import AtomicSitePublisher
from settings.project_knowledge.source_registry import FileSourceRegistry
from settings.project_knowledge.sqlite_index import (
    SQLiteIndexBusyError,
    SQLiteProjectKnowledgeIndex,
)
from settings.project_knowledge.sync_store import SQLiteProjectStateSyncStore


def _as_of() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _git_head(root: Path) -> str:
    head_path = root / ".git/HEAD"
    value = head_path.read_text(encoding="utf-8").strip()
    if value.startswith("ref: "):
        reference = root / ".git" / value.removeprefix("ref: ")
        if reference.is_file():
            return reference.read_text(encoding="utf-8").strip()
    return value


_REBUILD_FAMILY_SUFFIXES = ("", "-wal", "-shm", "-journal")


def _clear_rebuild_family(temporary: Path, database_path: Path) -> None:
    expected = database_path.with_suffix(".sqlite3.rebuild")
    if temporary != expected or temporary.parent.resolve() != database_path.parent.resolve():
        raise ValueError("temporary index path is outside the registered rebuild family")
    for suffix in _REBUILD_FAMILY_SUFFIXES:
        candidate = Path(f"{temporary}{suffix}")
        if candidate.is_symlink():
            raise ValueError(f"temporary index member is a symlink: {candidate.name}")
        candidate.unlink(missing_ok=True)


def _atomic_replace_index(
    temporary: Path,
    database_path: Path,
    *,
    fail_at: str | None = None,
) -> None:
    SQLiteProjectKnowledgeIndex.prepare_single_file_for_atomic_replace(temporary)
    if database_path.exists():
        SQLiteProjectKnowledgeIndex.prepare_single_file_for_atomic_replace(database_path)
    if fail_at == "before_replace":
        raise RuntimeError("injected failure before atomic index replace")
    os.replace(temporary, database_path)
    directory = os.open(database_path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def build_application(project_root: Path) -> ProjectKnowledgeCommandService:
    root = project_root.resolve()
    registry_path = root / ".factory/project-knowledge/source-registry.json"
    database_path = root / ".factory/index/project-knowledge.sqlite3"
    sync_database_path = root / ".factory/runtime/project-state-sync.sqlite3"
    site_root = root / ".factory/cache/site"
    field_map_path = root / (
        ".factory/workitems/FLOW-CONTRACT-001/drafts/"
        "REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R009.json"
    )

    def indexer(path: Path = database_path) -> ProjectKnowledgeIndexService:
        return ProjectKnowledgeIndexService(
            FileSourceRegistry(
                root,
                registry_path,
                discovery_cache_path=root
                / ".factory/cache/project-knowledge/source-discovery.json",
            ),
            SQLiteProjectKnowledgeIndex(path),
            default_extractors(),
        )

    def check() -> dict[str, Any]:
        return SQLiteKnowledgeQueryStore(database_path, root).check()

    def _progress_snapshot(path: Path) -> dict[str, Any]:
        project_config = json.loads((root / ".factory/project.json").read_text(encoding="utf-8"))
        with closing(sqlite3.connect(path)) as connection:
            generation = connection.execute(
                "SELECT as_of FROM pk_generation WHERE status='current'"
            ).fetchone()
            tasks = connection.execute(
                """
                SELECT entity_id,display_name,summary,lifecycle_status
                  FROM pk_entity WHERE entity_kind='work_item'
                 ORDER BY display_name,entity_id
                """
            ).fetchall()
        prepared_at = str(generation[0])[:10] if generation is not None else "unknown"
        owner = str(project_config.get("owner") or "unknown")
        return {
            "schema_id": "ProjectProgressSnapshot/v2",
            "project_id": str(project_config.get("project_name") or root.name),
            "project": {
                "name": str(project_config.get("project_name") or root.name),
                "code": {"$state": "not_applicable"},
                "manager": owner,
            },
            "document_control": {
                "prepared_by": "AI_EXECUTOR",
                "reviewed_by": owner,
                "prepared_at": prepared_at,
            },
            "sections": {
                "charter": {
                    "background_and_purpose": str(project_config.get("idea") or "未登记"),
                    "goals": "以确定性索引、最小上下文和只读站点支撑项目执行。",
                    "milestones": [],
                    "acceptance_criteria": "正式事实可追溯，派生物可删除重建。",
                    "assumptions": "本地工作区是事实读取边界。",
                    "constraints": "SQLite、HTML 和缓存不进入 Git。",
                    "stakeholders": [],
                },
                "members": {
                    "rows": [{"member_id": owner, "name": owner, "project_role": "项目负责人"}]
                },
                "wbs": {
                    "rows": [
                        {
                            "task_id": str(row[0]),
                            "code": str(row[0]),
                            "task_name": str(row[1]),
                            "activity": str(row[2] or "当前来源未登记更详细的任务说明"),
                            "parent_task_id": None,
                            "dependency_ids": [],
                            "raw_status": str(row[3]),
                        }
                        for row in tasks
                    ],
                    "member_columns": [],
                },
                "schedule": {"rows": []},
                "risks": {"rows": []},
                "communication": {"rows": []},
                "meetings": {"rows": []},
                "status_reports": {"rows": []},
                "changes": {"rows": []},
                "summary": {"project_id": str(project_config.get("project_name") or root.name)},
            },
        }

    def _project_pm(path: Path) -> dict[str, Any]:
        with closing(sqlite3.connect(path)) as connection:
            connection.execute("PRAGMA foreign_keys=ON")
            generation = connection.execute(
                "SELECT generation_id,source_root_sha256 FROM pk_generation WHERE status='current'"
            ).fetchone()
            if generation is None:
                raise ValueError("project knowledge index has no current generation")
            result = ProjectManagementProjector(field_map_path).project(
                _progress_snapshot(path),
                connection,
                generation_id=str(generation[0]),
                source_manifest_sha256=str(generation[1]),
            )
            connection.commit()
        return asdict(result)

    def refresh() -> dict[str, Any]:
        report = indexer().refresh(as_of=_as_of(), git_commit=_git_head(root))
        projection = _project_pm(database_path) if report.changed else None
        return {**asdict(report), "pm_projection": projection}

    def rebuild() -> dict[str, Any]:
        temporary = database_path.with_suffix(".sqlite3.rebuild")
        _clear_rebuild_family(temporary, database_path)
        report = indexer(temporary).refresh(as_of=_as_of(), git_commit=_git_head(root))
        projection = _project_pm(temporary)
        try:
            _atomic_replace_index(temporary, database_path)
        except SQLiteIndexBusyError as error:
            raise QueryFailure("CONCURRENT_WRITER", str(error), exit_code=7) from error
        return {**asdict(report), "pm_projection": projection}

    def enqueue_sync(head: str, scope: str) -> dict[str, Any]:
        now = datetime.now(UTC)
        request = ProjectStateSyncRequest.create(
            fact_high_watermark=head,
            source_scope=scope,
            authorization_profile="local-owner",
            generator_version=RENDERER_VERSION,
            commit_authorized=False,
            requested_at=now,
        )
        receipt = SQLiteProjectStateSyncStore(sync_database_path).enqueue(request, now=now)
        return asdict(receipt)

    def sync_head(scope: str) -> dict[str, Any]:
        return enqueue_sync(_git_head(root), scope)

    def snapshot(**arguments: Any) -> dict[str, Any]:
        if bool(arguments.get("rebuild")):
            index_result: dict[str, Any] | None = rebuild()
        elif not database_path.is_file():
            index_result = rebuild()
        elif bool(arguments.get("check")):
            index_result = check()
        else:
            index_result = refresh()
        profile = str(arguments.get("profile") or "local-owner")
        service = ProjectSiteService(
            SQLiteSiteDataStore(database_path, project_name=root.name),
            ProjectSiteRenderer(),
            AtomicSitePublisher(site_root, database_path=database_path),
        )
        result = service.snapshot(profile=profile, built_at=_as_of())
        result["index"] = index_result
        result["read_only"] = True
        return result

    def maintain(apply: bool) -> dict[str, Any]:
        builds = site_root / "builds"
        protected: list[str] = []
        current = site_root / "current"
        if current.is_symlink():
            protected.append(current.resolve().name)
        if builds.is_dir():
            previous = sorted(
                (
                    child
                    for child in builds.iterdir()
                    if child.is_dir()
                    and child.name not in protected
                    and not child.name.endswith(".tmp")
                ),
                key=lambda child: child.stat().st_mtime_ns,
                reverse=True,
            )
            if previous:
                protected.append(previous[0].name)
        legal_holds = (
            tuple(
                child.name
                for child in builds.iterdir()
                if builds.is_dir() and child.is_dir() and (child / ".legal-hold").is_file()
            )
            if builds.is_dir()
            else ()
        )
        service = ProjectKnowledgeMaintenance(
            project_root=root,
            registrations=(
                CacheRegistration(
                    cache_key="site-builds",
                    relative_root=".factory/cache/site/builds",
                    ttl_seconds=86_400,
                    max_bytes=268_435_456,
                    current_refs=tuple(protected),
                    legal_holds=legal_holds,
                ),
            ),
        )
        now = datetime.now(UTC)
        plan = service.plan(now=now)
        if not apply:
            return {"mode": "dry-run", "plan": asdict(plan)}
        return {
            "mode": "apply",
            "plan": asdict(plan),
            "receipt": asdict(service.apply(plan, now=now)),
        }

    query = ProjectKnowledgeQueryService(SQLiteKnowledgeQueryStore(database_path, root))
    return ProjectKnowledgeCommandService(
        query,
        check_index=check,
        refresh_index=refresh,
        rebuild_index=rebuild,
        enqueue_sync=enqueue_sync,
        sync_head=sync_head,
        snapshot=snapshot,
        maintain=maintain,
    )


def main(argv: list[str] | None = None) -> int:
    return run(
        list(sys.argv[1:] if argv is None else argv),
        build_application(Path.cwd()),
    )


if __name__ == "__main__":
    raise SystemExit(main())
