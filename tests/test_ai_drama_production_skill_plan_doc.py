from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = (
    REPO_ROOT
    / "docs"
    / "04-project-development"
    / "04-design"
    / "ai-drama-production-skill-system.md"
)


def test_ai_drama_production_plan_doc_exists_and_defines_three_skill_boundary() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    assert "writer-room" in content
    assert "director-room" in content
    assert "art-room" in content
    assert "不新增第四个 `post-room`" in content
    assert "不生成图像资产" in content
    assert "不改故事 canon" in content
    assert "不改剧本" in content


def test_ai_drama_production_plan_doc_defines_shared_project_layout() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_paths = (
        "project/{project-name}/",
        "production/series-video-rules.md",
        "art/series-asset-plan.md",
        "assets/asset-index.json",
        "production/video-production-plan.md",
        "art/asset-prep-plan.md",
        "production/render-manifest.json",
        "qc/shot-qc-report.json",
        "edit/edit-decision-list.json",
        "audio/dialogue-plan.json",
        "audio/audio-manifest.json",
        "post/delivery-qc-report.md",
        "legacy/",
        "migration/migration-map.json",
        "migration/backfill-plan.md",
        "migration/migration-report.md",
        "memory/failure-patterns.json",
    )

    for expected_path in expected_paths:
        assert expected_path in content


def test_ai_drama_production_plan_doc_defines_revision_and_handoff_rules() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_terms = (
        "方案修订规范",
        "正式文件修改规则",
        "canonical 文件",
        "handoff lock",
        "render lock",
        "Revision Log",
        "revision_log",
        "owner skill 修复 canonical 文件",
        "不含扩展名，不超过 20 个字符",
    )

    for expected_term in expected_terms:
        assert expected_term in content

    assert "分镜 v0" not in content
    assert "提示词刷新 v1" not in content


def test_ai_drama_production_plan_doc_defines_generation_and_reading_handoffs() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_terms = (
        "环节生成与下游读取清单",
        "全剧基础创建",
        "资产前导演分镜包",
        "单集前置资产",
        "资产后视频生产包",
        "ComfyUI 渲染登记",
        "镜头 QC 与修复分流",
        "AI 配音与声音",
        "经验写回",
        "下一环节固定读取",
    )

    for expected_term in expected_terms:
        assert expected_term in content


def test_ai_drama_production_plan_doc_defines_prompt_asset_audio_rules() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_terms = (
        "结构化提示词格式",
        "角色卡提示词",
        "物品卡提示词",
        "场景卡提示词",
        "视频制作提示词",
        "ComfyUI 资产使用原则",
        "旗帜、徽章和精细物品一致性",
        "长镜头处理",
        "AI 配音和后期方案",
        "不建议让视频模型直接一次性生成带精准对白的视频",
        "AI TTS",
        "audio/voice-bible.md",
        "needs_audio_fix",
        "生产元数据",
        "模型可见提示词",
        "对白不按每个分镜逐条创建",
        "3 分钟视频的简单工作量估算",
    )

    for expected_term in expected_terms:
        assert expected_term in content

    forbidden_model_prompt_terms = (
        "- 输出文件短名",
        "- shot_id",
        "- 生成方式：T2V / I2V / FLF2V / REDRAW",
        "- 使用资产短名",
    )

    for forbidden_term in forbidden_model_prompt_terms:
        assert forbidden_term not in content


def test_ai_drama_production_plan_doc_defines_prompt_examples_and_migration() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_terms = (
        "角色卡完整示例",
        "物品卡完整示例",
        "场景卡完整示例",
        "视频制作完整示例",
        "生产元数据用于流程追踪，不进入模型正文",
        "生产元数据用于资产索引和 ComfyUI 条件引用，不进入模型正文",
        "旧项目迁移方案",
        "legacy/",
        "migration/migration-map.json",
        "migration/backfill-plan.md",
        "migration/migration-report.md",
        "保守迁移",
        "快速迁移",
        "下游只读取 canonical 文件，不能继续读取 `legacy/`",
    )

    for expected_term in expected_terms:
        assert expected_term in content

    assert "旧提示词不能原样继承" in content
    assert "必须拆成生产元数据和模型可见提示词两层" in content


def test_ai_drama_production_plan_doc_defines_detailed_skill_development_plan() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")

    expected_terms = (
        "Skill 修改开发计划",
        "阶段 0：冻结方案契约",
        "阶段 1：修改 writer-room",
        "阶段 2：修改 director-room 的导演与视频生产契约",
        "阶段 3：修改 art-room",
        "阶段 4：修改 director-room 的 AI 配音与后期能力",
        "阶段 5：端到端试点验证",
        "开发顺序",
        "writer-room 不声明图像资产、视频渲染或音频生产职责",
        "comfyui-shot-prompts.json 分成 production metadata 和 model-visible prompt",
        "asset-card-prompt-templates.md",
        "dialogue-plan.schema.json",
        "第一版落地范围",
        "暂不要求",
    )

    for expected_term in expected_terms:
        assert expected_term in content


def test_ai_drama_production_plan_doc_is_indexed() -> None:
    design_index = (
        REPO_ROOT / "docs" / "04-project-development" / "04-design" / "index.md"
    ).read_text(encoding="utf-8")
    document_index = (
        REPO_ROOT
        / "docs"
        / "04-project-development"
        / "10-traceability"
        / "document-index.md"
    ).read_text(encoding="utf-8")
    doc_map = (REPO_ROOT / ".factory" / "memory" / "doc-map.md").read_text(
        encoding="utf-8"
    )

    assert "ai-drama-production-skill-system.md" in design_index
    assert "ai-drama-production-skill-system.md" in document_index
    assert "ai-drama-production-skill-system.md" in doc_map
