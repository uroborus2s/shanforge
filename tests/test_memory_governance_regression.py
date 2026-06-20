from __future__ import annotations

import unittest
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Mapping

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
    CandidateDrafts,
    DistillationResult,
    EvidenceRecord,
    MemoryCandidate,
    MemoryDistillationSample,
    MemoryKind,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
    RecallQuery,
    SummaryResult,
)
from domain.memory.service import DefaultMemoryDomainService
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession, SessionArtifact, SessionEvent
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
    entries: list[object] = field(default_factory=list)

    def list_lifecycle_queue_entries(self, session_id: str) -> tuple[object, ...]:
        return tuple(entry for entry in self.entries if entry.session_id == session_id)

    def replace_lifecycle_queue_entries(
        self,
        session_id: str,
        entries: tuple[object, ...],
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
class _DigestStore:
    digests: list[SubAgentDigest] = field(default_factory=list)

    def save(self, digest: SubAgentDigest) -> None:
        self.digests.append(digest)

    def list_by_session(self, session_id: str) -> tuple[SubAgentDigest, ...]:
        return tuple(digest for digest in self.digests if digest.parent_session_id == session_id)


@dataclass(slots=True)
class _TracingProvider:
    initialized: list[tuple[str, MemoryProviderBinding]] = field(default_factory=list)
    synced: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    ended: list[tuple[str, tuple[str, ...]]] = field(default_factory=list)
    delegated: list[str] = field(default_factory=list)

    def initialize(self, binding: MemoryProviderBinding, session_id: str) -> None:
        self.initialized.append((session_id, binding))

    def prefetch(self, query: RecallQuery, session_id: str) -> str:
        del query, session_id
        return "Remote recall block."

    def sync_turn(self, session_id: str, latest_events: tuple[SessionEvent, ...]) -> None:
        self.synced.append((session_id, tuple(event.id for event in latest_events)))

    def on_session_end(self, session_id: str, distillation_result: DistillationResult) -> None:
        self.ended.append(
            (session_id, tuple(record.id for record in distillation_result.promoted_records))
        )

    def on_delegation(self, digest: SubAgentDigest) -> None:
        self.delegated.append(digest.child_session_id)

    def contract_metadata(self) -> dict[str, object]:
        return {
            "bridge_kind": "remote",
            "provider_kind": "augmentation",
            "retrieval_kind": "remote_http",
            "response_contract": "remote_memory_prefetch_v1",
        }

    def prefetch_diagnostics(self, session_id: str) -> Mapping[str, object]:
        del session_id
        return {
            "access_trace": {
                "access_kind": "endpoint_url",
                "access_ref": "https://memory.example/recall",
                "attempt_count": 1,
            },
            "budget_trace": {
                "selected_hit_count": 1,
                "selected_hit_ids": ("remote-001",),
                "query_text_present": True,
            },
            "writeback_trace": {
                "supported": True,
                "configured": True,
                "session_writable": True,
                "enabled": True,
            },
        }


@dataclass(slots=True, frozen=True)
class _ProjectDraftRecallGovernancePolicy(RecallGovernancePolicy):
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
        del provider_decision, default_limit
        assert project_scope_key is not None
        return RecallGovernanceDecision(
            scope_filters=((MemoryScope.APP, app_id), (MemoryScope.PROJECT, project_scope_key)),
            allowed_statuses=(MemoryStatus.ACCEPTED, MemoryStatus.DRAFT),
            total_limit=2,
            within_scope_order=("created_at:desc", "id:asc"),
            overflow_order=("scope_order:desc", "created_at:desc", "id:asc"),
            include_external_augmentation=False,
            metadata={
                "session_id": session.id,
                "workflow_id": workflow_id,
                "profile_id": profile_id,
                "policy_id": "project-draft-recall",
            },
        )


@dataclass(slots=True, frozen=True)
class _AugmentOnlyProviderGovernancePolicy(MemoryProviderGovernancePolicy):
    def decide(
        self,
        binding: MemoryProviderBinding | None,
    ) -> MemoryProviderGovernanceDecision:
        if binding is None:
            return super().decide(binding)
        return MemoryProviderGovernanceDecision(
            binding=binding,
            allow_augmentation=True,
            allow_sync_turn=False,
            allow_session_end_writeback=False,
            allow_delegation_writeback=True,
            require_shared_write_capability_for_delegation=True,
            metadata={"policy_id": "augment-only"},
        )


@dataclass(slots=True)
class _ReasoningStub:
    def summarize_evidence(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> SummaryResult:
        del session, evidence_records
        return SummaryResult(episode_summary="Summarized evidence.")

    def extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
        summary: SummaryResult,
    ) -> CandidateDrafts:
        del summary
        procedural = MemoryCandidate(
            id=f"candidate-procedural-{session.id}",
            kind=MemoryKind.PROCEDURAL,
            scope=MemoryScope.APP,
            scope_key=session.app_id,
            title="Reusable procedure",
            body="Prefer the approved drafting sequence.",
            source_event_ids=tuple(event.id for event in session.events),
            evidence_ids=tuple(record.id for record in evidence_records),
            confidence=0.91,
        )
        return CandidateDrafts(candidates=(procedural,))


class MemoryGovernanceRegressionTests(unittest.TestCase):
    def test_tc013_recall_governance_controls_scope_status_budget_and_ranking(self) -> None:
        app = _build_app()
        workflow = _build_workflow()
        policy = _ProjectDraftRecallGovernancePolicy()
        session = AgentSession(
            id="session-tc013",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Continue the draft.",
        )
        decision = policy.decide(
            session=session,
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            profile_id="writer-profile",
            project_scope_key="shanforge",
            provider_decision=None,
        )

        self.assertEqual(
            decision.scope_filters,
            ((MemoryScope.APP, "demo.writer"), (MemoryScope.PROJECT, "shanforge")),
        )
        self.assertEqual(
            decision.allowed_statuses,
            (MemoryStatus.ACCEPTED, MemoryStatus.DRAFT),
        )
        self.assertEqual(decision.within_scope_order, ("created_at:desc", "id:asc"))

        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="app-older",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older app memory",
                    body="Older app body",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.99,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                ),
                MemoryRecord(
                    id="app-newer",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Newer app memory",
                    body="Newer app body",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.10,
                    supporting_refs=("event://2",),
                    created_at=datetime(2026, 4, 2, tzinfo=timezone.utc),
                ),
                MemoryRecord(
                    id="project-draft",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.PROJECT,
                    scope_key="shanforge",
                    title="Project draft memory",
                    body="Draft governance note.",
                    status=MemoryStatus.DRAFT,
                    confidence=0.55,
                    supporting_refs=("event://3",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=memory_repo,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            default_project_scope_key="shanforge",
            recall_governance_policy=policy,
        )

        bundle = service.prepare_session(session, app, workflow)
        preview = service.preview_recall(session, limit=2)

        self.assertEqual(
            tuple(record.id for record in bundle.retrieved_records),
            ("app-newer", "project-draft"),
        )
        self.assertEqual(
            memory_repo.scan_calls[0][1],
            (MemoryStatus.ACCEPTED, MemoryStatus.DRAFT),
        )
        self.assertEqual(preview.plan.allowed_statuses, decision.allowed_statuses)
        self.assertEqual(preview.plan.within_scope_order, decision.within_scope_order)
        self.assertEqual(preview.plan.metadata["policy_id"], "project-draft-recall")
        self.assertEqual(preview.scope_breakdowns[0].selected_record_ids, ("app-newer",))
        self.assertEqual(preview.scope_breakdowns[0].overflow_record_ids, ("app-older",))
        self.assertEqual(preview.record_rankings[0].record_id, "app-newer")
        self.assertEqual(preview.record_rankings[0].selection_reason, "scope_budget")
        self.assertEqual(preview.record_rankings[1].record_id, "project-draft")
        self.assertEqual(preview.record_rankings[1].selection_reason, "scope_budget")

    def test_tc014_provider_governance_controls_augmentation_delegation_and_writeback(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        policy = _AugmentOnlyProviderGovernancePolicy()
        binding = MemoryProviderBinding(
            provider_id="remote_http",
            source="profile",
            namespace="writer-profile",
            writable=True,
        )
        decision = policy.decide(binding)
        plain_digest = SubAgentDigest(
            parent_session_id="session-tc014",
            child_session_id="child-plain",
            summary="Plain child digest",
        )
        shared_digest = SubAgentDigest(
            parent_session_id="session-tc014",
            child_session_id="child-shared",
            summary="Shared child digest",
            metadata={"shared_provider_write_capability": True},
        )

        self.assertTrue(decision.allow_augmentation)
        self.assertFalse(decision.allow_sync_turn)
        self.assertFalse(decision.allow_session_end_writeback)
        self.assertFalse(decision.allow_lifecycle_writeback)
        self.assertFalse(decision.allows_delegation(plain_digest))
        self.assertTrue(decision.allows_delegation(shared_digest))

        provider = _TracingProvider()
        digest_store = _DigestStore(digests=[plain_digest, shared_digest])
        service = DefaultMemoryDomainService(
            memory_records=_MemoryRepository(),
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            digest_store=digest_store,
            memory_provider_manager=DefaultMemoryProviderManager(provider=provider),
            provider_governance_policy=policy,
        )
        session = AgentSession(
            id="session-tc014",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Load remote memory.",
            context={"memory_provider_binding": binding.to_mapping()},
        )

        service.prepare_session(session, app, workflow)
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": workflow.id})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": workflow.id})
        service.distill_session(session)

        self.assertEqual(provider.initialized[0][0], "session-tc014")
        self.assertEqual(provider.delegated, ["child-shared"])
        self.assertEqual(provider.synced, [])
        self.assertEqual(provider.ended, [])

    def test_tc015_lifecycle_governance_supports_forgotten_and_hides_forgotten_records(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        policy = MemoryLifecyclePolicy()

        forget_accepted = policy.evaluate_transition(
            current_status=MemoryStatus.ACCEPTED,
            target_status=MemoryStatus.FORGOTTEN,
        )
        forget_superseded = policy.evaluate_transition(
            current_status=MemoryStatus.SUPERSEDED,
            target_status=MemoryStatus.FORGOTTEN,
        )
        revive_forgotten = policy.evaluate_transition(
            current_status=MemoryStatus.FORGOTTEN,
            target_status=MemoryStatus.ACCEPTED,
        )

        self.assertTrue(forget_accepted.allowed)
        self.assertTrue(forget_superseded.allowed)
        self.assertFalse(revive_forgotten.allowed)
        self.assertIn("forgotten", forget_accepted.metadata["allowed_targets"])

        memory_repo = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-current",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Current memory",
                    body="Visible current memory.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "workflow-style"},
                ),
                MemoryRecord(
                    id="memory-accepted",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older conflicting memory",
                    body="Visible memory.",
                    status=MemoryStatus.SUPERSEDED,
                    confidence=0.91,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "workflow-style"},
                ),
                MemoryRecord(
                    id="memory-forgotten",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Forgotten memory",
                    body="Should stay hidden.",
                    status=MemoryStatus.FORGOTTEN,
                    confidence=0.99,
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
            id="session-tc015",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Recall visible memories only.",
        )

        bundle = service.prepare_session(session, app, workflow)
        preview = service.preview_recall(session, limit=2)
        queue = service.load_lifecycle_queue(session)
        forgotten_queue = service.load_lifecycle_queue(
            session,
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                effective_statuses=(MemoryStatus.FORGOTTEN,),
            ),
        )
        explanation = service.explain_session_memory(session)

        self.assertEqual(
            tuple(record.id for record in bundle.retrieved_records),
            ("memory-current",),
        )
        self.assertEqual(memory_repo.scan_calls[0][1], (MemoryStatus.ACCEPTED,))
        self.assertEqual(
            tuple(record.id for record in preview.bundle.retrieved_records),
            ("memory-current",),
        )
        self.assertEqual(
            tuple(item.record_id for item in preview.record_rankings),
            ("memory-current",),
        )
        self.assertEqual(queue.selected_record_ids, ())
        self.assertEqual(
            forgotten_queue.selected_record_ids,
            (),
        )
        self.assertEqual(
            tuple(item.record_id for item in forgotten_queue.items),
            ("memory-forgotten",),
        )
        lifecycle_evaluations = {
            item["record_id"]: item for item in explanation["lifecycle_evaluations"]
        }
        self.assertEqual(
            lifecycle_evaluations["memory-accepted"]["effective_status"],
            "superseded",
        )
        self.assertEqual(
            lifecycle_evaluations["memory-accepted"]["reason"],
            "conflict_superseded",
        )
        self.assertTrue(lifecycle_evaluations["memory-accepted"]["hidden"])
        self.assertEqual(
            lifecycle_evaluations["memory-forgotten"]["effective_status"],
            "forgotten",
        )
        self.assertEqual(
            lifecycle_evaluations["memory-forgotten"]["reason"],
            "decay_expired",
        )
        self.assertTrue(lifecycle_evaluations["memory-forgotten"]["hidden"])
        self.assertEqual(
            explanation["lifecycle_queue_summary"]["selected_record_ids"],
            (),
        )
        self.assertEqual(
            explanation["lifecycle_queue_summary"]["reason_counts"],
            {},
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["entry_count"],
            0,
        )

    def test_tc015_lifecycle_review_reopen_and_note_update_surface_in_audit_summary(
        self,
    ) -> None:
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
                    title="Current memory",
                    body="Visible current memory.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.96,
                    supporting_refs=("event://0",),
                    created_at=datetime(2026, 4, 3, tzinfo=timezone.utc),
                    metadata={"conflict_key": "workflow-style"},
                ),
                MemoryRecord(
                    id="memory-older",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Older memory",
                    body="Needs reviewer input.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.71,
                    supporting_refs=("event://1",),
                    created_at=datetime(2026, 4, 1, tzinfo=timezone.utc),
                    metadata={"conflict_key": "workflow-style"},
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
            id="session-tc015-review",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Review lifecycle queue.",
        )

        service.load_lifecycle_queue(session)
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="dismiss for now",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        service.update_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="conflict confirmed by reviewer",
        )
        service.reopen_lifecycle_queue(
            session,
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
            note="reopen for manual confirmation",
        )
        explanation = service.explain_session_memory(session)

        self.assertEqual(
            explanation["lifecycle_audit_summary"]["action_counts"],
            {
                MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED.value: 1,
                MemoryLifecycleAuditAction.REVIEW_NOTE_UPDATED.value: 1,
                MemoryLifecycleAuditAction.REVIEW_REOPENED.value: 1,
            },
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["resolution_counts"],
            {
                MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED.value: 2,
            },
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["latest_entries"][0]["action"],
            MemoryLifecycleAuditAction.REVIEW_REOPENED.value,
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["latest_entries"][0]["resolution"],
            None,
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["latest_by_record"][0]["record_id"],
            "memory-older",
        )
        self.assertEqual(
            explanation["lifecycle_audit_summary"]["latest_by_record"][0]["action"],
            MemoryLifecycleAuditAction.REVIEW_REOPENED.value,
        )

    def test_tc016_explainability_governance_projects_recall_and_promotion_reasons(
        self,
    ) -> None:
        app = _build_app()
        workflow = _build_workflow()
        provider = _TracingProvider()
        service = DefaultMemoryDomainService(
            memory_records=_MemoryRepository(
                records=[
                    MemoryRecord(
                        id="memory-app",
                        kind=MemoryKind.EPISODIC,
                        scope=MemoryScope.APP,
                        scope_key=app.metadata.id,
                        title="Accepted app memory",
                        body="Remember the drafting style.",
                        status=MemoryStatus.ACCEPTED,
                        confidence=0.85,
                        supporting_refs=("event://1",),
                    ),
                ]
            ),
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            memory_provider_manager=DefaultMemoryProviderManager(provider=provider),
            reasoning=_ReasoningStub(),
        )
        session = AgentSession(
            id="session-tc016",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Use the approved drafting process.",
            context={
                "memory_provider_binding": {
                    "provider_id": "remote_http",
                    "source": "profile",
                    "namespace": "writer-profile",
                    "writable": True,
                }
            },
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": workflow.id})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": workflow.id})
        session.add_artifact(
            SessionArtifact(
                kind="capability",
                uri="capability://context.inspect",
                summary="Captured runtime context.",
            )
        )

        service.prepare_session(session, app, workflow)
        preview = service.preview_recall(session, limit=1)
        service.distill_session(session)
        explanation = service.explain_session_memory(session)

        assert preview.augmentation_preview is not None
        diagnostics = preview.augmentation_preview.diagnostics
        self.assertIn("contract_trace", diagnostics)
        self.assertIn("access_trace", diagnostics)
        self.assertIn("budget_trace", diagnostics)
        self.assertNotIn("bridge_kind", diagnostics)
        self.assertEqual(
            diagnostics["contract_trace"]["response_contract"],
            "remote_memory_prefetch_v1",
        )
        self.assertEqual(
            diagnostics["access_trace"]["access_ref"],
            "https://memory.example/recall",
        )
        self.assertEqual(
            preview.plan.within_scope_order,
            ("confidence:desc", "created_at:asc", "id:asc"),
        )
        self.assertEqual(preview.record_rankings[0].selection_reason, "scope_budget")
        self.assertEqual(explanation["promotion_statuses"], ("accepted", "draft"))
        self.assertEqual(
            explanation["promotion_reasons"],
            (
                "Candidate satisfied configurable promotion policy.",
                "Procedural memory remains draft until additional review.",
            ),
        )
        self.assertEqual(explanation["recalled_memory_statuses"], ("accepted",))
        self.assertEqual(explanation["memory_provider_binding"]["provider_id"], "remote_http")
        self.assertEqual(
            explanation["recall_plan"]["scope_filters"],
            (("app", "demo.writer"),),
        )
        self.assertEqual(explanation["promotion_decisions"][1]["status"], "draft")


if __name__ == "__main__":
    unittest.main()
