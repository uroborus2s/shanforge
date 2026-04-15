from __future__ import annotations

from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentAppMetadata
from domain.workflow.models import WorkflowDefinition
from domain.workflow.steps import StepKind, WorkflowStep


def build_demo_manifest() -> AgentAppManifest:
    """Creates a minimal manifest that exercises the platform scaffold."""

    return AgentAppManifest(
        metadata=AgentAppMetadata(
            id="demo.writer",
            name="Demo Writer",
            domain="demo",
            description="A tiny scaffold app used to validate the v2 runtime layers.",
        ),
        workflows=(
            WorkflowDefinition(
                id="default",
                name="Default Demo Workflow",
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

