from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.source_backends import ProfileSourceProviderPort
from runtime.profile_source.models import ResolvedProfile


@dataclass(slots=True)
class ProfileSourceService:
    """Self-owned scaffold for profile resolution and listing."""

    profile_source: ProfileSourceProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="profile_source",
            name="Profile Source",
            summary="Resolves and lists long-lived profiles for session and memory routing.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="profile_source.resolve",
                    method_name="resolve_profile",
                    summary="Resolve one profile from lookup hints.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="profile_source.list",
                    method_name="list_profiles",
                    summary="List all visible profiles.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("profile_source", required=False),
            ),
        )

    def resolve_profile(
        self,
        lookup: dict[str, Any],
        context: CapabilityInvocationContext,
    ) -> ResolvedProfile:
        raise NotImplementedError("Scaffold only: implement profile resolution in TASK-017.")

    def list_profiles(
        self,
        context: CapabilityInvocationContext,
    ) -> tuple[ResolvedProfile, ...]:
        raise NotImplementedError("Scaffold only: implement profile listing in TASK-017.")
