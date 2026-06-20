from __future__ import annotations

import unittest
from dataclasses import dataclass, field

from access.api.memory_api import MemoryAPI
from application.memory.governance_service import MemoryGovernanceService
from application.memory.inspection_service import MemoryInspectionService
from application.session.inspection_service import SessionInspectionService
from domain.memory import RecallBundle, RecallPlan, RecallPreview, RecallQuery
from domain.memory.assembly_models import MemoryProviderBinding, RecallAugmentationPreview
from domain.memory.models import (
    MemoryLifecycleApplyResult,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleAuditLog,
    MemoryLifecycleEvaluation,
    MemoryLifecycleQueue,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleQueueItem,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleQueueUpdateResult,
    MemoryLifecycleReviewResolution,
    MemoryLifecycleReviewResult,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
)
from domain.session.assembly_models import SessionAssemblyManifest
from domain.session.models import AgentSession, SessionArtifact
from runtime.session_search.query_adapter import SessionSearchQueryAdapter
from runtime.session_search.service import SessionSearchService
from settings.session import (
    EmptyVectorIndexProvider,
    InMemoryArtifactStore,
    InMemorySearchIndexProvider,
    InMemorySessionArchiveProvider,
    InMemorySessionAssemblyStore,
    InMemorySessionStore,
)


@dataclass(slots=True)
class _MemoryInspectionStub:
    preview_result: RecallPreview | None = None
    recalled_queries: list[RecallQuery] | None = None

    def recall(self, query: RecallQuery) -> RecallBundle:
        if self.recalled_queries is None:
            self.recalled_queries = []
        self.recalled_queries.append(query)
        return RecallBundle()

    def preview_recall(self, session_id: str, limit: int | None = None) -> RecallPreview:
        assert self.preview_result is not None
        return self.preview_result


