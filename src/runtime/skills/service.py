from __future__ import annotations

from dataclasses import dataclass

from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.source_backends import SkillManagementProviderPort, SkillSourceProviderPort
from runtime.skills.models import (
    SkillDescriptor,
    SkillDocument,
    SkillMutationPlan,
    SkillMutationResult,
)


@dataclass(slots=True)
class SkillCatalogService:
    """Self-owned scaffold for listing, viewing, and managing skills."""

    skill_source: SkillSourceProviderPort | None = None
    skill_management: SkillManagementProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="skills",
            name="Skills",
            summary="Lists, views, and governs project and global skills.",
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="skills.list",
                    method_name="list_skills",
                    summary="List skills for one scope.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="skills.view",
                    method_name="view_skill",
                    summary="View one skill document.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="skills.install",
                    method_name="install_skill",
                    summary="Install one skill from a source.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="skills.enable",
                    method_name="enable_skill",
                    summary="Enable one installed skill.",
                    risk_level="L1",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="skills.disable",
                    method_name="disable_skill",
                    summary="Disable one installed skill.",
                    risk_level="L1",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="skills.remove",
                    method_name="remove_skill",
                    summary="Remove one installed skill.",
                    risk_level="L2",
                    writes_data=True,
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("skill_source", required=False),
                CapabilityProviderDependency("skill_management", required=False),
            ),
        )

    def list_skills(
        self,
        scope: str | None,
        profile_id: str | None,
        context: CapabilityInvocationContext,
    ) -> tuple[SkillDescriptor, ...]:
        if self.skill_source is None:
            return ()

        del profile_id, context
        records = self.skill_source.list_skills()
        if scope is not None:
            records = tuple(record for record in records if record.get("scope") == scope)
        return tuple(self._descriptor_from_record(record) for record in records)

    def view_skill(
        self,
        skill_id: str,
        context: CapabilityInvocationContext,
    ) -> SkillDocument:
        del context
        record = self._require_skill_source().load_skill(skill_id)
        if record is None:
            raise KeyError(f"Unknown skill: {skill_id}")
        return SkillDocument(
            descriptor=self._descriptor_from_record(record),
            body=str(record.get("body") or record.get("raw_content") or ""),
            sections=tuple(record.get("sections") or ()),
        )

    def install_skill(
        self,
        source: str,
        scope: str | None,
        context: CapabilityInvocationContext,
    ) -> SkillMutationResult:
        self._ensure_mutation_allowed("install", context)
        result = self._require_skill_management().install_skill(source, scope)
        return self._mutation_result_from_payload(result)

    def enable_skill(
        self,
        skill_id: str,
        context: CapabilityInvocationContext,
    ) -> SkillMutationResult:
        self._ensure_mutation_allowed("enable", context)
        result = self._require_skill_management().set_skill_enabled(skill_id, True)
        return self._mutation_result_from_payload(result)

    def disable_skill(
        self,
        skill_id: str,
        context: CapabilityInvocationContext,
    ) -> SkillMutationResult:
        self._ensure_mutation_allowed("disable", context)
        result = self._require_skill_management().set_skill_enabled(skill_id, False)
        return self._mutation_result_from_payload(result)

    def remove_skill(
        self,
        skill_id: str,
        context: CapabilityInvocationContext,
    ) -> SkillMutationResult:
        self._ensure_mutation_allowed("remove", context)
        result = self._require_skill_management().remove_skill(skill_id)
        return self._mutation_result_from_payload(result)

    def build_mutation_plan(
        self,
        action: str,
        skill_id: str | None,
        source: str | None,
        scope: str | None,
        context: CapabilityInvocationContext,
    ) -> SkillMutationPlan:
        requires_approval = action in {"install", "remove"}
        return SkillMutationPlan(
            action=action,
            skill_id=skill_id,
            source=source,
            scope=scope,
            enabled=True if action == "enable" else False if action == "disable" else None,
            metadata={
                "session_id": context.session_id,
                "risk_level": context.risk_level,
                "requires_approval": requires_approval,
                "sandbox_decision": context.sandbox_decision,
            },
        )

    def _descriptor_from_record(self, record: dict[str, object]) -> SkillDescriptor:
        return SkillDescriptor(
            skill_id=str(record.get("skill_id") or record.get("name") or ""),
            name=str(record.get("name") or record.get("skill_id") or ""),
            summary=str(record.get("summary") or ""),
            scope=str(record.get("scope") or "project"),
            enabled=bool(record.get("enabled", True)),
            metadata={
                "path": record.get("path"),
                "linked_files": record.get("linked_files") or (),
                "required_environment_variables": record.get("required_environment_variables")
                or (),
                "missing_required_environment_variables": record.get(
                    "missing_required_environment_variables"
                )
                or (),
                "setup_needed": bool(record.get("setup_needed", False)),
            },
        )

    def _mutation_result_from_payload(
        self,
        payload: dict[str, object],
    ) -> SkillMutationResult:
        return SkillMutationResult(
            action=str(payload.get("action") or ""),
            skill_id=str(payload.get("skill_id") or ""),
            status=str(payload.get("status") or "unknown"),
            summary=str(payload.get("summary") or ""),
            metadata={
                key: value
                for key, value in payload.items()
                if key not in {"action", "skill_id", "status", "summary"}
            },
        )

    def _require_skill_source(self) -> SkillSourceProviderPort:
        if self.skill_source is None:
            raise RuntimeError("Skill source provider is not configured.")
        return self.skill_source

    def _require_skill_management(self) -> SkillManagementProviderPort:
        if self.skill_management is None:
            raise RuntimeError("Skill management provider is not configured.")
        return self.skill_management

    def _ensure_mutation_allowed(
        self,
        action: str,
        context: CapabilityInvocationContext,
    ) -> None:
        if context.sandbox_decision == "denied":
            raise PermissionError("Sandbox denied the skill mutation request.")
        if action in {"install", "remove"} and not context.approval_ref:
            raise PermissionError(f"Approval is required before skill action: {action}")
