# Asset Card Prompt Templates

Use this reference when writing asset design JSON, `art-image-prompts.json`, or
background image thread prompts.

## Short Filename Rule

All generated asset files use a stable short code. The basename without
extension must be 20 characters or fewer.

Examples:

```text
c001m.png
c001e01.png
p001m.png
p001e01.png
l001m.png
l001e01.png
f001m.png
r001s02.png
```

Store semantic names in JSON indexes, not long filenames.

## Output Path Routing

Use root `assets/` only for whole-series reusable assets:

```text
assets/characters/c001m.png
assets/locations/l001m.png
assets/props/p001m.png
assets/costumes/p002m.png
assets/style/s001m.png
```

Episode state cards belong to the episode directory:

```text
01/assets/characters/c001e01.png
01/assets/locations/l001e01.png
01/assets/props/p001e01.png
01/assets/costumes/p002e01.png
```

Do not place `character_episode_state_card`, `prop_episode_state_card`, or
`location_episode_scene_card` files in root `assets/`.

## Card Subtypes

- `character_master_card`: whole-series identity card for face, bone structure,
  body type, temperament, and identity anchors.
- `character_episode_state_card`: episode state card for wardrobe, wounds,
  dirt, emotion, props, and action state.
- `prop_master_card`: reusable item/flag/emblem/prop card for silhouette,
  material, proportions, markings, and use.
- `prop_episode_state_card`: episode item state card for wear, dirt, damage,
  placement, and use state.
- `location_master_scene_card`: reusable place card for geography, entrances,
  exits, spatial layout, light, material, and action zones.
- `location_episode_scene_card`: episode location state card for current time,
  weather, damage, staging, and continuity anchors.

## Character Card Fields

Required design fields:

```text
asset_id
file
asset_type
asset_subtype
display_name
identity_lock
body_metrics
episode_state
card_layout
continuity_refs
source_refs
usage
```

`identity_lock` must cover age impression, face shape/features, eyes, hair,
skin texture, height/body type, movement habits, and forbidden future reveals.

`body_metrics` must make scale visible to image models:

```text
height
weight_build
body_ratio
silhouette
scale_refs
```

Prefer relative visual scale in addition to numbers, for example "one head
taller than a human guard" or "twice the mass of a lightly armored soldier".

Character card output requirements:

```text
output_format_requirements
master_card_background: neutral plain
cutout_background: transparent alpha
required_views: front, side, back, three-quarter
detail_crops: face, hands, wardrobe texture, identity marks
scale_reference_required: true
```

## Prop And Item Card Fields

Required design fields:

```text
asset_id
file
asset_type
asset_subtype
display_name
prop_lock
physical_dimensions
episode_state
card_layout
continuity_refs
source_refs
usage
```

`prop_lock` must cover story use, owner character/faction, silhouette,
proportion, scale, material, wear/marks, flag/emblem/symbol rules, and
forbidden future reveals.

`physical_dimensions` must include concrete scale when useful:

```text
length
width
height
scale_reference
weight_feel
material_thickness
```

Use human-hand, tabletop, doorway, body, or carrying references when exact
numbers alone would not guide image generation.

For flags, emblems, symbols, records, seals, and text-like props, plan a master
card plus reference/line control. If exact marks are required, prefer a
transparent PNG/SVG post-composite over asking the video model to invent the
symbol.

Prop and item output requirements:

```text
output_format_requirements
master_card_background: neutral plain
cutout_background: transparent alpha
required_views: front, side, back, top/bottom when useful
detail_crops: material, markings, mechanism, damage, edges
scale_reference_required: true
```

## Location Scene Card Fields

Required design fields:

```text
asset_id
file
asset_type
asset_subtype
display_name
location_lock
episode_state
card_layout
continuity_refs
source_refs
usage
```

`location_lock` must cover story function, geography, entrances/exits, spatial
structure, action zones, camera-facing zones, continuity anchors, and prohibited
modern or wrong elements.

Location and video frame output requirements:

```text
output_format_requirements
canvas_aspect_ratio: 16:9 or project_defined
background_policy: scene_context or video_frame
composition_layers: foreground, midground, background
camera_requirements: distance, angle, screen direction, light, weather/time
```

## Scene Image Information Budget

Use this section whenever a location card, establishing plate, video reference
frame, or shot override is a wide scene, distant scene, crowd scene, battlefield,
large city, fortress, mountain pass, mass interior, or any scene with many
repeated small objects. The budget prevents image models from assigning equal
importance to the whole frame.

Add this optional design field to wide/group-heavy location and reference-frame
records:

```text
scene_information_budget:
  shot_scale: distant establishing wide shot | epic wide shot | large group scene | other
  main_visual_functions:
    - large readable shapes
    - lighting and atmosphere
    - clear silhouettes and scale
  detail_priority:
    highest_detail:
      max_elements: 3-5
      examples: central gate, main road, nearest banners, hero silhouette,
        largest creatures, primary light source
    medium_detail: midground masses, wall flags, readable fires, nearest groups
    low_detail: distant soldiers, guards, background towers, far terrain
    impression_only: distant crowds, arrows, tiny weapons, parapet figures,
      far banners, secondary animals or vehicles
  distance_simplification:
    grouped_silhouettes: true
    massing_over_individuals: true
    atmospheric_perspective: fog, smoke, snow, rain, dust, haze, or depth falloff
  forbidden_detail_behavior:
    - equal-detail rendering across the whole frame
    - over-detailed distant figures
    - granular crowd texture
    - particleized stone or architecture
    - noisy micro-detail or AI speckle
    - full-frame ultra-detail
    - visual information overload
```

