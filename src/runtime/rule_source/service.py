from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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
        resolved_workspace_root = workspace_root or context.workspace_root
        if self.rule_source is not None:
            payload = dict(
                self.rule_source.load_rule_bundle(resolved_workspace_root, profile_id)
            )
        else:
            project_scope_key = self._derive_project_scope_key(resolved_workspace_root)
            payload = {
                "source": "workspace-default",
                "project_scope_key": project_scope_key,
                "summary": (
                    f"Workspace rules resolved for '{project_scope_key}'."
                    if project_scope_key
                    else "Workspace rules are unavailable."
                ),
            }
        if resolved_workspace_root is not None:
            payload.setdefault("workspace_root", resolved_workspace_root)
        if profile_id is not None:
            payload.setdefault("profile_id", profile_id)
        return RuleBundle(
            workspace_root=resolved_workspace_root,
            profile_id=profile_id,
            values=payload,
        )

    @staticmethod
    def _derive_project_scope_key(workspace_root: str | None) -> str | None:
        if workspace_root is None:
            return None
        name = Path(workspace_root).expanduser().resolve().name.strip()
        return name or None
