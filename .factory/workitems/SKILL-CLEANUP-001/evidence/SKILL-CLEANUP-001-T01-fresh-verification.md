# SKILL-CLEANUP-001-T01 新鲜验证

- 时间：`2026-07-27`
- 结论：`passed`

## 定向测试

```bash
uv run pytest -q tests/test_go_developer_skill.py tests/test_remaining_skill_project_status_contract.py tests/test_deprecated_skill_cleanup.py
```

- exit code：`0`
- 结果：`14 passed in 0.05s`

```bash
uv run pytest -q tests/test_crawler4j_model_skill_integration.py tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py tests/test_ui_ux_pro_max_skill.py -k 'not professional_prefixes_are_unchanged_for_exactly_31_work_skills and not local_status_and_needs_are_forwarded_without_normalization'
```

- exit code：`0`
- 结果：`19 passed, 2 deselected in 0.25s`
- 两个取消选择的测试依赖其他工作项尚未提交的冻结哈希和状态字段，不纳入本任务。

## 静态与差异检查

```bash
uv run ruff check tests/test_go_developer_skill.py tests/test_crawler4j_model_skill_integration.py tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py
```

- exit code：`0`
- 结果：`All checks passed!`

任务范围 `git diff --check`：

- exit code：`0`
- 结果：无错误。

## 目录、引用与全局链接

- `skills/skill-creator` 不存在。
- `skills/go-backend-developer` 不存在。
- `skills/go-developer/SKILL.md` 存在。
- 非历史文件未发现旧目录或本地 `skill-creator` 执行路径；命中项均为历史 summary。
- 仓内存在 `SKILL.md` 的 Skill：`37`。
- Codex 全局项目 Skill 软链接：`37`。
- 名称集合差异：`0`。
- 目标名称差异：`0`。
- `go-developer` 链接目标正确，`go-backend-developer` 与 `skill-creator` 全局旧链接均不存在。

第一次诊断脚本把没有 `SKILL.md` 的空目录 `skills/project-management/` 也计为 Skill，产生 `38 != 37` 的假失败。改用正式契约 `skills/*/SKILL.md` 计数后，仓内与全局集合完全一致；这不是实现缺陷，无需行为修改。

## Go 模板新鲜复验

按原批准版本把 `skills/go-developer/assets/service-template/` 渲染到临时目录后，
`go mod tidy`、`gofmt -d`、`go vet ./...`、`go test ./...` 和
`go test -race ./...` 全部退出 `0`。完整记录见
`.factory/workitems/GO-BACKEND-SKILL-001/evidence/TASK-SKILL-001-final-fresh-verification-20260727.md`。
