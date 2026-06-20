---
name: art-room
description: Codex-native art room and visual asset department for creating whole-series master assets, episode prep assets, character cards, prop/item cards, location scene cards, style boards, and shot reference image assets from a fixed ./project/{project-name}/{episode-id} production directory. Use when Codex needs an 美术资产部, Art Room, visual asset pipeline, character sheets, scene concept art, prop boards, scene cards, item cards, style bible, image prompt briefs, short filename asset indexes, or Codex background threads to generate project image assets from director-room outputs.
---

# Art Room

Use this skill after shot planning has produced stable director-room outputs
under `./project/{project-name}/{episode-id}/`. The parent Codex instance acts as
the art producer: it verifies the project root and episode root, coordinates
asset planning agents, writes machine-readable manifests, then uses Codex
background threads to generate the actual image assets into fixed project
directories.

## Department Boundary

Art Room owns visual asset consistency, not shot planning, not story canon, and
not final ComfyUI prompt engineering. It translates story bibles, shot lists,
storyboard panels, continuity locks, and generation strategy into reusable
character cards, prop/item cards, location scene cards, style assets, and
reference-frame assets. Director Room's prompt-engineering pass can later
refresh ComfyUI-ready prompts using these assets.

Default pipeline:

```text
creative brief
  -> final script package
  -> director-room
  -> art-room
  -> director-room prompt refresh
  -> comfyui-production
  -> post-production
```

## Project Input

Read from a single production project root:

```text
./project/{project-name}/
```

Before running department agents for `{episode-id}`, verify these canonical
files exist:

```text
bible/characters.md
bible/scenes.md
{episode-id}/script/final-script.md
{episode-id}/director/director-brief.md
{episode-id}/director/camera-plan.md
{episode-id}/shots/scene-breakdown.json
{episode-id}/shots/shot-list.json
{episode-id}/storyboard/storyboard-plan.md
{episode-id}/continuity/visual-continuity-bible.json
{episode-id}/production/generation-plan.json
{episode-id}/prompts/shot-prompts-draft.json
```

Optional project-level inputs for whole-series asset planning:

```text
bible/continuity.md
bible/visual-style.md
production/series-video-rules.md
assets/asset-index.json
```

Do not create a detached art-room project. If the user provides a project root,
all art outputs and generated images must be written under that same root. If a
required director-room artifact is missing and cannot be inferred safely from
the project directory, ask one concise question before generating assets.

## Outputs

Required planning outputs:

```text
art/series-asset-plan.md
art/series-thread-plan.json
art/series-thread-results.json
assets/asset-index.json
{episode-id}/art/asset-prep-plan.md
{episode-id}/art/art-direction.md
{episode-id}/art/asset-manifest.json
{episode-id}/art/character-designs.json
{episode-id}/art/location-designs.json
{episode-id}/art/prop-costume-designs.json
{episode-id}/art/style-continuity-bible.json
{episode-id}/prompts/art-image-prompts.json
{episode-id}/art/thread-plan.json
{episode-id}/art/thread-results.json
{episode-id}/art/asset-index.json
{episode-id}/art/asset-qc-report.md
```

Required review, audit, and run output directories:

```text
art/reports/
art/audits/
art/reviews/
art/runs/
{episode-id}/art/reports/
{episode-id}/art/audits/
{episode-id}/art/reviews/
{episode-id}/art/runs/
```

Required image output directories:

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

Root `assets/` directories are for whole-series reusable assets only. Episode
state cards are episode assets: write `character_episode_state_card`,
`prop_episode_state_card`, and `location_episode_scene_card` images under the
matching `{episode-id}/assets/<type>/` directory. For example, `c001m.png`
belongs in `assets/characters/`, while `c001e01.png` belongs in
`01/assets/characters/`.

## Output Directory Discipline

Keep `art/` and `{episode-id}/art/` readable. The root of `art/` is reserved
for current effective whole-series control files only:

```text
art/series-asset-plan.md
art/series-thread-plan.json
art/series-thread-results.json
```

The root of `{episode-id}/art/` is reserved for the fixed episode handoff files
listed in Required planning outputs. Do not write ad hoc `*-audit*`,
`*-review*`, `*-score*`, `*-rewrite*`, `*-after-fix*`, retry notes, worker
scratch, or run-specific intermediate files directly into either art root.

Route non-canonical files by purpose:

