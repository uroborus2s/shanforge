# Language Prompt Fix Flow Minor Contracts

## Scope

Only edit:

- `skills/agent-harness-construction/SKILL.md`
- `skills/ai-first-engineering/SKILL.md`
- `skills/article-writing/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/gitcommitzh/SKILL.md`
- `skills/skill-creator/SKILL.md`
- `skills/stratix-service/SKILL.md`
- `skills/subagent-driven-development/SKILL.md`

## Goal

Fix lower-severity language/prompt issues:

- add or tighten output contract and blocked semantics;
- add "do not use" boundaries where triggers are broad;
- reduce repeated gates without deleting required protections;
- clarify `subagent-driven-development` continuous execution versus `using-shanforge` routing;
- preserve all existing workflow hard gates and test-required phrases.

## Constraints

- Do not edit references, agents metadata, tests, or config.
- Be conservative with `gitcommitzh`, `document-templates`, `stratix-service`, and `subagent-driven-development`; current tests assert specific phrases.
- Do not remove PR / commit / review / human confirmation gates.

## Verification

Run relevant tests if possible:

- `uv run pytest tests/test_pr_commit_workflow_rules.py tests/test_execution_workflow_skills.py tests/test_deprecated_skill_cleanup.py tests/test_stratix_service_skill.py tests/test_skill_creator_skill_principles.py`
