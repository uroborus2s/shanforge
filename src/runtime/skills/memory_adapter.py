from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from domain.memory.ports import MemorySkillCatalogPort
from runtime.capability.contracts import CapabilityInvocationContext
from runtime.skills.service import SkillCatalogService


@dataclass(slots=True)
class MemorySkillCatalogAdapter(MemorySkillCatalogPort):
    """Adapts the skills capability package to the memory domain."""

    service: SkillCatalogService
    inspection_session_id: str = "session-assembly"

    def list_skill_index(
        self,
        app_id: str,
        workflow_id: str,
    ) -> tuple[Mapping[str, Any], ...]:
        descriptors = self.service.list_skills(
            scope=None,
            profile_id=None,
            context=CapabilityInvocationContext(
                session_id=self.inspection_session_id,
                metadata={"app_id": app_id, "workflow_id": workflow_id},
            ),
        )
        return tuple(
            {
                "skill_id": descriptor.skill_id,
                "name": descriptor.name,
                "scope": descriptor.scope,
                "summary": descriptor.summary,
                "reason": "skill-catalog-index",
                **descriptor.metadata,
            }
            for descriptor in descriptors
            if descriptor.enabled
        )
