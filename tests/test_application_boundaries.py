from __future__ import annotations

import unittest

from application import ports as application_ports
from application.app_compilation.service import AgentAppService
from application.workflow_resolution.service import WorkflowService


class ApplicationBoundaryTests(unittest.TestCase):
    def test_application_facades_require_explicit_domain_service_injection(self) -> None:
        with self.assertRaisesRegex(TypeError, "domain_service"):
            AgentAppService()

        with self.assertRaisesRegex(TypeError, "domain_service"):
            WorkflowService()

    def test_application_ports_exports_drop_legacy_owner_contracts(self) -> None:
        self.assertEqual(
            application_ports.__all__,
            ["AgentKernelPort", "MemoryAssemblyQueryPort"],
        )
        self.assertFalse(hasattr(application_ports, "ArtifactStorePort"))
        self.assertFalse(hasattr(application_ports, "MemorySystemPort"))
        self.assertFalse(hasattr(application_ports, "SessionStorePort"))


if __name__ == "__main__":
    unittest.main()
