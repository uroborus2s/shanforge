## 子代理需要多代理支持

在 Codex 配置 `~/.codex/config.toml` 中加入：

```toml
[features]
multi_agent = true
```

这会启用 `spawn_agent`、`wait_agent`、`close_agent`，供 `dispatching-parallel-agents`、`subagent-driven-development` 等 skill 使用。使用 `subagent-driven-development` 时，implementer / reviewer 子代理完成后必须关闭。

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
需要执行本地提交时，流程总控应路由到 `gitcommitzh`，提交当前任务范围，并保留 work item、review、evidence 和 memory sync 记录。

## Codex App 收尾

若 sandbox 阻止建分支或 push（外部托管 worktree 中的 detached HEAD），agent 应只整理并提交当前任务范围，并提示用户使用 App 原生控件：

- **"Create branch"**：命名分支，再通过 App UI commit / push / PR。
- **"Hand off to local"**：把工作交接到用户本地 checkout。

agent 仍可运行测试、暂存文件，并给出建议分支名、commit message 和 PR 描述。