```text
art/reports/ or {episode-id}/art/reports/
  human QC reports, approval summaries, dependency review documents
art/audits/ or {episode-id}/art/audits/
  consistency audits, readability audits, rewrite scores, after-fix audits
art/reviews/ or {episode-id}/art/reviews/
  per-asset prompt reviews and targeted human review notes
art/runs/{run-id}/ or {episode-id}/art/runs/{run-id}/
  run logs, retry records, worker scratch JSON, superseded thread plans/results
```

If a later run replaces a current effective root file such as
`series-thread-plan.json`, move the superseded copy into the relevant
`art/runs/{run-id}/` directory before writing the new current file. Do not leave
multiple dated, scored, reviewed, or after-fix variants beside the canonical
root files.

## Asset Cards And Prompt Layers

Every reusable production asset is a three-part card:

```text
design specification JSON
  -> image prompt record
  -> canonical image file
```

Supported asset subtypes include:

```text
character_master_card
character_episode_state_card
prop_master_card
prop_episode_state_card
location_master_scene_card
location_episode_scene_card
style_reference
reference_frame
shot_override
```

Generated filenames must be short stable codes. The basename without extension
must be 20 characters or fewer, for example `c001m.png`, `c001e01.png`,
`p001m.png`, `p001e01.png`, `l001m.png`, `l001e01.png`, `f001m.png`, and
`r001s02.png`. The semantic name, owner, source refs, usage, and QC status live
in JSON indexes, not in long filenames.

Image prompts must separate `production_metadata` from
`model_visible_prompt`. Metadata contains process fields such as `asset_id`,
`asset_subtype`, `output_file`, `prompt_id`, `source_refs`,
`continuity_refs`, and `usage`. The model-visible prompt uses six sections:
visible goal, style and image quality, subject content, composition and motion,
visible continuity constraints, and negative prompt. Do not put `asset_id`,
`episode_id`, `output_file`, source refs, or usage notes into the visible prompt
body.

Every prompt record must also include `copy_ready` fields that a human can copy
directly into image models such as ChatGPT or Gemini. `copy_ready` contains a
merged positive prompt, a standalone negative prompt, and natural-language
ChatGPT/Gemini prompt variants. These fields are derived from
`model_visible_prompt`; they do not replace the structured fields used for
audit.

Asset planning must expose creation order and dependencies before image
generation starts. `asset-prep-plan.md`, `asset-manifest.json`, and
`thread-plan.json` must identify `creation_order`, `creation_phase`,
`depends_on_assets`, `blocks_assets`, `dependency_reason`, and `priority` when
applicable, so the user can review what must be made first.

Character cards must include a literal `body_metrics` object with visible body
metrics such as height, build, body ratio, silhouette, and scale references.
Prop/item cards must include a literal `physical_dimensions` object with
physical dimensions such as length, width, height, scale reference, weight feel,
and material thickness when those details affect generation.

For precise flags, emblems, symbols, records, seals, and text-like props, create
a master prop card first and plan reference/line control or transparent PNG/SVG
post-composite when exact shape is required.

## Image Output Format Contract

Every planned image asset must carry a literal `output_format` object in
`asset-prep-plan.md`, `asset-manifest.json`, `art-image-prompts.json`, and the
thread prompt. `asset-qc-report.md` must verify the same contract before marking
an image ready. Required `output_format` fields are `deliverable_kind`,
`file_format`, `minimum_resolution`, `background_policy`, `alpha_policy`,
`canvas_aspect_ratio`, `required_views`, `composition_layers`, and `qc_checks`.

Reusable character, prop, item, and costume card work must not be treated as a
final video frame. Plan the required deliverables explicitly:

```text
neutral master card
transparent cutout
turnaround sheet
detail crop sheet
scale reference
```

Character and prop/item master cards use a neutral plain background for readable
shape, material, and scale. Transparent cutouts must be separate planned PNG or
SVG outputs with `alpha_policy="required"`; do not rely on a neutral card as a
cutout substitute. Turnaround sheets must include front, side, back, and
three-quarter views when the asset will be reused across shots. Detail crop
sheets must isolate face, hands, costume texture, markings, mechanisms, damage,
or material details that affect continuity.

Video-generation reference frames are different from asset cards. First frames,
last frames, reference frames, and shot overrides must be 16:9 or the
project-defined delivery ratio, must use `background_policy="video_frame"` and
`alpha_policy="forbidden"`, and must describe foreground, midground, and
background in `composition_layers`. These frames need scene composition, camera
distance, camera angle, screen direction, lighting, weather/time, and action
state; they must not use transparent or isolated card backgrounds unless the
shot is explicitly a compositing element.

