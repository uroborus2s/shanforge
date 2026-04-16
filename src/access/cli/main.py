from __future__ import annotations

from access.cli.commands.run_demo import build_demo_manifest
from settings.composition import build_default_container


def main() -> None:
    """Runs the local scaffold demo through the default container."""

    container = build_default_container()
    result = container.runtime_api.run_manifest(
        manifest=build_demo_manifest(),
        user_input="Build the abstract shanforge v2 platform scaffold.",
    )
    print(result.response.raw_output)


if __name__ == "__main__":
    main()
