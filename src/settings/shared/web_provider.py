from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote_to_bytes, urlparse
from urllib.request import Request, urlopen

from runtime.ports.execution_backends import WebDocumentProviderPort, WebSearchProviderPort


class _ReadableTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if stripped:
            self._parts.append(stripped)

    def text(self) -> str:
        return "\n".join(self._parts)


@dataclass(slots=True)
class InMemoryWebSearchProvider(WebSearchProviderPort):
    """Token-matching search provider for local development and tests."""

    records: tuple[dict[str, Any], ...] = ()

    def search(
        self,
        query: str,
        limit: int = 10,
        filters: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], ...]:
        normalized_limit = max(1, min(limit, 20))
        normalized_filters = dict(filters or {})
        normalized_query = query.strip()
        if not normalized_query:
            return self.records[:normalized_limit]

        if _looks_like_url(normalized_query):
            return (
                {
                    "url": normalized_query,
                    "title": normalized_query,
                    "snippet": "Direct URL lookup",
                    "rank": 1,
                },
            )

        tokens = tuple(token for token in normalized_query.lower().split() if token)
        matched: list[dict[str, Any]] = []
        for record in self.records:
            if not _record_matches_filters(record, normalized_filters):
                continue
            haystack = " ".join(
                str(record.get(field) or "").lower()
                for field in ("url", "title", "snippet", "search_text")
            )
            score = sum(haystack.count(token) for token in tokens)
            if score <= 0:
                continue
            payload = dict(record)
            payload["score"] = float(score)
            matched.append(payload)

        matched.sort(key=lambda item: item.get("score", 0.0), reverse=True)
        return tuple(matched[:normalized_limit])


@dataclass(slots=True)
class LocalWebDocumentProvider(WebDocumentProviderPort):
    """Minimal fetch/extract provider for local files, data URLs, and HTTP(S)."""

    timeout_seconds: float = 10.0
    user_agent: str = "shanforge-local-web-provider/0.1"

    def fetch(self, url: str) -> dict[str, Any]:
        parsed = urlparse(url)
        if parsed.scheme == "file":
            return self._fetch_file_url(url, parsed)
        if parsed.scheme == "data":
            return self._fetch_data_url(url)
        if parsed.scheme in {"http", "https"}:
            return self._fetch_http_url(url)
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme or '<empty>'}")

    def extract(self, url: str, mode: str = "readable") -> dict[str, Any]:
        payload = self.fetch(url)
        content = str(payload.get("content") or "")
        extracted_text = _extract_readable_text(content)
        result = dict(payload)
        result["mode"] = mode
        result["extracted_text"] = extracted_text
        return result

    def _fetch_file_url(self, url: str, parsed) -> dict[str, Any]:
        local_path = Path(unquote_to_bytes(parsed.path).decode("utf-8")).expanduser()
        content = local_path.read_text(encoding="utf-8")
        return {
            "url": url,
            "title": _detect_title(content, fallback=local_path.name),
            "content": content,
            "metadata": {
                "source": "file",
                "path": str(local_path),
            },
        }

    def _fetch_data_url(self, url: str) -> dict[str, Any]:
        header, _, raw_data = url.partition(",")
        is_base64 = header.endswith(";base64")
        media_type = header[5:].removesuffix(";base64") or "text/plain;charset=utf-8"
        data_bytes = (
            base64.b64decode(raw_data)
            if is_base64
            else unquote_to_bytes(raw_data)
        )
        try:
            content = data_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Data URL is not valid UTF-8 text") from exc
        return {
            "url": url,
            "title": _detect_title(content, fallback="data-url"),
            "content": content,
            "metadata": {
                "source": "data",
                "media_type": media_type,
                "size_bytes": len(data_bytes),
            },
        }

    def _fetch_http_url(self, url: str) -> dict[str, Any]:
        request = Request(url, headers={"User-Agent": self.user_agent})
        with urlopen(request, timeout=self.timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            data = response.read()
            try:
                content = data.decode(charset)
            except (LookupError, UnicodeDecodeError, binascii.Error):
                content = data.decode("utf-8", errors="replace")
            return {
                "url": url,
                "title": _detect_title(content, fallback=url),
                "content": content,
                "metadata": {
                    "source": "http",
                    "status": getattr(response, "status", None),
                    "media_type": response.headers.get_content_type(),
                    "size_bytes": len(data),
                },
            }


def _looks_like_url(value: str) -> bool:
    return value.startswith(("http://", "https://", "file://", "data:"))


def _record_matches_filters(record: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, expected in filters.items():
        if expected is None:
            continue
        if record.get(key) != expected:
            return False
    return True


def _extract_readable_text(content: str) -> str:
    if "<" not in content or ">" not in content:
        return content.strip()

    parser = _ReadableTextParser()
    parser.feed(content)
    text = parser.text().strip()
    return text or re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", content)).strip()


def _detect_title(content: str, fallback: str) -> str:
    title_match = re.search(r"<title>\s*(?P<title>.*?)\s*</title>", content, re.IGNORECASE | re.DOTALL)
    if title_match:
        return re.sub(r"\s+", " ", title_match.group("title")).strip()

    heading_match = re.search(r"^\s*#\s+(?P<title>.+)$", content, re.MULTILINE)
    if heading_match:
        return heading_match.group("title").strip()

    return fallback
