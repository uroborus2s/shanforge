---
name: director-room
description: 导演部门与导演分镜部 AI 视频生产规划技能。用于从固定项目目录读取成稿剧本、角色设定、场景设定和连续性报告，组织导演、场景拆解、分镜、摄影、视觉连续性、场景控制包、生成策略、提示词、工作流参数、渲染质检、剪辑、音频与交付质检等员工子任务，循环评审直到各员工产物达标，并输出导演部门完整生产包和交给后续美术规划的场景图片资源包。当用户提到导演部门、导演分镜部、导演分镜、分镜说明、镜头设计、场景一致性、角色一致性、平面调度、场景母图、低模预演、深度图、线稿、机位图、ComfyUI 提示词、AI 视频渲染、AI 配音、剪辑或后期交付时使用。
---

# 导演部门

本技能把定稿剧本包转化为导演部门的可执行视频生产包。主协调代理只负责调度、依赖检查、质量评审、失败返工、文件装配和最终交付；具体创作、规划和质检由各员工子任务完成。

本技能不绑定特定运行平台。若运行环境支持子任务、子代理或多任务执行，各员工以子任务形式运行；若环境不支持，主协调代理按相同输入/输出契约顺序执行对应员工职责。不得为了本部门流程创建新的顶层项目、顶层线程或脱离当前项目根的任务空间。

## 部门职责

导演部门只关心自身输入、内部加工和输出。它不规定其他部门如何工作，也不引用其他 skill 的名称。

导演部门负责：

- 读取固定项目输入；
- 将剧本转化为场景、镜头、摄影、分镜、连续性、生成策略和提示词生产资产；
- 建立场景一致性所需的场景控制包；
- 输出可供视频生成、剪辑、音频、后期和交付质检使用的导演部门产物；
- 输出交给后续美术规划的场景图片资源包。

导演部门不负责：

- 改写剧本；
- 兼容任意旧目录或散文件；
- 替其他部门制定工作流；
- 用提示词掩盖缺失资产、缺失控制图或缺失配置；
- 在缺少必需输入时继续猜测。

## 项目输入

从单一项目根读取：

```text
./project/{project-name}/
```

运行 `{episode-id}` 前，以下文件必须存在。缺少任一项即报错并停止，返回 `blocked`，不得询问、推断、兼容或自动改名。

```text
bible/characters.md
bible/scenes.md
{episode-id}/script/final-script.md
{episode-id}/reports/continuity-report.md
{episode-id}/reports/script-score.md
production/series-video-rules.md
```

可选输入只在存在时读取；不存在不报错，但必须在交付摘要中说明未使用：

```text
bible/continuity.md
bible/visual-style.md
assets/asset-index.json
{episode-id}/assets/source-reference-index.json
{episode-id}/production/render-feedback.json
```

固定输入建立后，不得修改源剧本、角色设定、场景设定、连续性报告或评分报告。

## 员工子任务与模型选择

每个员工角色是当前部门流程内的子任务，不是新的顶层任务。子任务只接收本角色所需输入，只返回本角色 artifact envelope。

模型选择规则：

- 默认继承主协调代理所在运行环境的模型和权限。
- 若项目或运行环境显式提供 `role_model_profiles`，主协调代理可按该配置为员工子任务选择模型。
- 员工不得自行升级、切换或声明模型；缺少模型配置时写 `needs_config`，不伪造能力。
- 主协调代理不得为了模型选择改变项目输入、输出路径或质量门槛。

## 输出

