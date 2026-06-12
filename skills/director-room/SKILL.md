---
name: director-room
description: 面向 Codex 的导演分镜部与 AI 视频生产规划技能。用于从 ./project/{project-name}/{episode-id} 的成稿剧本、角色圣经和场景圣经出发，生成导演阐述、场景拆解、分镜表、摄影方案、视觉连续性圣经、场景控制包、ComfyUI 双语提示词包、工作流参数计划、渲染登记、质检报告、剪辑计划、AI 配音与后期交付方案。当用户提到导演分镜部、Director Room、分镜说明、镜头设计、场景一致性、角色一致性、平面调度、场景母图、Blender/Unreal 低模预演、深度图、线稿、机位图、ComfyUI 提示词、AI 视频渲染、AI 配音、剪辑或后期交付时使用。
---

# 导演分镜部

本技能用于把已经定稿的剧本包转化为可执行的视频生产包。父级 Codex 实例担任总导演、制片统筹和提示词总监：先核验项目输入，再组织各角色卡执行分工，最后汇总、校验并写入项目产物。

本技能特别处理 AI 视频制作中的一致性问题。它不把“一致性”寄托在单条提示词上，而是要求建立可复用的场景证据：场景圣经、平面调度、场景母图、低模场景、机位图、深度图、线稿、遮罩、首尾关键帧和 ComfyUI 条件输入。视频模型负责生成画面，空间、站位和镜头约束由这些证据共同锁定。

## 部门边界

故事场景设计不属于导演分镜部的首要职责。上游应当已经给出地点、戏剧目的、可见行动和基本可拍性。本技能负责把这些材料整理成生产单位：场景、镜头、双语分镜面板、视觉连续性锁点、场景控制包、生成方法、提示词草稿、ComfyUI 双语提示词和后期交付文件。

本技能同时承担原“提示词工程”职责。同一集不再另行调用独立的 prompt-room。提示词产物必须从成稿剧本、导演方案、摄影方案、分镜、视觉连续性、场景控制包和生成策略中推导。已有 art-room 资产可以使用，但第一次从剧本到提示词的生产规划不得以 art-room 资产为前置条件。

默认流水线：

```text
创作简报
  -> 成稿剧本包
  -> director-room 前资产分镜包
  -> 场景控制包和低模预演计划
  -> art-room 资产
  -> director-room 后资产视频生产包
  -> ComfyUI 生产
  -> director-room 渲染质检 / 剪辑 / AI 配音 / 后期交付
```

## 运行模型

- 把 Codex 视为运行时。不得另写 Python agent loop，也不得让项目 LLM provider 代替 Codex 子代理执行部门角色。
- 父级协调器在可用时使用 `multi_agent_v1.spawn_agent`。只有当用户明确要求 Codex 原生部门制或多代理分镜工作流时，才启动子代理。
- 子代理只执行一个角色卡。子代理不得再次要求 `spawn_agent`，也不得擅自修改共享文件；它只返回结构化 artifact envelope。
- 父级协调器负责输入核验、编排、文件写入、结构校验、质量门禁和向用户提出必要问题。
- 子代理只接收完成本角色所需的 artifact 文本和角色卡，避免把整个项目无差别塞入上下文。
- 若父级协调器没有子代理工具，应明确说明“每个角色均由 Codex 子代理执行”的要求暂时受阻，并询问是否继续采用父级单代理模拟。

## 项目输入

从单一项目根读取：

```text
./project/{project-name}/
```

对 `{episode-id}` 运行前，必须核验以下标准文件：

```text
bible/characters.md
bible/scenes.md
{episode-id}/script/final-script.md
{episode-id}/reports/continuity-report.md
{episode-id}/reports/script-score.md
```

如果用户给出的项目目录使用等价旧名称，应在同一项目目录内归一到上述固定路径。不得创建脱离项目根的 director-room 输入目录，也不得把零散文件视为默认输入。若某类必需来源缺失且无法安全推断，只问一个简洁问题。固定输入建立后，不得修改源剧本、角色圣经和场景圣经。

可选项目级输入：

```text
bible/continuity.md
bible/visual-style.md
production/series-video-rules.md
assets/asset-index.json
```

系列搭建阶段若缺少 `production/series-video-rules.md`，应先创建该文件。该文件固定画幅、帧率、镜头风格、运动限制、质量下限、禁止的视觉/声音选择、渲染反馈格式，以及 AI 音频和后期规则。

## 场景控制包

每个需要保持空间连续性的场景，都应建立场景控制包。它不是美术参考图的集合，而是供下游模型反复查验的生产证据。

推荐目录：

