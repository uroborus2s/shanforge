from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from domain.memory.assembly_models import MemoryProviderBinding
from domain.session.delegation_models import SubAgentDigest


@dataclass(slots=True, frozen=True)
class ProjectRuleBundle:
    """Read model describing the workspace rules loaded for one session."""

    source: str | None = None
    project_scope_key: str | None = None
    summary: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "project_scope_key": self.project_scope_key,
            "summary": self.summary,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any] | None) -> "ProjectRuleBundle | None":
        if payload is None:
            return None
        return cls(
            source=str(payload.get("source") or "") or None,
            project_scope_key=str(payload.get("project_scope_key") or "") or None,
            summary=str(payload.get("summary") or "") or None,
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class SkillActivation:
    """Read model describing one skill activated for the session assembly."""

    skill_id: str
    name: str
    scope: str | None = None
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "scope": self.scope,
            "reason": self.reason,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "SkillActivation":
        return cls(
            skill_id=str(payload.get("skill_id") or payload.get("id") or payload.get("name") or ""),
            name=str(payload.get("name") or payload.get("skill_id") or payload.get("id") or ""),
            scope=str(payload.get("scope") or "") or None,
            reason=str(payload.get("reason") or "") or None,
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class BackendBinding:
    """Read model describing one selected backend binding for the session."""

    family: str
    binding_id: str
    source: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "family": self.family,
            "binding_id": self.binding_id,
            "source": self.source,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "BackendBinding":
        return cls(
            family=str(payload.get("family") or payload.get("name") or ""),
            binding_id=str(payload.get("binding_id") or payload.get("value") or ""),
            source=str(payload.get("source") or "") or None,
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class ModelBinding:
    """Read model describing one selected or executed model binding."""

    provider_id: str | None = None
    model_id: str | None = None
    source: str | None = None
    step_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "provider_id": self.provider_id,
            "model_id": self.model_id,
            "source": self.source,
            "step_id": self.step_id,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "ModelBinding":
        return cls(
            provider_id=str(
                payload.get("provider_id") or payload.get("provider") or ""
            )
            or None,
            model_id=str(payload.get("model_id") or payload.get("model") or "") or None,
            source=str(payload.get("source") or "") or None,
            step_id=str(payload.get("step_id") or "") or None,
            metadata=dict(payload.get("metadata") or {}),
        )


@dataclass(slots=True, frozen=True)
class SessionAssemblyManifest:
    """Read model describing how one session was assembled."""

    session_id: str
    profile_id: str | None = None
    workspace_root: str | None = None
    rule_bundle: ProjectRuleBundle | None = None
    active_skills: tuple[SkillActivation, ...] = ()
    recall_scope_filters: tuple[tuple[str, str], ...] = ()
    recalled_memory_ids: tuple[str, ...] = ()
    child_session_ids: tuple[str, ...] = ()
    child_digests: tuple[SubAgentDigest, ...] = ()
    memory_provider_binding: MemoryProviderBinding | None = None
    selected_model: ModelBinding | None = None
    model_bindings: tuple[ModelBinding, ...] = ()
    backend_bindings: tuple[BackendBinding, ...] = ()
    provider_bindings: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "profile_id": self.profile_id,
            "workspace_root": self.workspace_root,
            "rule_bundle": self.rule_bundle.to_mapping() if self.rule_bundle is not None else None,
            "active_skills": tuple(skill.to_mapping() for skill in self.active_skills),
            "recall_scope_filters": tuple(tuple(item) for item in self.recall_scope_filters),
            "recalled_memory_ids": tuple(self.recalled_memory_ids),
            "child_session_ids": tuple(self.child_session_ids),
            "child_digests": tuple(digest.to_mapping() for digest in self.child_digests),
            "memory_provider_binding": (
                self.memory_provider_binding.to_mapping()
                if self.memory_provider_binding is not None
                else None
            ),
            "selected_model": (
                self.selected_model.to_mapping() if self.selected_model is not None else None
            ),
            "model_bindings": tuple(binding.to_mapping() for binding in self.model_bindings),
            "backend_bindings": tuple(binding.to_mapping() for binding in self.backend_bindings),
            "provider_bindings": tuple(self.provider_bindings),
            "sources": tuple(self.sources),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any]) -> "SessionAssemblyManifest":
        return cls(
            session_id=str(payload.get("session_id") or ""),
            profile_id=str(payload.get("profile_id") or "") or None,
            workspace_root=str(payload.get("workspace_root") or "") or None,
            rule_bundle=ProjectRuleBundle.from_mapping(payload.get("rule_bundle")),
            active_skills=tuple(
                SkillActivation.from_mapping(item)
                for item in payload.get("active_skills", ())
            ),
            recall_scope_filters=tuple(
                (str(scope), str(scope_key))
                for scope, scope_key in payload.get("recall_scope_filters", ())
            ),
            recalled_memory_ids=tuple(str(item) for item in payload.get("recalled_memory_ids", ())),
            child_session_ids=tuple(str(item) for item in payload.get("child_session_ids", ())),
            child_digests=tuple(
                SubAgentDigest.from_mapping(item) for item in payload.get("child_digests", ())
            ),
            memory_provider_binding=(
                MemoryProviderBinding.from_mapping(payload["memory_provider_binding"])
                if isinstance(payload.get("memory_provider_binding"), Mapping)
                else None
            ),
            selected_model=(
                ModelBinding.from_mapping(payload["selected_model"])
                if isinstance(payload.get("selected_model"), Mapping)
                else None
            ),
            model_bindings=tuple(
                ModelBinding.from_mapping(item) for item in payload.get("model_bindings", ())
            ),
            backend_bindings=tuple(
                BackendBinding.from_mapping(item) for item in payload.get("backend_bindings", ())
            ),
            provider_bindings=tuple(str(item) for item in payload.get("provider_bindings", ())),
            sources=tuple(str(item) for item in payload.get("sources", ())),
            metadata=dict(payload.get("metadata") or {}),
        )
