# SF-SP-003 Existing Skill References Evidence

- Work item：`SF-SP-003`
- 范围：已有 skill 的 references 模板迁移切片。
- 状态：`partial_ready_for_review`
- 日期：2026-07-05

## Red

- 命令：`.venv/bin/pytest tests/test_superpowers_reference_migration.py`
- 结果：失败，`2 failed`
- 失败原因：
  - 缺少 `skills/requirements-engineering/references/prd-template.md`
  - `.factory/memory/tasks.summary.md` 未记录“未来 workflow skill 的 references 仍待随对应 skill 创建迁移”

## Green

- 命令：`.venv/bin/pytest tests/test_superpowers_reference_migration.py`
- 结果：`2 passed`

- 命令：`.venv/bin/ruff check tests/test_superpowers_reference_migration.py`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/requirements-engineering`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/document-templates`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/tdd-workflow`
- 结果：通过

- 命令：`.venv/bin/python skills/skill-creator/scripts/quick_validate.py skills/gitcommitzh`
- 结果：通过

## 覆盖点

- `requirements-engineering` 已新增 PRD 模板。
- `document-templates` 已新增技术设计模板。
- `tdd-workflow` 已新增根因定位清单和 evidence 报告模板。
- `gitcommitzh` 已新增提交说明 rubric。
- `tasks.summary.md` 已明确未来 workflow skill 的 references 不能提前标记完成。

## 偏离

- `uv` 当前不在 PATH，本轮沿用仓库 `.venv/bin/*` 执行验证。
- `SF-SP-003` 尚未整体完成；`writing-plans`、`requesting-code-review`、`verification-before-completion`、`systematic-debugging` 的 references 需随对应 skill 创建继续迁移。
