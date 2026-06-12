---
name: director-room
description: 导演部门与导演分镜部 AI 视频生产规划和工作室执行技能。用于从固定项目目录读取成稿剧本、角色设定、场景设定和连续性报告，组织导演、场景拆解、分镜、摄影、视觉连续性、平面调度坐标、场景控制包、低模预演、工具执行、生成策略、提示词、工作流参数、渲染质检、剪辑、音频与交付质检等员工子任务，循环评审直到各员工产物达标，并输出导演部门完整生产包、场景图片资源、逐镜头图片生成任务单、实际工具执行清单和最终综合中文报告。当用户提到导演部门、导演分镜部、导演工作室、分镜说明、镜头设计、场景一致性、角色一致性、平面调度、场景母图、低模预演、Blender、Krita、GIMP、ComfyUI、深度图、线稿、机位图、AI 生图、AI 视频渲染、AI 配音、剪辑或后期交付时使用。
---

# 导演部门

本技能把定稿剧本包转化为导演部门的可执行视频生产包。主协调代理负责调度、依赖检查、工具能力检查、质量评审、失败返工、用户反馈返工、文件装配和最终交付；具体创作、规划、工具执行和质检由各员工子任务完成。

本技能不绑定特定运行平台。若运行环境支持子任务、子代理或多任务执行，各员工以子任务形式运行；若环境不支持，主协调代理按相同输入/输出契约顺序执行对应员工职责。不得为了本部门流程创建新的顶层项目、顶层线程或脱离当前项目根的任务空间。

## 部门职责

导演部门只关心自身输入、内部加工和输出。它不规定其他部门如何工作，也不引用其他 skill 的名称。

导演部门负责：

- 读取固定项目输入；
- 将剧本转化为场景、镜头、摄影、分镜、连续性、生成策略和提示词生产资产；
- 建立平面调度坐标和 `layout.yaml`，把场景空间、角色站位、道具位置、运动路径和机位坐标固定下来；
- 建立场景一致性所需的场景控制包；
- 在运行环境提供工具时，调用可用图像生成能力、Blender、ComfyUI、Krita、GIMP 或桌面自动化，把低模场景、顶视图、机位图、导演视角图、深度图、线稿、mask、场景母图和逐镜头参考图实际产出；
- 输出可供视频生成、剪辑、音频、后期和交付质检使用的导演部门产物；
- 输出交给后续美术规划的场景图片资源包、逐镜头图片生成任务单和最终综合中文报告。

导演部门不负责：

