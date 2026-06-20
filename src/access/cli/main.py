from __future__ import annotations

from access.api.runtime_api import RuntimeAPI
from access.cli.commands.run_demo import build_demo_manifest


def main(runtime_api: RuntimeAPI) -> None:
    """Runs the local scaffold demo through an injected runtime API."""

    result = runtime_api.run_manifest(
        manifest=build_demo_manifest(),
        user_input="Build the abstract shanforge v2 platform scaffold.",
    )
    print(result.response.raw_output)


if __name__ == "__main__":
    raise SystemExit("Use scripts/shanforge-cli to launch the demo scaffold.")
