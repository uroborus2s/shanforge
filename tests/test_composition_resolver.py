from __future__ import annotations

import unittest
from tempfile import TemporaryDirectory

from shanforge_di import UnknownComponentError

from settings.composition import build_component_container
from settings.hermes.bridge import HermesBridgeConfig

HERMES_REPO_ROOT = "/Users/uroborus/AiProject/hermes-agent"


class CompositionResolverTests(unittest.TestCase):
    def test_singleton_and_transient_lifecycle_behave_as_expected(self) -> None:
        container = build_component_container()

        first = container.resolve("llm_provider", "mock")
        second = container.resolve("llm_provider", "mock")
        self.assertIs(first, second)

        with TemporaryDirectory() as first_root, TemporaryDirectory() as second_root:
            one = container.resolve("memory_store", "jsonl", root=first_root)
            two = container.resolve("memory_store", "jsonl", root=second_root)

        self.assertIsNot(one, two)
        self.assertNotEqual(one.root, two.root)

    def test_resolves_runtime_local_components(self) -> None:
        container = build_component_container()

        self.assertEqual(
            container.resolve("capability_registry", "local").__class__.__name__,
            "InMemoryCapabilityRegistry",
        )
        self.assertEqual(
            container.resolve("approval_policy", "local").__class__.__name__,
            "ApprovalGate",
        )
        self.assertEqual(
            container.resolve("delegation_transport", "local").__class__.__name__,
            "DelegationCoordinator",
        )

    def test_resolves_hermes_adapters_with_runtime_overrides(self) -> None:
        container = build_component_container()
        bridge = HermesBridgeConfig.from_repo_root(HERMES_REPO_ROOT)
        capability_fallback = container.resolve("capability_registry", "local")
        approval_fallback = container.resolve("approval_policy", "local")
        delegation_fallback = container.resolve("delegation_transport", "local")

        self.assertEqual(
            container.resolve(
                "capability_registry",
                "hermes",
                fallback=capability_fallback,
                bridge=bridge,
            ).__class__.__name__,
            "HermesCapabilityRegistryAdapter",
        )
        self.assertEqual(
            container.resolve(
                "approval_policy",
                "hermes",
                fallback=approval_fallback,
                bridge=bridge,
            ).__class__.__name__,
            "HermesApprovalPolicyAdapter",
        )
        self.assertEqual(
            container.resolve(
                "delegation_transport",
                "hermes",
                fallback=delegation_fallback,
                bridge=bridge,
            ).__class__.__name__,
            "HermesDelegationTransportAdapter",
        )

    def test_rejects_unknown_component(self) -> None:
        container = build_component_container()

        with self.assertRaises(UnknownComponentError):
            container.resolve("missing_family")


if __name__ == "__main__":
    unittest.main()
