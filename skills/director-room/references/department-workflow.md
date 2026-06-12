# 导演部门调度工作流

主协调代理是唯一调度者。员工子任务不得继续派生员工，不得向用户发问，不得写共享文件；只返回 artifact envelope。

## 子任务与顶层任务

- 每个员工是当前导演部门流程中的子任务。
- 不创建新的顶层项目、顶层线程或脱离当前项目根的新任务空间。
- 若运行环境没有子任务能力，主协调代理按同一契约顺序执行各员工职责。
- 若运行环境必须把员工隔离为独立任务，主协调代理必须保持同一项目根、同一输入输出路径和同一评审账本。

## 模型选择

- 默认继承主协调代理所在运行环境的模型。
- 只有显式配置 `role_model_profiles` 时，才按配置为员工选择模型。
- 员工不得自行切换模型，不得把模型能力写成事实。
- 缺少模型、工具或节点配置时，产物标为 `needs_config` 或 `blocked`。

## 工具能力检查

工作室执行前，主协调代理必须要求 `studio-tool-execution-agent` 生成工具能力报告：

```text
{episode-id}/production/tool-capability-report.json
```

报告必须说明以下能力是否可用：

- 图像生成能力；
- 桌面自动化；
- Blender；
- ComfyUI；
- Krita；
- GIMP；
- 可选 Photoshop。

Photoshop 不得被视为必需工具。ComfyUI 不影响导演规划；只有当用户要求本地可复现生成而 ComfyUI 缺失时，相关执行任务才标为 `needs_config` 或 `blocked`。

## 默认派工格式

```text
你是导演部门中的 <role>。
阅读角色卡：
<skills/director-room/agents/<role>.md 的内容>

项目契约：
<artifact 契约摘要>

输入：
<本角色需要的 artifact>

只返回结构化 envelope 和完整 artifact 内容。
不要直接编辑文件。
不要调用其他员工。
```

## 依赖顺序

- 输入校验通过后，运行 `director-agent`。
- `director-agent` 通过评审后，运行 `scene-breakdown-agent` 与 `visual-continuity-agent`。
- 两者均通过评审后，运行 `shot-planner-agent`。
- `shot-planner-agent` 通过后，运行 `scene-coordinate-agent`，生成 `layout.yaml`、场景圣经和低模搭建计划。
- `scene-coordinate-agent` 通过后，运行 `cinematographer-agent`。
- `cinematographer-agent` 通过后，运行 `storyboard-agent`。
- `storyboard-agent` 通过后，运行 `generation-strategy-agent`。
- `generation-strategy-agent` 通过后，运行 `shot-prompt-agent`。
- `shot-prompt-agent` 通过后，运行 `prompt-director-agent`。
- `prompt-director-agent` 通过后，运行 `style-preset-agent` 与 `asset-conditioning-agent`。
- 两者均通过后，运行 `shot-prompt-engineer-agent`。
- `shot-prompt-engineer-agent` 通过后，运行 `workflow-parameter-agent`。
- `workflow-parameter-agent` 通过后，运行 `prompt-qc-agent`。
- `prompt-qc-agent` 通过后，运行 `scene-image-resource-agent`。
- `scene-image-resource-agent` 通过后，运行 `studio-tool-execution-agent`，执行低模搭建、控制图导出、场景母图、导演参考图和修图任务。
- 若存在渲染反馈，运行 `comfyui-feedback-agent`。
- 若进入剪辑、音频或交付阶段，依次运行 `edit-planner-agent`、`audio-planner-agent`、`delivery-qc-agent`。
- 若存在人工审核反馈，运行 `user-feedback-triage-agent`，再把返工项退回受影响员工或工具执行任务。
- 所有被请求阶段均通过评审后，主协调代理装配最终综合中文报告。

## 镜头与分镜连续规划

镜头和分镜必须先整体连续规划，再拆分图片执行任务。

- `shot-planner-agent` 必须一次性整体处理本集所有场景与镜头，产出统一镜头表；不得按单镜头孤立派工生成镜头顺序。
- `storyboard-agent` 必须一次性整体处理本集分镜计划，确保相邻镜头的轴线、机位、动作方向、视线方向、光线、道具状态和角色站位连续。
- 主协调代理只有在完整镜头表和完整分镜计划通过评审后，才能派发逐镜头图片任务。
- 单镜头场景图和导演参考图必须拆成独立任务，每个任务引用同一套场景控制包、镜头 ID、摄影方案、分镜说明和控制图依据。
- 逐镜头图片任务只执行本镜头的场景输出图、导演参考图或控制图生成，不得重排镜头、重设场景、重放角色或改变道具位置。

