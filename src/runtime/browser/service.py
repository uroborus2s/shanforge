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
        raise NotImplementedError("Scaffold only: implement browser session open in TASK-017.")

    def inspect_dom(
        self,
        session_token: str,
        selector: str | None,
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        raise NotImplementedError("Scaffold only: implement DOM inspection in TASK-017.")

    def click(
        self,
        session_token: str,
        target: str,
        context: CapabilityInvocationContext,
    ) -> BrowserActionReceipt:
        raise NotImplementedError("Scaffold only: implement click actions in TASK-017.")

    def type_text(
        self,
        session_token: str,
        target: str,
        value: str,
        context: CapabilityInvocationContext,
    ) -> BrowserActionReceipt:
        raise NotImplementedError("Scaffold only: implement typing actions in TASK-017.")

    def wait_for(
        self,
        session_token: str,
        condition: dict[str, Any],
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        raise NotImplementedError("Scaffold only: implement waits in TASK-017.")

    def capture_screenshot(
        self,
        session_token: str,
        label: str | None,
        context: CapabilityInvocationContext,
    ) -> BrowserObservation:
        raise NotImplementedError("Scaffold only: implement screenshots in TASK-017.")
