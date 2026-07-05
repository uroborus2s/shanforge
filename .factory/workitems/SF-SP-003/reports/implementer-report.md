# SF-SP-003 Implementer Report

- Work item：`SF-SP-003`
- 实现者状态：`partial_ready_for_review`
- 范围：已有 skill 的 references 模板迁移切片。
- 日期：2026-07-05

## 本次完成

- 新增 `tests/test_superpowers_reference_migration.py`，用测试固定 references 迁移和未完成边界。
- 新增 `skills/requirements-engineering/references/prd-template.md`。
- 新增 `skills/document-templates/references/technical-design-template.md`。
- 新增 `skills/tdd-workflow/references/root-cause-checklist.md`。
- 新增 `skills/tdd-workflow/references/evidence-report-template.md`。
- 新增 `skills/gitcommitzh/references/commit-message-rubric.md`。
- 更新对应 `SKILL.md`，让主流程能指向新增 references。
- 更新 `tasks.summary.md`，明确未来 workflow skill 的 references 仍待随对应 skill 创建迁移。

## 未完成

- `writing-plans` 的 work item plan 和 task brief 模板尚未迁移。
- `requesting-code-review` 的 task review / PR review / 独立 review task 模板尚未迁移。
- `verification-before-completion` 的完成证据模板尚未迁移。
- `systematic-debugging` 的根因定位流程尚未作为独立 workflow skill 创建。

## 风险

- 本切片只覆盖已有 skill，不能代表 `SF-SP-003` 整体关闭。
- 后续创建 workflow skill 时，需要继续按 `skill-creator` 的含义保留清单和独立 review gate 执行。

## 验证

见 `evidence/test-report.md`。

## 下一步

- 先对本切片做 task review。
- review 通过后，继续 `SF-SP-004`，创建并本地化 `writing-plans`。