```text
{episode-id}/control/
  scene-packages/
    SC###/
      scene-bible.md
      layout.yaml
      master-reference-front.png
      master-reference-reverse.png
      blockout-plan.md
      top-view.png
      camera-map.png
      shot-guides/
      depth/
      lineart/
      masks/
```

各素材职责如下：

- `scene-bible.md`：固定场景空间、材质、光源、道具、角色出入口和禁止变更项。
- `layout.yaml`：用坐标记录房间尺寸、门窗、家具、道具、角色站位、运动路径和机位；这是空间连续性的事实源。
- 场景母图：固定美术气质、材质语言和光线基调；它不能替代平面调度。
- 平面调度图：从 `layout.yaml` 或同一个低模场景导出，用于锁定人物、道具和摄影机相对位置。
- 低模场景：可由 Blender 或 Unreal 建立。所有镜头应从同一低模场景导出机位图、深度图、线稿和遮罩。
- 深度图、线稿、机位图：作为 ComfyUI ControlNet、IP-Adapter、参考图、首尾帧和重绘流程的条件输入。

原则：文生图可以用于探索场景母图，不能单独承担空间一致性。生产级一致性来自固定坐标、低模场景和可复现导出。

## 输出

必需的前资产部门交付：

```text
{episode-id}/director/director-brief.md
{episode-id}/director/camera-plan.md
{episode-id}/shots/scene-breakdown.json
{episode-id}/shots/shot-list.json
{episode-id}/storyboard/storyboard-plan.md
{episode-id}/continuity/visual-continuity-bible.json
{episode-id}/production/generation-plan.json
{episode-id}/production/video-production-plan.md
{episode-id}/prompts/shot-prompts-draft.json
```

必需的场景控制交付：

```text
{episode-id}/control/scene-packages/
{episode-id}/control/scene-packages/SC###/scene-bible.md
{episode-id}/control/scene-packages/SC###/layout.yaml
{episode-id}/control/scene-packages/SC###/blockout-plan.md
{episode-id}/control/scene-packages/SC###/top-view.png
{episode-id}/control/scene-packages/SC###/camera-map.png
{episode-id}/control/scene-packages/SC###/shot-guides/
{episode-id}/control/scene-packages/SC###/depth/
{episode-id}/control/scene-packages/SC###/lineart/
{episode-id}/control/scene-packages/SC###/masks/
```

必需的后资产视频生产交付：

```text
{episode-id}/prompts/comfyui-prompt-brief.md
{episode-id}/prompts/comfyui-style-preset.json
{episode-id}/prompts/comfyui-asset-prompt-pack.json
{episode-id}/prompts/comfyui-shot-prompts.json
{episode-id}/prompts/comfyui-workflow-plan.json
{episode-id}/prompts/comfyui-render-prompts.md
{episode-id}/prompts/comfyui-tuning-log.json
{episode-id}/reports/comfyui-prompt-qc.md
```

在用户请求渲染、剪辑、音频或下游反馈存在时，生成以下产物：

```text
{episode-id}/production/render-manifest.json
{episode-id}/qc/shot-qc-report.json
{episode-id}/qc/episode-qc-report.md
{episode-id}/edit/edit-plan.md
{episode-id}/edit/edit-decision-list.json
{episode-id}/audio/voice-bible.md
{episode-id}/audio/dialogue-plan.json
{episode-id}/audio/audio-manifest.json
{episode-id}/audio/audio-qc.md
{episode-id}/audio/dialogue/
{episode-id}/audio/sfx/
{episode-id}/audio/music/
{episode-id}/post/post-production-plan.md
{episode-id}/post/subtitle-script.md
{episode-id}/post/sound-plan.md
{episode-id}/post/color-plan.md
{episode-id}/post/delivery-qc-report.md
```

协调器辅助输出：

```text
{episode-id}/logs/director-room-agent-calls.jsonl
```

## 参考文件

按需加载，不要一次性读取无关材料：

- `references/artifact-contract.md`：子代理返回 envelope 和 artifact 的规则。
- `references/department-workflow.md`：子代理启动、并行、上下文切片、恢复和文件写入规则。
- `references/comfyui-prompting-guide.md`：双语提示词结构、生成方法映射、控制图输入、JSON 上下文传递、参数计划和反馈调优规则。
- `agents/*.md`：每个子代理的角色卡。不得把 `agents/openai.yaml` 当作角色卡。
- `schemas/*.json`：JSON 产物和测试使用的结构契约。

## 工作流程

