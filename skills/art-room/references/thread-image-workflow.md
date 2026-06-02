# Codex Thread Image Workflow

The parent Codex instance owns background thread orchestration. Planning child
agents should not call thread tools.

## Required Tools

Use the Codex app thread tools when available:

- `codex_app.create_thread`
- `codex_app.read_thread`
- `codex_app.send_message_to_thread`

If these tools are unavailable, write `{episode-id}/art/thread-results.json`
with `status="blocked"` and preserve the full
`{episode-id}/art/thread-plan.json` for a later run.

## Dispatch Rules

1. Read `{episode-id}/art/thread-plan.json` and group jobs by disjoint output
   directory.
2. Create one background thread per batch when practical:
   `characters`, `locations`, `props-costumes`, `style`, and
   `reference-frames`.
3. Use a project target with local environment when the production project lives
   inside the current workspace. Do not use a separate worktree for image files
   unless the user explicitly asks.
4. Omit model overrides unless the user explicitly requests one.
5. Include in each thread prompt:
   - project root and episode ID;
   - batch ID;
   - exact canonical final output paths;
   - prompt records from `{episode-id}/prompts/art-image-prompts.json`;
   - continuity references;
   - requirement to use available image generation capability;
   - requirement that final confirmed images are written only to the canonical
     output paths;
   - requirement that retained intermediate, rejected, or superseded images are
     moved to a sibling `history/` directory and named with filename suffixes
     such as `.v001`, `.v002`, never placed in version folders;
   - requirement to return a compact JSON manifest of final files and history
     files created.

## Polling And Retry

- Poll each thread with `codex_app.read_thread`.
- If a thread reports missing inputs or ambiguous output paths, send one
  corrective prompt with `codex_app.send_message_to_thread`.
- Do not retry more than once per batch without user approval.
- Preserve every blocked item in `{episode-id}/art/thread-results.json`.

## Result Recording

Write `{episode-id}/art/thread-results.json` with:

```json
{
  "version": "1",
  "status": "completed",
  "threads": [
    {
      "batch_id": "characters",
      "thread_id": "thread-id",
      "status": "completed",
      "created_files": ["assets/characters/hero__turnaround.png"],
      "history_files": ["assets/characters/history/hero__turnaround.v001.png"],
      "warnings": []
    }
  ],
  "blocked_jobs": []
}
```

Generated images should stay inside these project-relative directories:

```text
assets/characters/
assets/locations/
assets/props/
assets/costumes/
assets/style/
{episode-id}/assets/reference-frames/
{episode-id}/assets/shot-overrides/
{episode-id}/assets/temp/
```

Only final confirmed images should remain at their canonical output paths.
Retained intermediate versions belong in a `history/` directory inside the
relevant asset directory, with the version number appended to the filename
before the extension. Do not create `v1/`, `v2/`, `versions/`, or `drafts/`
directories for generated art assets.
