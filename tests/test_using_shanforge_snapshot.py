from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "using-shanforge" / "scripts" / "project_snapshot.py"


class ProjectSnapshotTest(unittest.TestCase):
    def test_skill_first_boundary_has_no_repository_runtime(self) -> None:
        self.assertFalse((ROOT / "src").exists())
        for path in (
            ROOT / "skills" / "using-shanforge" / "SKILL.md",
            ROOT / "skills" / "using-shanforge" / "references" / "pm-dashboard-rendering.md",
        ):
            content = path.read_text(encoding="utf-8")
            self.assertIn("scripts/project_snapshot.py", content)
            self.assertNotIn("PYTHONPATH=src", content)
            self.assertNotIn("settings.composition.project_knowledge", content)

    def test_external_project_snapshot_is_self_contained_and_cached(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            work_item = project / ".factory" / "workitems" / "WI-001"
            task_briefs = work_item / "task-briefs"
            task_briefs.mkdir(parents=True)
            (work_item / "brief.md").write_text(
                "# WI-001：交付登录流程\n\n"
                "- 状态：in_progress\n"
                "- 用户目标：让门店员工安全登录并继续处理订单。\n",
                encoding="utf-8",
            )
            (task_briefs / "WI-001-T01.md").write_text(
                "# WI-001-T01：完成登录流程验收\n\n"
                "- 状态：ready_for_review\n"
                "- 优先级：P0\n"
                "- 任务层级：requirement\n"
                "- 关联目标：REQ-LOGIN-001\n\n"
                "## 目标\n\n"
                "确认登录功能满足门店业务要求。\n\n"
                "## 验证\n\n"
                "登录成功、失败提示和移动端布局均通过验收。\n",
                encoding="utf-8",
            )
            (work_item / "ledger.jsonl").write_text(
                json.dumps(
                    {
                        "time": "2026-07-29T00:01:00+08:00",
                        "task_card_id": "WI-001-T01",
                        "task_title": "完成登录流程验收",
                        "status": "ready_for_review",
                        "next_required_action": "request_independent_review",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            completed = project / ".factory" / "workitems" / "WI-OLD"
            completed.mkdir()
            (completed / "brief.md").write_text(
                "# WI-OLD：旧登录方案\n\n- 状态：superseded\n",
                encoding="utf-8",
            )
            (completed / "ledger.jsonl").write_text(
                json.dumps({"status": "superseded"}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            attention = project / ".factory" / "workitems" / "WI-DECISION"
            attention.mkdir()
            (attention / "brief.md").write_text(
                "# WI-DECISION：确认登录方式\n\n- 状态：needs_user_input\n",
                encoding="utf-8",
            )
            (attention / "ledger.jsonl").write_text(
                json.dumps({"status": "needs_user_input"}, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            (project / ".factory" / "workitems" / "implementation").mkdir()

            first = self._run(project)
            second = self._run(project)
            relative = self._run(project, "--relative-paths")

            self.assertEqual(first["status"], "success")
            self.assertFalse(first["cache_hit"])
            self.assertTrue(second["cache_hit"])
            self.assertEqual(relative["html_path"], ".factory/cache/site/current/index.html")
            output = project / ".factory" / "cache" / "site" / "current" / "index.html"
            html = output.read_text(encoding="utf-8")
            self.assertIn("当前重点", html)
            self.assertIn("交付登录流程", html)
            self.assertIn("让门店员工安全登录并继续处理订单", html)
            self.assertIn("完成登录流程验收", html)
            self.assertIn("确认登录功能满足门店业务要求", html)
            self.assertIn("REQ-LOGIN-001", html)
            self.assertIn("P0", html)
            self.assertIn("需求任务", html)
            self.assertIn("等待独立评审", html)
            self.assertIn("下一步：完成独立评审", html)
            self.assertLess(html.index("需要关注（1）"), html.index("正在推进（1）"))
            self.assertLess(html.index("正在推进（1）"), html.index("已完成（1）"))
            self.assertNotIn("implementation · implementation", html)
            self.assertIn('class="skip-link"', html)
            self.assertIn('<main id="main">', html)
            self.assertNotIn(str(ROOT / "src"), html)

    def test_failures_use_receipt_and_output_cannot_escape_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            project = base / "project"
            factory = project / ".factory"
            factory.mkdir(parents=True)
            (factory / "cache").write_text("conflict", encoding="utf-8")

            conflict = self._raw_run(project)
            self.assertEqual(conflict.returncode, 2)
            self.assertEqual(json.loads(conflict.stdout)["status"], "failed")
            self.assertNotIn("Traceback", conflict.stderr)

            (factory / "cache").unlink()
            outside = base / "outside"
            outside.mkdir()
            (factory / "cache").symlink_to(outside, target_is_directory=True)

            escaped = self._raw_run(project)
            self.assertEqual(escaped.returncode, 2)
            self.assertIn("outside project root", json.loads(escaped.stdout)["error"])
            self.assertFalse((outside / "site" / "current" / "index.html").exists())

            metadata_project = base / "metadata-project"
            current = metadata_project / ".factory" / "cache" / "site" / "current"
            current.mkdir(parents=True)
            (current / "index.html").write_text("old", encoding="utf-8")
            (current / "snapshot.json").write_text("[]\n", encoding="utf-8")

            invalid_metadata = self._raw_run(metadata_project)
            self.assertEqual(invalid_metadata.returncode, 2)
            self.assertIn(
                "metadata must be an object",
                json.loads(invalid_metadata.stdout)["error"],
            )
            self.assertNotIn("Traceback", invalid_metadata.stderr)

    def _run(self, project: Path, *arguments: str) -> dict[str, object]:
        result = self._raw_run(project, *arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def _raw_run(self, project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(project),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
