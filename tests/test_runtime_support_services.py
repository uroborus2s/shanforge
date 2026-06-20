from __future__ import annotations

import unittest
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from runtime.capability.contracts import CapabilityInvocationContext
from runtime.clock_identity.service import ClockIdentityService
from runtime.profile_source.service import ProfileSourceService
from runtime.rule_source.service import RuleSourceService


@dataclass(slots=True, frozen=True)
class _ProfileProvider:
    payload: dict[str, object] | None = None

    def resolve_profile(self, lookup: dict[str, object]) -> dict[str, object] | None:
        del lookup
        return dict(self.payload) if self.payload is not None else None

    def list_profiles(self) -> tuple[dict[str, object], ...]:
        if self.payload is None:
            return ()
        return (dict(self.payload),)


@dataclass(slots=True, frozen=True)
class _RuleProvider:
    payload: dict[str, object]

    def load_rule_bundle(
        self,
        workspace_root: str | None,
        profile_id: str | None,
    ) -> dict[str, object]:
        return {
            **self.payload,
            "workspace_root": workspace_root,
            "profile_id": profile_id,
        }


@dataclass(slots=True, frozen=True)
class _ClockProvider:
    value: datetime

    def now(self) -> datetime:
        return self.value


@dataclass(slots=True, frozen=True)
class _IdProvider:
    value: str

    def new_id(self, prefix: str) -> str:
        return f"{prefix}-{self.value}"


class RuntimeSupportServiceTests(unittest.TestCase):
    def test_profile_source_service_resolves_and_lists_profiles_with_fallback(self) -> None:
        context = CapabilityInvocationContext(
            session_id="session-profile",
            profile_id="writer-profile",
            workspace_root="/tmp/project",
        )
        service = ProfileSourceService()

        resolved = service.resolve_profile(
            {"app_id": "demo.writer", "workflow_id": "compose"},
            context,
        )
        listed = service.list_profiles(context)

        self.assertEqual(resolved.profile_id, "writer-profile")
        self.assertEqual(resolved.label, "writer-profile")
        self.assertEqual(resolved.metadata["workspace_root"], "/tmp/project")
        self.assertEqual(resolved.metadata["app_id"], "demo.writer")
        self.assertEqual(listed[0].profile_id, "writer-profile")

    def test_profile_source_service_prefers_provider_payload(self) -> None:
        context = CapabilityInvocationContext(session_id="session-profile-provider")
        service = ProfileSourceService(
            profile_source=_ProfileProvider(
                {"profile_id": "local-dev", "label": "Local Dev", "tier": "default"}
            )
        )

        resolved = service.resolve_profile({}, context)
        listed = service.list_profiles(context)

        self.assertEqual(resolved.profile_id, "local-dev")
        self.assertEqual(resolved.label, "Local Dev")
        self.assertEqual(resolved.metadata["tier"], "default")
        self.assertEqual(listed[0].profile_id, "local-dev")

    def test_rule_source_service_loads_default_workspace_bundle(self) -> None:
        workspace_root = str(Path("/tmp/runtime-rule-workspace"))
        service = RuleSourceService()
        context = CapabilityInvocationContext(
            session_id="session-rule",
            workspace_root=workspace_root,
            profile_id="local-dev",
        )

        bundle = service.load_rule_bundle(workspace_root, "local-dev", context)

        self.assertEqual(bundle.workspace_root, workspace_root)
        self.assertEqual(bundle.profile_id, "local-dev")
        self.assertEqual(bundle.values["project_scope_key"], "runtime-rule-workspace")
        self.assertEqual(bundle.values["source"], "workspace-default")

    def test_rule_source_service_prefers_provider_payload(self) -> None:
        service = RuleSourceService(
            rule_source=_RuleProvider(
                {
                    "source": "workspace-config",
                    "project_scope_key": "shanforge",
                    "summary": "Workspace rules loaded from provider.",
                }
            )
        )
        context = CapabilityInvocationContext(session_id="session-rule-provider")

        bundle = service.load_rule_bundle("/tmp/project", "writer-profile", context)

        self.assertEqual(bundle.values["project_scope_key"], "shanforge")
        self.assertEqual(bundle.values["profile_id"], "writer-profile")
        self.assertEqual(bundle.values["source"], "workspace-config")

    def test_clock_identity_service_uses_fallbacks_and_providers(self) -> None:
        fallback_service = ClockIdentityService()
        now = fallback_service.now()
        generated = fallback_service.new_id("session")

        self.assertIsNotNone(now.tzinfo)
        self.assertTrue(generated.startswith("session-"))

        explicit_service = ClockIdentityService(
            clock_provider=_ClockProvider(datetime(2026, 4, 16, 12, 0)),
            id_provider=_IdProvider("001"),
        )
        explicit_now = explicit_service.now()

        self.assertEqual(explicit_now.isoformat(), "2026-04-16T12:00:00+00:00")
        self.assertEqual(explicit_service.new_id("session"), "session-001")


if __name__ == "__main__":
    unittest.main()
