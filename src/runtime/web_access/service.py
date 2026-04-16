from __future__ import annotations

from dataclasses import dataclass

from runtime.capability.contracts import (
    CapabilityCitation,
    CapabilityInvocationContext,
    CapabilityOperationDescriptor,
    CapabilityPackageDescriptor,
    CapabilityProviderDependency,
)
from runtime.ports.execution_backends import WebDocumentProviderPort, WebSearchProviderPort
from runtime.web_access.models import WebDocument, WebSearchHit


@dataclass(slots=True)
class WebAccessService:
    """Self-owned scaffold for the web search and extraction capability package."""

    search_provider: WebSearchProviderPort | None = None
    document_provider: WebDocumentProviderPort | None = None

    def describe_package(self) -> CapabilityPackageDescriptor:
        return CapabilityPackageDescriptor(
            package_id="web_access",
            name="Web Access",
            summary=(
                "Searches the web, fetches URLs, extracts readable documents, "
                "and emits citations."
            ),
            operations=(
                CapabilityOperationDescriptor(
                    operation_id="web.search",
                    method_name="search_web",
                    summary="Search web documents.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="web.fetch_url",
                    method_name="fetch_url",
                    summary="Fetch one URL resource.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="web.extract_document",
                    method_name="extract_document",
                    summary="Extract readable document content from one URL.",
                ),
                CapabilityOperationDescriptor(
                    operation_id="web.normalize_citation",
                    method_name="normalize_citation",
                    summary="Normalize one web document into a citation.",
                ),
            ),
            provider_dependencies=(
                CapabilityProviderDependency("web_search", required=False),
                CapabilityProviderDependency("web_document", required=False),
            ),
        )

    def search_web(
        self,
        query: str,
        limit: int,
        filters: dict[str, object] | None,
        context: CapabilityInvocationContext,
    ) -> tuple[WebSearchHit, ...]:
        raise NotImplementedError("Scaffold only: implement web search in TASK-017.")

    def fetch_url(
        self,
        url: str,
        context: CapabilityInvocationContext,
    ) -> WebDocument:
        raise NotImplementedError("Scaffold only: implement URL fetch in TASK-017.")

    def extract_document(
        self,
        url: str,
        mode: str,
        context: CapabilityInvocationContext,
    ) -> WebDocument:
        raise NotImplementedError("Scaffold only: implement document extraction in TASK-017.")

    def normalize_citation(
        self,
        document: WebDocument,
        context: CapabilityInvocationContext,
    ) -> CapabilityCitation:
        raise NotImplementedError("Scaffold only: implement citation normalization in TASK-017.")
