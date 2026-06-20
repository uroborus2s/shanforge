from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from runtime.capability.contracts import CapabilityInvocationContext
from runtime.browser.service import BrowserService
from runtime.terminal.models import CommandExecutionRequest
from runtime.terminal.service import TerminalService
from runtime.web_access.service import WebAccessService
from settings.shared import (
    InMemoryBrowserAutomationProvider,
    InMemoryWebSearchProvider,
    LocalWebDocumentProvider,
)
from settings.workspace import LocalGitProvider, LocalShellCommandProvider


class RuntimeExecutionBridgeTests(unittest.TestCase):
    def test_web_access_service_searches_fetches_extracts_and_cites(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            page_path = root / "page.html"
            page_path.write_text(
                "<html><head><title>Bridge Doc</title></head><body><h1>Bridge</h1><p>Search token</p></body></html>",
                encoding="utf-8",
            )
            page_url = page_path.resolve().as_uri()
            service = WebAccessService(
                search_provider=InMemoryWebSearchProvider(
                    records=(
                        {
                            "url": page_url,
                            "title": "Bridge Doc",
                            "snippet": "Search token snippet",
                            "search_text": "bridge doc search token",
                        },
                    )
                ),
                document_provider=LocalWebDocumentProvider(),
            )
            context = CapabilityInvocationContext(session_id="session-web")

            hits = service.search_web("search token", 5, None, context)
            self.assertEqual(hits[0].title, "Bridge Doc")

            fetched = service.fetch_url(page_url, context)
            extracted = service.extract_document(page_url, "readable", context)
            citation = service.normalize_citation(extracted, context)

            self.assertEqual(fetched.title, "Bridge Doc")
            self.assertIn("Search token", extracted.extracted_text)
            self.assertEqual(citation.source_uri, page_url)

    def test_terminal_service_runs_commands_and_git_with_writeset_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            service = TerminalService(
                shell_provider=LocalShellCommandProvider(),
                git_provider=LocalGitProvider(),
            )
            context = CapabilityInvocationContext(
                session_id="session-terminal",
                workspace_root=str(root),
                cwd=str(root),
                approval_ref="approval-terminal",
            )

            command_result = service.run_command(
                CommandExecutionRequest(
                    argv=("/bin/sh", "-lc", "printf 'bridge' > output.txt"),
                    cwd=str(root),
                ),
                context,
            )
            command_writeset = service.inspect_writeset(command_result, context)
            self.assertIn("output.txt", command_writeset.created_paths)
            self.assertEqual(command_result.exit_code, 0)

            git_init = service.run_git(("init",), str(root), context)
            self.assertEqual(git_init.exit_code, 0)

    def test_browser_service_opens_inspects_waits_and_mutates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            page_path = root / "form.html"
            page_path.write_text(
                "<html><head><title>Browser Form</title></head><body><button>Submit</button><div>Ready</div></body></html>",
                encoding="utf-8",
            )
            page_url = page_path.resolve().as_uri()
            service = BrowserService(
                browser_provider=InMemoryBrowserAutomationProvider(
                    document_provider=LocalWebDocumentProvider()
                )
            )
            read_context = CapabilityInvocationContext(session_id="session-browser")
            write_context = CapabilityInvocationContext(
                session_id="session-browser",
                approval_ref="approval-browser",
            )

            handle = service.open_page(page_url, read_context)
            inspection = service.inspect_dom(handle.session_token, "Submit", read_context)
            click_receipt = service.click(handle.session_token, "Submit", write_context)
            type_receipt = service.type_text(
                handle.session_token,
                "input[name=q]",
                "bridge",
                write_context,
            )
            wait_observation = service.wait_for(
                handle.session_token,
                {"text": "Ready"},
                read_context,
            )
            screenshot = service.capture_screenshot(handle.session_token, "ready", read_context)

            self.assertEqual(handle.current_url, page_url)
            self.assertEqual(inspection.kind, "dom")
            self.assertEqual(click_receipt.status, "clicked")
            self.assertEqual(type_receipt.status, "typed")
            self.assertEqual(wait_observation.value, "matched")
            self.assertTrue(screenshot.value.startswith("browser://"))


if __name__ == "__main__":
    unittest.main()
