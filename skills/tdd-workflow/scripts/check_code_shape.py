#!/usr/bin/env python3
"""Reject named local functions and report one-call helper candidates."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path


class ShapeVisitor(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.depth = 0
        self.local_functions: list[str] = []
        self.local_lambdas: list[str] = []
        self.functions: list[str] = []
        self.calls: dict[str, int] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if self.depth:
            self.local_functions.append(
                f"{self.path}:{node.lineno}: named local function {node.name}"
            )
        else:
            self.functions.append(node.name)
        self.depth += 1
        self.generic_visit(node)
        self.depth -= 1

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, node: ast.Lambda) -> None:
        if self.depth:
            self.local_lambdas.append(
                f"{self.path}:{node.lineno}: lambda in function body"
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name):
            self.calls[node.func.id] = self.calls.get(node.func.id, 0) + 1
        self.generic_visit(node)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    violations: list[str] = []
    helpers: list[str] = []
    for path in args.paths:
        visitor = ShapeVisitor(path)
        visitor.visit(ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
        violations.extend(visitor.local_functions)
        violations.extend(visitor.local_lambdas)
        helpers.extend(
            f"{path}: helper candidate {name} has one call site"
            for name in visitor.functions
            if name != "main" and visitor.calls.get(name) == 1
        )
    print("\n".join([*violations, *helpers]))
    return int(bool(violations))


if __name__ == "__main__":
    raise SystemExit(main())
