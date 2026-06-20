from __future__ import annotations

import unittest
from datetime import datetime, timezone

from domain.memory.assembly_models import (
    MemoryProviderAugmentation,
    MemoryProviderBinding,
    RecallPlan,
)
from domain.memory.governance import RecallGovernanceDecision
from domain.memory.models import MemoryKind, MemoryRecord, MemoryScope, MemoryStatus
from runtime.memory.recall_planner import DefaultRecallPlanner
from runtime.memory.recall_ranker import DefaultRecallRanker


class RuntimeMemoryRecallPipelineTests(unittest.TestCase):
    def test_recall_planner_emits_scope_budgets_and_external_augmentation_flag(self) -> None:
        planner = DefaultRecallPlanner(default_limit=6)
        plan = planner.plan(
            RecallGovernanceDecision(
                scope_filters=(
                    (MemoryScope.APP, "demo.writer"),
                    (MemoryScope.PROJECT, "shanforge"),
                ),
                total_limit=6,
                include_external_augmentation=True,
                metadata={
                    "session_id": "session-001",
                    "app_id": "demo.writer",
                    "workflow_id": "compose",
                    "profile_id": "writer-profile",
                },
            ),
        )

        self.assertEqual(
            plan.scope_filters,
            ((MemoryScope.APP, "demo.writer"), (MemoryScope.PROJECT, "shanforge")),
        )
        self.assertEqual(plan.total_limit, 6)
        self.assertEqual(plan.scope_budgets["app:demo.writer"], 3)
        self.assertEqual(plan.scope_budgets["project:shanforge"], 3)
        self.assertTrue(plan.include_external_augmentation)
        self.assertEqual(plan.metadata["profile_id"], "writer-profile")
        self.assertEqual(
            plan.within_scope_order,
            ("confidence:desc", "created_at:asc", "id:asc"),
        )
        self.assertEqual(
            plan.overflow_order,
            ("scope_order:asc", "confidence:desc", "created_at:asc", "id:asc"),
        )

    def test_recall_ranker_respects_scope_budgets_and_total_limit(self) -> None:
        ranker = DefaultRecallRanker()
        plan = RecallPlan(
            scope_filters=((MemoryScope.APP, "demo.writer"), (MemoryScope.PROJECT, "shanforge")),
            allowed_statuses=(MemoryStatus.ACCEPTED,),
            total_limit=3,
            scope_budgets={"app:demo.writer": 1, "project:shanforge": 2},
            include_external_augmentation=True,
        )
        records = (
            MemoryRecord(
                id="app-01",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="App One",
                body="App body 1",
                status=MemoryStatus.ACCEPTED,
                confidence=0.91,
                supporting_refs=("event://1",),
            ),
            MemoryRecord(
                id="app-02",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="App Two",
                body="App body 2",
                status=MemoryStatus.ACCEPTED,
                confidence=0.82,
                supporting_refs=("event://2",),
            ),
            MemoryRecord(
                id="project-01",
                kind=MemoryKind.DECLARATIVE,
                scope=MemoryScope.PROJECT,
                scope_key="shanforge",
                title="Project One",
                body="Project body 1",
                status=MemoryStatus.ACCEPTED,
                confidence=0.95,
                supporting_refs=("event://3",),
            ),
            MemoryRecord(
                id="project-02",
                kind=MemoryKind.DECLARATIVE,
                scope=MemoryScope.PROJECT,
                scope_key="shanforge",
                title="Project Two",
                body="Project body 2",
                status=MemoryStatus.ACCEPTED,
                confidence=0.88,
                supporting_refs=("event://4",),
            ),
        )

        ranked = ranker.rank(
            plan=plan,
            records=records,
            augmentation=MemoryProviderAugmentation(
                binding=MemoryProviderBinding(provider_id="jsonl"),
                recall_block="External recall block.",
            ),
        )

        self.assertEqual(
            tuple(record.id for record in ranked),
            ("app-01", "project-01", "project-02"),
        )

    def test_recall_ranker_respects_explicit_sort_orders_from_plan(self) -> None:
        ranker = DefaultRecallRanker()
        plan = RecallPlan(
            scope_filters=((MemoryScope.APP, "demo.writer"),),
            total_limit=2,
            scope_budgets={"app:demo.writer": 2},
            within_scope_order=("created_at:desc", "id:desc"),
            overflow_order=("scope_order:asc", "created_at:desc", "id:desc"),
        )
        records = (
            MemoryRecord(
                id="app-01",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="Older",
                body="Body 1",
                status=MemoryStatus.ACCEPTED,
                confidence=0.10,
                supporting_refs=("event://1",),
                created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
            ),
            MemoryRecord(
                id="app-02",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="Newer",
                body="Body 2",
                status=MemoryStatus.ACCEPTED,
                confidence=0.99,
                supporting_refs=("event://2",),
                created_at=datetime(2026, 4, 2, tzinfo=timezone.utc),
            ),
        )

        ranked = ranker.rank(plan=plan, records=records)

        self.assertEqual(tuple(record.id for record in ranked), ("app-02", "app-01"))


if __name__ == "__main__":
    unittest.main()