@dataclass(slots=True)
class _MemoryGovernanceStub:
    review_result: MemoryLifecycleReviewResult | None = None
    queue_result: MemoryLifecycleQueue | None = None
    audit_result: MemoryLifecycleAuditLog | None = None
    apply_result: MemoryLifecycleApplyResult | None = None
    update_result: MemoryLifecycleQueueUpdateResult | None = None
    review_calls: list[str] = field(default_factory=list)
    queue_calls: list[tuple[str, MemoryLifecycleQueueFilter | None]] = field(
        default_factory=list
    )
    audit_calls: list[tuple[str, MemoryLifecycleAuditFilter | None]] = field(
        default_factory=list
    )
    apply_calls: list[
        tuple[str, str, tuple[str, ...] | None, MemoryLifecycleQueueFilter | None]
    ] = field(default_factory=list)
    reopen_calls: list[
        tuple[str, str, tuple[str, ...] | None, MemoryLifecycleQueueFilter | None, str | None]
    ] = field(
        default_factory=list
    )
    update_calls: list[
        tuple[
            str,
            str,
            tuple[str, ...] | None,
            MemoryLifecycleQueueFilter | None,
            MemoryLifecycleQueueReviewStatus,
            str | None,
            MemoryLifecycleReviewResolution | None,
        ]
    ] = field(default_factory=list)

    def review_lifecycle(self, session_id: str) -> MemoryLifecycleReviewResult:
        self.review_calls.append(session_id)
        assert self.review_result is not None
        return self.review_result

    def load_lifecycle_queue(
        self,
        session_id: str,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue:
        self.queue_calls.append((session_id, queue_filter))
        assert self.queue_result is not None
        return self.queue_result

    def load_lifecycle_audit(
        self,
        session_id: str,
        audit_filter: MemoryLifecycleAuditFilter | None = None,
    ) -> MemoryLifecycleAuditLog:
        self.audit_calls.append((session_id, audit_filter))
        assert self.audit_result is not None
        return self.audit_result

    def apply_lifecycle(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult:
        self.apply_calls.append((session_id, actor, record_ids, queue_filter))
        assert self.apply_result is not None
        return self.apply_result

    def reopen_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
    ) -> MemoryLifecycleQueueUpdateResult:
        self.reopen_calls.append((session_id, actor, record_ids, queue_filter, note))
        assert self.update_result is not None
        return self.update_result

    def update_lifecycle_queue(
        self,
        session_id: str,
        actor: str,
        review_status: MemoryLifecycleQueueReviewStatus,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
        resolution: MemoryLifecycleReviewResolution | None = None,
    ) -> MemoryLifecycleQueueUpdateResult:
        self.update_calls.append(
            (session_id, actor, record_ids, queue_filter, review_status, note, resolution)
        )
        assert self.update_result is not None
        return self.update_result


class SessionInspectionServiceTests(unittest.TestCase):
    def test_inspection_service_exposes_session_archive_slice_and_assembly_queries(self) -> None:
        session_store = InMemorySessionStore()
        artifact_store = InMemoryArtifactStore()
        assembly_store = InMemorySessionAssemblyStore()
        archive_provider = InMemorySessionArchiveProvider(
            session_store=session_store,
            artifact_store=artifact_store,
            assembly_store=assembly_store,
        )
        query_service = SessionSearchService(
            structured_store=archive_provider,
            search_index=InMemorySearchIndexProvider(archive_provider),
            vector_index=EmptyVectorIndexProvider(),
        )
        query_adapter = SessionSearchQueryAdapter(service=query_service)
        inspection_service = SessionInspectionService(
            session_ledger=session_store,
            archive_query=query_adapter,
            transcript_query=query_adapter,
            assembly_query=query_adapter,
        )
        memory_service = _MemoryInspectionStub(
            preview_result=RecallPreview(
                session_id="session-inspect",
                query=RecallQuery(
                    session_id="session-inspect",
                    app_id="demo.writer",
                    workflow_id="compose",
                    scope_filters=((MemoryScope.APP, "demo.writer"),),
                    allowed_statuses=(MemoryStatus.ACCEPTED,),
                    limit=2,
                ),
                plan=RecallPlan(
                    scope_filters=((MemoryScope.APP, "demo.writer"),),
                    allowed_statuses=(MemoryStatus.ACCEPTED,),
                    total_limit=2,
                    scope_budgets={"app:demo.writer": 2},
                    include_external_augmentation=True,
                ),
                bundle=RecallBundle(
                    retrieved_records=(
                        MemoryRecord(
                            id="memory-001",
                            kind="episodic",
                            scope="app",
                            scope_key="demo.writer",
                            title="Remember this",
                            body="Previewed memory",
                            status="accepted",
                            confidence=0.9,
                            supporting_refs=("event://1",),
                        ),
                    ),
                ),
                memory_provider_binding=MemoryProviderBinding(provider_id="jsonl"),
                augmentation_preview=RecallAugmentationPreview(
                    provider_id="jsonl",
                    recall_block_source="session_context",
                    recall_block_present=True,
                ),
                external_recall_block="<external-memory>\nPreview block\n</external-memory>",
            )
        )
        governance_service = _MemoryGovernanceStub(
            review_result=MemoryLifecycleReviewResult(
                session_id="session-inspect",
                scope_filters=((MemoryScope.APP, "demo.writer"),),
                evaluations=(
                    MemoryLifecycleEvaluation(
                        record_id="memory-001",
                        scope=MemoryScope.APP,
                        scope_key="demo.writer",
                        current_status=MemoryStatus.ACCEPTED,
                        effective_status=MemoryStatus.ACCEPTED,
                        reason="state_retained",
                        allowed=True,
                        hidden=False,
                    ),
                ),
            ),
            queue_result=MemoryLifecycleQueue(
                session_id="session-inspect",
                scope_filters=((MemoryScope.APP, "demo.writer"),),
                queue_filter=MemoryLifecycleQueueFilter(
                    effective_statuses=(MemoryStatus.SUPERSEDED,),
                ),
                items=(
                    MemoryLifecycleQueueItem(
                        record_id="memory-001",
                        scope=MemoryScope.APP,
                        scope_key="demo.writer",
                        current_status=MemoryStatus.ACCEPTED,
                        effective_status=MemoryStatus.SUPERSEDED,
                        reason="conflict_superseded",
                        allowed=True,
                        hidden=True,
                        action_required=True,
                        selected_by_default=True,
                    ),
                ),
                selected_record_ids=("memory-001",),
                total_evaluation_count=1,
                actionable_count=1,
                hidden_count=1,
            ),
            audit_result=MemoryLifecycleAuditLog(
                session_id="session-inspect",
                audit_filter=MemoryLifecycleAuditFilter(
                    actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                ),
                entries=(
                    MemoryLifecycleAuditEntry(
                        id="audit-001",
                        session_id="session-inspect",
                        record_id="memory-001",
                        actor="memory-reviewer",
                        action=MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,
                        current_status=MemoryStatus.ACCEPTED,
                        effective_status=MemoryStatus.SUPERSEDED,
                        queue_review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                        resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                        reason="conflict_superseded",
                        note="manual triage",
                    ),
                ),
            ),
            apply_result=MemoryLifecycleApplyResult(
                session_id="session-inspect",
                actor="memory-reviewer",
                queue_filter=MemoryLifecycleQueueFilter(
                    effective_statuses=(MemoryStatus.SUPERSEDED,),
                ),
                selected_record_ids=("memory-001",),
                applied_record_ids=(),
                skipped_record_ids=("memory-001",),
            ),
            update_result=MemoryLifecycleQueueUpdateResult(
                session_id="session-inspect",
                actor="memory-reviewer",
                review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                requested_record_ids=("memory-001",),
                updated_record_ids=("memory-001",),
            ),
        )
        api = MemoryAPI(
            session_service=inspection_service,
            memory_service=memory_service,
            memory_governance_service=governance_service,
        )

        session = AgentSession(
            id="session-inspect",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Inspect the assembly plane.",
            context={
                "profile_id": "writer-profile",
                "workspace_root": "/tmp/shanforge",
            },
        )
        session_store.save_session(session)
        assembly_store.save(
            SessionAssemblyManifest.from_mapping(
                {
                    "session_id": "session-inspect",
                    "profile_id": "writer-profile",
                    "workspace_root": "/tmp/shanforge",
                    "rule_bundle": {
                        "source": "workspace-rules",
                        "project_scope_key": "shanforge",
                        "summary": "Workspace rules loaded.",
                    },
                    "active_skills": (
                        {
                            "skill_id": "python-uv-project",
                            "name": "python-uv-project",
                            "scope": "project",
                            "reason": "workflow-required",
                        },
                    ),
                    "recall_scope_filters": (("app", "demo.writer"), ("project", "shanforge")),
                    "recalled_memory_ids": ("memory-001",),
                    "child_session_ids": ("child-001",),
                    "child_digests": (
                        {
                            "parent_session_id": "session-inspect",
                            "child_session_id": "child-001",
                            "summary": "Child agent captured a focused repository digest.",
                            "responsibility_scope": ("inspection",),
                            "evidence_refs": ("event://child-001",),
                        },
                    ),
                    "selected_model": {
                        "provider_id": "mock",
                        "model_id": "mock-chat",
                        "source": "execution",
                        "step_id": "draft",
                    },
                    "model_bindings": (
                        {
                            "provider_id": "mock",
                            "model_id": "mock-chat",
                            "source": "execution",
                            "step_id": "draft",
                        },
                    ),
                    "backend_bindings": (
                        {
                            "family": "llm_provider",
                            "binding_id": "mock",
                            "source": "profile",
                        },
                    ),
                    "sources": ("profile", "workspace", "skills", "memory"),
                }
            )
        )
        session.add_event("assistant", "Loaded the assembly manifest.", {"step_id": "inspect"})
        for event in session.events:
            session_store.append_event(session.id, event)
        artifact_store.save_artifact(
            session.id,
            SessionArtifact(
                kind="report",
                uri="file:///tmp/shanforge/report.md",
                summary="Inspection report",
            ),
        )

        stored_session = api.get_session("session-inspect")
        archive_hits = api.search_session_archive("assembly manifest", "writer-profile", 5)
        transcript_slice = api.load_session_slice("session-inspect", None, 20)
        manifest = api.explain_session_assembly("session-inspect")
        preview = api.preview_recall("session-inspect", limit=2)
        lifecycle_review = api.review_lifecycle("session-inspect")
        lifecycle_queue = api.load_lifecycle_queue(
            "session-inspect",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
        )
        lifecycle_audit = api.load_lifecycle_audit(
            "session-inspect",
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                resolutions=(MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,),
            ),
        )
        lifecycle_queue_reopen = api.reopen_lifecycle_queue(
            "session-inspect",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
            note="reopen for manual confirmation",
        )
        lifecycle_apply = api.apply_lifecycle(
            "session-inspect",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
        )
        lifecycle_queue_update = api.update_lifecycle_queue(
            "session-inspect",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="manual triage",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )

        self.assertEqual(stored_session.id, "session-inspect")
        self.assertEqual(archive_hits[0].session_id, "session-inspect")
        self.assertEqual(transcript_slice.events[0]["summary"], "Loaded the assembly manifest.")
        self.assertIsInstance(manifest, SessionAssemblyManifest)
        self.assertEqual(manifest.rule_bundle.project_scope_key, "shanforge")
        self.assertEqual(manifest.active_skills[0].skill_id, "python-uv-project")
        self.assertEqual(manifest.recalled_memory_ids, ("memory-001",))
        self.assertEqual(manifest.selected_model.provider_id, "mock")
        self.assertEqual(manifest.model_bindings[0].step_id, "draft")
        self.assertEqual(manifest.backend_bindings[0].family, "llm_provider")
        self.assertEqual(manifest.child_session_ids, ("child-001",))
        self.assertEqual(
            manifest.child_digests[0].summary,
            "Child agent captured a focused repository digest.",
        )
        self.assertEqual(preview.plan.total_limit, 2)
        self.assertEqual(preview.memory_provider_binding.provider_id, "jsonl")
        self.assertIn("Preview block", preview.external_recall_block)
        self.assertEqual(preview.augmentation_preview.provider_id, "jsonl")
        self.assertTrue(preview.augmentation_preview.recall_block_present)
        self.assertEqual(lifecycle_review.evaluations[0].record_id, "memory-001")
        self.assertEqual(lifecycle_queue.selected_record_ids, ("memory-001",))
        self.assertEqual(
            tuple(entry.record_id for entry in lifecycle_audit.entries),
            ("memory-001",),
        )
        self.assertEqual(
            lifecycle_queue_reopen.review_status,
            MemoryLifecycleQueueReviewStatus.DISMISSED,
        )
        self.assertEqual(lifecycle_apply.actor, "memory-reviewer")
        self.assertEqual(
            lifecycle_queue_update.review_status,
            MemoryLifecycleQueueReviewStatus.DISMISSED,
        )
        self.assertEqual(
            lifecycle_queue_update.resolution,
            MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        self.assertEqual(
            governance_service.apply_calls,
            [
                (
                    "session-inspect",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                )
            ],
        )
        self.assertEqual(
            governance_service.update_calls,
            [
                (
                    "session-inspect",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                    MemoryLifecycleQueueReviewStatus.DISMISSED,
                    "manual triage",
                    MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                )
            ],
        )
        self.assertEqual(
            governance_service.reopen_calls,
            [
                (
                    "session-inspect",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        actionable_only=False,
                        review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
                    ),
                    "reopen for manual confirmation",
                )
            ],
        )
        self.assertEqual(
            governance_service.queue_calls,
            [
                (
                    "session-inspect",
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                )
            ],
        )
        self.assertEqual(
            governance_service.audit_calls,
            [
                (
                    "session-inspect",
                    MemoryLifecycleAuditFilter(
                        actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                        resolutions=(MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,),
                    ),
                )
            ],
        )

    def test_memory_inspection_service_loads_session_and_delegates_preview(self) -> None:
        @dataclass(slots=True)
        class _MemoryDomainServiceStub:
            preview_calls: list[tuple[str, int | None]]

            def preview_recall(
                self,
                session: AgentSession,
                limit: int | None = None,
            ) -> RecallPreview:
                self.preview_calls.append((session.id, limit))
                return RecallPreview(
                    session_id=session.id,
                    query=RecallQuery(
                        session_id=session.id,
                        app_id=session.app_id,
                        workflow_id=session.workflow_id,
                        scope_filters=((MemoryScope.APP, session.app_id),),
                        allowed_statuses=(MemoryStatus.ACCEPTED,),
                        limit=limit or 8,
                    ),
                    plan=RecallPlan(
                        scope_filters=((MemoryScope.APP, session.app_id),),
                        allowed_statuses=(MemoryStatus.ACCEPTED,),
                        total_limit=limit or 8,
                        scope_budgets={f"app:{session.app_id}": limit or 8},
                    ),
                    bundle=RecallBundle(),
                )

        session_store = InMemorySessionStore()
        session_store.save_session(
            AgentSession(
                id="session-preview",
                app_id="demo.writer",
                workflow_id="compose",
                user_input="Preview my recall plan.",
            )
        )
        memory_domain = _MemoryDomainServiceStub(preview_calls=[])
        service = MemoryInspectionService(
            session_ledger=session_store,
            memory_service=memory_domain,
        )

        preview = service.preview_recall("session-preview", limit=3)

        self.assertEqual(memory_domain.preview_calls, [("session-preview", 3)])
        self.assertEqual(preview.plan.total_limit, 3)

    def test_memory_governance_service_loads_session_and_delegates_review_and_apply(self) -> None:
        @dataclass(slots=True)
        class _MemoryDomainServiceStub:
            review_calls: list[str]
            queue_calls: list[tuple[str, MemoryLifecycleQueueFilter | None]]
            audit_calls: list[tuple[str, MemoryLifecycleAuditFilter | None]]
            apply_calls: list[
                tuple[str, str, tuple[str, ...] | None, MemoryLifecycleQueueFilter | None]
            ]
            reopen_calls: list[
                tuple[
                    str,
                    str,
                    tuple[str, ...] | None,
                    MemoryLifecycleQueueFilter | None,
                    str | None,
                ]
            ]
            update_calls: list[
                tuple[
                    str,
                    str,
                    tuple[str, ...] | None,
                    MemoryLifecycleQueueFilter | None,
                    MemoryLifecycleQueueReviewStatus,
                    str | None,
                    MemoryLifecycleReviewResolution | None,
                ]
            ]

            def review_lifecycle(self, session: AgentSession) -> MemoryLifecycleReviewResult:
                self.review_calls.append(session.id)
                return MemoryLifecycleReviewResult(
                    session_id=session.id,
                    scope_filters=((MemoryScope.APP, session.app_id),),
                    evaluations=(
                        MemoryLifecycleEvaluation(
                            record_id="memory-001",
                            scope=MemoryScope.APP,
                            scope_key=session.app_id,
                            current_status=MemoryStatus.ACCEPTED,
                            effective_status=MemoryStatus.SUPERSEDED,
                            reason="conflict_superseded",
                            allowed=True,
                            hidden=True,
                        ),
                    ),
                )

            def load_lifecycle_queue(
                self,
                session: AgentSession,
                queue_filter: MemoryLifecycleQueueFilter | None = None,
            ) -> MemoryLifecycleQueue:
                self.queue_calls.append((session.id, queue_filter))
                return MemoryLifecycleQueue(
                    session_id=session.id,
                    scope_filters=((MemoryScope.APP, session.app_id),),
                    queue_filter=queue_filter or MemoryLifecycleQueueFilter(),
                    items=(
                        MemoryLifecycleQueueItem(
                            record_id="memory-001",
                            scope=MemoryScope.APP,
                            scope_key=session.app_id,
                            current_status=MemoryStatus.ACCEPTED,
                            effective_status=MemoryStatus.SUPERSEDED,
                            reason="conflict_superseded",
                            allowed=True,
                            hidden=True,
                            action_required=True,
                            selected_by_default=True,
                        ),
                    ),
                    selected_record_ids=("memory-001",),
                    total_evaluation_count=1,
                    actionable_count=1,
                    hidden_count=1,
                )

            def load_lifecycle_audit(
                self,
                session: AgentSession,
                audit_filter: MemoryLifecycleAuditFilter | None = None,
            ) -> MemoryLifecycleAuditLog:
                self.audit_calls.append((session.id, audit_filter))
                return MemoryLifecycleAuditLog(
                    session_id=session.id,
                    audit_filter=audit_filter or MemoryLifecycleAuditFilter(),
                    entries=(
                        MemoryLifecycleAuditEntry(
                            id="audit-001",
                            session_id=session.id,
                            record_id="memory-001",
                            actor="memory-reviewer",
                        action=MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,
                        current_status=MemoryStatus.ACCEPTED,
                        effective_status=MemoryStatus.SUPERSEDED,
                        queue_review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                        resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                        reason="conflict_superseded",
                    ),
                ),
            )

            def apply_lifecycle(
                self,
                session: AgentSession,
                actor: str,
                record_ids: tuple[str, ...] | None = None,
                queue_filter: MemoryLifecycleQueueFilter | None = None,
            ) -> MemoryLifecycleApplyResult:
                self.apply_calls.append((session.id, actor, record_ids, queue_filter))
                return MemoryLifecycleApplyResult(
                    session_id=session.id,
                    actor=actor,
                    queue_filter=queue_filter,
                    selected_record_ids=record_ids or ("memory-001",),
                    applied_record_ids=("memory-001",),
                )

            def reopen_lifecycle_queue(
                self,
                session: AgentSession,
                actor: str,
                record_ids: tuple[str, ...] | None = None,
                queue_filter: MemoryLifecycleQueueFilter | None = None,
                note: str | None = None,
            ) -> MemoryLifecycleQueueUpdateResult:
                self.reopen_calls.append((session.id, actor, record_ids, queue_filter, note))
                return MemoryLifecycleQueueUpdateResult(
                    session_id=session.id,
                    actor=actor,
                    review_status=MemoryLifecycleQueueReviewStatus.PENDING,
                    requested_record_ids=record_ids or ("memory-001",),
                    queue_filter=queue_filter,
                    updated_record_ids=record_ids or ("memory-001",),
                )

            def update_lifecycle_queue(
                self,
                session: AgentSession,
                actor: str,
                review_status: MemoryLifecycleQueueReviewStatus,
                record_ids: tuple[str, ...] | None = None,
                queue_filter: MemoryLifecycleQueueFilter | None = None,
                note: str | None = None,
                resolution: MemoryLifecycleReviewResolution | None = None,
            ) -> MemoryLifecycleQueueUpdateResult:
                self.update_calls.append(
                    (
                        session.id,
                        actor,
                        record_ids,
                        queue_filter,
                        review_status,
                        note,
                        resolution,
                    )
                )
                return MemoryLifecycleQueueUpdateResult(
                    session_id=session.id,
                    actor=actor,
                    review_status=review_status,
                    resolution=resolution,
                    requested_record_ids=record_ids or ("memory-001",),
                    queue_filter=queue_filter,
                    updated_record_ids=record_ids or ("memory-001",),
                )

        session_store = InMemorySessionStore()
        session_store.save_session(
            AgentSession(
                id="session-governance",
                app_id="demo.writer",
                workflow_id="compose",
                user_input="Review lifecycle.",
            )
        )
        memory_domain = _MemoryDomainServiceStub(
            review_calls=[],
            queue_calls=[],
            audit_calls=[],
            apply_calls=[],
            reopen_calls=[],
            update_calls=[],
        )
        service = MemoryGovernanceService(
            session_ledger=session_store,
            memory_service=memory_domain,
        )

        review = service.review_lifecycle("session-governance")
        queue = service.load_lifecycle_queue(
            "session-governance",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
        )
        audit_log = service.load_lifecycle_audit(
            "session-governance",
            audit_filter=MemoryLifecycleAuditFilter(
                actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                resolutions=(MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,),
            ),
        )
        apply_result = service.apply_lifecycle(
            "session-governance",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
        )
        reopen_result = service.reopen_lifecycle_queue(
            "session-governance",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                actionable_only=False,
                review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
            ),
            note="reopen for manual confirmation",
        )
        update_result = service.update_lifecycle_queue(
            "session-governance",
            actor="memory-reviewer",
            queue_filter=MemoryLifecycleQueueFilter(
                effective_statuses=(MemoryStatus.SUPERSEDED,),
            ),
            review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
            note="manual triage",
            resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )

        self.assertEqual(memory_domain.review_calls, ["session-governance"])
        self.assertEqual(
            memory_domain.queue_calls,
            [
                (
                    "session-governance",
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                )
            ],
        )
        self.assertEqual(
            memory_domain.audit_calls,
            [
                (
                    "session-governance",
                    MemoryLifecycleAuditFilter(
                        actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                        resolutions=(MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,),
                    ),
                )
            ],
        )
        self.assertEqual(
            memory_domain.apply_calls,
            [
                (
                    "session-governance",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                )
            ],
        )
        self.assertEqual(review.evaluations[0].reason, "conflict_superseded")
        self.assertEqual(queue.selected_record_ids, ("memory-001",))
        self.assertEqual(tuple(entry.record_id for entry in audit_log.entries), ("memory-001",))
        self.assertEqual(apply_result.applied_record_ids, ("memory-001",))
        self.assertEqual(reopen_result.review_status, MemoryLifecycleQueueReviewStatus.PENDING)
        self.assertEqual(update_result.updated_record_ids, ("memory-001",))
        self.assertEqual(
            update_result.resolution,
            MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
        )
        self.assertEqual(
            memory_domain.reopen_calls,
            [
                (
                    "session-governance",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        actionable_only=False,
                        review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
                    ),
                    "reopen for manual confirmation",
                )
            ],
        )
        self.assertEqual(
            memory_domain.update_calls,
            [
                (
                    "session-governance",
                    "memory-reviewer",
                    None,
                    MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.SUPERSEDED,),
                    ),
                    MemoryLifecycleQueueReviewStatus.DISMISSED,
                    "manual triage",
                    MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                )
            ],
        )


if __name__ == "__main__":
    unittest.main()
