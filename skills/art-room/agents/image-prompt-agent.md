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
- Include subject, composition, style tokens, continuity references, output path,
  negative prompt notes, and downstream usage.
- Preserve any hierarchy-sensitive species rules from character designs and the
  style continuity bible. For Zerg or insectoid factions, prompts for upper-tier
  characters should state the humanized or humanoid balance and restrained
  insectoid motifs; prompts for lower-tier characters should state the stronger
  insectoid anatomy, carapace, limbs, eyes, mandibles, and swarm material
  language. Do not reuse the same insectoid descriptors across all tiers.
- Keep prompts suitable for image generation but not ComfyUI-specific.
- Mark assets that require a prior reference image or cannot be generated safely.

## Required Artifacts

- `{episode-id}/prompts/art-image-prompts.json`

## Artifact Contract

Return the envelope from `references/artifact-contract.md`. The artifact content
must be complete JSON that can be written directly to
`{episode-id}/prompts/art-image-prompts.json`.

## Quality Bar

Every prompt must trace to an asset ID and expected output path. Avoid prompts
that contradict continuity locks.
