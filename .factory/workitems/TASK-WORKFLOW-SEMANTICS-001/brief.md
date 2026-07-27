# TASK-WORKFLOW-SEMANTICS-001 Brief

## 目标

把“任务、任务卡、工作流、方法、工具、Gate、Event、Evidence”的边界落到 Shanforge workflow skill，并补齐会话分析 / 项目任务卡判定、Bug 两段式确认、并行子任务执行、美术资源管线和黑盒 eval 场景。

## 非目标

- 不新增万能 `execute_task`。
- 不恢复旧中心命令、动作注册表、`factory-*` 或旧全局流程脚本。
- 不把读文件、运行命令、提问、等待确认写成任务卡。

## 执行任务卡

- `TASK-001-flow-entry-semantics`：流程入口判定、brainstorming 和需求分析契约。
- `TASK-002-plan-parallel-execution`：任务卡粒度和可并行子任务执行规则。
- `TASK-003-bug-two-phase-workflow`：Bug 调查确认和修复确认 Gate。
- `TASK-004-art-asset-pipeline`：美术方向和资源包生产 skill。
- `TASK-005-black-box-task-card-boundaries`：黑盒 eval 补直接分析 / 拆分任务卡场景。
- `TASK-006-integration-verification`：整合、验证和提交前说明。

## 成功标准

- 直接问“分析系统登录的需求”时不创建任务卡。
- 从“分析 XX 系统”拆出的登录需求分析必须创建任务卡。
- 两种分析共享核心输出契约。
- Bug 未复现 / 未根因确认 / 未修复方案确认时不得进入修复。
- 同层无依赖、无冲突、无 Gate 的任务卡可以并行子任务执行。
- 美术资源包只包含用户确认过的图，未确认中间图必须删除。
- 目标 pytest 和 ruff 通过。
