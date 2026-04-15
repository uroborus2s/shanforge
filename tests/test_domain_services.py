from __future__ import annotations

import unittest
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone

from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentAppMetadata
from domain.memory.models import (
    CandidateDrafts,
    EvidenceRecord,
    MemoryCandidate,
    MemoryDistillationSample,
    MemoryKind,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
    SummaryResult,
)
from domain.session.models import AgentSession, SessionArtifact, SessionEvent
from domain.workflow.models import WorkflowDefinition
from domain.workflow.steps import StepKind, WorkflowStep


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


def _build_manifest() -> AgentAppManifest:
    workflow = _build_workflow()
    return AgentAppManifest(
        metadata=AgentAppMetadata(
            id="demo.writer",
            name="Writer",
            domain="demo",
        ),
        workflows=(workflow,),
        default_workflow_id=workflow.id,
        required_capabilities=("context.inspect",),
    )


@dataclass(slots=True)
class _MemoryRepository:
    records: list[MemoryRecord] = field(default_factory=list)
    last_query: object | None = None

    def save_memory_record(self, record: MemoryRecord) -> None:
        for index, existing in enumerate(self.records):
            if existing.id == record.id:
                self.records[index] = record
                break
        else:
            self.records.append(record)

    def query_memory_records(self, query: object) -> tuple[MemoryRecord, ...]:
        self.last_query = query
        scope_filters = set(query.scope_filters)
        allowed_statuses = set(query.allowed_statuses)
        records = [
            record
            for record in self.records
            if (record.scope, record.scope_key) in scope_filters
            and record.status in allowed_statuses
        ]
        records.sort(key=lambda item: (item.scope.value, -item.confidence, item.created_at))
        return tuple(records[: query.limit])


@dataclass(slots=True)
class _EvidenceRepository:
    records: list[EvidenceRecord] = field(default_factory=list)

    def save_evidence(self, record: EvidenceRecord) -> None:
        for index, existing in enumerate(self.records):
            if existing.id == record.id:
                self.records[index] = record
                break
        else:
            self.records.append(record)

    def list_evidence(self, session_id: str) -> tuple[EvidenceRecord, ...]:
        return tuple(record for record in self.records if record.session_id == session_id)


@dataclass(slots=True)
class _DatasetRepository:
    samples: list[MemoryDistillationSample] = field(default_factory=list)

    def save_sample(self, sample: MemoryDistillationSample) -> None:
        for index, existing in enumerate(self.samples):
            if existing.id == sample.id:
                self.samples[index] = sample
                break
        else:
            self.samples.append(sample)

    def list_samples(self, session_id: str) -> tuple[MemoryDistillationSample, ...]:
        return tuple(sample for sample in self.samples if sample.session_id == session_id)


@dataclass(slots=True, frozen=True)
class _ProfileResolver:
    payload: dict[str, object]

    def resolve_profile(self, session: AgentSession, app_id: str, workflow_id: str) -> dict[str, object]:
        return dict(self.payload)


@dataclass(slots=True, frozen=True)
class _RuleBundle:
    payload: dict[str, object]

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> dict[str, object]:
        return dict(self.payload)


@dataclass(slots=True, frozen=True)
class _SkillCatalog:
    skills: tuple[dict[str, object], ...]

    def list_skill_index(self, app_id: str, workflow_id: str) -> tuple[dict[str, object], ...]:
        return self.skills


class _ReasoningPort:
    def summarize_evidence(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> SummaryResult:
        return SummaryResult(
            episode_summary=f"Summarized {len(evidence_records)} evidence record(s).",
            metadata={"session_id": session.id},
        )

    def extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
        summary: SummaryResult,
    ) -> CandidateDrafts:
        return CandidateDrafts(
            candidates=(
                MemoryCandidate(
                    id="generated-procedure",
                    kind=MemoryKind.PROCEDURAL,
                    scope=MemoryScope.APP,
                    scope_key=session.app_id,
                    title="Reusable Procedure",
                    body=summary.episode_summary or "Fallback summary",
                    source_event_ids=tuple(event.id for event in session.events),
                    evidence_ids=tuple(record.id for record in evidence_records),
                    confidence=0.61,
                ),
            )
        )


