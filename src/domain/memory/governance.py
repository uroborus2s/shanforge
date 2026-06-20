from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

from domain.memory.assembly_models import MemoryProviderBinding, RecallPlan
from domain.memory.models import MemoryRecord, MemoryScope, MemoryStatus
from domain.session.delegation_models import SubAgentDigest
from domain.session.models import AgentSession


@dataclass(slots=True, frozen=True)
class RecallGovernanceDecision:
    """Domain decision describing what one recall pass should try to retrieve."""

    scope_filters: tuple[tuple[MemoryScope, str], ...]
    allowed_statuses: tuple[MemoryStatus, ...] = (MemoryStatus.ACCEPTED,)
    total_limit: int = 8
    ranking_strategy: str = "scope_budget_confidence_recency"
    within_scope_order: tuple[str, ...] = ("confidence:desc", "created_at:asc", "id:asc")
    overflow_order: tuple[str, ...] = (
        "scope_order:asc",
        "confidence:desc",
        "created_at:asc",
        "id:asc",
    )
    overflow_fill_enabled: bool = True
    include_external_augmentation: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_recall_plan(self, scope_budgets: Mapping[str, int]) -> RecallPlan:
        return RecallPlan(
            scope_filters=self.scope_filters,
            allowed_statuses=self.allowed_statuses,
            total_limit=max(1, int(self.total_limit or 1)),
            scope_budgets={str(key): int(value) for key, value in scope_budgets.items()},
            ranking_strategy=self.ranking_strategy,
            within_scope_order=self.within_scope_order,
            overflow_order=self.overflow_order,
            overflow_fill_enabled=self.overflow_fill_enabled,
            include_external_augmentation=self.include_external_augmentation,
            metadata=dict(self.metadata),
        )


@dataclass(slots=True, frozen=True)
class MemoryProviderGovernanceDecision:
    """Domain decision describing whether one external provider can participate."""

    binding: MemoryProviderBinding | None = None
    allow_augmentation: bool = False
    allow_sync_turn: bool = False
    allow_session_end_writeback: bool = False
    allow_lifecycle_writeback: bool = False
    allow_delegation_writeback: bool = False
    require_shared_write_capability_for_delegation: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def allows_delegation(self, digest: SubAgentDigest) -> bool:
        if not self.allow_delegation_writeback:
            return False
        if not self.require_shared_write_capability_for_delegation:
            return True
        return bool(digest.metadata.get("shared_provider_write_capability", False))


@dataclass(slots=True, frozen=True)
class MemoryLifecycleDecision:
    """Domain decision describing whether one lifecycle transition is allowed."""

    current_status: MemoryStatus | None
    target_status: MemoryStatus
    allowed: bool
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class RecallGovernancePolicy:
    """Default domain policy for recall scope, status, and augmentation decisions."""

    default_limit: int = 8
    default_ranking_strategy: str = "scope_budget_confidence_recency"

    def decide(
        self,
        session: AgentSession,
        app_id: str,
        workflow_id: str,
        profile_id: str | None,
        project_scope_key: str | None,
        provider_decision: MemoryProviderGovernanceDecision | None,
        default_limit: int | None = None,
    ) -> RecallGovernanceDecision:
        total_limit = max(1, int(default_limit or self.default_limit or 8))
        scope_filters: list[tuple[MemoryScope, str]] = [(MemoryScope.APP, app_id)]
        if project_scope_key:
            scope_filters.append((MemoryScope.PROJECT, project_scope_key))
        return RecallGovernanceDecision(
            scope_filters=tuple(scope_filters),
            total_limit=total_limit,
            ranking_strategy=self.default_ranking_strategy,
            include_external_augmentation=bool(
                provider_decision is not None and provider_decision.allow_augmentation
            ),
            metadata={
                "session_id": session.id,
                "app_id": app_id,
                "workflow_id": workflow_id,
                "profile_id": profile_id,
                "project_scope_key": project_scope_key,
            },
        )


