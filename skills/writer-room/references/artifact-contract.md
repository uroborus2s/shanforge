# Writer Room Artifact Contract

Every child Codex agent returns a single structured envelope. The parent Codex
coordinator writes the files to disk after reviewing the envelope.

## Envelope

```json
{
  "status": "success",
  "summary": "One sentence result.",
  "artifacts": [
    {
      "path": "{episode-id}/script/script-v01.md",
      "kind": "markdown",
      "content": "# Script v01\n..."
    }
  ],
  "next_actions": ["script-doctor-agent"],
  "warnings": [],
  "handoff": {
    "main_output": "{episode-id}/script/script-v01.md",
    "assumptions": [],
    "quality_notes": [],
    "blocked_questions": []
  }
}
```

## Status Values

- `success`: output is ready for the next agent.
- `warning`: output is usable but contains risks the parent should preserve.
- `blocked`: the agent cannot continue without parent/user input.

## Artifact Rules

- Use project-relative paths only.
- Use Markdown for human-readable creative artifacts.
- Use JSON only for machine-readable summaries, scorecards, and failure patterns.
- Do not include absolute paths in child-agent output; the parent resolves them.
- Keep artifact content complete enough to write directly to disk.

## Required Handoff Fields

- `main_output`: one project-relative path.
- `assumptions`: concrete assumptions made by the role.
- `quality_notes`: role-specific risks or strengths.
- `blocked_questions`: questions only when `status` is `blocked`.
