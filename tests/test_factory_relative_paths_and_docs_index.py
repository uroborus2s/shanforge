import importlib.util
import json
import os
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
FACTORY_PROJECT_COMPRESS = REPO_ROOT / "scripts" / "factory-project-compress"
FACTORY_INIT = REPO_ROOT / "scripts" / "factory-init"
FACTORY_AGENT_SESSION = REPO_ROOT / "scripts" / "factory-agent-session"
FACTORY_DISPATCH = REPO_ROOT / "scripts" / "factory-dispatch"
FACTORY_DOCS_STANDARD_UPGRADE_BATCH = REPO_ROOT / "scripts" / "factory-docs-standard-upgrade-batch"
LEGACY_ROOT = str(Path("/") / "Users" / "uroborus" / "shanforge")
EXAMPLE_PROJECT = Path("/tmp/example-project")


def load_script_module(module_name: str, script_path: Path):
    script_dir = str(script_path.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    loader = SourceFileLoader(module_name, str(script_path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FactoryRelativePathAndDocsIndexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_compress = load_script_module("factory_project_compress", FACTORY_PROJECT_COMPRESS)
        cls.factory_init = load_script_module("factory_init", FACTORY_INIT)
        cls.agent_session = load_script_module("factory_agent_session", FACTORY_AGENT_SESSION)
        cls.dispatch = load_script_module("factory_dispatch", FACTORY_DISPATCH)
        cls.docs_upgrade_batch = load_script_module("factory_docs_standard_upgrade_batch", FACTORY_DOCS_STANDARD_UPGRADE_BATCH)
        cls.factory_core = sys.modules["factory_core"]
        cls.example_project_resolved = EXAMPLE_PROJECT.resolve()
        cls.expected_runtime_protocol = Path(
            os.path.relpath(
                REPO_ROOT / "skills" / "software-factory-cli" / "references" / "ai-runtime-protocol.md",
                cls.example_project_resolved,
            )
        ).as_posix()
        cls.expected_role_charter = Path(
            os.path.relpath(
                REPO_ROOT / "skills" / "software-factory-cli" / "references" / "ai-role-charter.md",
                cls.example_project_resolved,
            )
        ).as_posix()
        cls.expected_dispatch = Path(
            os.path.relpath(REPO_ROOT / "scripts" / "factory-dispatch", cls.example_project_resolved)
        ).as_posix()
        cls.expected_docs_index = Path(
            os.path.relpath(REPO_ROOT / "docs" / "index.md", cls.example_project_resolved)
        ).as_posix()
        cls.expected_brainstorm_skill = Path(
            os.path.relpath(REPO_ROOT / "skills" / "brainstorming" / "SKILL.md", cls.example_project_resolved)
        ).as_posix()

    def test_project_compress_agents_md_uses_relative_workspace_paths(self):
        output = self.project_compress.build_agents_md(
            EXAMPLE_PROJECT,
            {"project_name": "example-project"},
        )

        self.assertIn(f"`{self.expected_runtime_protocol}`", output)
        self.assertIn(f"`{self.expected_role_charter}`", output)
        self.assertIn("项目根目录：`.`", output)
        self.assertNotIn("`/Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_project_compress_gemini_md_uses_relative_workspace_paths(self):
        output = self.project_compress.build_gemini_md(
            EXAMPLE_PROJECT,
            {"project_name": "example-project"},
        )

        self.assertIn(f"`{self.expected_runtime_protocol}`", output)
        self.assertIn(f"`{self.expected_role_charter}`", output)
        self.assertIn("项目根目录：`.`", output)
        self.assertNotIn("`/Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_project_compress_runtime_brief_uses_relative_dispatch_path(self):
        output = self.project_compress.build_runtime_brief(
            EXAMPLE_PROJECT,
            {
                "project_name": "example-project",
                "stage": "MAINTENANCE",
                "active_mode": "DEFAULT",
                "stack": "node",
            },
            owner="tester",
            note="path-regression",
        )

        self.assertIn(f"python3 {self.expected_dispatch}", output)
        self.assertIn('--project "."', output)
        self.assertNotIn("python3 /Users/", output)
        self.assertNotIn(LEGACY_ROOT, output)

    def test_agent_session_recommended_commands_use_relative_dispatch_path(self):
        commands = self.agent_session.recommended_commands(
            EXAMPLE_PROJECT,
            "MAINTENANCE",
            "tester",
            "focus",
            0,
        )

        command_blob = "\n".join(commands)
        self.assertIn(f"python3 {self.expected_dispatch}", command_blob)
        self.assertIn('--project "."', command_blob)
        self.assertNotIn("python3 /Users/", command_blob)
        self.assertNotIn(LEGACY_ROOT, command_blob)

    def test_dispatch_resolves_docs_standard_upgrade_alias(self):
        self.assertEqual(self.dispatch.resolve_action("docs-upgrade"), "docs-standard-upgrade")
        self.assertEqual(self.dispatch.resolve_action("upgrade-docs-standard"), "docs-standard-upgrade")
        self.assertEqual(self.dispatch.resolve_action("docs-upgrade-batch"), "docs-standard-upgrade-batch")

    def test_load_project_config_normalizes_legacy_current_stage(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            factory_dir = project_root / ".factory"
            factory_dir.mkdir(parents=True)
            (factory_dir / "project.json").write_text(
                json.dumps(
                    {
                        "project_name": "legacy-project",
                        "current_stage": "MAINTENANCE",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            config = self.factory_core.load_project_config(project_root)

        self.assertEqual(config["stage"], "MAINTENANCE")

    def test_factory_init_project_config_uses_relative_paths(self):
        payload = json.loads(
            self.factory_init.build_project_config(
                project_name="example-project",
                idea="idea",
                stack="python",
                owner="tester",
                target=EXAMPLE_PROJECT,
                config=self.factory_init.load_config(),
            )
        )

        self.assertEqual(payload["project_root"], ".")
        self.assertIn(self.expected_runtime_protocol, payload["ai_runtime_docs"])
        self.assertIn(self.expected_docs_index, payload["human_workflow_docs"])
        self.assertIn(self.expected_brainstorm_skill, [item["path"] for item in payload["shared_skills"]])
        self.assertFalse(any(Path(item).is_absolute() for item in payload["ai_runtime_docs"]))
        self.assertFalse(any(Path(item["path"]).is_absolute() for item in payload["shared_skills"]))

    def test_docs_stratego_indexes_have_front_matter_and_nav(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "04-project-development" / "03-requirements").mkdir(parents=True)
            (project_root / "docs" / "04-project-development" / "04-design" / "private-design").mkdir(parents=True)
            (project_root / "docs" / "04-project-development" / "03-requirements" / "prd.md").write_text(
                "# 产品需求文档\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "04-project-development" / "04-design" / "system-architecture.md").write_text(
                "# 系统架构设计\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "04-project-development" / "04-design" / "private-design" / "overview.md").write_text(
                "# 内部方案总览\n",
                encoding="utf-8",
            )

            written = self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            requirements_index = (
                project_root / "docs" / "04-project-development" / "03-requirements" / "index.md"
            ).read_text(encoding="utf-8")
            solution_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "index.md"
            ).read_text(encoding="utf-8")
            private_design_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "private-design" / "index.md"
            ).read_text(encoding="utf-8")

        self.assertIn("docs/index.md", written)
        self.assertIn("---\n", root_index)
        self.assertIn("title: 示例项目", root_index)
        self.assertIn("home_access: public", root_index)
        self.assertIn("path: 04-project-development/index.md", root_index)
        self.assertIn("path: 04-project-development/03-requirements/index.md", root_index)
        self.assertIn("path: 04-project-development/03-requirements/prd.md", root_index)
        self.assertIn("path: 04-project-development/04-design/index.md", root_index)
        self.assertIn("path: 04-project-development/04-design/system-architecture.md", root_index)
        self.assertIn("title: 内部专题", root_index)
        self.assertIn("path: 04-project-development/04-design/private-design/index.md", root_index)
        self.assertIn("path: 04-project-development/04-design/private-design/overview.md", root_index)
        self.assertIn("access: public", root_index)
        self.assertIn("access: private", root_index)
        self.assertTrue(requirements_index.startswith("# 需求概览\n"))
        self.assertIn("目录树、页面路径和访问级别统一由根 `docs/index.md` 声明", requirements_index)
        self.assertNotIn("建议阅读顺序", requirements_index)
        self.assertNotIn("mkdocs:", requirements_index)
        self.assertNotIn("default_access:", requirements_index)
        self.assertTrue(solution_index.startswith("# 设计文档概览\n"))
        self.assertIn("目录树、页面路径和访问级别统一由根 `docs/index.md` 声明", solution_index)
        self.assertNotIn("建议阅读顺序", solution_index)
        self.assertTrue(private_design_index.startswith("# 内部专题概览\n"))
        self.assertIn("本页是该目录的正文首页", private_design_index)
        self.assertNotIn("/Users/", root_index)

    def test_docs_stratego_source_status_detects_missing_indexes_and_absolute_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "04-project-development" / "02-discovery").mkdir(parents=True)
            input_path = project_root / "docs" / "04-project-development" / "02-discovery" / "input.md"
            input_path.write_text("# 项目输入\n\n路径 `/Users/example/project`。\n", encoding="utf-8")

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            input_path.write_text("# 项目输入\n\n使用相对路径 `./docs/index.md`。\n", encoding="utf-8")
            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status_before, "异常")
        self.assertTrue(any("docs/index.md" in line or "机器绝对路径" in line for line in lines_before))
        self.assertEqual(status_after, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line or "未发现明显机器绝对路径污染" in line for line in lines_after))

    def test_docs_stratego_source_status_detects_missing_nav_targets_and_explicit_self_anchors(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            user_guide_dir = project_root / "docs" / "02-user-guide"
            user_guide_dir.mkdir(parents=True)
            prompt_path = user_guide_dir / "prompt-templates.md"
            prompt_path.write_text(
                "# 提示词速查\n\n[跳转](#3-空目录新项目初始化)\n\n## 3. 空目录新项目初始化\n",
                encoding="utf-8",
            )
            (user_guide_dir / "user-guide.md").write_text("# 使用指南\n", encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_path.write_text(
                root_text.replace(
                    "path: 02-user-guide/user-guide.md\n          access: public\n",
                    "path: 02-user-guide/user-guide.md\n"
                    "          access: public\n"
                    "        - title: 缺失页面\n"
                    "          path: 02-user-guide/missing.md\n"
                    "          access: public\n",
                ),
                encoding="utf-8",
            )

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            prompt_path.write_text(
                "# 提示词速查\n\n[跳转](#3-空目录新项目初始化)\n\n<a id=\"3-空目录新项目初始化\"></a>\n\n## 3. 空目录新项目初始化\n",
                encoding="utf-8",
            )
            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status_before, "异常")
        self.assertTrue(any("导航项指向不存在的页面" in line for line in lines_before))
        self.assertTrue(any("未声明显式锚点" in line for line in lines_before))
        self.assertEqual(status_after, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines_after))

    def test_factory_init_creates_section_indexes_for_docs_stratego(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "managed-project"
            written = self.factory_init.initialize_project(
                target=project_root,
                project_name="managed-project",
                idea="ship docs",
                stack="python",
                owner="tester",
                force=False,
            )
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            governance_index = (
                project_root / "docs" / "04-project-development" / "01-governance" / "index.md"
            ).read_text(encoding="utf-8")
            solution_index = (
                project_root / "docs" / "04-project-development" / "04-design" / "index.md"
            ).read_text(encoding="utf-8")
            developer_index = (
                project_root / "docs" / "03-developer-guide" / "index.md"
            ).read_text(encoding="utf-8")
            status, lines = self.factory_core.docs_stratego_source_status(project_root, "managed-project")

        self.assertIn(str(project_root / "docs" / "index.md"), written)
        self.assertIn(str(project_root / "docs" / "04-project-development" / "01-governance" / "index.md"), written)
        self.assertIn("home_access: public", root_index)
        self.assertIn("path: 01-getting-started/index.md", root_index)
        self.assertIn("path: 04-project-development/index.md", root_index)
        self.assertTrue(governance_index.startswith("# 项目治理概览\n"))
        self.assertIn("本页是该目录的正文首页", governance_index)
        self.assertNotIn("mkdocs:", governance_index)
        self.assertTrue(solution_index.startswith("# 设计文档概览\n"))
        self.assertIn("本页是该目录的正文首页", solution_index)
        self.assertIn("module 开发、调试、交付与排错", developer_index)
        self.assertEqual(status, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines))

    def test_detect_docs_profile_omits_developer_guide_for_docs_site(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "README.md").write_text(
                "# 章略·墨衡 文档站点\n\n这是一个供用户阅读和运营维护的 docs-stratego / mkdocs 文档站点。\n",
                encoding="utf-8",
            )
            (project_root / "mkdocs.yml").write_text("site_name: docs-site\n", encoding="utf-8")

            profile = self.factory_core.detect_docs_profile(
                project_root,
                project_name="docs-site",
                idea="构建章略·墨衡文档站点，供用户阅读和站点运维，不提供 SDK、插件或对外 API。",
                stack="mkdocs",
            )

        self.assertEqual(profile["project_kind"], "docs_site")
        self.assertEqual(profile["modules"]["02-user-guide"], "required")
        self.assertEqual(profile["modules"]["03-developer-guide"], "omit")
        self.assertFalse(profile["surfaces"]["secondary_development"])

    def test_factory_init_uses_docs_profile_to_omit_developer_guide(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "docs-site"
            written = self.factory_init.initialize_project(
                target=project_root,
                project_name="docs-site",
                idea="构建章略·墨衡文档站点，供用户阅读和站点运维，不提供 SDK、插件或对外 API。",
                stack="mkdocs",
                owner="tester",
                force=False,
            )
            project_config = json.loads((project_root / ".factory" / "project.json").read_text(encoding="utf-8"))
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            publication_policy = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")

        self.assertIn(str(project_root / "docs" / "publication-policy.json"), written)
        self.assertEqual(project_config["docs_profile"]["modules"]["03-developer-guide"], "omit")
        self.assertFalse((project_root / "docs" / "03-developer-guide").exists())
        self.assertNotIn("path: 03-developer-guide/index.md", root_index)
        self.assertNotIn("docs/03-developer-guide/**", publication_policy)
        self.assertFalse(any("03-developer-guide/application-development.md" in item for item in project_config["human_workflow_docs"]))

    def test_docs_stratego_source_status_accepts_custom_index_content(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "03-developer-guide").mkdir(parents=True)
            (project_root / "docs" / "03-developer-guide" / "application-development.md").write_text(
                "# 应用开发\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "03-developer-guide" / "plugin-development.md").write_text(
                "# 插件开发\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_front_matter, _ = self.factory_core.split_markdown_front_matter(root_text)
            self.assertIsNotNone(root_front_matter)
            root_path.write_text(
                f"{root_front_matter}\n# 示例项目自定义入口\n\n这里保留人工维护的正文，不要求和生成模板逐字一致。\n",
                encoding="utf-8",
            )

            developer_index_path = project_root / "docs" / "03-developer-guide" / "index.md"
            developer_index_path.write_text(
                "# 开发者指南\n\n## 自定义正文\n\n先看应用开发，再看插件开发，函数和接口按项目实际情况扩展。\n",
                encoding="utf-8",
            )

            status, lines = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status, "就绪")
        self.assertTrue(any("根 `docs/index.md`" in line for line in lines))

    def test_write_docs_stratego_indexes_preserves_custom_index_bodies(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "03-developer-guide").mkdir(parents=True)
            (project_root / "docs" / "03-developer-guide" / "application-development.md").write_text(
                "# 应用开发\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_front_matter, _ = self.factory_core.split_markdown_front_matter(root_text)
            root_path.write_text(
                f"{root_front_matter}\n# 自定义首页\n\n保留人工撰写的首页正文。\n",
                encoding="utf-8",
            )

            developer_index_path = project_root / "docs" / "03-developer-guide" / "index.md"
            developer_index_path.write_text(
                "# 自定义开发者指南\n\n这里是人工维护的目录概览，不应被刷新动作覆盖。\n",
                encoding="utf-8",
            )

            (project_root / "docs" / "03-developer-guide" / "function-reference.md").write_text(
                "# 函数说明\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            refreshed_root = root_path.read_text(encoding="utf-8")
            refreshed_developer_index = developer_index_path.read_text(encoding="utf-8")

        self.assertIn("# 自定义首页", refreshed_root)
        self.assertIn("path: 03-developer-guide/function-reference.md", refreshed_root)
        self.assertEqual(
            refreshed_developer_index,
            "# 自定义开发者指南\n\n这里是人工维护的目录概览，不应被刷新动作覆盖。\n",
        )

    def test_write_docs_stratego_indexes_preserves_manual_nav_grouping_and_order(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            developer_dir = project_root / "docs" / "03-developer-guide"
            user_dir = project_root / "docs" / "02-user-guide"
            getting_started_dir = project_root / "docs" / "01-getting-started"
            project_dev_dir = project_root / "docs" / "04-project-development"
            developer_dir.mkdir(parents=True)
            user_dir.mkdir(parents=True)
            getting_started_dir.mkdir(parents=True)
            project_dev_dir.mkdir(parents=True)
            (developer_dir / "index.md").write_text("# 开发者指南\n", encoding="utf-8")
            (developer_dir / "application-development.md").write_text("# 应用开发\n", encoding="utf-8")
            (developer_dir / "function-reference.md").write_text("# 函数说明\n", encoding="utf-8")
            (developer_dir / "plugin-development.md").write_text("# 插件开发\n", encoding="utf-8")
            (user_dir / "index.md").write_text("# 用户指南\n", encoding="utf-8")
            (user_dir / "user-guide.md").write_text("# 使用指南\n", encoding="utf-8")
            (getting_started_dir / "index.md").write_text("# 入门说明\n", encoding="utf-8")
            (getting_started_dir / "quick-start.md").write_text("# 快速开始\n", encoding="utf-8")
            (project_dev_dir / "index.md").write_text("# 项目开发文档\n", encoding="utf-8")

            custom_root = """---
title: 示例项目
mkdocs:
  home_access: public
  nav:
    - title: 二次开发中心
      children:
        - title: 概览
          path: 03-developer-guide/index.md
          access: public
        - title: 函数先看
          path: 03-developer-guide/function-reference.md
          access: public
        - title: 应用开发
          path: 03-developer-guide/application-development.md
          access: public
    - title: 用户入口
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
        - title: 使用指南
          path: 02-user-guide/user-guide.md
          access: public
---
# 自定义首页

这里保留人工维护的导航分组顺序。
"""
            (project_root / "docs" / "index.md").write_text(custom_root, encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_root = (project_root / "docs" / "index.md").read_text(encoding="utf-8")

        self.assertIn("title: 二次开发中心", refreshed_root)
        self.assertIn("title: 用户入口", refreshed_root)
        self.assertIn("title: 函数先看", refreshed_root)
        self.assertIn("path: 03-developer-guide/plugin-development.md", refreshed_root)
        self.assertLess(refreshed_root.index("title: 二次开发中心"), refreshed_root.index("title: 用户入口"))
        self.assertLess(
            refreshed_root.index("path: 03-developer-guide/function-reference.md"),
            refreshed_root.index("path: 03-developer-guide/application-development.md"),
        )
        self.assertLess(
            refreshed_root.index("path: 03-developer-guide/application-development.md"),
            refreshed_root.index("path: 03-developer-guide/plugin-development.md"),
        )
        self.assertIn("title: 入门说明", refreshed_root)
        self.assertIn("title: 项目开发文档（内）", refreshed_root)

    def test_write_docs_stratego_indexes_refreshes_generated_directory_indexes_without_mkdocs(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            concepts_dir = project_root / "docs" / "03-developer-guide" / "01-concepts"
            concepts_dir.mkdir(parents=True)
            (concepts_dir / "01-system-map.md").write_text(
                "# 1.1 系统地图与术语\n",
                encoding="utf-8",
            )
            (concepts_dir / "02-real-constraints.md").write_text(
                "# 1.2 当前真实约束\n",
                encoding="utf-8",
            )
            stale_index_path = concepts_dir / "index.md"
            stale_index_path.write_text(
                "# 01 concepts概览\n\n本目录收纳与“01 concepts”相关的页面和子目录。\n\n建议阅读顺序：\n\n1. 1.1 系统地图与术语\n2. 1.2 当前真实约束\n",
                encoding="utf-8",
            )

            written = self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_index = stale_index_path.read_text(encoding="utf-8")

        self.assertIn("docs/03-developer-guide/01-concepts/index.md", written)
        self.assertTrue(refreshed_index.startswith("# 01 概念与约束概览\n"))
        self.assertIn("系统地图、术语和真实约束", refreshed_index)
        self.assertIn("本页是该目录的正文首页", refreshed_index)
        self.assertNotIn("建议阅读顺序", refreshed_index)

    def test_docs_stratego_indexes_include_contract_files_and_preserve_access_overrides(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            openapi_dir = project_root / "docs" / "04-project-development" / "04-design" / "subsystems" / "gateway" / "openapi"
            tools_dir = project_root / "docs" / "03-developer-guide" / "tools"
            openapi_dir.mkdir(parents=True)
            tools_dir.mkdir(parents=True)
            (openapi_dir / "index.md").write_text("# Gateway OpenAPI 概览\n", encoding="utf-8")
            (tools_dir / "index.md").write_text("# 工具契约概览\n", encoding="utf-8")
            (openapi_dir / "app.openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: App API\n  version: 1.0.0\npaths: {}\n",
                encoding="utf-8",
            )
            (tools_dir / "public-agent.mcp-tools.json").write_text(
                json.dumps(
                    {
                        "tools": [
                            {
                                "name": "build_site",
                                "title": "Public Agent Tools",
                                "description": "Build docs site.",
                                "inputSchema": {"type": "object"},
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")

            root_path = project_root / "docs" / "index.md"
            root_text = root_path.read_text(encoding="utf-8")
            root_text = root_text.replace("home_access: public", "home_access: private")
            root_text = root_text.replace("title: App API", "title: 外部 App API")
            root_text = root_text.replace(
                "path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml\n"
                "                          access: private",
                "path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml\n"
                "                          access: public",
            )
            root_path.write_text(root_text, encoding="utf-8")

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            refreshed_root = root_path.read_text(encoding="utf-8")

        self.assertIn("home_access: private", refreshed_root)
        self.assertIn("path: 04-project-development/04-design/subsystems/gateway/openapi/app.openapi.yaml", refreshed_root)
        self.assertIn("title: 外部 App API", refreshed_root)
        self.assertIn("access: public", refreshed_root)
        self.assertIn("path: 03-developer-guide/tools/public-agent.mcp-tools.json", refreshed_root)
        self.assertIn("title: Public Agent Tools", refreshed_root)

    def test_docs_stratego_source_status_rejects_invalid_contract_pages_and_assets_contracts(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            openapi_dir = project_root / "docs" / "03-developer-guide" / "openapi"
            assets_dir = project_root / "docs" / "03-developer-guide" / "assets"
            openapi_dir.mkdir(parents=True)
            assets_dir.mkdir(parents=True)
            (openapi_dir / "index.md").write_text("# OpenAPI 概览\n", encoding="utf-8")
            (openapi_dir / "broken.openapi.yaml").write_text(
                "openapi: 3.1.0\ninfo:\n  title: Broken API\npaths: {}\n",
                encoding="utf-8",
            )
            (assets_dir / "hidden.mcp-tools.yaml").write_text(
                "tools:\n  - name: hidden\n    description: hidden tool\n    inputSchema:\n      type: object\n",
                encoding="utf-8",
            )

            self.factory_core.write_docs_stratego_indexes(project_root, "示例项目")
            status, lines = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

        self.assertEqual(status, "异常")
        self.assertTrue(any("broken.openapi.yaml" in line and "info.version" in line for line in lines))
        self.assertTrue(any("assets/" in line and "契约文件" in line for line in lines))

    def test_upgrade_docs_source_standard_migrates_legacy_project_and_returns_ready(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "02-requirements").mkdir(parents=True)
            (project_root / "docs" / "08-handover").mkdir(parents=True)
            (project_root / "docs" / "README.md").write_text("# 旧入口\n", encoding="utf-8")
            (project_root / "docs" / "02-requirements" / "prd.md").write_text("# 产品需求文档\n", encoding="utf-8")
            (project_root / "docs" / "08-handover" / "user-guide.md").write_text("# 用户指南\n", encoding="utf-8")

            result = self.factory_core.upgrade_docs_source_standard(project_root, "示例项目")

            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            policy_text = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")

        self.assertTrue(result["migrated"])
        self.assertEqual(result["status"], "就绪")
        self.assertIn("path: 04-project-development/03-requirements/prd.md", root_index)
        self.assertIn("docs/index.md", policy_text)

    def test_discover_upgrade_candidate_projects_finds_managed_projects_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            managed_a = root / "proj-a"
            managed_b = root / "group" / "proj-b"
            unmanaged = root / "proj-c"
            skipped = root / "node_modules" / "proj-d"

            for project in [managed_a, managed_b]:
                (project / ".factory").mkdir(parents=True)
                (project / "docs").mkdir(parents=True)
                (project / ".factory" / "project.json").write_text('{"project_name":"demo"}', encoding="utf-8")

            (unmanaged / "docs").mkdir(parents=True)
            (skipped / ".factory").mkdir(parents=True)
            (skipped / "docs").mkdir(parents=True)
            (skipped / ".factory" / "project.json").write_text('{"project_name":"skip"}', encoding="utf-8")

            discovered = self.docs_upgrade_batch.discover_upgrade_candidate_projects([root], max_depth=3)

        self.assertEqual(discovered, sorted([managed_a.resolve(), managed_b.resolve()]))

    def test_migrate_docs_structure_upgrades_legacy_layout_and_rewrites_links(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            (project_root / "docs" / "02-requirements").mkdir(parents=True)
            (project_root / "docs" / "03-solution").mkdir(parents=True)
            (project_root / "docs" / "08-handover").mkdir(parents=True)
            (project_root / "docs" / "README.md").write_text(
                "# 旧入口\n\n查看 [需求](./02-requirements/prd.md)。\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "02-requirements" / "prd.md").write_text(
                "# 产品需求文档\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "03-solution" / "solution-overview.md").write_text(
                "# 总体方案与协作总览\n\n- [PRD](../02-requirements/prd.md)\n- [用户指南](../08-handover/user-guide.md)\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "08-handover" / "user-guide.md").write_text(
                "# 用户指南\n",
                encoding="utf-8",
            )
            (project_root / "docs" / "08-handover" / "historical-project-prompt-templates.md").write_text(
                "# 历史项目标准提示词模板\n",
                encoding="utf-8",
            )

            status_before, lines_before = self.factory_core.docs_stratego_source_status(project_root, "示例项目")
            result = self.factory_core.migrate_docs_structure(project_root, "示例项目")
            status_after, lines_after = self.factory_core.docs_stratego_source_status(project_root, "示例项目")

            overview_path = project_root / "docs" / "04-project-development" / "04-design" / "solution-overview.md"
            migrated_text = overview_path.read_text(encoding="utf-8")
            project_overview = (project_root / "docs" / "01-getting-started" / "project-overview.md").read_text(encoding="utf-8")
            root_index = (project_root / "docs" / "index.md").read_text(encoding="utf-8")
            policy_text = (project_root / "docs" / "publication-policy.json").read_text(encoding="utf-8")
            legacy_solution_exists = (project_root / "docs" / "03-solution").exists()
            prompt_templates_exists = (project_root / "docs" / "02-user-guide" / "prompt-templates.md").exists()

            self.assertEqual(status_before, "异常")
            self.assertTrue(any("docs-migrate-structure" in line for line in lines_before))
            self.assertTrue(any("docs/03-solution/solution-overview.md" in item for item in result["moved"]))
            self.assertFalse(legacy_solution_exists)
            self.assertTrue(prompt_templates_exists)
            self.assertIn("[PRD](../03-requirements/prd.md)", migrated_text)
            self.assertIn("[用户指南](../../02-user-guide/user-guide.md)", migrated_text)
            self.assertIn("[需求](../04-project-development/03-requirements/prd.md)", project_overview)
            self.assertIn("title: 入门说明", root_index)
            self.assertIn("title: 项目开发文档（内）", root_index)
            self.assertIn("docs/03-developer-guide/**", policy_text)
            self.assertEqual(status_after, "就绪")
            self.assertTrue(any("根 `docs/index.md`" in line for line in lines_after))


if __name__ == "__main__":
    unittest.main()
