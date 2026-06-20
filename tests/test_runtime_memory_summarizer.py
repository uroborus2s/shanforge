from __future__ import annotations

import unittest

from domain.agent_app.policies import ModelPolicy
from domain.memory.models import EvidenceRecord, MemoryKind, MemoryScope
from domain.model.models import ModelRef, ModelRequest, ModelResponse, TokenUsage
from domain.session.models import AgentSession
from runtime.llm.runtime import LLMRuntime
from runtime.memory.summarizer import LLMMemorySummarizer
from runtime.ports.llm_provider import LLMProviderPort
from settings.model.mock_provider import MockLLMProvider


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


def _build_session(session_id: str) -> AgentSession:
    session = AgentSession(
        id=session_id,
        app_id="demo.writer",
        workflow_id="compose",
        user_input="Learn a repeatable pattern.",
    )
    session.status = "completed"
    session.add_event("workflow_started", "Started workflow.", {"workflow_id": "compose"})
    return session


def _build_evidence(session: AgentSession) -> tuple[EvidenceRecord, ...]:
    return (
        EvidenceRecord(
            session_id=session.id,
            source_kind="event",
            source_id=session.events[0].id,
            source_ref=f"event://{session.events[0].id}",
            summary=session.events[0].summary,
            payload={"type": session.events[0].type},
        ),
    )


class LLMMemorySummarizerTests(unittest.TestCase):
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
        session = _build_session("session-llm")
        evidence_records = _build_evidence(session)

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
        session = _build_session("session-invalid-schema")
        evidence_records = _build_evidence(session)

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
        session = _build_session("session-override")
        evidence_records = _build_evidence(session)

        summary = summarizer.summarize_evidence(session, evidence_records)
        drafts = summarizer.extract_candidates(session, evidence_records, summary)

        self.assertEqual(len(drafts.candidates), 1)
        self.assertEqual(drafts.candidates[0].title, "Override Title")
        self.assertEqual(drafts.candidates[0].kind, MemoryKind.PROCEDURAL)
        self.assertEqual(drafts.candidates[0].scope, MemoryScope.APP)
        self.assertEqual(drafts.candidates[0].confidence, 0.64)


if __name__ == "__main__":
    unittest.main()
