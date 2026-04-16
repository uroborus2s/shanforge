from __future__ import annotations

from typing import Any, Mapping, Protocol


class SkillSourceProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for skill sources."""

    def list_skills(self) -> tuple[Mapping[str, Any], ...]: ...

    def load_skill(self, skill_id: str) -> Mapping[str, Any] | None: ...


class SkillManagementProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for skill management."""

    def install_skill(
        self,
        source: str,
        scope: str | None = None,
    ) -> Mapping[str, Any]: ...

    def set_skill_enabled(
        self,
        skill_id: str,
        enabled: bool,
    ) -> Mapping[str, Any]: ...

    def remove_skill(self, skill_id: str) -> Mapping[str, Any]: ...


class RuleSourceProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for rule sources."""

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> Mapping[str, Any]: ...


class ProfileSourceProviderPort(Protocol):
    """Settings-provider contract owned by the basic capability layer for profile sources."""

    def resolve_profile(self, lookup: Mapping[str, Any]) -> Mapping[str, Any] | None: ...

    def list_profiles(self) -> tuple[Mapping[str, Any], ...]: ...
