from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

from application.project_knowledge.site_service import ProjectSiteService
from runtime.project_artifacts.site_renderer import (
    ProjectArtifactSiteData,
    ProjectArtifactSiteRenderer,
)
from runtime.project_knowledge.site_renderer import site_input_token
from settings.project_knowledge.site_publisher import AtomicSitePublisher


def _model() -> dict[str, Any]:
    document_relation = {
        "direction": "outgoing",
        "relation_type": "CONTAINS",
        "strength": "strong",
        "entity_id": "DESIGN-ASSET-UX-UI-001",
        "entity_kind": "design_asset",
        "display_name": "项目只读站点 UX/UI 设计资产",
    }
    api_relation = {
        "direction": "outgoing",
        "relation_type": "CONTAINS",
        "strength": "strong",
        "entity_id": "API-HTTP-PROJECT-STATUS",
        "entity_kind": "api_operation",
        "display_name": "查询项目状态",
    }
    test_relation = {
        "direction": "incoming",
        "relation_type": "VERIFIES",
        "strength": "strong",
        "entity_id": "TEST-API-PROJECT-STATUS-001",
        "entity_kind": "test",
        "display_name": "项目状态接口合同校验",
    }
    return {
        "project": {"name": "Shanforge", "status": "in_progress", "completion": 50},
        "generation": {
            "generation_id": "generation:artifact-site",
            "source_manifest_sha256": "a" * 64,
            "pm_projection_sha256": "b" * 64,
        },
        "entities": [
            {
                "entity_id": "doc:DESIGN-UX-UI-001",
                "entity_kind": "document",
                "display_name": "UX/UI 设计",
                "summary": "面向只读项目站点的交互与视觉规范。",
                "lifecycle_status": "active",
                "details": {},
                "relations": [document_relation],
                "locators": [],
            },
            {
                "entity_id": "doc:DESIGN-API-001",
                "entity_kind": "document",
                "display_name": "API 设计",
                "summary": "接口用途、边界与机器合同。",
                "lifecycle_status": "active",
                "details": {},
                "relations": [api_relation, test_relation],
                "locators": [],
            },
            {
                "entity_id": "DESIGN-ASSET-UX-UI-001",
                "entity_kind": "design_asset",
                "display_name": "项目只读站点 UX/UI 设计资产",
                "summary": "等待连接真实 Penpot 文件",
                "lifecycle_status": "awaiting_penpot_connection",
                "details": {
                    "source_format": "penpot",
                    "source_file": None,
                    "connection_required": True,
                    "tokens_file": "design/ux-ui/tokens.json",
                },
                "relations": [
                    {
                        "direction": "outgoing",
                        "relation_type": "CONTAINS",
                        "strength": "strong",
                        "entity_id": "UI-PAGE-PROJECT-DASHBOARD",
                        "entity_kind": "ui_page",
                        "display_name": "项目任务看板",
                    }
                ],
                "locators": [],
            },
            {
                "entity_id": "UI-PAGE-PROJECT-DASHBOARD",
                "entity_kind": "ui_page",
                "display_name": "项目任务看板",
                "summary": "让负责人快速查看当前任务并进入详情。",
                "lifecycle_status": "awaiting_penpot_connection",
                "details": {"purpose": "让负责人快速查看当前任务并进入详情。"},
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "API-HTTP-PROJECT-STATUS",
                "entity_kind": "api_operation",
                "display_name": "查询项目状态",
                "summary": "读取指定项目的当前任务、进度和阻塞摘要。",
                "lifecycle_status": "active",
                "details": {
                    "method": "GET",
                    "path": "/projects/{project_id}/status",
                    "requirements": ["REQ-PKI-008"],
                    "tests": ["TEST-API-PROJECT-STATUS-001"],
                },
                "relations": [],
                "locators": [],
            },
            {
                "entity_id": "TEST-API-PROJECT-STATUS-001",
                "entity_kind": "test",
                "display_name": "项目状态接口合同校验",
                "summary": "确认项目状态接口具备中文说明和稳定追踪。",
                "lifecycle_status": "active",
                "details": {
                    "definition_status": "active",
                    "traceability": {
                        "requirements": ["REQ-PKI-008"],
                        "designs": ["DESIGN-API-001"],
                    },
                },
                "test": {
                    "test_status": "definition:active",
                    "last_evidence_entity_id": None,
                },
                "relations": [],
                "locators": [],
            },
        ],
        "documents": [
            {
                "document_id": "PRD",
                "title": "产品需求文档",
                "chinese_name": "产品需求文档",
                "audience": "产品、研发、测试",
                "owner": "Product",
                "doc_status": "active",
                "relative_path": "docs/04-product/prd.md",
                "sections": [],
                "content_markdown": "# 产品需求文档\n\n说明系统解决什么问题。",
            },
            {
                "document_id": "DESIGN-UX-UI-001",
                "title": "UX/UI 设计",
                "chinese_name": "UX/UI 设计",
                "audience": "产品、设计、前端",
                "owner": "Design",
                "doc_status": "candidate",
                "relative_path": "docs/05-design/ux-ui-design.md",
                "sections": [{"section_id": "overview", "display_title": "设计目标"}],
                "content_markdown": "# UX/UI 设计\n\n定义页面、组件、状态与视觉规范。",
            },
            {
                "document_id": "DESIGN-API-001",
                "title": "API 设计",
                "chinese_name": "API 设计",
                "audience": "前后端与集成方",
                "owner": "API",
                "doc_status": "candidate",
                "relative_path": "docs/05-design/api-design.md",
                "sections": [{"section_id": "http", "display_title": "HTTP API"}],
                "content_markdown": "# API 设计\n\n解释接口用途、边界和错误语义。",
            },
        ],
        "diagnostics": [],
        "versions": [],
        "pm": {},
    }


