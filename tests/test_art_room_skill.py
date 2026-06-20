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
    "art/series-asset-plan.md",
    "art/series-thread-plan.json",
    "art/series-thread-results.json",
    "assets/asset-index.json",
    "{episode-id}/art/asset-prep-plan.md",
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

ART_REVIEW_DIRS = (
    "art/reports/",
    "art/audits/",
    "art/reviews/",
    "art/runs/",
    "{episode-id}/art/reports/",
    "{episode-id}/art/audits/",
    "{episode-id}/art/reviews/",
    "{episode-id}/art/runs/",
)

IMAGE_DIRS = (
    "assets/characters/",
    "assets/locations/",
    "assets/props/",
    "assets/costumes/",
    "assets/style/",
    "{episode-id}/assets/characters/",
    "{episode-id}/assets/locations/",
    "{episode-id}/assets/props/",
    "{episode-id}/assets/costumes/",
    "{episode-id}/assets/reference-frames/",
    "{episode-id}/assets/shot-overrides/",
    "{episode-id}/assets/temp/",
)


class ArtRoomSkillTests(unittest.TestCase):
    def test_skill_frontmatter_project_contract_and_thread_boundary(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        normalized_content = " ".join(content.split())

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
        self.assertIn("character_master_card", content)
        self.assertIn("prop_master_card", content)
        self.assertIn("location_master_scene_card", content)
        self.assertIn("production_metadata", content)
        self.assertIn("model_visible_prompt", content)
        self.assertIn("copy_ready", content)
        self.assertIn("creation_order", content)
        self.assertIn("depends_on_assets", content)
        self.assertIn("body_metrics", content)
        self.assertIn("physical_dimensions", content)
        self.assertIn("output_format", content)
        self.assertIn("transparent cutout", content)
        self.assertIn("foreground, midground, and background", normalized_content)
        self.assertIn("20 characters or fewer", content)

        self.assertIn("Output Directory Discipline", content)
        self.assertIn("art/runs/{run-id}/", content)
        self.assertIn("*-audit*", content)
        self.assertIn("*-review*", content)
        self.assertIn("*-score*", content)

        for path in REQUIRED_INPUTS + REQUIRED_OUTPUTS + ART_REVIEW_DIRS + IMAGE_DIRS:
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
            "asset-card-prompt-templates.md",
        )
        expected_schemas = (
            "agent-result.schema.json",
            "series-asset-plan.schema.json",
            "asset-prep-plan.schema.json",
            "asset-manifest.schema.json",
            "character-designs.schema.json",
            "location-designs.schema.json",
            "prop-costume-designs.schema.json",
            "style-continuity-bible.schema.json",
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
        prep_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-prep-plan.schema.json").read_text(
                encoding="utf-8"
            )
        )

        expected_types = ["character", "location", "prop", "costume", "style", "reference_frame"]
        expected_subtypes = [
            "character_master_card",
            "character_episode_state_card",
            "prop_master_card",
            "prop_episode_state_card",
            "location_master_scene_card",
            "location_episode_scene_card",
            "style_reference",
            "reference_frame",
            "shot_override",
        ]
        self.assertEqual(
            asset_schema["properties"]["assets"]["items"]["properties"]["asset_type"]["enum"],
            expected_types,
        )
        asset_item = asset_schema["properties"]["assets"]["items"]
        self.assertIn("asset_subtype", asset_item["required"])
        self.assertIn("file", asset_item["required"])
        for dependency_field in (
            "creation_order",
            "creation_phase",
            "depends_on_assets",
            "blocks_assets",
            "dependency_reason",
            "priority",
        ):
            self.assertIn(dependency_field, asset_item["required"])
        self.assertIn("output_format", asset_item["required"])
        self.assertEqual(asset_item["properties"]["asset_subtype"]["enum"], expected_subtypes)
        self.assertEqual(asset_item["properties"]["file"]["pattern"], "^[^/]{1,20}\\.[^./]+$")
        self.assertEqual(asset_item["properties"]["output_format"]["$ref"], "#/$defs/output_format")
        self.assertEqual(
            prompt_schema["properties"]["prompts"]["items"]["properties"]["asset_type"]["enum"],
            expected_types,
        )
        prompt_item = prompt_schema["properties"]["prompts"]["items"]
        self.assertIn("production_metadata", prompt_item["required"])
        self.assertIn("model_visible_prompt", prompt_item["required"])
        self.assertIn("output_format", prompt_item["required"])
        self.assertIn("copy_ready", prompt_item["required"])
        self.assertIn("asset_subtype", prompt_item["required"])
        metadata_required = prompt_item["properties"]["production_metadata"]["required"]
        visible_required = prompt_item["properties"]["model_visible_prompt"]["required"]
        copy_ready_required = prompt_item["properties"]["copy_ready"]["required"]
        for field in (
            "asset_id",
            "asset_subtype",
            "output_file",
            "prompt_id",
            "source_refs",
            "continuity_refs",
            "usage",
        ):
            self.assertIn(field, metadata_required)
        for field in (
            "visible_goal",
            "style_quality",
            "subject_content",
            "composition_motion",
            "visible_continuity",
            "negative_prompt",
        ):
            self.assertIn(field, visible_required)
        for field in (
            "positive_prompt",
            "negative_prompt",
            "chatgpt_image_prompt",
            "gemini_image_prompt",
        ):
            self.assertIn(field, copy_ready_required)

        prep_item = prep_schema["properties"]["required_assets"]["items"]
        for dependency_field in (
            "creation_order",
            "creation_phase",
            "depends_on_assets",
            "blocks_assets",
            "dependency_reason",
            "priority",
        ):
            self.assertIn(dependency_field, prep_item["required"])
        self.assertIn("output_format", prep_item["required"])
        batch_item = thread_schema["properties"]["batches"]["items"]
        self.assertIn("thread_prompt", batch_item["required"])
        self.assertIn("output_paths", batch_item["required"])
        self.assertIn("creation_order", batch_item["required"])
        self.assertIn("depends_on_batches", batch_item["required"])
        self.assertIn("depends_on_assets", batch_item["required"])
        self.assertIn("output_format_contracts", batch_item["required"])
        output_contract = batch_item["properties"]["output_format_contracts"]["items"]
        self.assertIn("asset_type", output_contract["required"])
        self.assertIn("asset_subtype", output_contract["required"])

        output_format = asset_schema["$defs"]["output_format"]
        for field in (
            "deliverable_kind",
            "file_format",
            "minimum_resolution",
            "background_policy",
            "alpha_policy",
            "canvas_aspect_ratio",
            "required_views",
            "composition_layers",
            "qc_checks",
        ):
            self.assertIn(field, output_format["required"])
        self.assertIn(
            "transparent_alpha",
            output_format["properties"]["background_policy"]["enum"],
        )
        self.assertIn("video_frame", output_format["properties"]["background_policy"]["enum"])
        self.assertIn("required", output_format["properties"]["alpha_policy"]["enum"])
        self.assertIn("forbidden", output_format["properties"]["alpha_policy"]["enum"])
        self.assertIn("16:9", output_format["properties"]["canvas_aspect_ratio"]["enum"])
        self.assertEqual(
            output_format["properties"]["composition_layers"]["required"],
            ["foreground", "midground", "background"],
        )

    def test_character_and_prop_design_schemas_capture_scale_detail(self) -> None:
        character_schema = json.loads(
            (SKILL_ROOT / "schemas" / "character-designs.schema.json").read_text(
                encoding="utf-8"
            )
        )
        prop_schema = json.loads(
            (SKILL_ROOT / "schemas" / "prop-costume-designs.schema.json").read_text(
                encoding="utf-8"
            )
        )
        location_schema = json.loads(
            (SKILL_ROOT / "schemas" / "location-designs.schema.json").read_text(
                encoding="utf-8"
            )
        )

        character_item = character_schema["properties"]["characters"]["items"]
        self.assertIn("body_metrics", character_item["required"])
        self.assertIn("output_format_requirements", character_item["required"])
        self.assertEqual(
            character_item["properties"]["body_metrics"]["required"],
            ["height", "weight_build", "body_ratio", "silhouette", "scale_refs"],
        )
        character_format = character_item["properties"]["output_format_requirements"]
        self.assertEqual(
            character_format["required"],
            [
                "master_card_background",
                "cutout_background",
                "required_views",
                "detail_crops",
                "scale_reference_required",
            ],
        )
        self.assertEqual(
            character_format["properties"]["cutout_background"]["const"],
            "transparent_alpha",
        )

        prop_item = prop_schema["properties"]["props"]["items"]
        self.assertIn("physical_dimensions", prop_item["required"])
        self.assertIn("output_format_requirements", prop_item["required"])
        self.assertEqual(
            prop_item["properties"]["physical_dimensions"]["required"],
            [
                "length",
                "width",
                "height",
                "scale_reference",
                "weight_feel",
                "material_thickness",
            ],
        )
        self.assertEqual(
            prop_item["properties"]["output_format_requirements"]["properties"][
                "master_card_background"
            ]["const"],
            "neutral_plain",
        )

        location_item = location_schema["properties"]["locations"]["items"]
        self.assertIn("output_format_requirements", location_item["required"])
        location_format = location_item["properties"]["output_format_requirements"]
        self.assertEqual(
            location_format["properties"]["composition_layers"]["required"],
            ["foreground", "midground", "background"],
        )
        self.assertEqual(
            location_format["properties"]["camera_requirements"]["required"],
            ["camera_distance", "camera_angle", "screen_direction", "light", "weather_time"],
        )

    def test_asset_card_prompt_reference_defines_required_templates(self) -> None:
        content = (
            SKILL_ROOT / "references" / "asset-card-prompt-templates.md"
        ).read_text(encoding="utf-8")

        expected_terms = (
            "Short Filename Rule",
            "Output Path Routing",
            "character_master_card",
            "character_episode_state_card",
            "prop_master_card",
            "prop_episode_state_card",
            "location_master_scene_card",
            "location_episode_scene_card",
            "production_metadata",
            "model_visible_prompt",
            "copy_ready",
            "Copy-Ready Prompt Fields",
            "Creation Dependencies",
            "body_metrics",
            "physical_dimensions",
            "output_format",
            "Image Output Format Contract",
            "background_policy",
            "alpha_policy",
            "transparent cutout",
            "foreground, midground, background",
            "video reference frame",
            "Never put `asset_id`, `episode_id`, `output_file`",
            "Six Visible Prompt Sections",
            "transparent PNG/SVG post-composite",
        )

        for term in expected_terms:
            self.assertIn(term, content)

    def test_asset_path_schemas_route_episode_cards_to_episode_directories(self) -> None:
        asset_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-manifest.schema.json").read_text(encoding="utf-8")
        )
        prompt_schema = json.loads(
            (SKILL_ROOT / "schemas" / "art-image-prompts.schema.json").read_text(
                encoding="utf-8"
            )
        )
        asset_index_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-index.schema.json").read_text(encoding="utf-8")
        )
        thread_schema = json.loads(
            (SKILL_ROOT / "schemas" / "thread-plan.schema.json").read_text(encoding="utf-8")
        )

        def assert_route(
            rules: list[dict],
            path_key: str,
            asset_type: str | None,
            asset_subtype: str,
            pattern: str,
        ) -> None:
            for rule in rules:
                condition = rule["if"]["properties"]
                type_matches = asset_type is None or condition.get("asset_type", {}).get(
                    "const"
                ) == asset_type
                subtype_matches = condition.get("asset_subtype", {}).get("const") == asset_subtype
                route_matches = rule["then"]["properties"][path_key]["pattern"] == pattern
                if type_matches and subtype_matches and route_matches:
                    return
            self.fail(f"Missing route for {asset_type}:{asset_subtype} -> {pattern}")

        route_expectations = (
            ("character", "character_master_card", "^assets/characters/"),
            ("character", "character_episode_state_card", "^[0-9]{2}/assets/characters/"),
            ("location", "location_master_scene_card", "^assets/locations/"),
            ("location", "location_episode_scene_card", "^[0-9]{2}/assets/locations/"),
            ("prop", "prop_master_card", "^assets/props/"),
            ("prop", "prop_episode_state_card", "^[0-9]{2}/assets/props/"),
            ("costume", "prop_master_card", "^assets/costumes/"),
            ("costume", "prop_episode_state_card", "^[0-9]{2}/assets/costumes/"),
        )

        manifest_item = asset_schema["properties"]["assets"]["items"]
        prompt_item = prompt_schema["properties"]["prompts"]["items"]
        index_item = asset_index_schema["properties"]["assets"]["items"]
        contract_item = thread_schema["properties"]["batches"]["items"]["properties"][
            "output_format_contracts"
        ]["items"]

        for asset_type, asset_subtype, pattern in route_expectations:
            assert_route(manifest_item["allOf"], "output_path", asset_type, asset_subtype, pattern)
            assert_route(prompt_item["allOf"], "output_path", asset_type, asset_subtype, pattern)
            assert_route(index_item["allOf"], "file_path", asset_type, asset_subtype, pattern)
            assert_route(contract_item["allOf"], "output_path", asset_type, asset_subtype, pattern)

        for rules, path_key in (
            (manifest_item["allOf"], "output_path"),
            (prompt_item["allOf"], "output_path"),
            (index_item["allOf"], "file_path"),
            (contract_item["allOf"], "output_path"),
        ):
            assert_route(
                rules,
                path_key,
                None,
                "reference_frame",
                "^[0-9]{2}/assets/reference-frames/",
            )
            assert_route(
                rules,
                path_key,
                None,
                "shot_override",
                "^[0-9]{2}/assets/shot-overrides/",
            )

    def test_thread_workflow_reference_uses_codex_thread_tools(self) -> None:
        content = (SKILL_ROOT / "references" / "thread-image-workflow.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("codex_app.create_thread", content)
        self.assertIn("codex_app.read_thread", content)
        self.assertIn("codex_app.send_message_to_thread", content)
        self.assertIn("{episode-id}/assets/characters/", content)
        self.assertIn("{episode-id}/assets/locations/", content)
        self.assertIn("{episode-id}/assets/props/", content)
        self.assertIn("{episode-id}/assets/costumes/", content)
        self.assertIn("{episode-id}/assets/reference-frames/", content)
        self.assertIn("Episode state cards", content)
        self.assertIn("output_format", content)
        self.assertIn("foreground, midground, and background", content)
        self.assertIn("Only current effective thread plan/result files", content)
        self.assertIn("runs/{run-id}/", content)

    def test_art_output_directory_discipline_routes_noncanonical_artifacts(self) -> None:
        skill_content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        contract_content = (SKILL_ROOT / "references" / "artifact-contract.md").read_text(
            encoding="utf-8"
        )

        for content in (skill_content, contract_content):
            self.assertIn("reports/", content)
            self.assertIn("audits/", content)
            self.assertIn("reviews/", content)
            self.assertIn("runs/{run-id}/", content)
            self.assertIn("*-audit*", content)
            self.assertIn("*-review*", content)
            self.assertIn("*-score*", content)

        for filename in (
            "asset-breakdown-agent.md",
            "image-prompt-agent.md",
            "thread-plan-agent.md",
            "asset-qc-agent.md",
        ):
            with self.subTest(filename=filename):
                content = (SKILL_ROOT / "agents" / filename).read_text(encoding="utf-8")
                self.assertIn("art root", content)
                routed_dirs = ("reports/", "audits/", "reviews/", "runs/{run-id}/")
                self.assertTrue(
                    any(term in content for term in routed_dirs)
                )

    def test_asset_versioning_keeps_only_final_outputs_canonical(self) -> None:
        skill_content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        workflow_content = (SKILL_ROOT / "references" / "thread-image-workflow.md").read_text(
            encoding="utf-8"
        )

        for content in (skill_content, workflow_content):
            self.assertIn("history/", content)
            self.assertIn(".v001", content)
            self.assertIn("version folders", content)

        for filename in (
            "asset-breakdown-agent.md",
            "image-prompt-agent.md",
            "thread-plan-agent.md",
            "asset-qc-agent.md",
        ):
            with self.subTest(filename=filename):
                content = (SKILL_ROOT / "agents" / filename).read_text(encoding="utf-8")
                self.assertIn("history/", content)
                self.assertIn(".v001", content)

    def test_asset_path_schemas_separate_final_and_history_files(self) -> None:
        asset_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-manifest.schema.json").read_text(encoding="utf-8")
        )
        thread_results_schema = json.loads(
            (SKILL_ROOT / "schemas" / "thread-results.schema.json").read_text(encoding="utf-8")
        )
        asset_index_schema = json.loads(
            (SKILL_ROOT / "schemas" / "asset-index.schema.json").read_text(encoding="utf-8")
        )

        output_path_schema = asset_schema["properties"]["assets"]["items"]["properties"][
            "output_path"
        ]
        output_path_guards = output_path_schema["allOf"]
        self.assertIn({"not": {"pattern": "(^|/)history/"}}, output_path_guards)
        self.assertIn(
            {"not": {"pattern": "(^|/)(v[0-9]+|versions?|drafts?)(/|$)"}},
            output_path_guards,
        )
        self.assertIn({"not": {"pattern": "\\.v[0-9]{3}\\.[^/]+$"}}, output_path_guards)

        thread_props = thread_results_schema["properties"]["threads"]["items"]["properties"]
        self.assertIn("history_files", thread_props)
        history_file_schema = thread_props["history_files"]["items"]
        self.assertIn({"pattern": "(^|/)history/"}, history_file_schema["allOf"])
        self.assertIn({"pattern": "\\.v[0-9]{3}\\.[^/]+$"}, history_file_schema["allOf"])

        index_props = asset_index_schema["properties"]["assets"]["items"]["properties"]
        self.assertIn("history_files", index_props)
        self.assertIn(
            "output_format",
            asset_index_schema["properties"]["assets"]["items"]["required"],
        )

    def test_openai_metadata_invokes_skill_name(self) -> None:
        content = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "Art Room"', content)
        self.assertIn("Use $art-room", content)

    def test_faction_hierarchy_guidance_is_generic(self) -> None:
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
        combined_content = "\n".join(
            (skill_content, character_content, style_content, prompt_content)
        )

        for content in (skill_content, character_content, style_content, prompt_content):
            self.assertIn("project inputs", content)
            self.assertIn("visual", content)

        self.assertIn("project-specific anatomy, culture, or lore", skill_content)
        self.assertIn("project-defined visual", character_content)
        self.assertIn("hierarchy drift", style_content)
        self.assertIn("generic descriptor set", prompt_content)

        for project_specific_term in ("Zerg", "insectoid", "虫族"):
            self.assertNotIn(project_specific_term, combined_content)


if __name__ == "__main__":
    unittest.main()