QC must reject video reference frames that do not clearly separate foreground,
midground, and background.

## Scene Image Information Budget Bible

Scene-context location cards, establishing plates, video reference frames, and
shot overrides must control visual information before image generation starts.
Wide shots and distant scenes fail when every soldier, banner, creature, wall
block, weapon, and background object is treated as equally important. The result
is particleized stone, granular crowd texture, noisy micro-detail, soft mush, or
AI speckle.

For distant establishing shots, epic wide shots, battlefields, cities, crowd
scenes, fortress scenes, mountain passes, large interiors, and any scene with
many repeated objects, Art Room must prioritize only three functions:

```text
large readable shapes
lighting and atmosphere
clear silhouettes and scale
```

These shots must not try to make every small object readable. They are not
character sheets, unit showcases, architecture inventories, weapon catalogs, or
emblem proof sheets.

Before prompt generation, define a `scene_information_budget` for every
wide/group-heavy scene asset:

```text
detail_priority:
  highest_detail: only 3-5 elements, such as the central gate, main road,
    nearest banners, hero silhouette, or largest creatures
  medium_detail: important midground masses, readable light sources, major flags
  low_detail: distant soldiers, wall guards, background towers, far terrain
  impression_only: distant crowds, arrows, tiny weapons, parapet figures,
    secondary banners, far vehicles or animals
distance_simplification:
  use grouped silhouettes, massing, haze, smoke, snow, rain, dust, fog, and
  atmospheric perspective to simplify distant forms
forbidden_detail_behavior:
  no equal-detail rendering across the whole frame
  no over-detailed distant figures
  no full-frame ultra-detail
  no visual information overload
```

The prompt rule is:

```text
big shapes clear, details restrained, distant subjects grouped,
only a few nearby or central elements finely rendered
```

For wide scene prompts, include negative constraints against particleization and
information overload:

```text
no equal-detail rendering across the whole frame,
no over-detailed distant soldiers or crowd members,
no granular crowd texture,
no particleized stone,
no noisy micro-detail,
no AI speckle,
no smoke pretending to be architectural detail,
no distant objects rendered as sharp individual miniatures,
no full-frame ultra-detail,
no cluttered battlefield or city texture,
no visual information overload.
```

QC must reject any wide scene frame where distant repeated forms become noisy
particles, architecture becomes fake micro-texture, smoke is used as substitute
structure, or the whole frame receives the same level of detail.

## Asset Versioning And History

Generated art assets do not use version folders. Do not create directories such
as `v1/`, `v2/`, `versions/`, or `drafts/` for image iterations.

Each planned asset has one canonical `output_path`. That path is reserved for
the final confirmed version only:

```text
assets/characters/c001m.png
01/assets/characters/c001e01.png
{episode-id}/assets/reference-frames/sc01_sh010__first_frame.png
```

Intermediate, rejected, or superseded images that should be retained must be
moved into a sibling `history/` directory and renamed with a version suffix
before the file extension:

```text
assets/characters/history/c001m.v001.png
01/assets/characters/history/c001e01.v001.png
{episode-id}/assets/reference-frames/history/sc01_sh010__first_frame.v001.png
```

Planning artifacts must keep `output_path` pointed at the canonical final file,
not at a history file. Thread results and QC artifacts may record retained
intermediates in `history_files` for audit. Before handoff, no generated draft
or alternate image should remain outside the relevant `history/` directory.

## Operating Model

- Treat Codex as the runtime. Do not implement a Python agent loop and do not
  call a project LLM provider for department agents.
- Use `multi_agent_v1.spawn_agent` for bounded planning roles when available.
  Child planning agents return artifact envelopes; they do not call Codex thread
  tools and do not generate images directly.
- Use Codex background thread tools only after
  `{episode-id}/prompts/art-image-prompts.json` and
  `{episode-id}/art/thread-plan.json` exist. The parent coordinator calls
  `codex_app.create_thread`, checks progress with `codex_app.read_thread`, and
  steers retries with `codex_app.send_message_to_thread`.
- Create background threads only for disjoint image batches with explicit output
  paths. Typical batches are characters, locations, props/costumes, style board,
  and shot reference frames.
- In each thread prompt, instruct the worker Codex to use the available image
  generation capability for raster assets, write final confirmed images to the
  assigned project paths, archive retained intermediates in `history/` with
  `.v001`, `.v002`, etc. filename suffixes, and return a compact manifest of
  final files and history files created.