def test_renderer_has_one_project_document_entry_and_groups_documents() -> None:
    rendered = ProjectArtifactSiteRenderer().render(_model(), profile="local-owner")

    assert "documents/index.html" in rendered.pages
    assert not any(
        route == "design/index.html" or route.startswith("design/") for route in rendered.pages
    )
    combined = "\n".join(page for route, page in rendered.pages.items() if route.endswith(".html"))
    assert ">项目文档</a>" in combined
    assert ">设计</a>" not in combined
    assert 'href="../design/' not in combined
    documents = rendered.pages["documents/index.html"]
    assert "产品与需求" in documents
    assert "架构与设计" in documents
    assert "产品需求文档" in documents
    assert "UX/UI 设计" in documents


def test_document_details_combine_body_and_related_machine_artifacts() -> None:
    pages = ProjectArtifactSiteRenderer().render(_model(), profile="local-owner").pages
    ux_page = pages["documents/DESIGN-UX-UI-001.html"]
    api_page = pages["documents/DESIGN-API-001.html"]

    assert "定义页面、组件、状态与视觉规范。" in ux_page
    assert "适合谁看" in ux_page
    assert "artifact_id" not in ux_page
    assert "access_class" not in ux_page
    assert "关联机器附件" in ux_page
    assert "项目只读站点 UX/UI 设计资产" in ux_page
    assert "项目任务看板" in ux_page
    assert "等待在 Penpot 打开文件并连接插件" in ux_page
    assert 'href="design/ux-ui/' not in ux_page
    assert "design/ux-ui/tokens.json" in ux_page

    assert "查询项目状态" in api_page
    assert "GET /projects/{project_id}/status" in api_page
    assert "项目状态接口合同校验" in api_page
    assert "测试定义已登记 · 尚未执行" in api_page


def test_quality_page_never_presents_a_definition_as_a_passed_run() -> None:
    pages = ProjectArtifactSiteRenderer().render(_model(), profile="local-owner").pages

    assert "测试定义已登记 · 尚未执行" in pages["quality/index.html"]
    assert "测试定义已登记 · 尚未执行" in pages["quality/TEST-API-PROJECT-STATUS-001.html"]
    assert '<span class="status-chip">已通过</span>' not in pages["quality/index.html"]


def test_versioned_data_token_hits_cache_and_unchanged_document_hash_stays_stable(
    tmp_path: Path,
) -> None:
    model = _model()

    class Data:
        loads = 0

        def current_input_token(self, *, profile: str) -> str:
            return site_input_token(model["generation"], profile)

        def load(self, *, profile: str = "local-owner") -> dict[str, Any]:
            self.loads += 1
            return model

    source = Data()
    service = ProjectSiteService(
        ProjectArtifactSiteData(source),
        ProjectArtifactSiteRenderer(),
        AtomicSitePublisher(tmp_path / "site"),
    )
    first = service.snapshot(profile="local-owner", built_at="2026-07-23T00:00:00Z")
    second = service.snapshot(profile="local-owner", built_at="2026-07-23T00:00:01Z")

    assert first["cache_hit"] is False
    assert second["cache_hit"] is True
    assert source.loads == 1

    renderer = ProjectArtifactSiteRenderer()
    before = renderer.render(model, profile="local-owner")
    changed = deepcopy(model)
    changed["project"]["completion"] = 60
    after = renderer.render(changed, profile="local-owner")
    assert (
        before.page_fingerprints["documents/DESIGN-API-001.html"]
        == after.page_fingerprints["documents/DESIGN-API-001.html"]
    )
