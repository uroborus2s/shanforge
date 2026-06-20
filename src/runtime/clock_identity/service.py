from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from runtime.capability.contracts import (
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.execution_backends import ClockProviderPort, IdGeneratorProviderPort


@dataclass(slots=True)
class ClockIdentityService:
    """Self-owned scaffold for time and ID generation."""

    clock_provider: ClockProviderPort | None = None
    id_provider: IdGeneratorProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="clock_identity",
            name="Clock Identity",
            summary="Provides platform time and ID generation services.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="clock_identity.now",
                    method_name="now",
                    summary="Read the current platform time.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="clock_identity.new_id",
                    method_name="new_id",
                    summary="Generate one scoped platform ID.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("clock", required=False),
                CapabilityProviderDependency("id_generator", required=False),
            ),
        )

    def now(self) -> datetime:
        if self.clock_provider is not None:
            current = self.clock_provider.now()
        else:
            current = datetime.now(timezone.utc)
        if current.tzinfo is None:
            return current.replace(tzinfo=timezone.utc)
        return current.astimezone(timezone.utc)

    def new_id(self, prefix: str) -> str:
        normalized_prefix = prefix.strip() or "id"
        if self.id_provider is not None:
            return self.id_provider.new_id(normalized_prefix)
        return f"{normalized_prefix}-{uuid4()}"
