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
        del context
        provider = self._require_search_provider()
        normalized_limit = max(1, min(limit, 10))
        results = provider.search(query, limit=normalized_limit, filters=filters)
        return tuple(
            WebSearchHit(
                url=str(item.get("url") or ""),
                title=str(item.get("title") or item.get("url") or ""),
                snippet=str(item.get("snippet") or ""),
                rank=int(item.get("rank") or index),
                metadata={
                    key: value
                    for key, value in item.items()
                    if key not in {"url", "title", "snippet", "rank"}
                },
            )
            for index, item in enumerate(results, start=1)
        )

    def fetch_url(
        self,
        url: str,
        context: CapabilityInvocationContext,
    ) -> WebDocument:
        del context
        payload = self._require_document_provider().fetch(url)
        return self._document_from_payload(url, payload)

    def extract_document(
        self,
        url: str,
        mode: str,
        context: CapabilityInvocationContext,
    ) -> WebDocument:
        del context
        payload = self._require_document_provider().extract(url, mode)
        return self._document_from_payload(url, payload)

    def normalize_citation(
        self,
        document: WebDocument,
        context: CapabilityInvocationContext,
    ) -> CapabilityCitation:
        del context
        locator = str(document.metadata.get("locator") or "") or None
        return CapabilityCitation(
            source_uri=document.url,
            title=document.title,
            locator=locator,
        )

    def _document_from_payload(
        self,
        url: str,
        payload: dict[str, object],
    ) -> WebDocument:
        return WebDocument(
            url=str(payload.get("url") or url),
            title=str(payload.get("title") or "") or None,
            content=str(payload.get("content") or ""),
            extracted_text=str(payload.get("extracted_text") or ""),
            metadata={
                key: value
                for key, value in payload.items()
                if key not in {"url", "title", "content", "extracted_text"}
            },
        )

    def _require_search_provider(self) -> WebSearchProviderPort:
        if self.search_provider is None:
            raise RuntimeError("Web search provider is not configured.")
        return self.search_provider

    def _require_document_provider(self) -> WebDocumentProviderPort:
        if self.document_provider is None:
            raise RuntimeError("Web document provider is not configured.")
        return self.document_provider
