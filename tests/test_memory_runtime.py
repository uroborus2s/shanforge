from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from domain.agent_app.policies import ModelPolicy
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
from domain.model.models import ModelRef, ModelRequest, ModelResponse, TokenUsage
from domain.session.models import AgentSession, SessionArtifact
from adapters.model_providers.mock_provider import MockLLMProvider
from runtime.ports.llm_provider import LLMProviderPort
from runtime.llm.runtime import LLMRuntime
from runtime.memory.policy import MemoryPromotionPolicy
from runtime.memory.runtime import MemoryRuntime
from runtime.memory.summarizer import LLMMemorySummarizer
from storage.evidence.store import InMemoryEvidenceStore, JsonlEvidenceStore
from storage.memory.store import InMemoryMemoryStore, JsonlMemoryStore
from storage.memory_dataset.store import (
    InMemoryMemoryDatasetStore,
    JsonlMemoryDatasetStore,
)


class _StubSummarizer:
    def summarize_evidence(
        self,
        session: AgentSession,
        evidence_records: tuple[object, ...],
    ) -> SummaryResult:
        return SummaryResult(
            episode_summary=(
                f"Summarized {len(evidence_records)} evidence record(s) "
                f"for {session.workflow_id}."
            ),
        )

    def extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[object, ...],
        summary: SummaryResult,
    ) -> CandidateDrafts:
        return CandidateDrafts(
            candidates=(
                MemoryCandidate(
                    id="candidate-procedure",
                    kind=MemoryKind.PROCEDURAL,
                    scope=MemoryScope.APP,
                    scope_key=session.app_id,
                    title="Procedure Draft",
                    body=summary.episode_summary or "Fallback summary",
                    source_event_ids=tuple(event.id for event in session.events),
                    evidence_ids=tuple(record.id for record in evidence_records),
                    confidence=0.61,
                ),
            )
        )


class _InvalidExtractionSchemaProvider(LLMProviderPort):
    def generate(self, request: ModelRequest) -> ModelResponse:
        step_id = str(request.metadata.get("step_id", "step"))
        if step_id == "memory_summary":
            structured_output = {"summary": "Valid summary"}
        else:
            structured_output = {"summary": "Missing title/body schema"}
        return ModelResponse(
            model_ref=ModelRef(provider="mock", model=request.model_policy.model),
            content="invalid schema response",
            structured_output=structured_output,
            usage=TokenUsage(input_tokens=8, output_tokens=8),
        )


class _OverrideAttemptProvider(LLMProviderPort):
    def generate(self, request: ModelRequest) -> ModelResponse:
        step_id = str(request.metadata.get("step_id", "step"))
        if step_id == "memory_summary":
            structured_output = {"summary": "Summary with overrides"}
        else:
            structured_output = {
                "title": "Override Title",
                "body": "Override Body",
                "kind": "reflective",
                "scope": "project",
                "confidence": 0.99,
            }
        return ModelResponse(
            model_ref=ModelRef(provider="mock", model=request.model_policy.model),
            content="override attempt",
            structured_output=structured_output,
            usage=TokenUsage(input_tokens=8, output_tokens=8),
        )


