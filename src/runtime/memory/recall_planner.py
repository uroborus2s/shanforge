from __future__ import annotations

from dataclasses import dataclass

from domain.memory.assembly_models import RecallPlan
from domain.memory.governance import RecallGovernanceDecision
from domain.memory.models import MemoryScope
from domain.memory.ports import RecallPlannerPort


@dataclass(slots=True)
class DefaultRecallPlanner(RecallPlannerPort):
    """Builds the default recall budget and scope plan for one session."""

    default_limit: int = 8

    def plan(self, decision: RecallGovernanceDecision) -> RecallPlan:
        total_limit = max(1, int(decision.total_limit or self.default_limit or 8))
        scope_budgets = self._allocate_scope_budgets(decision.scope_filters, total_limit)
        return decision.to_recall_plan(scope_budgets=scope_budgets)

    @staticmethod
    def _allocate_scope_budgets(
        scope_filters: tuple[tuple[MemoryScope, str], ...],
        total_limit: int,
    ) -> dict[str, int]:
        if not scope_filters:
            return {}
        base = total_limit // len(scope_filters)
        remainder = total_limit % len(scope_filters)
        budgets: dict[str, int] = {}
        for index, (scope, scope_key) in enumerate(scope_filters):
            budgets[f"{scope.value}:{scope_key}"] = base + (1 if index < remainder else 0)
        return budgets
