from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any, Mapping

from domain.agent_app.models import AgentApp
from domain.memory.models import (
    CandidateDrafts,
    DistillationResult,
    EvidenceRecord,
    MemoryCandidate,
    MemoryDistillationSample,
    MemoryKind,
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
    MemoryProfileResolverPort,
    MemoryReasoningPort,
    MemoryRecordRepositoryPort,
    MemoryRuleBundlePort,
    MemorySemanticSearchPort,
    MemorySkillCatalogPort,
)
from domain.session.models import AgentSession
from domain.workflow.models import WorkflowDefinition


@dataclass(slots=True)
class DefaultMemoryDomainService:
    """Business-domain logic for recall, distillation, and explainability."""

    memory_records: MemoryRecordRepositoryPort
    evidence_records: EvidenceRepositoryPort
    dataset_records: MemoryDatasetRepositoryPort
    archive_query: MemoryArchiveQueryPort | None = None
    profile_resolver: MemoryProfileResolverPort | None = None
    rule_bundle: MemoryRuleBundlePort | None = None
    skill_catalog: MemorySkillCatalogPort | None = None
    reasoning: MemoryReasoningPort | None = None
    semantic_search: MemorySemanticSearchPort | None = None
    default_project_scope_key: str | None = None
    promotion_policy: MemoryPromotionPolicy = field(default_factory=MemoryPromotionPolicy)

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
        profile_id = str(profile.get("profile_id")) if profile.get("profile_id") is not None else None
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
        scope_filters: list[tuple[MemoryScope, str]] = [(MemoryScope.APP, app.metadata.id)]
        if project_scope_key:
            scope_filters.append((MemoryScope.PROJECT, project_scope_key))

        bundle = self.recall(
            RecallQuery(
                session_id=session.id,
                app_id=app.metadata.id,
                workflow_id=workflow.id,
                scope_filters=tuple(scope_filters),
            )
        )
        session.recalled_memories = list(bundle.retrieved_records)
        bundle.diagnostics.update(
            {
                "profile_id": profile_id,
                "project_scope_key": project_scope_key,
                "skill_count": len(skills),
            }
        )
        return bundle

    def recall(self, query: RecallQuery) -> RecallBundle:
        retrieved_records = self.memory_records.query_memory_records(query)
        pinned_records = tuple(
            record
            for record in retrieved_records
            if record.scope is MemoryScope.PROJECT and record.status is MemoryStatus.ACCEPTED
        )
        evidence_refs = tuple(ref for record in retrieved_records for ref in record.supporting_refs)
        diagnostics: dict[str, Any] = {
            "retrieved_count": len(retrieved_records),
            "pinned_count": len(pinned_records),
            "allowed_statuses": tuple(status.value for status in query.allowed_statuses),
            "scope_filters": tuple((scope.value, scope_key) for scope, scope_key in query.scope_filters),
            "limit": query.limit,
        }
        if self.semantic_search is not None:
            diagnostics["semantic_search_available"] = True
        return RecallBundle(
            pinned_records=pinned_records,
            retrieved_records=retrieved_records,
            evidence_refs=evidence_refs,
            diagnostics=diagnostics,
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
        session.memory_candidates = list(candidates)
        session.promotion_decisions = promotion_decisions
        session.context["memory_summary"] = summary.episode_summary
        return DistillationResult(
            evidence_records=evidence_records,
            candidates=candidates,
            promotion_decisions=tuple(promotion_decisions),
            promoted_records=tuple(
                record for record in promoted_records if record.status is MemoryStatus.ACCEPTED
            ),
        )

    def explain_session_memory(self, session: AgentSession) -> Mapping[str, Any]:
        return {
            "session_id": session.id,
            "app_id": session.app_id,
            "workflow_id": session.workflow_id,
            "recalled_memory_ids": tuple(record.id for record in session.recalled_memories),
            "candidate_ids": tuple(candidate.id for candidate in session.memory_candidates),
            "candidate_count": len(session.memory_candidates),
            "promotion_statuses": tuple(
                decision.status.value for decision in session.promotion_decisions
            ),
            "recalled_count": len(session.recalled_memories),
        }

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
