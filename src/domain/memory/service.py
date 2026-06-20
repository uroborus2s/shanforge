from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Any, Mapping

from domain.agent_app.models import AgentApp
from domain.memory.assembly_models import (
    MemoryProviderAugmentation,
    MemoryProviderBinding,
    RecallAugmentationPreview,
    RecallPlan,
    RecallPreview,
    RecallRecordRanking,
    RecallScopeBreakdown,
)
from domain.memory.augmentation_diagnostics import (
    compact_augmentation_diagnostics,
    project_preview_augmentation_diagnostics,
    project_stored_augmentation_diagnostics,
)
from domain.memory.governance import (
    MemoryLifecyclePolicy,
    MemoryProviderGovernanceDecision,
    MemoryProviderGovernancePolicy,
    RecallGovernanceDecision,
    RecallGovernancePolicy,
)
from domain.memory.models import (
    DistillationResult,
    EvidenceRecord,
    MemoryCandidate,
    MemoryDistillationSample,
    MemoryKind,
    MemoryLifecycleApplyResult,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditEntry,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleAuditLog,
    MemoryLifecycleEvaluation,
    MemoryLifecycleQueue,
    MemoryLifecycleQueueEntry,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleQueueItem,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleQueueUpdateResult,
    MemoryLifecycleResolutionOption,
    MemoryLifecycleReviewResolution,
    MemoryLifecycleReviewResult,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
    PromotionDecision,
    RecallBundle,
    RecallQuery,
    SummaryResult,
)
from domain.memory.policy import MemoryPromotionPolicy
from domain.memory.ports import (
    EvidenceRepositoryPort,
    MemoryArchiveQueryPort,
    MemoryDatasetRepositoryPort,
    MemoryLifecycleAuditRepositoryPort,
    MemoryLifecycleQueueRepositoryPort,
    MemoryProfileResolverPort,
    MemoryProviderManagerPort,
    MemoryReasoningPort,
    MemoryRecordRepositoryPort,
    MemoryRuleBundlePort,
    MemorySemanticSearchPort,
    MemorySkillCatalogPort,
    RecallPlannerPort,
    RecallRankerPort,
)
from domain.session.assembly_models import (
    BackendBinding,
    ModelBinding,
    ProjectRuleBundle,
    SessionAssemblyManifest,
    SkillActivation,
)
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession
from domain.session.ports import DelegationDigestStorePort, SessionAssemblyStorePort
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True)
class DefaultMemoryDomainService:
    """Business-domain logic for recall, distillation, and explainability."""

    memory_records: MemoryRecordRepositoryPort
    evidence_records: EvidenceRepositoryPort
    dataset_records: MemoryDatasetRepositoryPort
    lifecycle_queue_records: MemoryLifecycleQueueRepositoryPort | None = None
    lifecycle_audit_records: MemoryLifecycleAuditRepositoryPort | None = None
    assembly_store: SessionAssemblyStorePort | None = None
    digest_store: DelegationDigestStorePort | None = None
    archive_query: MemoryArchiveQueryPort | None = None
    profile_resolver: MemoryProfileResolverPort | None = None
    rule_bundle: MemoryRuleBundlePort | None = None
    skill_catalog: MemorySkillCatalogPort | None = None
    reasoning: MemoryReasoningPort | None = None
    semantic_search: MemorySemanticSearchPort | None = None
    memory_provider_manager: MemoryProviderManagerPort | None = None
    recall_planner: RecallPlannerPort | None = None
    recall_ranker: RecallRankerPort | None = None
    default_project_scope_key: str | None = None
    promotion_policy: MemoryPromotionPolicy = field(default_factory=MemoryPromotionPolicy)
    recall_governance_policy: RecallGovernancePolicy = field(
        default_factory=RecallGovernancePolicy
    )
    provider_governance_policy: MemoryProviderGovernancePolicy = field(
        default_factory=MemoryProviderGovernancePolicy
    )
    lifecycle_policy: MemoryLifecyclePolicy = field(default_factory=MemoryLifecyclePolicy)

    def prepare_session(
        self,
        session: AgentSession,
        app: AgentApp,
        workflow: WorkflowDefinition,
    ) -> RecallBundle:
        profile = (
            self.profile_resolver.resolve_profile(session, app.metadata.id, workflow.id)
            if self.profile_resolver is not None
            else {}
        )
        profile_id = (
            str(profile.get("profile_id"))
            if profile.get("profile_id") is not None
            else None
        )
        workspace_root = (
            str(session.context.get("workspace_root"))
            if session.context.get("workspace_root") is not None
            else None
        )
        rules = (
            self.rule_bundle.load_rule_bundle(workspace_root, profile_id)
            if self.rule_bundle is not None
            else {}
        )
        skills = (
            self.skill_catalog.list_skill_index(app.metadata.id, workflow.id)
            if self.skill_catalog is not None
            else ()
        )
        project_scope_key = self._resolve_project_scope_key(profile=profile, rules=rules)
        child_digests = (
            self.digest_store.list_by_session(session.id) if self.digest_store is not None else ()
        )
        memory_provider_binding = self._resolve_memory_provider_binding(
            session=session,
            profile=profile,
        )
        provider_governance = self.provider_governance_policy.decide(memory_provider_binding)
        recall_plan = self._plan_recall(
            session=session,
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            profile_id=profile_id,
            project_scope_key=project_scope_key,
            provider_decision=provider_governance,
        )
        recall_query = RecallQuery(
            session_id=session.id,
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            scope_filters=recall_plan.scope_filters,
            allowed_statuses=recall_plan.allowed_statuses,
            limit=recall_plan.total_limit,
            query_text=session.user_input or None,
        )
        augmentation = None
        augmentation_diagnostics: dict[str, Any] = {}
        if self.memory_provider_manager is not None and memory_provider_binding is not None:
            if provider_governance.allow_augmentation:
                augmentation = self.memory_provider_manager.start_session(
                    decision=provider_governance,
                    query=recall_query,
                )
                if augmentation is not None:
                    if augmentation.recall_block:
                        session.context["external_memory_recall_block"] = augmentation.recall_block
                    augmentation_diagnostics.update(
                        {
                            "memory_provider_id": augmentation.binding.provider_id,
                            "memory_provider_writable": augmentation.binding.writable,
                            "external_memory_block_present": augmentation.recall_block is not None,
                            **dict(augmentation.diagnostics),
                        }
                    )
                    augmentation_diagnostics = compact_augmentation_diagnostics(
                        augmentation_diagnostics
                    )
            for digest in child_digests:
                if provider_governance.allows_delegation(digest):
                    self.memory_provider_manager.on_delegation(provider_governance, digest)
        bundle = self.recall(
            recall_query,
            plan=recall_plan,
            augmentation=augmentation,
        )
        bundle.diagnostics.update(augmentation_diagnostics)
        session.recalled_memories = list(bundle.retrieved_records)
        bundle.diagnostics.update(
            {
                "profile_id": profile_id,
                "project_scope_key": project_scope_key,
                "skill_count": len(skills),
            }
        )
        if augmentation_diagnostics:
            session.context["memory_provider_diagnostics"] = dict(augmentation_diagnostics)
        if profile_id is not None:
            session.context["profile_id"] = profile_id
        if project_scope_key is not None:
            session.context["project_scope_key"] = project_scope_key
        if memory_provider_binding is not None:
            session.context["memory_provider_binding"] = memory_provider_binding.to_mapping()
        assembly_manifest = self._build_session_assembly_manifest(
            session=session,
            profile=profile,
            rules=rules,
            skills=skills,
            bundle=bundle,
            child_digests=child_digests,
            memory_provider_binding=memory_provider_binding,
            project_scope_key=project_scope_key,
        )
        session.context["assembly_manifest"] = assembly_manifest.to_mapping()
        if self.assembly_store is not None:
            self.assembly_store.save(assembly_manifest)
        return bundle

    def recall(
        self,
        query: RecallQuery,
        *,
        plan: RecallPlan | None = None,
        augmentation: MemoryProviderAugmentation | None = None,
    ) -> RecallBundle:
        recall_plan = plan or self._build_plan_from_query(query)
        scanned_records = self.memory_records.scan_memory_records(
            recall_plan.scope_filters,
            recall_plan.allowed_statuses,
        )
        retrieved_records = self._select_recall_records(recall_plan, scanned_records, augmentation)
        return self._build_recall_bundle(
            recall_plan,
            scanned_records,
            retrieved_records,
            augmentation,
        )

    def distill_session(self, session: AgentSession) -> DistillationResult:
        evidence_records = self._project_evidence(session)
        candidates = self._extract_candidates(session, evidence_records)
        summary = SummaryResult()
        generated_candidates: tuple[MemoryCandidate, ...] = ()
        if self.reasoning is not None:
            summary = self.reasoning.summarize_evidence(session, evidence_records)
            generated_candidates = self.reasoning.extract_candidates(
                session=session,
                evidence_records=evidence_records,
                summary=summary,
            ).candidates
        candidates = self._dedupe_candidates(
            (*candidates, *self._normalize_generated_candidates(session, generated_candidates))
        )
        promotion_decisions: list[PromotionDecision] = []
        promoted_records: list[MemoryRecord] = []
        for candidate in candidates:
            decision, record = self._promote_candidate(candidate)
            promotion_decisions.append(decision)
            self.dataset_records.save_sample(
                self._build_distillation_sample(
                    session=session,
                    candidate=candidate,
                    decision=decision,
                    record=record,
                )
            )
            if record is not None:
                promoted_records.append(record)
        result = DistillationResult(
            evidence_records=evidence_records,
            candidates=candidates,
            promotion_decisions=tuple(promotion_decisions),
            promoted_records=tuple(
                record for record in promoted_records if record.status is MemoryStatus.ACCEPTED
            ),
        )
        session.memory_candidates = list(candidates)
        session.promotion_decisions = promotion_decisions
        session.context["memory_summary"] = summary.episode_summary
        memory_provider_binding = self._resolve_memory_provider_binding(session=session, profile={})
        provider_governance = self.provider_governance_policy.decide(memory_provider_binding)
        if self.memory_provider_manager is not None and memory_provider_binding is not None:
            if provider_governance.allow_sync_turn:
                self.memory_provider_manager.sync_turn(
                    provider_governance,
                    session.id,
                    tuple(session.events),
                )
            if provider_governance.allow_session_end_writeback:
                self.memory_provider_manager.on_session_end(
                    provider_governance,
                    session.id,
                    result,
                )
            provider_diagnostics = self._resolve_memory_provider_diagnostics(
                provider_governance,
                session.id,
            )
            if provider_diagnostics:
                session.context["memory_provider_diagnostics"] = provider_diagnostics
        self._refresh_session_assembly_manifest(session)
        return result

    def preview_recall(
        self,
        session: AgentSession,
        limit: int | None = None,
    ) -> RecallPreview:
        manifest = self._resolve_session_assembly_manifest(session)
        memory_provider_binding = (
            manifest.memory_provider_binding
            if manifest is not None and manifest.memory_provider_binding is not None
            else self._resolve_memory_provider_binding(session=session, profile={})
        )
        plan = self._resolve_preview_plan(
            session=session,
            manifest=manifest,
            memory_provider_binding=memory_provider_binding,
            limit=limit,
        )
        query = RecallQuery(
            session_id=session.id,
            app_id=session.app_id,
            workflow_id=session.workflow_id,
            scope_filters=plan.scope_filters,
            allowed_statuses=plan.allowed_statuses,
            limit=plan.total_limit,
            query_text=session.user_input or None,
        )
        external_recall_block = self._resolve_external_recall_block(session=session)
        stored_augmentation_diagnostics = self._resolve_stored_augmentation_diagnostics(manifest)
        augmentation = (
            MemoryProviderAugmentation(
                binding=memory_provider_binding,
                recall_block=external_recall_block,
                diagnostics={
                    **stored_augmentation_diagnostics,
                    "source": "session_context",
                },
            )
            if memory_provider_binding is not None and external_recall_block is not None
            else None
        )
        scanned_records = self.memory_records.scan_memory_records(
            plan.scope_filters,
            plan.allowed_statuses,
        )
        retrieved_records = self._select_recall_records(plan, scanned_records, augmentation)
        bundle = self._build_recall_bundle(
            plan,
            scanned_records,
            retrieved_records,
            augmentation,
        )
        scope_breakdowns, record_rankings = self._build_preview_ranking(
            plan=plan,
            scanned_records=scanned_records,
            retrieved_records=retrieved_records,
        )
        metadata = {
            "manifest_sources": manifest.sources if manifest is not None else (),
            "uses_stored_augmentation": external_recall_block is not None,
        }
        return RecallPreview(
            session_id=session.id,
            query=query,
            plan=plan,
            bundle=bundle,
            scope_breakdowns=scope_breakdowns,
            record_rankings=record_rankings,
            augmentation_preview=self._build_augmentation_preview(
                memory_provider_binding=memory_provider_binding,
                augmentation=augmentation,
                external_recall_block=external_recall_block,
            ),
            memory_provider_binding=memory_provider_binding,
            external_recall_block=external_recall_block,
            metadata=metadata,
        )

    def explain_session_memory(self, session: AgentSession) -> Mapping[str, Any]:
        manifest = self._resolve_session_assembly_manifest(session)
        recall_plan = self._recall_plan_from_manifest(manifest)
        lifecycle_review = self.review_lifecycle(session)
        lifecycle_queue = self._project_lifecycle_queue(
            lifecycle_review,
            self._resolve_lifecycle_queue_entries(
                lifecycle_review,
                persist=False,
            ),
            MemoryLifecycleQueueFilter(),
        )
        lifecycle_audit = self.load_lifecycle_audit(session)
        provider_binding_payload = session.context.get("memory_provider_binding")
        if not isinstance(provider_binding_payload, Mapping):
            provider_binding_payload = (
                manifest.memory_provider_binding.to_mapping()
                if manifest is not None and manifest.memory_provider_binding is not None
                else None
            )
        return {
            "session_id": session.id,
            "app_id": session.app_id,
            "workflow_id": session.workflow_id,
            "recalled_memory_ids": tuple(record.id for record in session.recalled_memories),
            "recalled_memory_statuses": tuple(
                record.status.value for record in session.recalled_memories
            ),
            "recalled_memory_scopes": tuple(
                record.scope.value for record in session.recalled_memories
            ),
            "candidate_ids": tuple(candidate.id for candidate in session.memory_candidates),
            "candidate_count": len(session.memory_candidates),
            "promotion_statuses": tuple(
                decision.status.value for decision in session.promotion_decisions
            ),
            "promotion_reasons": tuple(
                decision.reason for decision in session.promotion_decisions
            ),
            "promotion_decisions": tuple(
                {
                    "candidate_id": decision.candidate_id,
                    "status": decision.status.value,
                    "reason": decision.reason,
                    "supporting_refs": decision.supporting_refs,
                }
                for decision in session.promotion_decisions
            ),
            "recalled_count": len(session.recalled_memories),
            "memory_provider_binding": (
                dict(provider_binding_payload)
                if isinstance(provider_binding_payload, Mapping)
                else None
            ),
            "recall_plan": recall_plan.to_mapping() if recall_plan is not None else None,
            "lifecycle_evaluations": tuple(
                self._lifecycle_evaluation_to_mapping(item)
                for item in lifecycle_review.evaluations
            ),
            "lifecycle_queue_summary": self._lifecycle_queue_to_summary_mapping(
                lifecycle_queue
            ),
            "lifecycle_audit_summary": self._lifecycle_audit_to_summary_mapping(
                lifecycle_audit
            ),
            "memory_summary": session.context.get("memory_summary"),
        }

    def review_lifecycle(self, session: AgentSession) -> MemoryLifecycleReviewResult:
        manifest = self._resolve_session_assembly_manifest(session)
        recall_plan = self._recall_plan_from_manifest(manifest)
        evaluations = self._build_lifecycle_evaluations(
            session=session,
            recall_plan=recall_plan,
        )
        scope_filters = (
            recall_plan.scope_filters
            if recall_plan is not None and recall_plan.scope_filters
            else ((MemoryScope.APP, session.app_id),)
        )
        return MemoryLifecycleReviewResult(
            session_id=session.id,
            scope_filters=scope_filters,
            evaluations=evaluations,
            metadata={
                "evaluation_count": len(evaluations),
                "actionable_count": sum(
                    1
                    for item in evaluations
                    if item.allowed and item.current_status is not item.effective_status
                ),
                "hidden_count": sum(1 for item in evaluations if item.hidden),
            },
        )

    def load_lifecycle_queue(
        self,
        session: AgentSession,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue:
        review = self.review_lifecycle(session)
        return self._project_lifecycle_queue(
            review,
            self._resolve_lifecycle_queue_entries(review, persist=True),
            queue_filter,
        )

    def reopen_lifecycle_queue(
        self,
        session: AgentSession,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
        note: str | None = None,
    ) -> MemoryLifecycleQueueUpdateResult:
        return self.update_lifecycle_queue(
            session,
            actor=actor,
            review_status=MemoryLifecycleQueueReviewStatus.PENDING,
            record_ids=record_ids,
            queue_filter=queue_filter,
            note=note,
        )

    def load_lifecycle_audit(
        self,
        session: AgentSession,
        audit_filter: MemoryLifecycleAuditFilter | None = None,
    ) -> MemoryLifecycleAuditLog:
        entries = (
            self.lifecycle_audit_records.list_lifecycle_audit_entries(session.id)
            if self.lifecycle_audit_records is not None
            else ()
        )
        return self._project_lifecycle_audit_log(
            session_id=session.id,
            entries=entries,
            audit_filter=audit_filter,
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
        review = self.review_lifecycle(session)
        entries = self._resolve_lifecycle_queue_entries(review, persist=False)
        (
            selected_record_ids,
            resolved_queue_filter,
            selection_source,
        ) = self._resolve_lifecycle_queue_selection(
            review=review,
            entries=entries,
            record_ids=record_ids,
            queue_filter=queue_filter,
            use_selected_by_default=False,
            require_selection=True,
            error_message=(
                "Lifecycle queue update requires record_ids or queue_filter."
            ),
        )
        entries_by_record_id = {entry.record_id: entry for entry in entries}
        updated_entries, updated_record_ids, missing_record_ids = (
            self._apply_lifecycle_queue_review_status(
                entries=entries,
                record_ids=selected_record_ids,
                review_status=review_status,
                actor=actor,
                note=note,
                resolution=resolution,
            )
        )
        if self.lifecycle_queue_records is not None:
            self.lifecycle_queue_records.replace_lifecycle_queue_entries(
                session.id,
                updated_entries,
            )
        queue = self._project_lifecycle_queue(
            review,
            updated_entries,
            MemoryLifecycleQueueFilter(),
        )
        result = MemoryLifecycleQueueUpdateResult(
            session_id=session.id,
            actor=actor,
            review_status=review_status,
            resolution=resolution,
            queue_filter=resolved_queue_filter,
            requested_record_ids=selected_record_ids,
            updated_record_ids=updated_record_ids,
            missing_record_ids=missing_record_ids,
            queue=queue,
            metadata={
                "note": note,
                "resolution": resolution.value if resolution is not None else None,
                "selection_source": selection_source,
                "updated_count": len(updated_record_ids),
                "missing_count": len(missing_record_ids),
                "audit_entry_count": 0,
            },
        )
        audit_entries = self._build_lifecycle_queue_update_audit_entries(
            session_id=session.id,
            actor=actor,
            previous_entries=entries_by_record_id,
            updated_entries=updated_entries,
            updated_record_ids=updated_record_ids,
            note=note,
        )
        if audit_entries and self.lifecycle_audit_records is not None:
            self.lifecycle_audit_records.append_lifecycle_audit_entries(
                session.id,
                audit_entries,
            )
        return replace(
            result,
            metadata={
                **dict(result.metadata),
                "audit_entry_count": len(audit_entries),
            },
        )

    def apply_lifecycle(
        self,
        session: AgentSession,
        actor: str,
        record_ids: tuple[str, ...] | None = None,
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleApplyResult:
        review = self.review_lifecycle(session)
        queue_entries = self._resolve_lifecycle_queue_entries(review, persist=True)
        queue_entries_by_record_id = {entry.record_id: entry for entry in queue_entries}
        (
            selected_record_ids,
            resolved_queue_filter,
            selection_source,
        ) = self._resolve_lifecycle_queue_selection(
            review=review,
            entries=queue_entries,
            record_ids=record_ids,
            queue_filter=queue_filter,
            use_selected_by_default=True,
            require_selection=False,
        )
        selected_set = set(selected_record_ids)
        records = self.memory_records.scan_memory_records(
            review.scope_filters,
            tuple(status for status in MemoryStatus),
        )
        records_by_id = {record.id: record for record in records}
        applied_ids: list[str] = []
        skipped_ids: list[str] = []
        updated_records: list[MemoryRecord] = []
        applied_evaluations: list[MemoryLifecycleEvaluation] = []
        applied_at = datetime.now(timezone.utc).isoformat()

        for evaluation in review.evaluations:
            if evaluation.record_id not in selected_set:
                continue
            if (
                evaluation.allowed
                and evaluation.current_status is not evaluation.effective_status
                and evaluation.record_id in records_by_id
            ):
                record = records_by_id[evaluation.record_id]
                updated_record = replace(
                    record,
                    status=evaluation.effective_status,
                    metadata={
                        **dict(record.metadata),
                        "lifecycle_previous_status": record.status.value,
                        "lifecycle_reason": evaluation.reason,
                        "lifecycle_hidden": evaluation.hidden,
                        "lifecycle_applied_at": applied_at,
                        "lifecycle_applied_by": actor,
                        "lifecycle_metadata": dict(evaluation.metadata),
                    },
                )
                self.memory_records.save_memory_record(updated_record)
                records_by_id[evaluation.record_id] = updated_record
                updated_records.append(updated_record)
                applied_ids.append(evaluation.record_id)
                applied_evaluations.append(evaluation)
            else:
                skipped_ids.append(evaluation.record_id)

        unknown_record_ids = tuple(
            record_id for record_id in selected_record_ids if record_id not in records_by_id
        )
        result = MemoryLifecycleApplyResult(
            session_id=session.id,
            actor=actor,
            queue_filter=resolved_queue_filter,
            selected_record_ids=selected_record_ids,
            applied_record_ids=tuple(applied_ids),
            skipped_record_ids=tuple(
                list(skipped_ids)
                + [record_id for record_id in unknown_record_ids if record_id not in skipped_ids]
            ),
            updated_records=tuple(updated_records),
            evaluations=tuple(applied_evaluations),
            metadata={
                "selection_source": selection_source,
                "requested_count": len(selected_record_ids),
                "applied_count": len(applied_ids),
                "skipped_count": len(skipped_ids),
                "unknown_record_ids": unknown_record_ids,
                "audit_entry_count": 0,
            },
        )
        refreshed_review = self.review_lifecycle(session)
        refreshed_entries = self._resolve_lifecycle_queue_entries(
            refreshed_review,
            persist=False,
        )
        refreshed_entries, _, _ = self._apply_lifecycle_queue_review_status(
            entries=refreshed_entries,
            record_ids=tuple(applied_ids),
            review_status=MemoryLifecycleQueueReviewStatus.APPLIED,
            actor=actor,
            note=None,
            resolution=None,
        )
        if self.lifecycle_queue_records is not None:
            self.lifecycle_queue_records.replace_lifecycle_queue_entries(
                session.id,
                refreshed_entries,
            )
        provider_binding = self._resolve_memory_provider_binding(session=session, profile={})
        provider_governance = self.provider_governance_policy.decide(provider_binding)
        provider_writeback_triggered = False
        audit_entries: tuple[MemoryLifecycleAuditEntry, ...] = ()
        if updated_records:
            if (
                self.memory_provider_manager is not None
                and provider_binding is not None
                and provider_governance.allow_lifecycle_writeback
                and result.applied_record_ids
            ):
                self.memory_provider_manager.on_lifecycle_apply(
                    provider_governance,
                    session.id,
                    result,
                )
                provider_writeback_triggered = True
                provider_diagnostics = self._resolve_memory_provider_diagnostics(
                    provider_governance,
                    session.id,
                )
                if provider_diagnostics:
                    session.context["memory_provider_diagnostics"] = provider_diagnostics
            updated_record_map = {record.id: record for record in updated_records}
            session.recalled_memories = [
                updated_record_map.get(record.id, record)
                for record in session.recalled_memories
                if updated_record_map.get(record.id, record).status is MemoryStatus.ACCEPTED
            ]
            session.context["memory_lifecycle_apply"] = {
                "actor": actor,
                "applied_record_ids": tuple(applied_ids),
                "applied_at": applied_at,
                "provider_writeback_triggered": provider_writeback_triggered,
            }
            self._refresh_session_assembly_manifest(session)
        audit_entries = self._build_lifecycle_apply_audit_entries(
            session_id=session.id,
            actor=actor,
            evaluations=tuple(applied_evaluations),
            queue_entries=queue_entries_by_record_id,
            provider_writeback_triggered=provider_writeback_triggered,
            queue_filter=resolved_queue_filter,
        )
        if audit_entries and self.lifecycle_audit_records is not None:
            self.lifecycle_audit_records.append_lifecycle_audit_entries(
                session.id,
                audit_entries,
            )
        return replace(
            result,
            metadata={
                **dict(result.metadata),
                "audit_entry_count": len(audit_entries),
                "provider_id": (
                    provider_binding.provider_id
                    if provider_binding is not None
                    else None
                ),
                "provider_writeback_triggered": provider_writeback_triggered,
            },
        )

    def _resolve_project_scope_key(
        self,
        profile: Mapping[str, Any],
        rules: Mapping[str, Any],
    ) -> str | None:
        for source in (rules, profile):
            value = source.get("project_scope_key")
            if value is not None:
                return str(value)
        return self.default_project_scope_key

    def _plan_recall(
        self,
        session: AgentSession,
        app_id: str,
        workflow_id: str,
        profile_id: str | None,
        project_scope_key: str | None,
        provider_decision: MemoryProviderGovernanceDecision,
        default_limit: int | None = None,
    ) -> RecallPlan:
        governance_decision = self.recall_governance_policy.decide(
            session=session,
            app_id=app_id,
            workflow_id=workflow_id,
            profile_id=profile_id,
            project_scope_key=project_scope_key,
            provider_decision=provider_decision,
            default_limit=default_limit,
        )
        if self.recall_planner is not None:
            return self.recall_planner.plan(governance_decision)
        return self._build_recall_plan_from_decision(governance_decision)

    def _build_recall_plan_from_decision(
        self,
        decision: RecallGovernanceDecision,
    ) -> RecallPlan:
        return decision.to_recall_plan(
            scope_budgets=self._allocate_scope_budgets(
                decision.scope_filters,
                decision.total_limit,
            )
        )

    def _build_plan_from_query(self, query: RecallQuery) -> RecallPlan:
        decision = RecallGovernanceDecision(
            scope_filters=query.scope_filters,
            allowed_statuses=query.allowed_statuses,
            total_limit=query.limit,
            ranking_strategy="scope_budget_confidence_recency",
            metadata={
                "session_id": query.session_id,
                "app_id": query.app_id,
                "workflow_id": query.workflow_id,
            },
        )
        return self._build_recall_plan_from_decision(decision)

    def _resolve_preview_plan(
        self,
        session: AgentSession,
        manifest: SessionAssemblyManifest | None,
        memory_provider_binding: MemoryProviderBinding | None,
        limit: int | None,
    ) -> RecallPlan:
        stored_plan = self._recall_plan_from_manifest(manifest)
        if stored_plan is None:
            scope_filters = self._preview_scope_filters(session=session, manifest=manifest)
            resolved_limit = max(1, int(limit or 8))
            return RecallPlan(
                scope_filters=scope_filters,
                allowed_statuses=(MemoryStatus.ACCEPTED,),
                total_limit=resolved_limit,
                scope_budgets=self._allocate_scope_budgets(scope_filters, resolved_limit),
                ranking_strategy="scope_budget_confidence_recency",
                within_scope_order=("confidence:desc", "created_at:asc", "id:asc"),
                overflow_order=(
                    "scope_order:asc",
                    "confidence:desc",
                    "created_at:asc",
                    "id:asc",
                ),
                overflow_fill_enabled=True,
                include_external_augmentation=memory_provider_binding is not None,
                metadata={
                    "session_id": session.id,
                    "app_id": session.app_id,
                    "workflow_id": session.workflow_id,
                    "preview": True,
                },
            )
        resolved_limit = max(1, int(limit or stored_plan.total_limit))
        return RecallPlan(
            scope_filters=stored_plan.scope_filters,
            allowed_statuses=stored_plan.allowed_statuses,
            total_limit=resolved_limit,
            scope_budgets=self._allocate_scope_budgets(
                stored_plan.scope_filters,
                resolved_limit,
            ),
            ranking_strategy=stored_plan.ranking_strategy,
            within_scope_order=stored_plan.within_scope_order,
            overflow_order=stored_plan.overflow_order,
            overflow_fill_enabled=stored_plan.overflow_fill_enabled,
            include_external_augmentation=(
                stored_plan.include_external_augmentation
                or memory_provider_binding is not None
            ),
            metadata={
                **dict(stored_plan.metadata),
                "session_id": session.id,
                "app_id": session.app_id,
                "workflow_id": session.workflow_id,
                "preview": True,
            },
        )

    def _preview_scope_filters(
        self,
        session: AgentSession,
        manifest: SessionAssemblyManifest | None,
    ) -> tuple[tuple[MemoryScope, str], ...]:
        if manifest is not None and manifest.recall_scope_filters:
            return tuple(
                (MemoryScope(scope), scope_key)
                for scope, scope_key in manifest.recall_scope_filters
            )
        return ((MemoryScope.APP, session.app_id),)

    def _recall_plan_from_manifest(
        self,
        manifest: SessionAssemblyManifest | None,
    ) -> RecallPlan | None:
        if manifest is None:
            return None
        diagnostics = manifest.metadata.get("diagnostics")
        if not isinstance(diagnostics, Mapping):
            return None
        payload = diagnostics.get("recall_plan")
        if not isinstance(payload, Mapping):
            return None
        return RecallPlan.from_mapping(payload)

    def _resolve_stored_augmentation_diagnostics(
        self,
        manifest: SessionAssemblyManifest | None,
    ) -> dict[str, Any]:
        if manifest is None:
            return {}
        diagnostics = manifest.metadata.get("diagnostics")
        if not isinstance(diagnostics, Mapping):
            return {}
        provider_id = (
            manifest.memory_provider_binding.provider_id
            if manifest.memory_provider_binding is not None
            else None
        )
        return project_stored_augmentation_diagnostics(
            diagnostics,
            provider_id=provider_id,
            binding_metadata=(
                manifest.memory_provider_binding.metadata
                if manifest.memory_provider_binding is not None
                else None
            ),
        )

    def _resolve_session_assembly_manifest(
        self,
        session: AgentSession,
    ) -> SessionAssemblyManifest | None:
        payload = session.context.get("assembly_manifest")
        if not isinstance(payload, Mapping):
            return None
        return SessionAssemblyManifest.from_mapping(payload)

    def _resolve_external_recall_block(self, session: AgentSession) -> str | None:
        payload = session.context.get("external_memory_recall_block")
        if payload is None:
            return None
        text = str(payload).strip()
        return text or None

    def _build_lifecycle_evaluations(
        self,
        *,
        session: AgentSession,
        recall_plan: RecallPlan | None,
    ) -> tuple[MemoryLifecycleEvaluation, ...]:
        scope_filters = (
            recall_plan.scope_filters
            if recall_plan is not None and recall_plan.scope_filters
            else ((MemoryScope.APP, session.app_id),)
        )
        records = self.memory_records.scan_memory_records(
            scope_filters,
            tuple(status for status in MemoryStatus),
        )
        scope_order = {scope_filter: index for index, scope_filter in enumerate(scope_filters)}
        ordered_records = tuple(
            sorted(
                records,
                key=lambda record: (
                    scope_order.get((record.scope, record.scope_key), len(scope_order)),
                    -record.created_at.timestamp(),
                    record.id,
                ),
            )
        )
        evaluations: list[MemoryLifecycleEvaluation] = []
        for record in ordered_records:
            decision = self.lifecycle_policy.evaluate_record(
                record,
                related_records=ordered_records,
            )
            evaluations.append(
                MemoryLifecycleEvaluation(
                    record_id=record.id,
                    scope=record.scope,
                    scope_key=record.scope_key,
                    current_status=record.status,
                    effective_status=decision.target_status,
                    reason=decision.reason,
                    allowed=decision.allowed,
                    hidden=bool(decision.metadata.get("hidden", False)),
                    metadata=dict(decision.metadata),
                )
            )
        return tuple(evaluations)

    @staticmethod
    def _lifecycle_evaluation_to_mapping(
        evaluation: MemoryLifecycleEvaluation,
    ) -> dict[str, Any]:
        return {
            "record_id": evaluation.record_id,
            "scope": evaluation.scope.value,
            "scope_key": evaluation.scope_key,
            "current_status": evaluation.current_status.value,
            "effective_status": evaluation.effective_status.value,
            "reason": evaluation.reason,
            "allowed": evaluation.allowed,
            "hidden": evaluation.hidden,
            "metadata": dict(evaluation.metadata),
        }

    def _resolve_lifecycle_queue_entries(
        self,
        review: MemoryLifecycleReviewResult,
        *,
        persist: bool,
    ) -> tuple[MemoryLifecycleQueueEntry, ...]:
        stored_entries = (
            self.lifecycle_queue_records.list_lifecycle_queue_entries(review.session_id)
            if self.lifecycle_queue_records is not None
            else ()
        )
        stored_by_record_id = {
            entry.record_id: entry
            for entry in stored_entries
        }
        entries = tuple(
            self._merge_lifecycle_queue_entry(
                review.session_id,
                evaluation,
                stored_by_record_id.get(evaluation.record_id),
            )
            for evaluation in review.evaluations
        )
        if persist and self.lifecycle_queue_records is not None:
            self.lifecycle_queue_records.replace_lifecycle_queue_entries(
                review.session_id,
                entries,
            )
        return entries

    def _merge_lifecycle_queue_entry(
        self,
        session_id: str,
        evaluation: MemoryLifecycleEvaluation,
        existing: MemoryLifecycleQueueEntry | None,
    ) -> MemoryLifecycleQueueEntry:
        action_required = bool(
            evaluation.allowed and evaluation.current_status is not evaluation.effective_status
        )
        review_status = (
            existing.review_status
            if existing is not None
            else MemoryLifecycleQueueReviewStatus.PENDING
        )
        return MemoryLifecycleQueueEntry(
            id=self._lifecycle_queue_entry_id(session_id, evaluation.record_id),
            session_id=session_id,
            record_id=evaluation.record_id,
            scope=evaluation.scope,
            scope_key=evaluation.scope_key,
            current_status=evaluation.current_status,
            effective_status=evaluation.effective_status,
            reason=evaluation.reason,
            allowed=evaluation.allowed,
            hidden=evaluation.hidden,
            action_required=action_required,
            selected_by_default=(
                action_required
                and review_status is MemoryLifecycleQueueReviewStatus.PENDING
            ),
            review_status=review_status,
            review_resolution=existing.review_resolution if existing is not None else None,
            reviewed_by=existing.reviewed_by if existing is not None else None,
            reviewed_at=existing.reviewed_at if existing is not None else None,
            review_note=existing.review_note if existing is not None else None,
            metadata=dict(evaluation.metadata),
        )

    @staticmethod
    def _lifecycle_queue_entry_id(session_id: str, record_id: str) -> str:
        return f"lifecycle-queue:{session_id}:{record_id}"

    def _project_lifecycle_queue(
        self,
        review: MemoryLifecycleReviewResult,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
        queue_filter: MemoryLifecycleQueueFilter | None = None,
    ) -> MemoryLifecycleQueue:
        resolved_filter = queue_filter or MemoryLifecycleQueueFilter()
        total_actionable = sum(1 for entry in entries if entry.action_required)
        selected_items: list[MemoryLifecycleQueueItem] = []
        for entry in entries:
            item = self._lifecycle_queue_item_from_entry(entry)
            if not self._matches_lifecycle_queue_filter(item, resolved_filter):
                continue
            selected_items.append(item)
            if (
                resolved_filter.limit is not None
                and len(selected_items) >= max(0, resolved_filter.limit)
            ):
                break
        selected_record_ids = tuple(
            item.record_id for item in selected_items if item.selected_by_default
        )
        reason_counts: dict[str, int] = {}
        effective_status_counts: dict[str, int] = {}
        review_status_counts: dict[str, int] = {}
        resolution_counts: dict[str, int] = {}
        resolution_required_count = 0
        for item in selected_items:
            reason_counts[item.reason] = reason_counts.get(item.reason, 0) + 1
            effective_key = item.effective_status.value
            effective_status_counts[effective_key] = (
                effective_status_counts.get(effective_key, 0) + 1
            )
            review_key = item.review_status.value
            review_status_counts[review_key] = review_status_counts.get(review_key, 0) + 1
            if item.resolution_required:
                resolution_required_count += 1
            if item.review_resolution is not None:
                resolution_key = item.review_resolution.value
                resolution_counts[resolution_key] = (
                    resolution_counts.get(resolution_key, 0) + 1
                )
        return MemoryLifecycleQueue(
            session_id=review.session_id,
            scope_filters=review.scope_filters,
            queue_filter=resolved_filter,
            items=tuple(selected_items),
            selected_record_ids=selected_record_ids,
            total_evaluation_count=len(review.evaluations),
            actionable_count=total_actionable,
            hidden_count=sum(1 for item in selected_items if item.hidden),
            metadata={
                "filtered_count": len(selected_items),
                "selected_count": len(selected_record_ids),
                "reason_counts": reason_counts,
                "effective_status_counts": effective_status_counts,
                "review_status_counts": review_status_counts,
                "resolution_counts": resolution_counts,
                "resolution_required_count": resolution_required_count,
            },
        )

    def _lifecycle_queue_item_from_entry(
        self,
        entry: MemoryLifecycleQueueEntry,
    ) -> MemoryLifecycleQueueItem:
        resolution_options = self._build_lifecycle_resolution_options(entry)
        return MemoryLifecycleQueueItem(
            record_id=entry.record_id,
            scope=entry.scope,
            scope_key=entry.scope_key,
            current_status=entry.current_status,
            effective_status=entry.effective_status,
            reason=entry.reason,
            allowed=entry.allowed,
            hidden=entry.hidden,
            action_required=entry.action_required,
            selected_by_default=entry.selected_by_default,
            review_status=entry.review_status,
            review_resolution=entry.review_resolution,
            resolution_required=bool(entry.action_required and resolution_options),
            resolution_options=resolution_options,
            reviewed_by=entry.reviewed_by,
            reviewed_at=entry.reviewed_at,
            review_note=entry.review_note,
            metadata=dict(entry.metadata),
        )

    @staticmethod
    def _build_lifecycle_resolution_options(
        entry: MemoryLifecycleQueueEntry,
    ) -> tuple[MemoryLifecycleResolutionOption, ...]:
        if not entry.action_required or not entry.allowed:
            return ()
        if entry.reason == "conflict_superseded":
            return (
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.CONFLICT_CONFIRMED,
                    description=(
                        "Confirm the newer conflicting memory should supersede this record."
                    ),
                    suggested_note=(
                        "Conflict confirmed; allow the newer memory to supersede this record."
                    ),
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.KEEP_CURRENT,
                    description=(
                        "Keep this memory active despite the newer conflicting record."
                    ),
                    suggested_note=(
                        "Keep current memory active; override the supersede recommendation."
                    ),
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.DEFERRED,
                    description="Leave this conflict pending for another reviewer pass.",
                    suggested_note="Defer conflict triage for manual follow-up.",
                ),
            )
        if entry.reason == "decay_expired":
            return (
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.STALE_SIGNAL,
                    description="Confirm the memory is stale and can be forgotten.",
                    suggested_note="Stale signal confirmed; allow this memory to expire.",
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.KEEP_CURRENT,
                    description=(
                        "Keep this memory active because the signal is still relevant."
                    ),
                    suggested_note="Keep current memory active; reject the stale-signal decay.",
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.DEFERRED,
                    description="Leave this stale-signal review pending for later follow-up.",
                    suggested_note="Defer stale-signal triage for manual follow-up.",
                ),
            )
        if entry.reason == "manual_override_applied":
            override_reason = entry.metadata.get("manual_override_reason")
            override_suffix = (
                f" ({override_reason})"
                if override_reason not in (None, "")
                else ""
            )
            return (
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.MANUAL_OVERRIDE,
                    description=(
                        "Accept the manual override as the authoritative lifecycle decision."
                        + override_suffix
                    ),
                    suggested_note=(
                        "Manual override confirmed; keep the reviewer-authored lifecycle state."
                    ),
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.KEEP_CURRENT,
                    description="Reject the override and keep the current lifecycle state.",
                    suggested_note="Keep current lifecycle state; manual override rejected.",
                ),
                MemoryLifecycleResolutionOption(
                    resolution=MemoryLifecycleReviewResolution.DEFERRED,
                    description="Defer the manual override for another reviewer pass.",
                    suggested_note="Defer manual override review for manual follow-up.",
                ),
            )
        return (
            MemoryLifecycleResolutionOption(
                resolution=MemoryLifecycleReviewResolution.DEFERRED,
                description="Leave this lifecycle item pending for a later review.",
                suggested_note="Defer lifecycle review for manual follow-up.",
            ),
        )

    def _apply_lifecycle_queue_review_status(
        self,
        *,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
        record_ids: tuple[str, ...],
        review_status: MemoryLifecycleQueueReviewStatus,
        actor: str,
        note: str | None,
        resolution: MemoryLifecycleReviewResolution | None,
    ) -> tuple[tuple[MemoryLifecycleQueueEntry, ...], tuple[str, ...], tuple[str, ...]]:
        entry_by_record_id = {
            entry.record_id: entry
            for entry in entries
        }
        updated_record_ids: list[str] = []
        missing_record_ids: list[str] = []
        reviewed_at = datetime.now(timezone.utc)
        for record_id in record_ids:
            entry = entry_by_record_id.get(record_id)
            if entry is None:
                missing_record_ids.append(record_id)
                continue
            next_resolution = (
                None
                if review_status is MemoryLifecycleQueueReviewStatus.PENDING
                else resolution
                if resolution is not None
                else entry.review_resolution
            )
            if (
                entry.review_status is review_status
                and entry.review_note == note
                and entry.review_resolution is next_resolution
            ):
                continue
            entry_by_record_id[record_id] = replace(
                entry,
                review_status=review_status,
                review_resolution=next_resolution,
                reviewed_by=actor,
                reviewed_at=reviewed_at,
                review_note=note,
                selected_by_default=(
                    entry.action_required
                    and review_status is MemoryLifecycleQueueReviewStatus.PENDING
                ),
            )
            updated_record_ids.append(record_id)
        ordered_entries = tuple(
            entry_by_record_id[entry.record_id]
            for entry in entries
        )
        return (
            ordered_entries,
            tuple(updated_record_ids),
            tuple(missing_record_ids),
        )

    def _resolve_lifecycle_queue_selection(
        self,
        *,
        review: MemoryLifecycleReviewResult,
        entries: tuple[MemoryLifecycleQueueEntry, ...],
        record_ids: tuple[str, ...] | None,
        queue_filter: MemoryLifecycleQueueFilter | None,
        use_selected_by_default: bool,
        require_selection: bool,
        error_message: str = "Lifecycle queue selection requires record_ids or queue_filter.",
    ) -> tuple[tuple[str, ...], MemoryLifecycleQueueFilter | None, str]:
        if record_ids is not None:
            return tuple(record_ids), None, "record_ids"
        if queue_filter is not None:
            queue = self._project_lifecycle_queue(review, entries, queue_filter)
            selected_record_ids = (
                queue.selected_record_ids
                if use_selected_by_default
                else tuple(item.record_id for item in queue.items)
            )
            return selected_record_ids, queue.queue_filter, "queue_filter"
        if require_selection:
            raise ValueError(error_message)
        return (
            tuple(item.record_id for item in review.evaluations),
            None,
            "default_all",
        )

    @staticmethod
    def _matches_lifecycle_queue_filter(
        item: MemoryLifecycleQueueItem,
        queue_filter: MemoryLifecycleQueueFilter,
    ) -> bool:
        if queue_filter.actionable_only and not item.action_required:
            return False
        if not queue_filter.include_hidden and item.hidden:
            return False
        if queue_filter.reasons and item.reason not in queue_filter.reasons:
            return False
        if (
            queue_filter.effective_statuses
            and item.effective_status not in queue_filter.effective_statuses
        ):
            return False
        if (
            queue_filter.current_statuses
            and item.current_status not in queue_filter.current_statuses
        ):
            return False
        if (
            queue_filter.review_statuses
            and item.review_status not in queue_filter.review_statuses
        ):
            return False
        if (
            queue_filter.review_resolutions
            and item.review_resolution not in queue_filter.review_resolutions
        ):
            return False
        return True

    @staticmethod
    def _lifecycle_queue_filter_to_mapping(
        queue_filter: MemoryLifecycleQueueFilter,
    ) -> dict[str, Any]:
        return {
            "actionable_only": queue_filter.actionable_only,
            "include_hidden": queue_filter.include_hidden,
            "reasons": queue_filter.reasons,
            "effective_statuses": tuple(
                status.value for status in queue_filter.effective_statuses
            ),
            "current_statuses": tuple(
                status.value for status in queue_filter.current_statuses
            ),
            "review_statuses": tuple(
                status.value for status in queue_filter.review_statuses
            ),
            "review_resolutions": tuple(
                resolution.value for resolution in queue_filter.review_resolutions
            ),
            "limit": queue_filter.limit,
        }

    def _lifecycle_queue_to_summary_mapping(
        self,
        queue: MemoryLifecycleQueue,
    ) -> dict[str, Any]:
        return {
            "filter": self._lifecycle_queue_filter_to_mapping(queue.queue_filter),
            "selected_record_ids": queue.selected_record_ids,
            "total_evaluation_count": queue.total_evaluation_count,
            "actionable_count": queue.actionable_count,
            "filtered_count": len(queue.items),
            "hidden_count": queue.hidden_count,
            "reason_counts": dict(queue.metadata.get("reason_counts", {})),
            "effective_status_counts": dict(
                queue.metadata.get("effective_status_counts", {})
            ),
            "review_status_counts": dict(
                queue.metadata.get("review_status_counts", {})
            ),
            "resolution_counts": dict(queue.metadata.get("resolution_counts", {})),
            "resolution_required_count": int(
                queue.metadata.get("resolution_required_count", 0)
            ),
        }

    def _build_lifecycle_queue_update_audit_entries(
        self,
        *,
        session_id: str,
        actor: str,
        previous_entries: Mapping[str, MemoryLifecycleQueueEntry],
        updated_entries: tuple[MemoryLifecycleQueueEntry, ...],
        updated_record_ids: tuple[str, ...],
        note: str | None,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        updated_by_record_id = {entry.record_id: entry for entry in updated_entries}
        audit_entries: list[MemoryLifecycleAuditEntry] = []
        for record_id in updated_record_ids:
            previous_entry = previous_entries.get(record_id)
            updated_entry = updated_by_record_id.get(record_id)
            if previous_entry is None or updated_entry is None:
                continue
            if previous_entry.review_status is not updated_entry.review_status:
                action = (
                    MemoryLifecycleAuditAction.REVIEW_REOPENED
                    if updated_entry.review_status
                    is MemoryLifecycleQueueReviewStatus.PENDING
                    else MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED
                )
            elif previous_entry.review_note != updated_entry.review_note:
                action = MemoryLifecycleAuditAction.REVIEW_NOTE_UPDATED
            else:
                continue
            audit_entries.append(
                MemoryLifecycleAuditEntry(
                    id=self._lifecycle_audit_entry_id(
                        session_id,
                        record_id,
                        action,
                        len(audit_entries),
                    ),
                    session_id=session_id,
                    record_id=record_id,
                    actor=actor,
                    action=action,
                    current_status=updated_entry.current_status,
                    effective_status=updated_entry.effective_status,
                    queue_review_status=updated_entry.review_status,
                    resolution=updated_entry.review_resolution,
                    reason=updated_entry.reason,
                    note=note,
                    metadata={
                        "previous_review_status": previous_entry.review_status.value,
                        "previous_review_resolution": (
                            previous_entry.review_resolution.value
                            if previous_entry.review_resolution is not None
                            else None
                        ),
                        "previous_review_note": previous_entry.review_note,
                    },
                )
            )
        return tuple(audit_entries)

    def _build_lifecycle_apply_audit_entries(
        self,
        *,
        session_id: str,
        actor: str,
        evaluations: tuple[MemoryLifecycleEvaluation, ...],
        queue_entries: Mapping[str, MemoryLifecycleQueueEntry],
        provider_writeback_triggered: bool,
        queue_filter: MemoryLifecycleQueueFilter | None,
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        audit_entries: list[MemoryLifecycleAuditEntry] = []
        for evaluation in evaluations:
            queue_entry = queue_entries.get(evaluation.record_id)
            audit_entries.append(
                MemoryLifecycleAuditEntry(
                    id=self._lifecycle_audit_entry_id(
                        session_id,
                        evaluation.record_id,
                        MemoryLifecycleAuditAction.LIFECYCLE_APPLIED,
                        len(audit_entries),
                    ),
                    session_id=session_id,
                    record_id=evaluation.record_id,
                    actor=actor,
                    action=MemoryLifecycleAuditAction.LIFECYCLE_APPLIED,
                    current_status=evaluation.current_status,
                    effective_status=evaluation.effective_status,
                    queue_review_status=MemoryLifecycleQueueReviewStatus.APPLIED,
                    resolution=(
                        queue_entry.review_resolution if queue_entry is not None else None
                    ),
                    reason=evaluation.reason,
                    metadata={
                        "previous_review_status": (
                            queue_entry.review_status.value
                            if queue_entry is not None
                            else None
                        ),
                        "provider_writeback_triggered": provider_writeback_triggered,
                        "queue_filter": (
                            self._lifecycle_queue_filter_to_mapping(queue_filter)
                            if queue_filter is not None
                            else None
                        ),
                    },
                )
            )
        return tuple(audit_entries)

    def _lifecycle_audit_entry_id(
        self,
        session_id: str,
        record_id: str,
        action: MemoryLifecycleAuditAction,
        offset: int,
    ) -> str:
        return "lifecycle-audit:" + self._stable_id(
            session_id,
            record_id,
            action.value,
            datetime.now(timezone.utc).isoformat(),
            str(offset),
        )

    def _project_lifecycle_audit_log(
        self,
        *,
        session_id: str,
        entries: tuple[MemoryLifecycleAuditEntry, ...],
        audit_filter: MemoryLifecycleAuditFilter | None,
    ) -> MemoryLifecycleAuditLog:
        resolved_filter = audit_filter or MemoryLifecycleAuditFilter()
        selected_entries = tuple(
            entry
            for entry in entries
            if self._matches_lifecycle_audit_filter(entry, resolved_filter)
        )
        selected_entries = self._order_lifecycle_audit_entries(selected_entries)
        if resolved_filter.latest_per_record_only:
            selected_entries = self._latest_lifecycle_audit_entries_by_record(
                selected_entries
            )
        if resolved_filter.limit is not None:
            selected_entries = selected_entries[: max(0, resolved_filter.limit)]
        action_counts: dict[str, int] = {}
        actor_counts: dict[str, int] = {}
        review_status_counts: dict[str, int] = {}
        resolution_counts: dict[str, int] = {}
        for entry in selected_entries:
            action_counts[entry.action.value] = action_counts.get(entry.action.value, 0) + 1
            actor_counts[entry.actor] = actor_counts.get(entry.actor, 0) + 1
            if entry.queue_review_status is not None:
                review_status_key = entry.queue_review_status.value
                review_status_counts[review_status_key] = (
                    review_status_counts.get(review_status_key, 0) + 1
                )
            if entry.resolution is not None:
                resolution_key = entry.resolution.value
                resolution_counts[resolution_key] = (
                    resolution_counts.get(resolution_key, 0) + 1
                )
        return MemoryLifecycleAuditLog(
            session_id=session_id,
            audit_filter=resolved_filter,
            entries=selected_entries,
            metadata={
                "entry_count": len(selected_entries),
                "action_counts": action_counts,
                "actor_counts": actor_counts,
                "review_status_counts": review_status_counts,
                "resolution_counts": resolution_counts,
            },
        )

    @staticmethod
    def _matches_lifecycle_audit_filter(
        entry: MemoryLifecycleAuditEntry,
        audit_filter: MemoryLifecycleAuditFilter,
    ) -> bool:
        if audit_filter.actions and entry.action not in audit_filter.actions:
            return False
        if audit_filter.record_ids and entry.record_id not in audit_filter.record_ids:
            return False
        if audit_filter.actors and entry.actor not in audit_filter.actors:
            return False
        if (
            audit_filter.queue_review_statuses
            and entry.queue_review_status not in audit_filter.queue_review_statuses
        ):
            return False
        if audit_filter.resolutions and entry.resolution not in audit_filter.resolutions:
            return False
        return True

    @staticmethod
    def _lifecycle_audit_filter_to_mapping(
        audit_filter: MemoryLifecycleAuditFilter,
    ) -> dict[str, Any]:
        return {
            "actions": tuple(action.value for action in audit_filter.actions),
            "record_ids": audit_filter.record_ids,
            "actors": audit_filter.actors,
            "queue_review_statuses": tuple(
                status.value for status in audit_filter.queue_review_statuses
            ),
            "resolutions": tuple(
                resolution.value for resolution in audit_filter.resolutions
            ),
            "latest_per_record_only": audit_filter.latest_per_record_only,
            "limit": audit_filter.limit,
        }

    def _lifecycle_audit_to_summary_mapping(
        self,
        audit_log: MemoryLifecycleAuditLog,
    ) -> dict[str, Any]:
        return {
            "filter": self._lifecycle_audit_filter_to_mapping(audit_log.audit_filter),
            "entry_count": len(audit_log.entries),
            "action_counts": dict(audit_log.metadata.get("action_counts", {})),
            "actor_counts": dict(audit_log.metadata.get("actor_counts", {})),
            "review_status_counts": dict(
                audit_log.metadata.get("review_status_counts", {})
            ),
            "resolution_counts": dict(
                audit_log.metadata.get("resolution_counts", {})
            ),
            "latest_entries": tuple(
                self._lifecycle_audit_entry_to_mapping(entry)
                for entry in audit_log.entries[:5]
            ),
            "latest_by_record": tuple(
                self._lifecycle_audit_entry_to_mapping(entry)
                for entry in self._latest_lifecycle_audit_entries_by_record(
                    audit_log.entries
                )
            ),
        }

    @staticmethod
    def _order_lifecycle_audit_entries(
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        indexed_entries = tuple(enumerate(entries))
        return tuple(
            entry
            for _, entry in sorted(
                indexed_entries,
                key=lambda item: (item[1].created_at, item[0]),
                reverse=True,
            )
        )

    @staticmethod
    def _latest_lifecycle_audit_entries_by_record(
        entries: tuple[MemoryLifecycleAuditEntry, ...],
    ) -> tuple[MemoryLifecycleAuditEntry, ...]:
        latest_by_record: dict[str, MemoryLifecycleAuditEntry] = {}
        ordered_entries: list[MemoryLifecycleAuditEntry] = []
        for entry in entries:
            if entry.record_id in latest_by_record:
                continue
            latest_by_record[entry.record_id] = entry
            ordered_entries.append(entry)
        return tuple(ordered_entries)

    @staticmethod
    def _lifecycle_audit_entry_to_mapping(
        entry: MemoryLifecycleAuditEntry,
    ) -> dict[str, Any]:
        return {
            "record_id": entry.record_id,
            "actor": entry.actor,
            "action": entry.action.value,
            "queue_review_status": (
                entry.queue_review_status.value
                if entry.queue_review_status is not None
                else None
            ),
            "resolution": (
                entry.resolution.value if entry.resolution is not None else None
            ),
            "current_status": entry.current_status.value,
            "effective_status": entry.effective_status.value,
            "reason": entry.reason,
            "note": entry.note,
            "created_at": entry.created_at.isoformat(),
        }

    @staticmethod
    def _allocate_scope_budgets(
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        total_limit: int,
    ) -> dict[str, int]:
        if not scope_filters:
            return {}
        base = total_limit // len(scope_filters)
        remainder = total_limit % len(scope_filters)
        budgets: dict[str, int] = {}
        for index, (scope, scope_key) in enumerate(scope_filters):
            budgets[f"{scope.value}:{scope_key}"] = base + (1 if index < remainder else 0)
        return budgets

    def _rank_records(
        self,
        plan: RecallPlan,
        records: tuple[MemoryRecord, ...],
    ) -> tuple[MemoryRecord, ...]:
        grouped: dict[tuple[MemoryScope, str], list[MemoryRecord]] = {
            scope_filter: [] for scope_filter in plan.scope_filters
        }
        for record in records:
            scope_filter = (record.scope, record.scope_key)
            if scope_filter in grouped:
                grouped[scope_filter].append(record)
        for bucket in grouped.values():
            self._sort_bucket(bucket, plan.within_scope_order)
        selected: list[MemoryRecord] = []
        leftovers: list[tuple[int, MemoryRecord]] = []
        for index, scope_filter in enumerate(plan.scope_filters):
            scope, scope_key = scope_filter
            bucket = grouped.get(scope_filter, [])
            budget = max(0, plan.budget_for(scope, scope_key))
            selected.extend(bucket[:budget])
            leftovers.extend((index, record) for record in bucket[budget:])
        if len(selected) < plan.total_limit and plan.overflow_fill_enabled:
            self._sort_overflow(leftovers, plan.overflow_order)
            selected.extend(
                record for _, record in leftovers[: max(0, plan.total_limit - len(selected))]
            )
        return tuple(selected[: plan.total_limit])

    def _select_recall_records(
        self,
        plan: RecallPlan,
        scanned_records: tuple[MemoryRecord, ...],
        augmentation: MemoryProviderAugmentation | None,
    ) -> tuple[MemoryRecord, ...]:
        if self.recall_ranker is not None:
            return self.recall_ranker.rank(
                plan=plan,
                records=scanned_records,
                augmentation=augmentation,
            )
        return self._rank_records(plan, scanned_records)

    def _build_recall_bundle(
        self,
        plan: RecallPlan,
        scanned_records: tuple[MemoryRecord, ...],
        retrieved_records: tuple[MemoryRecord, ...],
        augmentation: MemoryProviderAugmentation | None,
    ) -> RecallBundle:
        pinned_records = tuple(
            record
            for record in retrieved_records
            if record.scope is MemoryScope.PROJECT and record.status is MemoryStatus.ACCEPTED
        )
        evidence_refs = tuple(ref for record in retrieved_records for ref in record.supporting_refs)
        diagnostics: dict[str, Any] = {
            "retrieved_count": len(retrieved_records),
            "scanned_count": len(scanned_records),
            "pinned_count": len(pinned_records),
            "allowed_statuses": tuple(status.value for status in plan.allowed_statuses),
            "scope_filters": tuple(
                (scope.value, scope_key) for scope, scope_key in plan.scope_filters
            ),
            "limit": plan.total_limit,
            "recall_plan": plan.to_mapping(),
            "external_augmentation_present": augmentation is not None,
        }
        if self.semantic_search is not None:
            diagnostics["semantic_search_available"] = True
        return RecallBundle(
            pinned_records=pinned_records,
            retrieved_records=retrieved_records,
            evidence_refs=evidence_refs,
            diagnostics=diagnostics,
        )

    def _build_preview_ranking(
        self,
        plan: RecallPlan,
        scanned_records: tuple[MemoryRecord, ...],
        retrieved_records: tuple[MemoryRecord, ...],
    ) -> tuple[tuple[RecallScopeBreakdown, ...], tuple[RecallRecordRanking, ...]]:
        grouped: dict[tuple[MemoryScope, str], list[MemoryRecord]] = {
            scope_filter: [] for scope_filter in plan.scope_filters
        }
        for record in scanned_records:
            scope_filter = (record.scope, record.scope_key)
            if scope_filter in grouped:
                grouped[scope_filter].append(record)
        for bucket in grouped.values():
            self._sort_bucket(bucket, plan.within_scope_order)

        selected_order = {record.id: index for index, record in enumerate(retrieved_records)}
        scope_breakdowns: list[RecallScopeBreakdown] = []
        candidate_rankings: list[tuple[int, MemoryRecord, str]] = []
        overflow_candidates: list[tuple[int, MemoryRecord]] = []

        for scope_index, scope_filter in enumerate(plan.scope_filters):
            scope, scope_key = scope_filter
            bucket = grouped.get(scope_filter, [])
            budget = max(0, int(plan.budget_for(scope, scope_key)))
            within_budget = bucket[:budget]
            overflow = bucket[budget:]
            scope_breakdowns.append(
                RecallScopeBreakdown(
                    scope=scope.value,
                    scope_key=scope_key,
                    budget=budget,
                    scanned_record_ids=tuple(record.id for record in bucket),
                    selected_record_ids=tuple(
                        record.id for record in bucket if record.id in selected_order
                    ),
                    overflow_record_ids=tuple(record.id for record in overflow),
                )
            )
            candidate_rankings.extend(
                (scope_index, record, "scope_budget") for record in within_budget
            )
            overflow_candidates.extend((scope_index, record) for record in overflow)

        self._sort_overflow(overflow_candidates, plan.overflow_order)
        candidate_rankings.extend(
            (scope_index, record, "overflow_candidate")
            for scope_index, record in overflow_candidates
        )

        record_rankings: list[RecallRecordRanking] = []
        for rank_position, (_, record, reason) in enumerate(candidate_rankings):
            is_selected = record.id in selected_order
            selection_reason = reason
            if reason == "overflow_candidate" and is_selected:
                selection_reason = "overflow_fill"
            record_rankings.append(
                RecallRecordRanking(
                    record_id=record.id,
                    scope=record.scope.value,
                    scope_key=record.scope_key,
                    confidence=record.confidence,
                    rank_position=rank_position,
                    selected=is_selected,
                    selection_reason=selection_reason,
                    selected_order=selected_order.get(record.id),
                )
            )

        return tuple(scope_breakdowns), tuple(record_rankings)

    @classmethod
    def _sort_bucket(
        cls,
        bucket: list[MemoryRecord],
        order: tuple[str, ...],
    ) -> None:
        for token in reversed(order):
            field_name, reverse = cls._parse_sort_token(token)
            bucket.sort(
                key=lambda record: cls._record_field_value(record, field_name, 0),
                reverse=reverse,
            )

    @classmethod
    def _sort_overflow(
        cls,
        leftovers: list[tuple[int, MemoryRecord]],
        order: tuple[str, ...],
    ) -> None:
        for token in reversed(order):
            field_name, reverse = cls._parse_sort_token(token)
            leftovers.sort(
                key=lambda item: cls._record_field_value(item[1], field_name, item[0]),
                reverse=reverse,
            )

    @staticmethod
    def _parse_sort_token(token: str) -> tuple[str, bool]:
        field_name, _, direction = str(token).partition(":")
        normalized_field = field_name.strip() or "id"
        normalized_direction = direction.strip().lower() or "asc"
        return normalized_field, normalized_direction == "desc"

    @staticmethod
    def _record_field_value(
        record: MemoryRecord,
        field_name: str,
        scope_order: int,
    ) -> object:
        if field_name == "scope_order":
            return scope_order
        if field_name == "confidence":
            return record.confidence
        if field_name == "created_at":
            return record.created_at
        if field_name == "title":
            return record.title
        return record.id

    def _build_augmentation_preview(
        self,
        memory_provider_binding: MemoryProviderBinding | None,
        augmentation: MemoryProviderAugmentation | None,
        external_recall_block: str | None,
    ) -> RecallAugmentationPreview | None:
        if memory_provider_binding is None:
            return None
        diagnostics = (
            project_preview_augmentation_diagnostics(augmentation.diagnostics)
            if augmentation is not None
            else {}
        )
        recall_block_source = str(diagnostics.get("source") or "") or None
        if recall_block_source is None and external_recall_block is not None:
            recall_block_source = "session_context"
        return RecallAugmentationPreview(
            provider_id=memory_provider_binding.provider_id,
            source=memory_provider_binding.source,
            namespace=memory_provider_binding.namespace,
            mode=memory_provider_binding.mode,
            writable=memory_provider_binding.writable,
            recall_block_source=recall_block_source,
            recall_block_present=external_recall_block is not None,
            diagnostics=diagnostics,
        )

    def _build_session_assembly_manifest(
        self,
        session: AgentSession,
        profile: Mapping[str, Any],
        rules: Mapping[str, Any],
        skills: tuple[Mapping[str, Any], ...],
        bundle: RecallBundle,
        child_digests: tuple[SubAgentDigest, ...],
        memory_provider_binding: MemoryProviderBinding | None,
        project_scope_key: str | None,
    ) -> SessionAssemblyManifest:
        profile_id = str(profile.get("profile_id") or "") or None
        workspace_root = str(session.context.get("workspace_root") or "") or None
        rule_bundle = ProjectRuleBundle(
            source=str(rules.get("source") or "workspace-rules"),
            project_scope_key=project_scope_key,
            summary=str(rules.get("summary") or rules.get("rule_summary") or "") or None,
            metadata={
                key: value
                for key, value in rules.items()
                if key not in {"source", "summary", "rule_summary", "project_scope_key"}
            },
        )
        active_skills = tuple(
            SkillActivation(
                skill_id=str(
                    skill.get("skill_id") or skill.get("id") or skill.get("name") or ""
                ),
                name=str(skill.get("name") or skill.get("skill_id") or skill.get("id") or ""),
                scope=str(skill.get("scope") or "project") or None,
                reason=str(skill.get("reason") or "prepare_session") or None,
                metadata={
                    key: value
                    for key, value in skill.items()
                    if key not in {"skill_id", "id", "name", "scope", "reason"}
                },
            )
            for skill in skills
        )
        child_session_ids = self._merge_child_session_ids(
            explicit_ids=tuple(str(item) for item in session.context.get("child_session_ids", ())),
            child_digests=child_digests,
        )
        sources: list[str] = []
        if profile_id is not None:
            sources.append("profile")
        if workspace_root is not None:
            sources.append("workspace")
        if rules:
            sources.append("rules")
        if active_skills:
            sources.append("skills")
        if bundle.retrieved_records:
            sources.append("memory")
        if child_digests or child_session_ids:
            sources.append("delegation")
        if memory_provider_binding is not None:
            sources.append("external_memory_provider")
        if session.context.get("parent_session_id"):
            sources.append("parent_session")
        backend_bindings = self._build_backend_bindings(session=session, profile=profile)
        selected_model = self._build_selected_model(session=session, profile=profile)
        if backend_bindings:
            sources.append("bindings")
        if selected_model is not None:
            sources.append("model")

        return SessionAssemblyManifest(
            session_id=session.id,
            profile_id=profile_id,
            workspace_root=workspace_root,
            rule_bundle=rule_bundle,
            active_skills=active_skills,
            recall_scope_filters=tuple(
                (str(scope), str(scope_key))
                for scope, scope_key in bundle.diagnostics.get("scope_filters", ())
            ),
            recalled_memory_ids=tuple(record.id for record in bundle.retrieved_records),
            child_session_ids=child_session_ids,
            child_digests=tuple(child_digests),
            memory_provider_binding=memory_provider_binding,
            selected_model=selected_model,
            model_bindings=(),
            backend_bindings=backend_bindings,
            provider_bindings=self._build_provider_bindings(
                session=session,
                profile=profile,
                backend_bindings=backend_bindings,
                memory_provider_binding=memory_provider_binding,
            ),
            sources=tuple(sources),
            metadata={
                "project_scope_key": project_scope_key,
                "diagnostics": dict(bundle.diagnostics),
            },
        )

    def _merge_child_session_ids(
        self,
        explicit_ids: tuple[str, ...],
        child_digests: tuple[SubAgentDigest, ...],
    ) -> tuple[str, ...]:
        merged: list[str] = []
        seen: set[str] = set()
        for child_session_id in explicit_ids:
            if child_session_id and child_session_id not in seen:
                merged.append(child_session_id)
                seen.add(child_session_id)
        for digest in child_digests:
            if digest.child_session_id and digest.child_session_id not in seen:
                merged.append(digest.child_session_id)
                seen.add(digest.child_session_id)
        return tuple(merged)

    def _build_backend_bindings(
        self,
        session: AgentSession,
        profile: Mapping[str, Any],
    ) -> tuple[BackendBinding, ...]:
        backend_metadata_payload = (
            session.context.get("backend_binding_metadata")
            if isinstance(session.context.get("backend_binding_metadata"), Mapping)
            else {}
        )
        source = (
            "session_context"
            if isinstance(session.context.get("backend_ids"), dict)
            else "profile"
        )
        payload = (
            session.context.get("backend_ids")
            if isinstance(session.context.get("backend_ids"), dict)
            else profile.get("backend_ids")
        )
        if not isinstance(payload, Mapping):
            return ()
        bindings: list[BackendBinding] = []
        for family, binding_id in sorted(payload.items()):
            family_text = str(family).strip()
            binding_text = str(binding_id).strip()
            if not family_text or not binding_text:
                continue
            metadata = (
                dict(backend_metadata_payload.get(family_text) or {})
                if isinstance(backend_metadata_payload.get(family_text), Mapping)
                else {}
            )
            bindings.append(
                BackendBinding(
                    family=family_text,
                    binding_id=binding_text,
                    source=source,
                    metadata=metadata,
                )
            )
        return tuple(bindings)

    def _build_selected_model(
        self,
        session: AgentSession,
        profile: Mapping[str, Any],
    ) -> ModelBinding | None:
        session_binding = session.context.get("selected_model_binding")
        backend_ids = (
            session.context.get("backend_ids")
            if isinstance(session.context.get("backend_ids"), dict)
            else profile.get("backend_ids")
        )
        provider_id = None
        if isinstance(session_binding, Mapping):
            provider_id = session_binding.get("provider_id") or session_binding.get("provider")
        if provider_id is None and isinstance(backend_ids, Mapping):
            provider_id = backend_ids.get("llm_provider")
        if provider_id is None:
            provider_id = profile.get("provider_id")

        model_id = None
        if isinstance(session_binding, Mapping):
            model_id = session_binding.get("model_id") or session_binding.get("model")
        if model_id is None:
            model_id = profile.get("default_model")

        provider_text = str(provider_id).strip() if provider_id is not None else ""
        model_text = str(model_id).strip() if model_id is not None else ""
        if not provider_text and not model_text:
            return None
        metadata = (
            dict(session_binding.get("metadata") or {})
            if isinstance(session_binding, Mapping)
            else {}
        )
        source = None
        if isinstance(session_binding, Mapping):
            source = str(session_binding.get("source") or "") or None
        return ModelBinding(
            provider_id=provider_text or None,
            model_id=model_text or None,
            source=source or "assembly-default",
            step_id=(
                str(session_binding.get("step_id") or "") or None
                if isinstance(session_binding, Mapping)
                else None
            ),
            metadata=metadata,
        )

    def _refresh_session_assembly_manifest(self, session: AgentSession) -> None:
        manifest_payload = session.context.get("assembly_manifest")
        if not isinstance(manifest_payload, Mapping):
            return
        manifest = SessionAssemblyManifest.from_mapping(manifest_payload)
        model_binding_payload = session.context.get("model_bindings")
        if isinstance(model_binding_payload, (list, tuple)):
            model_bindings = tuple(
                ModelBinding.from_mapping(item)
                for item in model_binding_payload
                if isinstance(item, Mapping)
            )
        else:
            model_bindings = ()
        provider_diagnostics = (
            compact_augmentation_diagnostics(session.context.get("memory_provider_diagnostics"))
            if isinstance(session.context.get("memory_provider_diagnostics"), Mapping)
            else {}
        )
        if not model_bindings and not provider_diagnostics:
            return

        sources = list(manifest.sources)
        if model_bindings and "model" not in sources:
            sources.append("model")
        metadata = dict(manifest.metadata)
        if model_bindings:
            metadata["model_binding_count"] = len(model_bindings)
        diagnostics = (
            dict(metadata.get("diagnostics"))
            if isinstance(metadata.get("diagnostics"), Mapping)
            else {}
        )
        diagnostics.update(provider_diagnostics)
        diagnostics = compact_augmentation_diagnostics(diagnostics)
        metadata["diagnostics"] = diagnostics
        refreshed = SessionAssemblyManifest(
            session_id=manifest.session_id,
            profile_id=manifest.profile_id,
            workspace_root=manifest.workspace_root,
            rule_bundle=manifest.rule_bundle,
            active_skills=manifest.active_skills,
            recall_scope_filters=manifest.recall_scope_filters,
            recalled_memory_ids=manifest.recalled_memory_ids,
            child_session_ids=manifest.child_session_ids,
            child_digests=manifest.child_digests,
            memory_provider_binding=manifest.memory_provider_binding,
            selected_model=(
                manifest.selected_model or model_bindings[-1]
                if model_bindings
                else manifest.selected_model
            ),
            model_bindings=model_bindings,
            backend_bindings=manifest.backend_bindings,
            provider_bindings=manifest.provider_bindings,
            sources=tuple(sources),
            metadata=metadata,
        )
        session.context["assembly_manifest"] = refreshed.to_mapping()
        if self.assembly_store is not None:
            self.assembly_store.save(refreshed)

    def _resolve_memory_provider_diagnostics(
        self,
        provider_decision: MemoryProviderGovernanceDecision | None,
        session_id: str,
    ) -> dict[str, Any]:
        if self.memory_provider_manager is None or provider_decision is None:
            return {}
        provider_diagnostics = getattr(self.memory_provider_manager, "provider_diagnostics", None)
        if not callable(provider_diagnostics):
            return {}
        payload = provider_diagnostics(provider_decision, session_id)
        if not isinstance(payload, Mapping):
            return {}
        return compact_augmentation_diagnostics(payload)

    def _build_provider_bindings(
        self,
        session: AgentSession,
        profile: Mapping[str, Any],
        backend_bindings: tuple[BackendBinding, ...],
        memory_provider_binding: MemoryProviderBinding | None,
    ) -> tuple[str, ...]:
        payload = (
            session.context.get("provider_bindings")
            or profile.get("provider_bindings")
            or tuple(f"{binding.family}:{binding.binding_id}" for binding in backend_bindings)
        )
        bindings: list[str] = [str(item) for item in payload if str(item).strip()]
        if memory_provider_binding is not None:
            provider_binding_id = f"memory_provider:{memory_provider_binding.provider_id}"
            if provider_binding_id not in bindings:
                bindings.append(provider_binding_id)
        return tuple(bindings)

    def _resolve_memory_provider_binding(
        self,
        session: AgentSession,
        profile: Mapping[str, Any],
    ) -> MemoryProviderBinding | None:
        session_payload = session.context.get("memory_provider_binding")
        if isinstance(session_payload, Mapping):
            binding = MemoryProviderBinding.from_mapping(session_payload)
            if binding.provider_id and binding.provider_id != "none":
                return binding
            return None
        backend_ids = (
            session.context.get("backend_ids")
            if isinstance(session.context.get("backend_ids"), Mapping)
            else profile.get("backend_ids")
        )
        if not isinstance(backend_ids, Mapping):
            return None
        provider_id = str(backend_ids.get("memory_provider") or "").strip()
        if not provider_id or provider_id == "none":
            return None
        backend_metadata_payload = (
            session.context.get("backend_binding_metadata")
            if isinstance(session.context.get("backend_binding_metadata"), Mapping)
            else {}
        )
        metadata = (
            dict(backend_metadata_payload.get("memory_provider") or {})
            if isinstance(backend_metadata_payload.get("memory_provider"), Mapping)
            else {}
        )
        return MemoryProviderBinding(
            provider_id=provider_id,
            source=str(metadata.get("binding_source") or "session_context"),
            namespace=str(
                metadata.get("namespace")
                or session.context.get("profile_id")
                or profile.get("profile_id")
                or ""
            )
            or None,
            mode=str(metadata.get("mode") or "augmentation"),
            writable=bool(metadata.get("writable", False)),
            metadata=metadata,
        )

    def _project_evidence(self, session: AgentSession) -> tuple[EvidenceRecord, ...]:
        records: list[EvidenceRecord] = []
        for event in session.events:
            record = EvidenceRecord(
                id=self._stable_id("evidence", session.id, "event", event.id),
                session_id=session.id,
                source_kind="event",
                source_id=event.id,
                source_ref=f"event://{event.id}",
                summary=event.summary,
                payload={"type": event.type, "payload": event.payload},
            )
            self.evidence_records.save_evidence(record)
            records.append(record)
        for artifact in session.artifacts:
            record = EvidenceRecord(
                id=self._stable_id("evidence", session.id, "artifact", artifact.id),
                session_id=session.id,
                source_kind="artifact",
                source_id=artifact.id,
                source_ref=f"artifact://{artifact.id}",
                summary=artifact.summary,
                payload={"kind": artifact.kind, "uri": artifact.uri},
            )
            self.evidence_records.save_evidence(record)
            records.append(record)
        return tuple(records)

    def _extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> tuple[MemoryCandidate, ...]:
        if session.status != "completed":
            return ()

        completed_steps = tuple(
            event.payload["step_id"]
            for event in session.events
            if event.type == "step_completed" and "step_id" in event.payload
        )
        artifact_count = len(session.artifacts)
        body = (
            f"Session '{session.id}' completed workflow '{session.workflow_id}' for app "
            f"'{session.app_id}' after {len(completed_steps)} step(s)."
        )
        if artifact_count:
            body = f"{body} Captured {artifact_count} artifact(s) during execution."
        if session.user_input:
            body = f"{body} User goal: {session.user_input}"

        candidate = MemoryCandidate(
            id=self._stable_id("candidate", session.id, "episodic", session.workflow_id),
            kind=MemoryKind.EPISODIC,
            scope=MemoryScope.APP,
            scope_key=session.app_id,
            title=f"Workflow '{session.workflow_id}' completion",
            body=body,
            source_event_ids=tuple(event.id for event in session.events),
            evidence_ids=tuple(record.id for record in evidence_records),
            confidence=0.75,
            metadata={"workflow_id": session.workflow_id, "app_id": session.app_id},
        )
        return (candidate,)

    def _promote_candidate(
        self,
        candidate: MemoryCandidate,
    ) -> tuple[PromotionDecision, MemoryRecord | None]:
        supporting_refs = (
            tuple(f"event://{event_id}" for event_id in candidate.source_event_ids)
            + tuple(f"evidence://{evidence_id}" for evidence_id in candidate.evidence_ids)
        )
        if not supporting_refs:
            return (
                PromotionDecision(
                    candidate_id=candidate.id,
                    status=MemoryStatus.REJECTED,
                    reason="Candidate is missing supporting source references.",
                ),
                None,
            )

        status, reason = self.promotion_policy.evaluate(candidate)
        decision = PromotionDecision(
            candidate_id=candidate.id,
            status=status,
            reason=reason,
            supporting_refs=supporting_refs,
        )
        if status is MemoryStatus.REJECTED:
            return decision, None

        record = MemoryRecord(
            id=self._stable_id("memory", candidate.id),
            kind=candidate.kind,
            scope=candidate.scope,
            scope_key=candidate.scope_key,
            title=candidate.title,
            body=candidate.body,
            status=status,
            confidence=candidate.confidence,
            supporting_refs=supporting_refs,
            metadata={
                **candidate.metadata,
                "source_event_ids": candidate.source_event_ids,
                "evidence_ids": candidate.evidence_ids,
            },
        )
        self.memory_records.save_memory_record(record)
        return decision, record

    @staticmethod
    def _build_distillation_sample(
        session: AgentSession,
        candidate: MemoryCandidate,
        decision: PromotionDecision,
        record: MemoryRecord | None,
    ) -> MemoryDistillationSample:
        return MemoryDistillationSample(
            id=DefaultMemoryDomainService._stable_id("sample", session.id, candidate.id),
            session_id=session.id,
            candidate_id=candidate.id,
            candidate_kind=candidate.kind,
            candidate_scope=candidate.scope,
            candidate_scope_key=candidate.scope_key,
            decision_status=decision.status,
            decision_reason=decision.reason,
            supporting_refs=decision.supporting_refs,
            promoted_record_id=record.id if record is not None else None,
            metadata={
                **candidate.metadata,
                "workflow_id": session.workflow_id,
                "app_id": session.app_id,
            },
        )

    def _normalize_generated_candidates(
        self,
        session: AgentSession,
        candidates: tuple[MemoryCandidate, ...],
    ) -> tuple[MemoryCandidate, ...]:
        normalized: list[MemoryCandidate] = []
        for candidate in candidates:
            normalized.append(
                MemoryCandidate(
                    id=self._stable_id(
                        "candidate",
                        session.id,
                        "generated",
                        candidate.kind.value,
                        candidate.scope.value,
                        candidate.scope_key,
                        candidate.title,
                        candidate.body,
                    ),
                    kind=candidate.kind,
                    scope=candidate.scope,
                    scope_key=candidate.scope_key,
                    title=candidate.title,
                    body=candidate.body,
                    source_event_ids=candidate.source_event_ids,
                    evidence_ids=candidate.evidence_ids,
                    confidence=candidate.confidence,
                    metadata=candidate.metadata,
                    created_at=candidate.created_at,
                )
            )
        return tuple(normalized)

    @staticmethod
    def _dedupe_candidates(
        candidates: tuple[MemoryCandidate, ...],
    ) -> tuple[MemoryCandidate, ...]:
        deduped: dict[str, MemoryCandidate] = {}
        for candidate in candidates:
            deduped[candidate.id] = candidate
        return tuple(deduped.values())

    @staticmethod
    def _stable_id(*parts: str) -> str:
        digest = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:16]
        return digest
