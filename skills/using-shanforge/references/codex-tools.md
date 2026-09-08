## 子代理工具映射

只在当前会话已暴露协作工具且符合 `using-shanforge` 派发判定时使用子代理，不修改用户全局 Codex 配置。当前工具职责：

- `spawn_agent`：创建有明确边界的子任务。
- `send_message`：向运行中或空闲代理发送补充信息，不触发新一轮。
- `followup_task`：给现有代理追加任务，并在空闲时触发新一轮。
- `wait_agent`：等待代理进展或最终结果。
- `list_agents`：查看当前代理状态。
- `interrupt_agent`：需要停止正在执行的代理时中断其当前轮次。

已完成的代理无需额外关闭；是否允许创建子代理始终以当前会话暴露的工具、用户授权和适用 skill 约束为准。

## 可执行模型派发合同

worker、analyst、reviewer 的准入以 [子代理严格派发判定](../SKILL.md#子代理严格派发判定) 为准，
模型和推理强度只按该 skill 的“子任务模型决策表”选择，本参考不另设映射。
`workflow_id` / `write_policy` 与声明分支不匹配或多个分支可命中时，固定 `input_conflict, do_not_dispatch`；其余非派发任务保持 `dispatch_role=none, dispatch_required=false, dispatch_mode=direct`。

### 调用与角色能力

父会话先核对当前 `spawn_agent` 的模型、effort、role 和隔离能力，将来源记入 `capability_source`。
官方 API 支持某档不代表当前会话已暴露该组合；API effort 与 Codex/Work Ultra 编排模式不能混用。
不得省略 `model` 或 `reasoning_effort` 让宿主继承父配置；本合同固定 `fork_turns="none"`，`fork_turns=all` 不接受模型/effort override。

保留 `luna-worker`、`terra-worker`、`terra-reviewer` 三个固定 preset，只在其固定模型、effort 和职责与路由完全匹配时使用。
`.codex/agents/task-reader.toml` 只固定只读职责和 `sandbox_mode=read-only`，供 analyst 或独立 reviewer 使用，不固定模型/effort。
该文件通过 TOML 校验不代表当前宿主已加载；须在新会话实际暴露后才可调用。当前会话未暴露时明确不可用；普通独立 reviewer 可使用已暴露且匹配的 `terra-reviewer` / Terra/high。
Astra 深度 reviewer 或 analyst 必须有已暴露且不冲突的只读角色；不得用可写 generic role 冒充只读。
角色固定值与请求冲突即拒绝，不能省略参数绕过。worker 使用支持所选模型/effort、写入边界相符的角色。

父会话生成稳定 `dispatch_id`，写入 message 以绑定路由、调用和回执，真实调用已暴露的工具：

```text
spawn_agent({
  task_name: <stable task-card-derived name>,
  agent_type: <当前已暴露且与路由及读写权限匹配的 role>,
  message: <dispatch_id + 完整子任务 brief + allowed_paths + forbidden_actions + verification commands + status return format>,
  model: <execution_model>,
  reasoning_effort: <requested_reasoning_effort>,
  fork_turns: "none"
})
```

worker 的 message 使用完整实现简报和精确写集；reviewer 使用独立 review brief、候选、禁止写入和只读验证命令；
analyst 使用明确分析问题、只读输入、已有任务身份和父阶段，禁止写文件、改变父阶段或自批。
三个分支的 `model` / `reasoning_effort` 都必须逐值等于路由选择；子代理不继承父会话整段历史。

官方能力资料：[GPT-6 Astra 模型页](https://developers.openai.com/api/docs/models/gpt-6-astra)说明 API 推理档位；
[子代理模型与推理配置](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)说明省略参数时的继承及客户端能力边界；
[最新模型指南](https://developers.openai.com/api/docs/guides/latest-model)提供派发和验证建议。项目选档表是 Shanforge 策略，实际可用组合仍以当前会话工具为准。

### 父工具回执与失败关闭

工具成功返回至少提供 canonical task 或 agent ID。父会话将真实调用参数和返回值合并保存并回读：

```text
dispatch_receipt:
  dispatch_id: <parent-generated stable id>
  task_card_id: <existing task card>
  requested_model: <model argument>
  requested_reasoning_effort: <reasoning_effort argument>
  fork_turns: none
  agent_id: <returned agent id or canonical task>
  status: accepted
  source: parent_tool_receipt
```

`status: accepted` 只表示宿主接受了该请求，不是子代理完成态，也不证明底层模型内部身份。子代理自报不构成回执。
工具未暴露、`spawn_agent` 失败、模型/effort 不支持、角色不可用或固定值冲突、回执缺字段，或回执的 dispatch_id、任务身份、模型、effort、fork 与请求不一致时，
结果只能是 `dispatch_failed` 或 `worker_unavailable` 并交还主会话。禁止由主会话代写 worker、代替 reviewer、静默替换模型，或以子代理自报补足回执。
analyst 不可用时父会话可继续已授权只读分析，并明确记录未派发。

阶段或风险变化由父会话重评；连续两次失败先补复现/证据并收窄任务。需要改变模型、强度或角色时，新建 `dispatch_id` 和 `spawn_agent`，保留旧路由/回执。
`followup_task` 只能在同模型、同强度、同角色下补充上下文，不具备修改这些配置的参数。
不可用组合可以由父会话在同一授权范围内显式重选受支持且满足质量/风险下限的组合，再生成新路由重派，不能静默降级或改由父会话写实现。

## 环境检测

创建 worktree 或收尾分支前，先用只读 git 命令检测环境：

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

- `GIT_DIR != GIT_COMMON` -> 已在 linked worktree，跳过创建。
- `BRANCH` 为空 -> detached HEAD，不能从 sandbox 直接建分支、push 或建 PR。

这些信号只用于判断当前 Codex 环境是否允许本地分支、commit、push 或 PR 动作。
任务完成且有可提交改动时，流程总控应默认路由到 `gitcommitzh`，提交当前任务范围，并保留 work item、review、evidence 和 memory sync 记录；用户明确要求暂不提交时除外。

## Codex App 收尾

若 sandbox 阻止建分支或 push（外部托管 worktree 中的 detached HEAD），agent 应只整理并提交当前任务范围，并提示用户使用 App 原生控件：

- **"Create branch"**：命名分支，再通过 App UI commit / push / PR。
- **"Hand off to local"**：把工作交接到用户本地 checkout。

agent 仍可运行测试、暂存文件，并给出建议分支名、commit message 和 PR 描述。
