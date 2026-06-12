# 导演分镜部工作流

父级 Codex 实例是唯一协调器。子代理不得继续派生代理，不得向用户发问，也不得改动共享文件；除非父级明确分配了互不重叠的写入集合。

如果你是执行单一角色卡的子代理，不需要检查是否存在 sub-agent 工具。完成本角色任务并返回 artifact envelope。缺少 `spawn_agent` 只会阻塞父级“多代理”编排，不会阻塞角色本身的思考。

## 默认派工格式

父级协调器给子代理的提示应窄而完整：

```text
你是 Codex 原生导演分镜部中的 <role>。
阅读此角色卡：
<skills/director-room/agents/<role>.md 的内容>

项目契约：
<artifact 契约摘要>

输入：
<本角色确实需要的 artifact>

只返回结构化 envelope 和完整 artifact 内容。
不要直接编辑文件。
```

除非用户明确要求，不设置模型覆盖；使用当前 Codex 继承模型。

## 并行规则

只并行没有互相依赖的角色：

- `{episode-id}/director/director-brief.md` 存在后，`scene-breakdown-agent` 和 `visual-continuity-agent` 可以并行。
- `shot-planner-agent` 必须等待 `{episode-id}/shots/scene-breakdown.json`。
- `cinematographer-agent` 必须等待 `{episode-id}/shots/shot-list.json`。
- `storyboard-agent` 必须等待分镜表、摄影方案和视觉连续性圣经。
- `generation-strategy-agent` 必须等待分镜表、摄影方案、分镜计划、视觉连续性圣经，以及可用的场景控制包计划。
- `shot-prompt-agent` 必须等待生成策略。
- `{episode-id}/prompts/comfyui-prompt-brief.md` 存在后，`style-preset-agent` 和 `asset-conditioning-agent` 可以并行。
- `shot-prompt-engineer-agent` 必须等待风格预设、资产条件包、提示词草稿、摄影方案、分镜计划、视觉连续性圣经和生成计划。
- `workflow-parameter-agent`、`prompt-qc-agent`、`comfyui-feedback-agent` 顺序执行，因为每一步都依赖前一步的提示词或参数产物。
- `edit-planner-agent` 必须等待 `{episode-id}/qc/shot-qc-report.json` 中出现可接受渲染状态。
- `audio-planner-agent` 等待剪辑计划或剧本对白映射。音频按对白行、旁白行、音效 cue 和音乐 cue 规划，不按每个镜头一个音频文件规划。
- `delivery-qc-agent` 等待剪辑和音频清单；若缺少后期输入，应把对应项标为 `blocked`。

## 场景控制包流程

场景控制包介于视觉连续性、摄影、分镜和 ComfyUI 工作流之间。它的目标是降低抽卡，而不是替代美术判断。

父级协调器应执行以下判断：

1. 如果一个场景存在多镜头切换、反打、复杂调度、道具位置锁定、动作连续或角色站位风险，则要求建立场景控制包。
2. 先由 `visual-continuity-agent` 定义场景事实：空间关系、道具、角色站位、出入口、光源、屏幕方向和禁止变更项。
3. 再由 `cinematographer-agent` 规定每个镜头的机位、焦段、相机高度、轴线和运动。
4. 然后将这些事实写入 `layout.yaml` 和 `blockout-plan.md`。若项目可调用 Blender 或 Unreal，应从同一低模场景导出 `top-view.png`、`camera-map.png`、shot guide、depth、lineart 和 masks；若暂不能调用，应写清楚占位路径和生成条件。
5. `generation-strategy-agent` 和 `workflow-parameter-agent` 必须把这些控制图作为生产依赖，而不是把它们揉进自然语言提示词。

文生图可以生成场景母图和气氛探索图；它不能独立证明平面调度、站位和机位一致。凡是要求精确连续性的镜头，应优先依赖坐标、低模和可复现导出。

## JSON 上下文传递

JSON 文件不会自动完整发送给每一次模型调用。父级协调器为每个子角色决定上下文包。

- 小型 JSON artifact 可完整传递。
- 对长分镜表、生成计划或提示词包，传递全局元数据和本角色需要的场景/镜头记录。
- 始终保留稳定 ID 和 `source_refs`，使切片上下文可以追溯到完整项目 artifact。
- 用户明确要求全量审查时，在可行情况下传递完整 JSON；否则按场景或镜头族拆分，并确定性合并返回产物。
- 不得隐瞒省略内容。必须告诉子代理哪些内容被摘要或切片。

## 父级职责

父级 Codex 协调器必须：

- 核验项目根和五个标准输入文件；
- 保持前资产分镜包与后资产视频生产包分离；
- 统一写入子代理返回的项目文件；
- 向 `{episode-id}/logs/director-room-agent-calls.jsonl` 追加每个子代理调用记录；
- 保留警告，不得把风险改写为成功；
- 修复 JSON 格式时保持镜头 ID 稳定；
- 在可行时用本地 schema 校验 JSON 输出；
- 执行双语分镜与双语提示词字段要求；
- 执行生产元数据与模型可见提示词分离；
- 执行场景控制包依赖检查；
- 防止视频提示词要求模型生成精确对白；
- 向用户汇总最终结果、阻塞项和下一步交接。

## 恢复规则

如果子代理返回 `blocked`，父级判断缺失输入是否可以安全推断。不能安全推断时，只向用户提出一个简洁问题。

如果子代理返回畸形 JSON 或缺少 artifact 内容，要求同一代理重发 envelope 一次。若第二次仍失败，父级只在创作内容无歧义时修复格式；否则把运行标为 `warning`，并仅在下游仍可工作时继续。
