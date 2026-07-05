# Antigravity CLI (`agy`) 工具映射

skill 使用动作语义，如“派发子代理”“创建 todo”“读取文件”。在 Antigravity CLI (`agy`) 中，对应以下工具。

| skill 动作 | Antigravity CLI 对应方式 |
|----------------------|----------------------|
| 派发子代理（`Subagent (general-purpose):` 模板） | 使用 `invoke_subagent` 和内置 `TypeName`：`self` 用于完整能力任务，`research` 用于只读任务 |
| 任务跟踪（“create a todo”“mark complete”） | 使用 **task artifact**：`write_to_file` 设置 `IsArtifact: true` 和 `ArtifactType: "task"`（见 [任务跟踪](#任务跟踪)）。不要用 `manage_task`；它管理后台进程。 |

## 任务跟踪

Antigravity **没有 todo 工具**。`manage_task` 管理后台进程：`list` / `kill` / `status` / `send_input`；它不是清单工具。skill 要求创建 todo 或跟踪任务时，维护一个 **task artifact**：用 `write_to_file` 保存 Markdown 清单，并设置 `IsArtifact: true`、`ArtifactMetadata.ArtifactType: "task"`；后续用 `replace_file_content` / `multi_replace_file_content` 更新。

任何多步骤任务开始时，先创建 task artifact，列出计划所有步骤。每完成一步，编辑 artifact 标记为 `- [x]`。计划变化时更新清单。保持它为最新状态；它是剩余工作的事实源。对话变长后，每步开始前重读它。
