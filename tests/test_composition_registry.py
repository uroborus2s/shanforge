from __future__ import annotations

import unittest

from shanforge_di import ServiceContainer, UnknownComponentError

from settings.composition import build_component_container


class CompositionRegistryTests(unittest.TestCase):
    def test_builds_external_service_container_with_local_business_defaults(self) -> None:
        container = build_component_container()

        self.assertIsInstance(container, ServiceContainer)
        self.assertEqual(container.registry.get("llm_provider").name, "mock")
        self.assertEqual(container.registry.get("memory_store").name, "in_memory")
        self.assertEqual(
            container.registry.get("memory_lifecycle_queue_store").name,
            "in_memory",
        )
        self.assertEqual(
            container.registry.get("memory_lifecycle_audit_store").name,
            "in_memory",
        )

    def test_registers_expected_business_families(self) -> None:
        container = build_component_container()

        self.assertEqual(
            container.registry.names("llm_provider"),
            ("anthropic", "mock", "openai"),
        )
        self.assertEqual(
            container.registry.names("capability_registry"),
            ("hermes", "local"),
        )
        self.assertEqual(
            container.registry.names("memory_provider"),
            ("in_memory", "jsonl", "jsonl_vector", "none", "remote_http"),
        )
        self.assertEqual(
            container.registry.names("memory_lifecycle_queue_store"),
            ("in_memory", "jsonl"),
        )
        self.assertEqual(
            container.registry.names("memory_lifecycle_audit_store"),
            ("in_memory", "jsonl"),
        )
        self.assertEqual(
            container.registry.names("delegation_transport"),
            ("hermes", "local"),
        )
        self.assertEqual(container.registry.names("web_search"), ("local",))
        self.assertEqual(container.registry.names("web_document"), ("local",))
        self.assertEqual(container.registry.names("http_client"), ("local",))
        self.assertEqual(container.registry.names("shell_command"), ("local",))
        self.assertEqual(container.registry.names("git"), ("local",))
        self.assertEqual(container.registry.names("secret_catalog"), ("local",))
        self.assertEqual(container.registry.names("browser_automation"), ("local",))
        self.assertEqual(container.registry.names("embedding_provider"), ("null",))
        self.assertEqual(container.registry.names("blob_store"), ("in_memory",))
        self.assertEqual(container.registry.names("search_index"), ("empty",))
        self.assertEqual(container.registry.names("vector_index"), ("empty",))

    def test_rejects_unknown_family_or_choice(self) -> None:
        container = build_component_container()

        with self.assertRaises(UnknownComponentError):
            container.registry.get("missing_family")

        with self.assertRaises(UnknownComponentError):
            container.registry.get("approval_policy", "missing_choice")


if __name__ == "__main__":
    unittest.main()
