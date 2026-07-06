from __future__ import annotations

import sys
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from domain.agent_app.manifest import AgentAppManifest  # noqa: E402
from domain.agent_app.models import AgentAppMetadata  # noqa: E402
from domain.workflow.models import WorkflowDefinition  # noqa: E402
from domain.workflow.steps import StepKind, WorkflowStep  # noqa: E402


def build_runtime_test_manifest() -> AgentAppManifest:
    return AgentAppManifest(
        metadata=AgentAppMetadata(
            id="demo.writer",
            name="Runtime Test Writer",
            domain="test",
            description="Fixture app used by runtime integration tests.",
        ),
        workflows=(
            WorkflowDefinition(
                id="default",
                name="Default Runtime Test Workflow",
                description="Runs one prompt step through the mock provider.",
                steps=(
                    WorkflowStep(
                        id="draft",
                        name="Draft Response",
                        kind=StepKind.PROMPT,
                        instruction="Summarize the user request as the first v2 platform step.",
                        output_key="draft",
                    ),
                ),
            ),
        ),
        default_workflow_id="default",
    )
