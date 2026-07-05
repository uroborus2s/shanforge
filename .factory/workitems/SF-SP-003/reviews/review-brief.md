# SF-SP-003 Review Brief

- Work item：`SF-SP-003`
- Review 类型：Spec Review + Quality Review
- Review 范围：已有 skill references 迁移切片。
- 请求状态：`review_requested`

## 输入

- `tests/test_superpowers_reference_migration.py`
- `.factory/workitems/SF-SP-003/reports/implementer-report.md`
- `.factory/workitems/SF-SP-003/evidence/test-report.md`
- `skills/requirements-engineering/SKILL.md`
- `skills/requirements-engineering/references/prd-template.md`
- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/technical-design-template.md`
- `skills/tdd-workflow/SKILL.md`
- `skills/tdd-workflow/references/root-cause-checklist.md`
- `skills/tdd-workflow/references/evidence-report-template.md`
- `skills/gitcommitzh/SKILL.md`
- `skills/gitcommitzh/references/commit-message-rubric.md`
- `.factory/memory/tasks.summary.md`

## Spec Check

- 检查已有 skill 是否都有对应 references。
- 检查 references 是否只承载模板、rubric、清单和固定方法。
- 检查实现报告是否明确未来 workflow skill 仍未完成。
- 检查测试是否防止提前把 `SF-SP-003` 标记为整体完成。

## Quality Check

- `SKILL.md` 不应塞入长模板正文。
- references 内容应是中文短句，能直接指导后续工作。
- 测试不应绑定无关文本或无关旧实现。
- memory 更新应表达部分完成，而不是完成。
