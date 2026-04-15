from __future__ import annotations

from typing import Protocol

from domain.agent_app.policies import ModelPolicy


class ModelPolicyResolverPort(Protocol):
    """Runtime-owned model policy resolution contract."""

    def resolve(
        self,
        step_policy: ModelPolicy | None,
        app_policy: ModelPolicy | None,
    ) -> ModelPolicy: ...
