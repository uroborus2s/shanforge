# go-developer 改名与全局链接同步验证

## 基本信息

- Work item：`SKILL-CLEANUP-001`
- Actor：Codex
- 时间：`2026-07-22T23:52:30+08:00`
- 验证声明：仓内 `go-backend-developer` 已改名为 `go-developer`，Codex 全局项目 Skill 软链接与仓内 Skill 集合完全一致。
- 结论：`passed`

## 变更结果

- 仓内目录改名为 `skills/go-developer`。
- `SKILL.md` 的 `name`、标题和状态包 Skill 名已改为 `go-developer`。
- 测试文件改名为 `tests/test_go_developer_skill.py`，相关集合与冻结哈希契约已更新。
- 删除全局失效链接 `~/.codex/skills/skill-creator`。
- 删除全局旧名称链接 `~/.codex/skills/go-backend-developer`。
- 创建全局链接 `~/.codex/skills/go-developer -> /Users/uroborus/AiProject/shanforge/skills/go-developer`。
- `.system` 和 `codex-primary-runtime` 未修改。

## 新鲜验证

### Skill 与退役契约测试

```bash
uv run pytest -q tests/test_go_developer_skill.py tests/test_remaining_skill_project_status_contract.py tests/test_deprecated_skill_cleanup.py
```

- exit code：`0`
- 结果：`14 passed`
- 失败：`0`
- 跳过：`0`

### Ruff

```bash
uv run ruff check tests/test_go_developer_skill.py tests/test_remaining_skill_project_status_contract.py tests/test_work_skill_status_envelope_ownership.py
```

- exit code：`0`
- 结果：`All checks passed!`

### 旧名称扫描

- `skills/go-backend-developer` 不存在。
- `skills/go-developer/SKILL.md` 存在。
- 非历史文件中未发现 `go-backend-developer` 或 `skills/go-backend-developer`。
- exit code：`0`

### 全局链接集合

- 仓内 Skill：`37`。
- Codex 全局项目软链接：`37`。
- 名称集合差异：`0`。
- 目标路径差异：`0`。
- 失效软链接：`0`。
- exit code：`0`

## 偏离与残余风险

- 系统 `quick_validate.py` 未运行；当前环境缺少其 `PyYAML` 依赖。改名后的 frontmatter、目录名、状态包和资源完整性由定向测试覆盖。
- 当前任务已经加载的 Skill 列表可能继续显示旧快照；新建或重新加载 Codex 任务后刷新。

## 结论

改名和全局链接同步验证通过。实现状态为 `ready_for_review`，不代表独立 reviewer 已批准。
