"""Performance gates for warm snapshots, extraction, and durable enqueue."""

from __future__ import annotations

import json
import math
import time
from datetime import UTC, datetime
from pathlib import Path

from application.project_knowledge.site_service import ProjectSiteService
from application.project_knowledge.sync_service import ProjectStateSyncRequest
from domain.project_knowledge.models import AccessClass, SourceDefinition
from runtime.project_knowledge.extractors import JsonExtractor
from runtime.project_knowledge.site_renderer import ProjectSiteRenderer
from settings.project_knowledge.site_publisher import AtomicSitePublisher
from settings.project_knowledge.sync_store import SQLiteProjectStateSyncStore


def _model() -> dict[str, object]:
    return {
        "project": {"name": "performance", "status": "active", "completion": 1},
        "generation": {
            "generation_id": "g1",
            "source_root_sha256": "a" * 64,
            "pm_projection_sha256": "b" * 64,
        },
        "entities": [],
        "edges": [],
        "documents": [],
        "diagnostics": [],
        "versions": [],
        "pm": {},
    }


def _p95(samples: list[float]) -> float:
    return sorted(samples)[math.ceil(0.95 * len(samples)) - 1]


def test_warm_snapshot_cache_lookup_is_under_100ms(tmp_path: Path) -> None:
    model = _model()

    class Data:
        def current_input_token(self, *, profile: str) -> str:
            from runtime.project_knowledge.site_renderer import site_input_token

            return site_input_token(model["generation"], profile)  # type: ignore[arg-type]

        def load(self, *, profile: str = "local-owner") -> dict[str, object]:
            return model

    service = ProjectSiteService(
        Data(), ProjectSiteRenderer(), AtomicSitePublisher(tmp_path / "site")
    )
    service.snapshot(profile="local-owner", built_at="2026-07-22T00:00:00Z")
    samples = []
    for index in range(20):
        started = time.perf_counter()
        receipt = service.snapshot(
            profile="local-owner", built_at=f"2026-07-22T00:00:{index + 1:02d}Z"
        )
        samples.append((time.perf_counter() - started) * 1000)
        assert receipt["cache_hit"] is True
    assert _p95(samples) < 100


def test_ten_thousand_artifact_single_source_extraction_p95_is_under_500ms() -> None:
    source = SourceDefinition(
        source_id="source:performance-json",
        registry_source_id="PERFORMANCE",
        kind="json",
        relative_path="performance/artifacts.json",
        extractor_id="json-v1",
        registry_version="1",
        authority_rank=1,
        access_class=AccessClass.PROJECT,
    )
    content = json.dumps(
        {"artifacts": [{"id": f"ART-{index}", "status": "active"} for index in range(10_000)]},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    samples = []
    for _ in range(5):
        started = time.perf_counter()
        contribution = JsonExtractor().extract(source, content)
        samples.append((time.perf_counter() - started) * 1000)
        assert len(contribution["entities"]) >= 10_000
    assert _p95(samples) < 500


def test_sync_enqueue_is_under_100ms_and_does_not_run_projection(tmp_path: Path) -> None:
    store = SQLiteProjectStateSyncStore(tmp_path / "sync.sqlite3")
    request = ProjectStateSyncRequest.create(
        fact_high_watermark="head-1",
        source_scope="project",
        authorization_profile="local-owner",
        generator_version="ProjectSiteRenderer/v3",
        commit_authorized=False,
        requested_at=datetime(2026, 7, 22, tzinfo=UTC),
    )
    started = time.perf_counter()
    receipt = store.enqueue(request, now=datetime(2026, 7, 22, tzinfo=UTC))
    elapsed_ms = (time.perf_counter() - started) * 1000
    assert receipt.state.value == "queued"
    assert elapsed_ms < 100
    assert not (tmp_path / "site").exists()
