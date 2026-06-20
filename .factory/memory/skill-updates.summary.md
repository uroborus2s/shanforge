# Skill Updates Summary

## 2026-06-20

- 已将“修 Bug 必须先定位根因，禁止用未验证兜底替代修复”沉淀为 bug 修复类 skill 的共同约束：`tdd-workflow` 新增 Bug 根因先于修复规则和根因记录模板；`ai-regression-testing` 新增 Bug 根因修复门槛，明确回归测试不是为兜底方案背书；`ai-first-engineering` 新增团队级 Bug 修复纪律；`python-uv-project` 新增 Python 调试/修复时的根因与防兜底规则。新增 `tests/test_bug_fix_root_cause_skill_rules.py` 固定这些约束，避免后续 skill 演进时丢失。

## 2026-06-14

- 新增 `skills/browser-control/`，作为中文 Codex skill 收口本地浏览器控制工作流。触发词覆盖“本地浏览器 / browser-use / 真实浏览器 / Codex Browser / Codex Chrome / 访问 URL / 截图 / 页面状态 / localhost 调试”；当用户明确要求“用本地浏览器访问 URL”时，默认优先使用 `browser-use --headed --session browser-control --json open <URL>`，再读取 `state` 确认 URL、标题、可见文本和元素索引。skill 同时写明 Codex Browser、Codex Chrome、Computer Use 的路由边界，以及表单提交、上传、cookies、登录态、权限和敏感信息的动作时确认规则。

## 2026-06-04

- 2026-06-07 补充：`art-room` 已修正分集资产状态卡的目录路由。项目级 `assets/characters|locations|props|costumes|style` 只放全剧母资产和全剧 style reference；`character_episode_state_card`、`prop_episode_state_card`、`location_episode_scene_card` 必须写入对应 `{episode-id}/assets/characters|locations|props|costumes`。`asset-manifest`、`art-image-prompts`、`asset-index` 和 `thread-plan.output_format_contracts` 现在都按 `asset_type + asset_subtype` 约束 canonical path，`c001e01` 这类分集状态卡不得再落入全局目录。
- 2026-06-06 补充：`art-room` 已新增输出目录纪律，防止审计和运行中间文件继续平铺到 `art/` 根目录。项目级 `art/` 根目录仅保留当前有效 `series-asset-plan.md / series-thread-plan.json / series-thread-results.json`；episode 级 `{episode-id}/art/` 根目录仅保留固定 handoff 文件。所有 `*-audit* / *-review* / *-score* / *-rewrite* / *-after-fix*`、重试诊断、worker scratch 和 run-specific 中间文件必须路由到 `reports/`、`audits/`、`reviews/` 或 `runs/{run-id}/`。
- 2026-06-05 补充：`art-room` 已新增强制 `output_format` 输出格式契约，覆盖 asset prep、asset manifest、art image prompts、thread plan 和 asset index/QC；字段包括 `deliverable_kind / file_format / minimum_resolution / background_policy / alpha_policy / canvas_aspect_ratio / required_views / composition_layers / qc_checks`。角色/物品/服装资产要求中性背景 master card、透明 alpha cutout、多视角 turnaround、detail crop 和尺度参考；视频 reference frame / shot override 要求 16:9 或项目定义画幅、alpha 禁用、foreground/midground/background 三层构图。`director-room` 的 ComfyUI asset prompt pack 现也必须保留 `output_format`，后续 shot prompt 与 prompt QC 必须拒绝把透明 cutout、neutral card、turnaround sheet 或 detail crop sheet 当作 I2V/FLF2V 场景帧。
- 2026-06-05 补充：`art-room` 已新增可直接提交给图片模型的 `copy_ready` 提示词契约，包含 `positive_prompt / negative_prompt / chatgpt_image_prompt / gemini_image_prompt`；资产准备和线程计划新增 `creation_order / creation_phase / depends_on_assets / blocks_assets / dependency_reason / priority`；角色卡 schema 新增 `body_metrics`，物品卡 schema 新增 `physical_dimensions`，用于资产审核时清楚查看创建顺序、依赖顺序、身高体态、比例、长宽高、重量感和材质厚度。
- 已按 `ai-drama-production-skill-system.md` 修改三间房 skill 本体与测试：`writer-room` 现支持全剧基础层、单集剧本、最终成片 canon 写回和旧项目故事迁移模式；`director-room` 现覆盖资产前分镜包、资产后视频生产包、render manifest、shot QC、edit decision list、AI TTS 对白计划、audio manifest 和 post/delivery QC；`art-room` 现覆盖全剧母资产、单集 asset prep、角色卡/物品卡/场景卡、短文件名、资产 prompt 的 `production_metadata` / `model_visible_prompt` 分层。
- 新增或扩展三间房 schema 与 reference：`director-room` 增加 video/render/QC/edit/audio/post schema 和 edit/audio/delivery agent cards；`art-room` 增加 `references/asset-card-prompt-templates.md`、资产卡设计 schema、`asset_subtype` 与短文件名约束；相关测试已扩展到新增路径、schema、QC 状态和提示词分层，并通过三间房定向回归、skill validator、ruff 与仓库全量 `pytest`。
- 已将独立 `prompt-room` 合并进 `director-room`：`director-room` 现在直接从 `./project/{project-name}/{episode-id}` 剧本包生成分镜、镜头清单、视觉连续性、generation plan、双语 shot prompt draft 和双语 ComfyUI-ready prompt pack。
- `director-room` 新增 prompt-engineering 阶段角色：prompt director、style preset、asset conditioning、shot prompt engineer、workflow parameter、prompt QC 与 ComfyUI feedback tuning；原独立 `skills/prompt-room/` 目录与 `tests/test_prompt_room_skill.py` 已移除。
- `director-room` 分镜说明契约固定包含中英双语结构：`基础设定 / Basic Setup`、`氛围和画质 / Atmosphere and Image Quality`、`画面内容 / Shot Panels`，每个镜头必须包含中英双语的景别、构图、运镜、画面内容、光线色彩和连续性锚点。
- JSON prompt 契约已改为双语字段：草案使用 `prompt_zh / prompt_en / negative_prompt_notes_zh / negative_prompt_notes_en`，最终 ComfyUI prompts 使用 `positive_prompt_zh / positive_prompt_en / negative_prompt_zh / negative_prompt_en`。
- 已移除 Codex 全局 `prompt-room` symlink，保留全局 `director-room` 作为统一入口；`art-room` 的后续 handoff 改为回到 `director-room` prompt refresh。

