# SF-SP-010 Iteration 1 Verification

## Red

Command:

```bash
.venv/bin/pytest tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py
```

Observed result:

- Exit code: `1`
- Result: `2 failed, 4 passed`
- Failures:
  - Root navigation did not expose `memory-governance-implementation-plan.md`.
  - Superpowers plan and memory did not yet say `SF-SP-009` was committed as `9296f58` or that `SF-SP-010` had started.

## Green

Command:

```bash
.venv/bin/pytest tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py
```

Observed result:

- Exit code: `0`
- Result: `6 passed`

## Additional Checks

Command:

```bash
.venv/bin/ruff check tests/test_sf_sp_010_documentation_navigation.py tests/test_superpowers_reference_migration.py
```

Observed result:

- Exit code: `0`
- Result: `All checks passed!`

Command:

```bash
python3 -c 'import json, pathlib; files=[pathlib.Path(".factory/workitems/SF-SP-010/ledger.jsonl"), pathlib.Path(".factory/memory/review-ledger.jsonl")]; total=0
for path in files:
    count=0
    for lineno,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if line.strip():
            json.loads(line); total += 1; count += 1
    print(f"{path}: {count}")
print(f"parsed {total} jsonl records from {len(files)} files")'
```

Observed result:

- Exit code: `0`
- Result:
  - `.factory/workitems/SF-SP-010/ledger.jsonl: 5`
  - `.factory/memory/review-ledger.jsonl: 27`
  - `parsed 32 jsonl records from 2 files`

Command:

```bash
git diff --check
```

Observed result:

- Exit code: `0`
- Result: no output

## Pending Gate

- Independent review