1. 核验项目根和五个标准输入文件。必要时在同一项目目录内归一旧路径。系列搭建阶段若缺少 `production/series-video-rules.md`，先创建该文件。
2. 运行 `director-agent`，生成 `{episode-id}/director/director-brief.md`。
3. 运行 `scene-breakdown-agent` 和 `visual-continuity-agent`。导演阐述存在后，两者可以并行。
4. `visual-continuity-agent` 必须识别需要场景控制包的场景，定义场景圣经、平面调度、道具锁点、角色站位和低模导出需求。
5. 在 `{episode-id}/shots/scene-breakdown.json` 存在后运行 `shot-planner-agent`。
6. 在 `{episode-id}/shots/shot-list.json` 存在后运行 `cinematographer-agent`，生成机位、镜头轴线、焦段、运动、景深和光线方案。
7. 根据视觉连续性和摄影方案，为每个高一致性风险场景补齐场景控制包计划：`layout.yaml`、`blockout-plan.md`、`top-view.png`、`camera-map.png`、shot guide、depth、lineart 和 masks 的导出清单。
8. 在摄影方案和视觉连续性圣经存在后运行 `storyboard-agent`。
9. 在分镜表、摄影方案、分镜计划和视觉连续性圣经存在后运行 `generation-strategy-agent`。它必须决定每个镜头使用 `T2V`、`I2V`、`FLF2V`、`REFERENCE_IMAGE` 或 `REDRAW`，并说明是否需要首帧、尾帧、参考图、ControlNet 深度图、线稿、OpenPose、mask 或低模导出。
10. 在 `{episode-id}/production/generation-plan.json` 存在后运行 `shot-prompt-agent`。
11. 创建或更新 `{episode-id}/production/video-production-plan.md` 作为前资产视频生产计划，未解决的资产、模型、工作流和控制图依赖必须显式标记。
12. art-room 资产存在后，读取 `assets/asset-index.json`、`{episode-id}/art/asset-index.json`、`{episode-id}/art/asset-qc-report.md`、`{episode-id}/prompts/art-image-prompts.json` 和标准图像路径，并保留每个资产的 `output_format`；随后运行 `prompt-director-agent`，生成 `{episode-id}/prompts/comfyui-prompt-brief.md`。
13. 运行 `style-preset-agent` 和 `asset-conditioning-agent`。提示词简报存在后，两者可以并行。
14. 在提示词简报、风格预设、资产条件包、镜头提示词草稿、分镜表、摄影方案、分镜计划、视觉连续性圣经和生成计划齐备后，运行 `shot-prompt-engineer-agent`。
15. 在 `{episode-id}/prompts/comfyui-shot-prompts.json` 存在后运行 `workflow-parameter-agent`。该角色必须把参考图、首尾帧、ControlNet 深度图、线稿、OpenPose、mask、LoRA、IPAdapter 和输出路径写入 node binding hints；不得伪造未验证的节点模板。
16. 从风格预设和镜头提示词记录组装 `{episode-id}/prompts/comfyui-render-prompts.md`。该 Markdown 是给 ComfyUI 操作者复制使用的交付面，必须为每个镜头提供完整的 `positive_prompt_zh`、`negative_prompt_zh`、`positive_prompt_en` 和 `negative_prompt_en`。不得要求操作者手工拼接 JSON 字段。
17. 更新 `{episode-id}/production/video-production-plan.md` 为后资产视频生产计划，写明具体资产引用、控制图输入、渲染顺序、风险和未解决配置占位符。
18. 运行 `prompt-qc-agent`，生成 `{episode-id}/reports/comfyui-prompt-qc.md`。
19. 若存在 ComfyUI 渲染反馈，运行 `comfyui-feedback-agent`；否则仍写入 `{episode-id}/prompts/comfyui-tuning-log.json`，并设置 `status="no_feedback"`。
20. 渲染输出存在后，登记 `{episode-id}/production/render-manifest.json`，并在 `{episode-id}/qc/shot-qc-report.json` 中分类每个镜头。
21. 存在可接受镜头后，运行 `edit-planner-agent`，生成 `{episode-id}/edit/edit-plan.md` 和 `{episode-id}/edit/edit-decision-list.json`。
22. 运行 `audio-planner-agent`，规划 AI 配音、字幕、音效和音乐。音频按对白行、旁白行、音效 cue 和音乐 cue 管理，不按“每个镜头一个音频文件”管理。
23. 运行 `delivery-qc-agent`，生成后期计划、剧集质检、音频质检和交付质检产物。
24. 在可行时用本地 schema 校验 JSON 输出。只修复格式错误；不得在修复 JSON 时发明新的故事事实。
25. 向用户返回输出路径、警告、未解决模型/资产/控制图依赖，以及推荐的 ComfyUI 生产交接方式。

## 子代理顺序