## 2026-06-03

- 已将 `skills/prompt-room/` 链接到 Codex 全局 skills：`/Users/uroborus/.codex/skills/prompt-room -> /Users/uroborus/AiProject/shanforge/skills/prompt-room`。
- `prompt-room` 本地 skill 通过 `python3 skills/skill-creator/scripts/quick_validate.py skills/prompt-room` 校验。

## 2026-06-01

- `writer-room`、`director-room`、`art-room` 的文档契约已统一到仓库根目录下的 `./project/{project-name}/`，跨集公共资料放在项目根，单集产物放在 `{episode-id}/`，例如 `01/`、`02/`。
- 新增 `skills/prompt-room/`，作为 Codex-native 提示词工程部，从共享生产项目根读取最终剧本、导演分镜产物和美术资产包，输出 ComfyUI-ready prompt、资产 conditioning、workflow 参数计划、QC 报告与调优日志。
- `prompt-room` 固定读取 `script/`、`bible/`、`director-brief.md`、`camera-plan.md`、`shots/`、`storyboard/`、`continuity/`、`production/generation-plan.json`、`prompts/shot-prompts-draft.json` 以及 `art/` / `prompts/art-image-prompts.json` / `art/asset-index.json`。
- `prompt-room` 固定写入 `prompts/comfyui-prompt-brief.md`、`prompts/comfyui-style-preset.json`、`prompts/comfyui-asset-prompt-pack.json`、`prompts/comfyui-shot-prompts.json`、`prompts/comfyui-workflow-plan.json`、`prompts/comfyui-tuning-log.json` 与 `reports/comfyui-prompt-qc.md`。
- 新增 7 个提示词工程角色任务卡：prompt director、style preset、asset conditioning、shot prompt engineer、workflow parameter、prompt QC 与 ComfyUI feedback tuning。
- 新增 `skills/art-room/`，作为 Codex-native 美术资产部，从共享生产项目根读取导演分镜产物，输出一致化角色、场景、道具、服装、风格和镜头参考图资产计划。
- `art-room` 固定从 `./project/{project-name}/` 读取项目级 `bible/characters.md`、`bible/scenes.md` 以及 `{episode-id}/` 下的剧本、导演分镜、镜头、storyboard、visual continuity、generation plan 和 draft prompts；固定写入 `{episode-id}/art/`、`{episode-id}/prompts/art-image-prompts.json`、项目级共享 `assets/` 图片目录和 `{episode-id}/assets/` 镜头参考目录。
- `art-room` 的图片生成边界固定为父协调器先生成 `{episode-id}/art/thread-plan.json`，再使用 `codex_app.create_thread` / `read_thread` / `send_message_to_thread` 调用后台 Codex thread 分批生成图片；规划 agent 不直接生成图片。
- 新增 9 个美术资产角色任务卡：art director、asset breakdown、character design、environment design、prop costume design、style continuity、image prompt、thread plan 与 asset QC。
- 新增 `skills/director-room/`，作为 Codex-native 导演分镜与镜头生产拆解部门，把标准化最终剧本包转换为视频生产清单。
- `writer-room` 项目目录契约改为 `./project/{project-name}/`：跨集资料固定写入 `outline/series-outline.md`、`synopsis/story-synopsis.md`、`bible/characters.md`、`bible/scenes.md`、`bible/continuity.md`，单集资料固定写入 `{episode-id}/script/final-script.md`、`{episode-id}/reports/continuity-report.md`、`{episode-id}/reports/script-score.md` 等路径。
- `director-room` 固定从同一个 `./project/{project-name}/` 读取项目级 `bible/` 与 `{episode-id}/script/`、`{episode-id}/reports/` 下的标准文件；若存在等价旧文件名，只允许在项目目录内归一化，不再创建独立 director-room 输入目录。
- skill 明确故事场景设计只负责故事层场景，不承担导演分镜与镜头生产拆解。
- 新增 8 个导演分镜角色任务卡：director、scene breakdown、shot planner、cinematographer、storyboard、visual continuity、generation strategy 与 shot prompt。
- 首版输出契约覆盖 `{episode-id}/shots/scene-breakdown.json`、`{episode-id}/shots/shot-list.json`、`{episode-id}/storyboard/storyboard-plan.md`、`{episode-id}/continuity/visual-continuity-bible.json`、`{episode-id}/production/generation-plan.json` 和 `{episode-id}/prompts/shot-prompts-draft.json`，并补齐 agent envelope 与 JSON schema。

