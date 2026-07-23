# PK-SOURCE-MIGRATION-001 独立实现评审输入

## 评审对象

- `docs/04-product/prd.md`
- `docs/05-design/data-design.md`
- `docs/05-design/frontend-design.md`
- `.factory/project-knowledge/source-registry.json`
- `.factory/project-knowledge/relation-declarations.json`
- `src/runtime/project_knowledge/extractors.py`
- `src/runtime/project_knowledge/site_renderer.py`
- `src/settings/project_knowledge/sqlite_index.py`
- `src/settings/project_knowledge/pm_projection.py`
- `src/settings/project_knowledge/site_publisher.py`
- `src/settings/composition/project_knowledge.py`
- 本任务新增/修改测试和工作项包

## 必读

- `brief.md`
- `plan.md`
- `reviews/review-feedback-triage.md`
- `reviews/review-response.md`
- `evidence/implementation-verification.md`
- `reports/implementer-report.md`

## 重点问题

1. PRD 是否与冻结 R009 的 ID、标题、优先级、规范语句、AC 和 NFR 字段等价。
2. R009 requirement contract 是否只退出当前来源而未破坏 PM map/manifest/R014。
3. task brief 与多 ledger 是否通过 canonical task ID 稳定合并；九个端点和 88 条边是否完整。
4. warm migration、cold rebuild、章节定位和 AC parent/order/status 是否一致。
5. Markdown 正文读取和渲染是否 fail-closed，是否存在 symlink、TOCTOU、scheme、
   权限或缓存失效漏洞。
6. 需求、任务、代码、测试和文档详情路由是否都指向真实页面/锚点。

## 验证结论门

- Critical = 0。
- Important = 0。
- 无需新增人工产品决定；若只有同范围实现问题，直接给出整改项。
