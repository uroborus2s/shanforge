# 子任务：补齐 requirements-engineering 流程契约

## 背景

`SKILL-FLOW-AUDIT-001` 的流程测试指出：`requirements-engineering` 主文件偏方法论，缺少 Shanforge 标准输出路径、ledger 输出、memory sync、review gate 和状态包。

## 需求

- 补齐 `skills/requirements-engineering/SKILL.md` 的输入、输出、默认流程和状态包。
- 明确需求 skill 只能产出 `requirements_ready` 或阻塞状态，不能自批 `approved` / `done`。
- 明确需求事实写入 `.factory/workitems/<WORKITEM-ID>/`、`.factory/memory/` summary 和 work item ledger。
- 不让该 skill 决定下一步 skill，只通过 `needs` 回写。
- 新增结构测试固定这些约束。

## 非目标

- 不重写 PRD 模板。
- 不改正式需求文档。
- 不创建远端 PR。

## 完成标准

- `requirements-engineering/SKILL.md` 包含输出位置、memory sync、ledger、状态包和自批禁止项。
- 测试覆盖新增契约。
- 定向 pytest、ruff 和 ledger JSONL 验证通过。
