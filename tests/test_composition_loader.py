from __future__ import annotations

import unittest

from shanforge_di import (
    ImportNotAllowedError,
    InvalidReferenceError,
    SymbolImportError,
    load_symbol,
)


class CompositionLoaderTests(unittest.TestCase):
    def test_loads_allowed_symbol(self) -> None:
        symbol = load_symbol(
            "settings.composition.component_bindings:build_component_container",
            allowed_prefixes=("settings.composition",),
        )

        self.assertEqual(symbol.__name__, "build_component_container")

    def test_rejects_disallowed_module(self) -> None:
        with self.assertRaises(ImportNotAllowedError):
            load_symbol("os:path", allowed_prefixes=("settings.composition",))

    def test_rejects_malformed_reference(self) -> None:
        with self.assertRaises(InvalidReferenceError):
            load_symbol("not-a-reference", allowed_prefixes=("settings.composition",))

    def test_rejects_missing_symbol(self) -> None:
        with self.assertRaises(SymbolImportError):
            load_symbol(
                "settings.composition.component_bindings:Missing",
                allowed_prefixes=("settings.composition",),
            )


if __name__ == "__main__":
    unittest.main()