@dataclass(slots=True)
class _SessionLedger:
    saved_sessions: list[AgentSession] = field(default_factory=list)
    events_by_session: dict[str, list[SessionEvent]] = field(default_factory=dict)

    def save_session(self, session: AgentSession) -> None:
        self.saved_sessions.append(deepcopy(session))

    def load_session(self, session_id: str) -> AgentSession | None:
        for session in reversed(self.saved_sessions):
            if session.id == session_id:
                return deepcopy(session)
        return None

    def append_event(self, session_id: str, event: SessionEvent) -> None:
        self.events_by_session.setdefault(session_id, []).append(event)

    def list_events(self, session_id: str) -> tuple[SessionEvent, ...]:
        return tuple(self.events_by_session.get(session_id, ()))


@dataclass(slots=True)
class _SessionArtifactStore:
    artifacts: list[SessionArtifact] = field(default_factory=list)

    def save_artifact(self, session_id: str, artifact: SessionArtifact) -> None:
        self.artifacts.append(artifact)

    def load_artifact(self, artifact_id: str) -> SessionArtifact | None:
        for artifact in self.artifacts:
            if artifact.id == artifact_id:
                return artifact
        return None

    def list_artifacts(self, session_id: str) -> tuple[SessionArtifact, ...]:
        return tuple(self.artifacts)


class _Clock:
    def now(self) -> datetime:
        return datetime(2026, 4, 15, 12, 0, tzinfo=timezone.utc)


class _Identity:
    def __init__(self) -> None:
        self.generated: list[str] = []

    def new_id(self, prefix: str) -> str:
        new_value = f"{prefix}-001"
        self.generated.append(new_value)
        return new_value


