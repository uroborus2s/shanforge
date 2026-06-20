from __future__ import annotations

import contextlib
import hashlib
import hmac
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from settings import SETTINGS_DOMAINS, SETTINGS_LAYER_NAME, list_settings_capabilities
from settings.catalog import list_settings_domains
from settings.gateway import LocalHttpClientProvider
from settings.memory import RemoteHttpMetadataResolver
from settings.model import NullEmbeddingProvider
from settings.session import EmptySearchIndexProvider, InMemoryBlobStore
from settings.workspace import LocalSecretCatalogProvider


class _HttpFixtureHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        response = {
            "recall_block": "Remote scaffold note.",
            "query_echo": query.get("query_text"),
        }
        body = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return None


@contextlib.contextmanager
def _serve_http_fixture() -> str:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _HttpFixtureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


class _RetryHttpFixtureHandler(BaseHTTPRequestHandler):
    get_attempts: int = 0
    last_headers: dict[str, str] = {}

    def do_GET(self) -> None:  # noqa: N802
        self.__class__.get_attempts += 1
        self.__class__.last_headers = {
            key: value for key, value in self.headers.items()
        }
        if self.__class__.get_attempts == 1:
            body = json.dumps({"error": "temporary-unavailable"}).encode("utf-8")
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps({"ok": True}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return None


@contextlib.contextmanager
def _serve_retry_http_fixture() -> str:
    _RetryHttpFixtureHandler.get_attempts = 0
    _RetryHttpFixtureHandler.last_headers = {}
    server = ThreadingHTTPServer(("127.0.0.1", 0), _RetryHttpFixtureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


class SettingsLayerScaffoldTests(unittest.TestCase):
    def test_settings_layer_catalog_lists_expected_domains(self) -> None:
        domains = list_settings_domains()

        self.assertEqual(SETTINGS_LAYER_NAME, "base_settings")
        self.assertEqual(domains, SETTINGS_DOMAINS)
        self.assertEqual(
            tuple(domain.domain_id for domain in domains),
            (
                "model",
                "memory",
                "session",
                "skills",
                "workspace",
                "approval",
                "delegation",
                "gateway",
                "capability_registry",
                "hermes",
                "composition",
                "shared",
            ),
        )

    def test_settings_layer_catalog_exposes_expected_capabilities(self) -> None:
        capability_ids = {capability.capability_id for capability in list_settings_capabilities()}

        self.assertIn("embedding_provider", capability_ids)
        self.assertIn("http_client", capability_ids)
        self.assertIn("blob_store", capability_ids)
        self.assertIn("memory_lifecycle_audit_store", capability_ids)
        self.assertIn("memory_lifecycle_queue_store", capability_ids)
        self.assertIn("search_index", capability_ids)
        self.assertIn("secret_catalog", capability_ids)
        self.assertIn("vector_index", capability_ids)
        self.assertIn("default_container", capability_ids)

    def test_remote_http_metadata_resolver_normalizes_canonical_and_legacy_keys(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            canonical_bearer = root / "canonical-bearer.txt"
            canonical_bearer.write_text("canonical-token", encoding="utf-8")
            legacy_bearer = root / "legacy-bearer.txt"
            legacy_bearer.write_text("legacy-token", encoding="utf-8")

            resolver = RemoteHttpMetadataResolver()
            canonical_options = resolver.resolve_request_options(
                metadata={
                    "sync_bearer_token_file": str(canonical_bearer),
                    "auth_bearer_token_file": str(legacy_bearer),
                    "retry_status_codes": [503],
                },
                request_kind="sync",
                secret_catalog_provider=LocalSecretCatalogProvider(),
            )
            self.assertEqual(
                canonical_options["bearer_token_file"],
                str(canonical_bearer),
            )
            self.assertEqual(canonical_options["retry_status_codes"], [503])

            legacy_options = resolver.resolve_request_options(
                metadata={"auth_bearer_token_file": str(legacy_bearer)},
                request_kind="sync",
                secret_catalog_provider=LocalSecretCatalogProvider(),
            )
            self.assertEqual(
                legacy_options["bearer_token_file"],
                str(legacy_bearer),
            )
            self.assertEqual(
                resolver.resolve_prefetch_response_validation_mode(
                    {"response_validation": "strict"}
                ),
                "raise",
            )
            self.assertEqual(
                resolver.resolve_prefetch_response_validation_mode(
                    {
                        "recall_response_validation": "record",
                        "prefetch_response_validation": "ignore",
                    }
                ),
                "record",
            )
            self.assertEqual(
                resolver.resolve_writeback_response_validation_mode(
                    {"writeback_response_validation": "record"},
                    request_kind="sync",
                ),
                "record",
            )
            self.assertEqual(
                resolver.resolve_writeback_response_validation_mode(
                    {
                        "sync_response_validation": "raise",
                        "writeback_response_validation": "ignore",
                    },
                    request_kind="sync",
                ),
                "raise",
            )
            self.assertEqual(
                resolver.resolve_writeback_failure_policy(
                    {"writeback_failure_policy": "record"},
                    request_kind="sync",
                ),
                "record",
            )
            self.assertEqual(
                resolver.resolve_writeback_failure_policy(
                    {
                        "sync_failure_policy": "record",
                        "writeback_failure_policy": "raise",
                    },
                    request_kind="sync",
                ),
                "record",
            )
            self.assertEqual(
                resolver.resolve_endpoint_url(
                    {
                        "recall_endpoint_url": "https://memory.example/recall-v2",
                        "endpoint_url": "https://memory.example/recall-v1",
                    },
                    request_kind="recall",
                    default="https://memory.example/default",
                ),
                "https://memory.example/recall-v2",
            )
            self.assertEqual(
                resolver.resolve_endpoint_url(
                    {"endpoint_url": "https://memory.example/recall-v1"},
                    request_kind="recall",
                    default=None,
                ),
                "https://memory.example/recall-v1",
            )
            self.assertEqual(
                resolver.resolve_prefetch_response_contract(
                    {
                        "recall_response_contract": "remote_memory_prefetch_v2",
                        "prefetch_response_contract": "remote_memory_prefetch_v1",
                    },
                    default_contract="remote_memory_prefetch_v1",
                ),
                ("remote_memory_prefetch_v2", "metadata:recall_response_contract"),
            )
            self.assertEqual(
                resolver.resolve_writeback_response_contract(
                    {
                        "sync_response_contract": "remote_memory_writeback_ack_v2",
                        "writeback_response_contract": "remote_memory_writeback_ack_v1",
                    },
                    request_kind="sync",
                    default_contract="remote_memory_writeback_ack_v1",
                ),
                ("remote_memory_writeback_ack_v2", "metadata:sync_response_contract"),
            )
            self.assertTrue(
                resolver.writeback_enabled(
                    {"session_end_endpoint_url": "https://memory.example/session-end"},
                    default_sync_endpoint_url=None,
                    default_session_end_endpoint_url=None,
                    default_lifecycle_apply_endpoint_url=None,
                    default_delegation_endpoint_url=None,
                )
            )
            prefetch_governance = resolver.resolve_prefetch_governance(
                {
                    "recall_endpoint_url": "https://memory.example/recall-v2",
                    "recall_response_contract": "remote_memory_prefetch_v2",
                    "recall_response_validation": "record",
                },
                default_endpoint_url=None,
                default_contract="remote_memory_prefetch_v1",
                secret_catalog_provider=LocalSecretCatalogProvider(),
            )
            self.assertEqual(prefetch_governance.endpoint_url, "https://memory.example/recall-v2")
            self.assertEqual(
                prefetch_governance.response_contract,
                "remote_memory_prefetch_v2",
            )
            self.assertEqual(prefetch_governance.response_validation_mode, "record")
            writeback_governance = resolver.resolve_writeback_governance(
                {
                    "sync_endpoint_url": "https://memory.example/sync-v2",
                    "sync_response_contract": "remote_memory_writeback_ack_v2",
                    "sync_response_validation": "record",
                    "sync_failure_policy": "ignore",
                },
                request_kind="sync",
                default_endpoint_url=None,
                default_contract="remote_memory_writeback_ack_v1",
                secret_catalog_provider=LocalSecretCatalogProvider(),
            )
            self.assertEqual(writeback_governance.endpoint_url, "https://memory.example/sync-v2")
            self.assertEqual(
                writeback_governance.response_contract,
                "remote_memory_writeback_ack_v2",
            )
            self.assertEqual(writeback_governance.response_validation_mode, "record")
            self.assertEqual(writeback_governance.failure_policy, "ignore")

    def test_settings_skeleton_modules_have_stable_behavior(self) -> None:
        with self.assertRaises(NotImplementedError):
            NullEmbeddingProvider().embed(("hello",))

        with self.assertRaises(NotImplementedError):
            LocalHttpClientProvider().request("TRACE", "https://example.com")

        with TemporaryDirectory() as temp_dir:
            payload_path = Path(temp_dir) / "remote-memory.json"
            payload_path.write_text(
                json.dumps({"recall_block": "Remote scaffold note."}),
                encoding="utf-8",
            )
            response = LocalHttpClientProvider().request("GET", payload_path.as_uri())
            self.assertEqual(response["recall_block"], "Remote scaffold note.")

        with _serve_http_fixture() as base_url:
            response = LocalHttpClientProvider().request(
                "GET",
                f"{base_url}/recall",
                payload={"query_text": "remote scaffold"},
            )
            self.assertEqual(response["query_echo"], "remote scaffold")

        with _serve_retry_http_fixture() as base_url:
            response = LocalHttpClientProvider().request(
                "GET",
                f"{base_url}/recall",
                options={
                    "headers": {"X-Trace-Id": "trace-001"},
                    "bearer_token": "fixture-token",
                    "max_retries": 1,
                    "retry_status_codes": (503,),
                    "timeout_seconds": 0.2,
                },
            )
            self.assertTrue(response["ok"])
            self.assertEqual(_RetryHttpFixtureHandler.get_attempts, 2)
            self.assertEqual(
                _RetryHttpFixtureHandler.last_headers["Authorization"],
                "Bearer fixture-token",
            )
            self.assertEqual(
                _RetryHttpFixtureHandler.last_headers["X-Trace-Id"],
                "trace-001",
            )

        with TemporaryDirectory() as temp_dir:
            secret_path = Path(temp_dir) / "remote-signature.txt"
            secret_path.write_text("fixture-secret", encoding="utf-8")
            with _serve_retry_http_fixture() as base_url:
                with patch("settings.gateway.http_client.time.time", return_value=1700000000):
                    response = LocalHttpClientProvider().request(
                        "GET",
                        f"{base_url}/recall?z=9",
                        payload={"query_text": "remote scaffold", "limit": 2},
                        options={
                            "headers": {"X-Trace-Id": "trace-002"},
                            "signature_secret_file": str(secret_path),
                            "signature_key_id": "fixture-key",
                            "max_retries": 1,
                            "retry_status_codes": (503,),
                        },
                    )
            self.assertTrue(response["ok"])
            canonical_string = "\n".join(
                (
                    "GET",
                    "/recall",
                    "limit=2&query_text=remote+scaffold&z=9",
                    hashlib.sha256(b"").hexdigest(),
                    "1700000000",
                )
            )
            expected_signature = hmac.new(
                b"fixture-secret",
                canonical_string.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest()
            self.assertEqual(
                _RetryHttpFixtureHandler.last_headers["X-Shanforge-Signature"],
                f"sha256={expected_signature}",
            )
            self.assertEqual(
                _RetryHttpFixtureHandler.last_headers["X-Shanforge-Key-Id"],
                "fixture-key",
            )
            self.assertIn(
                "X-Shanforge-Timestamp",
                _RetryHttpFixtureHandler.last_headers,
            )

        with TemporaryDirectory() as temp_dir:
            bindings_root = Path(temp_dir) / "bindings"
            bindings_root.mkdir(parents=True)
            secrets_root = Path(temp_dir) / "secrets"
            secrets_root.mkdir(parents=True)
            (secrets_root / "remote-signature-v1.txt").write_text(
                "fixture-secret-v1",
                encoding="utf-8",
            )
            (secrets_root / "remote-signature-v2.txt").write_text(
                "fixture-secret-v2",
                encoding="utf-8",
            )
            catalog_path = Path(temp_dir) / "secret-catalog.json"
            catalog_path.write_text(
                json.dumps(
                    {
                        "default_signature_key_id": "fixture-key-v2",
                        "signature_keys": {
                            "fixture-key-v1": {
                                "signature_secret_file": "secrets/remote-signature-v1.txt"
                            },
                            "fixture-key-v2": {
                                "signature_secret_file": "secrets/remote-signature-v2.txt"
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )
            metadata_source_path = bindings_root / "writer-remote.json"
            metadata_source_path.write_text("{}", encoding="utf-8")

            catalog_provider = LocalSecretCatalogProvider()
            catalog, source_path = catalog_provider.load_catalog(
                {
                    "secret_catalog_file": "../secret-catalog.json",
                    "metadata_source_path": str(metadata_source_path),
                }
            )
            selection = catalog_provider.resolve_secret_selection(
                secret_catalog=catalog,
                metadata={},
                secret_family="signature_keys",
                requested_id_key="recall_signature_key_id",
                fallback_id_key="signature_key_id",
                default_id_key="default_signature_key_id",
                source_path=source_path,
            )

            self.assertEqual(selection.secret_id, "fixture-key-v2")
            self.assertEqual(
                selection.selection_source,
                "catalog:default_signature_key_id",
            )
            self.assertEqual(
                selection.get("signature_secret_file"),
                str((secrets_root / "remote-signature-v2.txt").resolve()),
            )
            self.assertEqual(source_path, str(catalog_path.resolve()))
            metadata_selection = catalog_provider.resolve_secret_selection(
                secret_catalog={},
                metadata={"signature_key_id": "fixture-key-inline"},
                secret_family="signature_keys",
                requested_id_key="recall_signature_key_id",
                fallback_id_key="signature_key_id",
                default_id_key="default_signature_key_id",
                source_path=None,
            )
            self.assertEqual(metadata_selection.secret_id, "fixture-key-inline")
            self.assertEqual(
                metadata_selection.selection_source,
                "metadata:signature_key_id",
            )
            self.assertEqual(dict(metadata_selection.payload), {})

        search_provider = EmptySearchIndexProvider()
        self.assertEqual(search_provider.search("sessions", "hello"), ())

        blob_store = InMemoryBlobStore()
        blob_store.put_blob("artifacts", "artifact-1", b"payload")
        self.assertEqual(blob_store.get_blob("artifacts", "artifact-1"), b"payload")
        self.assertIsNone(blob_store.get_blob("artifacts", "missing"))


if __name__ == "__main__":
    unittest.main()
