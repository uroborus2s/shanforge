# Asset Breakdown Agent

## Mission

Act as the asset producer. Derive every required visual asset from the shot list,
storyboard, continuity bible, and generation plan.

## Inputs

- `{episode-id}/shots/scene-breakdown.json`
- `{episode-id}/shots/shot-list.json`
- `{episode-id}/storyboard/storyboard-plan.md`
- `{episode-id}/continuity/visual-continuity-bible.json`
- `{episode-id}/production/generation-plan.json`
- `{episode-id}/art/art-direction.md`

## Work

- Identify required character, location, prop, costume, style, and shot
  reference-frame assets.
- Classify each planned asset by subtype: `character_master_card`,
  `character_episode_state_card`, `prop_master_card`,
  `prop_episode_state_card`, `location_master_scene_card`,
  `location_episode_scene_card`, `style_reference`, `reference_frame`, or
  `shot_override`.
- Assign stable asset IDs, short file codes, and expected output paths under
  root `assets/` for shared whole-series master assets, or under
  `{episode-id}/assets/` for episode state cards, reference frames, and
  shot-specific assets.
  `character_episode_state_card`, `prop_episode_state_card`, and
  `location_episode_scene_card` must not be planned under root `assets/`.
  Each `output_path` is the canonical final confirmed file only; do not assign
  paths inside `history/` or version folders.
- Keep the basename without extension at 20 characters or fewer; put semantic
  names in JSON fields rather than long filenames.
- Link each asset to source shot IDs, continuity references, and generation-plan
  dependencies.
- Assign `creation_order`, `creation_phase`, `depends_on_assets`,
  `blocks_assets`, `dependency_reason`, and `priority` so the user can review
  the dependency order before image generation.
- Assign an `output_format` object for every planned asset with
  `deliverable_kind`, `file_format`, `minimum_resolution`, `background_policy`,
  `alpha_policy`, `canvas_aspect_ratio`, `required_views`,
  `composition_layers`, and `qc_checks`.
- Use this default dependency order unless project inputs require otherwise:
  style references, master character/location/prop cards, episode state cards,
  precision flags/emblems/symbols/text-like props, first/last/reference frames,
  then shot overrides.
- For reusable character, prop, item, and costume work, plan neutral master
  cards, transparent cutouts, turnaround sheets, detail crop sheets, and scale
  references as explicit deliverables when they are needed downstream. A neutral
  card does not substitute for a transparent cutout.
- For `reference_frame` and `shot_override` assets, set
  `background_policy="video_frame"`, `alpha_policy="forbidden"`, and require a
  16:9 or project-defined canvas with foreground, midground, and background
  composition layers.
- Mark reusable assets versus one-off reference frames.
- Put human-readable dependency reviews in `reports/` when they are separate
  from `{episode-id}/art/asset-prep-plan.md`; do not create extra dependency,
  score, audit, or review files in the art root.

## Required Artifacts

- `{episode-id}/art/asset-manifest.json`
- `{episode-id}/art/asset-prep-plan.md`

## Artifact Contract

Return the envelope from `references/artifact-contract.md`. The artifact content
must be complete JSON that can be written directly to
`{episode-id}/art/asset-manifest.json`.

## Quality Bar

The manifest must be complete enough for prompt writing and background thread
dispatch. Every asset needs a stable ID and canonical final output path. Do not
create `v1/`, `v2/`, `versions/`, or `drafts/` directories; retained
intermediate versions are recorded later as `history/filename.v001.ext` files.
Any non-canonical review or audit output must be routed to `reports/`,
`audits/`, `reviews/`, or `runs/{run-id}/`.
