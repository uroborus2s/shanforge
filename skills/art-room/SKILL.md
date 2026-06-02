---
name: art-room
description: Codex-native art room and visual asset department for creating consistent character, location, prop, costume, style, and shot reference image assets from a fixed ./project/{project-name}/{episode-id} production directory. Use when Codex needs an 美术资产部, Art Room, visual asset pipeline, character sheets, scene concept art, prop boards, style bible, image prompt briefs, or Codex background threads to generate project image assets from director-room outputs.
---

# Art Room

Use this skill after shot planning has produced stable director-room outputs
under `./project/{project-name}/{episode-id}/`. The parent Codex instance acts as
the art producer: it verifies the project root and episode root, coordinates
asset planning agents, writes machine-readable manifests, then uses Codex
background threads to generate the actual image assets into fixed project
directories.

## Department Boundary

Art Room owns visual asset consistency, not shot planning and not final ComfyUI
prompt engineering. It translates shot lists, storyboard panels, continuity
locks, and generation strategy into reusable character, environment, prop,
costume, style, and reference-frame assets. Prompt Room later converts these
asset prompts into tool-specific ComfyUI-ready prompts.

Default pipeline:

```text
creative brief
  -> final script package
  -> director-room
  -> art-room
  -> prompt-room
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

Do not create a detached art-room project. If the user provides a project root,
all art outputs and generated images must be written under that same root. If a
required director-room artifact is missing and cannot be inferred safely from
the project directory, ask one concise question before generating assets.

## Outputs

Required planning outputs:

```text
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

Required image output directories:

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

## Asset Versioning And History

Generated art assets do not use version folders. Do not create directories such
as `v1/`, `v2/`, `versions/`, or `drafts/` for image iterations.

Each planned asset has one canonical `output_path`. That path is reserved for
the final confirmed version only:

```text
assets/characters/hero__turnaround.png
{episode-id}/assets/reference-frames/sc01_sh010__first_frame.png
```

Intermediate, rejected, or superseded images that should be retained must be
moved into a sibling `history/` directory and renamed with a version suffix
before the file extension:

```text
assets/characters/history/hero__turnaround.v001.png
assets/characters/history/hero__turnaround.v002.png
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
- `agents/*.md`: one task card per planning role. Do not treat
  `agents/openai.yaml` as a role card.
- `schemas/*.json`: structural contracts for JSON outputs and tests.

## Workflow

1. Verify the project root and required director-room outputs.
2. Run `art-director-agent` to produce
   `{episode-id}/art/art-direction.md`.
3. Run `asset-breakdown-agent` to produce
   `{episode-id}/art/asset-manifest.json`.
4. Run `character-design-agent`, `environment-design-agent`, and
   `prop-costume-design-agent` after the asset manifest exists. These may run
   in parallel.
5. Run `style-continuity-agent` after the design JSON files exist.
6. Run `image-prompt-agent` to produce
   `{episode-id}/prompts/art-image-prompts.json`.
7. Run `thread-plan-agent` to produce `{episode-id}/art/thread-plan.json`.
8. Parent coordinator creates Codex background threads according to
   `{episode-id}/art/thread-plan.json`, one disjoint asset batch per thread
   when practical.
9. Parent coordinator records thread IDs, statuses, generated file paths,
   retained history file paths, blocked items, and retry notes in
   `{episode-id}/art/thread-results.json`.
10. Run `asset-qc-agent` to produce `{episode-id}/art/asset-index.json` and
    `{episode-id}/art/asset-qc-report.md`.
11. Return the project root, generated asset directories, blocked image jobs,
    validation performed, and the recommended handoff to `prompt-room`.

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
- Every generated image must have an asset ID, source prompt ID, expected output
  path, continuity references, and downstream usage notes.
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
