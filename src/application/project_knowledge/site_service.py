"""Application orchestration for a deterministic HTML snapshot."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class RenderedSite:
    pages: dict[str, str]
    page_fingerprints: dict[str, str]
    page_input_fingerprints: dict[str, str]
    site_fingerprint: str
    input_token: str
    generation_id: str


class SiteDataPort(Protocol):
    def current_input_token(self, *, profile: str) -> str: ...

    def load(self, *, profile: str = "local-owner") -> dict[str, Any]: ...


class SiteRendererPort(Protocol):
    def render(
        self,
        model: dict[str, Any],
        *,
        profile: str,
        previous: dict[str, object] | None = None,
    ) -> RenderedSite: ...


class SitePublisherPort(Protocol):
    def lookup(self, *, input_token: str, profile: str) -> Any | None: ...

    def render_cache(self, *, profile: str) -> dict[str, object] | None: ...

    def publish(
        self,
        rendered: RenderedSite,
        *,
        profile: str,
        built_at: str,
        fail_at: str | None = None,
    ) -> Any: ...


class ProjectSiteService:
    def __init__(
        self,
        data: SiteDataPort,
        renderer: SiteRendererPort,
        publisher: SitePublisherPort,
    ) -> None:
        self._data = data
        self._renderer = renderer
        self._publisher = publisher

    def snapshot(self, *, profile: str, built_at: str) -> dict[str, Any]:
        input_token = self._data.current_input_token(profile=profile)
        cached = self._publisher.lookup(input_token=input_token, profile=profile)
        if cached is not None:
            return asdict(cached)
        rendered = self._renderer.render(
            self._data.load(profile=profile),
            profile=profile,
            previous=self._publisher.render_cache(profile=profile),
        )
        receipt = self._publisher.publish(rendered, profile=profile, built_at=built_at)
        return asdict(receipt)
