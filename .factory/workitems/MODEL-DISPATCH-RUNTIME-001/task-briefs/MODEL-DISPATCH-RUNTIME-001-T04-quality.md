# 任务简报：T04 集中质量与干净克隆

## 工作项

- 工作项：`MODEL-DISPATCH-RUNTIME-001`
- 任务：`MODEL-DISPATCH-RUNTIME-001-T04`
- 状态：`draft`
- 优先级：`P1`
- 任务层级：`system`
- 关联目标：`MODEL-DISPATCH-RUNTIME-001`
- 强关系：`DEPENDS_ON`
- 依赖：`T01`、`T02`、`T03`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- risk_level: `medium`
- execution_model: `gpt-5.6-terra`
- execution_authorized: `true`
- write_policy: `state_or_gate_write`
- current_gate: `T04_independent_review`
- dispatch_role: `reviewer`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `high`
- fork_turns: `none`
- route_reason: 独立评审需跨全部变更判断正确性、缺口和测试充分性。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 允许动作

- reviewer 只读检查本 WorkItem 候选与验证证据。
- Sol 运行验证、精确暂存、调用 `gitcommitzh`、创建临时干净克隆和回写本 WorkItem/memory。

## 禁止动作

- reviewer 不得写文件；不得 push、PR、merge、发布或部署。

## 完成口径

- 独立 Terra reviewer 结论为 approved，Critical/Important 为 0。
- 精确候选与最终干净克隆完整质量门全绿。
- WorkItem 有真实 Luna/Terra 派发回执、人类可读测试报告、提交哈希和关闭事件。

## 验证命令

```bash
uv run pytest
uv run ruff check .
for skill_dir in skills/*; do [ -f "$skill_dir/SKILL.md" ] || continue; uv run python "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" "$skill_dir" || exit 1; done
python3 -c 'import json,tomllib; from pathlib import Path; tomls=[Path("pyproject.toml"), *sorted(Path(".codex").rglob("*.toml"))]; [tomllib.loads(path.read_text()) for path in tomls]; jsons=sorted(Path(".factory").rglob("*.json")); jsonls=sorted(Path(".factory").rglob("*.jsonl")); [json.loads(path.read_text()) for path in jsons]; [[json.loads(line) for line in path.read_text().splitlines() if line] for path in jsonls]; print(f"TOML {len(tomls)}, JSON {len(jsons)}, JSONL {len(jsonls)} valid")'
git diff --check
```

期望：完整 pytest 0 failed/error/skipped/not_run；Ruff、38/38 Skill、TOML/JSON/JSONL 和 diff check 全部 exit code `0`。
