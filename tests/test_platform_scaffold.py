from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from access.cli.commands.run_demo import build_demo_manifest
from domain.agent_app.manifest import AgentAppManifest
from domain.agent_app.models import AgentAppMetadata
from domain.memory.models import (
    MemoryKind,
    MemoryLifecycleAuditAction,
    MemoryLifecycleAuditFilter,
    MemoryLifecycleQueueFilter,
    MemoryLifecycleQueueReviewStatus,
    MemoryLifecycleReviewResolution,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
)
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

    def test_file_backed_lifecycle_queue_persists_review_status_across_containers(self):
        manifest = build_demo_manifest()
        with TemporaryDirectory() as temp_dir:
            settings = Settings(memory_store_root=temp_dir)

            first_container = build_default_container(settings=settings)
            result = first_container.runtime_api.run_manifest(
                manifest=manifest,
                user_input="Create the first platform scaffold.",
            )
            first_container.memory_store.save_memory_record(
                MemoryRecord(
                    id="memory-decayed",
                    kind=MemoryKind.EPISODIC,
                    scope=MemoryScope.APP,
                    scope_key=manifest.metadata.id,
                    title="Stale episodic note",
                    body="This note should decay.",
                    status=MemoryStatus.ACCEPTED,
                    confidence=0.68,
                    supporting_refs=("event://2",),
                    metadata={
                        "decay_after_days": 30,
                        "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                    },
                )
            )
            first_container.memory_api.load_lifecycle_queue(result.session.id)
            first_container.memory_api.update_lifecycle_queue(
                result.session.id,
                actor="memory-reviewer",
                queue_filter=MemoryLifecycleQueueFilter(
                    effective_statuses=(MemoryStatus.FORGOTTEN,),
                ),
                review_status=MemoryLifecycleQueueReviewStatus.DISMISSED,
                note="manual triage",
                resolution=MemoryLifecycleReviewResolution.STALE_SIGNAL,
            )

            second_container = build_default_container(settings=settings)
            second_container.session_store.save_session(result.session)
            queue = second_container.memory_api.load_lifecycle_queue(
                result.session.id,
                queue_filter=MemoryLifecycleQueueFilter(
                    actionable_only=False,
                    review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
                ),
            )

            self.assertEqual(
                second_container.memory_lifecycle_queue_store.__class__.__name__,
                "JsonlMemoryLifecycleQueueStore",
            )
            self.assertEqual(tuple(item.record_id for item in queue.items), ("memory-decayed",))
            self.assertEqual(
                queue.items[0].review_status,
                MemoryLifecycleQueueReviewStatus.DISMISSED,
            )
            self.assertEqual(queue.items[0].review_note, "manual triage")
            self.assertEqual(
                queue.items[0].review_resolution,
                MemoryLifecycleReviewResolution.STALE_SIGNAL,
            )
            audit_log = second_container.memory_api.load_lifecycle_audit(
                result.session.id,
                audit_filter=MemoryLifecycleAuditFilter(
                    actions=(MemoryLifecycleAuditAction.REVIEW_STATUS_UPDATED,),
                ),
            )
            self.assertEqual(
                second_container.memory_lifecycle_audit_store.__class__.__name__,
                "JsonlMemoryLifecycleAuditStore",
            )
            self.assertEqual(
                tuple(entry.record_id for entry in audit_log.entries),
                ("memory-decayed",),
            )
            second_container.memory_api.reopen_lifecycle_queue(
                result.session.id,
                actor="memory-reviewer",
                queue_filter=MemoryLifecycleQueueFilter(
                    actionable_only=False,
                    review_statuses=(MemoryLifecycleQueueReviewStatus.DISMISSED,),
                ),
                note="reopen for manual confirmation",
            )
            reopened_queue = second_container.memory_api.load_lifecycle_queue(
                result.session.id,
            )
            reopened_audit = second_container.memory_api.load_lifecycle_audit(
                result.session.id,
                audit_filter=MemoryLifecycleAuditFilter(
                    actions=(MemoryLifecycleAuditAction.REVIEW_REOPENED,),
                ),
            )
            self.assertEqual(reopened_queue.selected_record_ids, ("memory-decayed",))
            self.assertIsNone(reopened_queue.items[0].review_resolution)
            self.assertEqual(
                tuple(entry.record_id for entry in reopened_audit.entries),
                ("memory-decayed",),
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

    def test_container_persists_session_assembly_snapshot(self):
        container = build_default_container()

        result = container.runtime_api.run_manifest(
            manifest=build_demo_manifest(),
            user_input="Create the first platform scaffold.",
        )

        manifest = container.assembly_store.get(result.session.id)

        self.assertIsNotNone(manifest)
        self.assertEqual(manifest.session_id, result.session.id)
        self.assertEqual(
            container.memory_api.explain_session_assembly(result.session.id).session_id,
            result.session.id,
        )
        preview = container.memory_api.preview_recall(result.session.id, limit=1)
        self.assertEqual(preview.session_id, result.session.id)
        self.assertEqual(preview.plan.total_limit, 1)
        self.assertEqual(preview.query.session_id, result.session.id)
        self.assertTrue(preview.scope_breakdowns)
        self.assertTrue(preview.record_rankings)

    def test_container_wires_runtime_support_services_into_session_assembly(self):
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            skill_root = workspace_root / "skills" / "alpha"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: alpha\ndescription: Alpha runtime skill\n---\n# Alpha\n",
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                    default_profile_id="writer-profile",
                )
            )

            result = container.runtime_api.run_manifest(
                manifest=build_demo_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)

            self.assertEqual(manifest.profile_id, "writer-profile")
            assert manifest.rule_bundle is not None
            self.assertEqual(manifest.rule_bundle.project_scope_key, workspace_root.name)
            self.assertEqual(manifest.rule_bundle.source, "workspace-default")
            self.assertEqual(manifest.active_skills[0].skill_id, "project:alpha")
            self.assertEqual(manifest.selected_model.provider_id, "mock")
            self.assertEqual(manifest.selected_model.model_id, "mock-chat")
            self.assertEqual(manifest.model_bindings[0].step_id, "draft")
            backend_bindings = {binding.family: binding for binding in manifest.backend_bindings}
            self.assertEqual(backend_bindings["browser_automation"].binding_id, "local")
            self.assertEqual(backend_bindings["capability_registry"].binding_id, "local")
            self.assertEqual(
                backend_bindings["approval_policy"].metadata["implementation_class"],
                "ApprovalGate",
            )
            self.assertIn(("project", workspace_root.name), manifest.recall_scope_filters)

    def test_http_route_specs_are_exposed(self):
        from access.http.routes import build_runtime_routes

        routes = build_runtime_routes()

        self.assertEqual(len(routes), 3)
        self.assertEqual(routes[0].path, "/apps/{app_id}/run")


if __name__ == "__main__":
    unittest.main()
