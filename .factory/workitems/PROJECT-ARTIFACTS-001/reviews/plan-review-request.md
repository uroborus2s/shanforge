# 计划评审请求

## 输入

- 计划：`.factory/workitems/PROJECT-ARTIFACTS-001/plan.md`
- 工作项简报：`.factory/workitems/PROJECT-ARTIFACTS-001/brief.md`
- 相关正式文档：`docs/05-design/ux-ui-design.md`、`docs/05-design/api-design.md`、
  `docs/06-delivery/test-plan.md`
- 相关记忆：`.factory/memory/agent-session.md`、`.factory/memory/doc-map.md`

## 评审重点

1. 四个任务是否可独立验收且顺序闭合。
2. 是否遵守五层依赖与 application port owner。
3. 是否避免伪造 `.penpot`、重复文档和运行结果冒充定义。
4. SQLite、HTML 和缓存是否仍是可重建投影。
5. 测试、证据、记忆和本地提交门是否完整。

## 期望输出

按 `skills/writing-plans/references/plan-review-template.md` 写入
`.factory/workitems/PROJECT-ARTIFACTS-001/reviews/plan-review.md`。
