from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from runtime.capability.contracts import CapabilityPackageDescriptor


@dataclass(slots=True)
class CapabilityPackageRegistry:
    """Registry for self-owned basic capability package scaffolds."""

    _descriptors: dict[str, CapabilityPackageDescriptor] = field(default_factory=dict)
    _services: dict[str, Any] = field(default_factory=dict)

    def register(
        self,
        descriptor: CapabilityPackageDescriptor,
        service: Any,
    ) -> None:
        self._descriptors[descriptor.package_id] = descriptor
        self._services[descriptor.package_id] = service

    def list_packages(self) -> tuple[CapabilityPackageDescriptor, ...]:
        return tuple(self._descriptors[key] for key in sorted(self._descriptors))

    def get_descriptor(self, package_id: str) -> CapabilityPackageDescriptor | None:
        return self._descriptors.get(package_id)

    def get_service(self, package_id: str) -> Any | None:
        return self._services.get(package_id)
