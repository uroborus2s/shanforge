from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from runtime.browser.models import BrowserActionReceipt, BrowserObservation, BrowserSessionHandle
from runtime.capability.contracts import (
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.execution_backends import BrowserAutomationProviderPort


@dataclass(slots=True)
class BrowserService:
    """Self-owned scaffold for browser automation capabilities."""

    browser_provider: BrowserAutomationProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="browser",
            name="Browser",
            summary=(
                "Opens browser sessions, inspects DOM state, performs actions, "
                "and captures screenshots."
            ),
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="browser.open_page",
                    method_name="open_page",
                    summary="Open one browser page.",
                    risk_level="L1",
                ),
                CapabilityOperationDescriptor(
                    operation_id="browser.inspect_dom",
                    method_name="inspect_dom",
                    summary="Inspect DOM state for one browser session.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="browser.click",
                    method_name="click",
                    summary="Perform one click action.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="browser.type_text",
                    method_name="type_text",
                    summary="Type text into one browser target.",
                    risk_level="L2",
                    writes_data=True,
                ),
                CapabilityOperationDescriptor(
                    operation_id="browser.wait_for",
                    method_name="wait_for",
                    summary="Wait for one browser condition.",
                    risk_level="L1",
                ),
                CapabilityOperationDescriptor(
                    operation_id="browser.capture_screenshot",
                    method_name="capture_screenshot",
                    summary="Capture one screenshot artifact.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("browser_automation", required=False),
            ),
        )

    def open_page(
        self,
        url: str,
        context: CapabilityInvocationContext,
    ) -> BrowserSessionHandle:
        payload = self._require_browser_provider().open_page(url, session_id=context.session_id)
        return BrowserSessionHandle(
            session_token=str(payload.get("session_token") or context.session_id),
            current_url=str(payload.get("current_url") or url),
            metadata=dict(payload.get("metadata") or {}),
        )

    def inspect_dom(
        self,
        session_token: str,
        selector: str | None,
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        del context
        payload = self._require_browser_provider().inspect_dom(session_token, selector)
        return self._observation_from_payload(session_token, payload)

    def click(
        self,
        session_token: str,
        target: str,
        context: CapabilityInvocationContext,
    ) -> BrowserActionReceipt:
        self._ensure_mutation_allowed(context)
        payload = self._require_browser_provider().click(session_token, target)
        return self._receipt_from_payload(session_token, "click", payload)

    def type_text(
        self,
        session_token: str,
        target: str,
        value: str,
        context: CapabilityInvocationContext,
    ) -> BrowserActionReceipt:
        self._ensure_mutation_allowed(context)
        payload = self._require_browser_provider().type_text(session_token, target, value)
        return self._receipt_from_payload(session_token, "type_text", payload)

    def wait_for(
        self,
        session_token: str,
        condition: dict[str, Any],
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        del context
        payload = self._require_browser_provider().wait_for(session_token, condition)
        return self._observation_from_payload(session_token, payload)

    def capture_screenshot(
        self,
        session_token: str,
        label: str | None,
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        del context
        payload = self._require_browser_provider().capture_screenshot(session_token, label)
        return self._observation_from_payload(session_token, payload)

    def _ensure_mutation_allowed(self, context: CapabilityInvocationContext) -> None:
        if context.sandbox_decision == "denied":
            raise PermissionError("Sandbox denied the browser interaction request.")
        if not context.approval_ref:
            raise PermissionError("Approval is required before mutating browser state.")

    def _require_browser_provider(self) -> BrowserAutomationProviderPort:
        if self.browser_provider is None:
            raise RuntimeError("Browser automation provider is not configured.")
        return self.browser_provider

    def _observation_from_payload(
        self,
        session_token: str,
        payload: dict[str, Any],
    ) -> BrowserObservation:
        return BrowserObservation(
            session_token=str(payload.get("session_token") or session_token),
            kind=str(payload.get("kind") or "browser"),
            value=str(payload.get("value") or ""),
            metadata=dict(payload.get("metadata") or {}),
        )

    def _receipt_from_payload(
        self,
        session_token: str,
        action: str,
        payload: dict[str, Any],
    ) -> BrowserActionReceipt:
        return BrowserActionReceipt(
            session_token=str(payload.get("session_token") or session_token),
            action=str(payload.get("action") or action),
            status=str(payload.get("status") or "completed"),
            metadata=dict(payload.get("metadata") or {}),
        )
