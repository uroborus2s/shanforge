from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from domain.agent_app.policies import ModelPolicy
from domain.memory.models import (
    CandidateDrafts,
    EvidenceRecord,
    MemoryCandidate,
    MemoryKind,
    MemoryScope,
    SummaryResult,
)
from domain.model.models import ModelRequest
from domain.session.models import AgentSession
from runtime.llm.runtime import LLMRuntime
from runtime.ports import MemorySummarizerPort


@dataclass(slots=True)
class LLMMemorySummarizer(MemorySummarizerPort):
    """LLM-backed summarizer that returns summary text and candidate drafts."""

    llm_runtime: LLMRuntime
    summary_policy: ModelPolicy
    extraction_policy: ModelPolicy
    candidate_kind: MemoryKind = MemoryKind.PROCEDURAL
    candidate_scope: MemoryScope = MemoryScope.APP
    candidate_confidence: float = 0.62
    summary_schema_version: str = "memory_summary_v1"
    candidate_schema_version: str = "memory_candidate_v1"

    def summarize_evidence(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> SummaryResult:
        response = self.llm_runtime.invoke(
            ModelRequest(
                model_policy=self.summary_policy,
                system_prompt="Summarize session evidence into a short reusable memory note.",
                user_prompt=self._render_summary_prompt(session, evidence_records),
                metadata={
                    "step_id": "memory_summary",
                    "session_id": session.id,
                    "workflow_id": session.workflow_id,
                    "response_schema": self.summary_schema_version,
                },
            )
        )
        episode_summary = self._extract_summary_text(response.structured_output, response.content)
        return SummaryResult(
            episode_summary=str(episode_summary),
            metadata={
                "provider": response.model_ref.provider,
                "model": response.model_ref.model,
                "usage": response.usage.input_tokens if response.usage is not None else 0,
                "schema_version": self.summary_schema_version,
            },
        )

    def extract_candidates(
        self,
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
        summary: SummaryResult,
    ) -> CandidateDrafts:
        if not evidence_records:
            return CandidateDrafts()

        response = self.llm_runtime.invoke(
            ModelRequest(
                model_policy=self.extraction_policy,
                system_prompt="Draft one reusable memory candidate from the summarized evidence.",
                user_prompt=self._render_extraction_prompt(session, evidence_records, summary),
                metadata={
                    "step_id": "memory_extract",
                    "session_id": session.id,
                    "workflow_id": session.workflow_id,
                    "response_schema": self.candidate_schema_version,
                },
            )
        )
        payload = self._extract_candidate_payload(response.structured_output)
        if payload is None:
            return CandidateDrafts()
        candidate = MemoryCandidate(
            kind=self.candidate_kind,
            scope=self.candidate_scope,
            scope_key=self._resolve_scope_key(session),
            title=payload["title"],
            body=payload["body"],
            source_event_ids=tuple(event.id for event in session.events),
            evidence_ids=tuple(record.id for record in evidence_records),
            confidence=self.candidate_confidence,
            metadata={
                "generator": "llm_summarizer",
                "summary_model": summary.metadata.get("model"),
                "extraction_model": response.model_ref.model,
                "schema_version": self.candidate_schema_version,
            },
        )
        return CandidateDrafts(candidates=(candidate,))

    def _resolve_scope_key(self, session: AgentSession) -> str:
        if self.candidate_scope is MemoryScope.APP:
            return session.app_id
        if self.candidate_scope is MemoryScope.PROJECT:
            return "shanforge"
        if self.candidate_scope is MemoryScope.SESSION:
            return session.id
        return session.app_id

    @staticmethod
    def _render_summary_prompt(
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
    ) -> str:
        evidence_lines = [
            f"- {record.source_kind}:{record.source_id} => {record.summary}"
            for record in evidence_records
        ]
        return "\n".join(
            [
                f"Workflow: {session.workflow_id}",
                f"User input: {session.user_input}",
                "Evidence:",
                *evidence_lines,
            ]
        )

    @staticmethod
    def _render_extraction_prompt(
        session: AgentSession,
        evidence_records: tuple[EvidenceRecord, ...],
        summary: SummaryResult,
    ) -> str:
        return "\n".join(
            [
                f"Workflow: {session.workflow_id}",
                f"Summary: {summary.episode_summary or ''}",
                f"Evidence count: {len(evidence_records)}",
                "Return one reusable candidate draft with fields: title, body.",
            ]
        )

    @staticmethod
    def _extract_summary_text(structured_output: Mapping[str, Any], raw_content: str) -> str:
        summary = structured_output.get("summary")
        if isinstance(summary, str) and summary.strip():
            return summary.strip()
        return raw_content.strip()

    @staticmethod
    def _extract_candidate_payload(
        structured_output: Mapping[str, Any],
    ) -> dict[str, str] | None:
        title = structured_output.get("title")
        body = structured_output.get("body")
        if not isinstance(title, str) or not title.strip():
            return None
        if not isinstance(body, str) or not body.strip():
            return None
        return {"title": title.strip(), "body": body.strip()}
