# MODEL-ORCHESTRATOR-SELECTION-001

## 目标

取消仓库对主会话模型和推理强度的固定选择；主会话模型由用户选择，主会话仍负责对子任务进行分级、授权、派发和失败关闭。

## 验收标准

- `.codex/config.toml` 不再设置主会话 `model` 或 `model_reasoning_effort`。
- 当前治理合同使用“主会话/父会话”描述控制责任，不把该责任绑定到 Sol。
- Luna/Terra worker 与 Terra reviewer 的模型、推理强度、沙箱和失败关闭规则保持不变。
- 正式 PRD、设计、用户指南、Skill 合同、任务模板和定向测试保持一致。
- 定向测试、Ruff 和 diff check 通过，独立只读 review 通过后才提交。
