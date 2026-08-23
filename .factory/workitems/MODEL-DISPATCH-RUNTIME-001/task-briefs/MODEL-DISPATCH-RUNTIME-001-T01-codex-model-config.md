# 任务简报：T01 Codex 原生模型配置

## 工作项

- 工作项：`MODEL-DISPATCH-RUNTIME-001`
- 任务：`MODEL-DISPATCH-RUNTIME-001-T01`
- 状态：`completed`
- 优先级：`P1`
- 任务层级：`system`
- 关联目标：`MODEL-DISPATCH-RUNTIME-001`
- 强关系：`IMPLEMENTS`

## 模型路由

- control_model: `gpt-5.6-sol`
- task_complexity: `simple`
- risk_level: `low`
- execution_model: `gpt-5.6-luna`
- execution_authorized: `true`
- write_policy: `source_or_test_write`
- current_gate: `closed`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- requested_reasoning_effort: `low`
- fork_turns: `none`
- route_reason: 机械的项目配置切片，接口已由 Sol 锁定且可用单一解析检查证明。
- escalation_triggers: `scope_expanded | input_conflict | risk_increased | verification_failed_twice | human_gate`

## 目标

创建 Codex 原生项目配置：Sol 为主控制模型；Luna/Terra 是受限执行者；Terra reviewer 只读。配置必须能被 Python 标准库解析。

## 允许修改

- `.codex/config.toml`
- `.codex/agents/luna-worker.toml`
- `.codex/agents/terra-worker.toml`
- `.codex/agents/terra-reviewer.toml`

## 禁止修改

- 其他所有文件；不得提交、推送或扩大配置能力。

## 完成口径

- 四个 TOML 均可由 `tomllib` 解析。
- 主配置明确 `model = "gpt-5.6-sol"`、`agents.enabled = true`、并发上限为 3。
- worker 的模型与推理强度分别为 Luna/low、Terra/medium；reviewer 为 Terra/high 且只读。
- 返回真实文件清单、命令结果和 concerns；不得自批 approved。

## 验证命令

```bash
uv run python -c 'import tomllib; from pathlib import Path; files=[Path(".codex/config.toml"), *sorted(Path(".codex/agents").glob("*.toml"))]; data=[tomllib.loads(p.read_text()) for p in files]; assert data[0]["model"]=="gpt-5.6-sol" and data[0]["model_reasoning_effort"]=="high"; agents={d["name"]: d for d in data[1:]}; assert agents["luna-worker"]["model"]=="gpt-5.6-luna" and agents["terra-worker"]["model"]=="gpt-5.6-terra" and agents["terra-reviewer"]["sandbox_mode"]=="read-only"; print("4 TOML profiles valid")'
```

期望：`4 TOML profiles valid`，exit code `0`。