- If Codex thread tools or image generation are unavailable, still produce
  `{episode-id}/art/thread-plan.json` and
  `{episode-id}/prompts/art-image-prompts.json`, then mark image generation as
  `blocked` in `{episode-id}/art/thread-results.json`.

## References

Load only what is needed:

- `references/artifact-contract.md`: child-agent envelope and artifact rules.
- `references/thread-image-workflow.md`: Codex background thread dispatch,
  polling, retry, and result recording rules.
- `references/asset-card-prompt-templates.md`: character, prop/item, location
  scene card fields; short filename rules; production metadata; model-visible
  six-section prompt templates; precision prop strategy.
- `agents/*.md`: one task card per planning role. Do not treat
  `agents/openai.yaml` as a role card.
- `schemas/*.json`: structural contracts for JSON outputs and tests.

## Workflow

1. Verify the project root and required director-room outputs.
2. For whole-series asset planning, produce `art/series-asset-plan.md` and
   initialize or refresh `assets/asset-index.json` for shared master cards.
3. Run `art-director-agent` to produce
   `{episode-id}/art/art-direction.md`.
4. Run `asset-breakdown-agent` to produce
   `{episode-id}/art/asset-prep-plan.md` and
   `{episode-id}/art/asset-manifest.json`.
5. Run `character-design-agent`, `environment-design-agent`, and
   `prop-costume-design-agent` after the asset manifest exists. These may run
   in parallel.
6. Run `style-continuity-agent` after the design JSON files exist.
7. Run `image-prompt-agent` to produce
   `{episode-id}/prompts/art-image-prompts.json`.
8. Run `thread-plan-agent` to produce `{episode-id}/art/thread-plan.json`.
9. Parent coordinator creates Codex background threads according to
   `{episode-id}/art/thread-plan.json`, one disjoint asset batch per thread
   when practical.
10. Parent coordinator records thread IDs, statuses, generated file paths,
   retained history file paths, blocked items, and retry notes in
   `{episode-id}/art/thread-results.json`.
11. Run `asset-qc-agent` to produce `{episode-id}/art/asset-index.json` and
    `{episode-id}/art/asset-qc-report.md`.
12. Return the project root, generated asset directories, blocked image jobs,
    validation performed, and the recommended handoff back to `director-room`
    prompt refresh.

## Agent Sequence

Use these task cards:

```text
agents/art-director-agent.md
agents/asset-breakdown-agent.md
agents/character-design-agent.md
agents/environment-design-agent.md
agents/prop-costume-design-agent.md
agents/style-continuity-agent.md
agents/image-prompt-agent.md
agents/thread-plan-agent.md
agents/asset-qc-agent.md
```

## Quality Rules

- Preserve visual continuity over isolated asset beauty. Character identity,
  wardrobe, props, geography, lighting logic, and material language must match
  `{episode-id}/continuity/visual-continuity-bible.json`.
- When project inputs define internal hierarchy, caste, rank, or role-based
  visual differences within a faction, species, or organization, preserve those
  differences instead of flattening all members into one look. Do not encode
  project-specific anatomy, culture, or lore in this reusable skill. Derive tier
  labels, authority cues, body language, costume, anatomy, materials, and visual
  trait balance from the project bible and continuity inputs. Character designs,
  style rules, and image prompts must explicitly label the relevant tier or role
  and the intended project-defined visual balance.
- Do not rewrite the story, shot list, or generation strategy.
- Do not write final ComfyUI workflow parameters. Art Room image prompts are
  tool-neutral asset prompts; Director Room owns ComfyUI prompt/workflow files.
- Every generated image must have an asset ID, asset subtype, short file code,
  source prompt ID, expected output path, continuity references, and downstream
  usage notes.
- Only the final confirmed version of an asset may live at its canonical
  `output_path`; all retained intermediate versions must live in `history/` and
  use filename suffixes such as `.v001`, never version directories.
- Prefer reusable reference assets over one-off images unless the shot explicitly
  requires a unique first frame, last frame, redraw target, or reference frame.
- Keep prompts specific but tool-neutral. Do not include ComfyUI node graphs,
  sampler settings, or final production parameters.
- Do not launch image-generation threads until output paths are stable and the
  prompt plan can be audited.

## Final Response

After the run, report:

- project root
- planning artifacts created
- image assets created or blocked
- Codex thread IDs and statuses
- validation performed
- next department handoff recommendation
