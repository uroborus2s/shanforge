from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from runtime.ports.execution_backends import BrowserAutomationProviderPort, WebDocumentProviderPort
from settings.shared.web_provider import LocalWebDocumentProvider


@dataclass(slots=True)
class InMemoryBrowserAutomationProvider(BrowserAutomationProviderPort):
    """Minimal session-oriented browser provider for local development and tests."""

    document_provider: WebDocumentProviderPort = field(default_factory=LocalWebDocumentProvider)
    _sessions: dict[str, dict[str, Any]] = field(default_factory=dict)

    def open_page(
        self,
        url: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        document = self.document_provider.fetch(url)
        session_token = session_id or f"browser-{uuid4().hex[:10]}"
        self._sessions[session_token] = {
            "url": url,
            "content": str(document.get("content") or ""),
            "extracted_text": str(document.get("extracted_text") or ""),
            "title": str(document.get("title") or ""),
            "inputs": {},
            "actions": [],
            "metadata": dict(document.get("metadata") or {}),
        }
        return {
            "session_token": session_token,
            "current_url": url,
            "metadata": {
                "title": document.get("title"),
                "content_bytes": len(str(document.get("content") or "").encode("utf-8")),
            },
        }

    def inspect_dom(
        self,
        session_token: str,
        selector: str | None = None,
    ) -> dict[str, Any]:
        session = self._require_session(session_token)
        value = self._select_value(session, selector)
        return {
            "session_token": session_token,
            "kind": "dom" if selector else "page",
            "value": value,
            "metadata": {
                "selector": selector,
                "matched": bool(value),
                "current_url": session["url"],
            },
        }

    def click(
        self,
        session_token: str,
        target: str,
    ) -> dict[str, Any]:
        session = self._require_session(session_token)
        matched = bool(self._select_value(session, target))
        session["actions"].append({"action": "click", "target": target, "matched": matched})
        return {
            "session_token": session_token,
            "action": "click",
            "status": "clicked" if matched else "not_found",
            "metadata": {
                "target": target,
                "current_url": session["url"],
            },
        }

    def type_text(
        self,
        session_token: str,
        target: str,
        value: str,
    ) -> dict[str, Any]:
        session = self._require_session(session_token)
        session["inputs"][target] = value
        session["actions"].append({"action": "type_text", "target": target, "value": value})
        return {
            "session_token": session_token,
            "action": "type_text",
            "status": "typed",
            "metadata": {
                "target": target,
                "value_length": len(value),
                "current_url": session["url"],
            },
        }

    def wait_for(
        self,
        session_token: str,
        condition: dict[str, Any],
    ) -> dict[str, Any]:
        session = self._require_session(session_token)
        matched = self._matches_condition(session, condition)
        return {
            "session_token": session_token,
            "kind": "wait",
            "value": "matched" if matched else "unmatched",
            "metadata": {
                "condition": dict(condition),
                "current_url": session["url"],
            },
        }

    def capture_screenshot(
        self,
        session_token: str,
        label: str | None = None,
    ) -> dict[str, Any]:
        session = self._require_session(session_token)
        label_value = label or "capture"
        uri = f"browser://{session_token}/screenshots/{label_value}"
        preview = self._select_value(session, None)[:160]
        return {
            "session_token": session_token,
            "kind": "screenshot",
            "value": uri,
            "metadata": {
                "label": label_value,
                "preview": preview,
                "current_url": session["url"],
            },
        }

    def _require_session(self, session_token: str) -> dict[str, Any]:
        try:
            return self._sessions[session_token]
        except KeyError as exc:
            raise KeyError(f"Unknown browser session: {session_token}") from exc

    def _select_value(self, session: dict[str, Any], selector: str | None) -> str:
        content = str(session.get("content") or "")
        if selector is None:
            return str(session.get("extracted_text") or content).strip()
        if selector in content:
            return selector
        lowered_content = content.lower()
        lowered_selector = selector.lower()
        if lowered_selector in lowered_content:
            return selector
        return ""

    def _matches_condition(self, session: dict[str, Any], condition: dict[str, Any]) -> bool:
        if "text" in condition:
            return str(condition["text"]) in self._select_value(session, None)
        if "selector" in condition:
            return bool(self._select_value(session, str(condition["selector"])))
        if "url_contains" in condition:
            return str(condition["url_contains"]) in str(session.get("url") or "")
        return False
