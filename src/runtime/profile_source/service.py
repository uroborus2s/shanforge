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
    default_profile_id: str = "local-dev"

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
        payload = self._resolve_payload(lookup, context)
        profile_id = self._first_non_empty(
            payload.get("profile_id"),
            context.profile_id,
            lookup.get("profile_id"),
            self.default_profile_id,
        )
        if profile_id is None:
            raise ValueError("Unable to resolve a profile identifier.")
        label = self._first_non_empty(payload.get("label"), profile_id)
        metadata = {
            key: value
            for key, value in payload.items()
            if key not in {"profile_id", "label"}
        }
        metadata.setdefault("session_id", context.session_id)
        if context.workspace_root is not None:
            metadata.setdefault("workspace_root", context.workspace_root)
        for key in ("app_id", "workflow_id"):
            value = lookup.get(key)
            if value is not None:
                metadata.setdefault(key, value)
        return ResolvedProfile(
            profile_id=profile_id,
            label=label,
            metadata=metadata,
        )

    def list_profiles(
        self,
        context: CapabilityInvocationContext,
    ) -> tuple[ResolvedProfile, ...]:
        if self.profile_source is not None:
            records = self.profile_source.list_profiles()
            if records:
                return tuple(self._profile_from_payload(record, context) for record in records)

        profile_id = self._first_non_empty(context.profile_id, self.default_profile_id)
        if profile_id is None:
            return ()
        return (
            ResolvedProfile(
                profile_id=profile_id,
                label=profile_id,
                metadata={
                    "session_id": context.session_id,
                    "workspace_root": context.workspace_root,
                    "source": "runtime-default",
                },
            ),
        )

    def _resolve_payload(
        self,
        lookup: dict[str, Any],
        context: CapabilityInvocationContext,
    ) -> dict[str, Any]:
        if self.profile_source is not None:
            payload = self.profile_source.resolve_profile(
                {
                    **lookup,
                    "session_id": context.session_id,
                    "context_profile_id": context.profile_id,
                    "workspace_root": context.workspace_root,
                }
            )
            if payload is not None:
                return dict(payload)
        return {
            **lookup,
            "profile_id": self._first_non_empty(lookup.get("profile_id"), context.profile_id),
        }

    def _profile_from_payload(
        self,
        payload: dict[str, Any],
        context: CapabilityInvocationContext,
    ) -> ResolvedProfile:
        profile_id = self._first_non_empty(payload.get("profile_id"), context.profile_id)
        if profile_id is None:
            raise ValueError("Profile source returned a record without profile_id.")
        return ResolvedProfile(
            profile_id=profile_id,
            label=self._first_non_empty(payload.get("label"), profile_id),
            metadata={
                key: value
                for key, value in payload.items()
                if key not in {"profile_id", "label"}
            },
        )

    @staticmethod
    def _first_non_empty(*values: object) -> str | None:
        for value in values:
            if value is None:
                continue
            normalized = str(value).strip()
            if normalized:
                return normalized
        return None
