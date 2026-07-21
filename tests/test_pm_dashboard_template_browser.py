from __future__ import annotations

import html
import json
import os
import re
import shutil
import struct
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = REPO_ROOT / "skills/using-shanforge/references/status-dashboard-template.html"
VIEWPORTS = ((1440, 900), (1024, 768), (768, 1024), (390, 844), (320, 568))
MODULE_PREFIXES = (
    "TEAM",
    "CHARTER",
    "WBS",
    "SCHEDULE",
    "RISKS",
    "COMMUNICATIONS",
    "MEETINGS",
    "STATUS_REPORTS",
    "CHANGES",
    "CLOSURE",
)
FRAGMENT_SLOTS = {
    "STATUS_DISTRIBUTION_SEGMENTS",
    "OVERVIEW_DETAIL_ROWS",
    *(f"{prefix}_ROWS" for prefix in MODULE_PREFIXES),
    *(f"{prefix}_SOURCE_DETAILS" for prefix in MODULE_PREFIXES),
}
VALIDATION_STATUSES = {"verified", "incomplete", "conflict", "stale", "failed"}
RENDER_DISPOSITIONS = {"FULL", "PARTIAL", "ERROR_ONLY"}
ERROR_ONLY_ALLOWED = {
    "PROJECT_NAME",
    "PROJECT_ID",
    "AS_OF_H",
    "AS_OF_TIME",
    "PROJECT_TIMEZONE",
    "VALIDATION_STATUS",
    "VALIDATION_MESSAGE",
    "RENDER_DISPOSITION",
    "ERROR_CODE",
    "AFFECTED_PATHS",
    "RECOVERY_ACTION",
}
ALLOWED_FRAGMENT_ATTRIBUTES = {
    "tr": {"data-row", "data-sort-value"},
    "td": set(),
    "span": {"class", "aria-label"},
    "dt": set(),
    "dd": set(),
}


class SafeFragment(str):
    """Marker for fragments produced by the fixed fixture renderer, never callers."""


