# Language Prompt Fix File And Text Tools

## Scope

Only edit:

- `skills/docx/SKILL.md`
- `skills/pdf/SKILL.md`
- `skills/xlsx/SKILL.md`
- `skills/humanizer/SKILL.md`
- `skills/webapp-testing/SKILL.md`

## Goal

Fix tool-speedrun style entrances:

- split read/create/edit/verify branches in prose;
- add safe output rules, verification requirements, failure semantics, and status package;
- remove or neutralize old author/tool-install wording such as default Claude author or global install instructions;
- clarify `webapp-testing` versus `browser-control` boundary.

## Constraints

- Do not edit scripts, templates, or binary assets.
- Do not add dependencies.
- Preserve useful command names and local scripts.

## Verification

Run a read/smoke check. If tests reference these skills, run the relevant tests.
