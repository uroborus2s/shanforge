from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class HttpRouteSpec:
    """Framework-agnostic HTTP route declaration."""

    method: str
    path: str
    name: str


def build_runtime_routes() -> tuple[HttpRouteSpec, ...]:
    """Exposes the platform runtime routes that a future HTTP server should bind."""

    return (
        HttpRouteSpec(method="POST", path="/apps/{app_id}/run", name="run_app"),
        HttpRouteSpec(method="POST", path="/manifests/run", name="run_manifest"),
        HttpRouteSpec(method="GET", path="/sessions/{session_id}", name="get_session"),
        HttpRouteSpec(
            method="GET",
            path="/projects/{project_id}/status",
            name="get_project_status",
        ),
    )