class _FragmentValidator(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in ALLOWED_FRAGMENT_ATTRIBUTES:
            raise ValueError(f"fragment tag is not registered: {tag}")
        allowed = ALLOWED_FRAGMENT_ATTRIBUTES[tag]
        for name, value in attrs:
            if name not in allowed or name.startswith("on"):
                raise ValueError(f"fragment attribute is not registered: {tag}.{name}")
            if value and "javascript:" in value.casefold():
                raise ValueError("javascript URLs are forbidden")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def _safe_fragment(markup: str) -> SafeFragment:
    validator = _FragmentValidator(convert_charrefs=True)
    validator.feed(markup)
    validator.close()
    return SafeFragment(markup)


def _find_node_with_playwright() -> tuple[str, dict[str, str]]:
    node_candidates = tuple(
        candidate
        for candidate in (
            os.environ.get("SHANFORGE_NODE_BIN"),
            shutil.which("node"),
            str(
                Path.home()
                / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
            ),
        )
        if candidate
    )
    module_candidates = tuple(
        candidate
        for candidate in (
            os.environ.get("SHANFORGE_NODE_PATH"),
            os.environ.get("NODE_PATH"),
            str(REPO_ROOT / "node_modules"),
            str(
                Path.home()
                / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
            ),
        )
        if candidate
    )
    checked: list[str] = []
    for node in node_candidates:
        if not Path(node).is_file():
            continue
        for module_path in module_candidates:
            environment = dict(os.environ)
            environment["NODE_PATH"] = module_path
            result = subprocess.run(
                [node, "-e", 'require.resolve("playwright")'],
                capture_output=True,
                text=True,
                env=environment,
                timeout=5,
            )
            checked.append(f"{node} / NODE_PATH={module_path}")
            if result.returncode == 0:
                return node, environment
    raise AssertionError(f"Node Playwright runtime not found; checked: {checked}")


PLAYWRIGHT_DRIVER = r"""
const { chromium } = require('playwright');
const [
  overrideChrome, probeUri, visualUri, screenshotPath, widthText, heightText
] = process.argv.slice(2);
(async () => {
  const launchOptions = {
    headless: true,
    args: [
      '--disable-background-networking', '--disable-component-update',
      '--disable-gpu', '--no-first-run'
    ]
  };
  if (overrideChrome) launchOptions.executablePath = overrideChrome;
  const browser = await chromium.launch(launchOptions);
  try {
    const viewport = {width: Number(widthText), height: Number(heightText)};
    const probePage = await browser.newPage({viewport, deviceScaleFactor: 1});
    const browserErrors = [];
    probePage.on('pageerror', error => browserErrors.push(String(error)));
    await probePage.goto(probeUri, {waitUntil: 'load'});
    const raw = await probePage.locator('#browser-probe').textContent({timeout: 5000});
    const result = JSON.parse(raw);
    result.browserExecutable = overrideChrome || chromium.executablePath();
    result.browserVersion = browser.version();
    result.consoleErrors.push(...browserErrors);
    await probePage.close();

    const visualPage = await browser.newPage({viewport, deviceScaleFactor: 1});
    await visualPage.goto(visualUri, {waitUntil: 'load'});
    await visualPage.evaluate(() => document.fonts.ready);
    await visualPage.screenshot({path: screenshotPath, fullPage: false});
    await visualPage.close();
    process.stdout.write(JSON.stringify(result));
  } finally {
    await browser.close();
  }
})().catch(error => {
  process.stderr.write(String(error && error.stack ? error.stack : error));
  process.exit(1);
});
"""


def _row(*values: str, sort_value: str) -> SafeFragment:
    cells = "".join(f"<td>{html.escape(value)}</td>" for value in values)
    return _safe_fragment(
        f'<tr data-row data-sort-value="{html.escape(sort_value)}">{cells}</tr>'
    )


def _source_details(source: str, digest: str) -> SafeFragment:
    return _safe_fragment(
        f"<dt>来源</dt><dd>{html.escape(source)}</dd>"
        f"<dt>摘要</dt><dd>{html.escape(digest)}</dd>"
    )


def _authorized_team_rows(records: list[dict[str, str]]) -> SafeFragment:
    rows = [
        _row(
            record["name"],
            record["role"],
            record["department"],
            record["responsibility"],
            sort_value=record["sort_value"],
        )
        for record in records
    ]
    return _safe_fragment("".join(rows))


def _fixture_values() -> dict[str, str | SafeFragment]:
    values: dict[str, str | SafeFragment] = {
        "PROJECT_NAME": "shanforge",
        "PROJECT_ID": "shanforge",
        "STAGE_NAME": "开发实施",
        "AS_OF_H": "128",
        "AS_OF_TIME": "2026-07-21 11:58:00 +08:00",
        "PROJECT_TIMEZONE": "Asia/Shanghai",
        "VALIDATION_STATUS": "verified",
        "VALIDATION_MESSAGE": "快照完整且已核对",
        "SNAPSHOT_ID": "snapshot-128",
        "SNAPSHOT_SHA256_SHORT": "a1b2c3d4e5f6",
        "SOURCE_ROOT_SHA256_SHORT": "112233445566",
        "AUTHORIZATION_DIGEST_SHORT": "ffeeddccbbaa",
        "RULE_VERSION": "project-progress-rules/v2",
        "RENDER_DISPOSITION": "FULL",
        "TOTAL_TASKS": "123",
        "COMPLETED_TASKS": "26",
        "COMPLETION_RATE": "21.14%",
        "ACTIVE_TASKS": "7",
        "PENDING_APPROVALS": "2",
        "BLOCKED_OR_OVERDUE_TASKS": "3",
        "DEPLOYED_DELIVERABLES": "1",
        "STATUS_DISTRIBUTION_SEGMENTS": _safe_fragment(
            '<span class="distribution-segment completed" aria-label="已完成 26"></span>'
            '<span class="distribution-segment active" aria-label="其他 97"></span>'
        ),
        "STATUS_DISTRIBUTION_LEGEND": "已完成 26 · 其他 97",
        "ACTIVE_SUMMARY": "7 项真正进行中，最近活动 3 分钟前",
        "APPROVAL_SUMMARY": "2 项待审批，最长等待 4 小时",
        "RECENT_COMPLETION_SUMMARY": "24 小时内完成 3 项",
        "DEPLOYMENT_SUMMARY": "1 个交付物已上线且健康",
        "BLOCKED_OVERDUE_SUMMARY": "2 项阻塞，1 项逾期",
        "NEXT_MILESTONE_SUMMARY": "R001 候选冻结 · 7 月 22 日",
        "ERROR_CODE": "--",
        "AFFECTED_PATHS": "--",
        "RECOVERY_ACTION": "--",
        "REDACTION_NOTICE": "联系方式和审批意见已按当前权限脱敏",
        "OVERVIEW_DETAIL_ROWS": _row(
            "TASK-001", "固定 H 查询", "进行中", "继续验证", sort_value="001"
        ),
    }
    row_shapes = {
        "TEAM": ("王工", "项目经理", "平台组", "总体负责"),
        "CHARTER": ("背景", "项目状态查询必须快且准", "已批准"),
        "WBS": ("2.0", "Beta 汇总", "in_progress", "AI_EXECUTOR"),
        "SCHEDULE": ("R001 候选", "2026-07-22", "AI_EXECUTOR", "按计划"),
        "RISKS": ("R-001", "事实页过期", "中", "开放"),
        "COMMUNICATIONS": ("项目负责人", "当前状态", "每轮", "对话"),
        "MEETINGS": ("M-001", "状态模板评审", "2026-07-21", "2 项行动"),
        "STATUS_REPORTS": ("SR-001", "按计划", "7 项进行中", "2 项待审批"),
        "CHANGES": ("CR-001", "模板校准", "已批准", "UI"),
        "CLOSURE": ("项目总结", "进行中", "已完成 26/123", "未关闭"),
    }
    for prefix, columns in row_shapes.items():
        values[f"{prefix}_COUNT"] = "2" if prefix == "WBS" else "1"
        values[f"{prefix}_MISSING_COUNT"] = "0"
        values[f"{prefix}_CONFLICT_COUNT"] = "0"
        values[f"{prefix}_AS_OF_TIME"] = values["AS_OF_TIME"]
        values[f"{prefix}_SOURCE_DIGEST_SHORT"] = f"{prefix.lower()}-digest"
        values[f"{prefix}_EMPTY_REASON"] = "有数据"
        rows = [_row(*columns, sort_value="002")]
        if prefix == "WBS":
            rows.append(_row("1.0", "Alpha 基线", "completed", "AI_EXECUTOR", sort_value="001"))
        values[f"{prefix}_ROWS"] = _safe_fragment("".join(rows))
        values[f"{prefix}_SOURCE_DETAILS"] = _source_details(
            "SRC-WORKITEM-LEDGER-001",
            "已绑定 snapshot-128",
        )
    return values


def _probe_script() -> str:
    return r"""
<script>
(() => {
  const rgb = value => (value.match(/[\d.]+/g) || []).slice(0, 3).map(Number);
  const luminance = value => {
    const channels = rgb(value).map(channel => {
      const normalized = channel / 255;
      return normalized <= .04045 ? normalized / 12.92 : ((normalized + .055) / 1.055) ** 2.4;
    });
    return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
  };
  const contrast = (a, b) => {
    const first = luminance(a), second = luminance(b);
    return (Math.max(first, second) + .05) / (Math.min(first, second) + .05);
  };
  const rect = element => {
    const value = element.getBoundingClientRect();
    return {left:value.left, top:value.top, right:value.right, bottom:value.bottom,
      width:value.width, height:value.height};
  };
  const required = [...document.querySelectorAll('[data-first-screen-required]')];
  const requiredRects = required.map(rect);
  const overlaps = [];
  for (let i = 0; i < requiredRects.length; i += 1) {
    for (let j = i + 1; j < requiredRects.length; j += 1) {
      const a = requiredRects[i], b = requiredRects[j];
      const width = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
      const height = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
      if (width > 1 && height > 1) overlaps.push([i, j, width, height]);
    }
  }
  const firstScreen = rect(document.querySelector('#overview-first-screen'));
  const moduleResults = [...document.querySelectorAll('.module-page')].map(section => {
    const sectionRect = rect(section);
    const blockSelector = [
      ':scope > .module-header', ':scope > .module-meta', ':scope > .toolbar',
      ':scope > .empty-note', ':scope > .table-scroll', ':scope > details',
      ':scope > .top-link'
    ].join(', ');
    const blocks = [...section.querySelectorAll(blockSelector)];
    const blockRects = blocks.map(rect);
    const blockOverlaps = [];
    for (let i = 0; i < blockRects.length; i += 1) {
      for (let j = i + 1; j < blockRects.length; j += 1) {
        const a = blockRects[i], b = blockRects[j];
        const width = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const height = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        if (width > 1 && height > 1) blockOverlaps.push([i, j, width, height]);
      }
    }
    const controls = [...section.querySelectorAll('input, button, summary, a.top-link')];
    const focusFailures = controls.filter(control => {
      control.focus({focusVisible:true});
      if (!document.hasFocus()) control.dispatchEvent(new FocusEvent('focusin', {bubbles:true}));
      const style = getComputedStyle(control);
      return document.activeElement !== control
        || style.outlineStyle === 'none'
        || parseFloat(style.outlineWidth) <= 0;
    }).map(control => control.id || control.tagName);
    return {
      id:section.id,
      blockCount:blocks.length,
      controls:controls.length,
      blockOverlaps,
      focusFailures,
      withinSection:blockRects.every(item =>
        item.left >= sectionRect.left - 1
        && item.right <= sectionRect.right + 1
        && item.width > 0 && item.height > 0
      ),
      notClipped:blocks.filter(element => !element.classList.contains('table-scroll'))
        .every(element =>
          element.scrollWidth <= element.clientWidth + 1
          && element.scrollHeight <= element.clientHeight + 1
        ),
      tableScrollContained:[...section.querySelectorAll('.table-scroll')]
        .every(element =>
          element.getBoundingClientRect().right <= sectionRect.right + 1
          && element.clientWidth > 0
        )
    };
  });
  const focusTarget = document.querySelector('.module-nav a');
  focusTarget.focus({focusVisible:true});
  if (!document.hasFocus()) focusTarget.dispatchEvent(new FocusEvent('focusin', {bubbles:true}));
  const focusStyle = getComputedStyle(focusTarget);
  const focusVisible = focusStyle.outlineStyle !== 'none'
    && parseFloat(focusStyle.outlineWidth) > 0;
  const focusDiagnostic = {active:document.activeElement === focusTarget,
    focus:focusTarget.matches(':focus'),visible:focusTarget.matches(':focus-visible'),
    style:focusStyle.outlineStyle,width:focusStyle.outlineWidth,color:focusStyle.outlineColor};
  const contrastSelector = [
    '[data-contrast]', '.module-page h2', '.module-page p', '.module-page label',
    '.module-page button', '.module-page input', '.module-page summary',
    '.module-page th', '.module-page td', '.module-meta span', '.module-meta strong'
  ].join(', ');
  const contrastResults = [...document.querySelectorAll(contrastSelector)].map(element => {
    const style = getComputedStyle(element);
    let owner = element;
    let background = style.backgroundColor;
    while (owner.parentElement
      && (background === 'rgba(0, 0, 0, 0)' || background === 'transparent')) {
      owner = owner.parentElement;
      background = getComputedStyle(owner).backgroundColor;
    }
    return contrast(style.color, background);
  });
  const filter = document.querySelector('#wbs-filter');
  filter.value = 'Beta';
  filter.dispatchEvent(new Event('input', {bubbles:true}));
  const visibleAfterFilter = [...document.querySelectorAll('#module-wbs [data-row]')]
    .filter(row => !row.hidden).map(row => row.textContent.trim());
  filter.value = '';
  filter.dispatchEvent(new Event('input', {bubbles:true}));
  document.querySelector('#wbs-sort').click();
  const sortedValues = [...document.querySelectorAll('#module-wbs [data-row]')]
    .map(row => row.dataset.sortValue);
  const details = document.querySelector('#module-wbs [data-source-details]');
  details.open = true;
  const result = {
    viewport:[innerWidth, innerHeight],
    bodyWidth:document.documentElement.scrollWidth,
    firstScreen,
    requiredInViewport:requiredRects.every(item =>
      item.left >= -1 && item.right <= innerWidth + 1
      && item.top >= -1 && item.bottom <= innerHeight + 1
      && item.width > 0 && item.height > 0
    ),
    requiredNotClipped:required.every(element =>
      element.scrollWidth <= element.clientWidth + 1
      && element.scrollHeight <= element.clientHeight + 1
    ),
    overlaps,
    focusVisible,
    focusDiagnostic,
    moduleResults,
    minimumContrast:Math.min(...contrastResults),
    visibleAfterFilter,
    sortedValues,
    sourceExpanded:details.open,
    consoleErrors:window.__pmConsoleErrors || []
  };
  const output = document.createElement('pre');
  output.id = 'browser-probe';
  output.textContent = JSON.stringify(result);
  document.body.appendChild(output);
})();
</script>
"""


def _validated_values(
    template: str,
    values: dict[str, str | SafeFragment],
) -> dict[str, str | SafeFragment]:
    placeholders = set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", template))
    if set(values) != placeholders:
        missing = sorted(placeholders - set(values))
        extra = sorted(set(values) - placeholders)
        raise ValueError(f"fixture slot mismatch; missing={missing}, extra={extra}")

    validation_status = str(values["VALIDATION_STATUS"])
    disposition = str(values["RENDER_DISPOSITION"])
    if validation_status not in VALIDATION_STATUSES:
        raise ValueError(f"unregistered validation status: {validation_status}")
    if disposition not in RENDER_DISPOSITIONS:
        raise ValueError(f"unregistered render disposition: {disposition}")
    if validation_status in {"conflict", "stale", "failed"} and disposition != "ERROR_ONLY":
        raise ValueError(f"{validation_status} must fail closed as ERROR_ONLY")
    if disposition == "PARTIAL" and validation_status != "incomplete":
        raise ValueError("PARTIAL is only valid for an incomplete snapshot")
    if disposition == "FULL" and validation_status != "verified":
        raise ValueError("FULL requires a verified snapshot")
    if disposition != "ERROR_ONLY":
        for prefix in MODULE_PREFIXES:
            if str(values[f"{prefix}_CONFLICT_COUNT"]) != "0":
                raise ValueError(f"{prefix}_CONFLICT_COUNT must force ERROR_ONLY")

    normalized = dict(values)
    if disposition == "ERROR_ONLY":
        for key, value in normalized.items():
            if key in ERROR_ONLY_ALLOWED:
                continue
            normalized[key] = SafeFragment("") if isinstance(value, SafeFragment) else ""
    return normalized


def _render_template(values: dict[str, str | SafeFragment], *, include_probe: bool = False) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    normalized = _validated_values(template, values)

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        value = normalized[key]
        if key in FRAGMENT_SLOTS:
            if not isinstance(value, SafeFragment):
                raise TypeError(f"{key} must be generated as a SafeFragment")
            return _safe_fragment(str(value))
        return html.escape(str(value), quote=True)

    rendered = re.sub(r"\{\{([A-Z0-9_]+)\}\}", replace, template)
    if include_probe:
        rendered = rendered.replace("</body>", f"{_probe_script()}</body>")
    assert "{{" not in rendered
    return rendered


def _render_fixture(path: Path) -> None:
    rendered = _render_template(_fixture_values(), include_probe=True)
    path.write_text(rendered, encoding="utf-8")


def _run_playwright(
    tmp_path: Path,
    probe_fixture: Path,
    visual_fixture: Path,
    screenshot: Path,
    width: int,
    height: int,
) -> dict[str, object]:
    node, environment = _find_node_with_playwright()
    driver = tmp_path / "pm-dashboard-playwright-driver.cjs"
    driver.write_text(PLAYWRIGHT_DRIVER, encoding="utf-8")
    result = subprocess.run(
        [
            node,
            str(driver),
            os.environ.get("SHANFORGE_CHROME_BIN", ""),
            probe_fixture.as_uri(),
            visual_fixture.as_uri(),
            str(screenshot),
            str(width),
            str(height),
        ],
        capture_output=True,
        text=True,
        env=environment,
        timeout=30,
    )
    if result.returncode != 0:
        raise AssertionError(f"Playwright Chrome driver failed: {result.stderr[-4000:]}")
    return json.loads(result.stdout)


def _png_dimensions(path: Path) -> tuple[int, int]:
    payload = path.read_bytes()
    assert len(payload) > 10_000
    assert payload[:8] == b"\x89PNG\r\n\x1a\n"
    return struct.unpack(">II", payload[16:24])


def test_fixture_renderer_escapes_scalars_and_rejects_unsafe_fragments() -> None:
    values = _fixture_values()
    values["PROJECT_NAME"] = '<img src=x onerror="alert(1)">'
    rendered = _render_template(values)
    assert '<img src=x onerror="alert(1)">' not in rendered
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in rendered

    for payload in (
        '<script>alert("x")</script>',
        '<tr data-row data-sort-value="1" onclick="alert(1)"><td>x</td></tr>',
        '<span class="distribution-segment" aria-label="javascript:alert(1)"></span>',
    ):
        unsafe = _fixture_values()
        unsafe["STATUS_DISTRIBUTION_SEGMENTS"] = SafeFragment(payload)
        with pytest.raises(ValueError):
            _render_template(unsafe)

    raw_fragment = _fixture_values()
    raw_fragment["TEAM_ROWS"] = "<tr><td>caller supplied HTML</td></tr>"
    with pytest.raises(TypeError):
        _render_template(raw_fragment)


@pytest.mark.parametrize("validation_status", ("conflict", "stale", "failed"))
def test_error_only_fails_closed_and_removes_old_business_values(
    validation_status: str,
) -> None:
    values = _fixture_values()
    values["VALIDATION_STATUS"] = validation_status
    values["RENDER_DISPOSITION"] = "ERROR_ONLY"
    values["ERROR_CODE"] = f"STATUS_{validation_status.upper()}"
    values["ACTIVE_SUMMARY"] = "OLD_ACTIVE_BUSINESS_SECRET"
    values["TEAM_ROWS"] = _row(
        "OLD_TEAM_BUSINESS_SECRET", "角色", "部门", "职责", sort_value="001"
    )
    rendered = _render_template(values)

    assert f'data-validation-status="{validation_status}"' in rendered
    assert 'data-render-disposition="ERROR_ONLY"' in rendered
    assert f"STATUS_{validation_status.upper()}" in rendered
    assert "OLD_ACTIVE_BUSINESS_SECRET" not in rendered
    assert "OLD_TEAM_BUSINESS_SECRET" not in rendered


@pytest.mark.parametrize("validation_status", ("conflict", "stale", "failed"))
def test_non_eligible_snapshots_cannot_render_business_dispositions(
    validation_status: str,
) -> None:
    values = _fixture_values()
    values["VALIDATION_STATUS"] = validation_status
    values["RENDER_DISPOSITION"] = "PARTIAL"
    with pytest.raises(ValueError, match="must fail closed"):
        _render_template(values)


def test_fixture_authorization_omits_denied_fields_and_unknown_slots() -> None:
    denied_email = "wang@example.invalid"
    denied_approval_comment = "SECRET_APPROVAL_COMMENT"
    raw_records = [
        {
            "name": "王工",
            "role": "项目经理",
            "department": "平台组",
            "responsibility": "总体负责",
            "sort_value": "001",
            "email": denied_email,
            "approval_comment": denied_approval_comment,
        }
    ]
    values = _fixture_values()
    values["TEAM_ROWS"] = _authorized_team_rows(raw_records)
    rendered = _render_template(values)
    assert denied_email not in rendered
    assert denied_approval_comment not in rendered
    assert "联系方式和审批意见已按当前权限脱敏" in rendered

    values["TEAM_EMAIL"] = denied_email
    with pytest.raises(ValueError, match="extra=.*TEAM_EMAIL"):
        _render_template(values)


@pytest.mark.parametrize(("width", "height"), VIEWPORTS)
def test_template_geometry_accessibility_and_interactions(
    tmp_path: Path,
    width: int,
    height: int,
) -> None:
    fixture = tmp_path / f"dashboard-{width}x{height}.html"
    _render_fixture(fixture)
    screenshot_root = Path(
        os.environ.get("PM_DASHBOARD_SCREENSHOT_DIR", str(tmp_path / "screenshots"))
    )
    screenshot_root.mkdir(parents=True, exist_ok=True)
    screenshot = screenshot_root / f"dashboard-{width}x{height}.png"
    visual_fixture = tmp_path / f"dashboard-{width}x{height}-visual.html"
    visual_fixture.write_text(_render_template(_fixture_values()), encoding="utf-8")
    result = _run_playwright(
        tmp_path,
        fixture,
        visual_fixture,
        screenshot,
        width,
        height,
    )

    assert result["viewport"] == [width, height], result
    assert Path(str(result["browserExecutable"])).is_file(), result
    assert re.search(r"\d+\.\d+", str(result["browserVersion"])), result
    assert result["bodyWidth"] <= result["viewport"][0] + 1
    assert result["firstScreen"]["top"] >= -1
    assert result["firstScreen"]["bottom"] <= result["viewport"][1] + 1
    assert result["requiredInViewport"] is True
    assert result["requiredNotClipped"] is True
    assert result["overlaps"] == []
    assert result["focusVisible"] is True, result["focusDiagnostic"]
    assert result["minimumContrast"] >= 4.5
    assert [item["id"] for item in result["moduleResults"]] == [
        f"module-{name}"
        for name in (
            "team",
            "charter",
            "wbs",
            "schedule",
            "risks",
            "communications",
            "meetings",
            "status-reports",
            "changes",
            "closure",
        )
    ]
    for module in result["moduleResults"]:
        assert module["blockCount"] == 7, module
        assert module["controls"] == 4, module
        assert module["blockOverlaps"] == [], module
        assert module["focusFailures"] == [], module
        assert module["withinSection"] is True, module
        assert module["notClipped"] is True, module
        assert module["tableScrollContained"] is True, module
    assert len(result["visibleAfterFilter"]) == 1
    assert "Beta" in result["visibleAfterFilter"][0]
    assert result["sortedValues"] == ["001", "002"]
    assert result["sourceExpanded"] is True
    assert result["consoleErrors"] == []

    image_width, image_height = _png_dimensions(screenshot)
    assert image_width == width
    assert image_height == height
