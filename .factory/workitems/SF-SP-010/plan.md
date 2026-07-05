# SF-SP-010 Work Item Plan

## Scope

- Synchronize the Superpowers workflow integration plan after `SF-SP-009` was committed.
- Ensure development-process navigation exposes the Superpowers plan, PM control plane, memory governance plan, and test report entry.
- Treat `project-management-control-plane.md` as a required navigation target when PM links are present.
- Update `.factory/memory/` summaries and `doc-map.md` so AI default reading points at the refreshed facts.
- Add focused structure tests for documentation navigation and stale summary prevention.

## Out Of Scope

- No new workflow skill.
- No script gate or CLI gate.
- No unrelated PM HTML, Stratix, writer-room, director-room, art-room, or architecture code changes.
- No PM control plane content rewrite beyond verifying it as a navigation target.
- No commit before independent review approval and human confirmation.

## Verification

- `.venv/bin/pytest tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py`
- `.venv/bin/ruff check tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py`
- JSONL parse for `.factory/workitems/SF-SP-010/ledger.jsonl` and `.factory/memory/review-ledger.jsonl`
- `git diff --check`

## Review Gate

Implementation can only reach `ready_for_review`. A separate independent review must approve it before human confirmation.