使用以下角色卡：

```text
agents/director-agent.md
agents/scene-breakdown-agent.md
agents/shot-planner-agent.md
agents/cinematographer-agent.md
agents/storyboard-agent.md
agents/visual-continuity-agent.md
agents/generation-strategy-agent.md
agents/shot-prompt-agent.md
agents/prompt-director-agent.md
agents/style-preset-agent.md
agents/asset-conditioning-agent.md
agents/shot-prompt-engineer-agent.md
agents/workflow-parameter-agent.md
agents/prompt-qc-agent.md
agents/comfyui-feedback-agent.md
agents/edit-planner-agent.md
agents/audio-planner-agent.md
agents/delivery-qc-agent.md
```

## 质量规则

- 保持剧本故事、人物意图和连续性。不得改写情节、增加新情节拍，或通过修改剧本来掩盖分镜问题。
- 镜头 ID 必须稳定且机器友好。除非项目已有更强约定，使用 `SC###-SH###`。
- 每个镜头必须可拍：有可见行动、明确主体、摄影方案、光线意图、音频说明、连续性锚点和生成方法。
- 前资产分镜包与后资产视频生产包必须分离。`shot-prompts-draft` 是给 art-room 和后续提示词工程使用的中间产物；最终 `comfyui-*` 提示词产物必须在资产质检后生成。
- 必须显式选择生成方法：`T2V`、`I2V`、`FLF2V`、`REFERENCE_IMAGE` 或 `REDRAW`，并写明理由和所需资产。
- 场景一致性优先于孤立镜头美观。角色外观、服装、道具、地理关系、轴线、光线和场景布局必须在相邻镜头中保持连贯。
- 精确空间连续性不得只靠文生图或形容词。需要锁定站位、道具和机位时，应使用 `layout.yaml`、低模场景、平面调度图、机位图、深度图、线稿、mask、首帧或尾帧。
- 生产元数据必须与模型可见提示词分离。`shot_id`、`generation_method`、`asset_id`、`episode_id`、`output_file` 和 workflow 标识属于元数据，不得写入模型可见提示词正文。
- ComfyUI 交付必须同时提供结构化提示词记录和可复制提示词 Markdown。`comfyui-shot-prompts.json` 是结构化事实源；`comfyui-render-prompts.md` 是派生的操作交付面。
- 使用 art-room 资产时必须尊重 `output_format`。中性母卡、转面图和细节图只作身份、尺度、材质和连续性参考；透明抠图用于 mask、叠加、合成或局部重绘；只有 `video_reference_frame` 和 `shot_override_frame` 可作为 I2V/FLF2V 的完整场景首帧、尾帧或参考帧。可作场景帧的参考图必须清楚呈现前景、中景、背景。不得把透明抠图或孤立卡片当成场景帧。
- 明显不可能、成本过高或含糊的镜头必须标记风险，不能藏进提示词。
- QC 状态必须机器可读：`accepted`、`needs_redraw`、`needs_regenerate`、`needs_prompt_tuning`、`needs_asset_fix`、`needs_script_fix`、`needs_audio_fix` 或 `blocked`。
- 分镜和提示词产物必须双语。人类可读的分镜区块应有中文和英文标签/内容；JSON 提示词记录必须包含中文和英文字段，不得只在备注中翻译。
- 不得发明 checkpoint ID、LoRA ID、ControlNet 模型名、IPAdapter 预设或节点模板 ID。只能使用用户或项目提供的 ID；缺失时写明确占位符，并把镜头标为 `needs_config`。
- 给子代理或模型调用传递 JSON 时，小文件完整传递；大文件按场景或镜头族切片，并保留全局摘要和 `source_refs`。
- 不要让视频模型生成精确对白。视频提示词可以描述说话状态、轻微口型、呼吸和表演意图；准确文本来自 `script/final-script.md`、`post/subtitle-script.md` 和 `audio/dialogue-plan.json`。
- 音频使用短文件名，例如 `audio/dialogue/d001.wav`、`audio/sfx/sfx001.wav`、`audio/music/mx001.wav`。废弃 take 应进入历史记录，并由 `audio/audio-manifest.json` 建索引。

## 最终回复

运行结束后，向用户报告：

- director-room 项目根
- 已创建的 artifact
- 阻塞项或警告项
- 已创建的双语提示词产物
- 已创建的可复制 ComfyUI 渲染提示词 Markdown
- 已创建或待补的场景控制包、平面调度、低模导出、深度图、线稿、机位图和 mask
- 仍需模型、配置、资产或控制图决策的镜头
- 已执行的校验
- 推荐的 ComfyUI 生产交接方式
