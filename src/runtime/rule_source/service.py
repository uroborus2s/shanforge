from __future__ import annotations

from dataclasses import dataclass

from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.source_backends import RuleSourceProviderPort
from runtime.rule_source.models import RuleBundle


@dataclass(slots=True)
class RuleSourceService:
    """Self-owned scaffold for workspace rule loading."""

    rule_source: RuleSourceProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="rule_source",
            name="Rule Source",
            summary="Loads workspace rule bundles used by session and memory assembly.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="rule_source.load_bundle",
                    method_name="load_rule_bundle",
                    summary="Load one workspace rule bundle.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("rule_source", required=False),
            ),
        )

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
        context: CapabilityInvocationContext,
    ) -> RuleBundle:
        raise NotImplementedError("Scaffold only: implement rule loading in TASK-017.")
