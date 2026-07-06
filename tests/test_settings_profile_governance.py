from __future__ import annotations

import contextlib
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import parse_qs, urlparse

from conftest import build_runtime_test_manifest

from domain.memory.models import (
    MemoryKind,
    MemoryLifecycleQueueFilter,
    MemoryRecord,
    MemoryScope,
    MemoryStatus,
)
from settings.composition import Settings, build_default_container
from settings.workspace.source_provider import LocalProfileSourceProvider, LocalRuleSourceProvider


class _RemoteMemoryHandler(BaseHTTPRequestHandler):
    posts: list[tuple[str, dict[str, object]]] = []
    get_attempts: int = 0
    last_get_headers: dict[str, str] = {}
    last_post_headers: dict[str, dict[str, str]] = {}
    post_failure_statuses: dict[str, int] = {}
    post_payload_overrides: dict[str, dict[str, object]] = {}
    get_failure_count: int = 1
    get_payload_override: dict[str, object] | None = None

    def do_GET(self) -> None:  # noqa: N802
        self.__class__.get_attempts += 1
        self.__class__.last_get_headers = {
            key: value for key, value in self.headers.items()
        }
        if self.__class__.get_attempts <= self.__class__.get_failure_count:
            body = json.dumps({"error": "temporary-unavailable"}).encode("utf-8")
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        parsed = urlparse(self.path)
        query = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        response = self.__class__.get_payload_override or {
            "recall_block": "Remote memory service returned a scaffold note.",
            "hits": [
                {
                    "id": "remote-001",
                    "source_kind": "remote_snapshot",
                    "title": "Remote scaffold pattern",
                    "body": "Use the abstract platform scaffold for demo flows.",
                    "score": 0.92,
                }
            ],
            "query_echo": query.get("query_text"),
        }
        body = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length) if length else b"{}"
        payload = json.loads(raw_body.decode("utf-8"))
        self.__class__.posts.append((self.path, payload))
        self.__class__.last_post_headers[self.path] = {
            key: value for key, value in self.headers.items()
        }
        failure_status = self.__class__.post_failure_statuses.get(self.path)
        if failure_status is not None:
            body = json.dumps({"ok": False, "error": "writeback-failed"}).encode("utf-8")
            self.send_response(failure_status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        body = json.dumps(
            self.__class__.post_payload_overrides.get(self.path, {"ok": True})
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return None


@contextlib.contextmanager
def _serve_remote_memory_api(
    *,
    post_failure_statuses: dict[str, int] | None = None,
    post_payload_overrides: dict[str, dict[str, object]] | None = None,
    get_failure_count: int = 1,
    get_payload_override: dict[str, object] | None = None,
) -> str:
    _RemoteMemoryHandler.posts = []
    _RemoteMemoryHandler.get_attempts = 0
    _RemoteMemoryHandler.last_get_headers = {}
    _RemoteMemoryHandler.last_post_headers = {}
    _RemoteMemoryHandler.post_failure_statuses = dict(post_failure_statuses or {})
    _RemoteMemoryHandler.post_payload_overrides = dict(post_payload_overrides or {})
    _RemoteMemoryHandler.get_failure_count = get_failure_count
    _RemoteMemoryHandler.get_payload_override = (
        dict(get_payload_override) if get_payload_override is not None else None
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), _RemoteMemoryHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=2)
        server.server_close()


class SettingsProfileGovernanceTests(unittest.TestCase):
    def test_profile_source_provider_merges_provider_binding_catalog(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "label": "Writer Profile",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "provider-bindings.json").write_text(
                json.dumps(
                    {
                        "shared_provider_binding_metadata": {
                            "llm_provider": {"tier": "shared"}
                        },
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "provider_id": "anthropic",
                                "default_model": "anthropic-writer",
                                "provider_binding_metadata": {
                                    "llm_provider": {"policy_id": "creative-writing"}
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            profile_provider_path = (
                runtime_root / "profiles" / "writer" / "provider-bindings.json"
            )
            profile_provider_path.parent.mkdir(parents=True)
            profile_provider_path.write_text(
                json.dumps(
                    {
                        "default_model": "anthropic-writer-v2",
                        "provider_binding_metadata": {
                            "llm_provider": {"temperature_profile": "high"}
                        },
                    }
                ),
                encoding="utf-8",
            )

            provider = LocalProfileSourceProvider(
                default_profile_id="fallback",
                default_workspace_root=workspace_root,
            )

            resolved = provider.resolve_profile({"workspace_root": str(workspace_root)})

            assert resolved is not None
            self.assertEqual(resolved["provider_id"], "anthropic")
            self.assertEqual(resolved["default_model"], "anthropic-writer-v2")
            self.assertEqual(
                resolved["provider_binding_metadata"]["llm_provider"]["tier"],
                "shared",
            )
            self.assertEqual(
                resolved["provider_binding_metadata"]["llm_provider"]["policy_id"],
                "creative-writing",
            )
            self.assertEqual(
                resolved["provider_binding_metadata"]["llm_provider"]["temperature_profile"],
                "high",
            )
            self.assertEqual(
                resolved["provider_binding_metadata"]["llm_provider"]["binding_source"],
                "workspace-profile-provider-file",
            )

    def test_profile_source_provider_merges_backend_binding_catalog(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "label": "Writer Profile",
                                "default_model": "mock-writer",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "shared_backend_ids": {"web_search": "local"},
                        "shared_backend_binding_metadata": {
                            "web_search": {"policy_id": "shared-web"}
                        },
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_ids": {
                                    "approval_policy": "hermes",
                                    "capability_registry": "hermes",
                                },
                                "backend_binding_metadata": {
                                    "approval_policy": {"policy_id": "strict-approval"}
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            profile_backend_path = runtime_root / "profiles" / "writer" / "backend-bindings.json"
            profile_backend_path.parent.mkdir(parents=True)
            profile_backend_path.write_text(
                json.dumps(
                    {
                        "backend_ids": {"delegation_transport": "hermes"},
                        "backend_binding_metadata": {
                            "delegation_transport": {"policy_id": "parallel-delegation"}
                        },
                    }
                ),
                encoding="utf-8",
            )

            provider = LocalProfileSourceProvider(
                default_profile_id="fallback",
                default_workspace_root=workspace_root,
            )

            resolved = provider.resolve_profile({"workspace_root": str(workspace_root)})

            assert resolved is not None
            self.assertEqual(resolved["backend_ids"]["web_search"], "local")
            self.assertEqual(resolved["backend_ids"]["approval_policy"], "hermes")
            self.assertEqual(resolved["backend_ids"]["capability_registry"], "hermes")
            self.assertEqual(resolved["backend_ids"]["delegation_transport"], "hermes")
            self.assertEqual(
                resolved["backend_binding_metadata"]["web_search"]["policy_id"],
                "shared-web",
            )
            self.assertEqual(
                resolved["backend_binding_metadata"]["approval_policy"]["policy_id"],
                "strict-approval",
            )
            self.assertEqual(
                resolved["backend_binding_metadata"]["approval_policy"]["binding_source"],
                "workspace-backend-catalog",
            )
            self.assertEqual(
                resolved["backend_binding_metadata"]["delegation_transport"]["policy_id"],
                "parallel-delegation",
            )
            self.assertEqual(
                resolved["backend_binding_metadata"]["delegation_transport"]["binding_source"],
                "workspace-profile-backend-file",
            )

    def test_profile_source_provider_merges_backend_metadata_file(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            metadata_file = runtime_root / "bindings" / "writer-remote.json"
            metadata_file.parent.mkdir(parents=True)
            secret_file = runtime_root / "secrets" / "remote-signature.txt"
            secret_file.parent.mkdir(parents=True)
            secret_file.write_text("remote-secret", encoding="utf-8")
            metadata_file.write_text(
                json.dumps(
                    {
                        "endpoint_url": "https://memory.example/recall",
                        "sync_endpoint_url": "https://memory.example/sync",
                        "signature_secret_file": "../secrets/remote-signature.txt",
                        "writeback_failure_policy": "record",
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "label": "Writer Profile",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_ids": {
                                    "memory_provider": "remote_http",
                                },
                                "backend_binding_metadata": {
                                    "memory_provider": {
                                        "metadata_file": "bindings/writer-remote.json",
                                        "namespace": "writer-remote",
                                    }
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            provider = LocalProfileSourceProvider(
                default_profile_id="fallback",
                default_workspace_root=workspace_root,
            )

            resolved = provider.resolve_profile({"workspace_root": str(workspace_root)})

            assert resolved is not None
            self.assertEqual(resolved["backend_ids"]["memory_provider"], "remote_http")
            metadata = resolved["backend_binding_metadata"]["memory_provider"]
            self.assertEqual(metadata["endpoint_url"], "https://memory.example/recall")
            self.assertEqual(metadata["sync_endpoint_url"], "https://memory.example/sync")
            self.assertEqual(
                metadata["signature_secret_file"],
                str(secret_file.resolve()),
            )
            self.assertEqual(metadata["writeback_failure_policy"], "record")
            self.assertEqual(metadata["namespace"], "writer-remote")
            self.assertTrue(str(metadata["metadata_source_path"]).endswith("writer-remote.json"))

    def test_profile_source_provider_loads_workspace_profile_catalog(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            catalog_path = workspace_root / ".factory" / "runtime" / "profiles.json"
            catalog_path.parent.mkdir(parents=True)
            catalog_path.write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "shared_backend_ids": {"web_search": "local"},
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "label": "Writer Profile",
                                "default_model": "mock-writer",
                                "backend_ids": {"llm_provider": "mock"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            provider = LocalProfileSourceProvider(
                default_profile_id="fallback",
                default_workspace_root=workspace_root,
            )

            resolved = provider.resolve_profile({"workspace_root": str(workspace_root)})

            self.assertIsNotNone(resolved)
            assert resolved is not None
            self.assertEqual(resolved["profile_id"], "writer")
            self.assertEqual(resolved["label"], "Writer Profile")
            self.assertEqual(resolved["default_model"], "mock-writer")
            self.assertEqual(resolved["backend_ids"]["llm_provider"], "mock")
            self.assertEqual(resolved["backend_ids"]["web_search"], "local")

    def test_rule_source_provider_prefers_profile_rule_bundle(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            profile_rule_path = (
                workspace_root
                / ".factory"
                / "runtime"
                / "profiles"
                / "writer"
                / "rule-bundle.json"
            )
            profile_rule_path.parent.mkdir(parents=True)
            profile_rule_path.write_text(
                json.dumps(
                    {
                        "source": "workspace-profile",
                        "project_scope_key": "writer-scope",
                        "summary": "Writer profile rules.",
                    }
                ),
                encoding="utf-8",
            )
            provider = LocalRuleSourceProvider(default_workspace_root=workspace_root)

            payload = provider.load_rule_bundle(str(workspace_root), "writer")

            self.assertEqual(payload["source"], "workspace-profile")
            self.assertEqual(payload["project_scope_key"], "writer-scope")
            self.assertEqual(payload["profile_id"], "writer")

    def test_container_uses_profile_bindings_for_default_provider_and_store_root(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            catalog_path = workspace_root / ".factory" / "runtime" / "profiles.json"
            catalog_path.parent.mkdir(parents=True)
            catalog_path.write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "label": "Writer Profile",
                                "default_model": "mock-writer",
                                "backend_ids": {
                                    "llm_provider": "mock",
                                    "memory_store": "jsonl",
                                    "evidence_store": "jsonl",
                                    "memory_dataset_store": "jsonl",
                                },
                            }
                ],
                    }
                ),
                encoding="utf-8",
            )
            (workspace_root / ".factory" / "runtime" / "provider-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "provider_id": "mock",
                                "default_model": "mock-writer-provider",
                                "provider_binding_metadata": {
                                    "llm_provider": {"policy_id": "writer-policy"}
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                    default_provider="anthropic",
                    default_model="anthropic-default",
                )
            )

            self.assertEqual(container.model_registry.default_policy.provider, "mock")
            self.assertEqual(container.model_registry.default_policy.model, "mock-writer-provider")
            self.assertEqual(container.memory_store.__class__.__name__, "JsonlMemoryStore")
            self.assertIn(
                "/.factory/runtime/profiles/writer/stores",
                str(container.memory_store.root),
            )

            result = container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)

            self.assertEqual(manifest.profile_id, "writer")
            self.assertEqual(manifest.selected_model.provider_id, "mock")
            self.assertEqual(manifest.selected_model.model_id, "mock-writer-provider")
            self.assertEqual(
                manifest.selected_model.metadata["policy_id"],
                "writer-policy",
            )
            self.assertEqual(manifest.model_bindings[-1].step_id, "draft")
            self.assertEqual(
                {binding.family: binding.binding_id for binding in manifest.backend_bindings}[
                    "memory_store"
                ],
                "jsonl",
            )
            self.assertEqual(
                manifest.provider_bindings,
                ("llm_provider:mock",),
            )

    def test_container_uses_backend_binding_catalog_for_governance_adapters(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                                "backend_ids": {"llm_provider": "mock"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_ids": {
                                    "capability_registry": "hermes",
                                    "approval_policy": "hermes",
                                    "delegation_transport": "hermes",
                                },
                                "backend_binding_metadata": {
                                    "approval_policy": {"policy_id": "strict-approval"},
                                    "delegation_transport": {
                                        "transport_policy": "batch-delegation"
                                    },
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                    hermes_repo_root="/Users/uroborus/AiProject/hermes-agent",
                )
            )

            self.assertEqual(
                container.capability_registry.__class__.__name__,
                "HermesCapabilityRegistryAdapter",
            )
            self.assertEqual(
                container.approval_policy.__class__.__name__,
                "HermesApprovalPolicyAdapter",
            )
            self.assertEqual(
                container.delegation_transport.__class__.__name__,
                "HermesDelegationTransportAdapter",
            )

            result = container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)
            backend_bindings = {binding.family: binding for binding in manifest.backend_bindings}

            self.assertEqual(backend_bindings["capability_registry"].binding_id, "hermes")
            self.assertEqual(backend_bindings["approval_policy"].binding_id, "hermes")
            self.assertEqual(backend_bindings["delegation_transport"].binding_id, "hermes")
            self.assertEqual(
                backend_bindings["approval_policy"].metadata["policy_id"],
                "strict-approval",
            )
            self.assertEqual(
                backend_bindings["approval_policy"].metadata["binding_source"],
                "workspace-backend-catalog",
            )
            self.assertEqual(
                backend_bindings["delegation_transport"].metadata["transport_policy"],
                "batch-delegation",
            )

    def test_container_records_requested_backend_when_bridge_is_unavailable(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                                "backend_ids": {"llm_provider": "mock"},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_ids": {"capability_registry": "hermes"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                )
            )

            self.assertEqual(
                container.capability_registry.__class__.__name__,
                "InMemoryCapabilityRegistry",
            )

            result = container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)
            backend_bindings = {binding.family: binding for binding in manifest.backend_bindings}

            self.assertEqual(backend_bindings["capability_registry"].binding_id, "local")
            self.assertEqual(
                backend_bindings["capability_registry"].metadata["requested_binding_id"],
                "hermes",
            )
            self.assertEqual(
                backend_bindings["capability_registry"].metadata["binding_source"],
                "workspace-backend-catalog",
            )

    def test_container_records_requested_provider_when_provider_is_unavailable(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "provider-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "provider_id": "ghost-provider",
                                "default_model": "ghost-model",
                                "provider_binding_metadata": {
                                    "llm_provider": {"policy_id": "experimental"}
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                    default_provider="mock",
                    default_model="mock-chat",
                )
            )

            self.assertEqual(container.model_registry.default_policy.provider, "mock")
            self.assertEqual(container.model_registry.default_policy.model, "ghost-model")

            result = container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)
            backend_bindings = {binding.family: binding for binding in manifest.backend_bindings}

            self.assertEqual(backend_bindings["llm_provider"].binding_id, "mock")
            self.assertEqual(
                backend_bindings["llm_provider"].metadata["requested_binding_id"],
                "ghost-provider",
            )
            self.assertEqual(
                backend_bindings["llm_provider"].metadata["binding_source"],
                "workspace-provider-catalog",
            )
            assert manifest.selected_model is not None
            self.assertEqual(manifest.selected_model.provider_id, "mock")
            self.assertEqual(manifest.selected_model.model_id, "ghost-model")
            self.assertEqual(
                manifest.selected_model.metadata["requested_provider_id"],
                "ghost-provider",
            )

    def test_container_wires_external_memory_provider_binding_into_session_assembly(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                                "backend_ids": {
                                    "llm_provider": "mock",
                                    "memory_provider": "in_memory",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_binding_metadata": {
                                    "memory_provider": {
                                        "namespace": "writer-memory",
                                        "recall_block": "Remember the remote style guide.",
                                        "writable": False,
                                    }
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            container = build_default_container(
                settings=Settings(
                    workspace_root=str(workspace_root),
                    project_skills_root=str(workspace_root / "skills"),
                    default_provider="mock",
                    default_model="mock-chat",
                )
            )

            result = container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )
            manifest = container.memory_api.explain_session_assembly(result.session.id)
            backend_bindings = {binding.family: binding for binding in manifest.backend_bindings}

            self.assertIn("external_memory_recall_block", result.session.context)
            self.assertIn(
                "<external-memory>",
                result.session.context["external_memory_recall_block"],
            )
            assert manifest.memory_provider_binding is not None
            self.assertEqual(manifest.memory_provider_binding.provider_id, "in_memory")
            self.assertEqual(manifest.memory_provider_binding.namespace, "writer-memory")
            self.assertFalse(manifest.memory_provider_binding.writable)
            self.assertEqual(backend_bindings["memory_provider"].binding_id, "in_memory")
            self.assertEqual(
                backend_bindings["memory_provider"].metadata["binding_source"],
                "workspace-backend-catalog",
            )
            self.assertIn("memory_provider:in_memory", manifest.provider_bindings)

    def test_container_uses_jsonl_memory_provider_as_durable_external_backend(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                                "backend_ids": {
                                    "llm_provider": "mock",
                                    "memory_provider": "jsonl",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_binding_metadata": {
                                    "memory_provider": {
                                        "writable": True,
                                        "namespace": "writer-memory",
                                    }
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            settings = Settings(
                workspace_root=str(workspace_root),
                project_skills_root=str(workspace_root / "skills"),
                default_provider="mock",
                default_model="mock-chat",
            )

            first_container = build_default_container(settings=settings)
            self.assertEqual(
                first_container.memory_provider.__class__.__name__,
                "JsonlAugmentationMemoryProvider",
            )
            first_container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )

            second_container = build_default_container(settings=settings)
            second = second_container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Continue the scaffold with durable external memory.",
            )
            preview = second_container.memory_api.preview_recall(second.session.id, limit=2)

            self.assertIn("external_memory_recall_block", second.session.context)
            self.assertIn(
                "Workflow 'default' completion",
                second.session.context["external_memory_recall_block"],
            )
            self.assertNotIn(
                "legacy_aliases",
                preview.augmentation_preview.diagnostics,
            )
            self.assertEqual(
                preview.augmentation_preview.diagnostics["query_terms"],
                (
                    "continue",
                    "the",
                    "scaffold",
                    "with",
                    "durable",
                    "external",
                    "memory",
                ),
            )
            self.assertEqual(
                preview.augmentation_preview.diagnostics["source_breakdown"],
                {"snapshot": 1},
            )
            self.assertFalse(
                preview.augmentation_preview.diagnostics["result_truncated"]
            )
            budget_trace = preview.augmentation_preview.diagnostics["budget_trace"]
            self.assertEqual(
                budget_trace["selection_strategy"],
                "provider_window_confidence_recency",
            )
            self.assertEqual(budget_trace["candidate_hit_count"], 1)
            self.assertEqual(budget_trace["selected_hit_count"], 1)
            self.assertTrue(budget_trace["query_text_present"])
            self.assertEqual(
                len(budget_trace["selected_hit_ids"]),
                1,
            )
            self.assertEqual(budget_trace["rank_trace_count"], 1)
            self.assertFalse(budget_trace["rank_trace_truncated"])
            rank_trace = preview.augmentation_preview.diagnostics["rank_trace"]
            self.assertEqual(rank_trace[0]["source_kind"], "snapshot")
            self.assertTrue(rank_trace[0]["hit_id"])
            self.assertTrue(rank_trace[0]["selected"])
            self.assertEqual(rank_trace[0]["selection_reason"], "provider_window")
            hit_provenance = preview.augmentation_preview.diagnostics["hit_provenance"]
            self.assertEqual(hit_provenance[0]["source_kind"], "snapshot")
            self.assertEqual(hit_provenance[0]["origin_kind"], "provider_snapshot")
            self.assertTrue(hit_provenance[0]["session_id"])
            self.assertTrue(hit_provenance[0]["record_id"])
            contract_trace = preview.augmentation_preview.diagnostics["contract_trace"]
            self.assertEqual(contract_trace["bridge_kind"], "local")
            self.assertEqual(contract_trace["retrieval_kind"], "snapshot")
            self.assertEqual(contract_trace["storage_kind"], "jsonl")
            self.assertTrue(contract_trace["contract_ready"])
            access_trace = preview.augmentation_preview.diagnostics["access_trace"]
            self.assertEqual(access_trace["access_kind"], "state_root")
            self.assertEqual(access_trace["access_ref"], str(second_container.memory_provider.root))
            self.assertEqual(access_trace["attempt_count"], 1)
            self.assertEqual(access_trace["auth_kind"], "none")
            writeback_trace = preview.augmentation_preview.diagnostics["writeback_trace"]
            self.assertTrue(writeback_trace["supported"])
            self.assertTrue(writeback_trace["configured"])
            self.assertTrue(writeback_trace["session_writable"])
            self.assertTrue(writeback_trace["enabled"])
            self.assertNotIn("reports", writeback_trace)
            self.assertTrue(second_container.memory_provider.root.exists())

    def test_container_uses_jsonl_vector_memory_provider_for_ranked_external_hits(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            (runtime_root / "profiles.json").write_text(
                json.dumps(
                    {
                        "default_profile_id": "writer",
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "default_model": "mock-writer",
                                "backend_ids": {
                                    "llm_provider": "mock",
                                    "memory_provider": "jsonl_vector",
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (runtime_root / "backend-bindings.json").write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "profile_id": "writer",
                                "backend_binding_metadata": {
                                    "memory_provider": {
                                        "writable": True,
                                        "namespace": "writer-memory",
                                    }
                                },
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            settings = Settings(
                workspace_root=str(workspace_root),
                project_skills_root=str(workspace_root / "skills"),
                default_provider="mock",
                default_model="mock-chat",
            )

            first_container = build_default_container(settings=settings)
            self.assertEqual(
                first_container.memory_provider.__class__.__name__,
                "JsonlVectorAugmentationMemoryProvider",
            )
            first_container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Create the first platform scaffold.",
            )

            second_container = build_default_container(settings=settings)
            second = second_container.runtime_api.run_manifest(
                manifest=build_runtime_test_manifest(),
                user_input="Continue the platform scaffold with vector external memory.",
            )
            preview = second_container.memory_api.preview_recall(second.session.id, limit=2)

            self.assertIn("external_memory_recall_block", second.session.context)
            self.assertIn(
                "Vector augmentation hits:",
                second.session.context["external_memory_recall_block"],
            )
            self.assertNotIn(
                "legacy_aliases",
                preview.augmentation_preview.diagnostics,
            )
            self.assertEqual(
                preview.augmentation_preview.diagnostics["query_terms"],
                (
                    "continue",
                    "the",
                    "platform",
                    "scaffold",
                    "with",
                    "vector",
                    "external",
                    "memory",
                ),
            )
            self.assertEqual(
                preview.augmentation_preview.diagnostics["source_breakdown"],
                {"snapshot": 1, "turn": 1},
            )
            self.assertFalse(
                preview.augmentation_preview.diagnostics["result_truncated"]
            )
            budget_trace = preview.augmentation_preview.diagnostics["budget_trace"]
            self.assertEqual(
                budget_trace["selection_strategy"],
                "provider_window_query_overlap",
            )
            self.assertEqual(budget_trace["candidate_hit_count"], 2)
            self.assertEqual(budget_trace["selected_hit_count"], 2)
            self.assertTrue(budget_trace["query_text_present"])
            self.assertEqual(len(budget_trace["selected_hit_ids"]), 2)
            self.assertEqual(budget_trace["rank_trace_count"], 2)
            self.assertFalse(budget_trace["rank_trace_truncated"])
            rank_trace = preview.augmentation_preview.diagnostics["rank_trace"]
            self.assertEqual(rank_trace[0]["source_kind"], "snapshot")
            self.assertTrue(rank_trace[0]["selected"])
            self.assertEqual(rank_trace[1]["source_kind"], "turn")
            self.assertTrue(rank_trace[1]["selected"])
            hit_provenance = preview.augmentation_preview.diagnostics["hit_provenance"]
            self.assertEqual(hit_provenance[0]["origin_kind"], "provider_snapshot")
            self.assertEqual(hit_provenance[1]["origin_kind"], "provider_turn")
            self.assertTrue(hit_provenance[1]["session_id"])
            self.assertTrue(hit_provenance[1]["event_ids"])
            contract_trace = preview.augmentation_preview.diagnostics["contract_trace"]
            self.assertEqual(contract_trace["bridge_kind"], "local")
            self.assertEqual(contract_trace["retrieval_kind"], "vector")
            self.assertEqual(contract_trace["storage_kind"], "jsonl")
            self.assertTrue(contract_trace["contract_ready"])
            access_trace = preview.augmentation_preview.diagnostics["access_trace"]
            self.assertEqual(access_trace["access_kind"], "state_root")
            self.assertEqual(access_trace["access_ref"], str(second_container.memory_provider.root))
            self.assertEqual(access_trace["attempt_count"], 1)
            self.assertEqual(access_trace["auth_kind"], "none")
            writeback_trace = preview.augmentation_preview.diagnostics["writeback_trace"]
            self.assertTrue(writeback_trace["supported"])
            self.assertTrue(writeback_trace["configured"])
            self.assertTrue(writeback_trace["session_writable"])
            self.assertTrue(writeback_trace["enabled"])
            self.assertNotIn("reports", writeback_trace)
            self.assertTrue(second_container.memory_provider.root.exists())

    def test_container_uses_remote_http_memory_provider_bridge(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                post_failure_statuses={"/session-end": 500}
            ) as base_url:
                recall_url = f"{base_url}/recall"
                sync_url = f"{base_url}/sync"
                session_end_url = f"{base_url}/session-end"
                metadata_file = runtime_root / "bindings" / "writer-remote.json"
                metadata_file.parent.mkdir(parents=True)
                secret_file = runtime_root / "secrets" / "remote-signature.txt"
                secret_file.parent.mkdir(parents=True)
                secret_file.write_text("remote-secret", encoding="utf-8")
                metadata_file.write_text(
                    json.dumps(
                        {
                            "endpoint_url": recall_url,
                            "sync_endpoint_url": sync_url,
                            "session_end_endpoint_url": session_end_url,
                            "request_headers": {"X-Profile-Id": "writer"},
                            "signature_secret_file": "../secrets/remote-signature.txt",
                            "signature_key_id": "writer-key",
                            "timeout_seconds": 0.25,
                            "max_retries": 1,
                            "retry_status_codes": [503],
                            "session_end_failure_policy": "record",
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                    "memory_provider": {
                                        "metadata_file": "bindings/writer-remote.json",
                                        "namespace": "writer-remote",
                                        "writable": True,
                                    }
                                },
                            }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )
                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )

                self.assertEqual(
                    container.memory_provider.__class__.__name__,
                    "RemoteAugmentationMemoryProvider",
                )

                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with remote memory.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertIn(
                    "Remote augmentation hits:",
                    result.session.context["external_memory_recall_block"],
                )
                self.assertIn(
                    "Remote scaffold pattern",
                    result.session.context["external_memory_recall_block"],
                )
                self.assertNotIn(
                    "legacy_aliases",
                    preview.augmentation_preview.diagnostics,
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["query_terms"],
                    (
                        "continue",
                        "the",
                        "platform",
                        "scaffold",
                        "with",
                        "remote",
                        "memory",
                    ),
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["source_breakdown"],
                    {"remote_snapshot": 1},
                )
                self.assertFalse(
                    preview.augmentation_preview.diagnostics["result_truncated"]
                )
                budget_trace = preview.augmentation_preview.diagnostics["budget_trace"]
                self.assertEqual(
                    budget_trace["selection_strategy"],
                    "remote_response_order",
                )
                self.assertEqual(budget_trace["candidate_hit_count"], 1)
                self.assertEqual(budget_trace["selected_hit_count"], 1)
                self.assertTrue(budget_trace["query_text_present"])
                self.assertEqual(
                    budget_trace["selected_hit_ids"],
                    ("remote-001",),
                )
                self.assertEqual(budget_trace["rank_trace_count"], 1)
                self.assertFalse(budget_trace["rank_trace_truncated"])
                rank_trace = preview.augmentation_preview.diagnostics["rank_trace"]
                self.assertEqual(rank_trace[0]["hit_id"], "remote-001")
                self.assertEqual(rank_trace[0]["source_kind"], "remote_snapshot")
                self.assertTrue(rank_trace[0]["selected"])
                self.assertEqual(
                    rank_trace[0]["selection_reason"],
                    "remote_response_order",
                )
                hit_provenance = preview.augmentation_preview.diagnostics["hit_provenance"]
                self.assertEqual(hit_provenance[0]["hit_id"], "remote-001")
                self.assertEqual(hit_provenance[0]["origin_kind"], "remote_response")
                self.assertEqual(hit_provenance[0]["response_position"], 0)
                contract_trace = preview.augmentation_preview.diagnostics["contract_trace"]
                self.assertEqual(contract_trace["bridge_kind"], "remote")
                self.assertEqual(contract_trace["retrieval_kind"], "remote_http")
                self.assertTrue(contract_trace["contract_ready"])
                self.assertEqual(
                    contract_trace["response_contract"],
                    "remote_memory_prefetch_v1",
                )
                self.assertEqual(
                    contract_trace["response_contract_source"],
                    "built-in",
                )
                self.assertEqual(
                    contract_trace["response_keys"],
                    ("hits", "query_echo", "recall_block"),
                )
                access_trace = preview.augmentation_preview.diagnostics["access_trace"]
                self.assertEqual(access_trace["access_kind"], "endpoint_url")
                self.assertEqual(access_trace["access_ref"], recall_url)
                self.assertEqual(access_trace["attempt_count"], 2)
                self.assertEqual(access_trace["auth_kind"], "signature-hmac-sha256")
                self.assertEqual(access_trace["signature_key_id"], "writer-key")
                self.assertEqual(
                    access_trace["signature_key_selection_source"],
                    "metadata:signature_key_id",
                )
                self.assertEqual(access_trace["timeout_seconds"], 0.25)
                self.assertEqual(access_trace["max_retries"], 1)
                self.assertEqual(access_trace["retry_status_codes"], (503,))
                self.assertEqual(access_trace["retry_backoff_seconds"], 0.0)
                writeback_trace = preview.augmentation_preview.diagnostics["writeback_trace"]
                self.assertTrue(writeback_trace["supported"])
                self.assertTrue(writeback_trace["configured"])
                self.assertTrue(writeback_trace["session_writable"])
                self.assertTrue(writeback_trace["enabled"])
                self.assertNotIn("reports", writeback_trace)
                self.assertIn("sync", writeback_trace["detail_reports"])
                self.assertIn("session_end", writeback_trace["detail_reports"])
                self.assertEqual(
                    writeback_trace["failure_policies"],
                    {
                        "sync": "raise",
                        "session_end": "record",
                    },
                )
                self.assertEqual(
                    _RemoteMemoryHandler.last_get_headers["X-Shanforge-Key-Id"],
                    "writer-key",
                )
                self.assertEqual(
                    _RemoteMemoryHandler.last_get_headers["X-Profile-Id"],
                    "writer",
                )
                self.assertIn(
                    "X-Shanforge-Signature",
                    _RemoteMemoryHandler.last_get_headers,
                )
                self.assertIn(
                    "X-Shanforge-Timestamp",
                    _RemoteMemoryHandler.last_get_headers,
                )
                writeback_reports = writeback_trace["detail_reports"]
                self.assertEqual(writeback_reports["sync"]["path"], "/sync")
                self.assertEqual(writeback_reports["sync"]["request_kind"], "sync")
                self.assertEqual(
                    writeback_reports["sync"]["response_contract"],
                    "remote_memory_writeback_ack_v1",
                )
                self.assertEqual(
                    writeback_reports["session_end"]["path"],
                    "/session-end",
                )
                self.assertFalse(writeback_reports["session_end"]["success"])
                self.assertEqual(writeback_reports["session_end"]["status_code"], 500)
                self.assertEqual(
                    writeback_reports["session_end"]["failure_policy"],
                    "record",
                )
                posted_paths = [path for path, _ in _RemoteMemoryHandler.posts]
                self.assertIn("/sync", posted_paths)
                self.assertIn("/session-end", posted_paths)

    def test_container_supports_canonical_remote_http_endpoint_and_contract_keys(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(get_failure_count=0) as base_url:
                recall_url = f"{base_url}/recall"
                sync_url = f"{base_url}/sync"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "recall_endpoint_url": recall_url,
                                            "endpoint_url": "https://memory.example/legacy-recall",
                                            "sync_endpoint_url": sync_url,
                                            "recall_response_contract": (
                                                "remote_memory_prefetch_v2"
                                            ),
                                            "prefetch_response_contract": (
                                                "remote_memory_prefetch_v1"
                                            ),
                                            "sync_response_contract": (
                                                "remote_memory_writeback_ack_v2"
                                            ),
                                            "writeback_response_contract": (
                                                "remote_memory_writeback_ack_v1"
                                            ),
                                            "namespace": "writer-remote",
                                            "writable": True,
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with canonical remote keys.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertNotIn(
                    "legacy_aliases",
                    preview.augmentation_preview.diagnostics,
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"]["access_ref"],
                    recall_url,
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["contract_trace"][
                        "response_contract"
                    ],
                    "remote_memory_prefetch_v2",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["contract_trace"][
                        "response_contract_source"
                    ],
                    "metadata:recall_response_contract",
                )
                sync_report = preview.augmentation_preview.diagnostics["writeback_trace"][
                    "detail_reports"
                ]["sync"]
                self.assertEqual(
                    sync_report["response_contract"],
                    "remote_memory_writeback_ack_v2",
                )
                self.assertEqual(
                    sync_report["response_contract_source"],
                    "metadata:sync_response_contract",
                )

    def test_container_prefers_canonical_remote_http_recall_response_validation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                get_payload_override={
                    "recall_block": "Remote memory validation note.",
                    "hits": "invalid",
                },
            ) as base_url:
                recall_url = f"{base_url}/recall"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "recall_response_validation": "record",
                                            "prefetch_response_validation": "ignore",
                                            "namespace": "writer-remote",
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with canonical validation.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertEqual(
                    preview.augmentation_preview.diagnostics["contract_trace"][
                        "response_validation_error"
                    ],
                    "hits must be a list of objects",
                )

    def test_container_prefers_canonical_remote_http_sync_failure_policy(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                post_failure_statuses={"/sync": 500},
            ) as base_url:
                recall_url = f"{base_url}/recall"
                sync_url = f"{base_url}/sync"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "sync_endpoint_url": sync_url,
                                            "sync_failure_policy": "record",
                                            "writeback_failure_policy": "raise",
                                            "namespace": "writer-remote",
                                            "writable": True,
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with canonical failure policy.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                sync_report = preview.augmentation_preview.diagnostics["writeback_trace"][
                    "detail_reports"
                ]["sync"]
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["writeback_trace"][
                        "failure_policies"
                    ]["sync"],
                    "record",
                )
                self.assertEqual(sync_report["failure_policy"], "record")
                self.assertFalse(sync_report["success"])
                self.assertEqual(sync_report["status_code"], 500)

    def test_container_records_remote_http_prefetch_response_validation_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                get_payload_override={
                    "recall_block": "Remote memory validation note.",
                    "hits": "invalid",
                },
            ) as base_url:
                recall_url = f"{base_url}/recall"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "namespace": "writer-remote",
                                            "prefetch_response_validation": "record",
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )

                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with remote validation.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertIn(
                    "Remote memory validation note.",
                    result.session.context["external_memory_recall_block"],
                )
                self.assertNotIn(
                    "Remote augmentation hits:",
                    result.session.context["external_memory_recall_block"],
                )
                self.assertIn(
                    "response_validation_error",
                    preview.augmentation_preview.diagnostics["contract_trace"],
                )

    def test_container_uses_remote_http_secret_catalog_key_rotation(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(get_failure_count=0) as base_url:
                recall_url = f"{base_url}/recall"
                metadata_file = runtime_root / "bindings" / "writer-remote.json"
                metadata_file.parent.mkdir(parents=True)
                secrets_root = runtime_root / "secrets"
                secrets_root.mkdir(parents=True)
                (secrets_root / "remote-signature-v1.txt").write_text(
                    "remote-secret-v1",
                    encoding="utf-8",
                )
                (secrets_root / "remote-signature-v2.txt").write_text(
                    "remote-secret-v2",
                    encoding="utf-8",
                )
                (secrets_root / "remote-bearer.txt").write_text(
                    "remote-bearer-token",
                    encoding="utf-8",
                )
                secret_catalog = secrets_root / "remote-secrets.json"
                secret_catalog.write_text(
                    json.dumps(
                        {
                            "default_signature_key_id": "writer-key-v2",
                            "signature_keys": {
                                "writer-key-v1": {
                                    "signature_secret_file": "remote-signature-v1.txt"
                                },
                                "writer-key-v2": {
                                    "signature_secret_file": "remote-signature-v2.txt"
                                },
                            },
                            "default_bearer_token_id": "remote-api",
                            "bearer_tokens": {
                                "remote-api": {
                                    "bearer_token_file": "remote-bearer.txt"
                                }
                            },
                        }
                    ),
                    encoding="utf-8",
                )
                metadata_file.write_text(
                    json.dumps(
                        {
                            "endpoint_url": recall_url,
                            "secret_catalog_file": "../secrets/remote-secrets.json",
                            "request_headers": {"X-Profile-Id": "writer"},
                            "timeout_seconds": 0.25,
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "metadata_file": "bindings/writer-remote.json",
                                            "namespace": "writer-remote",
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with rotated remote secrets.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertEqual(
                    _RemoteMemoryHandler.last_get_headers["X-Shanforge-Key-Id"],
                    "writer-key-v2",
                )
                self.assertEqual(
                    _RemoteMemoryHandler.last_get_headers["Authorization"],
                    "Bearer remote-bearer-token",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"][
                        "signature_key_id"
                    ],
                    "writer-key-v2",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"][
                        "signature_key_selection_source"
                    ],
                    "catalog:default_signature_key_id",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"][
                        "bearer_token_id"
                    ],
                    "remote-api",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"][
                        "bearer_token_selection_source"
                    ],
                    "catalog:default_bearer_token_id",
                )
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["access_trace"][
                        "secret_catalog_source_path"
                    ],
                    str(secret_catalog.resolve()),
                )

    def test_container_records_remote_http_writeback_success_read_model(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                post_payload_overrides={
                    "/sync": {
                        "ok": True,
                        "status": "accepted",
                        "report_id": "sync-001",
                        "message": "queued",
                    }
                },
            ) as base_url:
                recall_url = f"{base_url}/recall"
                sync_url = f"{base_url}/sync"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "sync_endpoint_url": sync_url,
                                            "namespace": "writer-remote",
                                            "writable": True,
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with writeback success.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                writeback_trace = preview.augmentation_preview.diagnostics[
                    "writeback_trace"
                ]
                self.assertNotIn("reports", writeback_trace)
                sync_report = writeback_trace["detail_reports"]["sync"]
                self.assertTrue(sync_report["success"])
                self.assertTrue(sync_report["response_ok"])
                self.assertEqual(sync_report["response_status"], "accepted")
                self.assertEqual(sync_report["response_report_id"], "sync-001")
                self.assertEqual(sync_report["response_message"], "queued")
                self.assertEqual(writeback_trace["successes"], {"sync": True})
                self.assertEqual(writeback_trace["response_oks"], {"sync": True})
                self.assertEqual(
                    writeback_trace["response_statuses"],
                    {"sync": "accepted"},
                )
                self.assertEqual(
                    writeback_trace["response_report_ids"],
                    {"sync": "sync-001"},
                )
                self.assertEqual(
                    writeback_trace["response_messages"],
                    {"sync": "queued"},
                )
                self.assertEqual(
                    sync_report["response_contract"],
                    "remote_memory_writeback_ack_v1",
                )
                self.assertEqual(
                    sync_report["response_contract_source"],
                    "built-in",
                )
                self.assertEqual(
                    sync_report["response_keys"],
                    ("message", "ok", "report_id", "status"),
                )

    def test_container_records_remote_http_lifecycle_apply_writeback(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                post_payload_overrides={
                    "/lifecycle-apply": {
                        "ok": True,
                        "status": "accepted",
                        "report_id": "lifecycle-001",
                        "message": "applied",
                    }
                },
            ) as base_url:
                recall_url = f"{base_url}/recall"
                lifecycle_apply_url = f"{base_url}/lifecycle-apply"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "lifecycle_apply_endpoint_url": lifecycle_apply_url,
                                            "namespace": "writer-remote",
                                            "writable": True,
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Apply lifecycle writeback to remote provider.",
                )
                container.memory_store.save_memory_record(
                    MemoryRecord(
                        id="memory-decayed",
                        kind=MemoryKind.EPISODIC,
                        scope=MemoryScope.APP,
                        scope_key=result.session.app_id,
                        title="Stale episodic note",
                        body="This note should decay.",
                        status=MemoryStatus.ACCEPTED,
                        confidence=0.68,
                        supporting_refs=("event://2",),
                        metadata={
                            "decay_after_days": 30,
                            "last_reinforced_at": "2026-01-05T00:00:00+00:00",
                        },
                    )
                )

                apply_result = container.memory_api.apply_lifecycle(
                    result.session.id,
                    actor="memory-reviewer",
                    queue_filter=MemoryLifecycleQueueFilter(
                        effective_statuses=(MemoryStatus.FORGOTTEN,),
                    ),
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                self.assertEqual(apply_result.applied_record_ids, ("memory-decayed",))
                self.assertTrue(apply_result.metadata["provider_writeback_triggered"])
                writeback_trace = preview.augmentation_preview.diagnostics[
                    "writeback_trace"
                ]
                lifecycle_report = writeback_trace["detail_reports"]["lifecycle_apply"]
                self.assertTrue(lifecycle_report["success"])
                self.assertTrue(lifecycle_report["response_ok"])
                self.assertEqual(lifecycle_report["response_status"], "accepted")
                self.assertEqual(
                    lifecycle_report["response_report_id"],
                    "lifecycle-001",
                )
                self.assertEqual(lifecycle_report["response_message"], "applied")
                self.assertEqual(lifecycle_report["path"], "/lifecycle-apply")
                self.assertEqual(lifecycle_report["request_kind"], "lifecycle_apply")

    def test_container_records_remote_http_writeback_response_validation_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            workspace_root = Path(temp_dir)
            (workspace_root / "skills").mkdir(parents=True)
            runtime_root = workspace_root / ".factory" / "runtime"
            runtime_root.mkdir(parents=True)
            with _serve_remote_memory_api(
                get_failure_count=0,
                post_payload_overrides={"/sync": {"ok": "invalid"}},
            ) as base_url:
                recall_url = f"{base_url}/recall"
                sync_url = f"{base_url}/sync"
                (runtime_root / "profiles.json").write_text(
                    json.dumps(
                        {
                            "default_profile_id": "writer",
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "default_model": "mock-writer",
                                    "backend_ids": {
                                        "llm_provider": "mock",
                                        "memory_provider": "remote_http",
                                    },
                                }
                            ],
                        }
                    ),
                    encoding="utf-8",
                )
                (runtime_root / "backend-bindings.json").write_text(
                    json.dumps(
                        {
                            "profiles": [
                                {
                                    "profile_id": "writer",
                                    "backend_binding_metadata": {
                                        "memory_provider": {
                                            "endpoint_url": recall_url,
                                            "sync_endpoint_url": sync_url,
                                            "namespace": "writer-remote",
                                            "writable": True,
                                            "sync_response_validation": "record",
                                        }
                                    },
                                }
                            ]
                        }
                    ),
                    encoding="utf-8",
                )

                container = build_default_container(
                    settings=Settings(
                        workspace_root=str(workspace_root),
                        project_skills_root=str(workspace_root / "skills"),
                        default_provider="mock",
                        default_model="mock-chat",
                    )
                )
                result = container.runtime_api.run_manifest(
                    manifest=build_runtime_test_manifest(),
                    user_input="Continue the platform scaffold with writeback validation.",
                )
                preview = container.memory_api.preview_recall(result.session.id, limit=2)

                writeback_reports = preview.augmentation_preview.diagnostics[
                    "writeback_trace"
                ]["detail_reports"]
                self.assertEqual(
                    preview.augmentation_preview.diagnostics["writeback_trace"][
                        "response_validation_errors"
                    ]["sync"],
                    "writeback response ok must be true",
                )
                self.assertFalse(writeback_reports["sync"]["success"])
                self.assertEqual(
                    writeback_reports["sync"]["response_validation_error"],
                    "writeback response ok must be true",
                )


if __name__ == "__main__":
    unittest.main()
