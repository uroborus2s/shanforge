from __future__ import annotations

import unittest
from dataclasses import dataclass, field
from datetime import datetime, timezone

from domain.agent_app.models import AgentApp, AgentAppMetadata
from domain.memory.assembly_models import MemoryProviderBinding
from domain.memory.governance import (
    MemoryLifecyclePolicy,
    MemoryProviderGovernanceDecision,
    MemoryProviderGovernancePolicy,
    RecallGovernanceDecision,
    RecallGovernancePolicy,
)
from domain.memory.models import (
    EvidenceRecord,
    MemoryDistillationSample,
    MemoryKind,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleQueueEntry,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
)
from domain.memory.service import DefaultMemoryDomainService
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession, SessionEvent
from domain.workflow.models import WorkflowDefinition
from domain.workflow.steps import StepKind, WorkflowStep
from runtime.memory.provider_manager import DefaultMemoryProviderManager


def _build_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        id="compose",
        name="Compose",
        description="Draft and refine a response.",
        steps=(
            WorkflowStep(
                id="draft",
                name="Draft",
                kind=StepKind.PROMPT,
                instruction="Create a first draft.",
                output_key="draft",
            ),
        ),
    )


def _build_app() -> AgentApp:
    workflow = _build_workflow()
    return AgentApp(
        metadata=AgentAppMetadata(
            id="demo.writer",
            name="Writer",
            domain="demo",
        ),
        workflows={workflow.id: workflow},
        default_workflow_id=workflow.id,
    )


@dataclass(slots=True)
class _MemoryRepository:
    records: list[MemoryRecord] = field(default_factory=list)
    scan_calls: list[tuple[tuple[tuple[MemoryScope, str], ...], tuple[MemoryStatus, ...]]] = (
        field(default_factory=list)
    )

    def save_memory_record(self, record: MemoryRecord) -> None:
        for index, existing in enumerate(self.records):
            if existing.id == record.id:
                self.records[index] = record
                break
        else:
            self.records.append(record)

    def scan_memory_records(
        self,
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        allowed_statuses: tuple[MemoryStatus, ...],
    ) -> tuple[MemoryRecord, ...]:
        self.scan_calls.append((scope_filters, allowed_statuses))
        scope_filter_set = set(scope_filters)
        allowed_status_set = set(allowed_statuses)
        return tuple(
            record
            for record in self.records
            if (record.scope, record.scope_key) in scope_filter_set
            and record.status in allowed_status_set
        )

    def query_memory_records(self, query: object) -> tuple[MemoryRecord, ...]:
        del query
        return ()


@dataclass(slots=True)
class _EvidenceRepository:
    records: list[EvidenceRecord] = field(default_factory=list)

    def save_evidence(self, record: EvidenceRecord) -> None:
        self.records.append(record)

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(record for record in self.records if record.session_id == session_id)


@dataclass(slots=True)
class _DatasetRepository:
    samples: list[MemoryDistillationSample] = field(default_factory=list)

    def save_sample(self, sample: MemoryDistillationSample) -> None:
        self.samples.append(sample)

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return tuple(sample for sample in self.samples if sample.session_id == session_id)


@dataclass(slots=True)
class _LifecycleQueueRepository:
    entries: list[MemoryLifecycleQueueEntry] = field(default_factory=list)

    def list_lifecycle_queue_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleQueueEntry, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def replace_lifecycle_queue_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
    ) -> None:
        retained = [entry for entry in self.entries if entry.session_id != session_id]
        self.entries = [*retained, *entries]


