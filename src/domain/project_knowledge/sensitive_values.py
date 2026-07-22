"""Deterministic redaction shared by indexing, receipts and rendered views."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

REDACTED = "[REDACTED]"

_SENSITIVE_KEY = re.compile(
    r"(?:^|[_-])(password|passwd|secret|token|api[_-]?key|private[_-]?key|"
    r"authorization|cookie|client[_-]?secret)(?:$|[_-])",
    re.IGNORECASE,
)
_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
    re.compile(r"\b(?:sk|pk)-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}\b", re.IGNORECASE),
)
_VALUE_MARKERS = (
    "PRIVATE KEY",
    "sk-",
    "pk-",
    "ghp_",
    "github_pat_",
    "AKIA",
    "Bearer ",
    "bearer ",
)


def redact_text(value: str) -> str:
    """Fast-path ordinary text and redact recognizable credential material."""

    if not any(marker in value for marker in _VALUE_MARKERS):
        return value
    redacted = value
    for pattern in _VALUE_PATTERNS:
        redacted = pattern.sub(REDACTED, redacted)
    return redacted


def sanitize_value(value: Any, *, key: str | None = None) -> Any:
    """Return a JSON-compatible value with sensitive keys and strings redacted."""

    if key is not None and _SENSITIVE_KEY.search(key):
        return REDACTED
    if isinstance(value, Mapping):
        return {
            str(item_key): sanitize_value(item_value, key=str(item_key))
            for item_key, item_value in value.items()
        }
    if isinstance(value, tuple):
        return tuple(sanitize_value(item) for item in value)
    if isinstance(value, list):
        return [sanitize_value(item) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value
