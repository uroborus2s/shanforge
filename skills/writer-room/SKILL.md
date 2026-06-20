---
name: writer-room
description: Codex-native writer room orchestration for producing series bibles, episode scripts, short dramas, screenplays, script rewrites, script-doctor reviews, final canon writeback, and self-evolving writing-room artifacts. Use when the user asks for a 编剧室, 编辑室, writer room, screenwriting agent team, AI drama story foundation, Codex sub-agents writing a script, self-evolving script workflow, or wants every writing agent to be performed by Codex rather than by Python code or an app LLM provider.
---

# Writer Room

Use this skill to run a Codex-native writer room. The parent Codex instance acts as
the producer/coordinator, and each writing role is delegated to a Codex sub-agent
with a bounded task card.

## Operating Model

- Treat Codex as the runtime. Do not implement a Python agent loop and do not call
  a project LLM provider for the child agents.
- The parent coordinator uses `multi_agent_v1.spawn_agent` when available. Spawn
  child agents only because the user explicitly requested Codex agents or a
  writer-room team.
- A child agent executing one role card must not require `spawn_agent`; it should
  perform its assigned role and return the artifact envelope.
- Keep the parent in charge of orchestration, artifact assembly, quality gates,
  and user-facing questions.
- Keep child agents focused on one role and one handoff. Pass only the required
  artifact text and that role's task card.
- Have child agents return structured artifact content. The parent writes the
  actual files into the project folder unless the user explicitly requests direct
  worker edits.
- If the parent coordinator has no sub-agent tool, state that the exact "each
  agent is Codex" requirement is blocked and ask whether to continue with
  parent-only simulation.
- Writer Room owns story facts only. It does not generate image assets, video
  prompts, render manifests, audio files, ComfyUI parameters, edit decisions, or
  post-production deliverables.

## Production Modes

- `series mode`: create the whole-series story foundation and canonical bibles.
- `episode mode`: create the episode brief, outline, draft, final script,
  continuity report, and score.
- `writeback mode`: write only final confirmed cut facts into story continuity
  and memory after downstream production completes.
- `migration mode`: map legacy story files into canonical Writer Room paths and
  record missing story backfill without letting downstream departments read
  `legacy/` as a fixed input.

## Project Layout

Create or reuse one shared production project directory per series/project.
The project root is always:

```text
./project/{project-name}/
```

Project-level folders hold cross-episode material:

```text
./project/{project-name}/
  project.json
  bible/world.md
  bible/geography.md
  bible/factions.md
  bible/timeline.md
  outline/series-outline.md
  outline/episode-outline-index.md
  synopsis/story-synopsis.md
  bible/characters.md
  bible/scenes.md
  bible/continuity.md
  bible/visual-style.md
  memory/current-state.md
  memory/failure-patterns.json
  memory/evolution-notes.md
```

Writer Room writes episode outputs under a zero-padded episode directory:

```text
./project/{project-name}/{episode-id}/
  brief/episode-brief.md
  script/episode-outline.md
  script/script-v01.md
  script/final-script.md
  reports/critique-v01.md
  reports/continuity-report.md
  reports/script-score.md
  logs/writer-room-agent-calls.jsonl
  memory/current-state.md
  memory/failure-patterns.json
  memory/evolution-notes.md
```

Use a user-provided `./project/{project-name}/` path when present. Otherwise
create a short slug under `project/`. Use `01`, `02`, `03`, ... as episode IDs
unless the user provides another stable numbering convention. Do not create a
writer-room-specific root. `{episode-id}/script/final-script.md`,
`bible/characters.md`, `bible/scenes.md`,
`{episode-id}/reports/continuity-report.md`, and
`{episode-id}/reports/script-score.md` are the fixed handoff contract for the
next department. `{episode-id}/logs/writer-room-agent-calls.jsonl` is the fixed
coordinator log path for the episode.

For legacy projects, keep original material read-only under `legacy/` and record
story mapping in `migration/migration-map.json`,
`migration/backfill-plan.md`, and `migration/migration-report.md`. Only
canonical files under the shared project root become downstream inputs.

