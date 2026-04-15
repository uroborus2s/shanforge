from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ApprovalDecision:
    """Result of approval evaluation for a single step."""

    approved: bool
    reason: str


@dataclass(slots=True, frozen=True)
class SandboxDecision:
    """Result of sandbox policy evaluation."""

    allowed: bool
    reason: str
    denied_writeset: tuple[str, ...] = field(default_factory=tuple)


@dataclass(slots=True, frozen=True)
class ExecutionPermit:
    """Combined execution permit for approval + sandbox gates."""

    approved: bool
    sandboxed: bool
    reason: str