## 2026-05-31

- 新增 `skills/writer-room/`，将编剧室从 Python 调度 LLM 的方案收口为 Codex-native skill。
- skill 明确主 Codex 线程作为制片主任 / 调度器，子 Codex agent 分别承担 showrunner、story architect、character、scene、dialogue、script doctor、rewrite、continuity、evaluator、memory librarian 与 learning evolution 职责。
- 新增 `agents/*.md` 角色任务卡、`references/` 调度与评分契约、`assets/templates/` 输出模板和 `schemas/` 结构化结果契约。
- 自我进化口径固定为先产出 `memory/evolution-notes.md` 和失败模式记录；修改 skill 本体前必须取得用户明确批准。

## 2026-05-02

- `skills/crawler4j-model-project/` 已对齐 `crawler4j 0.4.0` 的 `core-native-v2` 模块协议。
- skill 主体、references 与 `agents/openai.yaml` 现统一切到：
  - `crawler4j module init`
  - `interface/component/workflow/page-action/data/candidate/cleanup/page create`
  - `.crawler4j/manifest.lock.json`
  - `check structure/release/full`
  - `package build/verify`
  - `host devlink/install/debug config`
- 已显式标记旧叙事为迁移对象或禁用项：
  - `TaskScript`
  - `TaskFlow`
  - `TaskSpec`
  - `WorkflowSpec`
  - `module_runtime.py`
  - `env_selectors/`
  - `ui_extension`
  - `config_schema.json`
  - `crawler4j init-model`
  - `crawler4j new`
  - `crawler4j add-workflow`
  - `crawler4j add-ui`
- 新版 skill 也补上了宿主边界：目录源码只能走 `host devlink`，正式安装只走 ZIP 或 GitHub `owner/repo`，不把 `.whl` 当模块安装格式。
