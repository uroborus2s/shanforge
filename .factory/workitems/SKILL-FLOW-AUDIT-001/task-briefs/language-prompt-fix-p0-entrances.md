# Language Prompt Fix P0 Entrances

## Scope

Only edit:

- `skills/ui-ux-pro-max/SKILL.md`
- `skills/shadcn/SKILL.md`
- `skills/doc-coauthoring/SKILL.md`
- `skills/algorithmic-art/SKILL.md`

## Goal

Use `.factory/workitems/SKILL-FLOW-AUDIT-001/reviews/language-prompt-review-iteration-2.md` to fix the P0 low-score issues:

- reduce verbose tutorial/database content in main `SKILL.md`;
- remove old ecosystem wording such as Claude, injected `!npx` snippets, Anthropic brand requirements;
- clarify when to use / not use the skill;
- add output contract, evidence, verification, and failure semantics;
- keep frontmatter valid.

## Constraints

- Do not edit references, tests, config, or other skills.
- Do not delete useful assets/scripts/data.
- Prefer a short main entrance that points to existing references/assets when needed.
- Preserve any phrases required by current tests if they exist.

## Verification

Run at least a syntax/read smoke check for the edited files. If time allows, run relevant pytest discovered from tests.
