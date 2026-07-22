"""Prepare an auditable, non-destructive migration package for legacy project facts."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

CATALOG_SOURCE = "docs/05-design/ai-sdlc-catalog.source.json"
CATALOG_MANIFEST = "docs/05-design/ai-sdlc-catalog.manifest.json"
PM_EXACT = (
    ".factory/pm/README.md",
    ".factory/pm/project-brief.md",
    ".factory/pm/team-raci.md",
    ".factory/pm/milestones.md",
    ".factory/pm/wbs.md",
    ".factory/pm/risk-register.jsonl",
    ".factory/pm/communication-plan.md",
    ".factory/pm/change-register.jsonl",
    ".factory/pm/closure-report.md",
    ".factory/pm/dashboard.md",
)
PM_GLOBS = (".factory/pm/meeting-notes/*.md", ".factory/pm/status-reports/*.md")


@dataclass(frozen=True, slots=True)
class MigrationItem:
    source: str
    target: str
    disposition: str
    before_sha256: str
    rollback_path: str


@dataclass(frozen=True, slots=True)
class MigrationPrepareReceipt:
    schema_id: str
    job_id: str
    package_path: str
    written: bool
    items: tuple[MigrationItem, ...]
    legacy_delete_count: int
    strong_relations_before: int
    strong_relations_after: int


class ProjectKnowledgeMigrationPreparer:
    def __init__(self, project_root: Path) -> None:
        self._root = project_root.resolve()

    def prepare(self, *, job_id: str, apply: bool) -> MigrationPrepareReceipt:
        if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", job_id) is None:
            raise ValueError("migration job_id is not a safe path token")
        package_relative = f".factory/cache/project-knowledge/migration/{job_id}/after-images"
        sources = self._sources()
        items = tuple(self._item(relative, package_relative) for relative in sources)
        strong_count = self._strong_relation_count()
        receipt = MigrationPrepareReceipt(
            "ProjectKnowledgeMigrationPrepareReceipt/v1",
            job_id,
            package_relative,
            apply,
            items,
            0,
            strong_count,
            strong_count,
        )
        if not apply:
            return receipt
        package = self._root / package_relative
        package.mkdir(parents=True, exist_ok=False)
        for item in items:
            source = self._root / item.source
            rollback = self._root / item.rollback_path
            rollback.parent.mkdir(parents=True, exist_ok=True)
            rollback.write_bytes(source.read_bytes())
            if item.source in {CATALOG_SOURCE, CATALOG_MANIFEST}:
                target = package / item.target
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            else:
                disposition = package / "dispositions" / f"{item.before_sha256}.json"
                disposition.parent.mkdir(parents=True, exist_ok=True)
                disposition.write_text(
                    json.dumps(
                        asdict(item),
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    encoding="utf-8",
                )
        manifest = {
            **asdict(receipt),
            "items": [asdict(item) for item in items],
            "strong_relation_loss": receipt.strong_relations_before
            - receipt.strong_relations_after,
        }
        (package / "migration-plan.json").write_text(
            json.dumps(manifest, ensure_ascii=False, separators=(",", ":"), sort_keys=True),
            encoding="utf-8",
        )
        return receipt

    def _sources(self) -> tuple[str, ...]:
        relative_paths = [CATALOG_SOURCE, CATALOG_MANIFEST, *PM_EXACT]
        for pattern in PM_GLOBS:
            relative_paths.extend(
                path.relative_to(self._root).as_posix()
                for path in sorted(self._root.glob(pattern))
                if path.is_file()
            )
        missing = [relative for relative in relative_paths if not (self._root / relative).is_file()]
        if missing:
            raise FileNotFoundError(f"legacy migration sources are missing: {missing}")
        return tuple(relative_paths)

    def _item(self, source: str, package_relative: str) -> MigrationItem:
        content = (self._root / source).read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        if source == CATALOG_SOURCE:
            target = ".factory/catalog/ai-sdlc-catalog.source.json"
            disposition = "move_stable_machine_config"
        elif source == CATALOG_MANIFEST:
            target = (
                ".factory/workitems/FLOW-CONTRACT-001/evidence/"
                "TASK-DESIGN-001-R019-ai-sdlc-catalog-release-manifest.json"
            )
            disposition = "archive_release_receipt"
        else:
            target = f"project-knowledge://legacy-pm-disposition/{source}"
            disposition = "reconcile_owner_before_remove"
        return MigrationItem(
            source,
            target,
            disposition,
            digest,
            f"{package_relative}/rollback/{source}",
        )

    def _strong_relation_count(self) -> int:
        path = self._root / ".factory/project-knowledge/relation-declarations.json"
        if not path.is_file():
            return 0
        value = json.loads(path.read_text(encoding="utf-8"))
        relations = value.get("relations", []) if isinstance(value, dict) else []
        return sum(
            1
            for relation in relations
            if isinstance(relation, dict) and relation.get("strength") == "strong"
        )
