# Codex Thread Image Workflow

The parent Codex instance owns background thread orchestration. Planning child
agents should not call thread tools.

## Required Tools

Use the Codex app thread tools when available:

- `codex_app.create_thread`
- `codex_app.read_thread`
- `codex_app.send_message_to_thread`

If these tools are unavailable, write the current effective
`{episode-id}/art/thread-results.json` with `status="blocked"` and preserve the
full `{episode-id}/art/thread-plan.json` for a later run. Any superseded,
retry-specific, or diagnostic copies belong under
`{episode-id}/art/runs/{run-id}/`.

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
   - their `production_metadata` and six-section `model_visible_prompt`;
   - their `copy_ready` prompt text for direct image-model submission;
   - their `output_format` contract, including background policy, alpha policy,
     canvas ratio, required views, composition layers, minimum resolution, and
     QC checks;
   - any `scene_information_budget` for wide, distant, group-heavy, battlefield,
     city, fortress, mountain pass, or other large repeated-object scene assets;
   - continuity references;
   - creation order and dependencies from asset prep/manifest/thread plan;
   - short filename rule: basename without extension is 20 characters or fewer;
   - requirement to use available image generation capability;
   - requirement that final confirmed images are written only to the canonical
     output paths;
   - requirement that transparent cutouts and precision overlays preserve alpha
     intent, while video reference frames and shot overrides are scene frames
     with foreground, midground, and background layers;
   - requirement that wide and distant scene images follow their information
     budget: only 3-5 elements receive high detail, distant subjects remain
     grouped silhouettes or masses, atmosphere simplifies small forms, and the
     worker avoids particleized stone, granular crowd texture, noisy micro-detail,
     AI speckle, full-frame ultra-detail, and visual information overload;
   - requirement that retained intermediate, rejected, or superseded images are
     moved to a sibling `history/` directory and named with filename suffixes
     such as `.v001`, `.v002`, never placed in version folders;
   - requirement to return a compact JSON manifest of final files and history
     files created.

## Polling And Retry

- Poll each thread with `codex_app.read_thread`.
- If a thread reports missing inputs or ambiguous output paths, send one
  corrective prompt with `codex_app.send_message_to_thread`.
- If a thread depends on unfinished batches or assets, do not start it; mark it
  blocked or wait until dependency outputs are confirmed.
- Do not retry more than once per batch without user approval.
- Preserve every blocked item in `{episode-id}/art/thread-results.json`.
- Preserve retry diagnostics, worker scratch, and superseded thread plans or
  results in `art/runs/{run-id}/` or `{episode-id}/art/runs/{run-id}/`, not in
  the art root.

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
      "created_files": ["assets/characters/c001m.png", "01/assets/characters/c001e01.png"],
      "history_files": ["assets/characters/history/c001m.v001.png", "01/assets/characters/history/c001e01.v001.png"],
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
{episode-id}/assets/characters/
{episode-id}/assets/locations/
{episode-id}/assets/props/
{episode-id}/assets/costumes/
{episode-id}/assets/reference-frames/
{episode-id}/assets/shot-overrides/
{episode-id}/assets/temp/
```

Whole-series master cards stay in root `assets/`. Episode state cards, including
`character_episode_state_card`, `prop_episode_state_card`, and
`location_episode_scene_card`, stay under the matching episode asset directory.

Only final confirmed images should remain at their canonical output paths.
Retained intermediate versions belong in a `history/` directory inside the
relevant asset directory, with the version number appended to the filename
before the extension. Do not create `v1/`, `v2/`, `versions/`, or `drafts/`
directories for generated art assets.

Only current effective thread plan/result files belong in the art root. Do not
write `*-audit*`, `*-review*`, `*-score*`, `*-after-fix*`, or run-specific
diagnostic files beside `thread-plan.json` or `thread-results.json`; route them
to `audits/`, `reviews/`, `reports/`, or `runs/{run-id}/` according to purpose.
