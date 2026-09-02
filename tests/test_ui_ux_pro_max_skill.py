from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / "skills" / "ui-ux-pro-max"
SKILL = SKILL_DIR / "SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def run_search(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SKILL_DIR / "scripts" / "search.py"), *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_skill_triggers_cover_all_requested_platforms_and_motion() -> None:
    content = read(SKILL)
    frontmatter = content.split("---", maxsplit=2)[1]

    for phrase in (
        "Web",
        "小程序",
        "iOS",
        "iPadOS",
        "macOS",
        "Android",
        "Windows/Linux",
        "跨平台",
        "微交互",
        "页面转场",
        "手势动效",
    ):
        assert phrase in frontmatter

    assert "纯后端或只生成最终图片资源时不使用" in frontmatter


def test_main_entry_links_every_reference_directly() -> None:
    content = read(SKILL)
    linked = set(re.findall(r"\(references/([^)]+\.md)\)", content))
    actual = {path.name for path in (SKILL_DIR / "references").glob("*.md")}

    assert linked == actual
    for name in linked:
        assert (SKILL_DIR / "references" / name).is_file()


def test_skill_keeps_specialized_routing_and_project_contract() -> None:
    content = read(SKILL)

    for specialized_skill in (
        "art-asset-pipeline",
        "shadcn",
        "frontend-patterns",
        "webapp-testing",
        "skill-creator",
    ):
        assert specialized_skill in content

    for phrase in (
        "非 Shanforge work item 的最终响应结尾必须单独回写",
        "- work_item: <WORKITEM-ID or none>",
        "- skill: ui-ux-pro-max",
        "- status: ready_for_review | blocked | needs_user_input",
        "- outputs:",
        "- evidence:",
        "- ledger_event: <event id or none>",
        "- needs:",
        "../using-shanforge/references/work-skill-return-contract.md",
    ):
        assert phrase in content


def test_design_search_is_not_described_as_a_business_database() -> None:
    content = read(SKILL)

    assert "设计知识检索命中" in content
    assert "数据库命中" not in content


def test_platform_references_cover_native_constraints() -> None:
    expected = {
        "web.md": ("语义 HTML", "400%", "prefers-reduced-motion"),
        "admin-web.md": (
            "shadcn/ui",
            "Radix",
            "`new-york`",
            "lucide-react",
            "motion/react",
            "独立 URL 页面",
        ),
        "mobile-high-fidelity.md": (
            "Penpot 承载",
            "`imagegen`",
            "`art-asset-pipeline`",
            "不写入 `approved/`",
            "不能直接当组件稿",
        ),
        "mini-programs.md": ("基础库", "包体", "真机", "宿主", "固定 88rpx"),
        "apple-platforms.md": ("Dynamic Type", "VoiceOver", "多窗口", "44×44 pt"),
        "android.md": ("48×48 dp", "TalkBack", "预测返回", "折叠屏"),
        "desktop.md": ("窗口", "快捷键", "高 DPI", "多显示器"),
        "cross-platform.md": ("产品语义层", "平台映射层", "必交平台矩阵"),
    }

    for name, phrases in expected.items():
        content = read(SKILL_DIR / "references" / name)
        for phrase in phrases:
            assert phrase in content, f"{name} missing {phrase}"


def test_admin_web_uses_one_component_icon_and_motion_baseline() -> None:
    content = read(SKILL_DIR / "references" / "admin-web.md")
    skill = read(SKILL)

    for forbidden_alternative in (
        "Tabler",
        "Heroicons",
        "Phosphor",
        "GSAP",
        "Anime.js",
        "React Spring",
    ):
        assert forbidden_alternative in content

    assert "禁止同项目混用" in content
    assert "禁止另行引入" in content
    assert 'iconLibrary: "lucide"' in content
    assert "禁止页面级另选技术栈" in skill


def test_motion_contract_covers_intent_interruption_accessibility_and_budget() -> None:
    content = read(SKILL_DIR / "references" / "motion.md")

    for phrase in (
        "动效意图",
        "中断",
        "reduced-motion",
        "静态/淡入替代",
        "Lottie",
        "Rive",
        "包体",
        "60Hz",
        "120Hz",
        "目标低端设备",
    ):
        assert phrase in content


def test_open_source_research_is_traceable_and_license_aware() -> None:
    content = read(SKILL_DIR / "references" / "open-source-landscape.md")

    assert "2026-07-22 调研快照" in content
    for project in (
        "nextlevelbuilder/ui-ux-pro-max-skill",
        "storybookjs/storybook",
        "penpot/penpot",
        "NervJS/taro",
        "motiondivision/motion",
        "airbnb/lottie-web",
        "AvaloniaUI/Avalonia",
        "android/compose-samples",
        "thesysdev/openui",
        "open-pencil/open-pencil",
        "microsoft/WinUI-Gallery",
    ):
        assert project in content

    for license_name in ("MIT", "MPL-2.0", "Apache-2.0"):
        assert license_name in content

    upstream_license = read(SKILL_DIR / "LICENSE.upstream.txt")
    assert "MIT License" in upstream_license
    assert "Copyright (c) 2024 Next Level Builder" in upstream_license


def test_v211_stable_sync_adds_desktop_stacks_without_generated_duplicates() -> None:
    stacks = SKILL_DIR / "data" / "stacks"
    for name in ("avalonia", "javafx", "uno", "uwp", "winui", "wpf"):
        assert (stacks / f"{name}.csv").is_file()

    for obsolete in (
        SKILL_DIR / "data" / "_sync_all.py",
        SKILL_DIR / "data" / "design.csv",
        SKILL_DIR / "data" / "draft.csv",
    ):
        assert not obsolete.exists()

    tracked = subprocess.run(
        ["git", "ls-files", str(SKILL_DIR.relative_to(REPO_ROOT))],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert not any("__pycache__" in path or path.endswith(".pyc") for path in tracked)


def test_search_cli_generates_design_system_and_queries_native_stacks() -> None:
    design_system = run_search(
        "healthcare dashboard calm accessible",
        "--design-system",
        "--format",
        "markdown",
        "--project-name",
        "Care Console",
    )
    assert design_system.returncode == 0, design_system.stderr
    assert "Care Console" in design_system.stdout
    assert "Color" in design_system.stdout

    for stack, query in (
        ("swiftui", "navigation accessibility"),
        ("jetpack-compose", "adaptive navigation"),
        ("winui", "keyboard navigation"),
        ("avalonia", "responsive layout"),
    ):
        result = run_search(query, "--stack", stack, "--max-results", "1")
        assert result.returncode == 0, result.stderr
        assert result.stdout.strip(), stack


def test_codex_interface_metadata_is_present() -> None:
    content = read(SKILL_DIR / "agents" / "openai.yaml")

    assert 'display_name: "全平台 UI/UX Pro Max"' in content
    assert "跨 Web、小程序、移动端与桌面端" in content
    assert "$ui-ux-pro-max" in content
