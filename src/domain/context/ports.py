from __future__ import annotations

from typing import Any, Mapping, Protocol


class ContextRuleBundlePort(Protocol):
    """Foundation capability contract consumed by the context domain for rule lookup."""

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> Mapping[str, Any]: ...


class ContextSkillContentPort(Protocol):
    """Foundation capability contract consumed by the context domain for skill content loading."""

    def load_skill(self, skill_id: str) -> Mapping[str, Any] | None: ...


class ContextTokenEstimationPort(Protocol):
    """Foundation capability contract consumed by the context domain for token estimation."""

    def estimate_tokens(self, value: Any) -> int: ...


class ContextRenderingPort(Protocol):
    """Foundation capability contract consumed by the context domain for message rendering."""

    def render_segment(self, segment_type: str, payload: Mapping[str, Any]) -> str: ...
