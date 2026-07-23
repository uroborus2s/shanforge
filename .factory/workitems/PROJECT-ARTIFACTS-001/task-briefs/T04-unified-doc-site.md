# 任务简报

## 工作项

- 工作项：`PROJECT-ARTIFACTS-001`
- 任务：`T04` 单一项目文档入口与增量快照
- 状态：`approved`
- 上游计划：`.factory/workitems/PROJECT-ARTIFACTS-001/plan.md`
- 流水账：`.factory/workitems/PROJECT-ARTIFACTS-001/ledger.jsonl`

## 目标

移除设计/文档双入口，在同一文档详情组合展示正文、章节和相关机器附件，并保持增量静态快照。

## 允许修改

- `src/runtime/project_artifacts/site_renderer.py`
- `src/settings/composition/project_knowledge.py`（只切换 renderer 装配）
- `tests/test_project_artifact_site_renderer.py`
- 本工作项 evidence/report/ledger 与相关 memory summary。

## 禁止修改

- 动态服务端、写操作页面和侧边抽屉详情。
- 现有缓存安全、原子发布和路径校验。
- `PK-SOURCE-MIGRATION-001-T04` 的人工确认状态。

## 验证命令

```bash
uv run pytest -q tests/test_project_artifact_site_renderer.py tests/test_project_site_renderer.py
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge project snapshot --html --json
PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge project snapshot --html --json
```

期望：pytest exit 0；第一次快照成功；第二次回执 `cache_hit=true`，未变化页面 hash 不变。

## 实施步骤

1. Red：导航仍同时出现“设计/文档”，文档页没有附件。
2. Green：artifact-aware renderer 包装现有 renderer，只移除重复入口并组合附件元数据。
3. 不复制 PNG/SVG/`.penpot`；真实文件只显示相对文件名，缺失时显示等待连接。
4. 跑两次 snapshot，第二次断言 `cache_hit=true`；未变化页 hash 不变。
5. 对暂存区逐 hunk 审计，确认没有旧 T04 改动。
6. 写 `evidence/task-4.md`、`reports/task-4.md` 和 ledger 事件。

## 完成口径

导航只有一个“项目文档”入口，正文和附件可读，详情有返回按钮，第二次快照命中缓存。
