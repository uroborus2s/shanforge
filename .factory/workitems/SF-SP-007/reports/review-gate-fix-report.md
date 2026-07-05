# Review Gate Fix Report

- Work item: SF-SP-007
- Task: independent review hard gate repair
- Actor: codex
- Status: self_check_passed

## Root Cause

`requesting-code-review` and the Superpowers workflow plan allowed same-thread review language to behave like independent review. This made it possible to record `approved`, `review_score=96`, and `pending_human_confirmation` without real reviewer independence evidence.

Direct cause:
- `skills/requesting-code-review/SKILL.md` still allowed same-thread review packaging to use the independent review template.
- `review-score-rubric.md` did not require `reviewer_type`, `reviewer_id`, or `reviewer_independence_evidence`.
- Task and independent review templates did not separate `author_self_check_score` from `review_score`.
- The plan document did not explicitly block `pending_human_confirmation` when independent review evidence is missing.

## Changes

- Added `tests/test_independent_review_gate.py` as a regression gate.
- Updated `skills/requesting-code-review/SKILL.md` to make same-thread author self-check produce only `self_check_passed`.
- Updated review templates and rubric to require reviewer independence metadata before `approved` or `review_score`.
- Updated `superpowers-workflow-integration-plan.md` sections 7.6-7.8 with the hard gate.
- Appended correction events to `SF-SP-007` and `.factory/memory/review-ledger.jsonl`.

## Current State

This repair is implemented and locally verified. It is not independently approved. The current gate remains `needs_independent_review` before SF-SP-008 or human confirmation.
