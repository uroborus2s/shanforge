# SF-SP-004 iteration-2 评审输入简报

## 评审目标

确认 `writing-plans/references` 是否已经按中文短句完整重写，且没有遗留旧英文模板叙述。

## 修改文件

- `skills/writing-plans/references/workitem-plan-template.md`
- `skills/writing-plans/references/task-brief-template.md`
- `skills/writing-plans/references/plan-review-template.md`
- `tests/test_writing_plans_skill.py`

## 重点检查

- references 的标题、章节、字段、检查项和输出说明是否为中文。
- 是否保留了原 Superpowers 计划模板语义：目标、架构、技术栈、输入、范围、文件结构、TDD 步骤、验证命令、证据、评审门和 memory 同步。
- 是否只保留必要的代码标识符、路径、命令、状态值和产品名。
- 测试是否能防止旧英文模板回退。

## 验证摘要

- `tests/test_writing_plans_skill.py`：`3 passed`
- `tests/test_writing_plans_skill.py tests/test_execution_workflow_skills.py tests/test_superpowers_reference_migration.py`：`11 passed`
- ruff：通过
- `skills/writing-plans` validator：通过
- 旧英文模板短语扫描：无匹配
- 尾随空白和 `git diff --check`：通过

## 请求结论

请独立评审者给出 `approved` 或 `changes_requested`，并列出阻塞项。
