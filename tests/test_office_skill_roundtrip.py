from __future__ import annotations

import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("skill", "suffix", "contents"),
    [
        (
            "docx",
            ".docx",
            {
                "[Content_Types].xml": b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
                "_rels/.rels": b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>',
                "word/document.xml": b'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body/></w:document>',
            },
        ),
        (
            "xlsx",
            ".xlsx",
            {
                "[Content_Types].xml": b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
                "_rels/.rels": b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>',
                "xl/workbook.xml": b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"/>',
                "xl/worksheets/sheet1.xml": b'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"/>',
            },
        ),
    ],
)
def test_minimal_unpack_pack_unpack_roundtrip(
    tmp_path: Path, skill: str, suffix: str, contents: dict[str, bytes]
) -> None:
    original = tmp_path / f"source{suffix}"
    with zipfile.ZipFile(original, "w") as archive:
        for name, content in contents.items():
            archive.writestr(name, content)
    office = REPO_ROOT / "skills" / skill / "scripts/office"
    unpacked = tmp_path / "unpacked"
    packed = tmp_path / f"repacked{suffix}"
    repeated = tmp_path / "repeated"
    shim = tmp_path / "shim" / "defusedxml"
    shim.mkdir(parents=True)
    (shim / "minidom.py").write_text("from xml.dom.minidom import *\n", encoding="utf-8")
    environment = {**os.environ, "PYTHONPATH": str(tmp_path / "shim")}

    for command in (
        [
            sys.executable, str(office / "unpack.py"), str(original), str(unpacked),
            "--merge-runs", "false", "--simplify-redlines", "false",
        ],
        [
            sys.executable, str(office / "pack.py"), str(unpacked), str(packed),
            "--validate", "false",
        ],
        [
            sys.executable, str(office / "unpack.py"), str(packed), str(repeated),
            "--merge-runs", "false", "--simplify-redlines", "false",
        ],
        [sys.executable, str(office / "validate.py"), str(packed), "--package-only"],
    ):
        result = subprocess.run(command, text=True, capture_output=True, env=environment)
        assert result.returncode == 0, result.stderr + result.stdout

    with zipfile.ZipFile(packed) as archive:
        assert set(contents).issubset(archive.namelist())
    assert all((repeated / name).is_file() for name in contents)