- 改写剧本；
- 兼容任意旧目录或散文件；
- 替其他部门制定工作流；
- 用提示词掩盖缺失资产、缺失控制图或缺失配置；
- 假定 Photoshop 必然存在，或把 Photoshop 作为必需工具；
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
production/tool-profiles.json
{episode-id}/reviews/human-feedback.md
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
{episode-id}/control/scene-packages/SC###/blockout.blend
{episode-id}/control/scene-packages/SC###/blockout-export-manifest.json
{episode-id}/control/scene-packages/SC###/top-view.png
{episode-id}/control/scene-packages/SC###/camera-map.png
{episode-id}/control/scene-packages/SC###/shot-guides/
{episode-id}/control/scene-packages/SC###/shot-guides/SC###-SH###.png
{episode-id}/control/scene-packages/SC###/depth/
{episode-id}/control/scene-packages/SC###/lineart/
{episode-id}/control/scene-packages/SC###/masks/
```

工作室执行产物：

```text
{episode-id}/production/tool-capability-report.json
{episode-id}/production/studio-execution-manifest.json
```

必需的美术规划交接包：

```text
{episode-id}/handoff/art-planning/scene-image-brief.md
{episode-id}/handoff/art-planning/scene-image-resource-index.json
{episode-id}/handoff/art-planning/scene-reference-prompts.json
{episode-id}/handoff/art-planning/shot-image-task-list.json
{episode-id}/assets/director-room/scenes/
{episode-id}/assets/director-room/scenes/SC###/master-reference-front.png
{episode-id}/assets/director-room/scenes/SC###/master-reference-reverse.png
{episode-id}/assets/director-room/scenes/SC###/key-prop-placement.png
{episode-id}/assets/director-room/scenes/SC###/blocking-overview.png
{episode-id}/assets/director-room/shots/
{episode-id}/assets/director-room/shots/SC###-SH###/shot-scene-image.png
{episode-id}/assets/director-room/shots/SC###-SH###/director-reference.png
```

最终人类审阅报告：

```text
{episode-id}/reports/director-room-final-report.md
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
{episode-id}/reviews/human-feedback-log.jsonl
{episode-id}/reviews/feedback-revision-plan.json
```

## 员工输入与输出

主技能只列出员工的输入和输出；员工的具体方法、约束和返工重点写在各自角色卡内。

| 员工 | 输入 | 输出 |
| --- | --- | --- |
| `director-agent` | 标准必需输入 | `{episode-id}/director/director-brief.md` |
| `scene-breakdown-agent` | 场景设定、成稿剧本、连续性报告、导演阐述 | `{episode-id}/shots/scene-breakdown.json` |
| `visual-continuity-agent` | 角色设定、场景设定、成稿剧本、连续性报告、导演阐述 | `{episode-id}/continuity/visual-continuity-bible.json` |
| `shot-planner-agent` | 成稿剧本、场景拆解、导演阐述、视觉连续性圣经 | `{episode-id}/shots/shot-list.json` |
| `scene-coordinate-agent` | 场景拆解、视觉连续性圣经、分镜表、场景设定 | `{episode-id}/control/scene-packages/SC###/layout.yaml`、`scene-bible.md`、`blockout-plan.md` |
| `cinematographer-agent` | 导演阐述、场景拆解、分镜表、角色设定、场景设定、场景坐标包 | `{episode-id}/director/camera-plan.md` |
| `storyboard-agent` | 导演阐述、分镜表、摄影方案、视觉连续性圣经 | `{episode-id}/storyboard/storyboard-plan.md` |
| `generation-strategy-agent` | 导演阐述、分镜表、摄影方案、分镜计划、视觉连续性圣经 | `{episode-id}/production/generation-plan.json`、`{episode-id}/production/video-production-plan.md` |
| `shot-prompt-agent` | 分镜表、摄影方案、分镜计划、视觉连续性圣经、生成计划 | `{episode-id}/prompts/shot-prompts-draft.json` |
| `prompt-director-agent` | 成稿剧本、角色设定、场景设定、导演阐述、摄影方案、分镜表、分镜计划、视觉连续性圣经、生成计划 | `{episode-id}/prompts/comfyui-prompt-brief.md` |
| `style-preset-agent` | 提示词简报、导演阐述、摄影方案、分镜计划、视觉连续性圣经、角色设定、场景设定 | `{episode-id}/prompts/comfyui-style-preset.json` |
| `asset-conditioning-agent` | 角色设定、场景设定、分镜表、视觉连续性圣经、生成计划、可选资产索引、场景控制素材 | `{episode-id}/prompts/comfyui-asset-prompt-pack.json` |
| `shot-prompt-engineer-agent` | 提示词简报、风格预设、资产条件包、提示词草稿、分镜表、摄影方案、分镜计划、生成计划、视觉连续性圣经 | `{episode-id}/prompts/comfyui-shot-prompts.json` |
| `workflow-parameter-agent` | 生成计划、最终镜头提示词、资产条件包、风格预设、分镜表 | `{episode-id}/prompts/comfyui-workflow-plan.json` |
| `prompt-qc-agent` | 提示词简报、风格预设、资产条件包、最终镜头提示词、工作流计划 | `{episode-id}/reports/comfyui-prompt-qc.md` |
| `scene-image-resource-agent` | 视觉连续性圣经、场景控制包、分镜计划、摄影方案、生成计划 | 美术规划交接包、场景图片资源索引和逐镜头图片任务单 |
| `studio-tool-execution-agent` | 场景控制包、逐镜头图片任务单、最终提示词、工作流计划、工具配置、可选人工反馈 | 工具能力报告、工作室执行清单和实际图片/控制图产物 |
| `user-feedback-triage-agent` | 人工反馈、评审账本、最终报告、相关产物清单 | `{episode-id}/reviews/feedback-revision-plan.json`、`{episode-id}/reviews/human-feedback-log.jsonl` |
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
  -> scene-coordinate-agent
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
  -> studio-tool-execution-agent
  -> 可选：comfyui-feedback-agent / edit-planner-agent / audio-planner-agent / delivery-qc-agent
  -> 可选：user-feedback-triage-agent -> 受影响员工返工 -> studio-tool-execution-agent
  -> 最终评分、综合中文报告与交付