必需的导演部门生产包：

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
{episode-id}/prompts/comfyui-prompt-brief.md
{episode-id}/prompts/comfyui-style-preset.json
{episode-id}/prompts/comfyui-asset-prompt-pack.json
{episode-id}/prompts/comfyui-shot-prompts.json
{episode-id}/prompts/comfyui-workflow-plan.json
{episode-id}/prompts/comfyui-render-prompts.md
{episode-id}/prompts/comfyui-tuning-log.json
{episode-id}/reports/comfyui-prompt-qc.md
```

必需的场景控制包：

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

必需的美术规划交接包：

```text
{episode-id}/handoff/art-planning/scene-image-brief.md
{episode-id}/handoff/art-planning/scene-image-resource-index.json
{episode-id}/handoff/art-planning/scene-reference-prompts.json
{episode-id}/assets/director-room/scenes/
{episode-id}/assets/director-room/scenes/SC###/master-reference-front.png
{episode-id}/assets/director-room/scenes/SC###/master-reference-reverse.png
{episode-id}/assets/director-room/scenes/SC###/key-prop-placement.png
{episode-id}/assets/director-room/scenes/SC###/blocking-overview.png
```

在渲染、剪辑、音频或交付阶段被请求时，生成以下产物：

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

调度与评审日志：

```text
{episode-id}/logs/director-room-agent-calls.jsonl
{episode-id}/reviews/director-room-review-ledger.json
{episode-id}/reviews/director-room-scorecard.md
```

## 员工输入与输出

主技能只列出员工的输入和输出；员工的具体方法、约束和返工重点写在各自角色卡内。

| 员工 | 输入 | 输出 |
| --- | --- | --- |
| `director-agent` | 标准必需输入 | `{episode-id}/director/director-brief.md` |
| `scene-breakdown-agent` | 场景设定、成稿剧本、连续性报告、导演阐述 | `{episode-id}/shots/scene-breakdown.json` |
| `visual-continuity-agent` | 角色设定、场景设定、成稿剧本、连续性报告、导演阐述 | `{episode-id}/continuity/visual-continuity-bible.json` |
| `shot-planner-agent` | 成稿剧本、场景拆解、导演阐述、视觉连续性圣经 | `{episode-id}/shots/shot-list.json` |
| `cinematographer-agent` | 导演阐述、场景拆解、分镜表、角色设定、场景设定 | `{episode-id}/director/camera-plan.md` |
| `storyboard-agent` | 导演阐述、分镜表、摄影方案、视觉连续性圣经 | `{episode-id}/storyboard/storyboard-plan.md` |
| `generation-strategy-agent` | 导演阐述、分镜表、摄影方案、分镜计划、视觉连续性圣经 | `{episode-id}/production/generation-plan.json`、`{episode-id}/production/video-production-plan.md` |
| `shot-prompt-agent` | 分镜表、摄影方案、分镜计划、视觉连续性圣经、生成计划 | `{episode-id}/prompts/shot-prompts-draft.json` |
| `prompt-director-agent` | 成稿剧本、角色设定、场景设定、导演阐述、摄影方案、分镜表、分镜计划、视觉连续性圣经、生成计划 | `{episode-id}/prompts/comfyui-prompt-brief.md` |
| `style-preset-agent` | 提示词简报、导演阐述、摄影方案、分镜计划、视觉连续性圣经、角色设定、场景设定 | `{episode-id}/prompts/comfyui-style-preset.json` |
| `asset-conditioning-agent` | 角色设定、场景设定、分镜表、视觉连续性圣经、生成计划、可选资产索引、场景控制素材 | `{episode-id}/prompts/comfyui-asset-prompt-pack.json` |
| `shot-prompt-engineer-agent` | 提示词简报、风格预设、资产条件包、提示词草稿、分镜表、摄影方案、分镜计划、生成计划、视觉连续性圣经 | `{episode-id}/prompts/comfyui-shot-prompts.json` |
| `workflow-parameter-agent` | 生成计划、最终镜头提示词、资产条件包、风格预设、分镜表 | `{episode-id}/prompts/comfyui-workflow-plan.json` |
| `prompt-qc-agent` | 提示词简报、风格预设、资产条件包、最终镜头提示词、工作流计划 | `{episode-id}/reports/comfyui-prompt-qc.md` |
| `scene-image-resource-agent` | 视觉连续性圣经、场景控制包、分镜计划、摄影方案、生成计划 | 美术规划交接包和场景图片资源索引 |
| `comfyui-feedback-agent` | 最终提示词、工作流计划、风格预设、资产条件包、渲染反馈 | `{episode-id}/prompts/comfyui-tuning-log.json`、`{episode-id}/qc/shot-qc-report.json` |
| `edit-planner-agent` | 分镜表、镜头质检、渲染登记、成稿剧本、最终提示词 | `{episode-id}/edit/edit-plan.md`、`{episode-id}/edit/edit-decision-list.json`、`{episode-id}/qc/episode-qc-report.md` |
| `audio-planner-agent` | 成稿剧本、剪辑方案、剪辑决定表、分镜表、可选字幕脚本 | 音频与字幕规划产物 |
| `delivery-qc-agent` | 镜头质检、剧集质检、剪辑决定表、音频清单、音频质检、字幕和声音计划 | 后期与交付质检产物 |

## 总工作流

主协调代理按依赖图调度员工子任务：

```text
输入校验
  -> director-agent
  -> scene-breakdown-agent + visual-continuity-agent
  -> shot-planner-agent
  -> cinematographer-agent
  -> storyboard-agent
  -> generation-strategy-agent
  -> shot-prompt-agent
  -> prompt-director-agent
  -> style-preset-agent + asset-conditioning-agent
  -> shot-prompt-engineer-agent
  -> workflow-parameter-agent
  -> prompt-qc-agent
  -> scene-image-resource-agent
  -> 可选：comfyui-feedback-agent / edit-planner-agent / audio-planner-agent / delivery-qc-agent
  -> 最终评分与交付
