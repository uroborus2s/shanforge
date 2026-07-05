# Pi 工具映射

skill 使用动作语义，如“派发子代理”“创建 todo”“读取文件”。在 Pi 中，对应以下工具。

| skill 动作 | Pi 对应方式 |
| --- | --- |
| 派发子代理（`Subagent (general-purpose):` 模板） | 若已安装可用子代理工具，使用它；例如 `pi-subagents` 的 `subagent` |
| 任务跟踪（“create a todo”“mark complete”） | 若已安装 todo/task 工具，使用它；否则在计划文件或 `TODO.md` 中跟踪 |

## 子代理

Pi core 不内置标准子代理工具。`pi-subagents` 是推荐可选包，提供 `subagent` 工具，支持单代理、链式、并行、异步、forked-context、resume/status 工作流。若没有可用子代理工具，不要伪造 `Task` 调用；改为在当前会话顺序执行，或说明未安装可选子代理能力。

## 任务列表

Pi core 不内置标准任务列表工具。若安装了 todo/task 扩展，按其文档使用。否则用 Superpowers 计划文件、Markdown 清单或仓库本地 `TODO.md` 跟踪任务。旧版 Superpowers 文档可能提到 `TodoWrite`；按上面的任务跟踪动作处理。
