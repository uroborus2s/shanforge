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
    "scene-image-resource-agent.md",
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
    "production/series-video-rules.md",
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
    "{episode-id}/handoff/art-planning/scene-image-brief.md",
    "{episode-id}/handoff/art-planning/scene-image-resource-index.json",
    "{episode-id}/handoff/art-planning/scene-reference-prompts.json",
    "{episode-id}/handoff/art-planning/shot-image-task-list.json",
    "{episode-id}/assets/director-room/scenes/",
    "{episode-id}/assets/director-room/shots/",
    "{episode-id}/assets/director-room/shots/SC###-SH###/shot-scene-image.png",
    "{episode-id}/assets/director-room/shots/SC###-SH###/director-reference.png",
    "{episode-id}/reports/director-room-final-report.md",
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
        self.assertNotIn("面向 Codex", frontmatter)
        self.assertNotIn("TODO", content)
        self.assertIn("本技能不绑定特定运行平台", content)
        self.assertIn("每个员工角色是当前部门流程内的子任务", content)
        self.assertIn("./project/{project-name}/", content)
        self.assertIn("{episode-id}", content)
        self.assertIn("缺少任一项即报错并停止", content)
        self.assertIn("不得询问、推断、兼容或自动改名", content)
        self.assertIn("role_model_profiles", content)
        self.assertIn("shot-prompts-draft", content)
        self.assertIn("分镜和提示词产物必须双语", content)
        self.assertIn("production/series-video-rules.md", content)
        self.assertIn("主技能只列出员工的输入和输出", content)
        self.assertIn("评审与返工循环", content)
        self.assertIn("默认通过线为 85 分", content)
        self.assertIn("关键产物通过线为 90 分", content)
        self.assertIn("scene-image-resource-agent", content)
        self.assertIn("美术规划交接包", content)
        self.assertIn("scene-image-resource-index.json", content)
        self.assertIn("不要让视频模型生成精确对白", content)
        self.assertIn("layout.yaml", content)
        self.assertIn("低模场景", content)
        self.assertIn("深度图", content)
        self.assertIn("线稿", content)
        self.assertIn("场景控制包", content)
        self.assertIn("最终综合中文报告", content)
        self.assertIn(
            "所有输出文档、结构化文件、控制包、图片资源目录、逐镜头图片任务单及其作用",
            content,
        )
        self.assertIn("每个员工最终产物的审查分析、最终评分、通过线、返工次数", content)
        self.assertIn("缺少该报告时，导演部门不得标记为完成", content)
        self.assertIn("镜头规划和分镜规划必须服务于连续性", content)
        self.assertIn("必须一次性整体处理本集所有场景与镜头", content)
        self.assertIn("单镜头场景图和导演参考图必须拆成独立任务", content)
        self.assertIn("shot-image-task-list.json", content)

        for path in REQUIRED_INPUTS + REQUIRED_OUTPUTS:
            self.assertIn(path, content)

        self.assertNotIn("inputs/final-script.md", content)

    def test_skill_keeps_story_owner_boundary(self) -> None:
        combined_content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".json"}
        )

        lowered = combined_content.lower()
        self.assertNotIn("skills/writer-room", lowered)
        self.assertNotIn("art-room", lowered)
        self.assertNotIn("writer room", lowered)
        self.assertNotIn("prompt-room", lowered)
        self.assertIn("needs_script_fix", combined_content)
        self.assertIn("脚本源文件需要修订", combined_content)
        self.assertIn("固定必需输入缺失时", combined_content)

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
            "scene-image-resource-index.schema.json",
            "scene-reference-prompts.schema.json",
            "shot-image-task-list.schema.json",
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

    def test_scene_image_resource_handoff_contract_is_explicit(self) -> None:
        resource_schema = json.loads(
            (SKILL_ROOT / "schemas" / "scene-image-resource-index.schema.json").read_text(
                encoding="utf-8"
            )
        )
        prompt_schema = json.loads(
            (SKILL_ROOT / "schemas" / "scene-reference-prompts.schema.json").read_text(
                encoding="utf-8"
            )
        )
        task_schema = json.loads(
            (SKILL_ROOT / "schemas" / "shot-image-task-list.schema.json").read_text(
                encoding="utf-8"
            )
        )
        agent_card = (SKILL_ROOT / "agents" / "scene-image-resource-agent.md").read_text(
            encoding="utf-8"
        )

        resource_item = resource_schema["properties"]["resources"]["items"]
        prompt_item = prompt_schema["properties"]["prompts"]["items"]
        task_item = task_schema["properties"]["tasks"]["items"]
        for field in (
            "resource_id",
            "scene_id",
            "resource_type",
            "target_path",
            "status",
            "usage",
            "continuity_locks",
            "source_refs",
        ):
            self.assertIn(field, resource_item["required"])
        resource_types = resource_item["properties"]["resource_type"]["enum"]
        self.assertIn("master_reference_front", resource_types)
        self.assertIn("blocking_overview", resource_item["properties"]["resource_type"]["enum"])
        self.assertIn("shot_scene_image", resource_types)
        self.assertIn("director_reference_image", resource_types)
        self.assertIn("prompt_zh", prompt_item["required"])
        self.assertIn("prompt_en", prompt_item["required"])
        for field in (
            "task_id",
            "shot_id",
            "scene_id",
            "task_type",
            "target_path",
            "status",
            "input_refs",
            "control_refs",
            "continuity_locks",
            "forbidden_changes",
        ):
            self.assertIn(field, task_item["required"])
        task_types = task_item["properties"]["task_type"]["enum"]
        self.assertIn("shot_scene_image", task_types)
        self.assertIn("director_reference_image", task_types)
        self.assertIn("每个任务只处理一个镜头的一类图片资源", agent_card)
        self.assertIn("不得把整集、整场或多个镜头合并为一个出图任务", agent_card)
        self.assertIn("每个镜头必须至少有一个单镜头场景图或导演参考图任务", agent_card)
        self.assertIn("场景图片资源包是关键产物，通过线为 90 分", agent_card)

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
        self.assertIn("每个员工是当前导演部门流程中的子任务", workflow)
        self.assertIn("默认继承主协调代理所在运行环境的模型", workflow)
        self.assertIn("评审循环", workflow)
        self.assertIn("评分未达标时", workflow)
        self.assertIn("镜头和分镜必须先整体连续规划，再拆分图片执行任务", workflow)
        self.assertIn("单镜头场景图和导演参考图必须拆成独立任务", workflow)
        self.assertIn("最终综合中文报告", workflow)
        self.assertIn("每个输出文档的作用", workflow)
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
        owner_fix = qc_schema["properties"]["shots"]["items"]["properties"]["owner_fix"]["enum"]
        self.assertIn("image-asset-source", owner_fix)
        self.assertIn("script-source", owner_fix)
        self.assertNotIn("art-room", owner_fix)
        self.assertNotIn("writer-room", owner_fix)

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
        self.assertIn("调用 director-room", content)
        self.assertIn("场景图片资源包", content)


if __name__ == "__main__":
    unittest.main()