class MemoryRuntimeTests(unittest.TestCase):
    def test_distill_session_promotes_app_scoped_episode(self) -> None:
        runtime = MemoryRuntime(
            memory_store=InMemoryMemoryStore(),
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            project_scope_key="shanforge",
        )
        session = AgentSession(
            id="session-1",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Write the platform note.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": "compose"})
        session.add_artifact(
            SessionArtifact(
                kind="capability",
                uri="capability://context.inspect",
                summary="Captured a runtime snapshot.",
            )
        )

        result = runtime.distill_session(session)

        self.assertGreaterEqual(len(result.evidence_records), 4)
        self.assertEqual(len(result.candidates), 1)
        self.assertEqual(result.candidates[0].kind, MemoryKind.EPISODIC)
        self.assertEqual(result.promotion_decisions[0].status, MemoryStatus.ACCEPTED)
        self.assertEqual(len(result.promoted_records), 1)
        self.assertEqual(result.promoted_records[0].scope, MemoryScope.APP)
        self.assertEqual(len(runtime.memory_store.records), 1)
        self.assertEqual(session.promotion_decisions[0].status, MemoryStatus.ACCEPTED)
        self.assertEqual(len(runtime.dataset_store.entries), 1)
        self.assertEqual(runtime.dataset_store.entries[0].decision_status, MemoryStatus.ACCEPTED)

    def test_distill_session_includes_summarizer_candidates_and_dataset_samples(self) -> None:
        runtime = MemoryRuntime(
            memory_store=InMemoryMemoryStore(),
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            summarizer=_StubSummarizer(),
            project_scope_key="shanforge",
        )
        session = AgentSession(
            id="session-summary",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Extract repeatable procedure.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": "compose"})

        result = runtime.distill_session(session)

        self.assertEqual(len(result.candidates), 2)
        self.assertEqual(result.candidates[1].kind, MemoryKind.PROCEDURAL)
        self.assertEqual(result.promotion_decisions[1].status, MemoryStatus.DRAFT)
        self.assertEqual(len(runtime.dataset_store.entries), 2)
        self.assertEqual(runtime.dataset_store.entries[1].candidate_kind, MemoryKind.PROCEDURAL)

    def test_distill_session_is_idempotent_for_same_session(self) -> None:
        runtime = MemoryRuntime(
            memory_store=InMemoryMemoryStore(),
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            summarizer=_StubSummarizer(),
            project_scope_key="shanforge",
        )
        session = AgentSession(
            id="session-idempotent",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Extract repeatable procedure.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        session.add_event("workflow_completed", "Completed workflow.", {"workflow_id": "compose"})

        first = runtime.distill_session(session)
        second = runtime.distill_session(session)

        self.assertEqual(len(first.candidates), 2)
        self.assertEqual(len(second.candidates), 2)
        self.assertEqual(len(runtime.memory_store.records), 2)
        self.assertEqual(len(runtime.evidence_store.records), 3)
        self.assertEqual(len(runtime.dataset_store.entries), 2)

    def test_prepare_session_recalls_only_accepted_records(self) -> None:
        memory_store = InMemoryMemoryStore(
            records=[
                MemoryRecord(
                    id="memory-accepted",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key="demo.writer",
                    title="Accepted Summary",
                    body="Accepted record for this app.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.8,
                    supporting_refs=("event://1", "evidence://1"),
                ),
                MemoryRecord(
                    id="memory-draft",
                    kind=MemoryKind.PROCEDURAL,
                    scope=MemoryScope.APP,
                    scope_key="demo.writer",
                    title="Draft Procedure",
                    body="Should not be recalled by default.",
                    status=MemoryStatus.DRAFT,
                    confidence=0.7,
                    supporting_refs=("event://2", "evidence://2"),
                ),
            ]
        )
        runtime = MemoryRuntime(
            memory_store=memory_store,
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            project_scope_key="shanforge",
        )
        session = AgentSession(
            id="session-2",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Continue the document.",
        )

        bundle = runtime.prepare_session(
            session,
            app_id=session.app_id,
            workflow_id=session.workflow_id,
        )

        self.assertEqual(len(bundle.retrieved_records), 1)
        self.assertEqual(bundle.retrieved_records[0].id, "memory-accepted")
        self.assertEqual(len(session.recalled_memories), 1)
        self.assertEqual(session.recalled_memories[0].title, "Accepted Summary")

    def test_promote_candidate_rejects_missing_supporting_refs(self) -> None:
        runtime = MemoryRuntime(
            memory_store=InMemoryMemoryStore(),
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            project_scope_key="shanforge",
        )
        candidate = MemoryCandidate(
            id="candidate-1",
            kind=MemoryKind.DECLARATIVE,
            scope=MemoryScope.PROJECT,
            scope_key="shanforge",
            title="Project Fact",
            body="This should be rejected without source refs.",
            source_event_ids=(),
            evidence_ids=(),
            confidence=0.9,
        )

        decision, record = runtime.promote_candidate(candidate)

        self.assertEqual(decision.status, MemoryStatus.REJECTED)
        self.assertIsNone(record)

    def test_custom_promotion_policy_rejects_low_confidence_candidate(self) -> None:
        runtime = MemoryRuntime(
            memory_store=InMemoryMemoryStore(),
            evidence_store=InMemoryEvidenceStore(),
            dataset_store=InMemoryMemoryDatasetStore(),
            promotion_policy=MemoryPromotionPolicy(
                default_min_confidence=0.6,
                min_confidence_by_kind={MemoryKind.DECLARATIVE: 0.95},
            ),
            project_scope_key="shanforge",
        )
        candidate = MemoryCandidate(
            id="candidate-low-confidence",
            kind=MemoryKind.DECLARATIVE,
            scope=MemoryScope.PROJECT,
            scope_key="shanforge",
            title="Weak Project Fact",
            body="Should be rejected by stricter declarative threshold.",
            source_event_ids=("event-1",),
            evidence_ids=("evidence-1",),
            confidence=0.9,
        )

        decision, record = runtime.promote_candidate(candidate)

        self.assertEqual(decision.status, MemoryStatus.REJECTED)
        self.assertIn("confidence", decision.reason.lower())
        self.assertIsNone(record)

    def test_llm_summarizer_uses_runtime_and_returns_candidate_drafts(self) -> None:
        summarizer = LLMMemorySummarizer(
            llm_runtime=LLMRuntime(
                providers={"mock": MockLLMProvider()},
                default_provider="mock",
            ),
            summary_policy=ModelPolicy(provider="mock", model="mock-memory-summary"),
            extraction_policy=ModelPolicy(provider="mock", model="mock-memory-extract"),
            candidate_kind=MemoryKind.PROCEDURAL,
            candidate_confidence=0.64,
        )
        session = AgentSession(
            id="session-llm",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Learn a repeatable pattern.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        session.add_event("step_completed", "Completed draft.", {"step_id": "draft"})
        evidence_records = (
            EvidenceRecord(
                session_id=session.id,
                source_kind="event",
                source_id=session.events[0].id,
                source_ref=f"event://{session.events[0].id}",
                summary=session.events[0].summary,
                payload={"type": session.events[0].type},
            ),
        )

        summary = summarizer.summarize_evidence(session, evidence_records)
        drafts = summarizer.extract_candidates(session, evidence_records, summary)

        self.assertIn("mock-memory-summary", summary.metadata["model"])
        self.assertEqual(len(drafts.candidates), 1)
        self.assertEqual(drafts.candidates[0].kind, MemoryKind.PROCEDURAL)
        self.assertEqual(drafts.candidates[0].confidence, 0.64)

    def test_llm_summarizer_rejects_invalid_candidate_schema(self) -> None:
        summarizer = LLMMemorySummarizer(
            llm_runtime=LLMRuntime(
                providers={"mock": _InvalidExtractionSchemaProvider()},
                default_provider="mock",
            ),
            summary_policy=ModelPolicy(provider="mock", model="mock-memory-summary"),
            extraction_policy=ModelPolicy(provider="mock", model="mock-memory-extract"),
        )
        session = AgentSession(
            id="session-invalid-schema",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Learn a repeatable pattern.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        evidence_records = (
            EvidenceRecord(
                session_id=session.id,
                source_kind="event",
                source_id=session.events[0].id,
                source_ref=f"event://{session.events[0].id}",
                summary=session.events[0].summary,
                payload={"type": session.events[0].type},
            ),
        )

        summary = summarizer.summarize_evidence(session, evidence_records)
        drafts = summarizer.extract_candidates(session, evidence_records, summary)

        self.assertEqual(len(drafts.candidates), 0)

    def test_llm_summarizer_ignores_model_override_fields(self) -> None:
        summarizer = LLMMemorySummarizer(
            llm_runtime=LLMRuntime(
                providers={"mock": _OverrideAttemptProvider()},
                default_provider="mock",
            ),
            summary_policy=ModelPolicy(provider="mock", model="mock-memory-summary"),
            extraction_policy=ModelPolicy(provider="mock", model="mock-memory-extract"),
            candidate_kind=MemoryKind.PROCEDURAL,
            candidate_scope=MemoryScope.APP,
            candidate_confidence=0.64,
        )
        session = AgentSession(
            id="session-override",
            app_id="demo.writer",
            workflow_id="compose",
            user_input="Learn a repeatable pattern.",
        )
        session.status = "completed"
        session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
        evidence_records = (
            EvidenceRecord(
                session_id=session.id,
                source_kind="event",
                source_id=session.events[0].id,
                source_ref=f"event://{session.events[0].id}",
                summary=session.events[0].summary,
                payload={"type": session.events[0].type},
            ),
        )

        summary = summarizer.summarize_evidence(session, evidence_records)
        drafts = summarizer.extract_candidates(session, evidence_records, summary)

        self.assertEqual(len(drafts.candidates), 1)
        self.assertEqual(drafts.candidates[0].title, "Override Title")
        self.assertEqual(drafts.candidates[0].kind, MemoryKind.PROCEDURAL)
        self.assertEqual(drafts.candidates[0].scope, MemoryScope.APP)
        self.assertEqual(drafts.candidates[0].confidence, 0.64)

    def test_jsonl_stores_round_trip_memory_evidence_and_dataset(self) -> None:
        with TemporaryDirectory() as temp_dir:
            memory_store = JsonlMemoryStore(temp_dir)
            evidence_store = JsonlEvidenceStore(temp_dir)
            dataset_store = JsonlMemoryDatasetStore(temp_dir)

            record = MemoryRecord(
                id="memory-file",
                kind=MemoryKind.EPISODIC,
                scope=MemoryScope.APP,
                scope_key="demo.writer",
                title="File-backed memory",
                body="Persisted to jsonl.",
                status=MemoryStatus.ACCEPTED,
                confidence=0.77,
                supporting_refs=("event://1",),
            )
            evidence = SessionArtifact(
                id="artifact-file",
                kind="capability",
                uri="capability://context.inspect",
                summary="Persisted artifact.",
            )
            sample = MemoryDistillationSample(
                id="sample-file",
                session_id="session-file",
                candidate_id="candidate-file",
                candidate_kind=MemoryKind.EPISODIC,
                candidate_scope=MemoryScope.APP,
                candidate_scope_key="demo.writer",
                decision_status=MemoryStatus.ACCEPTED,
                decision_reason="Accepted for training corpus.",
                supporting_refs=("event://1",),
            )

            memory_store.save(record)
            evidence_store.save_evidence_from_artifact("session-file", evidence)
            dataset_store.save_entry(sample)

            self.assertEqual(
                memory_store.list_by_scope(MemoryScope.APP, "demo.writer")[0].id,
                "memory-file",
            )
            self.assertEqual(
                evidence_store.list_by_session("session-file")[0].source_id,
                "artifact-file",
            )
            self.assertEqual(dataset_store.list_by_session("session-file")[0].id, "sample-file")


if __name__ == "__main__":
    unittest.main()
