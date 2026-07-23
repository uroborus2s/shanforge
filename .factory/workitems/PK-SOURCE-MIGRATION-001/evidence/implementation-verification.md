# PK-SOURCE-MIGRATION-001 实施验证

## 冻结输入

- R009 requirement contract SHA-256：
  `53923f55c2bcc16bce6ad60ed1045c671dd490b6733885725641fe39e6859977`
- R009 PM field map SHA-256：
  `17af8c254017bc60eb44e73b8e61322bc57eb577ffa6baa2711f100d48251055`
- R009 final manifest SHA-256：
  `8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae`
- 冻结文件均未修改。

## 自动化验证

- 任务范围：
  `PYTHONPATH=src .venv/bin/python -m pytest tests/test_prd_project_knowledge_requirements.py tests/test_project_knowledge_extractors.py tests/test_project_knowledge_index.py tests/test_project_site_renderer.py tests/test_project_knowledge_security.py tests/test_project_knowledge_pm.py tests/test_project_knowledge_integration.py -q`
  → `62 passed`
- 静态检查：`.venv/bin/ruff check src tests` → `All checks passed`
- 类型检查：`PYTHONPATH=src .venv/bin/mypy src`
  → `Success: no issues found in 279 source files`
- 全仓：`PYTHONPATH=src .venv/bin/python -m pytest -q`
  → `1342 passed, 3 failed`。三个失败分别位于
  `test_skill_flow_process_audit.py` 和
  `test_work_skill_status_envelope_ownership.py`，目标是本任务未修改的
  `skills/ui-ux-pro-max/SKILL.md`、`skills/writing-plans/SKILL.md`；与已有全仓
  验证记录中的三项范围外 Skill 合同失败一致。

## 冷重建与 SQL

- `project index rebuild --json` 成功，来源 599，失败来源 0。
- `REQ-PKI-*`：16；`NFR-PKI-*`：11；`REQ-PKI-*` AC：64。
- 27 个 REQ/NFR 的 `source_section_key` 均非空且与同 ID
  `pk_document_section.section_id` 精确对应。
- AC `unknown`：0；R009 requirement contract 当前 `pk_source`：0。
- 九个实施任务端点均存在，`Task --IMPLEMENTS--> REQ/NFR` 强关系：88。
- 八个曾由旧 ledger JSONL 投影的实施任务均有 v4 source-scoped ID →
  canonical ID alias；`TASK-IMPLEMENT-003-P001-T05` 只有 task brief、没有旧 JSONL
  实体，因此无可迁移 alias。
- warm JSON→PRD refresh 与 cold PRD rebuild 的 requirement、AC、section、
  locator 和 edge after-image 完全一致。

## 站点与缓存

- `project snapshot --html --rebuild --json` 成功，随后增量发布当前工作项整改记录：
  当前共 1892 页，原子发布当前入口。
- 三个本任务详情页使用 canonical 任务编号和中文标题；机器身份不再取
  `display_name`，不存在“任务标题待补充”。
- 紧接零变化运行：`cache_hit=true`、`rendered_pages=0`、`reused_pages=1892`。
- Playwright 本地静态页断言：需求顶层 27、`REQ-PKI-004` 验收锚点 4、
  需求→任务深链存在、任务→需求深链 10、PRD 正文可读、移动端看板 6 列、
  控制台错误 0。
- 安全负例覆盖：raw HTML、`javascript:`、Hash mismatch、路径逃逸、
  symlink、超 2 MiB、restricted 正文在 shared profile 中不可见。

## 工作 Skill 回写

- work_item: `PK-SOURCE-MIGRATION-001`
- skill: `webapp-testing`
- status: `completed`
- outputs:
  - `.factory/cache/site/current/index.html`
- evidence:
  - 本文件中的 Playwright DOM、深链、响应式和控制台断言
- ledger_event: `PK-SOURCE-MIGRATION-001:completed:v1`
- needs:
  - none

## 任务详情可读性增补

- 用户验收反馈：任务详情不展示 locator path、`block_sha256`、内部 document ID 或
  原始 DTO；应直接展示可点击的关联需求和相关设计。
- Red：
  `pytest` 定向执行 → `3 failed`，分别证明旧模板仍显示“定向来源”、没有独立的
  “关联需求 / 相关设计”区域、`FLOW-TASK-011` 没有需求关系。
- Green：项目站点、PRD 关系声明、索引与安全相关回归 → `41 passed`；
  Ruff 通过；Mypy 通过。
- 真实冷重建：来源 599、失败 0；`FLOW-TASK-011 --IMPLEMENTS--> REQ-PKI-008`
  与 `doc:DESIGN-FRONTEND-001 --SATISFIES--> REQ-PKI-008` 均已落入 SQLite。
- Playwright 从 `tasks/FLOW-TASK-011.html` 实际点击：
  - 需求“可商用的只读多页面项目站点” → `requirements/REQ-PKI-008.html`
  - 设计“前端架构与页面设计” → `design/DESIGN-FRONTEND-001.html`
  - 六类内部字段不可见，控制台错误 0。
- 临时截图：`/private/tmp/FLOW-TASK-011-traceability.png`，不进入 Git。
- 独立评审 UI-I1 整改：仅接受 outgoing strong Task→Requirement，以及
  Requirement 侧 incoming strong `SATISFIES` Design；删除直接 Task→Design 旁路。
- 三类攻击负例（weak requirement、非 `SATISFIES` design、direct task-design）
  均未进入任务详情；完整项目知识回归 `62 passed`，Ruff、Mypy 通过。
- `ProjectSiteRenderer/v10` 增量发布后再次通过真实页面点击与六类内部字段隐藏断言，
  控制台错误 0。
- 同一独立 reviewer 复审：`approved / 99 / C0-I0-M0`，UI-I1 关闭，无需人工确认。
