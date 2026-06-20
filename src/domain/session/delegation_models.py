from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(slots=True, frozen=True)
class SubAgentDigest:
    """Read model describing one child-session summary returned to the parent session."""

    parent_session_id: str
    child_session_id: str
    summary: str
    responsibility_scope: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    status: str = "pending"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "summary": self.summary,
            "responsibility_scope": tuple(self.responsibility_scope),
            "evidence_refs": tuple(self.evidence_refs),
            "status": self.status,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "SubAgentDigest":
        return cls(
            parent_session_id=str(payload.get("parent_session_id") or ""),
            child_session_id=str(payload.get("child_session_id") or ""),
            summary=str(payload.get("summary") or ""),
            responsibility_scope=tuple(
                str(item) for item in payload.get("responsibility_scope", ())
            ),
            evidence_refs=tuple(str(item) for item in payload.get("evidence_refs", ())),
            status=str(payload.get("status") or "pending"),
            metadata=dict(payload.get("metadata") or {}),
        )