class DomainServiceTests(unittest.TestCase):
    def test_agent_app_domain_service_builds_app_and_lists_capabilities(self) -> None:
        from domain.agent_app.service import DefaultAgentAppDomainService

        manifest = _build_manifest()
        service = DefaultAgentAppDomainService()

        app = service.build_from_manifest(manifest)

        self.assertEqual(app.metadata.id, "demo.writer")
        self.assertEqual(service.list_required_capabilities(app), ("context.inspect",))

    def test_workflow_domain_service_resolves_workflow_and_opens_state(self) -> None:
        from domain.workflow.service import DefaultWorkflowDomainService

        app = _build_manifest().to_agent_app()
        service = DefaultWorkflowDomainService()

        workflow = service.resolve_workflow(app, workflow_id="compose")
        state = service.open_run_state(workflow)

        self.assertEqual(workflow.id, "compose")
        self.assertEqual(state.workflow_id, "compose")
        self.assertEqual(state.step_records, [])

    def test_session_domain_service_tracks_lifecycle_and_artifacts(self) -> None:
        from domain.session.service import DefaultSessionDomainService

        ledger = _SessionLedger()
        artifacts = _SessionArtifactStore()
        service = DefaultSessionDomainService(
            ledger=ledger,
            artifact_store=artifacts,
            clock=_Clock(),
            identity=_Identity(),
        )

        session = service.open_session(
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Write a draft.",
        )
        session = service.attach_artifacts(
            session,
            (
                SessionArtifact(
                    kind="capability",
                    uri="capability://context.inspect",
                    summary="Captured runtime context.",
                ),
            ),
        )
        completed = service.complete_session(session)

        failed = service.open_session(
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Fail this run.",
            session_id="session-explicit",
        )
        failed = service.fail_session(failed, reason="capability timeout")

        self.assertEqual(session.id, "session-001")
        self.assertEqual(completed.status, "completed")
        self.assertEqual(failed.status, "failed")
        self.assertEqual(len(artifacts.artifacts), 1)
        self.assertGreaterEqual(len(ledger.saved_sessions), 4)
        self.assertEqual(ledger.list_events("session-001")[0].type, "session_opened")
        self.assertEqual(ledger.list_events("session-001")[-1].type, "session_completed")
        self.assertEqual(ledger.list_events("session-explicit")[-1].type, "session_failed")

    def test_memory_domain_service_prepares_session_from_domain_ports(self) -> None:
        from domain.memory.service import DefaultMemoryDomainService

        manifest = _build_manifest()
        app = manifest.to_agent_app()
        workflow = app.resolve_workflow()
        repository = _MemoryRepository(
            records=[
                MemoryRecord(
                    id="memory-app",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Accepted App Memory",
                    body="Remember this app-specific fact.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.9,
                    supporting_refs=("event://1",),
                ),
                MemoryRecord(
                    id="memory-project",
                    kind=MemoryKind.DECLARATIVE,
                    scope=MemoryScope.PROJECT,
                    scope_key="shanforge",
                    title="Project Convention",
                    body="Follow the architecture contract.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.8,
                    supporting_refs=("event://2",),
                ),
                MemoryRecord(
                    id="memory-draft",
                    kind=MemoryKind.PROCEDURAL,
                    scope=MemoryScope.APP,
                    scope_key=app.metadata.id,
                    title="Draft Procedure",
                    body="Should not be recalled by default.",
                    status=MemoryStatus.DRAFT,
                    confidence=0.7,
                    supporting_refs=("event://3",),
                ),
            ]
        )
        service = DefaultMemoryDomainService(
            memory_records=repository,
            evidence_records=_EvidenceRepository(),
            dataset_records=_DatasetRepository(),
            profile_resolver=_ProfileResolver({"profile_id": "writer-profile"}),
            rule_bundle=_RuleBundle({"project_scope_key": "shanforge"}),
            skill_catalog=_SkillCatalog(({"id": "python-uv-project"},)),
            default_project_scope_key="fallback-project",
        )
        session = AgentSession(
            id="session-prepare",
            app_id=app.metadata.id,
            workflow_id=workflow.id,
            user_input="Continue the document.",
        )

        bundle = service.prepare_session(session=session, app=app, workflow=workflow)

        self.assertEqual(len(bundle.retrieved_records), 2)
        self.assertEqual(session.recalled_memories[0].id, "memory-app")
        self.assertIn((MemoryScope.PROJECT, "shanforge"), repository.last_query.scope_filters)
        self.assertEqual(bundle.diagnostics["profile_id"], "writer-profile")
        self.assertEqual(bundle.diagnostics["project_scope_key"], "shanforge")
        self.assertEqual(bundle.diagnostics["skill_count"], 1)

    def test_memory_domain_service_distills_session_and_persists_results(self) -> None:
        from domain.memory.service import DefaultMemoryDomainService

        repository = _MemoryRepository()
        evidence_repository = _EvidenceRepository()
        dataset_repository = _DatasetRepository()
        service = DefaultMemoryDomainService(
            memory_records=repository,
            evidence_records=evidence_repository,
            dataset_records=dataset_repository,
            reasoning=_ReasoningPort(),
            default_project_scope_key="shanforge",
        )
        session = AgentSession(
            id="session-distill",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Extract a reusable procedure.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": "compose"})
        session.add_artifact(
            SessionArtifact(
                kind="capability",
                uri="capability://context.inspect",
                summary="Captured runtime context.",
            )
        )

        result = service.distill_session(session)
        explanation = service.explain_session_memory(session)

        self.assertEqual(len(result.evidence_records), 4)
        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(result.promotion_decisions[0].status, MemoryStatus.ACCEPTED)
        self.assertEqual(result.promotion_decisions[1].status, MemoryStatus.DRAFT)
        self.assertEqual(len(result.promoted_records), 1)
        self.assertEqual(len(repository.records), 2)
        self.assertEqual(len(evidence_repository.records), 4)
        self.assertEqual(len(dataset_repository.samples), 2)
        self.assertEqual(session.memory_candidates[1].kind, MemoryKind.PROCEDURAL)
        self.assertEqual(explanation["candidate_count"], 2)
        self.assertEqual(explanation["promotion_statuses"], ("accepted", "draft"))


if __name__ == "__main__":
    unittest.main()
