"""Artifact-aware composition for the deterministic read-only project site."""

from __future__ import annotations

import hashlib
import html
import json
import re
from dataclasses import dataclass
from typing import Any

from application.project_knowledge.site_service import (
    RenderedSite,
    SiteDataPort,
)
from domain.project_knowledge.models import canonical_json
from domain.project_knowledge.sensitive_values import redact_text
from runtime.project_knowledge.site_renderer import (
    RENDERER_VERSION as BASE_RENDERER_VERSION,
)
from runtime.project_knowledge.site_renderer import ProjectSiteRenderer

RENDERER_VERSION = "ProjectArtifactSiteRenderer/v1"

_ATTACHMENT_KINDS = frozenset({"design_asset", "ui_page", "ui_component", "api_operation", "test"})
_ATTACHMENT_KIND_LABELS = {
    "design_asset": "UX/UI 设计源",
    "ui_page": "交互页面",
    "ui_component": "界面组件",
    "api_operation": "API 操作",
    "test": "测试定义",
}
_DOCUMENT_CATEGORIES = {
    "01-getting-started": ("01", "项目介绍与开始"),
    "02-user-guide": ("02", "用户指南"),
    "03-developer-guide": ("03", "开发者指南"),
    "04-product": ("04", "产品与需求"),
    "05-design": ("05", "架构与设计"),
    "06-delivery": ("06", "测试、发布与运维"),
}
_ARTIFACT_STYLES = """

.document-groups{display:grid;gap:1.25rem}
.document-group{border:1px solid var(--line);border-radius:16px;padding:1rem;
background:var(--surface)}
.document-group h2{margin-top:0}
.machine-attachments{margin-top:2rem;border-top:1px solid var(--line);padding-top:1.5rem}
.attachment-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}
.attachment-card{border:1px solid var(--line);border-radius:14px;padding:1rem;
background:var(--surface)}
.attachment-card h3{margin:.4rem 0}.attachment-card p{overflow-wrap:anywhere}
.attachment-meta{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center}
.attachment-kind{font-weight:700;color:var(--accent)}
.attachment-trace{margin:.75rem 0 0;padding-left:1.25rem}
.document-summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));
gap:.75rem;margin:1rem 0 1.5rem}
.document-summary-item{border:1px solid var(--line);border-radius:12px;padding:.85rem;
background:var(--surface)}
.document-summary-label{margin:0 0 .25rem;color:var(--muted);font-size:.82rem}
.document-summary-value{margin:0;font-weight:650;overflow-wrap:anywhere}
"""


def _safe(value: Any) -> str:
    return html.escape(redact_text("" if value is None else str(value)), quote=True)


def _route_id(value: Any) -> str:
    raw = str(value)
    if re.fullmatch(r"[A-Za-z0-9._~-]{1,120}", raw):
        return raw
    readable = re.sub(r"[^A-Za-z0-9._~-]+", "-", raw).strip("-")[:72] or "entity"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    return f"{readable}-{digest}"