Wide scene prompts should state that the image is an establishing shot, not a
character sheet, unit showcase, architecture inventory, weapon catalog, or
emblem proof sheet. Only the `highest_detail` elements may receive fine detail;
all other content must be simplified by distance, atmosphere, and grouping.

Use this copy-ready wording pattern for wide scene prompts:

```text
This is a true distant establishing wide shot. Prioritize scale, atmosphere,
composition, and silhouette clarity over small object detail. Keep strong depth
layers. Only 3-5 elements may receive high detail. Distant people, creatures,
vehicles, wall figures, weapons, and small banners must read as grouped
silhouettes or masses, not individually readable miniatures. Let fog, smoke,
snow, dust, rain, haze, and atmospheric perspective simplify small forms.
```

Wide scene negative prompts must include:

```text
no equal-detail rendering across the whole frame, no over-detailed distant
soldiers or crowd members, no granular crowd texture, no particleized stone, no
noisy micro-detail, no AI speckle, no smoke pretending to be architectural
detail, no distant objects rendered as sharp individual miniatures, no
full-frame ultra-detail, no cluttered battlefield or city texture, no visual
information overload.
```

## Image Output Format Contract

Every asset plan, manifest record, image prompt record, thread prompt, and QC
report must preserve this contract:

```text
output_format:
  deliverable_kind
  file_format
  minimum_resolution
  background_policy
  alpha_policy
  canvas_aspect_ratio
  required_views
  composition_layers
  qc_checks
```

Use these policies:

```text
background_policy: neutral_plain | transparent_alpha | scene_context | video_frame
alpha_policy: required | forbidden | optional
canvas_aspect_ratio: 1:1 | 4:5 | 16:9 | project_defined
```

`composition_layers` must always exist. For asset cards and cutouts, fill
foreground, midground, and background with "not_applicable" or the literal card
layout layer. For video reference frames and shot overrides, foreground,
midground, and background must describe visible scene content.

Required deliverable behavior:

```text
neutral master card:
  neutral_plain background, alpha forbidden, readable shape and scale
transparent cutout:
  transparent_alpha background, alpha required, clean full silhouette
turnaround sheet:
  neutral_plain background, front/side/back/three-quarter views
detail crop sheet:
  neutral_plain background, labeled visual crops without process metadata
video reference frame:
  video_frame background, alpha forbidden, 16:9, foreground/midground/background
shot override frame:
  video_frame background, alpha forbidden, 16:9, exact shot composition
precision overlay:
  transparent_alpha background, alpha required, exact symbol/edge control
```

## Prompt Split

Every prompt record separates process metadata from visible model text:

```text
production_metadata:
  asset_id
  asset_subtype
  output_file
  prompt_id
  source_refs
  continuity_refs
  usage

model_visible_prompt:
  visible_goal
  style_quality
  subject_content
  composition_motion
  visible_continuity
  negative_prompt
```

Never put `asset_id`, `episode_id`, `output_file`, `source_refs`, or `usage`
inside `model_visible_prompt`.

## Copy-Ready Prompt Fields

Every `art-image-prompts.json` record must include copy-ready prompt text:

```text
copy_ready:
  positive_prompt
  negative_prompt
  chatgpt_image_prompt
  gemini_image_prompt
```

`positive_prompt` is the merged visible prompt: visible goal, style and image
quality, subject content, composition and motion, and visible continuity.
`negative_prompt` is the standalone negative prompt. `chatgpt_image_prompt` and
`gemini_image_prompt` are complete natural-language instructions that can be
copied directly into those tools. They may mention that the output should be an
image, but they must not include process metadata such as file paths or asset
IDs.

## Six Visible Prompt Sections

1. Visible goal: what asset card or reference image should be created.
2. Style and image quality: realism, film texture, materials, light, and medium.
3. Subject content: identity, object, location, wardrobe, damage, weather, or
   visible state.
4. Composition and motion: reference board layout, view angles, scale details,
   natural poses, or scene viewpoints.
5. Visible continuity constraints: what must remain unchanged and what must not
   be revealed early.
6. Negative prompt: unwanted styles, artifacts, wrong marks, wrong text,
   modern elements, watermarks, and continuity violations.

## Creation Dependencies

Asset plans must expose creation order before image generation starts:

```text
creation_order
creation_phase
depends_on_assets
blocks_assets
dependency_reason
priority
```

Recommended order:

```text
style references
-> master character/location/prop cards
-> episode state cards
-> precision flags/emblems/symbols/text-like props
-> first/last/reference frames
-> shot overrides
```

Use `depends_on_assets` for hard visual dependencies, for example an episode
state card depending on a master character card, or a reference frame depending
on character, prop, and location cards.
