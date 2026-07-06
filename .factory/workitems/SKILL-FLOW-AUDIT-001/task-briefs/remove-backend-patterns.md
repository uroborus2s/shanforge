# 子任务：删除 backend-patterns skill

## 背景

用户确认 `backend-patterns` 只是通用后端教程，不应继续作为当前 Shanforge 开发流程 skill 保留。

## 需求

- 删除 `skills/backend-patterns/`。
- 清理活跃流程、项目配置和测试中的 `backend-patterns` 引用。
- 保留历史审计报告中的评分记录，不回写历史事实。
- 按 `SKILL-FLOW-AUDIT-001 Plan` 补 evidence、ledger 和结构测试。

## 任务分解

1. 影响面扫描：查找 `backend-patterns` 的所有引用。
2. 删除目录：移除 `skills/backend-patterns/`。
3. 配置清理：从 `.factory/project.json` 和 `config/software-factory.defaults.json` 删除共享 skill / 角色 skill 引用。
4. 流程文档清理：从 Superpowers 流程方案的实施技术栈 skill 清单删除该行。
5. 测试修正：更新 deprecated cleanup 测试，确认 `backend-patterns` 已删除且活跃流程不再引用。
6. 验证：跑定向 pytest、ruff、JSON 解析和引用扫描。

## 非目标

- 不重写后端设计文档。
- 不删除 `api-design`、`python-uv-project`、`stratix-service` 等仍在用的后端相关 skill。
- 不修改历史审计报告里的原始评分。

## 完成标准

- `skills/backend-patterns/` 不存在。
- 活跃流程、项目配置和默认配置不再引用 `backend-patterns`。
- 定向测试通过。
- ledger 和 evidence 已记录。
