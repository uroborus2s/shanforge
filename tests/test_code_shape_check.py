from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/tdd-workflow/scripts/check_code_shape.py"


def test_rejects_named_local_function_and_reports_one_call_helper(tmp_path: Path) -> None:
    source = tmp_path / "sample.py"
    source.write_text(
        "def helper():\n    return 1\n\n"
        "def outer():\n    def local():\n        return helper()\n    return local()\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(source)], text=True, capture_output=True
    )

    assert result.returncode == 1
    assert "named local function local" in result.stdout
    assert "helper candidate helper has one call site" in result.stdout


def test_rejects_lambda_in_function_but_allows_module_lambda(tmp_path: Path) -> None:
    nested = tmp_path / "nested.py"
    nested.write_text("def outer():\n    return lambda: 1\n", encoding="utf-8")
    module = tmp_path / "module.py"
    module.write_text("callback = lambda: 1\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(nested), str(module)],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert f"{nested}:2: lambda in function body" in result.stdout
    assert f"{module}:1: lambda in function body" not in result.stdout


def test_allows_flat_functions(tmp_path: Path) -> None:
    source = tmp_path / "flat.py"
    source.write_text("def main():\n    return 1\n", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(source)], text=True, capture_output=True
    )

    assert result.returncode == 0
