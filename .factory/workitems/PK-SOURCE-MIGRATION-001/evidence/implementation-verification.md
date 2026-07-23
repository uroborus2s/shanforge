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
