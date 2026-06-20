from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from domain.memory.ports import MemoryProfileResolverPort
from domain.session.models import AgentSession
from runtime.capability.contracts import CapabilityInvocationContext
from runtime.profile_source.service import ProfileSourceService


@dataclass(slots=True)
class MemoryProfileResolverAdapter(MemoryProfileResolverPort):
    """Adapts the profile_source capability package to the memory domain."""

    service: ProfileSourceService

    def resolve_profile(
        self,
        session: AgentSession,
        app_id: str,
        workflow_id: str,
    ) -> Mapping[str, Any]:
        resolved = self.service.resolve_profile(
            lookup={
                "profile_id": session.context.get("profile_id"),
                "app_id": app_id,
                "workflow_id": workflow_id,
                "provider_bindings": session.context.get("provider_bindings"),
            },
            context=CapabilityInvocationContext(
                session_id=session.id,
                profile_id=(
                    str(session.context.get("profile_id"))
                    if session.context.get("profile_id") is not None
                    else None
                ),
                workspace_root=(
                    str(session.context.get("workspace_root"))
                    if session.context.get("workspace_root") is not None
                    else None
                ),
            ),
        )
        return {
            "profile_id": resolved.profile_id,
            "label": resolved.label,
            **resolved.metadata,
        }
