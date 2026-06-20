# 编剧室模拟器设计方案

## 1. 目标

编剧室模拟器是 Shanforge 多 Agent 工作流的可视化前台原型。它用 2.5D 办公室界面展示 Agent App 的执行过程：每个 agent 有工位、名字、等级、状态、当前任务、输入产物和输出产物；agent 之间发生交接、审核、返工时，界面通过移动、会议和白板问题卡展示真实 workflow event。

本页面不是替代 Shanforge CLI，也不是替代业务 Agent App runtime。它是一个面向人类观察、调试和演示的 UI 宿主。

## 2. 当前交付

当前先交付一个静态 HTML 原型：

- [Writer Room Simulator 静态原型](./design-assets/writer-room-simulator.html)

原型不依赖 React、Vite 或 Phaser，便于直接打开审阅。后续正式实现应迁移为 `React + Vite + Phaser + WebSocket/SSE event stream`。

## 3. 推荐正式技术栈

| 层 | 技术 | 职责 |
| --- | --- | --- |
| UI shell | React + Vite + TypeScript | 顶部阶段条、侧边栏、Inspector、日志、Gate 控件。 |
| 2.5D scene | Phaser 3 + Tiled isometric map | 办公室地图、agent sprite、工位、移动、会议、白板动画。 |
| State | XState 或 Zustand | Agent 状态机、事件缓冲、回放状态。 |
| Event stream | WebSocket 或 SSE | 从 Shanforge workflow/runtime 推送结构化事件。 |
| Backend | Shanforge Agent App runtime | 产出 agent 状态、产物、handoff、eval、memory 事件。 |

## 4. 事件驱动原则

界面不得编造状态。所有动画和状态变化必须来自后端事件或回放事件：

```json
{
  "type": "handoff_requested",
  "from_agent": "script-doctor-agent",
  "to_agent": "rewrite-agent",
  "reason": "weak_motivation",
  "artifact": "reports/critique_v01.json"
}
```

前端只做事件解释：

- `agent_status_changed`：更新人物状态和进度。
- `artifact_created`：资料柜新增文件卡。
- `issue_found`：白板新增问题卡。
- `handoff_requested`：发起人物移动。
- `meeting_started`：两名 agent 进入面对面沟通。
- `gate_waiting`：流程暂停，等待人工确认。
- `eval_completed`：评分台展示结果。
- `memory_updated`：资料管理员归档经验。
- `evolution_proposed`：进化代理生成 skill/prompt/rubric 改进建议。

## 5. UI 信息架构

```text
顶部：阶段时间线
左侧：项目产物和问题白板
中间：2.5D 编剧室办公室
右侧：Agent Inspector
底部：事件日志和回放控制
```

## 6. Agent 与空间映射

| Agent | 空间位置 | 主要动作 |
| --- | --- | --- |
| `showrunner-agent` | 主桌 / 白板旁 | 规划 brief、召集会议。 |
| `story-architect-agent` | 结构白板 | 拆 beat、贴结构卡。 |
| `character-agent` | 角色墙 | 维护人物卡和成长弧。 |
| `scene-agent` | 场景板 | 设计场景和视觉锚点。 |
| `dialogue-agent` | 写作工位 | 写 `script_v01`。 |
| `script-doctor-agent` | 审核桌 | 标注问题和发起返工。 |
| `rewrite-agent` | 改写工位 | 根据 critique 改稿。 |
| `continuity-agent` | 连续性检查台 | 检查角色、场景、道具、情绪连续。 |
| `script-evaluator-agent` | 评分台 | 计算 score 和 pass/revise。 |
| `memory-librarian` | 档案柜 | 归档状态、失败模式和经验。 |
| `learning-evolution-agent` | 研究台 | 生成进化建议。 |

## 7. 状态机

Agent 状态最小集合：

```text
idle -> reading -> thinking -> writing -> reviewing -> walking -> meeting -> done
                                      -> blocked
```

每个状态都应可回放、可暂停、可在 Inspector 中查看输入和输出。

## 8. Shanforge 集成点

正式实现时建议新增一个 UI 宿主目录，而不是把 UI 逻辑塞进平台 core：

```text
apps/writer-room-simulator/
  package.json
  vite.config.ts
  src/
    App.tsx
    scene/WriterRoomScene.ts
    state/workflowStore.ts
    events/eventTypes.ts
```

后端集成点：

```text
src/access/api/workflow_events_api.py
src/application/execution/service.py
src/domain/workflow/models.py
```

事件记录仍保持 JSONL 和结构化 event record，前端只消费事件流。

## 9. MVP 验收

- 可打开静态原型页面。
- 页面包含 2.5D 办公室、11 个 agent、阶段条、Inspector、事件日志和白板。
- 点击 agent 可查看岗位、等级、状态、任务和产物。
- 点击播放后可模拟完整编剧室流程。
- `script-doctor-agent` 到 `rewrite-agent` 的 handoff 有移动和会议表现。
- 页面明确映射未来 React + Phaser 实现路径。

## 10. Codex-native 编剧室 Skill

当前先把“每个 agent 都由 Codex 完成各自任务”的工作方式收口为
`skills/writer-room/`，而不是先落 Python agent loop。

该 skill 的职责边界如下：

- 主 Codex 线程承担制片主任 / 调度器职责，负责创建项目目录、读取产物、派发子 agent、写入最终文件和汇总结果。
- 子 Codex agent 承担总编剧、故事结构师、人物设计师、场景设计师、对白编剧、剧本医生、改写编剧、连续性审查、评分员、记忆管理员和进化管理员职责。
- Python 代码最多用于后续确定性校验、文件整理或打包，不作为子 agent 的 LLM 调用层。
- 自我进化先输出 `memory/evolution-notes.md` 和失败模式记录；任何 skill prompt、rubric 或模板升级都必须经过用户明确批准。

这一路线使编剧室可以直接在 Codex 环境内运行，并且保留未来接入
Shanforge Agent App runtime 或 UI simulator 的空间。
