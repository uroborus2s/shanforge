from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from settings.project_knowledge.maintenance import (
    CacheRegistration,
    ProjectKnowledgeMaintenance,
)

NOW = datetime(2026, 7, 22, 8, 0, tzinfo=UTC)


def _touch(path: Path, *, content: bytes, age_hours: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    timestamp = (NOW - timedelta(hours=age_hours)).timestamp()
    os.utime(path, (timestamp, timestamp))


def test_maintenance_only_deletes_registered_unreferenced_non_held_cache(tmp_path: Path) -> None:
    cache = tmp_path / ".factory/cache/site/builds"
    old = cache / "site-old/page.html"
    current = cache / "site-current/page.html"
    held = cache / "site-held/page.html"
    _touch(old, content=b"old", age_hours=48)
    _touch(current, content=b"current", age_hours=48)
    _touch(held, content=b"held", age_hours=48)
    service = ProjectKnowledgeMaintenance(
        project_root=tmp_path,
        registrations=(
            CacheRegistration(
                cache_key="site",
                relative_root=".factory/cache/site/builds",
                ttl_seconds=86_400,
                max_bytes=1024,
                current_refs=("site-current",),
                legal_holds=("site-held",),
            ),
        ),
    )

    plan = service.plan(now=NOW)
    assert [item.relative_path for item in plan.items] == [".factory/cache/site/builds/site-old"]
    assert old.exists() and current.exists() and held.exists()
    receipt = service.apply(plan, now=NOW)
    assert receipt.deleted_paths == (".factory/cache/site/builds/site-old",)
    assert not old.exists()
    assert current.exists() and held.exists()


def test_maintenance_rejects_symlink_escape_unowned_and_unregistered_targets(
    tmp_path: Path,
) -> None:
    outside = tmp_path / "outside"
    outside.mkdir()
    cache = tmp_path / ".factory/cache/site"
    cache.mkdir(parents=True)
    (cache / "escape").symlink_to(outside, target_is_directory=True)
    service = ProjectKnowledgeMaintenance(
        project_root=tmp_path,
        registrations=(
            CacheRegistration(
                cache_key="site",
                relative_root=".factory/cache/site",
                ttl_seconds=0,
                max_bytes=0,
            ),
        ),
    )
    with pytest.raises(ValueError, match="symlink"):
        service.plan(now=NOW)
