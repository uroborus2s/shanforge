# 项目策划 / 任务书

## 项目背景

shanforge 正在把 AI 软件工厂流程从脚本/提示词驱动，收敛为项目状态、work item、ledger、skill 和 memory 驱动的开发体系。

## 项目目标

- 从一句话需求推进到需求、设计、计划、实现、评审、验证、人工确认和记忆同步。
- 防止 AI 不按流程执行、重复执行、跳过计划、跳过验证或自我批准。
- 让人类能快速查看当前项目状态，而不是翻 ledger 和长文档。

## 验收标准

- PM 控制面覆盖 Excel 十模块。
- `.factory/pm/` 保存事实文件。
- HTML 模板位于 `using-shanforge/references/`。
- 人类要求查看状态时生成 `.factory/pm/generated/status-dashboard.html`。
- HTML 不作为事实源。

## 假设

- 当前项目仍以 Markdown、JSONL 和 work item ledger 为主要事实源。
- 用户希望减少新概念，优先复用已有 `using-shanforge`。

## 约束

- 不新增独立 `project-management` skill。
- 不把 Excel、HTML 或聊天记录当作唯一事实源。
- 不默认读取全部 `docs/`。