## References

Load only what is needed:

- `references/codex-agent-workflow.md`: coordinator workflow and spawn prompts.
- `references/artifact-contract.md`: required envelope and artifact format.
- `references/rubric.md`: script scoring rubric and rewrite gate.
- `agents/*.md`: one task card per child agent. Do not treat `agents/openai.yaml`
  as a role card.
- `assets/templates/*.md`: optional output skeletons.
- `schemas/*.json`: structural contracts for validation or test authoring.

## Workflow

1. Normalize the user request into project and episode context:
   `seed`, `format`, `duration`, `genre`, `tone`, `audience`, `constraints`,
   `video_readiness`, `revision_budget`, `project_name`, `episode_id`, and
   `production_mode`.
2. Create `project.json` with project id, input, requested outputs, status, and
   the planned agent sequence when it does not exist. Create or update
   `{episode-id}/brief/episode-brief.md` for the current episode.
3. In `series mode`, create or refresh `bible/world.md`,
   `bible/geography.md`, `bible/factions.md`, `bible/timeline.md`,
   `bible/characters.md`, `bible/scenes.md`, `bible/continuity.md`,
   `bible/visual-style.md`, `outline/series-outline.md`,
   `outline/episode-outline-index.md`, and `synopsis/story-synopsis.md`.
4. In `episode mode`, run the blocking agents in order:
   `showrunner-agent` -> `story-architect-agent`.
5. Run `character-agent` and `scene-agent` in parallel after
   `{episode-id}/script/episode-outline.md` exists.
6. Run `dialogue-agent` after the episode brief, episode outline, character
   bible, and scene bible exist.
7. Run `script-doctor-agent` on `{episode-id}/script/script-v01.md`.
8. Run `rewrite-agent` using the critique.
9. Run `continuity-agent`, then `script-evaluator-agent`.
10. If the score is below the target, default `85`, run one doctor/rewrite/check
   loop unless the user requested a different revision budget.
11. In `writeback mode`, read only confirmed delivery/QC facts, then update
    `bible/continuity.md`, project `memory/current-state.md`, and episode
    memory. Never write failed renders, discarded assets, or experimental audio
    takes into story canon.
12. Run `memory-librarian` and `learning-evolution-agent`.
13. Return the project root, final script path, score, warnings, and recommended
    next actions.

## Agent Sequence

Use these task cards:

```text
agents/showrunner-agent.md
agents/story-architect-agent.md
agents/character-agent.md
agents/scene-agent.md
agents/dialogue-agent.md
agents/script-doctor-agent.md
agents/rewrite-agent.md
agents/continuity-agent.md
agents/script-evaluator-agent.md
agents/memory-librarian.md
agents/learning-evolution-agent.md
```

## Quality Rules

- Make assumptions when they are low-risk; record them in `project.json` and in
  each agent handoff.
- Ask the user one concise question only when a missing choice would change the
  premise, target genre, or output format.
- Prefer filmable action over inner monologue. Every major beat should be visible,
  audible, or representable as a shot.
- Keep short-drama scripts built around a first-five-seconds hook, frequent
  conflict escalation, and a final turn.
- Keep `bible/visual-style.md` at story-side visual tone and prohibitions only.
  It is not an asset style bible and must not contain image-generation prompts
  or ComfyUI settings.
- When downstream departments report `needs_script_fix`, repair only
  Writer Room owned files and require downstream refresh of dependent
  director, asset, prompt, render, edit, audio, and post files.
- Do not generate video prompts, image assets, audio production files, edit
  decisions, post-production deliverables, or ComfyUI parameters.
- Only final confirmed cut facts may be written back as story canon.
- Do not turn failed generation results into canon. Only final confirmed cut
  facts may enter `bible/continuity.md`.
- Do not auto-edit this skill from `evolution-notes.md`. Evolution notes are
  proposals; require explicit user approval before changing prompts, rubrics, or
  templates.

## Final Response

After the run, report:

- final script file path
- score and pass/revise decision
- artifacts created
- unresolved warnings
- next step toward shot planning or ComfyUI prompt generation when relevant
