# FLOW-TASK-011 升级 PM 视图

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-011`
- 状态：`completed_independently_approved`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

让 PM 看板按 Project、Baseline、Requirement、Task、Gate、Evidence 展示状态，并继续声明 HTML 不是事实源。

## 输入

- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- `.factory/project-knowledge/`
- `src/runtime/project_knowledge/`
- `src/settings/project_knowledge/`
- 流程契约实施方案。

## 允许修改

- `skills/using-shanforge/references/pm-dashboard-rendering.md`
- PM 生成逻辑或测试。
- `.factory/cache/site/current/` 可重建输出（不提交 Git）。

## 验证命令

```bash
PYTHONPATH=src .venv/bin/python -m pytest \
  tests/test_project_management_control_plane.py \
  tests/test_project_site_renderer.py \
  tests/test_prd_project_knowledge_requirements.py -q
```

期望输出：

```text
通过；项目总览、中文敏捷看板、独立详情页、需求/设计追踪及只读边界均有回归断言。
```

## 完成口径

PM 视图只能展示从正式文档、ledger、登记关系和受控摘要投影出的事实。当前实现由固定
CLI 增量刷新 SQLite 和静态 HTML；无变化时复用最后有效页面；SQLite、HTML 与 cache
不提交 Git。该任务已经由项目知识站点实现、浏览器验证和两轮独立复审覆盖。
