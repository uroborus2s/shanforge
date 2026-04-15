from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class StepExecutionStatus(StrEnum):
    """Normalized per-step execution status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(slots=True, frozen=True)
class StepExecutionRecord:
    """A compact, auditable execution entry for one workflow step."""

    step_id: str
    status: StepExecutionStatus
    summary: str
    output_key: str | None = None


@dataclass(slots=True)
class WorkflowRunState:
    """Mutable runtime view of an executing workflow."""

    workflow_id: str
    step_records: list[StepExecutionRecord] = field(default_factory=list)

    def append(self, record: StepExecutionRecord) -> None:
        self.step_records.append(record)

