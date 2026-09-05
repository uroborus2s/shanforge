#!/usr/bin/env python3
"""BM25 search CLI and candidate-only design-system CLI."""

import argparse
import json
import sys

from core import AVAILABLE_STACKS, CSV_CONFIG, MAX_RESULTS, search, search_stack
from design_system import generate_design_system


def format_output(result: dict) -> str:
    if "error" in result:
        return f"Error: {result['error']}"
    heading = "Stack Guidelines" if result.get("stack") else "Search Results"
    lines = [f"## UI Pro Max {heading}", f"**Query:** {result['query']}"]
    for row in result["results"]:
        lines.append(f"- {json.dumps(row, ensure_ascii=False)}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UI Pro Max Search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--domain", "-d", choices=list(CSV_CONFIG), help="Search one domain")
    parser.add_argument("--stack", "-s", choices=AVAILABLE_STACKS, help="Stack guideline context")
    parser.add_argument("--max-results", "-n", type=int, default=MAX_RESULTS, help="Positive result limit")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--design-system", "-ds", action="store_true", help="Return design candidates")
    parser.add_argument("--project-name", "-p")
    parser.add_argument("--format", "-f", choices=["ascii", "markdown"], default=None)
    parser.add_argument("--persist", action="store_true", help="Create a candidate JSON file")
    parser.add_argument("--page", help="Candidate page context")
    parser.add_argument("--output-dir", "-o")
    parser.add_argument("--platform", choices=["web", "mini-program", "apple", "android", "desktop"])
    parser.add_argument("--surface", choices=["persuade", "operate", "read", "experience"])
    parser.add_argument("--locale")
    parser.add_argument("--variance", type=int, choices=range(1, 11), metavar="1-10")
    parser.add_argument("--motion", type=int, choices=range(1, 11), metavar="1-10")
    parser.add_argument("--density", type=int, choices=range(1, 11), metavar="1-10")
    args = parser.parse_args()
    if not args.query.strip():
        parser.error("query must not be blank")
    if args.max_results < 1:
        parser.error("max-results must be a positive integer")
    if args.domain and args.design_system:
        parser.error("--domain conflicts with --design-system")
    if args.domain and args.stack:
        parser.error("--domain conflicts with --stack")
    if args.persist and not args.design_system:
        parser.error("--persist requires --design-system")
    if args.output_dir and not args.persist:
        parser.error("--output-dir requires --persist")
    if args.page and not args.design_system:
        parser.error("--page requires --design-system")
    if not args.design_system and any((args.project_name, args.format, args.platform, args.surface,
                                       args.locale, args.variance, args.motion, args.density)):
        parser.error("project-name, format, platform, surface, locale, and dials require --design-system")
    return args


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parse_args()
    if args.design_system:
        try:
            result = generate_design_system(
                args.query, args.project_name, "json" if args.json else (args.format or "ascii"),
                persist=args.persist, page=args.page, output_dir=args.output_dir,
                variance=args.variance, motion=args.motion, density=args.density,
                stack=args.stack, platform=args.platform, surface=args.surface,
                locale=args.locale, max_results=args.max_results,
            )
        except (ValueError, FileExistsError, OSError) as error:
            print(f"search.py: error: {error}", file=sys.stderr)
            return 2
        print(result)
        return 0
    result = search_stack(args.query, args.stack, args.max_results) if args.stack else search(args.query, args.domain, args.max_results)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else format_output(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
