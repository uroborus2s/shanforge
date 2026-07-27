from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


class PrototypeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.buttons: list[dict[str, str | None]] = []
        self.work_cards = 0
        self.columns = 0
        self.mobile_lanes = 0
        self.management_elements = 0
        self.external_resources: list[str] = []
        self.scripts: list[str] = []
        self._in_script = False
        self._script_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(str(values["id"]))
        classes = set((values.get("class") or "").split())
        if tag == "button":
            self.buttons.append(values)
        if "work-card" in classes:
            self.work_cards += 1
        if "kanban-column" in classes:
            self.columns += 1
        if "mobile-lane" in classes:
            self.mobile_lanes += 1
        if "element-card" in classes:
            self.management_elements += 1
        for attribute in ("src", "href"):
            value = values.get(attribute)
            if value and not value.startswith("#"):
                self.external_resources.append(value)
        if tag == "script":
            self._in_script = True
            self._script_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._in_script:
            self.scripts.append("".join(self._script_parts))
            self._in_script = False

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._script_parts.append(data)


prototype = Path(__file__).with_name("status-dashboard-prototype.html")
payload = prototype.read_text(encoding="utf-8")
parser = PrototypeParser()
parser.feed(payload)
parser.close()

duplicate_ids = sorted(name for name, count in Counter(parser.ids).items() if count > 1)
buttons_without_type = [index for index, attrs in enumerate(parser.buttons) if attrs.get("type") != "button"]
assert not duplicate_ids, duplicate_ids
assert not buttons_without_type, buttons_without_type
assert parser.work_cards == 9, parser.work_cards
assert parser.columns == 5, parser.columns
assert parser.mobile_lanes == 5, parser.mobile_lanes
assert parser.management_elements == 10, parser.management_elements
assert not parser.external_resources, parser.external_resources
assert len(payload.encode("utf-8")) < 180_000
assert re.search(r"\{\{[A-Z0-9_]+\}\}", payload) is None
assert "@media(max-width:720px)" in payload
assert "@media(prefers-reduced-motion:reduce)" in payload
assert ":focus-visible" in payload
assert 'role="dialog"' in payload
assert 'aria-modal="true"' in payload
assert 'role="tablist"' in payload
assert 'aria-live="polite"' in payload
assert 'data-card-id="pm-dashboard-design"' in payload
assert 'data-lane="ready"' in payload
assert "fetch(" not in payload
assert ".factory/pm" not in payload
assert len(parser.scripts) == 1

management_element_ids = re.findall(r'data-element-id="([^"]+)"', payload)
assert len(management_element_ids) == 10, management_element_ids
assert len(set(management_element_ids)) == 10, management_element_ids
for management_element_id in management_element_ids:
    assert f'"{management_element_id}":{{element:true' in payload, management_element_id
assert 'document.querySelectorAll("[data-element-id]")' in payload
assert "openDrawerItem(item,button)" in payload

for management_element in (
    "项目成员",
    "项目策划",
    "WBS",
    "进度计划",
    "风险管理",
    "沟通计划",
    "会议与行动",
    "状态报告",
    "变更管理",
    "项目总结",
):
    assert management_element in payload, management_element

for template_field_group in (
    "成员 / 角色、项目角色、责任、RACI",
    "项目背景、项目目标、验收标准、假设、约束",
    "WBS、Work item、目标、输出、当前状态",
    "里程碑、目标、当前状态、下一动作",
    "风险 ID、标题、等级、状态、影响、缓解措施、责任人",
    "干系人、所需信息、频率、方法、责任人",
    "日期、主题、结论；行动、责任、状态",
    "当前状态、已完成、未完成、风险、下一步",
    "变更 ID、时间、标题、状态、原因、影响、批准人",
    "当前结论、有效做法、需要修正、后续判断",
):
    assert template_field_group in payload, template_field_group

node = "/Users/uroborus/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
syntax = subprocess.run(
    [node, "--check"],
    input=parser.scripts[0],
    text=True,
    capture_output=True,
    timeout=10,
    check=False,
)
assert syntax.returncode == 0, syntax.stderr

print(
    json.dumps(
        {
            "bytes": len(payload.encode("utf-8")),
            "unique_ids": len(parser.ids),
            "buttons": len(parser.buttons),
            "work_cards": parser.work_cards,
            "columns": parser.columns,
            "mobile_lanes": parser.mobile_lanes,
            "management_elements": parser.management_elements,
            "external_resources": parser.external_resources,
            "javascript_syntax": "passed",
            "accessibility_contract": "passed",
            "responsive_contract": "passed",
        },
        ensure_ascii=False,
        indent=2,
    )
)
