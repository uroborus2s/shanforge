# T06 集成、站点与完整验证证据

**任务：** `TASK-IMPLEMENT-003-P001-T06`
**日期：** 2026-07-22
**作者结论：** `ready_for_review`

## 真实仓索引与 CLI

- 逻辑表：39；FTS 虚表：2；SQLite shadow table：8。
- 当前 generation 来源：461（`pk_source_state` 保留 465 条 current/previous 状态）；实体：7,576；文档：57；章节：1,701。
- 需求：27；验收条件：64；任务：39；代码文件：366；代码符号：3,532；测试：723。
- 强关系：20；诊断：45。
- `find 数据与存储设计` 返回文档与章节两个稳定实体。
- `show doc:DESIGN-DATA-001` 返回 Markdown semantic locator，不使用行号。
- `trace REQ-PKI-004 --depth 2` 返回设计、实现类和验证测试关系。
- `context doc:DESIGN-DATA-001` 返回 1 文件、24 bytes、`body_read=false`。
- `maintain --dry-run` 返回零删除项。

标准 `snapshot --html --json` 会先检查 registry source stat：文件变化时增量刷新；无变化时 `parsed_count=0`、`cache_hit=true`、`rendered_pages=0`。本轮实测：

- 当前有效站点：762 个 HTML 页面；每个代码文件一个详情页，3,532 个 AST 符号在文件页内使用稳定锚点。
- 同进程无变化 20 次：P95 `32.884 ms`，包含全部页面摘要校验。
- 单个既有 Python 来源完整 CLI 五次：`0.69, 0.69, 0.69, 0.69, 0.70 s`，P95 `0.70 s`；每次解析 1 个来源、重建 6 页、复用 759 页。
- 冷重建既有证据：`3.00 s`；10,000 artifact extractor P95 `402.268 ms`。
- Git HEAD 变化会发布新 generation，但不重复解析文件。

## 站点与可访问性

- 真实 Chromium：1440×900、1024×768、768×1024、390×844 四视口通过。
- 11 个主导航；所有本地链接存在；无 console/page error；无 form/input/edit 控件。
- 需求和任务详情使用独立页面与返回按钮；无 drawer、dialog 或侧边详情栏。
- PM 总览固定 10 个管理要素；任务详情显示“目标与说明 / 当前状态 / 下一步”。
- 键盘首焦点为 skip link；打印样式隐藏导航；四视口均无横向 body overflow。
- 代码详情另在 1440×900 和 390×844 检查返回按钮、稳定符号锚点、定义签名、可聚焦滚动表格及长 ID 换行；手机宽度无 body overflow。
- axe-core 4.11.4 扫描总览桌面/手机、需求、任务、项目管理、代码详情桌面/手机 7 页：`violation_count=0`。渐变/状态色对比度仍有工具 incomplete，不冒充完整 WCAG 认证。
- 浏览器证据在 `/tmp/shanforge-project-site-browser/`，不提交 Git；本文件记录稳定结论。

## 自动验证

| 命令 | 结果 |
|---|---|
| `PYTHONPATH=src uv run pytest tests/test_project_knowledge_*.py tests/test_project_cli.py tests/test_project_site_renderer.py tests/test_system_task_integration.py -q` | `87 passed` |
| T05 三文件测试 | `8 passed` |
| Security + performance | `5 passed` |
| PM + site renderer + integration | `11 passed` |
| Skill / memory / docs 定向集合 | 本任务断言通过；同文件中 2 项 unrelated writing-plans 既有失败 |
| `uv run ruff check src tests` | passed |
| `uv run mypy src` | 279 source files，0 issue |
| 文档结构、完整会话路由、定向读取静态合同 | `15 passed` |
| `docs-stratego source validate` | exit 0；工具报告 `pages=0/contracts=0`，因此另以 34 Markdown、0 非 Markdown与导航测试补证，不把该输出夸大为正文覆盖 |
| `git diff --check` | exit 0；仅有无关 CRLF 提示 |
| `uv run ruff format --check`（本任务范围） | 40 files formatted |

## 全仓回归归属

全仓 `uv run pytest -q`：`1322 passed, 3 failed`。三个失败来自用户工作区中既有、非本任务的 `writing-plans` / `ui-ux-pro-max` skill 改动：

1. `test_prompt_review_target_skills_have_work_item_status_packages` 缺 `ui-ux-pro-max` 旧短语。
2. `test_local_status_and_needs_are_forwarded_without_normalization` 与 professional prefix Hash 均指向 `writing-plans` 既有契约变化。

本任务不修改这两个 skill。全仓 format 唯一剩余项是无关 `tests/test_task_workflow_semantics.py`；本任务 42 个文件均通过 format check。