@dataclass(slots=True, frozen=True)
class MemoryProviderGovernancePolicy:
    """Default domain policy for external provider participation and writeback gates."""

    require_shared_write_capability_for_delegation: bool = True

    def decide(
        self,
        binding: MemoryProviderBinding | None,
    ) -> MemoryProviderGovernanceDecision:
        if binding is None or not binding.provider_id or binding.provider_id == "none":
            return MemoryProviderGovernanceDecision()
        writable = bool(binding.writable)
        return MemoryProviderGovernanceDecision(
            binding=binding,
            allow_augmentation=True,
            allow_sync_turn=writable,
            allow_session_end_writeback=writable,
            allow_lifecycle_writeback=writable,
            allow_delegation_writeback=writable,
            require_shared_write_capability_for_delegation=(
                self.require_shared_write_capability_for_delegation
            ),
            metadata={
                "provider_id": binding.provider_id,
                "source": binding.source,
                "namespace": binding.namespace,
                "mode": binding.mode,
                "writable": binding.writable,
            },
        )


@dataclass(slots=True, frozen=True)
class MemoryLifecyclePolicy:
    """Default domain policy for lifecycle transition eligibility."""

    allowed_transitions: Mapping[MemoryStatus | None, tuple[MemoryStatus, ...]] = field(
        default_factory=lambda: {
            None: (
                MemoryStatus.DRAFT,
                MemoryStatus.ACCEPTED,
                MemoryStatus.REJECTED,
            ),
            MemoryStatus.DRAFT: (
                MemoryStatus.DRAFT,
                MemoryStatus.ACCEPTED,
                MemoryStatus.REJECTED,
                MemoryStatus.FORGOTTEN,
            ),
            MemoryStatus.ACCEPTED: (
                MemoryStatus.ACCEPTED,
                MemoryStatus.SUPERSEDED,
                MemoryStatus.FORGOTTEN,
            ),
            MemoryStatus.REJECTED: (MemoryStatus.REJECTED,),
            MemoryStatus.SUPERSEDED: (
                MemoryStatus.SUPERSEDED,
                MemoryStatus.FORGOTTEN,
            ),
            MemoryStatus.FORGOTTEN: (MemoryStatus.FORGOTTEN,),
        }
    )
    allow_forced_manual_override: bool = True
    default_decay_after_days: int | None = None

    def evaluate_transition(
        self,
        current_status: MemoryStatus | None,
        target_status: MemoryStatus,
    ) -> MemoryLifecycleDecision:
        allowed_targets = self.allowed_transitions.get(current_status, ())
        allowed = target_status in allowed_targets
        if allowed and current_status is None:
            reason = "initial_transition_allowed"
        elif allowed:
            reason = "transition_allowed"
        else:
            reason = "transition_not_allowed"
        return MemoryLifecycleDecision(
            current_status=current_status,
            target_status=target_status,
            allowed=allowed,
            reason=reason,
            metadata={"allowed_targets": tuple(status.value for status in allowed_targets)},
        )

    def evaluate_record(
        self,
        record: MemoryRecord,
        *,
        related_records: tuple[MemoryRecord, ...] = (),
        as_of: datetime | None = None,
    ) -> MemoryLifecycleDecision:
        override_status = self._resolve_override_status(record)
        if override_status is not None:
            base_transition = self.evaluate_transition(record.status, override_status)
            forced = bool(self.allow_forced_manual_override and not base_transition.allowed)
            allowed = bool(base_transition.allowed or forced)
            return MemoryLifecycleDecision(
                current_status=record.status,
                target_status=override_status,
                allowed=allowed,
                reason=(
                    "manual_override_applied"
                    if allowed
                    else "manual_override_transition_not_allowed"
                ),
                metadata={
                    **dict(base_transition.metadata),
                    "forced": forced,
                    "hidden": self._is_hidden_status(override_status),
                    "manual_override_actor": record.metadata.get("manual_override_actor"),
                    "manual_override_reason": record.metadata.get("manual_override_reason"),
                    "visible_for_default_recall": override_status is MemoryStatus.ACCEPTED,
                },
            )

        superseding_record = self._find_superseding_record(record, related_records)
        if superseding_record is not None:
            base_transition = self.evaluate_transition(record.status, MemoryStatus.SUPERSEDED)
            return MemoryLifecycleDecision(
                current_status=record.status,
                target_status=MemoryStatus.SUPERSEDED,
                allowed=base_transition.allowed,
                reason="conflict_superseded" if base_transition.allowed else base_transition.reason,
                metadata={
                    **dict(base_transition.metadata),
                    "hidden": True,
                    "conflict_key": self._conflict_key(record),
                    "superseded_by_record_id": superseding_record.id,
                    "superseded_by_created_at": superseding_record.created_at.isoformat(),
                    "visible_for_default_recall": False,
                },
            )

        decay_after_days = self._resolve_decay_after_days(record)
        last_active_at = self._resolve_last_active_at(record)
        effective_as_of = as_of or datetime.now(timezone.utc)
        if (
            decay_after_days is not None
            and decay_after_days >= 0
            and self._supports_decay(record.status)
            and (effective_as_of - last_active_at).days >= decay_after_days
        ):
            base_transition = self.evaluate_transition(record.status, MemoryStatus.FORGOTTEN)
            return MemoryLifecycleDecision(
                current_status=record.status,
                target_status=MemoryStatus.FORGOTTEN,
                allowed=base_transition.allowed,
                reason="decay_expired" if base_transition.allowed else base_transition.reason,
                metadata={
                    **dict(base_transition.metadata),
                    "hidden": True,
                    "decay_after_days": decay_after_days,
                    "last_active_at": last_active_at.isoformat(),
                    "evaluated_at": effective_as_of.isoformat(),
                    "visible_for_default_recall": False,
                },
            )

        retained_transition = self.evaluate_transition(record.status, record.status)
        return MemoryLifecycleDecision(
            current_status=record.status,
            target_status=record.status,
            allowed=retained_transition.allowed,
            reason="state_retained" if retained_transition.allowed else retained_transition.reason,
            metadata={
                **dict(retained_transition.metadata),
                "hidden": self._is_hidden_status(record.status),
                "visible_for_default_recall": record.status is MemoryStatus.ACCEPTED,
            },
        )

    @staticmethod
    def _resolve_override_status(record: MemoryRecord) -> MemoryStatus | None:
        value = record.metadata.get("manual_override_status")
        if value is None:
            return None
        try:
            return MemoryStatus(str(value))
        except ValueError:
            return None

    def _find_superseding_record(
        self,
        record: MemoryRecord,
        related_records: tuple[MemoryRecord, ...],
    ) -> MemoryRecord | None:
        if record.status not in (MemoryStatus.ACCEPTED, MemoryStatus.SUPERSEDED):
            return None
        candidates = [
            candidate
            for candidate in related_records
            if candidate.id != record.id
            and candidate.status is MemoryStatus.ACCEPTED
            and candidate.scope is record.scope
            and candidate.scope_key == record.scope_key
            and candidate.kind is record.kind
            and self._records_conflict(record, candidate)
        ]
        if not candidates:
            return None
        winner = max(
            candidates,
            key=lambda item: (
                item.created_at,
                item.confidence,
                item.id,
            ),
        )
        if winner.created_at > record.created_at:
            return winner
        if winner.created_at == record.created_at and winner.confidence > record.confidence:
            return winner
        if (
            winner.created_at == record.created_at
            and winner.confidence == record.confidence
            and winner.id > record.id
        ):
            return winner
        return None

    @staticmethod
    def _records_conflict(left: MemoryRecord, right: MemoryRecord) -> bool:
        left_conflict_key = MemoryLifecyclePolicy._conflict_key(left)
        right_conflict_key = MemoryLifecyclePolicy._conflict_key(right)
        if left_conflict_key or right_conflict_key:
            return bool(left_conflict_key and left_conflict_key == right_conflict_key)
        return left.title.strip().casefold() == right.title.strip().casefold()

    @staticmethod
    def _conflict_key(record: MemoryRecord) -> str | None:
        value = record.metadata.get("conflict_key")
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    def _resolve_decay_after_days(self, record: MemoryRecord) -> int | None:
        value = record.metadata.get("decay_after_days", self.default_decay_after_days)
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _resolve_last_active_at(record: MemoryRecord) -> datetime:
        value = (
            record.metadata.get("last_reinforced_at")
            or record.metadata.get("last_accessed_at")
            or record.created_at
        )
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(str(value))
        except ValueError:
            return record.created_at

    @staticmethod
    def _supports_decay(status: MemoryStatus) -> bool:
        return status in (
            MemoryStatus.DRAFT,
            MemoryStatus.ACCEPTED,
            MemoryStatus.SUPERSEDED,
            MemoryStatus.FORGOTTEN,
        )

    @staticmethod
    def _is_hidden_status(status: MemoryStatus | None) -> bool:
        return status in (
            MemoryStatus.REJECTED,
            MemoryStatus.SUPERSEDED,
            MemoryStatus.FORGOTTEN,
        )
