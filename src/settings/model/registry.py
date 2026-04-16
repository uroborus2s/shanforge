from __future__ import annotations

from dataclasses import dataclass

from domain.agent_app.policies import ModelPolicy, ReasoningEffort


@dataclass(slots=True)
class InMemoryModelRegistry:
    """Minimal model policy resolver used by the scaffold runtime."""

    default_policy: ModelPolicy

    @classmethod
    def with_defaults(
        cls,
        provider: str = "mock",
        model: str = "mock-chat",
    ) -> "InMemoryModelRegistry":
        return cls(
            default_policy=ModelPolicy(
                provider=provider,
                model=model,
                reasoning_effort=ReasoningEffort.MEDIUM,
            )
        )

    def resolve(
        self,
        step_policy: ModelPolicy | None,
        app_policy: ModelPolicy | None,
    ) -> ModelPolicy:
        return step_policy or app_policy or self.default_policy
