from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "art-room"

ROLE_CARDS = (
    "art-director-agent.md",
    "asset-breakdown-agent.md",
    "character-design-agent.md",
    "environment-design-agent.md",
    "prop-costume-design-agent.md",
    "style-continuity-agent.md",
    "image-prompt-agent.md",
    "thread-plan-agent.md",
    "asset-qc-agent.md",
)

REQUIRED_INPUTS = (
    "{episode-id}/script/final-script.md",
    "bible/characters.md",
    "bible/scenes.md",
    "{episode-id}/director/director-brief.md",
    "{episode-id}/director/camera-plan.md",
    "{episode-id}/shots/scene-breakdown.json",
    "{episode-id}/shots/shot-list.json",
    "{episode-id}/storyboard/storyboard-plan.md",
    "{episode-id}/continuity/visual-continuity-bible.json",
    "{episode-id}/production/generation-plan.json",
    "{episode-id}/prompts/shot-prompts-draft.json",
)

REQUIRED_OUTPUTS = (
    "{episode-id}/art/art-direction.md",
    "{episode-id}/art/asset-manifest.json",
    "{episode-id}/art/character-designs.json",
    "{episode-id}/art/location-designs.json",
    "{episode-id}/art/prop-costume-designs.json",
    "{episode-id}/art/style-continuity-bible.json",
    "{episode-id}/prompts/art-image-prompts.json",
    "{episode-id}/art/thread-plan.json",
    "{episode-id}/art/thread-results.json",
    "{episode-id}/art/asset-index.json",
    "{episode-id}/art/asset-qc-report.md",
)

IMAGE_DIRS = (
    "assets/characters/",
    "assets/locations/",
    "assets/props/",
    "assets/costumes/",
    "assets/style/",
    "{episode-id}/assets/reference-frames/",
    "{episode-id}/assets/shot-overrides/",
    "{episode-id}/assets/temp/",
)


class ArtRoomSkillTests(unittest.TestCase):
    def test_skill_frontmatter_project_contract_and_thread_boundary(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---", 2)[1]
        self.assertIn("name: art-room", frontmatter)
        self.assertIn("visual asset department", frontmatter)
        self.assertNotIn("TODO", content)
        self.assertIn("./project/{project-name}/", content)
        self.assertIn("under `./project/{project-name}/{episode-id}/`", content)
        self.assertIn("Do not create a detached art-room project", content)
        self.assertIn("Child planning agents return artifact envelopes", content)
        self.assertIn("codex_app.create_thread", content)
        self.assertIn("codex_app.read_thread", content)
        self.assertIn("codex_app.send_message_to_thread", content)

        for path in REQUIRED_INPUTS + REQUIRED_OUTPUTS + IMAGE_DIRS:
            self.assertIn(path, content)

    def test_all_role_cards_exist_with_artifact_contracts(self) -> None:
        for filename in ROLE_CARDS:
            with self.subTest(filename=filename):
                content = (SKILL_ROOT / "agents" / filename).read_text(encoding="utf-8")

                self.assertIn("## Mission", content)
                self.assertIn("## Inputs", content)
                self.assertIn("## Required Artifacts", content)
                self.assertIn("## Artifact Contract", content)
                self.assertNotIn("TODO", content)

    def test_references_and_schemas_are_present(self) -> None:
        expected_references = (
            "artifact-contract.md",
            "thread-image-workflow.md",
        )
        expected_schemas = (
            "agent-result.schema.json",
            "asset-manifest.schema.json",
            "art-image-prompts.schema.json",
            "thread-plan.schema.json",
            "thread-results.schema.json",
            "asset-index.schema.json",
        )

        for filename in expected_references:
            self.assertTrue((SKILL_ROOT / "references" / filename).exists())
        for filename in expected_schemas:
            payload = json.loads((SKILL_ROOT / "schemas" / filename).read_text(encoding="utf-8"))
            self.assertIn("title", payload)
            self.assertIn("type", payload)

    def test_asset_and_thread_schema_contracts_are_explicit(self) -> None:
        asset_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-manifest.schema.json").read_text(encoding="utf-8")
        )
        prompt_schema = json.loads(
            (SKILL_ROOT / "schemas" / "art-image-prompts.schema.json").read_text(
                encoding="utf-8"
            )
        )
        thread_schema = json.loads(
            (SKILL_ROOT / "schemas" / "thread-plan.schema.json").read_text(encoding="utf-8")
        )

        expected_types = ["character", "location", "prop", "costume", "style", "reference_frame"]
        self.assertEqual(
            asset_schema["properties"]["assets"]["items"]["properties"]["asset_type"]["enum"],
            expected_types,
        )
        self.assertEqual(
            prompt_schema["properties"]["prompts"]["items"]["properties"]["asset_type"]["enum"],
            expected_types,
        )
        batch_item = thread_schema["properties"]["batches"]["items"]
        self.assertIn("thread_prompt", batch_item["required"])
        self.assertIn("output_paths", batch_item["required"])

    def test_thread_workflow_reference_uses_codex_thread_tools(self) -> None:
        content = (SKILL_ROOT / "references" / "thread-image-workflow.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("codex_app.create_thread", content)
        self.assertIn("codex_app.read_thread", content)
        self.assertIn("codex_app.send_message_to_thread", content)
        self.assertIn("{episode-id}/assets/reference-frames/", content)

    def test_openai_metadata_invokes_skill_name(self) -> None:
        content = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "Art Room"', content)
        self.assertIn("Use $art-room", content)

    def test_insectoid_hierarchy_guidance_is_explicit(self) -> None:
        skill_content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        character_content = (
            SKILL_ROOT / "agents" / "character-design-agent.md"
        ).read_text(encoding="utf-8")
        style_content = (
            SKILL_ROOT / "agents" / "style-continuity-agent.md"
        ).read_text(encoding="utf-8")
        prompt_content = (
            SKILL_ROOT / "agents" / "image-prompt-agent.md"
        ).read_text(encoding="utf-8")

        for content in (skill_content, character_content, style_content, prompt_content):
            self.assertIn("Zerg or", content)
            self.assertIn("insectoid factions", content)
            self.assertIn("upper-tier", content)
            self.assertIn("lower-tier", content)

        self.assertIn("humanized-to-insectoid", skill_content)
        self.assertIn("humanization level", character_content)
        self.assertIn("hierarchy drift", style_content)
        self.assertIn("same insectoid descriptors across all tiers", prompt_content)


if __name__ == "__main__":
    unittest.main()
