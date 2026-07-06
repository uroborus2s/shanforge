from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from conftest import build_runtime_test_manifest

from settings.composition import Settings, build_default_container

HERMES_REPO_ROOT = "/Users/uroborus/AiProject/hermes-agent"


class CompositionContainerTests(unittest.TestCase):
    def test_container_switches_selected_implementations(self) -> None:
        with TemporaryDirectory() as temp_dir:
            container = build_default_container(
                settings=Settings(
                    default_provider="mock",
                    default_model="mock-chat",
                    memory_store_root=temp_dir,
                    hermes_repo_root=HERMES_REPO_ROOT,
                    hermes_enabled_adapters=(
                        "capability_registry",
                        "approval",
                        "delegation",
                    ),
                )
            )

            self.assertEqual(container.model_registry.default_policy.provider, "mock")
            self.assertEqual(
                container.runtime_api.service.kernel.execution_engine.llm_runtime.providers[
                    "mock"
                ].__class__.__name__,
                "MockLLMProvider",
            )
            self.assertEqual(container.memory_store.__class__.__name__, "JsonlMemoryStore")
            self.assertEqual(container.evidence_store.__class__.__name__, "JsonlEvidenceStore")
            self.assertEqual(
                container.memory_dataset_store.__class__.__name__,
                "JsonlMemoryDatasetStore",
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
            self.assertTrue(backend_bindings["capability_registry"].metadata["contract_ready"])
            self.assertEqual(
                tuple(backend_bindings["capability_registry"].metadata["bridge_modules"]),
                ("tools/registry.py", "model_tools.py"),
            )
            self.assertEqual(
                backend_bindings["approval_policy"].metadata["fallback_class"],
                "ApprovalGate",
            )
            self.assertEqual(
                backend_bindings["delegation_transport"].metadata["fallback_class"],
                "DelegationCoordinator",
            )


if __name__ == "__main__":
    unittest.main()