```

## 工作室执行模式

导演部门可以作为总工作室完成规划和实际资产产出，但必须先确认工具能力，再执行，不得假装工具已经完成工作。

- 可调用运行环境提供的图像生成能力，用于场景母图、气氛探索、导演参考图和逐镜头参考图。
- 可调用 Blender 或等价 3D 工具，根据 `layout.yaml` 建立低模场景，导出顶视图、机位图、导演视角图、深度图、线稿、mask 和低模工程文件。
- 可调用 ComfyUI 或等价节点式生成环境，执行可复现的图像、控制图和视频生成工作流。
- 可调用 Krita、GIMP 或等价图像编辑工具，执行遮罩清理、抠图、局部修正、色彩统一、分层整理和输出格式整理。
- 不得把 Photoshop 作为必需工具；只有在 `production/tool-profiles.json` 明确配置 Photoshop 时，才可把它列为可选执行工具。
- ComfyUI 不是导演规划的必需条件；若用户要求本地可复现批量生成而 ComfyUI 不可用，相关任务必须写为 `needs_config` 或 `blocked`。
- Krita 和 GIMP 已安装时，优先作为修图、mask、抠图和资产清理工具；它们不替代 `layout.yaml` 或低模场景的空间证明作用。

工具能力检查结果写入：

```text
{episode-id}/production/tool-capability-report.json
```

实际执行、失败、返工和输出路径写入：

```text
{episode-id}/production/studio-execution-manifest.json
```

若工具不可用，主协调代理仍可完成规划和任务单，但不得把未生成图片标记为 `ready`。

## 镜头与分镜连续规划

镜头规划和分镜规划必须服务于连续性，而不是拆成孤立镜头逐条猜测。

- `shot-planner-agent` 必须一次性整体处理本集所有场景与镜头，建立稳定镜头 ID、镜头顺序、空间方向、轴线关系、角色站位、道具状态、入画出画和相邻镜头衔接。
- `storyboard-agent` 必须基于完整分镜表一次性整体处理本集分镜，不得把每个镜头交给彼此隔离的任务分别规划。
- 主协调代理评审分镜表和分镜计划时，必须检查前后镜头的场景、角色、道具、站位、动作方向、视线方向、光线状态和机位关系。
- 只有在整体镜头表和整体分镜计划通过评审后，才能进入逐镜头图片资源任务拆分。

逐镜头出图任务必须拆分，以免单个任务过长，但拆分不得破坏连续性：

- 单镜头场景图和导演参考图必须拆成独立任务；每个镜头至少有一个可追踪的图片生成任务记录。
- 每个图片任务必须引用同一套上游连续性依据：`shot-list.json`、`storyboard-plan.md`、`camera-plan.md`、`visual-continuity-bible.json`、对应 `scene-packages/SC###/layout.yaml`、机位图、深度图、线稿或 mask。
- 逐镜头任务只负责生成或整理本镜头的场景输出图、导演参考图或控制图，不得重新设计场景空间、角色站位、道具位置或镜头顺序。
- 逐镜头任务清单写入 `{episode-id}/handoff/art-planning/shot-image-task-list.json`，供后续逐项执行、返工和追踪。

## 平面调度坐标

`layout.yaml` 是平面调度坐标的权威来源。导演部门可以先依据剧本、场景设定和分镜规划起草坐标，再用低模场景和导出图验证坐标。

`layout.yaml` 至少记录：

- 坐标原点、单位、轴向、场景尺寸和比例；
- 墙体、门窗、楼梯、固定家具、可移动道具和关键光源；
- 角色在每个镜头的起点、终点、朝向、视线方向和运动路径；
- 摄影机位置、镜头朝向、高度、焦段、视角、运动轨迹和轴线关系；
- 每个镜头的导演视角图、深度图、线稿和 mask 对应路径；
- 禁止改变的空间关系、道具状态和连续性锁点。

