from __future__ import annotations

import hashlib
import hmac
import json
import os
import time
import urllib.error
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qsl, unquote, urlencode, urlparse
from urllib.request import Request, urlopen


@dataclass(slots=True)
class LocalHttpClientProvider:
    """Reserved skeleton provider for outbound HTTP backends."""

    backend_name: str = "local-http"
    timeout_seconds: float = 5.0
    user_agent: str = "shanforge-local-http/0.1"
    retry_status_codes: tuple[int, ...] = (408, 429, 500, 502, 503, 504)
    retry_backoff_seconds: float = 0.0
    _last_request_report: dict[str, Any] = field(default_factory=dict)

    def request(
        self,
        method: str,
        url: str,
        payload: Mapping[str, Any] | None = None,
        options: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        normalized_method = str(method or "").upper()
        parsed = urlparse(url)
        if normalized_method == "GET" and parsed.scheme == "file":
            path = Path(unquote(parsed.path)).expanduser().resolve()
            document = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(document, dict):
                return dict(document)
            return {"data": document}
        if parsed.scheme in {"http", "https"}:
            return self._request_http(
                normalized_method,
                url,
                payload,
                options=options,
            )
        raise NotImplementedError(
            "LocalHttpClientProvider is a settings-layer skeleton. "
            "Bind a real HTTP backend before use."
        )

    def last_request_report(self) -> Mapping[str, Any]:
        return dict(self._last_request_report)

    def _request_http(
        self,
        method: str,
        url: str,
        payload: Mapping[str, Any] | None = None,
        *,
        options: Mapping[str, Any] | None = None,
    ) -> Mapping[str, Any]:
        request_options = dict(options or {})
        headers = self._base_headers(request_options)
        timeout_seconds = self._timeout_seconds(request_options)
        max_retries = self._max_retries(request_options)
        retry_status_codes = self._retry_status_codes(request_options)
        retry_backoff_seconds = self._retry_backoff_seconds(request_options)
        request_url = url
        data: bytes | None = None
        if method == "GET":
            if payload:
                query = urlencode(
                    {
                        key: value
                        for key, value in payload.items()
                        if value is not None
                    },
                    doseq=True,
                )
                separator = "&" if "?" in request_url else "?"
                request_url = f"{request_url}{separator}{query}" if query else request_url
        elif method in {"POST", "PUT", "PATCH", "DELETE"}:
            headers["Content-Type"] = "application/json"
            data = json.dumps(dict(payload or {})).encode("utf-8")
        else:
            raise NotImplementedError(f"Unsupported HTTP method: {method}")
        auth_kind = self._apply_auth_headers(
            headers,
            options=request_options,
            method=method,
            request_url=request_url,
            data=data,
        )

        attempt_count = 0
        while True:
            attempt_count += 1
            request = Request(request_url, data=data, headers=headers, method=method)
            try:
                with urlopen(request, timeout=timeout_seconds) as response:
                    raw_body = response.read()
                    parsed = self._parse_response_body(raw_body, response.headers)
                    self._record_request_report(
                        method=method,
                        url=request_url,
                        auth_kind=auth_kind,
                        headers=headers,
                        options=request_options,
                        timeout_seconds=timeout_seconds,
                        max_retries=max_retries,
                        retry_status_codes=retry_status_codes,
                        retry_backoff_seconds=retry_backoff_seconds,
                        attempt_count=attempt_count,
                        success=True,
                        status_code=getattr(response, "status", None),
                    )
                    return parsed
            except urllib.error.HTTPError as exc:
                if attempt_count <= max_retries and exc.code in retry_status_codes:
                    self._sleep_before_retry(retry_backoff_seconds)
                    continue
                self._record_request_report(
                    method=method,
                    url=request_url,
                    auth_kind=auth_kind,
                    headers=headers,
                    options=request_options,
                    timeout_seconds=timeout_seconds,
                    max_retries=max_retries,
                    retry_status_codes=retry_status_codes,
                    retry_backoff_seconds=retry_backoff_seconds,
                    attempt_count=attempt_count,
                    success=False,
                    status_code=exc.code,
                )
                raise ConnectionError(
                    f"HTTP request failed for {request_url} with status {exc.code}"
                ) from exc
            except urllib.error.URLError as exc:
                if attempt_count <= max_retries:
                    self._sleep_before_retry(retry_backoff_seconds)
                    continue
                self._record_request_report(
                    method=method,
                    url=request_url,
                    auth_kind=auth_kind,
                    headers=headers,
                    options=request_options,
                    timeout_seconds=timeout_seconds,
                    max_retries=max_retries,
                    retry_status_codes=retry_status_codes,
                    retry_backoff_seconds=retry_backoff_seconds,
                    attempt_count=attempt_count,
                    success=False,
                    error=str(exc.reason or exc),
                )
                raise ConnectionError(f"HTTP request failed for {request_url}") from exc

    def _base_headers(
        self,
        options: Mapping[str, Any],
    ) -> dict[str, str]:
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }
        raw_headers = options.get("headers")
        if isinstance(raw_headers, Mapping):
            for key, value in raw_headers.items():
                header_name = str(key).strip()
                if not header_name or value is None:
                    continue
                headers[header_name] = str(value)
        return headers

    def _apply_auth_headers(
        self,
        headers: dict[str, str],
        *,
        options: Mapping[str, Any],
        method: str,
        request_url: str,
        data: bytes | None,
    ) -> str | None:
        auth_kind = None
        if headers.get("Authorization"):
            auth_kind = "explicit"

        if auth_kind is None:
            bearer_token = self._resolve_bearer_token(options)
            if bearer_token:
                headers["Authorization"] = f"Bearer {bearer_token}"
                auth_kind = "bearer"

        signature_secret = self._resolve_signature_secret(options)
        if signature_secret:
            auth_kind = self._apply_signature_headers(
                headers,
                options=options,
                signature_secret=signature_secret,
                method=method,
                request_url=request_url,
                data=data,
            )
        return auth_kind

    @staticmethod
    def _resolve_bearer_token(options: Mapping[str, Any]) -> str | None:
        return LocalHttpClientProvider._resolve_secret_value(
            options,
            direct_key="bearer_token",
            env_key="bearer_token_env",
            file_key="bearer_token_file",
        )

    @staticmethod
    def _resolve_signature_secret(options: Mapping[str, Any]) -> str | None:
        return LocalHttpClientProvider._resolve_secret_value(
            options,
            direct_key="signature_secret",
            env_key="signature_secret_env",
            file_key="signature_secret_file",
        )

    @staticmethod
    def _resolve_secret_value(
        options: Mapping[str, Any],
        *,
        direct_key: str,
        env_key: str,
        file_key: str,
    ) -> str | None:
        direct_value = str(options.get(direct_key) or "").strip()
        if direct_value:
            return direct_value
        env_name = str(options.get(env_key) or "").strip()
        if env_name:
            env_value = os.getenv(env_name, "").strip()
            if env_value:
                return env_value
        file_path = str(options.get(file_key) or "").strip()
        if not file_path:
            return None
        resolved_path = Path(file_path).expanduser().resolve()
        return resolved_path.read_text(encoding="utf-8").strip() or None

    @staticmethod
    def _apply_signature_headers(
        headers: dict[str, str],
        *,
        options: Mapping[str, Any],
        signature_secret: str,
        method: str,
        request_url: str,
        data: bytes | None,
    ) -> str:
        signature_algorithm = str(
            options.get("signature_algorithm") or "hmac-sha256"
        ).strip().lower()
        if signature_algorithm != "hmac-sha256":
            raise NotImplementedError(f"Unsupported signature algorithm: {signature_algorithm}")
        timestamp_header = str(
            options.get("signature_timestamp_header") or "X-Shanforge-Timestamp"
        ).strip()
        signature_header = str(
            options.get("signature_header") or "X-Shanforge-Signature"
        ).strip()
        key_id_header = str(
            options.get("signature_key_id_header") or "X-Shanforge-Key-Id"
        ).strip()
        timestamp_value = str(int(time.time()))
        string_to_sign = LocalHttpClientProvider._canonical_signature_string(
            method=method,
            request_url=request_url,
            data=data,
            timestamp_value=timestamp_value,
        )
        signature = hmac.new(
            signature_secret.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        headers[timestamp_header] = timestamp_value
        headers[signature_header] = f"sha256={signature}"
        key_id = str(options.get("signature_key_id") or "").strip()
        if key_id:
            headers[key_id_header] = key_id
        return "signature-hmac-sha256"

    @staticmethod
    def _canonical_signature_string(
        *,
        method: str,
        request_url: str,
        data: bytes | None,
        timestamp_value: str,
    ) -> str:
        parsed = urlparse(request_url)
        normalized_query = LocalHttpClientProvider._canonical_query_string(parsed.query)
        payload_digest = hashlib.sha256(data or b"").hexdigest()
        return "\n".join(
            (
                method.upper(),
                parsed.path or "/",
                normalized_query,
                payload_digest,
                timestamp_value,
            )
        )

    @staticmethod
    def _canonical_query_string(raw_query: str) -> str:
        if not raw_query:
            return ""
        pairs = parse_qsl(raw_query, keep_blank_values=True)
        pairs.sort(key=lambda item: (item[0], item[1]))
        return urlencode(pairs, doseq=True)

    def _timeout_seconds(self, options: Mapping[str, Any]) -> float:
        raw_value = options.get("timeout_seconds")
        if raw_value in {None, ""}:
            return self.timeout_seconds
        return float(raw_value)

    @staticmethod
    def _max_retries(options: Mapping[str, Any]) -> int:
        raw_value = options.get("max_retries")
        if raw_value in {None, ""}:
            return 0
        return max(0, int(raw_value))

    def _retry_status_codes(self, options: Mapping[str, Any]) -> tuple[int, ...]:
        raw_value = options.get("retry_status_codes")
        if isinstance(raw_value, (list, tuple, set)):
            return tuple(int(code) for code in raw_value)
        if raw_value in {None, ""}:
            return self.retry_status_codes
        return (int(raw_value),)

    def _retry_backoff_seconds(self, options: Mapping[str, Any]) -> float:
        raw_value = options.get("retry_backoff_seconds")
        if raw_value in {None, ""}:
            return self.retry_backoff_seconds
        return float(raw_value)

    @staticmethod
    def _sleep_before_retry(backoff_seconds: float) -> None:
        if backoff_seconds > 0:
            time.sleep(backoff_seconds)

    @staticmethod
    def _parse_response_body(raw_body: bytes, headers: Any) -> Mapping[str, Any]:
        charset = headers.get_content_charset() or "utf-8"
        text = raw_body.decode(charset) if raw_body else ""
        if not text:
            return {}
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return dict(parsed)
        return {"data": parsed}

    def _record_request_report(
        self,
        *,
        method: str,
        url: str,
        auth_kind: str | None,
        headers: Mapping[str, str],
        options: Mapping[str, Any],
        timeout_seconds: float,
        max_retries: int,
        retry_status_codes: tuple[int, ...],
        retry_backoff_seconds: float,
        attempt_count: int,
        success: bool,
        status_code: int | None = None,
        error: str | None = None,
    ) -> None:
        report: dict[str, Any] = {
            "method": method,
            "url": url,
            "request_header_names": tuple(sorted(headers)),
            "auth_kind": auth_kind,
            "timeout_seconds": timeout_seconds,
            "max_retries": max_retries,
            "retry_status_codes": tuple(retry_status_codes),
            "retry_backoff_seconds": retry_backoff_seconds,
            "attempt_count": attempt_count,
            "success": success,
        }
        if status_code is not None:
            report["status_code"] = status_code
        if error is not None:
            report["error"] = error
        signature_key_id = str(options.get("signature_key_id") or "").strip()
        if signature_key_id:
            report["signature_key_id"] = signature_key_id
        signature_key_selection_source = str(
            options.get("signature_key_selection_source") or ""
        ).strip()
        if signature_key_selection_source:
            report["signature_key_selection_source"] = signature_key_selection_source
        bearer_token_id = str(options.get("bearer_token_id") or "").strip()
        if bearer_token_id:
            report["bearer_token_id"] = bearer_token_id
        bearer_token_selection_source = str(
            options.get("bearer_token_selection_source") or ""
        ).strip()
        if bearer_token_selection_source:
            report["bearer_token_selection_source"] = bearer_token_selection_source
        secret_catalog_source_path = str(options.get("secret_catalog_source_path") or "").strip()
        if secret_catalog_source_path:
            report["secret_catalog_source_path"] = secret_catalog_source_path
        self._last_request_report = report
