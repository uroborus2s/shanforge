# T04 PM 投影与只读站点 Red/Green 证据

- Work item：`FLOW-CONTRACT-001`
- Task：`TASK-IMPLEMENT-003-P001-T04`
- Actor：`AI_EXECUTOR`
- 日期：2026-07-22
- 状态：`green_automated / browser_ui_pending`

## Red

`tests/test_project_knowledge_pm.py tests/test_project_site_renderer.py` 首次运行产生 2 个 collection error，exit 2；缺少 PM projector 与 site renderer，失败原因符合预期。

## Green

- T04 定向：`7 passed in 0.13s`。
- T01–T04 合并：`30 passed in 0.39s`。
- Ruff：`All checks passed!`。
- mypy：`Success: no issues found in 19 source files`。
- exit 0；失败 0，错误 0，跳过 0，未运行 0。

## 覆盖的硬门

- R009 137 fields / 13 row models / R014 发布 pin。
- PK、父键、key collision、类型、history/current-only。
- `known|unknown|not_registered|not_applicable` 四态分列存储，HTML 按状态原样渲染。
- 需求、设计、计划、任务、缺陷、文档、代码、质量、版本、报告与 10 个 PM 模块全页详情。
- 所有详情含返回链接，无 drawer/modal/写操作；HTML 转义、focus、打印和 768/1024 响应式 CSS 静态合同。
- immutable build、页面硬链复用、cache hit 不写、pointer 替换前崩溃保留旧站。

## 实仓站点

```text
current_index=/Users/uroborus/AiProject/shanforge/.factory/cache/site/current/index.html
pages=3983
first_build=584.81ms
manifest_fast_cache_hit=2.13ms
```

SQLite/站点均是 `.factory` 内可删除生成物。

## 未运行项

Playwright 四视口、axe、键盘实操、打印预览和人工视觉评审尚未运行；`NFR-PKI-009` 保持 blocked，不用静态测试冒充通过。

## 结论

T04 自动化实现进入 `ready_for_review`；UI 独立评审待 T06 集成候选完成。
