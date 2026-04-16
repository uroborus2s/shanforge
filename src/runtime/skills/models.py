from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class SkillDescriptor:
    """Normalized skill descriptor exposed by the skill catalog package."""

    skill_id: str
    name: str
    summary: str = ""
    scope: str = "project"
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SkillDocument:
    """One fully loaded skill document."""

    descriptor: SkillDescriptor
    body: str = ""
    sections: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class SkillMutationPlan:
    """Governed mutation request for skill management actions."""

    action: str
    skill_id: str | None = None
    source: str | None = None
    scope: str | None = None
    enabled: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SkillMutationResult:
    """Result returned after a governed skill management action."""

    action: str
    skill_id: str
    status: str
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
