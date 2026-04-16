from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True, frozen=True)
class CapabilityBudget:
    """Execution budget shared by every basic capability package."""

    max_operations: int | None = None
    max_bytes: int | None = None
    max_tokens: int | None = None


@dataclass(slots=True, frozen=True)
class CapabilityCitation:
    """Normalized citation emitted by one capability result."""

    source_uri: str
    title: str | None = None
    locator: str | None = None


@dataclass(slots=True, frozen=True)
class CapabilityArtifactRef:
    """Artifact reference emitted by one capability result."""

    uri: str
    kind: str
    summary: str | None = None


@dataclass(slots=True, frozen=True)
class CapabilityWarning:
    """Structured warning emitted by one capability result."""

    code: str
    message: str


@dataclass(slots=True, frozen=True)
class CapabilityUsage:
    """Usage counters emitted by one capability result."""

    input_tokens: int | None = None
    output_tokens: int | None = None
    duration_ms: int | None = None


@dataclass(slots=True, frozen=True)
class CapabilityProviderDependency:
    """One provider dependency declared by a basic capability package."""

    provider_key: str
    required: bool = False
    notes: str | None = None


@dataclass(slots=True, frozen=True)
class CapabilityOperationDescriptor:
    """One operation declared by a basic capability package."""

    operation_id: str
    method_name: str
    summary: str
    risk_level: str = "L0"
    writes_data: bool = False


@dataclass(slots=True, frozen=True)
class CapabilityPackageDescriptor:
    """Metadata published by one self-owned basic capability package."""

    package_id: str
    name: str
    summary: str
    operations: tuple[CapabilityOperationDescriptor, ...] = ()
    provider_dependencies: tuple[CapabilityProviderDependency, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class CapabilityInvocationContext:
    """Shared invocation context for every self-owned capability package."""

    session_id: str
    step_id: str | None = None
    profile_id: str | None = None
    workspace_root: str | None = None
    cwd: str | None = None
    user_intent: str | None = None
    risk_level: str = "L0"
    approval_ref: str | None = None
    sandbox_decision: str | None = None
    budget: CapabilityBudget = field(default_factory=CapabilityBudget)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class CapabilityResourceEnvelope:
    """Unified result envelope that wraps capability-specific payloads."""

    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    artifacts: tuple[CapabilityArtifactRef, ...] = ()
    citations: tuple[CapabilityCitation, ...] = ()
    usage: CapabilityUsage | None = None
    warnings: tuple[CapabilityWarning, ...] = ()
    backend: str = "shanforge-scaffold"
    cache_key: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
