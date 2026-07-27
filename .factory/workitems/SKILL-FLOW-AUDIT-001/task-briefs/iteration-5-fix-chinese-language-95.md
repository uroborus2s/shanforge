# SKILL-FLOW-AUDIT-001 Iteration 5 Chinese Language Fix to 95+

## 目标

把 [chinese-language-review-iteration-5.md](../reviews/chinese-language-review-iteration-5.md) 中指出的问题修到下一轮中文语言评审预期 95 分以上。

本任务是实现任务，不是评审任务。完成后只能回写 `ready_for_review`，不得自批 `approved`。

## 必读输入

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/chinese-language-review-iteration-5.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/prompt-engineering-review-iteration-5.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/skill-flow-completeness-test-iteration-5.md`
- `skills/skill-creator/SKILL.md`
- `skills/gitcommitzh/SKILL.md`
- `skills/stratix-service/SKILL.md`
- `skills/stratix-admin-web/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/requirements-engineering/SKILL.md`

## 允许修改

- 上述 6 个 `SKILL.md`
- 这些 skill 已有 `references/` 中直接承接下沉内容的文件
- 对应结构测试：
  - `tests/test_skill_creator_skill_principles.py`
  - `tests/test_pr_commit_workflow_rules.py`
  - `tests/test_stratix_service_skill.py`
  - `tests/test_stratix_admin_web_skill.py`
  - `tests/test_sf_sp_010_documentation_navigation.py`
  - `tests/test_requirements_engineering_skill.py`
- 本任务自己的 report / evidence / review input
- `.factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl`

不要修改 memory；由主线程统一同步。

## 已知脏改动

当前工作区中 `skills/stratix-service/SKILL.md` 和 `skills/stratix-admin-web/SKILL.md` 已有触发边界收窄改动。保留并继续基于这些改动，不得回退。

## 修复要求

1. `skill-creator`：主入口只保留最小创建/修改流程、中文短句、评审隔离、状态包。评估、benchmark、描述优化、打包下沉到 references；核实或去掉无法确认的 `eval-viewer/generate_review.py`、`package_skill.py`、`.skill` 事实。
2. `gitcommitzh`：合并重复的授权、范围、提交信息一致性和真实 hash 回显规则。用一个分支表表达“只写草案 / 已授权提交 / blocked”。明确用户直接限制优先于自动提交触发。
3. `stratix-service`：主入口按解释、评审、小修、新项目、上线分级验证。生产化双项目矩阵、完整 CLI、加解密细节下沉到 references。补齐 `work_item` / `ledger_event`。
4. `document-templates`：把默认文档包、模板路径映射、迁移流程下沉到 references。主入口只保留判断、边界、治理规则、状态包和按需引用。
5. `requirements-engineering`：把 INVEST、AC 示例、NFR 示例、优先级教材下沉；去掉旧角色绑定口吻；收口 `requirements_ready` 和 `ready_for_review` 关系。
6. `stratix-service` 与 `stratix-admin-web`：收口 `web-admin/admin-page/admin-crud` 边界，确保后端 service 不承担后台前端页面开发规则。

## 验证

至少运行：

```bash
uv run pytest tests/test_skill_creator_skill_principles.py tests/test_pr_commit_workflow_rules.py tests/test_stratix_service_skill.py tests/test_stratix_admin_web_skill.py tests/test_sf_sp_010_documentation_navigation.py tests/test_requirements_engineering_skill.py
uv run ruff check tests/test_skill_creator_skill_principles.py tests/test_pr_commit_workflow_rules.py tests/test_stratix_service_skill.py tests/test_stratix_admin_web_skill.py tests/test_sf_sp_010_documentation_navigation.py tests/test_requirements_engineering_skill.py
git diff --check
```

## 输出

- `.factory/workitems/SKILL-FLOW-AUDIT-001/reports/iteration-5-fix-chinese-language-95-report.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/evidence/iteration-5-fix-chinese-language-95-verification.md`
- `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/iteration-5-fix-chinese-language-95-review-input.md`
- ledger event：`iteration-5-fix-chinese-language-95:implementation`
