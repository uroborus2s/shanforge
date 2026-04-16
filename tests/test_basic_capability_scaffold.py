from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from settings.composition import build_default_container
from domain.session.models import AgentSession, SessionArtifact
from runtime.capability.contracts import CapabilityInvocationContext, CapabilityResourceEnvelope
from runtime.file_access.service import FileAccessService
from runtime.session_search.service import SessionSearchService
from runtime.skills.service import SkillCatalogService
from settings.session import (
    EmptyVectorIndexProvider,
    InMemoryArtifactStore,
    InMemorySearchIndexProvider,
    InMemorySessionArchiveProvider,
    InMemorySessionStore,
)
from settings.skills import LocalSkillCatalogProvider
from settings.workspace import LocalWorkspaceProvider


class BasicCapabilityScaffoldTests(unittest.TestCase):
    def test_container_exposes_basic_capability_scaffold_services(self):
        container = build_default_container()

        self.assertEqual(container.file_access.__class__.__name__, "FileAccessService")
        self.assertEqual(container.web_access.__class__.__name__, "WebAccessService")
        self.assertEqual(container.terminal.__class__.__name__, "TerminalService")
        self.assertEqual(container.browser.__class__.__name__, "BrowserService")
        self.assertEqual(container.session_search.__class__.__name__, "SessionSearchService")
        self.assertEqual(container.skills.__class__.__name__, "SkillCatalogService")
        self.assertEqual(container.rule_source.__class__.__name__, "RuleSourceService")
        self.assertEqual(container.profile_source.__class__.__name__, "ProfileSourceService")
        self.assertEqual(container.clock_identity.__class__.__name__, "ClockIdentityService")

    def test_container_registers_capability_package_descriptors(self):
        container = build_default_container()

        package_ids = tuple(
            descriptor.package_id for descriptor in container.capability_packages.list_packages()
        )

        self.assertEqual(
            package_ids,
            (
                "browser",
                "clock_identity",
                "file_access",
                "profile_source",
                "rule_source",
                "session_search",
                "skills",
                "terminal",
                "web_access",
            ),
        )
        file_package = container.capability_packages.get_descriptor("file_access")
        self.assertIsNotNone(file_package)
        self.assertEqual(file_package.operations[0].method_name, "read_text")
        self.assertEqual(file_package.operations[-1].method_name, "apply_write")

    def test_capability_contract_models_have_stable_defaults(self):
        context = CapabilityInvocationContext(session_id="session-001")
        envelope = CapabilityResourceEnvelope(kind="file")

        self.assertEqual(context.session_id, "session-001")
        self.assertEqual(context.risk_level, "L0")
        self.assertEqual(envelope.kind, "file")
        self.assertEqual(envelope.backend, "shanforge-scaffold")
        self.assertEqual(envelope.payload, {})

    def test_file_access_service_reads_lists_and_writes_within_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "notes").mkdir()
            (root / "notes" / "todo.txt").write_text("ship basic capability layer\n", encoding="utf-8")
            (root / "data.json").write_text('{"status": "ok"}\n', encoding="utf-8")
            provider = LocalWorkspaceProvider(workspace_root=root)
            service = FileAccessService(
                file_provider=provider,
                workspace_provider=provider,
            )
            context = CapabilityInvocationContext(
                session_id="session-file",
                workspace_root=str(root),
            )

            read_result = service.read_text("notes/todo.txt", context)
            self.assertTrue(read_result.exists)
            self.assertIn("ship basic capability layer", read_result.content)

            structured_result = service.read_structured("data.json", "json", context)
            self.assertEqual(structured_result.metadata["parsed"]["status"], "ok")

            snapshot = service.search_paths("**/*.txt", None, context)
            self.assertEqual(snapshot.matches[0].path, "notes/todo.txt")

            plan = service.plan_write("notes/out.txt", "done\n", "create", context)
            apply_result = service.apply_write(plan, context)
            self.assertEqual(apply_result.content, "done\n")
            self.assertTrue((root / "notes" / "out.txt").exists())

            with self.assertRaises(ValueError):
                service.plan_write("notes/out.txt", "noop\n", "patch", context)

    def test_skill_catalog_service_lists_views_and_manages_local_skills(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project_root = root / "skills"
            managed_root = root / ".factory" / "runtime" / "skills"
            imports_root = root / "imports" / "sample-skill"
            state_path = root / ".factory" / "runtime" / "skill-state.json"
            (project_root / "alpha").mkdir(parents=True)
            (project_root / "alpha" / "SKILL.md").write_text(
                (
                    "---\n"
                    "name: alpha\n"
                    "description: Alpha summary\n"
                    "prerequisites:\n"
                    "  env_vars: [ALPHA_KEY]\n"
                    "setup:\n"
                    "  collect_secrets:\n"
                    "    - env_var: ALPHA_SECRET\n"
                    "---\n"
                    "# Alpha\n\nDo alpha.\n"
                ),
                encoding="utf-8",
            )
            (imports_root).mkdir(parents=True)
            (imports_root / "SKILL.md").write_text(
                "---\nname: beta\ndescription: Beta summary\n---\n# Beta\n\nDo beta.\n",
                encoding="utf-8",
            )
            provider = LocalSkillCatalogProvider(
                project_root=project_root,
                managed_root=managed_root,
                state_path=state_path,
            )
            service = SkillCatalogService(
                skill_source=provider,
                skill_management=provider,
            )
            base_context = CapabilityInvocationContext(session_id="session-skill")

            listed = service.list_skills(scope=None, profile_id=None, context=base_context)
            self.assertEqual([item.skill_id for item in listed], ["project:alpha"])
            self.assertTrue(listed[0].metadata["setup_needed"])
            self.assertEqual(
                listed[0].metadata["missing_required_environment_variables"],
                ("ALPHA_KEY", "ALPHA_SECRET"),
            )

            viewed = service.view_skill("project:alpha", base_context)
            self.assertEqual(viewed.descriptor.name, "alpha")
            self.assertIn("Do alpha.", viewed.body)

            install_context = CapabilityInvocationContext(
                session_id="session-skill-install",
                approval_ref="approval-001",
            )
            installed = service.install_skill(str(imports_root), None, install_context)
            self.assertEqual(installed.status, "installed")

            disabled = service.disable_skill("managed:beta", base_context)
            self.assertEqual(disabled.status, "disabled")
            relisted = service.list_skills(scope=None, profile_id=None, context=base_context)
            beta_descriptor = next(item for item in relisted if item.skill_id == "managed:beta")
            self.assertFalse(beta_descriptor.enabled)

            removed = service.remove_skill("managed:beta", install_context)
            self.assertEqual(removed.status, "removed")

    def test_session_search_service_supports_recent_search_slice_and_artifacts(self):
        session_store = InMemorySessionStore()
        artifact_store = InMemoryArtifactStore()
        archive_provider = InMemorySessionArchiveProvider(
            session_store=session_store,
            artifact_store=artifact_store,
        )
        service = SessionSearchService(
            structured_store=archive_provider,
            search_index=InMemorySearchIndexProvider(archive_provider),
            vector_index=EmptyVectorIndexProvider(),
        )

        current_session = AgentSession(
            id="session-current",
            app_id="app",
            workflow_id="wf",
            user_input="Current work",
        )
        previous_session = AgentSession(
            id="session-previous",
            app_id="app",
            workflow_id="wf",
            user_input="Fix docker networking in gateway",
            context={"profile_id": "default", "workspace_root": "/tmp/project"},
        )
        session_store.save_session(current_session)
        session_store.save_session(previous_session)
        previous_session.add_event("assistant", "Investigated docker network namespace", {"command": "docker ps"})
        previous_session.add_event("assistant", "Applied gateway routing fix", {"file": "src/gateway.py"})
        for event in previous_session.events:
            session_store.append_event(previous_session.id, event)
        artifact_store.save_artifact(
            previous_session.id,
            SessionArtifact(
                kind="patch",
                uri="file:///tmp/project/src/gateway.py",
                summary="Gateway routing fix patch",
            ),
        )

        context = CapabilityInvocationContext(session_id="session-current")
        recent_hits = service.search_session_archive("", None, 5, context)
        self.assertEqual(recent_hits[0].session_id, "session-previous")

        search_hits = service.search_session_archive("docker gateway", None, 5, context)
        self.assertEqual(search_hits[0].session_id, "session-previous")
        self.assertIn("docker", search_hits[0].summary.lower())

        slice_result = service.load_session_slice("session-previous", None, 1, context)
        self.assertEqual(len(slice_result.events), 1)
        self.assertEqual(slice_result.cursor, "1")

        explanation = service.explain_session_assembly("session-previous", context)
        self.assertIn("events", explanation.sources)
        self.assertIn("artifacts", explanation.sources)

        artifact_hits = service.search_session_artifacts({"query": "routing fix"}, context)
        self.assertEqual(artifact_hits[0].session_id, "session-previous")


if __name__ == "__main__":
    unittest.main()
