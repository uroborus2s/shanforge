# T04 137 字段 PM 投影与只读多页面站点

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`TASK-IMPLEMENT-003-P001-T04`
- 状态：`ready_for_review`
- 上游：T01–T03、R009 PM field map、R014 released pin

## 目标

交付 10 张 PM 当前投影、137 字段完整映射、页面级 fingerprint 和只读多页面站点；需求、设计、任务、缺陷、代码、文档、质量、版本、报告与 PM record 的所有详情都是带返回按钮的独立页面，不使用侧边抽屉或 modal。

## 允许修改

- `src/application/project_knowledge/site_service.py`
- `src/runtime/project_knowledge/site_renderer.py`
- `src/settings/project_knowledge/pm_projection.py`
- `src/settings/project_knowledge/site_publisher.py`
- `tests/test_project_knowledge_pm.py`
- `tests/test_project_site_renderer.py`
- 当前任务 evidence/report/review/ledger 和记忆摘要

## 禁止修改

- 页面新增/编辑/审批/拖拽、CDN、前端框架、HTML 内状态推导、无关脏文件。

## 测试与验证

```bash
PYTHONPATH=src uv run pytest tests/test_project_knowledge_pm.py tests/test_project_site_renderer.py -q
```

必须验证 137 fields 以及 PK/父键/key collision/cardinality/type/nullable/history/R014 pin，分别构造并断言 `known|unknown|not_registered|not_applicable` 四态，HTML 不得把一种状态推成另一种；同时验证 HTML 转义、全部详情深链/返回、打印/键盘/四视口/axe、immutable build + atomic current symlink 的崩溃与并发、cache hit 不写、单页变化最小重绘。浏览器证据未运行时 NFR-PKI-009 保持阻塞。实现者只能进入 `ready_for_review`，UI review 必须独立完成。
