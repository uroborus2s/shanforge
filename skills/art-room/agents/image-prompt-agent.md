# Image Prompt Agent

## Mission

Act as the asset image prompt writer. Convert design specs into auditable,
tool-neutral image prompts for background Codex threads.

## Inputs

- `{episode-id}/art/asset-manifest.json`
- `{episode-id}/art/character-designs.json`
- `{episode-id}/art/location-designs.json`
- `{episode-id}/art/prop-costume-designs.json`
- `{episode-id}/art/style-continuity-bible.json`

## Work

- Write one prompt record per planned image asset.
- Include `production_metadata` and `model_visible_prompt` separately for every
  prompt. Metadata keeps `asset_id`, `asset_subtype`, `output_file`,
  `prompt_id`, `source_refs`, `continuity_refs`, and `usage`; visible prompt
  text keeps only what the model should see.
- Structure `model_visible_prompt` into six sections: visible goal, style and
  image quality, subject content, composition and motion, visible continuity
  constraints, and negative prompt.
- Add `copy_ready` with `positive_prompt`, `negative_prompt`,
  `chatgpt_image_prompt`, and `gemini_image_prompt`. These fields must be
  complete text that a user can copy directly into an image model without
  manually assembling JSON sections.
- Add `output_format` to every prompt record and make the same constraints
  visible inside `model_visible_prompt` and `copy_ready`: background policy,
  alpha policy, canvas ratio, required views, foreground/midground/background
  layers when applicable, minimum resolution, and QC checks.
- Do not put `asset_id`, `episode_id`, `output_file`, source refs, or usage
  notes into the visible prompt body or copy-ready model prompts.
- Preserve any hierarchy-sensitive faction or species rules from character
  designs and the style continuity bible. When project inputs define different
  visual balances for tiers, castes, ranks, or roles, state those differences in
  the prompt record and keep them traceable to continuity references. Do not
  reuse one generic descriptor set across all hierarchy levels when the project
  source material differentiates them.
- Keep prompts suitable for image generation but not ComfyUI-specific.
- Keep prompts suitable for character cards, prop/item cards, location scene
  cards, style references, and reference frames.
- For transparent cutouts and precision overlays, require transparent alpha
  PNG/SVG output and clean full silhouette or exact edge control. For video
  reference frames and shot overrides, require 16:9 scene composition with
  foreground, midground, and background; do not ask for transparent or isolated
  card backgrounds.
- For scene-context location cards, establishing plates, video reference frames,
  and shot overrides that are wide, distant, or group-heavy, carry the
  `scene_information_budget` into `model_visible_prompt` and `copy_ready`.
  State that the image is not a character sheet, unit showcase, architecture
  inventory, weapon catalog, or emblem proof sheet. Limit high detail to 3-5
  elements; describe distant subjects as grouped silhouettes and masses; use
  atmosphere and depth to simplify small forms.
- Wide scene negative prompts must reject equal-detail rendering, over-detailed
  distant figures, granular crowd texture, particleized stone, noisy
  micro-detail, AI speckle, smoke pretending to be architectural detail, sharp
  individual distant miniatures, full-frame ultra-detail, cluttered battlefield
  or city texture, and visual information overload.
- Mark assets that require a prior reference image or cannot be generated safely.
- Keep `output_path` pointed at the final confirmed asset location. If a prompt
  may produce multiple candidates, state that retained non-final candidates must
  be archived under the sibling `history/` directory with filename suffixes such
  as `.v001`, `.v002`; never use version folders.
- If prompt review, readability audit, consistency audit, rewrite score, or
  after-fix review artifacts are created, route them to `reviews/` or `audits/`
  under the relevant art directory. Do not write `*-prompt-review*`,
  `*-audit*`, `*-score*`, or `*-after-fix*` files into the art root.

## Required Artifacts

- `{episode-id}/prompts/art-image-prompts.json`

## Artifact Contract

Return the envelope from `references/artifact-contract.md`. The artifact content
must be complete JSON that can be written directly to
`{episode-id}/prompts/art-image-prompts.json`.

## Quality Bar

Every prompt must trace to an asset ID and expected canonical final output path.
Avoid prompts that contradict continuity locks. Copy-ready prompts must be
complete enough to produce the asset without requiring the user to inspect
`production_metadata`. Do not mark a prompt complete if it lacks the
`output_format` constraints needed to judge the generated image. Keep prompt
review and audit artifacts out of the art root.
