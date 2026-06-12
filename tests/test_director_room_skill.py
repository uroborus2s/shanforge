from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "director-room"

ROLE_CARDS = (
    "director-agent.md",
    "scene-breakdown-agent.md",
    "shot-planner-agent.md",
    "cinematographer-agent.md",
    "storyboard-agent.md",
    "visual-continuity-agent.md",
    "generation-strategy-agent.md",
    "shot-prompt-agent.md",
    "prompt-director-agent.md",
    "style-preset-agent.md",
    "asset-conditioning-agent.md",
    "shot-prompt-engineer-agent.md",
    "workflow-parameter-agent.md",
    "prompt-qc-agent.md",
    "comfyui-feedback-agent.md",
    "edit-planner-agent.md",
    "audio-planner-agent.md",
    "delivery-qc-agent.md",
)

REQUIRED_INPUTS = (
    "bible/characters.md",
    "bible/scenes.md",
    "{episode-id}/script/final-script.md",
    "{episode-id}/reports/continuity-report.md",
    "{episode-id}/reports/script-score.md",
)

REQUIRED_OUTPUTS = (
    "{episode-id}/director/director-brief.md",
    "{episode-id}/director/camera-plan.md",
    "{episode-id}/shots/scene-breakdown.json",
    "{episode-id}/shots/shot-list.json",
    "{episode-id}/storyboard/storyboard-plan.md",
    "{episode-id}/continuity/visual-continuity-bible.json",
    "{episode-id}/production/generation-plan.json",
    "{episode-id}/production/video-production-plan.md",
    "{episode-id}/prompts/shot-prompts-draft.json",
    "{episode-id}/control/scene-packages/",
    "{episode-id}/control/scene-packages/SC###/layout.yaml",
    "{episode-id}/control/scene-packages/SC###/top-view.png",
    "{episode-id}/control/scene-packages/SC###/camera-map.png",
    "{episode-id}/control/scene-packages/SC###/depth/",
    "{episode-id}/control/scene-packages/SC###/lineart/",
    "{episode-id}/control/scene-packages/SC###/masks/",
    "{episode-id}/prompts/comfyui-prompt-brief.md",
    "{episode-id}/prompts/comfyui-style-preset.json",
    "{episode-id}/prompts/comfyui-asset-prompt-pack.json",
    "{episode-id}/prompts/comfyui-shot-prompts.json",
    "{episode-id}/prompts/comfyui-workflow-plan.json",
    "{episode-id}/prompts/comfyui-render-prompts.md",
    "{episode-id}/prompts/comfyui-tuning-log.json",
    "{episode-id}/reports/comfyui-prompt-qc.md",
    "{episode-id}/production/render-manifest.json",
    "{episode-id}/qc/shot-qc-report.json",
    "{episode-id}/qc/episode-qc-report.md",
    "{episode-id}/edit/edit-plan.md",
    "{episode-id}/edit/edit-decision-list.json",
    "{episode-id}/audio/voice-bible.md",
    "{episode-id}/audio/dialogue-plan.json",
    "{episode-id}/audio/audio-manifest.json",
    "{episode-id}/audio/audio-qc.md",
    "{episode-id}/audio/dialogue/",
    "{episode-id}/audio/sfx/",
    "{episode-id}/audio/music/",
    "{episode-id}/post/post-production-plan.md",
    "{episode-id}/post/subtitle-script.md",
    "{episode-id}/post/sound-plan.md",
    "{episode-id}/post/color-plan.md",
    "{episode-id}/post/delivery-qc-report.md",
)


