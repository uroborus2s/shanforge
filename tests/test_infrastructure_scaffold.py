from __future__ import annotations

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from access.cli.commands.run_demo import build_demo_manifest
from domain.gateway.models import GatewayResult
from settings.composition import Settings, build_default_container

HERMES_REPO_ROOT = "/Users/uroborus/AiProject/hermes-agent"


class InfrastructureScaffoldTests(unittest.TestCase):
    def test_settings_parse_hermes_scaffold_flags_from_env(self):
        with patch.dict(
            os.environ,
            {
                "SHANFORGE_HERMES_REPO_ROOT": HERMES_REPO_ROOT,
                "SHANFORGE_HERMES_ENABLED_ADAPTERS": "capability_registry,approval,delegation",
            },
            clear=False,
        ):
            settings = Settings.from_env()

        self.assertEqual(settings.hermes_repo_root, HERMES_REPO_ROOT)
        self.assertEqual(
            settings.hermes_enabled_adapters,
            ("capability_registry", "approval", "delegation"),
        )

    def test_hermes_bridge_config_resolves_expected_module_paths(self):
        from settings.hermes.bridge import HermesBridgeConfig

        bridge = HermesBridgeConfig.from_repo_root(HERMES_REPO_ROOT)

        self.assertEqual(bridge.repo_root, Path(HERMES_REPO_ROOT))
        self.assertTrue(bridge.has_module("tools/registry.py"))
        self.assertTrue(bridge.has_module("gateway/session_context.py"))
        self.assertEqual(bridge.module_path("tools/approval.py").name, "approval.py")

    def test_container_can_switch_to_hermes_backed_scaffolds(self):
        container = build_default_container(
            settings=Settings(
                hermes_repo_root=HERMES_REPO_ROOT,
                hermes_enabled_adapters=(
                    "capability_registry",
                    "approval",
                    "delegation",
                ),
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
            manifest=build_demo_manifest(),
            user_input="Create the first platform scaffold.",
        )

        self.assertEqual(result.session.status, "completed")
        self.assertIn("Mock response generated", result.response.summary)

    def test_in_memory_gateway_adapter_round_trips_payload(self):
        from settings.gateway.local_gateway import InMemoryGatewayAdapter

        gateway = InMemoryGatewayAdapter(channel="cli")
        inbound = gateway.bind(
            {
                "session_id": "session-001",
                "user_input": "Run the scaffold",
                "metadata": {"source": "test"},
            }
        )

        emitted = gateway.emit(
            GatewayResult(
                channel=inbound.context.channel,
                session_id=inbound.context.session_id,
                summary="Scaffold completed.",
                payload={"status": "ok"},
            )
        )

        self.assertEqual(inbound.context.channel, "cli")
        self.assertEqual(inbound.context.session_id, "session-001")
        self.assertEqual(emitted["session_id"], "session-001")
        self.assertEqual(emitted["payload"]["status"], "ok")


if __name__ == "__main__":
    unittest.main()
