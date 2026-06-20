from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from domain.memory.ports import MemoryRuleBundlePort
from runtime.capability.contracts import CapabilityInvocationContext
from runtime.rule_source.service import RuleSourceService


@dataclass(slots=True)
class MemoryRuleBundleAdapter(MemoryRuleBundlePort):
    """Adapts the rule_source capability package to the memory domain."""

    service: RuleSourceService
    inspection_session_id: str = "session-assembly"

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> Mapping[str, Any]:
        bundle = self.service.load_rule_bundle(
            workspace_root=workspace_root,
            profile_id=profile_id,
            context=CapabilityInvocationContext(
                session_id=self.inspection_session_id,
                profile_id=profile_id,
                workspace_root=workspace_root,
            ),
        )
        return {
            **bundle.values,
            "workspace_root": bundle.workspace_root,
            "profile_id": bundle.profile_id,
        }
