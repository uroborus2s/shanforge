# SF-SP-008 测试证据

- Work item：`SF-SP-008`
- 状态：`ready_for_review`
- 时间：`2026-07-05T13:17:18+08:00`

## 已执行

红测：

```bash
.venv/bin/pytest tests/test_pr_commit_workflow_rules.py
```

首次结果：`4 failed`。失败点为 `gitcommitzh` 缺 PR 闭环前置检查、缺 `pr-closure-checklist.md`、流程总控缺提交门、正式计划未记录 `SF-SP-008` 规则。

绿测：

```bash
.venv/bin/pytest tests/test_pr_commit_workflow_rules.py
```

结果：`4 passed`。

联合回归：

```bash
.venv/bin/pytest tests/test_pr_commit_workflow_rules.py tests/test_superpowers_reference_migration.py tests/test_execution_workflow_skills.py tests/test_review_workflow_skills.py tests/test_independent_review_gate.py tests/test_verification_debugging_workflow_skills.py tests/test_writing_plans_skill.py
```

结果：`32 passed`。

```bash
.venv/bin/ruff check tests/test_pr_commit_workflow_rules.py tests/test_superpowers_reference_migration.py
```

结果：`All checks passed!`。

```bash
python3 skills/skill-creator/scripts/quick_validate.py skills/gitcommitzh
python3 skills/skill-creator/scripts/quick_validate.py skills/using-shanforge
```

结果：两个 skill validator 均通过。

```bash
python3 -m json.tool .factory/project.json
```

结果：JSON 解析通过。

```bash
python3 - <<'PY'
import json
from pathlib import Path
for path in [
    '.factory/workitems/SF-SP-005/ledger.jsonl',
    '.factory/workitems/SF-SP-006/ledger.jsonl',
    '.factory/workitems/SF-SP-007/ledger.jsonl',
    '.factory/workitems/SF-SP-008/ledger.jsonl',
    '.factory/memory/review-ledger.jsonl',
]:
    for idx, line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        if line.strip():
            json.loads(line)
    print(f'{path}: ok')
PY
```

结果：5 个 JSONL 文件均解析通过。

```bash
git diff --check
```

结果：通过，无输出。

## 结论

`SF-SP-008` 实现已具备新鲜验证证据，当前可进入独立 review。
