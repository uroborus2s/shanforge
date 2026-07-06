# Iteration 1 Verification

## 验证时间

2026-07-06

## 验证范围

- `.factory/workitems/SKILL-FLOW-AUDIT-001/`
- `tests/test_skill_flow_process_audit.py`

## 命令与结果

### 1. 结构测试

```text
uv run pytest tests/test_skill_flow_process_audit.py
```

首次运行结果：

```text
1 failed, 2 passed
```

失败原因：

- 新增测试断言查找 `review response`。
- 现有 `skills/receiving-code-review/SKILL.md` 使用的是 `response 已写入`。
- 产品 skill 已有对应语义，测试断言用词过死。

修正后重新运行：

```text
3 passed in 0.01s
```

### 2. Ruff

```text
uv run ruff check tests/test_skill_flow_process_audit.py
```

结果：

```text
All checks passed!
```

### 3. Ledger JSONL

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```

## 收尾验证：独立评审后 ledger 同步

### 命令与结果

```text
uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
11 passed in 0.02s
```

```text
uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
All checks passed!
```

```text
python3 -c 'import json, pathlib; paths=[pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"), pathlib.Path(".factory/memory/review-ledger.jsonl")]; [json.loads(line) for p in paths for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("jsonl ok")'
```

结果：

```text
jsonl ok
```

## 追加验证：brainstorming 流程契约修复

### 决策

- 按 `reviews/skill-flow-test-report.md` 修复 `brainstorming` 的工作 skill 路由口径冲突。
- `brainstorming` 现在只回写 brief、批准状态、outputs、evidence、ledger_event 和 `needs`。
- `using-shanforge` 继续拥有唯一流程路由权。
- 本轮不实现远端 PR / push / merge 闭环，不新增中心脚本。

### 命令与结果

```text
uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
11 passed in 0.01s
```

```text
uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
All checks passed!
```

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```

## 追加验证：brainstorming 流程契约修复

### 决策

- `brainstorming` 只输出 brief、批准状态、产物路径、证据、ledger_event 和 `needs`。
- 删除状态回写包中的 `下一步 skill` 字段。
- 保留 `using-shanforge` 拥有流程路由的断言。

### 命令与结果

```text
uv run pytest tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
11 passed in 0.01s
```

```text
uv run ruff check tests/test_brainstorming_skill.py tests/test_skill_flow_process_audit.py tests/test_requirements_engineering_skill.py
```

结果：

```text
All checks passed!
```

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```

## 追加验证：requirements-engineering 流程契约修复

### 决策

- 修复 `requirements-engineering` 主文件缺少 Shanforge 输出契约的问题。
- 新增 `tests/test_requirements_engineering_skill.py` 固定输出路径、ledger、memory sync、状态包和自批禁止项。
- 不修改共享 `.factory/memory/tasks.summary.md`，避免混入当前工作区已有脏改动。

### 首次宽范围验证

```text
uv run pytest tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py tests/test_skill_flow_process_audit.py
```

结果：

```text
1 failed, 8 passed
```

失败项：

- `tests/test_superpowers_reference_migration.py::test_workflow_template_migration_progress_is_tracked`
- 失败原因是 `.factory/memory/tasks.summary.md` 缺少旧断言文本 `` `SF-SP-001/002/003/004/005/006/007` 已人工确认``。
- 该失败属于既有共享 memory 口径，不是本轮 `requirements-engineering` 修复引入。

### 本轮相关验证

```text
uv run pytest tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py::test_existing_skills_have_migrated_reference_templates tests/test_skill_flow_process_audit.py
```

结果：

```text
6 passed in 0.01s
```

```text
uv run pytest tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
9 passed in 0.02s
```

```text
uv run ruff check tests/test_requirements_engineering_skill.py tests/test_superpowers_reference_migration.py tests/test_skill_flow_process_audit.py tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
All checks passed!
```

```text
python3 skills/skill-creator/scripts/quick_validate.py skills/requirements-engineering
```

结果：

```text
Skill is valid!
```

```text
rg -n 'requirements_ready|不得把工作项写成|流程路由由 `using-shanforge` 判断|\.factory/workitems/<WORKITEM-ID>/ledger\.jsonl|\.factory/memory/prd\.summary\.md' skills/requirements-engineering/SKILL.md tests/test_requirements_engineering_skill.py
```

结果：

```text
命中 `requirements-engineering/SKILL.md` 和 `tests/test_requirements_engineering_skill.py` 中的目标契约。
```

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```

## 未运行项

- 未跑全仓测试。当前工作区已有大量既有脏改动，本轮只验证新增流程审计产物。
- 未创建 PR、未 push、未 commit。

## 结论

本轮新增 work item 文件、两份子任务报告归档、流程说明和结构测试通过定向验证。状态只能记为 `self_check_passed`，正式关闭仍需独立 review 和人工确认。

## 追加验证：未接入开发流程的 skill 删除

### 决策

- 删除 `skills/find-skills`。
- 删除 `skills/web-artifacts-builder`。
- 保留 `skills/ai-regression-testing`、`skills/agent-harness-construction`、`skills/ai-first-engineering`。

保留原因：

- `ai-regression-testing` 仍在 `using-shanforge` 的 Bug / 验证失败路由和 Superpowers 流程方案中。
- `agent-harness-construction` 仍在当前流程方案的项目所需 skill 清单中。
- `ai-first-engineering` 仍在当前流程方案和根因修复纪律测试中。

### 命令与结果

```text
uv run pytest tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
9 passed in 0.02s
```

```text
uv run ruff check tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
All checks passed!
```

```text
uv run pytest tests/test_skill_flow_process_audit.py
```

结果：

```text
3 passed in 0.01s
```

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```

## 追加验证：backend-patterns 删除

### 决策

- 删除 `skills/backend-patterns`。
- 从 `.factory/project.json`、`config/software-factory.defaults.json` 和 Superpowers 流程方案中移除活跃引用。
- 保留历史审计报告中的 `backend-patterns` 评分记录。

### 命令与结果

```text
rg -n "backend-patterns" skills/using-shanforge .factory/project.json config/software-factory.defaults.json docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md
```

结果：

```text
无输出，exit code 1，表示活跃流程和配置中未命中 backend-patterns。
```

```text
python3 -m json.tool .factory/project.json
python3 -m json.tool config/software-factory.defaults.json
```

结果：

```text
两个 JSON 文件均可解析。
```

```text
uv run pytest tests/test_skill_flow_process_audit.py tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
12 passed in 0.02s
```

```text
uv run ruff check tests/test_skill_flow_process_audit.py tests/test_deprecated_skill_cleanup.py tests/test_bug_fix_root_cause_skill_rules.py
```

结果：

```text
All checks passed!
```

```text
python3 -c 'import json, pathlib; p=pathlib.Path(".factory/workitems/SKILL-FLOW-AUDIT-001/ledger.jsonl"); [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]; print("ledger jsonl ok")'
```

结果：

```text
ledger jsonl ok
```