def _versioned_token(base_token: str) -> str:
    return hashlib.sha256(
        canonical_json(
            {
                "renderer": RENDERER_VERSION,
                "base_renderer": BASE_RENDERER_VERSION,
                "base_input_token": base_token,
            }
        ).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class ProjectArtifactSiteData:
    """Version the existing read-only DTO token without rereading project sources."""

    delegate: SiteDataPort

    def current_input_token(self, *, profile: str) -> str:
        return _versioned_token(self.delegate.current_input_token(profile=profile))

    def load(self, *, profile: str = "local-owner") -> dict[str, Any]:
        return self.delegate.load(profile=profile)


def _document_category(document: dict[str, Any]) -> tuple[str, str]:
    relative_path = str(document.get("relative_path") or "")
    parts = relative_path.split("/")
    directory = parts[1] if len(parts) > 2 and parts[0] == "docs" else ""
    return _DOCUMENT_CATEGORIES.get(directory, ("99", "项目索引与其他文档"))


def _document_groups(documents: list[dict[str, Any]]) -> str:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for document in documents:
        if not str(document.get("relative_path") or "").startswith("docs/"):
            continue
        grouped.setdefault(_document_category(document), []).append(document)
    sections: list[str] = []
    for (_, label), items in sorted(grouped.items()):
        rows = []
        for document in sorted(
            items,
            key=lambda item: str(item.get("chinese_name") or item.get("title") or ""),
        ):
            document_id = str(document.get("document_id") or "")
            title = document.get("chinese_name") or document.get("title") or document_id
            audience = document.get("audience") or "未登记"
            owner = document.get("owner") or "未登记"
            status = document.get("doc_status") or "未登记"
            rows.append(
                '<li class="record-row"><div><a class="record-link" href="'
                f'{_safe(_route_id(document_id))}.html">{_safe(title)}</a>'
                f"<p>读者：{_safe(audience)} · Owner：{_safe(owner)}</p></div>"
                f'<span class="status-chip">{_safe(status)}</span></li>'
            )
        sections.append(
            f'<section class="document-group"><h2>{_safe(label)}</h2>'
            f'<ul class="record-list">{"".join(rows)}</ul></section>'
        )
    if not sections:
        return '<div class="empty"><strong>当前没有已登记项目文档</strong></div>'
    return '<div class="document-groups">' + "".join(sections) + "</div>"


def _document_summary(document: dict[str, Any]) -> str:
    _, category = _document_category(document)
    fields = (
        ("文档类别", category),
        ("适合谁看", document.get("audience") or "未登记"),
        ("负责人", document.get("owner") or "未登记"),
        ("当前状态", document.get("doc_status") or "未登记"),
        ("源文件", document.get("relative_path") or "未登记"),
    )
    return (
        '<div class="document-summary-grid">'
        + "".join(
            '<div class="document-summary-item">'
            f'<p class="document-summary-label">{_safe(label)}</p>'
            f'<p class="document-summary-value">{_safe(value)}</p></div>'
            for label, value in fields
        )
        + "</div>"
    )


def _related_attachments(
    document_id: str,
    entities: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_id = {str(entity.get("entity_id")): entity for entity in entities if entity.get("entity_id")}
    document = by_id.get(f"doc:{document_id}")
    if document is None:
        return []
    selected: dict[str, dict[str, Any]] = {}
    pending = [dict(relation) for relation in document.get("relations") or []]
    while pending:
        relation = pending.pop(0)
        entity_id = str(relation.get("entity_id") or "")
        entity = by_id.get(entity_id)
        if entity is None or str(entity.get("entity_kind")) not in _ATTACHMENT_KINDS:
            continue
        if entity_id in selected:
            continue
        selected[entity_id] = entity
        pending.extend(
            dict(child)
            for child in entity.get("relations") or []
            if child.get("direction") == "outgoing"
            and child.get("relation_type") == "CONTAINS"
            and child.get("strength") == "strong"
        )
    order = {
        "design_asset": 0,
        "ui_page": 1,
        "ui_component": 2,
        "api_operation": 3,
        "test": 4,
    }
    return sorted(
        selected.values(),
        key=lambda item: (
            order.get(str(item.get("entity_kind")), 99),
            str(item.get("display_name") or item.get("entity_id") or ""),
        ),
    )


def _attachment_status(item: dict[str, Any]) -> str:
    test = item.get("test")
    if isinstance(test, dict) and str(test.get("test_status") or "").startswith("definition:"):
        return "测试定义已登记 · 尚未执行"
    status = str(item.get("lifecycle_status") or "")
    return {
        "active": "已登记",
        "awaiting_penpot_connection": "等待连接 Penpot",
        "candidate": "候选",
        "deprecated": "已停用",
        "ready": "可使用",
    }.get(status, status.replace("_", " ") or "未登记")


def _trace_rows(item: dict[str, Any]) -> str:
    relations = [
        dict(relation)
        for relation in item.get("relations") or []
        if relation.get("relation_type") in {"SATISFIES", "VERIFIES"}
    ]
    if not relations:
        details = item.get("details")
        traceability = details.get("traceability") if isinstance(details, dict) else None
        if isinstance(traceability, dict):
            values = [
                str(target)
                for targets in traceability.values()
                if isinstance(targets, list)
                for target in targets
            ]
            if values:
                return (
                    '<ul class="attachment-trace">'
                    + "".join(f"<li>{_safe(value)}</li>" for value in values)
                    + "</ul>"
                )
        return ""
    return (
        '<ul class="attachment-trace">'
        + "".join(
            "<li>"
            f"{_safe(relation.get('relation_type'))} · "
            f"{_safe(relation.get('display_name') or relation.get('entity_id'))}"
            "</li>"
            for relation in relations
        )
        + "</ul>"
    )


def _attachment_card(item: dict[str, Any]) -> str:
    kind = str(item.get("entity_kind") or "")
    raw_details = item.get("details")
    details: dict[str, Any] = dict(raw_details) if isinstance(raw_details, dict) else {}
    entity_id = str(item.get("entity_id") or "")
    title = item.get("display_name") or entity_id
    purpose = (
        details.get("purpose")
        or details.get("objective")
        or item.get("summary")
        or "当前附件没有登记用途说明。"
    )
    specifics: list[str] = []
    if kind == "design_asset":
        source_file = details.get("source_file")
        if source_file:
            specifics.append(f"设计源：<code>{_safe(source_file)}</code>")
        elif details.get("connection_required"):
            specifics.append("设计源：等待在 Penpot 打开文件并连接插件")
        if details.get("tokens_file"):
            specifics.append(f"设计 Token：<code>{_safe(details['tokens_file'])}</code>")
    elif kind == "api_operation":
        method = str(details.get("method") or "")
        path = str(details.get("path") or "")
        if method or path:
            specifics.append(f"接口：<code>{_safe(f'{method} {path}'.strip())}</code>")
    elif kind == "test":
        specifics.append("执行结果：尚无已验证的运行证据")
    details_html = "".join(f"<p>{value}</p>" for value in specifics)
    return (
        '<div class="attachment-card">'
        '<div class="attachment-meta">'
        f'<span class="attachment-kind">{_safe(_ATTACHMENT_KIND_LABELS.get(kind, kind))}</span>'
        f'<span class="status-chip">{_safe(_attachment_status(item))}</span></div>'
        f"<h3>{_safe(title)}</h3><p>{_safe(purpose)}</p>"
        f"<p>稳定 ID：<code>{_safe(entity_id)}</code></p>"
        + details_html
        + _trace_rows(item)
        + "</div>"
    )


def _attachment_section(attachments: list[dict[str, Any]]) -> str:
    if not attachments:
        return (
            '<section class="machine-attachments"><h2>关联机器附件</h2>'
            '<p class="missing-state">当前文档没有通过索引关系绑定机器附件。</p></section>'
        )
    return (
        '<section class="machine-attachments"><h2>关联机器附件</h2>'
        "<p>以下内容来自 SQLite 当前索引关系；文档仍是人类说明入口，机器附件负责可执行合同。</p>"
        '<div class="attachment-grid">'
        + "".join(_attachment_card(item) for item in attachments)
        + "</div></section>"
    )


def _rewrite_navigation_and_links(page: str) -> str:
    page = re.sub(
        r'<a href="([^"]*?)design/index\.html">设计</a>',
        "",
        page,
    )
    page = re.sub(
        r'<a href="([^"]*?documents/index\.html)">文档</a>',
        r'<a href="\1">项目文档</a>',
        page,
    )
    page = re.sub(
        r'href="([^"]*?)design/([^"]+\.html)"',
        r'href="\1documents/\2"',
        page,
    )
    return page


class ProjectArtifactSiteRenderer:
    """Compose human documents and indexed machine attachments into one site."""

    def __init__(self, base: ProjectSiteRenderer | None = None) -> None:
        self._base = base or ProjectSiteRenderer()

    def render(
        self,
        model: dict[str, Any],
        *,
        profile: str,
        previous: dict[str, object] | None = None,
    ) -> RenderedSite:
        render_model = dict(model)
        entities: list[dict[str, Any]] = []
        for raw_entity in model.get("entities") or []:
            entity = dict(raw_entity)
            raw_test = entity.get("test")
            if isinstance(raw_test, dict):
                test = dict(raw_test)
                if str(test.get("test_status") or "").startswith("definition:"):
                    readable = "测试定义已登记 · 尚未执行"
                    entity["lifecycle_status"] = readable
                    test["test_status"] = readable
                entity["test"] = test
            entities.append(entity)
        render_model["entities"] = entities
        base_previous: dict[str, object] | None = None
        if previous is not None:
            raw_pages = previous.get("pages")
            base_previous = {
                "pages": raw_pages if isinstance(raw_pages, dict) else {},
                # Wrapper-level attachments and global navigation affect every detail page.
                "page_inputs": {},
            }
        rendered = self._base.render(
            render_model,
            profile=profile,
            previous=base_previous,
        )
        pages = {
            route: content
            for route, content in rendered.pages.items()
            if route != "design/index.html" and not route.startswith("design/")
        }
        documents = [
            dict(document)
            for document in model.get("documents") or []
            if str(document.get("relative_path") or "").startswith("docs/")
        ]
        documents_index = pages.get("documents/index.html")
        if documents_index is not None:
            documents_index = documents_index.replace("人类文档目录", "项目文档")
            documents_index = re.sub(
                r'<ul class="record-list">.*?</ul>',
                _document_groups(documents),
                documents_index,
                count=1,
                flags=re.DOTALL,
            )
            pages["documents/index.html"] = documents_index
        for document in documents:
            document_id = str(document.get("document_id") or "")
            route = f"documents/{_route_id(document_id)}.html"
            page = pages.get(route)
            if page is None:
                continue
            page = re.sub(
                r'<dl class="definition-grid">.*?</dl>',
                _document_summary(document),
                page,
                count=1,
                flags=re.DOTALL,
            )
            section = _attachment_section(_related_attachments(document_id, entities))
            pages[route] = (
                page.rsplit("</article>", 1)[0]
                + section
                + "</article>"
                + page.rsplit("</article>", 1)[1]
            )
        for route, page in tuple(pages.items()):
            if route.endswith(".html"):
                pages[route] = _rewrite_navigation_and_links(page)
        pages["assets/styles.css"] = pages.get("assets/styles.css", "") + _ARTIFACT_STYLES
        if "assets/snapshot.js" in pages:
            pages["assets/snapshot.js"] = pages["assets/snapshot.js"].replace(
                BASE_RENDERER_VERSION,
                RENDERER_VERSION,
            )
        fingerprints = {
            route: hashlib.sha256(content.encode("utf-8")).hexdigest()
            for route, content in pages.items()
        }
        page_inputs = {
            route: hashlib.sha256(f"{RENDERER_VERSION}:{value}".encode("utf-8")).hexdigest()
            for route, value in rendered.page_input_fingerprints.items()
            if route in fingerprints
        }
        site_fingerprint = hashlib.sha256(
            canonical_json(
                {
                    "renderer": RENDERER_VERSION,
                    "profile": profile,
                    "pages": sorted(fingerprints.items()),
                }
            ).encode("utf-8")
        ).hexdigest()
        return RenderedSite(
            pages=pages,
            page_fingerprints=fingerprints,
            page_input_fingerprints=page_inputs,
            site_fingerprint=site_fingerprint,
            input_token=_versioned_token(rendered.input_token),
            generation_id=rendered.generation_id,
        )


def manifest_json(rendered: RenderedSite) -> str:
    """Small deterministic inspection helper for tests and diagnostics."""

    return json.dumps(
        {
            "renderer": RENDERER_VERSION,
            "input_token": rendered.input_token,
            "site_fingerprint": rendered.site_fingerprint,
            "pages": rendered.page_fingerprints,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
