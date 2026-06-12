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
- `shot-planner-agent` 通过后，运行 `cinematographer-agent`。
- `cinematographer-agent` 通过后，运行 `storyboard-agent`。
- `storyboard-agent` 通过后，运行 `generation-strategy-agent`。
- `generation-strategy-agent` 通过后，运行 `shot-prompt-agent`。
- `shot-prompt-agent` 通过后，运行 `prompt-director-agent`。
- `prompt-director-agent` 通过后，运行 `style-preset-agent` 与 `asset-conditioning-agent`。
- 两者均通过后，运行 `shot-prompt-engineer-agent`。
- `shot-prompt-engineer-agent` 通过后，运行 `workflow-parameter-agent`。
- `workflow-parameter-agent` 通过后，运行 `prompt-qc-agent`。
- `prompt-qc-agent` 通过后，运行 `scene-image-resource-agent`。
- 若存在渲染反馈，运行 `comfyui-feedback-agent`。
- 若进入剪辑、音频或交付阶段，依次运行 `edit-planner-agent`、`audio-planner-agent`、`delivery-qc-agent`。

## 评审循环

每个员工完成后立即评审：

1. 读取员工 envelope。
2. 验证 artifact 路径、结构、必需字段和 schema。
3. 检查来源追溯、连续性、双语字段、控制图依赖和状态标记。
4. 按员工评分量表给出 0 到 100 分。
5. 达到通过线后写入项目文件，并进入下一个员工。
6. 未达到通过线时，把评审记录退回同一员工重做。
7. 重做后的 artifact 重新进入同一评审流程。

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

## 场景图片资源交付

`scene-image-resource-agent` 在提示词与工作流计划通过后运行。它汇总场景控制包、分镜面板和摄影方案，输出给后续美术规划使用的场景图片资源包。

资源包必须说明：

- 每个场景需要哪些母图、反向母图、关键道具位置图和调度概览图；
- 哪些图片已经存在，哪些需要生成；
- 每张图的用途、尺寸建议、连续性锁点和禁止变更项；
- 与 `layout.yaml`、分镜表、摄影方案和视觉连续性圣经的来源引用。

## 阻塞规则

固定必需输入缺失时，整体状态为 `blocked`，不得提问、猜测或兼容。

若同一员工因工具、模型、配置或事实缺失无法达标，主协调代理持续返工直到达标；若运行预算或外部条件使继续返工不可能，整体状态为 `blocked`，并写清缺失条件。
