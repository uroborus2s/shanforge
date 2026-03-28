#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the host CLI to trigger (read the
skill) for a set of queries. Supports Claude, Gemini, and Codex.
"""

import argparse
import json
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from providers import get_provider
from utils import parse_skill_md


def find_project_root() -> Path:
    """Find the nearest usable project root for host CLI execution."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if any((parent / marker).exists() for marker in (".agents", ".gemini", ".codex", ".claude", ".git")):
            return parent
    return current


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query and return whether the skill was triggered."""
    provider = get_provider(model or "claude")
    try:
        result = provider.run_query(query, skill_name, skill_description, timeout, project_root)
        return result.triggered
    except Exception as e:
        print(f"Error running query '{query}': {e}", file=sys.stderr)
        return False


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description in SKILL.md")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=1, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model for evaluation")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)
    name, description, _ = parse_skill_md(skill_path)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=args.description or description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=find_project_root(),
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
