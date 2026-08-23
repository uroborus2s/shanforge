## 子代理工具映射

只在当前会话已暴露协作工具且任务符合 `subagent-driven-development` 边界时使用子代理，不修改用户全局 Codex 配置。当前工具职责：

- `spawn_agent`：创建有明确边界的子任务。
- `send_message`：向运行中或空闲代理发送补充信息，不触发新一轮。
- `followup_task`：给现有代理追加任务，并在空闲时触发新一轮。
- `wait_agent`：等待代理进展或最终结果。
- `list_agents`：查看当前代理状态。
- `interrupt_agent`：需要停止正在执行的代理时中断其当前轮次。

已完成的代理无需额外关闭；是否允许创建子代理始终以当前会话暴露的工具、用户授权和适用 skill 约束为准。

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