## 平面调度坐标与低模导出

`layout.yaml` 是平面调度坐标的权威来源。它由 `scene-coordinate-agent` 生成，经评审通过后，才能交给工具执行环节建立低模场景。

低模执行顺序：

1. 根据 `layout.yaml` 和 `blockout-plan.md` 建立低模场景。
2. 导出顶视图、机位图和每个镜头的导演视角图。
3. 导出深度图、线稿和 mask。
4. 对照镜头表、摄影方案和视觉连续性圣经评审导出图。
5. 若用户或评审认为空间关系不成立，优先返工 `layout.yaml` 和低模场景，再重新导出图，不得只改提示词。

低模导出结果写入：

```text
{episode-id}/control/scene-packages/SC###/blockout.blend
{episode-id}/control/scene-packages/SC###/blockout-export-manifest.json
{episode-id}/production/studio-execution-manifest.json
```

## 评审循环

每个员工完成后立即评审：

1. 读取员工 envelope。
2. 验证 artifact 路径、结构、必需字段和 schema。
3. 检查来源追溯、连续性、双语字段、控制图依赖和状态标记。
4. 按员工评分量表给出 0 到 100 分。
5. 达到通过线后写入项目文件，并进入下一个员工。
6. 未达到通过线时，把评审记录退回同一员工重做。
7. 重做后的 artifact 重新进入同一评审流程。
8. 人工审核不通过时，先运行 `user-feedback-triage-agent`，再把反馈映射到对应员工或工具任务返工。

默认通过线：

- 普通产物：85 分。
- 关键产物：90 分。关键产物包括视觉连续性圣经、分镜表、摄影方案、生成计划、最终提示词、工作流计划和场景图片资源交接包。

评分未达标时，不得由主协调代理绕过员工重写创作内容。主协调代理只能修复明显格式错误；创意、规划、判断和提示词实质内容必须由对应员工返工。

## 评审账本

主协调代理必须维护：

```text
{episode-id}/reviews/director-room-review-ledger.json
{episode-id}/reviews/director-room-scorecard.md
```

账本记录每个员工每次尝试的分数、失败项、返工要求、最终通过状态和已写入 artifact。

人工反馈另写入：

```text
{episode-id}/reviews/human-feedback-log.jsonl
{episode-id}/reviews/feedback-revision-plan.json
```

每条人工反馈必须有状态：`open`、`in_progress`、`resolved` 或 `blocked`。

## 最终综合中文报告

所有员工产物通过评审后，主协调代理必须生成：

```text
{episode-id}/reports/director-room-final-report.md
```

报告必须面向人类审阅，使用中文说明：

- 所有输出文档、结构化文件、控制包、图片资源目录和逐镜头图片任务单；
- 每个输出文档的作用、来源依据、使用部门或使用阶段；
- 每个员工最终评分、通过线、返工次数、主要审查意见和最终状态；
- 工具能力检查、实际执行结果、生成文件路径和失败原因；
- 用户审核反馈、返工处理状态和未关闭问题；
- 场景连续性、镜头连续性、角色与道具一致性的审查结论；
- 已通过校验、警告项、阻塞项和后续交接建议。

缺少最终综合中文报告时，导演部门不得标记完成。

## 场景图片资源交付

`scene-image-resource-agent` 在提示词与工作流计划通过后运行。它汇总场景控制包、分镜面板和摄影方案，输出给后续美术规划使用的场景图片资源包。

资源包必须说明：

- 每个场景需要哪些母图、反向母图、关键道具位置图和调度概览图；
- 哪些图片已经存在，哪些需要生成；
- 每张图的用途、尺寸建议、连续性锁点和禁止变更项；
- 每个镜头对应的独立图片生成任务，尤其是单镜头场景图和导演参考图；
- 与 `layout.yaml`、分镜表、摄影方案和视觉连续性圣经的来源引用。

## 阻塞规则

固定必需输入缺失时，整体状态为 `blocked`，不得提问、猜测或兼容。

若同一员工因工具、模型、配置或事实缺失无法达标，主协调代理持续返工直到达标；若运行预算或外部条件使继续返工不可能，整体状态为 `blocked`，并写清缺失条件。
