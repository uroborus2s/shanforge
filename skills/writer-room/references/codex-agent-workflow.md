# Codex Agent Workflow

The parent Codex instance is the only coordinator. Child agents should not spawn
more agents, ask the user, or change shared files unless explicitly assigned a
disjoint write set.

If you are a child agent executing a single role card, do not inspect or require
the sub-agent tool. Complete your role and return the artifact envelope. Missing
`spawn_agent` is only a parent-coordinator blocker.

## Default Spawn Pattern

Use a worker sub-agent with a narrow prompt:

```text
You are the <role> in a Codex-native writer room.
Read this task card:
<contents of skills/writer-room/agents/<role>.md>

Project contract:
<brief artifact contract summary>

Inputs:
<only the artifacts this role needs>

Return only the structured envelope and complete artifact contents.
Do not edit files directly.
```

Do not set a model override unless the user explicitly requests one. Use the
inherited Codex model.

## Parallelism

Only parallelize independent roles:

- After `{episode-id}/script/episode-outline.md`, run `character-agent` and
  `scene-agent` in parallel.
- Keep `dialogue-agent` blocked until both character and scene artifacts are ready.
- Keep review and rewrite sequential because each depends on the previous report.

## Parent Responsibilities

The parent Codex coordinator must:

- write project files from returned artifacts;
- append one JSONL record per child agent to
  `{episode-id}/logs/writer-room-agent-calls.jsonl`;
- preserve warnings instead of hiding them;
- run the scoring gate and optional rewrite loop;
- summarize the final result for the user.

## Recovery

If a child agent returns `blocked`, the parent should decide whether the missing
input can be inferred safely. If not, ask the user one concise question.

If a child agent returns malformed JSON or missing artifact content, ask that
same agent to resend the envelope once. If it fails again, the parent may repair
formatting only when the creative content is unambiguous; otherwise mark the
run `warning` and continue only if downstream agents can still work.
