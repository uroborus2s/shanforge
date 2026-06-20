from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "writer-room"

ROLE_CARDS = (
    "showrunner-agent.md",
    "story-architect-agent.md",
    "character-agent.md",
    "scene-agent.md",
    "dialogue-agent.md",
    "script-doctor-agent.md",
    "rewrite-agent.md",
    "continuity-agent.md",
    "script-evaluator-agent.md",
    "memory-librarian.md",
    "learning-evolution-agent.md",
)


class WriterRoomSkillTests(unittest.TestCase):
    def test_skill_frontmatter_and_body_are_codex_native(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---", 2)[1]
        self.assertIn("name: writer-room", frontmatter)
        self.assertIn("Codex-native writer room orchestration", frontmatter)
        self.assertNotIn("TODO", content)
        self.assertIn("multi_agent_v1.spawn_agent", content)
        self.assertIn("A child agent executing one role card must not require", content)
        self.assertIn("Do not implement a Python agent loop", content)
        self.assertIn("Do not auto-edit this skill", content)

    def test_project_layout_uses_shared_project_directory_contract(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("./project/{project-name}/", content)
        self.assertIn("bible/world.md", content)
        self.assertIn("bible/geography.md", content)
        self.assertIn("bible/factions.md", content)
        self.assertIn("bible/timeline.md", content)
        self.assertIn("bible/visual-style.md", content)
        self.assertIn("outline/series-outline.md", content)
        self.assertIn("outline/episode-outline-index.md", content)
        self.assertIn("synopsis/story-synopsis.md", content)
        self.assertIn("{episode-id}/script/final-script.md", content)
        self.assertIn("bible/characters.md", content)
        self.assertIn("bible/scenes.md", content)
        self.assertIn("memory/current-state.md", content)
        self.assertIn("migration/migration-map.json", content)
        self.assertIn("{episode-id}/reports/continuity-report.md", content)
        self.assertIn("{episode-id}/reports/script-score.md", content)
        self.assertIn("{episode-id}/logs/writer-room-agent-calls.jsonl", content)
        self.assertNotIn(".factory/runtime/writer-room/<project-id>/", content)
        self.assertNotIn(".factory/runtime/video-projects/<project-id>/", content)
        self.assertNotIn("script/script_v02_final.md", content)

    def test_all_role_cards_exist_with_artifact_contracts(self) -> None:
        for filename in ROLE_CARDS:
            with self.subTest(filename=filename):
                path = SKILL_ROOT / "agents" / filename
                content = path.read_text(encoding="utf-8")

                self.assertIn("## Mission", content)
                self.assertIn("## Inputs", content)
                self.assertIn("## Required Artifacts", content)
                self.assertIn("## Artifact Contract", content)
                self.assertNotIn("TODO", content)

    def test_final_writer_outputs_use_fixed_project_paths(self) -> None:
        combined_content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        )

        self.assertIn("{episode-id}/script/final-script.md", combined_content)
        self.assertIn("{episode-id}/logs/writer-room-agent-calls.jsonl", combined_content)
        self.assertIn("bible/world.md", combined_content)
        self.assertIn("bible/visual-style.md", combined_content)
        self.assertIn("outline/episode-outline-index.md", combined_content)
        self.assertNotIn("script/script_v02_final.md", combined_content)

    def test_writer_room_modes_and_owner_boundary_are_explicit(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        combined_content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        )

        for mode in ("series mode", "episode mode", "writeback mode", "migration mode"):
            self.assertIn(mode, content)

        forbidden_responsibilities = (
            "does not generate image assets",
            "video prompts",
            "audio files",
            "ComfyUI parameters",
            "Only final confirmed cut facts",
        )
        for phrase in forbidden_responsibilities:
            self.assertIn(phrase, content)

        self.assertIn("Do not create character cards", combined_content)
        self.assertIn("Do not include image prompts", combined_content)
        self.assertIn("Do not create scene cards", combined_content)

    def test_references_templates_and_schemas_are_present(self) -> None:
        expected_references = (
            "artifact-contract.md",
            "codex-agent-workflow.md",
            "rubric.md",
        )
        expected_templates = (
            "brief.md",
            "beat-sheet.md",
            "character-bible.md",
            "scene-outline.md",
            "script.md",
            "critique.md",
            "score.md",
            "evolution-notes.md",
        )
        expected_schemas = (
            "agent-result.schema.json",
            "script-score.schema.json",
            "writer-room-project.schema.json",
        )

        for filename in expected_references:
            self.assertTrue((SKILL_ROOT / "references" / filename).exists())
        for filename in expected_templates:
            self.assertTrue((SKILL_ROOT / "assets" / "templates" / filename).exists())
        for filename in expected_schemas:
            payload = json.loads((SKILL_ROOT / "schemas" / filename).read_text(encoding="utf-8"))
            self.assertIn("title", payload)
            self.assertIn("type", payload)

        project_schema = json.loads(
            (SKILL_ROOT / "schemas" / "writer-room-project.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("production_mode", project_schema["required"])
        self.assertEqual(
            project_schema["properties"]["production_mode"]["enum"],
            ["series", "episode", "writeback", "migration"],
        )
        canonical_paths = project_schema["properties"]["canonical_project_paths"]["items"]["enum"]
        self.assertIn("bible/world.md", canonical_paths)
        self.assertIn("bible/visual-style.md", canonical_paths)
        self.assertIn("outline/episode-outline-index.md", canonical_paths)

    def test_agent_result_schema_preserves_handoff_shape(self) -> None:
        schema = json.loads(
            (SKILL_ROOT / "schemas" / "agent-result.schema.json").read_text(encoding="utf-8")
        )

        self.assertEqual(schema["properties"]["status"]["enum"], ["success", "warning", "blocked"])
        self.assertIn("handoff", schema["required"])
        self.assertIn("main_output", schema["properties"]["handoff"]["required"])
        self.assertIn("content", schema["properties"]["artifacts"]["items"]["required"])


if __name__ == "__main__":
    unittest.main()
