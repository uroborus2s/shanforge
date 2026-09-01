# 总体方案与协作治理设计

## 文档控制

| 项目 | 内容 |
|---|---|
| 文档 ID | `DESIGN-SOLUTION-001` |
| 正式版本 | `v4.0.0` |
| 状态 | 已批准并生效 |
| 负责人 | `HUMAN_ARCHITECTURE_DOMAIN_LEAD` |
| 上游 | `PRD-SHANFORGE-001`、`DESIGN-ARCH-001` |
| 下游 | 专项 skills、正式设计、测试 |

## 文档职责

- 保存 Skill-first 交付边界和协作治理结论。
- 不保存宿主 runtime、服务、数据库或历史平台实现细节。

## 当前设计

Shanforge 是由代理宿主加载的 skill-first 软件工厂资产。`using-shanforge` 先判定请求是否影响项目；项目化请求按需恢复事实，再选择一个专项 skill。专项 skill 在授权范围内修改目标项目的代码、文档、测试和 `.factory/` 事实。

正式事实保存在 `docs/`，任务状态、证据和 Gate 保存在 WorkItem ledger，`.factory/memory/` 只保存有界恢复摘要。缓存和 HTML 快照是可重建投影。Sol 负责整体设计、分级和路由；Terra/Luna 只执行完整授权任务包，遇到范围、输入、风险、连续验证失败或人工 Gate 即交回 Sol。

## 适用验证

- `tests/test_lifecycle_governance.py` 校验当前设计不再引用已废止的平台路径和机器附件。
- `git diff --check` 校验文档变更格式。

## 正式版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| `v4.0.0` | 2026-09-01 | 以当前 Skill-first 边界替换旧平台调研正文。 |
| `v3.1.0` | 2026-04-13 | 历史：旧平台调研与协作治理设计。 |