```

## 评审与返工循环

每个员工完成后，主协调代理必须立即评审其产物。评审未通过时，产物必须退回同一员工子任务重做，不得由主协调代理代写创作内容。

评审至少包含：

- schema 或结构检查；
- 必需字段和必需文件检查；
- 来源追溯检查；
- 与上游产物的一致性检查；
- 双语字段检查；
- 场景、角色、道具、站位和机位连续性检查；
- 员工专属评分量表。

评分规则：

- 每个员工产物满分 100 分。
- 默认通过线为 85 分；关键产物通过线为 90 分。关键产物包括视觉连续性圣经、分镜表、摄影方案、生成计划、最终提示词、工作流计划和场景图片资源交接包。
- 低于通过线时，主协调代理写明失败项、证据和返工要求，退回原员工。
- 循环持续到所有员工产物达到通过线。若运行预算、工具缺失或同一阻塞重复出现导致无法继续，整体状态为 `blocked`，不得降级为通过。

评审结果写入：

```text
{episode-id}/reviews/director-room-review-ledger.json
{episode-id}/reviews/director-room-scorecard.md
```

## 场景控制包原则

每个需要空间连续性的场景都应建立场景控制包。场景控制包不是泛泛的美术参考，而是让模型和制作人员反复核对的证据集。

- `scene-bible.md` 固定场景空间、材质、光源、道具、角色出入口和禁止变更项。
- `layout.yaml` 用坐标记录房间尺寸、门窗、家具、道具、角色站位、运动路径和机位。
- 场景母图固定美术气质、材质语言和光线基调，但不能替代平面调度。
- 平面调度图、机位图、深度图、线稿和 mask 应来自固定坐标或同一低模场景。
- 文生图可以用于场景母图和气氛探索，不能单独证明站位、道具和机位一致。

## 质量规则

- 保持剧本故事、人物意图和连续性。不得改写情节或新增故事节拍。
- 固定输入缺失时立即 `blocked`，不得兼容、推断、自动改名或继续生产。
- 镜头 ID 必须稳定且机器友好。除非项目已有更强约定，使用 `SC###-SH###`。
- 每个镜头必须有可见行动、明确主体、摄影方案、光线意图、连续性锚点和生成方法。
- 生产元数据必须与模型可见提示词分离。
- 精确空间连续性不得只靠文生图或形容词，应使用 `layout.yaml`、低模场景、平面调度图、机位图、深度图、线稿、mask、首帧或尾帧。
- 分镜和提示词产物必须双语。
- 不得发明 checkpoint ID、LoRA ID、ControlNet 模型名、IPAdapter 预设或节点模板 ID。
- 不要让视频模型生成精确对白；准确文本来自剧本、字幕和音频规划产物。
- 所有最终交付必须先通过评分循环。

## 最终回复

运行结束后，报告：

- 项目根和集 ID；
- 已创建的导演部门 artifact；
- 每个员工的最终评分和返工次数；
- 已创建的场景控制包；
- 已创建的场景图片资源和美术规划交接包；
- 仍需模型、配置、资产或控制图决策的镜头；
- 已执行的校验；
- 阻塞项或警告项。
