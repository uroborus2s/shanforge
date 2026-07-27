# T04 红绿测试与静态页面验证

- 工作项：`PK-SOURCE-MIGRATION-001`
- 任务：`PK-SOURCE-MIGRATION-001-T04`
- 验证日期：2026-07-23
- 验证对象：任务语义投影、任务详情可读化、需求验收树、静态站点

## 红灯证据

- `TEST-UNIT-PK-TASK-BRIEF-001`：新增任务简报语义提取测试后，`goal`、`work_items`、
  `deliverables` 等字段不存在，测试失败。
- `TEST-CONTRACT-PK-TASK-MERGE-001`：新增任务简报与 Ledger 同编号合并测试后，人类说明
  被较新的 Ledger 详情覆盖，测试失败。
- `TEST-UI-PK-REQUIREMENT-TREE-001`：新增需求四层树结构断言后，旧版扁平分类页面不满足，
  测试失败。
- `TEST-UI-PK-TASK-DETAIL-001`：新增任务四个首要说明区块断言后，旧版通用详情不满足，
  测试失败。
- 首轮结果：`4 failed`，失败点均与新增行为一一对应。
- 合并优先级补充红灯：将 Ledger 写入不同的 `goal` 后，测试再次出现 `1 failed`，证明
  旧合并顺序会丢失任务简报中的人类语义。

## 绿灯证据

- 四项新增行为测试修复后：`4 passed`。
- 合并优先级修复后：补充用例 `1 passed`。
- 项目知识目标测试：
  `uv run pytest tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py tests/test_project_knowledge_integration.py tests/test_prd_project_knowledge_requirements.py -q`
  最新结果：`64 passed in 1.39s`。
- 静态检查：
  `uv run ruff check src/runtime/project_knowledge/extractors.py src/settings/project_knowledge/sqlite_index.py src/runtime/project_knowledge/site_renderer.py tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py`
  结果：通过。
- 类型检查：`.venv/bin/mypy src`
  结果：`Success: no issues found in 279 source files`。

## CLI 快照

- 命令：
  `PYTHONPATH=src .venv/bin/python -m settings.composition.project_knowledge project snapshot --html --json`
- 生成号：
  `generation:03f3a471b44f3c39b899d2e980beff36a21daad5505cc94f353ea9aa3beba8ef`
- 结果：`parsed=2`、`rendered=8`、`reused=1909`。
- 最后有效站点：`.factory/cache/site/current/index.html`。
- HTML、SQLite 与 cache 仍为本地派生物，不进入 Git。

## 真实浏览器验证

- 浏览器：本机 Google Chrome，无头模式。
- 桌面视口：`1440 × 900`。
- 移动视口：`390 × 844`。
- 启动方式：直接打开 CLI 生成的 `file://` 静态页面；无服务端、无端口、无需关闭服务。
- 健康检查：入口和目标详情文件存在，页面可加载、可展开、可返回、深链可达。
- 需求页：存在 `产品 → 业务域 → 需求 → 验收标准` 四层树；共识别 17 个业务域、
  27 项需求和 64 条验收链接。
- 任务页：存在“为什么要做这项任务”“具体要做什么”“完成后得到什么”
  “怎样确认已经完成”四个首要区块，并能跳转到 `REQ-PKI-008`。
- 移动端：`scrollWidth=390`，无横向溢出。
- 控制台：错误数 `0`。
- API 验证：不适用，本任务没有 API 变更。
- 发布验证：不适用，本任务只生成本地只读静态快照。

## 截图

- `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-requirements-tree-desktop.png`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-task-detail-desktop.png`
- `.factory/workitems/PK-SOURCE-MIGRATION-001/evidence/T04-requirements-tree-mobile.png`

## 评审前门禁

- 2026-07-23 14:30（Asia/Shanghai）重新执行项目知识目标测试、Ruff 和 Mypy。
- 三项命令退出码均为 `0`，评审输入与当前实现一致。