若用户审核认为空间不对，返工必须优先修改 `layout.yaml` 和低模场景，再重新导出图像，不得只改提示词。

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
- 用户人工审核不通过时，主协调代理必须记录反馈、定位受影响产物和员工、退回对应员工或工具执行任务返工，直到用户反馈被解决或进入 `blocked`。

评审结果写入：

```text
{episode-id}/reviews/director-room-review-ledger.json
{episode-id}/reviews/director-room-scorecard.md
{episode-id}/reviews/human-feedback-log.jsonl
{episode-id}/reviews/feedback-revision-plan.json
```

## 最终综合中文报告

所有员工产物通过评审后，主协调代理必须生成一份供人类查看的综合性中文 Markdown 文件：

```text
{episode-id}/reports/director-room-final-report.md
```

该报告不得只是日志转写，必须用清晰中文说明：

- 本次导演部门运行的项目根、集 ID、输入文件、可选输入使用情况和阻塞条件；
- 所有输出文档、结构化文件、控制包、图片资源目录、逐镜头图片任务单及其作用；
- 每个员工最终产物的审查分析、最终评分、通过线、返工次数、未通过原因摘要和最终状态；
- 场景控制包如何支撑场景母图、平面调度、机位图、深度图、线稿、mask 和逐镜头参考图；
- 镜头与分镜如何一次性整体规划，逐镜头图片任务如何拆分执行；
- 实际使用了哪些工具，哪些图已经真实生成，哪些图仍是计划、配置缺失或阻塞；
- 用户审核意见如何被处理，哪些产物经历了返工，哪些反馈仍未关闭；
- 已通过校验、仍需人工或外部工具决策的事项、警告项、风险项和交接建议。

最终报告是必需交付物。缺少该报告时，导演部门不得标记为完成。

## 场景控制包原则

每个需要空间连续性的场景都应建立场景控制包。场景控制包不是泛泛的美术参考，而是让模型和制作人员反复核对的证据集。

- `scene-bible.md` 固定场景空间、材质、光源、道具、角色出入口和禁止变更项。
- `layout.yaml` 用坐标记录房间尺寸、门窗、家具、道具、角色站位、运动路径和机位。
- 场景母图固定美术气质、材质语言和光线基调，但不能替代平面调度。
- 平面调度图、机位图、深度图、线稿和 mask 应来自固定坐标或同一低模场景。
- 文生图可以用于场景母图和气氛探索，不能单独证明站位、道具和机位一致。
- 低模场景、坐标文件和导出图发生冲突时，以 `layout.yaml` 和重新验证后的低模场景为准。

## 质量规则

- 保持剧本故事、人物意图和连续性。不得改写情节或新增故事节拍。
- 固定输入缺失时立即 `blocked`，不得兼容、推断、自动改名或继续生产。
- 镜头 ID 必须稳定且机器友好。除非项目已有更强约定，使用 `SC###-SH###`。
- 每个镜头必须有可见行动、明确主体、摄影方案、光线意图、连续性锚点和生成方法。
- 生产元数据必须与模型可见提示词分离。
- 精确空间连续性不得只靠文生图或形容词，应使用 `layout.yaml`、低模场景、平面调度图、机位图、深度图、线稿、mask、首帧或尾帧。
- 生图、ComfyUI、Blender、Krita、GIMP 或桌面自动化输出必须记录工具、输入、输出路径、状态和失败原因。
- 分镜和提示词产物必须双语。
- 不得发明 checkpoint ID、LoRA ID、ControlNet 模型名、IPAdapter 预设或节点模板 ID。
- 不要让视频模型生成精确对白；准确文本来自剧本、字幕和音频规划产物。
- 所有最终交付必须先通过评分循环。

## 最终回复

运行结束后，报告：

- 项目根和集 ID；
- 最终综合中文报告路径；
- 已创建的导演部门 artifact；
- 每个员工的最终评分和返工次数；
- 已创建的场景控制包；
- 已创建的场景图片资源和美术规划交接包；
- 已执行的工具、生成的低模场景、顶视图、机位图、导演视角图、深度图、线稿、mask、场景母图和逐镜头参考图；
- 用户审核反馈的处理状态；
- 仍需模型、配置、资产或控制图决策的镜头；
- 已执行的校验；
- 阻塞项或警告项。
