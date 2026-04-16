from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from access.cli.commands.run_demo import build_demo_manifest
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentAppMetadata
from domain.memory.models import MemoryScope
from domain.workflow.models import WorkflowDefinition
from domain.workflow.steps import StepKind, WorkflowStep
from settings.composition import Settings, build_default_container


class PlatformScaffoldTests(unittest.TestCase):
    def test_default_container_runs_demo_manifest(self):
        container = build_default_container()

        result = container.runtime_api.run_manifest(
            manifest=build_demo_manifest(),
            user_input="Create the first platform scaffold.",
        )

        self.assertEqual(result.session.status, "completed")
        self.assertEqual(result.state.workflow_id, "default")
        self.assertEqual(len(result.state.step_records), 1)
        self.assertIn("Mock response generated", result.response.summary)
        self.assertIn("draft", result.session.context)
        context_event = next(
            event for event in result.session.events if event.type == "context_compiled"
        )
        self.assertGreaterEqual(context_event.payload["segment_count"], 3)
        self.assertGreater(context_event.payload["max_input_tokens"], 0)

    def test_capability_step_returns_context_snapshot(self):
        container = build_default_container()
        manifest = AgentAppManifest(
            metadata=AgentAppMetadata(
                id="demo.capability",
                name="Capability Demo",
                domain="demo",
            ),
            workflows=(
                WorkflowDefinition(
                    id="inspect",
                    name="Inspect Context",
                    description="Validates capability execution wiring.",
                    steps=(
                        WorkflowStep(
                            id="inspect_context",
                            name="Inspect Context",
                            kind=StepKind.CAPABILITY,
                            instruction="Return the current runtime context.",
                            capability_id="context.inspect",
                            output_key="snapshot",
                        ),
                    ),
                ),
            ),
            default_workflow_id="inspect",
        )

        result = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Inspect the current runtime context.",
        )

        self.assertEqual(result.response.summary, "Returned the current runtime context snapshot.")
        self.assertEqual(result.response.tool_calls[0].tool_name, "context.inspect")
        self.assertIn("snapshot", result.session.context)
        self.assertEqual(len(container.artifact_store.artifacts), 1)

    def test_second_prompt_step_receives_first_step_output_in_context(self):
        container = build_default_container()
        manifest = AgentAppManifest(
            metadata=AgentAppMetadata(
                id="demo.multistep",
                name="Multi-Step Demo",
                domain="demo",
            ),
            workflows=(
                WorkflowDefinition(
                    id="compose",
                    name="Compose",
                    description="Draft and then revise with step-level context rebuilds.",
                    steps=(
                        WorkflowStep(
                            id="draft",
                            name="Draft",
                            kind=StepKind.PROMPT,
                            instruction="Create a first draft.",
                            output_key="draft",
                        ),
                        WorkflowStep(
                            id="revise",
                            name="Revise",
                            kind=StepKind.PROMPT,
                            instruction="Revise using all previously produced context.",
                            output_key="revision",
                        ),
                    ),
                ),
            ),
            default_workflow_id="compose",
        )

        result = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Write and revise the platform note.",
        )

        self.assertEqual(len(result.state.step_records), 2)
        self.assertIn("draft", result.session.context)
        self.assertIn("revision", result.session.context)
        self.assertIn("- draft:", result.response.raw_output)
        self.assertIn("Mock response generated for 'draft'.", result.response.raw_output)

        context_events = [
            event for event in result.session.events if event.type == "context_compiled"
        ]
        self.assertEqual(len(context_events), 2)
        self.assertEqual(context_events[0].payload["step_id"], "draft")
        self.assertEqual(context_events[1].payload["step_id"], "revise")

    def test_second_session_receives_recalled_memory_from_first_session(self):
        container = build_default_container()
        manifest = build_demo_manifest()

        first = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Create the first platform scaffold.",
        )
        second = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Continue the scaffold with the previous session context.",
        )

        self.assertEqual(first.session.status, "completed")
        self.assertGreaterEqual(len(container.memory_store.records), 1)
        self.assertGreaterEqual(len(second.session.recalled_memories), 1)
        self.assertEqual(second.session.recalled_memories[0].scope_key, manifest.metadata.id)
        self.assertGreaterEqual(len(container.memory_dataset_store.entries), 1)

    def test_file_backed_memory_persists_across_container_instances(self):
        manifest = build_demo_manifest()
        with TemporaryDirectory() as temp_dir:
            settings = Settings(memory_store_root=temp_dir)

            first_container = build_default_container(settings=settings)
            first_container.runtime_api.run_manifest(
                manifest=manifest,
                user_input="Create the first platform scaffold.",
            )

            second_container = build_default_container(settings=settings)
            second = second_container.runtime_api.run_manifest(
                manifest=manifest,
                user_input="Continue the scaffold with persisted memory.",
            )

            records = second_container.memory_store.list_by_scope(
                MemoryScope.APP,
                manifest.metadata.id,
            )
            self.assertGreaterEqual(len(records), 1)
            self.assertGreaterEqual(len(second.session.recalled_memories), 1)
            self.assertGreaterEqual(
                len(second_container.memory_dataset_store.list_by_session(second.session.id)),
                1,
            )

    def test_container_can_enable_llm_memory_summarizer(self):
        container = build_default_container(
            settings=Settings(
                memory_summarizer_provider="mock",
                memory_summarizer_model="mock-memory-summary",
                memory_summarizer_extract_model="mock-memory-extract",
            )
        )
        manifest = build_demo_manifest()

        result = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Create the first platform scaffold and derive a reusable procedure.",
        )

        self.assertGreaterEqual(len(result.session.memory_candidates), 2)
        self.assertEqual(result.session.memory_candidates[1].kind.value, "procedural")
        self.assertEqual(result.session.promotion_decisions[1].status.value, "draft")
        self.assertGreaterEqual(len(container.memory_dataset_store.entries), 2)

    def test_container_applies_custom_memory_promotion_settings(self):
        container = build_default_container(
            settings=Settings(
                memory_summarizer_provider="mock",
                memory_summarizer_model="mock-memory-summary",
                memory_summarizer_extract_model="mock-memory-extract",
                memory_promotion_min_confidence_by_kind={"procedural": 0.9},
            )
        )
        manifest = build_demo_manifest()

        result = container.runtime_api.run_manifest(
            manifest=manifest,
            user_input="Create the first platform scaffold and derive a reusable procedure.",
        )

        self.assertGreaterEqual(len(result.session.memory_candidates), 2)
        self.assertEqual(result.session.promotion_decisions[1].status.value, "rejected")
        self.assertIn("threshold", result.session.promotion_decisions[1].reason)

    def test_http_route_specs_are_exposed(self):
        from access.http.routes import build_runtime_routes

        routes = build_runtime_routes()

        self.assertEqual(len(routes), 3)
        self.assertEqual(routes[0].path, "/apps/{app_id}/run")


if __name__ == "__main__":
    unittest.main()
