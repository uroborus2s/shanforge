## 子代理工具映射

只在当前会话已暴露协作工具且任务符合 `subagent-driven-development` 边界时使用子代理，不修改用户全局 Codex 配置。当前工具职责：

- `spawn_agent`：创建有明确边界的子任务。
- `send_message`：向运行中或空闲代理发送补充信息，不触发新一轮。
- `followup_task`：给现有代理追加任务，并在空闲时触发新一轮。
- `wait_agent`：等待代理进展或最终结果。
- `list_agents`：查看当前代理状态。
- `interrupt_agent`：需要停止正在执行的代理时中断其当前轮次。

已完成的代理无需额外关闭；是否允许创建子代理始终以当前会话暴露的工具、用户授权和适用 skill 约束为准。

## 可执行模型派发合同

只有以下两个互斥分支可以派发；父 Sol 先生成稳定 `dispatch_id`，并把它放入 `message` 以绑定路由、调用和回执：

| 分支 | 前提 | `model` / `reasoning_effort` | sandbox 与输入 |
|---|---|---|---|
| `worker` | `execution-workflow`、`source_or_test_write`、已授权 | Luna/`low`（`simple + low`）或 Terra/`medium`（其余） | 精确写集内写入；完整 task brief、写集、禁令、验证命令 |
| `reviewer` | `review-workflow`、`state_or_gate_write`、`reviewer_type=independent_subagent`、身份/范围完整、实现/验证完成 | Terra/`high` | 只读；完整 review brief、候选范围、禁止写入、只读验证命令 |

`workflow_id` / `write_policy` 与声明分支不匹配，或多个分支可命中时，固定 `input_conflict, do_not_dispatch` 并交还 Sol；不得以默认 direct 修复冲突。其余任务不派发，保持 `dispatch_role=none, dispatch_required=false, dispatch_mode=direct`。父会话必须真实调用已暴露的 `spawn_agent`，不得只在文字中写模型名：

```text
spawn_agent({
  task_name: <stable task-card-derived name>,
  message: <dispatch_id + 完整 task brief + allowed_paths + forbidden_actions + verification commands + status return format>,
  model: <execution_model>,
  reasoning_effort: <requested_reasoning_effort>,
  fork_turns: "none"
})
```

worker 的 `task brief` 指完整实现简报；reviewer 的同一 message 位置改为完整 review brief。worker 的 `model` 必须逐值等于路由包的 `execution_model`；Luna/worker 固定 `low`，Terra/worker 固定 `medium`。reviewer 固定
`model: gpt-5.6-terra`、`reasoning_effort: high` 和只读 sandbox，不改写 worker 路由。两分支的 `fork_turns: "none"` 都是必填项，
不得让执行者继承父会话整段历史。

父 Sol 必须在调用前生成稳定 `dispatch_id`，用它绑定路由、调用和回执。成功返回至少提供 canonical task 或 agent ID；
父 Sol 随后保存并回读如下真实工具回执。子代理在消息中自报的模型不构成回执，也不得虚构模型内部身份：

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

`status: accepted` 只表示工具调用已成功接受，不是子代理完成态。该语义对两个分支相同。调用前先确认工具已暴露；工具未暴露、`spawn_agent` 失败、显式模型不可用、回执缺任一字段，或
`requested_model != execution_model` 时，结果只能是 `dispatch_failed` 或 `worker_unavailable` 并交还 Sol。禁止用 Sol
代写、替换模型或以子代理自报身份补足回执。

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
