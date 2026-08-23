from __future__ import annotations

import importlib.util
import json
import shlex
import socket
import subprocess
import sys
import types
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, path: Path):
    for module_name in tuple(sys.modules):
        if module_name == "office" or module_name.startswith("office."):
            sys.modules.pop(module_name)
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def make_docx(path: Path, document_xml: bytes = b"<w:document/>") -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document_xml)


def make_xlsx(path: Path) -> None:
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("_rels/.rels", "<Relationships/>")
        archive.writestr("xl/workbook.xml", "<workbook/>")
        archive.writestr("xl/worksheets/sheet1.xml", "<worksheet/>")


def test_docx_accept_changes_fails_on_timeout_and_unaccepted_output(
    tmp_path: Path, monkeypatch
) -> None:
    script = REPO_ROOT / "skills/docx/scripts/accept_changes.py"
    module = load_script("docx_accept_changes_test", script)
    source = tmp_path / "source.docx"
    output = tmp_path / "output.docx"
    make_docx(source, b"<w:document><w:ins/></w:document>")
    monkeypatch.setattr(module, "_setup_libreoffice_macro", lambda: True)

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("soffice", 30)

    monkeypatch.setattr(module.subprocess, "run", timeout)
    _, message = module.accept_changes(str(source), str(output))
    assert message.startswith("Error:")
    assert "timed out" in message

    monkeypatch.setattr(
        module.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess([], 0, "", ""),
    )
    _, message = module.accept_changes(str(source), str(output))
    assert message.startswith("Error:")
    assert "tracked changes remain" in message


def test_pdf_bounding_box_failure_is_nonzero(tmp_path: Path) -> None:
    fields = tmp_path / "fields.json"
    fields.write_text(
        json.dumps(
            {
                "form_fields": [
                    {
                        "description": "overlap",
                        "page_number": 1,
                        "label_bounding_box": [0, 0, 20, 20],
                        "entry_bounding_box": [10, 10, 30, 30],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    script = REPO_ROOT / "skills/pdf/scripts/check_bounding_boxes.py"
    result = subprocess.run(
        [sys.executable, str(script), str(fields)], capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "FAILURE" in result.stdout


def test_pdf_image_conversion_creates_output_directory(tmp_path: Path, monkeypatch) -> None:
    saved: list[Path] = []

    class FakeImage:
        size = (100, 100)

        def save(self, path):
            saved.append(Path(path))
            Path(path).write_bytes(b"png")

    fake_pdf2image = types.ModuleType("pdf2image")
    fake_pdf2image.convert_from_path = lambda *_args, **_kwargs: [FakeImage()]
    monkeypatch.setitem(sys.modules, "pdf2image", fake_pdf2image)
    module = load_script(
        "pdf_convert_test",
        REPO_ROOT / "skills/pdf/scripts/convert_pdf_to_images.py",
    )
    output = tmp_path / "missing" / "images"
    module.convert("input.pdf", output)
    assert saved == [output / "page_1.png"]
    assert saved[0].is_file()


def test_with_server_drains_logs_and_stops_the_process_tree(tmp_path: Path) -> None:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    server_code = (
        "print('x' * 200000, flush=True); "
        "from http.server import HTTPServer, BaseHTTPRequestHandler; "
        f"HTTPServer(('127.0.0.1', {port}), BaseHTTPRequestHandler).serve_forever()"
    )
    server_command = f"{shlex.quote(sys.executable)} -c {shlex.quote(server_code)}"
    script = REPO_ROOT / "skills/webapp-testing/scripts/with_server.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--server",
            server_command,
            "--port",
            str(port),
            "--timeout",
            "5",
            "--",
            sys.executable,
            "-c",
            "pass",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    with socket.socket() as check:
        check.settimeout(0.2)
        assert check.connect_ex(("127.0.0.1", port)) != 0


def test_xlsx_validator_accepts_xlsx_and_rejects_broken_package(
    tmp_path: Path,
) -> None:
    script = REPO_ROOT / "skills/xlsx/scripts/office/validate.py"
    valid = tmp_path / "valid.xlsx"
    make_xlsx(valid)
    result = subprocess.run(
        [sys.executable, str(script), str(valid)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr

    broken = tmp_path / "broken.xlsx"
    with zipfile.ZipFile(broken, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
    result = subprocess.run(
        [sys.executable, str(script), str(broken)], capture_output=True, text=True
    )
    assert result.returncode == 1


def test_xlsx_recalc_uses_isolated_profile_and_fails_on_timeout(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_script("xlsx_recalc_test", REPO_ROOT / "skills/xlsx/scripts/recalc.py")
    workbook = tmp_path / "book.xlsx"
    workbook.write_bytes(b"xlsx")
    captured_profile: list[Path] = []

    def setup(profile: Path) -> bool:
        captured_profile.append(profile)
        return True

    monkeypatch.setattr(module, "setup_libreoffice_macro", setup)

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("soffice", 1)

    monkeypatch.setattr(module.subprocess, "run", timeout)
    result = module.recalc(workbook, timeout=1)
    assert "timed out" in result["error"]
    assert len(captured_profile) == 1
    assert captured_profile[0].parent != Path.home()