class DirectorRoomSkillTests(unittest.TestCase):
    def test_skill_frontmatter_and_body_define_project_input_boundary(self) -> None:
        content = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---", 2)[1]
        self.assertIn("name: director-room", frontmatter)
        self.assertIn("导演分镜部", frontmatter)
        self.assertIn("场景一致性", frontmatter)
        self.assertNotIn("TODO", content)
        self.assertIn("故事场景设计不属于导演分镜部的首要职责", content)
        self.assertIn("./project/{project-name}/", content)
        self.assertIn("{episode-id}", content)
        self.assertIn("不得创建脱离项目根的 director-room 输入目录", content)
        self.assertIn("不得另写 Python agent loop", content)
        self.assertIn("shot-prompts-draft", content)
        self.assertIn("不再另行调用独立的 prompt-room", content)
        self.assertIn("分镜和提示词产物必须双语", content)
        self.assertIn("小文件完整传递", content)
        self.assertIn("production/series-video-rules.md", content)
        self.assertIn("前资产分镜包", content)
        self.assertIn("后资产视频生产包", content)
        self.assertIn("output_format", content)
        self.assertIn("透明抠图", content)
        self.assertIn("前景、中景、背景", content)
        self.assertIn("不要让视频模型生成精确对白", content)
        self.assertIn("layout.yaml", content)
        self.assertIn("低模场景", content)
        self.assertIn("深度图", content)
        self.assertIn("线稿", content)
        self.assertIn("场景控制包", content)

        for path in REQUIRED_INPUTS + REQUIRED_OUTPUTS:
            self.assertIn(path, content)

        self.assertNotIn("inputs/final-script.md", content)

    def test_skill_keeps_story_owner_boundary(self) -> None:
        combined_content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".json"}
        )

        self.assertNotIn("skills/writer-room", combined_content.lower())
        self.assertIn("needs_script_fix", combined_content)
        self.assertIn("不要在后期文件中修故事问题", combined_content)

    def test_all_role_cards_exist_with_artifact_contracts(self) -> None:
        for filename in ROLE_CARDS:
            with self.subTest(filename=filename):
                content = (SKILL_ROOT / "agents" / filename).read_text(encoding="utf-8")

                self.assertIn("## 使命", content)
                self.assertIn("## 输入", content)
                self.assertIn("## 必需产物", content)
                self.assertIn("## Artifact 契约", content)
                self.assertNotIn("TODO", content)

    def test_references_and_schemas_are_present(self) -> None:
        expected_references = (
            "artifact-contract.md",
            "comfyui-prompting-guide.md",
            "department-workflow.md",
        )
        expected_schemas = (
            "agent-result.schema.json",
            "scene-breakdown.schema.json",
            "shot-list.schema.json",
            "visual-continuity-bible.schema.json",
            "generation-plan.schema.json",
            "shot-prompts-draft.schema.json",
            "comfyui-style-preset.schema.json",
            "comfyui-asset-prompt-pack.schema.json",
            "comfyui-shot-prompts.schema.json",
            "comfyui-workflow-plan.schema.json",
            "comfyui-tuning-log.schema.json",
            "video-production-plan.schema.json",
            "render-manifest.schema.json",
            "shot-qc-report.schema.json",
            "episode-qc-report.schema.json",
            "edit-decision-list.schema.json",
            "post-production-plan.schema.json",
            "delivery-qc-report.schema.json",
            "dialogue-plan.schema.json",
            "audio-manifest.schema.json",
            "audio-qc.schema.json",
        )

        for filename in expected_references:
            self.assertTrue((SKILL_ROOT / "references" / filename).exists())
        for filename in expected_schemas:
            payload = json.loads((SKILL_ROOT / "schemas" / filename).read_text(encoding="utf-8"))
            self.assertIn("title", payload)
            self.assertIn("type", payload)

    def test_generation_method_contract_is_explicit(self) -> None:
        generation_schema = json.loads(
            (SKILL_ROOT / "schemas" / "generation-plan.schema.json").read_text(encoding="utf-8")
        )
        prompt_schema = json.loads(
            (SKILL_ROOT / "schemas" / "shot-prompts-draft.schema.json").read_text(
                encoding="utf-8"
            )
        )

        expected_methods = ["T2V", "I2V", "FLF2V", "REFERENCE_IMAGE", "REDRAW"]
        shot_item = generation_schema["properties"]["shots"]["items"]
        prompt_item = prompt_schema["properties"]["prompts"]["items"]

        self.assertEqual(shot_item["properties"]["method"]["enum"], expected_methods)
        self.assertEqual(prompt_item["properties"]["generation_method"]["enum"], expected_methods)
        self.assertIn("required_assets", shot_item["required"])
        self.assertIn("segment_id", shot_item["required"])
        self.assertIn("duration", shot_item["required"])
        self.assertIn("fps", shot_item["required"])
        self.assertIn("aspect_ratio", shot_item["required"])
        self.assertIn("control_inputs", shot_item["properties"])
        control_role = shot_item["properties"]["control_inputs"]["items"]["properties"]["role"]
        self.assertIn("depth", control_role["enum"])
        self.assertIn("lineart", control_role["enum"])
        self.assertIn("first_frame", control_role["enum"])
        self.assertIn("continuity_refs", prompt_item["required"])
        self.assertIn("prompt_zh", prompt_item["required"])
        self.assertIn("prompt_en", prompt_item["required"])
        self.assertIn("negative_prompt_notes_zh", prompt_item["required"])
        self.assertIn("negative_prompt_notes_en", prompt_item["required"])

    def test_scene_control_package_contract_is_explicit(self) -> None:
        visual_schema = json.loads(
            (SKILL_ROOT / "schemas" / "visual-continuity-bible.schema.json").read_text(
                encoding="utf-8"
            )
        )
        workflow_schema = json.loads(
            (SKILL_ROOT / "schemas" / "comfyui-workflow-plan.schema.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertIn("scene_control_packages", visual_schema["properties"])
        package_item = visual_schema["properties"]["scene_control_packages"]["items"]
        self.assertIn("layout_source", package_item["required"])
        self.assertIn("required_control_outputs", package_item["required"])
        outputs = package_item["properties"]["required_control_outputs"]["items"]["enum"]
        for expected in ("top_view", "camera_map", "depth", "lineart", "mask"):
            self.assertIn(expected, outputs)

        workflow_item = workflow_schema["properties"]["shots"]["items"]
        self.assertIn("control_inputs", workflow_item["properties"])
        roles = workflow_item["properties"]["control_inputs"]["items"]["properties"]["role"][
            "enum"
        ]
        for expected in (
            "ipadapter_reference",
            "controlnet_depth",
            "controlnet_lineart",
            "openpose",
            "mask",
        ):
            self.assertIn(expected, roles)

    def test_bilingual_comfyui_prompt_contract_is_explicit(self) -> None:
        prompt_schema = json.loads(
            (SKILL_ROOT / "schemas" / "comfyui-shot-prompts.schema.json").read_text(
                encoding="utf-8"
            )
        )
        style_schema = json.loads(
            (SKILL_ROOT / "schemas" / "comfyui-style-preset.schema.json").read_text(
                encoding="utf-8"
            )
        )
        asset_pack_schema = json.loads(
            (SKILL_ROOT / "schemas" / "comfyui-asset-prompt-pack.schema.json").read_text(
                encoding="utf-8"
            )
        )

        prompt_item = prompt_schema["properties"]["shots"]["items"]
        style_item = style_schema["properties"]["style_profiles"]["items"]

        self.assertIn("production_metadata", prompt_item["required"])
        self.assertIn("model_visible_prompt", prompt_item["required"])
        metadata_required = prompt_item["properties"]["production_metadata"]["required"]
        visible_required = prompt_item["properties"]["model_visible_prompt"]["required"]
        for field in (
            "episode_id",
            "shot_id",
            "segment_id",
            "generation_method",
            "duration",
            "fps",
            "aspect_ratio",
            "asset_refs",
            "audio_refs",
            "workflow_hint",
            "source_refs",
            "continuity_refs",
        ):
            self.assertIn(field, metadata_required)
        for field in (
            "visible_goal_zh",
            "visible_goal_en",
            "style_quality_zh",
            "style_quality_en",
            "subject_content_zh",
            "subject_content_en",
            "composition_motion_zh",
            "composition_motion_en",
            "visible_continuity_zh",
            "visible_continuity_en",
            "negative_prompt_zh",
            "negative_prompt_en",
        ):
            self.assertIn(field, visible_required)
        self.assertIn("global_positive_prefix_zh", style_item["required"])
        self.assertIn("global_positive_prefix_en", style_item["required"])
        self.assertIn("global_negative_zh", style_item["required"])
        self.assertIn("global_negative_en", style_item["required"])

        asset_item = asset_pack_schema["properties"]["assets"]["items"]
        self.assertIn("output_format", asset_item["required"])
        output_format = asset_pack_schema["$defs"]["output_format"]
        self.assertIn("transparent_alpha", output_format["properties"]["background_policy"]["enum"])
        self.assertIn("video_frame", output_format["properties"]["background_policy"]["enum"])
        self.assertEqual(
            output_format["properties"]["composition_layers"]["required"],
            ["foreground", "midground", "background"],
        )

    def test_storyboard_template_and_json_context_rules_are_documented(self) -> None:
        storyboard_card = (SKILL_ROOT / "agents" / "storyboard-agent.md").read_text(
            encoding="utf-8"
        )
        guide = (SKILL_ROOT / "references" / "comfyui-prompting-guide.md").read_text(
            encoding="utf-8"
        )
        workflow = (SKILL_ROOT / "references" / "department-workflow.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("1. 基础设定 / Basic Setup", storyboard_card)
        self.assertIn("2. 氛围和画质 / Atmosphere and Image Quality", guide)
        self.assertIn("3. 画面内容 / Shot Panels", guide)
        self.assertIn("控制图需求 / Control Inputs", guide)
        self.assertIn("JSON 文件不会自动完整发送", workflow)
        self.assertIn("小型 JSON artifact 可完整传递", workflow)
        self.assertIn("production_metadata", guide)
        self.assertIn("model_visible_prompt", guide)
        self.assertIn("美术资产输出格式", guide)
        self.assertIn("透明抠图", guide)
        self.assertIn("前景、中景、背景", guide)
        self.assertIn("视频模型可以被告知角色处于说话", guide)
        self.assertIn("场景控制输入", guide)

    def test_qc_edit_and_audio_contracts_are_explicit(self) -> None:
        qc_schema = json.loads(
            (SKILL_ROOT / "schemas" / "shot-qc-report.schema.json").read_text(encoding="utf-8")
        )
        edit_schema = json.loads(
            (SKILL_ROOT / "schemas" / "edit-decision-list.schema.json").read_text(
                encoding="utf-8"
            )
        )
        dialogue_schema = json.loads(
            (SKILL_ROOT / "schemas" / "dialogue-plan.schema.json").read_text(
                encoding="utf-8"
            )
        )

        expected_qc = [
            "accepted",
            "needs_redraw",
            "needs_regenerate",
            "needs_prompt_tuning",
            "needs_asset_fix",
            "needs_script_fix",
            "needs_audio_fix",
            "blocked",
        ]
        self.assertEqual(
            qc_schema["properties"]["shots"]["items"]["properties"]["status"]["enum"],
            expected_qc,
        )

        edit_item = edit_schema["properties"]["items"]["items"]
        self.assertIn("audio_refs", edit_item["required"])

        dialogue_item = dialogue_schema["properties"]["dialogue_lines"]["items"]
        for field in (
            "dialogue_id",
            "speaker",
            "text",
            "emotion",
            "target_duration",
            "linked_shots",
            "output_file",
        ):
            self.assertIn(field, dialogue_item["required"])

    def test_openai_metadata_invokes_skill_name(self) -> None:
        content = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")

        self.assertIn('display_name: "导演分镜部"', content)
        self.assertIn("使用 $director-room", content)
        self.assertIn("分镜、场景控制包和双语 ComfyUI", content)


if __name__ == "__main__":
    unittest.main()