@dataclass(slots=True)
class _LifecycleAuditRepository:
    entries: list[MemoryLifecycleAuditEntry] = field(default_factory=list)

    def list_lifecycle_audit_entries(
        self,
        session_id: str,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def append_lifecycle_audit_entries(
        self,
        session_id: str,
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> None:
        del session_id
        self.entries.extend(entries)


@dataclass(slots=True)
class _RecordingExternalMemoryProvider:
    initialized: list[str] = field(default_factory=list)
    synced: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    ended: list[str] = field(default_factory=list)
    lifecycle_applied: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        del binding
        self.initialized.append(session_id)

    def prefetch(self, query: object, session_id: str) -> str:
        del query, session_id
        return "External recall block."

    def sync_turn(self, session_id: str, latest_events: tuple[SessionEvent, ...]) -> None:
        self.synced.append((session_id, tuple(event.id for event in latest_events)))

    def on_session_end(self, session_id: str, distillation_result: object) -> None:
        del distillation_result
        self.ended.append(session_id)

    def on_lifecycle_apply(
        self,
        session_id: str,
        apply_result: object,
    ) -> None:
        applied_record_ids = getattr(apply_result, "applied_record_ids", ())
        self.lifecycle_applied.append((session_id, tuple(applied_record_ids)))

    def on_delegation(self, digest: SubAgentDigest) -> None:
        del digest


@dataclass(slots=True, frozen=True)
class _ProjectOnlyRecallGovernancePolicy(RecallGovernancePolicy):
    def decide(
        self,
        session: AgentSession,
        app_id: str,
        workflow_id: str,
        profile_id: str | None,
        project_scope_key: str | None,
        provider_decision: MemoryProviderGovernanceDecision | None,
        default_limit: int | None = None,
    ) -> RecallGovernanceDecision:
        del app_id, profile_id, provider_decision, default_limit
        assert project_scope_key is not None
        return RecallGovernanceDecision(
            scope_filters=((MemoryScope.PROJECT, project_scope_key),),
            total_limit=1,
            include_external_augmentation=False,
            metadata={
                "session_id": session.id,
                "workflow_id": workflow_id,
                "policy_id": "project-only",
            },
        )


@dataclass(slots=True, frozen=True)
class _DenyAugmentationProviderGovernancePolicy(MemoryProviderGovernancePolicy):
    def decide(
        self,
        binding: MemoryProviderBinding | None,
    ) -> MemoryProviderGovernanceDecision:
        if binding is None:
            return super().decide(binding)
        return MemoryProviderGovernanceDecision(
            binding=binding,
            allow_augmentation=False,
            metadata={"policy_id": "deny-augmentation"},
        )


@dataclass(slots=True, frozen=True)
class _NoWritebackProviderGovernancePolicy(MemoryProviderGovernancePolicy):
    def decide(
        self,
        binding: MemoryProviderBinding | None,
    ) -> MemoryProviderGovernanceDecision:
        if binding is None:
            return super().decide(binding)
        return MemoryProviderGovernanceDecision(
            binding=binding,
            allow_augmentation=True,
            metadata={"policy_id": "no-writeback"},
        )


class DomainMemoryGovernanceTests(unittest.TestCase):
    def test_recall_governance_policy_emits_domain_decision(self) -> None:
        policy = RecallGovernancePolicy(default_limit=6)
        session = AgentSession(
            id="session-001",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Continue the draft.",
        )

        decision = policy.decide(
            session=session,
            app_id="demo.writer",
            workflow_id="compose",
            profile_id="writer-profile",
            project_scope_key="shanforge",
            provider_decision=MemoryProviderGovernanceDecision(
                binding=MemoryProviderBinding(
                    provider_id="jsonl",
                    namespace="writer-profile",
                ),
                allow_augmentation=True,
            ),
        )

        self.assertEqual(
            decision.scope_filters,
            ((MemoryScope.APP, "demo.writer"), (MemoryScope.PROJECT, "shanforge")),
        )
        self.assertEqual(decision.allowed_statuses, (MemoryStatus.ACCEPTED,))
        self.assertEqual(decision.total_limit, 6)
        self.assertTrue(decision.include_external_augmentation)
        self.assertEqual(decision.metadata["profile_id"], "writer-profile")
        plan = decision.to_recall_plan(
            scope_budgets={
                "app:demo.writer": 3,
                "project:shanforge": 3,
            }
        )
        self.assertEqual(plan.scope_budgets["app:demo.writer"], 3)
        self.assertEqual(plan.scope_budgets["project:shanforge"], 3)

    def test_provider_governance_policy_freezes_writeback_and_delegation_gates(self) -> None:
        policy = MemoryProviderGovernancePolicy()
        read_only = policy.decide(
            MemoryProviderBinding(
                provider_id="remote_http",
                writable=False,
            )
        )
        writable = policy.decide(
            MemoryProviderBinding(
                provider_id="remote_http",
                writable=True,
            )
        )
        digest = SubAgentDigest(
            parent_session_id="session-001",
            child_session_id="child-001",
            summary="Child digest",
        )
        shared_digest = SubAgentDigest(
            parent_session_id="session-001",
            child_session_id="child-002",
            summary="Shared child digest",
            metadata={"shared_provider_write_capability": True},
        )

        self.assertTrue(read_only.allow_augmentation)
        self.assertFalse(read_only.allow_sync_turn)
        self.assertFalse(read_only.allow_session_end_writeback)
        self.assertFalse(read_only.allow_lifecycle_writeback)
        self.assertFalse(read_only.allows_delegation(digest))

        self.assertTrue(writable.allow_sync_turn)
        self.assertTrue(writable.allow_session_end_writeback)
        self.assertTrue(writable.allow_lifecycle_writeback)
        self.assertFalse(writable.allows_delegation(digest))
        self.assertTrue(writable.allows_delegation(shared_digest))

    def test_lifecycle_policy_freezes_default_transition_rules(self) -> None:
        policy = MemoryLifecyclePolicy()

        initial_accept = policy.evaluate_transition(
            current_status=None,
            target_status=MemoryStatus.ACCEPTED,
        )
        supersede = policy.evaluate_transition(
            current_status=MemoryStatus.ACCEPTED,
            target_status=MemoryStatus.SUPERSEDED,
        )
        forget = policy.evaluate_transition(
            current_status=MemoryStatus.ACCEPTED,
            target_status=MemoryStatus.FORGOTTEN,
        )
        reject_superseded = policy.evaluate_transition(
            current_status=MemoryStatus.SUPERSEDED,
            target_status=MemoryStatus.ACCEPTED,
        )

        self.assertTrue(initial_accept.allowed)
        self.assertEqual(initial_accept.reason, "initial_transition_allowed")
        self.assertTrue(supersede.allowed)
        self.assertEqual(supersede.reason, "transition_allowed")
        self.assertTrue(forget.allowed)
        self.assertIn("forgotten", forget.metadata["allowed_targets"])
        self.assertFalse(reject_superseded.allowed)
        self.assertEqual(reject_superseded.reason, "transition_not_allowed")

    def test_lifecycle_policy_marks_conflicting_record_superseded(self) -> None:
        policy = MemoryLifecyclePolicy()
        older = MemoryRecord(
            id="memory-older",
            kind=MemoryKind.DECLARATIVE,
            scope=MemoryScope.APP,
            scope_key="demo.writer",
            title="Writer style rule",
            body="Use the original style.",
            status=MemoryStatus.ACCEPTED,
            confidence=0.55,
            supporting_refs=("event://1",),
            created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
            metadata={"conflict_key": "writer-style"},
        )
        newer = MemoryRecord(
            id="memory-newer",
            kind=MemoryKind.DECLARATIVE,
            scope=MemoryScope.APP,
            scope_key="demo.writer",
            title="Writer style rule",
            body="Use the approved style.",
            status=MemoryStatus.ACCEPTED,
            confidence=0.88,
            supporting_refs=("event://2",),
            created_at=datetime(2026, 4, 2, tzinfo=timezone.utc),
            metadata={"conflict_key": "writer-style"},
        )

        decision = policy.evaluate_record(older, related_records=(older, newer))

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.target_status, MemoryStatus.SUPERSEDED)
        self.assertEqual(decision.reason, "conflict_superseded")
        self.assertEqual(decision.metadata["superseded_by_record_id"], "memory-newer")
        self.assertTrue(decision.metadata["hidden"])

    def test_lifecycle_policy_honors_forced_manual_override(self) -> None:
        policy = MemoryLifecyclePolicy()
        forgotten = MemoryRecord(
            id="memory-forgotten",
            kind=MemoryKind.EPISODIC,
            scope=MemoryScope.APP,
            scope_key="demo.writer",
            title="Forgotten rule",
            body="This memory was hidden.",
            status=MemoryStatus.FORGOTTEN,
            confidence=0.8,
            supporting_refs=("event://1",),
            metadata={
                "manual_override_status": "accepted",
                "manual_override_reason": "review_restored",
                "manual_override_actor": "memory-reviewer",
            },
        )

        decision = policy.evaluate_record(forgotten)

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.target_status, MemoryStatus.ACCEPTED)
        self.assertEqual(decision.reason, "manual_override_applied")
        self.assertTrue(decision.metadata["forced"])
        self.assertEqual(decision.metadata["manual_override_actor"], "memory-reviewer")

    def test_lifecycle_policy_forgets_decayed_record(self) -> None:
        policy = MemoryLifecyclePolicy()
        decayed = MemoryRecord(
            id="memory-decayed",
            kind=MemoryKind.DECLARATIVE,
            scope=MemoryScope.PROJECT,
            scope_key="shanforge",
            title="Stale project fact",
            body="This fact has not been reinforced.",
            status=MemoryStatus.ACCEPTED,
            confidence=0.72,
            supporting_refs=("event://1",),
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            metadata={
                "decay_after_days": 30,
                "last_reinforced_at": "2026-01-05T00:00:00+00:00",
            },
        )

        decision = policy.evaluate_record(
            decayed,
            as_of=datetime(2026, 3, 1, tzinfo=timezone.utc),
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.target_status, MemoryStatus.FORGOTTEN)
        self.assertEqual(decision.reason, "decay_expired")
        self.assertEqual(decision.metadata["decay_after_days"], 30)
        self.assertTrue(decision.metadata["hidden"])

    def test_prepare_session_uses_recall_governance_policy(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="app-001",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key="demo.writer",
                    title="App memory",
                    body="App recall body",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.82,
                    supporting_refs=("event://1",),
                ),
                MemoryRecord(
                    id="project-001",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.PROJECT,
                    scope_key="shanforge",
                    title="Project memory",
                    body="Project recall body",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.95,
                    supporting_refs=("event://2",),
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            default_project_scope_key="shanforge",
            recall_governance_policy=_ProjectOnlyRecallGovernancePolicy(),
        )
        session = AgentSession(
            id="session-001",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Continue the draft.",
        )

        service.prepare_session(session, app, workflow)

        self.assertEqual(
            memory_repo.scan_calls[0][0],
            ((MemoryScope.PROJECT, "shanforge"),),
        )

    def test_apply_lifecycle_persists_selected_updates(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-decayed",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Stale episodic note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
        )
        session = AgentSession(
            id="session-apply",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Review lifecycle.",
        )

        review = service.review_lifecycle(session)
        apply_result = service.apply_lifecycle(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older", "memory-decayed"),
        )

        records_by_id = {record.id: record for record in memory_repo.records}

        self.assertEqual(review.evaluations[1].reason, "conflict_superseded")
        self.assertEqual(
            tuple(item.record_id for item in apply_result.evaluations),
            ("memory-older", "memory-decayed"),
        )
        self.assertEqual(
            apply_result.applied_record_ids,
            ("memory-older", "memory-decayed"),
        )
        self.assertEqual(records_by_id["memory-older"].status, MemoryStatus.SUPERSEDED)
        self.assertEqual(records_by_id["memory-decayed"].status, MemoryStatus.FORGOTTEN)
        self.assertEqual(
            records_by_id["memory-older"].metadata["lifecycle_applied_by"],
            "memory-reviewer",
        )

    def test_load_lifecycle_queue_projects_actionable_items_and_batch_apply_by_filter(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-decayed",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Stale episodic note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
        )
        session = AgentSession(
            id="session-queue",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Queue lifecycle updates.",
        )

        default_queue = service.load_lifecycle_queue(session)
        forgotten_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
        )
        apply_result = service.apply_lifecycle(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
        )

        records_by_id = {record.id: record for record in memory_repo.records}

        self.assertEqual(default_queue.selected_record_ids, ("memory-older", "memory-decayed"))
        self.assertEqual(
            tuple(item.record_id for item in default_queue.items),
            ("memory-older", "memory-decayed"),
        )
        self.assertEqual(forgotten_queue.selected_record_ids, ("memory-decayed",))
        self.assertEqual(
            tuple(item.record_id for item in forgotten_queue.items),
            ("memory-decayed",),
        )
        self.assertEqual(
            apply_result.selected_record_ids,
            ("memory-decayed",),
        )
        self.assertEqual(apply_result.queue_filter.effective_statuses, (MemoryStatus.FORGOTTEN,))
        self.assertEqual(records_by_id["memory-older"].status, MemoryStatus.ACCEPTED)
        self.assertEqual(records_by_id["memory-decayed"].status, MemoryStatus.FORGOTTEN)

    def test_apply_lifecycle_uses_provider_governance_before_lifecycle_writeback(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        provider = _RecordingExternalMemoryProvider()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-decayed",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Stale episodic note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            memory_provider_manager=DefaultMemoryProviderManager(provider=provider),
        )
        session = AgentSession(
            id="session-provider-apply",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Apply lifecycle and sync provider.",
            context={
                "memory_provider_binding": MemoryProviderBinding(
                    provider_id="jsonl",
                    namespace="writer-profile",
                    writable=True,
                ).to_mapping()
            },
        )
        service.prepare_session(session, app, workflow)

        apply_result = service.apply_lifecycle(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
        )

        self.assertEqual(
            provider.lifecycle_applied,
            [("session-provider-apply", ("memory-decayed",))],
        )
        self.assertTrue(apply_result.metadata["provider_writeback_triggered"])
        self.assertEqual(apply_result.metadata["provider_id"], "jsonl")

    def test_update_lifecycle_queue_persists_dismissed_review_state(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-review",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Queue lifecycle updates.",
        )

        initial_queue = service.load_lifecycle_queue(session)
        update_result = service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="keep this visible for now",
            resolution=MemoryLifecycleReviewResolution.KEEP_CURRENT,
        )
        default_queue = service.load_lifecycle_queue(session)
        dismissed_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
        )

        self.assertEqual(initial_queue.selected_record_ids, ("memory-older",))
        self.assertEqual(update_result.updated_record_ids, ("memory-older",))
        self.assertEqual(update_result.review_status, MemoryLifecycleQueueReviewStatus.DISMISSED)
        self.assertEqual(
            update_result.resolution,
            MemoryLifecycleReviewResolution.KEEP_CURRENT,
        )
        self.assertEqual(default_queue.selected_record_ids, ())
        self.assertEqual(tuple(item.record_id for item in default_queue.items), ())
        self.assertEqual(tuple(item.record_id for item in dismissed_queue.items), ("memory-older",))
        self.assertEqual(
            dismissed_queue.items[0].review_status,
            MemoryLifecycleQueueReviewStatus.DISMISSED,
        )
        self.assertEqual(
            dismissed_queue.items[0].review_resolution,
            MemoryLifecycleReviewResolution.KEEP_CURRENT,
        )
        self.assertTrue(dismissed_queue.items[0].resolution_required)
        self.assertEqual(
            tuple(
                option.resolution
                for option in dismissed_queue.items[0].resolution_options
            ),
            (
                MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                MemoryLifecycleReviewResolution.KEEP_CURRENT,
                MemoryLifecycleReviewResolution.DEFERRED,
            ),
        )
        self.assertEqual(dismissed_queue.items[0].reviewed_by, "memory-reviewer")
        self.assertEqual(dismissed_queue.items[0].review_note, "keep this visible for now")
        self.assertEqual(
            tuple(entry.record_id for entry in queue_repo.list_lifecycle_queue_entries(session.id)),
            ("memory-current", "memory-older"),
        )
        audit_log = service.load_lifecycle_audit(session)
        self.assertEqual(tuple(entry.record_id for entry in audit_log.entries), ("memory-older",))
        self.assertEqual(
            audit_log.entries[0].action,
            MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,
        )
        self.assertEqual(
            audit_log.entries[0].queue_review_status,
            MemoryLifecycleQueueReviewStatus.DISMISSED,
        )
        self.assertEqual(
            audit_log.entries[0].resolution,
            MemoryLifecycleReviewResolution.KEEP_CURRENT,
        )
        self.assertEqual(audit_log.entries[0].note, "keep this visible for now")
        self.assertEqual(
            audit_log.entries[0].metadata["previous_review_status"],
            MemoryLifecycleQueueReviewStatus.PENDING.value,
        )

    def test_update_lifecycle_queue_projects_batch_selection_from_queue_filter(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-decayed-a",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="First stale note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
                MemoryRecord(
                    id="memory-decayed-b",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Second stale note",
                    body="This note should also decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.66,
                    supporting_refs=("event://3",),
                    created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-06T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-filter-update",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Dismiss all decayed lifecycle items.",
        )

        service.load_lifecycle_queue(session)
        update_result = service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss stale items in batch",
            resolution=MemoryLifecycleReviewResolution.STALE_SIGNAL,
        )
        dismissed_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
        )

        self.assertCountEqual(
            update_result.requested_record_ids,
            ("memory-decayed-a", "memory-decayed-b"),
        )
        self.assertCountEqual(
            update_result.updated_record_ids,
            ("memory-decayed-a", "memory-decayed-b"),
        )
        self.assertCountEqual(
            tuple(item.record_id for item in dismissed_queue.items),
            ("memory-decayed-a", "memory-decayed-b"),
        )
        for item in dismissed_queue.items:
            self.assertTrue(item.resolution_required)
            self.assertEqual(
                tuple(option.resolution for option in item.resolution_options),
                (
                    MemoryLifecycleReviewResolution.STALE_SIGNAL,
                    MemoryLifecycleReviewResolution.KEEP_CURRENT,
                    MemoryLifecycleReviewResolution.DEFERRED,
                ),
            )
        audit_log = service.load_lifecycle_audit(session)
        self.assertCountEqual(
            tuple(entry.record_id for entry in audit_log.entries),
            ("memory-decayed-a", "memory-decayed-b"),
        )

    def test_apply_lifecycle_marks_queue_entries_as_applied(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-decayed",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Stale episodic note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-apply",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Apply lifecycle queue updates.",
        )

        service.load_lifecycle_queue(session)
        apply_result = service.apply_lifecycle(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
        )
        applied_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.APPLIED,),
            ),
        )

        self.assertEqual(apply_result.applied_record_ids, ("memory-decayed",))
        self.assertEqual(tuple(item.record_id for item in applied_queue.items), ("memory-decayed",))
        self.assertEqual(
            applied_queue.items[0].review_status,
            MemoryLifecycleQueueReviewStatus.APPLIED,
        )
        self.assertEqual(applied_queue.items[0].current_status, MemoryStatus.FORGOTTEN)
        self.assertEqual(applied_queue.items[0].effective_status, MemoryStatus.FORGOTTEN)
        applied_audit = service.load_lifecycle_audit(
            session,
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.LIFECYCLE_APPLIED,),
            ),
        )
        self.assertEqual(
            tuple(entry.record_id for entry in applied_audit.entries),
            ("memory-decayed",),
        )
        self.assertEqual(
            applied_audit.entries[0].queue_review_status,
            MemoryLifecycleQueueReviewStatus.APPLIED,
        )
        self.assertEqual(
            applied_audit.entries[0].effective_status,
            MemoryStatus.FORGOTTEN,
        )

    def test_reopen_lifecycle_queue_restores_pending_selection_and_emits_reopen_audit(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-reopen",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Reopen lifecycle queue updates.",
        )

        service.load_lifecycle_queue(session)
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss for now",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        reopen_result = service.reopen_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            note="reopen for reconsideration",
        )
        pending_queue = service.load_lifecycle_queue(session)
        reopen_audit = service.load_lifecycle_audit(
            session,
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.REVIEW_REOPENED,),
            ),
        )

        self.assertEqual(reopen_result.review_status, MemoryLifecycleQueueReviewStatus.PENDING)
        self.assertEqual(reopen_result.updated_record_ids, ("memory-older",))
        self.assertEqual(pending_queue.selected_record_ids, ("memory-older",))
        self.assertIsNone(pending_queue.items[0].review_resolution)
        self.assertEqual(
            tuple(entry.record_id for entry in reopen_audit.entries),
            ("memory-older",),
        )
        self.assertEqual(
            reopen_audit.entries[0].queue_review_status,
            MemoryLifecycleQueueReviewStatus.PENDING,
        )
        self.assertIsNone(reopen_audit.entries[0].resolution)
        self.assertEqual(reopen_audit.entries[0].note, "reopen for reconsideration")

    def test_reopen_lifecycle_queue_projects_batch_selection_from_queue_filter(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-decayed-a",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="First stale note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                ),
                MemoryRecord(
                    id="memory-decayed-b",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Second stale note",
                    body="This note should also decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.66,
                    supporting_refs=("event://3",),
                    created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-06T00:00:00+00:00",
                    },
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-filter-reopen",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Reopen all dismissed lifecycle items.",
        )

        service.load_lifecycle_queue(session)
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss stale items in batch",
            resolution=MemoryLifecycleReviewResolution.STALE_SIGNAL,
        )
        reopen_result = service.reopen_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
            note="reopen stale items in batch",
        )
        pending_queue = service.load_lifecycle_queue(session)
        reopen_audit = service.load_lifecycle_audit(
            session,
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.REVIEW_REOPENED,),
            ),
        )

        self.assertCountEqual(
            reopen_result.requested_record_ids,
            ("memory-decayed-a", "memory-decayed-b"),
        )
        self.assertCountEqual(
            reopen_result.updated_record_ids,
            ("memory-decayed-a", "memory-decayed-b"),
        )
        self.assertCountEqual(
            pending_queue.selected_record_ids,
            ("memory-decayed-a", "memory-decayed-b"),
        )
        self.assertCountEqual(
            tuple(entry.record_id for entry in reopen_audit.entries),
            ("memory-decayed-a", "memory-decayed-b"),
        )

    def test_update_lifecycle_queue_requires_record_ids_or_queue_filter(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        service = DefaultMemoryDomainService(
            memory_records=_MemoryRepository(),
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
        )
        session = AgentSession(
            id="session-queue-selection-required",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Review lifecycle queue.",
        )

        with self.assertRaisesRegex(
            ValueError,
            "requires record_ids or queue_filter",
        ):
            service.update_lifecycle_queue(
                session,
                actor="memory-reviewer",
                review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            )

    def test_update_lifecycle_queue_same_status_updates_note_and_emits_note_audit(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-queue-note",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Annotate lifecycle queue updates.",
        )

        service.load_lifecycle_queue(session)
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss for now",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        note_result = service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="conflict confirmed by reviewer",
        )
        dismissed_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
        )
        note_audit = service.load_lifecycle_audit(
            session,
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.REVIEW_NOTE_UPDATED,),
            ),
        )

        self.assertEqual(note_result.updated_record_ids, ("memory-older",))
        self.assertEqual(
            dismissed_queue.items[0].review_resolution,
            MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        self.assertEqual(dismissed_queue.items[0].review_note, "conflict confirmed by reviewer")
        self.assertEqual(
            tuple(entry.record_id for entry in note_audit.entries),
            ("memory-older",),
        )
        self.assertEqual(
            note_audit.entries[0].queue_review_status,
            MemoryLifecycleQueueReviewStatus.DISMISSED,
        )
        self.assertEqual(
            note_audit.entries[0].resolution,
            MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        self.assertEqual(
            note_audit.entries[0].metadata["previous_review_resolution"],
            MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED.value,
        )
        self.assertEqual(note_audit.entries[0].note, "conflict confirmed by reviewer")

    def test_load_lifecycle_audit_can_project_latest_entry_per_record(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        queue_repo = _LifecycleQueueRepository()
        audit_repo = _LifecycleAuditRepository()
        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older style rule",
                    body="Use the original style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current style rule",
                    body="Use the approved style.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "writer-style"},
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            lifecycle_queue_records=queue_repo,
            lifecycle_audit_records=audit_repo,
        )
        session = AgentSession(
            id="session-audit-latest-per-record",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Inspect latest lifecycle audit state.",
        )

        service.load_lifecycle_queue(session)
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss for now",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="conflict confirmed by reviewer",
        )
        service.reopen_lifecycle_queue(
            session,
            actor="memory-reviewer",
            record_ids=("memory-older",),
            note="reopen for reconsideration",
        )

        latest_only_audit = service.load_lifecycle_audit(
            session,
            audit_filter=MemoryLifecycleAuditFilter(
                latest_per_record_only=True,
            ),
        )

        self.assertEqual(
            tuple(entry.record_id for entry in latest_only_audit.entries),
            ("memory-older",),
        )
        self.assertEqual(
            latest_only_audit.entries[0].action,
            MemoryLifecycleAuditAction.REVIEW_REOPENED,
        )
        self.assertEqual(
            latest_only_audit.entries[0].queue_review_status,
            MemoryLifecycleQueueReviewStatus.PENDING,
        )
        self.assertIsNone(latest_only_audit.entries[0].resolution)

    def test_prepare_session_uses_provider_governance_before_prefetch(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        provider = _RecordingExternalMemoryProvider()
        service = DefaultMemoryDomainService(
            memory_records=_MemoryRepository(),
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            memory_provider_manager=DefaultMemoryProviderManager(provider=provider),
            provider_governance_policy=_DenyAugmentationProviderGovernancePolicy(),
        )
        session = AgentSession(
            id="session-001",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Continue the draft.",
            context={
                "memory_provider_binding": MemoryProviderBinding(
                    provider_id="jsonl",
                    namespace="writer-profile",
                ).to_mapping()
            },
        )

        service.prepare_session(session, app, workflow)

        self.assertEqual(provider.initialized, [])
        self.assertNotIn("external_memory_recall_block", session.context)

    def test_distill_session_uses_provider_governance_before_writeback(self) -> None:
        provider = _RecordingExternalMemoryProvider()
        service = DefaultMemoryDomainService(
            memory_records=_MemoryRepository(),
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            memory_provider_manager=DefaultMemoryProviderManager(provider=provider),
            provider_governance_policy=_NoWritebackProviderGovernancePolicy(),
        )
        session = AgentSession(
            id="session-001",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Continue the draft.",
            context={
                "memory_provider_binding": MemoryProviderBinding(
                    provider_id="jsonl",
                    namespace="writer-profile",
                    writable=True,
                ).to_mapping()
            },
            events=[
                SessionEvent(
                    type="step_completed",
                    summary="Completed draft.",
                    payload={"step_id": "draft"},
                )
            ],
        )

        service.distill_session(session)

        self.assertEqual(provider.synced, [])
        self.assertEqual(provider.ended, [])


if __name__ == "__main__":
    unittest.main()
