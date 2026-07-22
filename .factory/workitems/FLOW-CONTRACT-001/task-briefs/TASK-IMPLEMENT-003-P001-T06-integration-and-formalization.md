# T06 装配、正式文档与整体资格化

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T06`
- 状态：`ready_for_review`
- 上游：T01–T05

## 目标

完成唯一 composition、真实仓 CLI/站点集成、安全/性能/响应式验证，并把 R009 原位融入现有正式 owner 文档、文档索引和最小 Memory。

## 允许修改

- `src/settings/composition/project_knowledge.py`
- `tests/test_project_knowledge_integration.py`
- `tests/test_project_knowledge_security.py`
- `tests/test_project_knowledge_performance.py`
- R009 明确列出的现有正式 owner 文档
- `.factory/project-knowledge/relation-declarations.json`
- `docs/05-design/ai-sdlc-catalog.source.json`（T05 package 校验通过后删除）
- `docs/05-design/ai-sdlc-catalog.manifest.json`（T05 package 校验通过后删除）
- `.factory/pm/README.md`、`project-brief.md`、`team-raci.md`、`milestones.md`、`wbs.md`、`risk-register.jsonl`、`communication-plan.md`、`meeting-notes/*.md`、`status-reports/*.md`、`change-register.jsonl`、`closure-report.md`、`dashboard.md`（逐项 disposition 后处理）
- `.factory/catalog/ai-sdlc-catalog.source.json`
- `.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-DESIGN-001-R019-ai-sdlc-catalog-release-manifest.json`
- `.factory/memory/` 中当前会话卡、doc-map 和受影响 summary
- 当前任务 evidence/report/review/ledger

## 禁止修改

- 新建平行 `docs/05-design/project-knowledge-*.md`、`TASK-IMPLEMENT-002-R001`、远端、部署和无关脏文件。

## 测试与验证

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_*.py tests/test_project_cli.py tests/test_system_task_integration.py -q
uv run ruff check src tests
uv run mypy src
uvx --from docs-stratego docs-stratego source validate --repo-path .
git diff --check
```

必须记录真实 exit code、测试计数、Memory 0/1/50/200、10k 单来源、warm/single/cold/enqueue/ordinary-sync 性能分位、固定时钟双构建 Hash、四视口/axe/键盘/打印/人工视觉结果。浏览器或硬 NFR 未运行时整体资格保持阻塞。整体独立 review 的 Critical/Important 为 0 后才可进入当前任务本地 `gitcommitzh` 提交；Push/PR/Merge/部署仍未授权。
