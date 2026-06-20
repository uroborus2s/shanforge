# Art Room Artifact Contract

Every planning child agent returns a single structured envelope. The parent
Codex coordinator writes files to disk after checking the envelope.

## Envelope

```json
{
  "status": "success",
  "summary": "One sentence result.",
  "artifacts": [
    {
      "path": "{episode-id}/art/asset-manifest.json",
      "kind": "json",
      "content": "{ \"assets\": [] }"
    }
  ],
  "next_actions": ["character-design-agent"],
  "warnings": [],
  "handoff": {
    "main_output": "{episode-id}/art/asset-manifest.json",
    "assumptions": [],
    "quality_notes": [],
    "blocked_questions": []
  }
}
```

## Status Values

- `success`: output is ready for the next agent.
- `warning`: output is usable but contains risks the parent should preserve.
- `blocked`: the agent cannot continue without parent or user input.

## Artifact Rules

- Use project-relative paths only.
- Use Markdown for art direction, QC reports, and human review notes.
- Use JSON for asset manifests, design specs, prompt plans, thread plans, thread
  results, and asset indexes.
- Do not include absolute paths in child-agent output; the parent resolves them.
- Do not generate image files from planning child agents. Image creation is a
  parent-coordinated Codex background thread step.
- Do not place ad hoc `*-audit*`, `*-review*`, `*-score*`, `*-rewrite*`,
  `*-after-fix*`, retry, scratch, or run-specific intermediate files in the
  root of `art/` or `{episode-id}/art/`.
- Route non-canonical artifacts to fixed subdirectories:
  `reports/` for QC and approval summaries, `audits/` for consistency,
  readability, rewrite, and after-fix audits, `reviews/` for per-asset prompt
  review notes, and `runs/{run-id}/` for worker scratch, retries, and
  superseded thread plans/results.

## Required Handoff Fields

- `main_output`: one project-relative path.
- `assumptions`: concrete assumptions made by the role.
- `quality_notes`: role-specific risks, tradeoffs, or strengths.
- `blocked_questions`: questions only when `status` is `blocked`.
