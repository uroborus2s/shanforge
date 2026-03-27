#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import textwrap
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

import fcntl


FACTORY_DIR_RELATIVE = ".factory"
FACTORY_MEMORY_RELATIVE = f"{FACTORY_DIR_RELATIVE}/memory"
FACTORY_PROCESS_RELATIVE = f"{FACTORY_DIR_RELATIVE}/process"
FACTORY_WORKITEMS_RELATIVE = f"{FACTORY_DIR_RELATIVE}/workitems"


def memory_file(*parts: str) -> str:
    cleaned = [part.strip("/") for part in parts if part.strip("/")]
    return "/".join([FACTORY_MEMORY_RELATIVE, *cleaned])


def process_file(*parts: str) -> str:
    cleaned = [part.strip("/") for part in parts if part.strip("/")]
    return "/".join([FACTORY_PROCESS_RELATIVE, *cleaned])


def workitems_file(*parts: str) -> str:
    cleaned = [part.strip("/") for part in parts if part.strip("/")]
    return "/".join([FACTORY_WORKITEMS_RELATIVE, *cleaned])


PROJECT_CONFIG_RELATIVE = f"{FACTORY_DIR_RELATIVE}/project.json"
PROJECT_LOCK_RELATIVE = f"{FACTORY_DIR_RELATIVE}/project.lock"
PR_STATE_RELATIVE = f"{FACTORY_DIR_RELATIVE}/prs.json"
TECH_PROFILE_STATE_RELATIVE = f"{FACTORY_DIR_RELATIVE}/tech-profile.json"
DESIGN_ASSET_STATE_RELATIVE = f"{FACTORY_DIR_RELATIVE}/design-assets.json"
PROJECT_INDEX_RELATIVE = memory_file("project-index.md")
CURRENT_STATE_RELATIVE = memory_file("current-state.md")
TASKS_SUMMARY_RELATIVE = memory_file("tasks.summary.md")
CHANGE_SUMMARY_RELATIVE = memory_file("change-summary.md")
AGENT_SESSION_RELATIVE = memory_file("agent-session.md")
TECH_STACK_SUMMARY_RELATIVE = memory_file("tech-stack.summary.md")
DESIGN_ASSETS_SUMMARY_RELATIVE = memory_file("design-assets.summary.md")
PR_SUMMARY_RELATIVE = memory_file("pr.summary.md")
PR_BOARD_SUMMARY_RELATIVE = memory_file("pr-board.summary.md")
PR_CHECK_SUMMARY_RELATIVE = memory_file("pr-check.summary.md")
PR_HANDOVER_SUMMARY_RELATIVE = memory_file("pr-handover.summary.md")
REMOTE_PR_SUMMARY_RELATIVE = memory_file("remote-pr.summary.md")
TRACEABILITY_GRAPH_RELATIVE = memory_file("graph", "traceability.json")
EXECUTION_LOG_RELATIVE = process_file("execution-log.md")
DAILY_STATUS_RELATIVE = process_file("daily-status.md")
RISK_REGISTER_RELATIVE = process_file("risk-register.md")
PULL_REQUESTS_RELATIVE = process_file("pull-requests.md")
PR_BOARD_RELATIVE = process_file("pr-board.md")
PR_HANDOVERS_RELATIVE = process_file("pr-handovers.md")
REMOTE_PRS_RELATIVE = process_file("remote-prs.md")
MULTI_AGENT_BOARD_RELATIVE = process_file("multi-agent-board.md")
ROLE_ASSIGNMENTS_RELATIVE = process_file("role-assignments.md")
ROLE_HANDOFFS_RELATIVE = process_file("role-handoffs.md")
ROLE_SYNC_RELATIVE = process_file("role-sync.md")
TEAM_SYNC_RELATIVE = process_file("team-sync.md")
TEAM_ENERGY_RELATIVE = process_file("team-energy.md")
AGENT_ACHIEVEMENTS_RELATIVE = process_file("agent-achievements.md")
RECOVERY_REVIEW_RELATIVE = process_file("recovery-review.md")
PATTERN_FIX_REPORT_RELATIVE = process_file("pattern-fix-report.md")
CHAT_BOOTSTRAP_RELATIVE = process_file("chat-bootstrap.md")
TEAM_RETRO_RELATIVE = process_file("team-retro.md")
PR_CHECK_REPORT_RELATIVE = process_file("pr-check-report.md")
STAGE_CHECK_REPORT_RELATIVE = process_file("stage-check-report.md")
QUALITY_CHECK_REPORT_RELATIVE = process_file("quality-check-report.md")
STATE_DOCTOR_REPORT_RELATIVE = process_file("state-doctor-report.md")
ROLE_REVIEWS_RELATIVE = process_file("role-reviews.md")
ROLE_CLOSEOUTS_RELATIVE = process_file("role-closeouts.md")
TEAM_CLOSEOUTS_RELATIVE = process_file("team-closeouts.md")
ROLE_RETROSPECTIVES_RELATIVE = process_file("role-retrospectives")
ROLE_WORKBENCHES_RELATIVE = process_file("role-workbenches")
MOTIVATION_STATE_RELATIVE = memory_file("motivation-state.md")
AUTONOMY_RULES_RELATIVE = memory_file("autonomy-rules.md")
RECOVERY_PLAYBOOK_RELATIVE = memory_file("recovery-playbook.md")
EVOLUTION_BASELINE_RELATIVE = memory_file("evolution-baseline.md")
PATTERN_FIX_SUMMARY_RELATIVE = memory_file("pattern-fix.summary.md")
PROJECT_LOCK_ENV = "FACTORY_PROJECT_LOCK_ACTIVE"
DEFAULT_LOCK_TIMEOUT_SECONDS = 60.0
ITEM_FILE_LOCATIONS = {
    "TASK-": workitems_file("implementation"),
    "CR-": workitems_file("changes"),
    "BUG-": workitems_file("bugs"),
}
DEFAULT_ITEM_SPECS: Sequence[tuple[str, str]] = (
    (workitems_file("implementation"), "TASK"),
    (workitems_file("changes"), "CR"),
    (workitems_file("bugs"), "BUG"),
)
DEFAULT_FIELD_PATTERNS = {
    "id": re.compile(r"^- 编号：(.*)$"),
    "type": re.compile(r"^- 类型：(.*)$"),
    "status": re.compile(r"^- 状态：(.*)$"),
    "priority": re.compile(r"^- 优先级：(.*)$"),
    "owner": re.compile(r"^- 负责人：(.*)$"),
    "hours": re.compile(r"^- 预估总(?:人天|工时)：(.*)$"),
    "links": re.compile(r"^- 关联项：(.*)$"),
    "created_at": re.compile(r"^- 创建日期：(.*)$"),
}
WORK_BLOCK_ROW_PATTERN = re.compile(r"^\|\s*(WB-[^|]+)\s*\|\s*(.*?)\s*\|\s*([0-9]+(?:\.[0-9]+)?)\s*(?:人天|h)\s*\|\s*(.*?)\s*\|$")
WORK_BLOCK_PLACEHOLDER_PATTERN = re.compile(r"^补充工作块\s+\d+$")
HOURS_PER_PERSON_DAY = 8.0
MIN_EFFORT_DAYS = 0.5
CLOSED_STATUSES = {"已完成", "已关闭", "已取消", "已驳回"}
CLOSED_RISK_STATUSES = {"已关闭", "已接受", "已消除"}
MERGED_PR_STATUSES = {"merged"}
ACTIVE_PR_STATUSES = {"draft", "open", "reviewing", "changes_requested", "approved", "blocked"}
TECH_PROFILE_PRESETS = {
    "nodejs-backend": {
        "id": "nodejs-backend",
        "title": "Node.js 后端画像",
        "stack": "nodejs backend",
        "summary": "适用于 Node.js 服务端项目，强调接口契约、模块边界、测试和交付文档同步。",
        "projects": ["业务后端服务工程"],
        "modules": ["Node.js 运行时", "包管理器", "测试与回归验证模块", "日志与配置模块"],
        "rules": [
            "进入实施前先明确目录结构、配置管理、错误处理和日志规范。",
            "所有接口和模块改动同时更新 technical-selection、api-design、backend-design、test-plan。",
            "PR 评审时检查环境变量、依赖安装和测试脚本是否齐全。",
        ],
        "admin_requirements": [],
        "commands": ["初始化 Node.js 后端工程骨架并登记依赖清单。"],
        "guides": [],
        "required_skills": ["backend-patterns", "api-design", "tdd-workflow"],
        "role_required_skills": {
            "solution-architect": ["backend-patterns", "api-design"],
            "backend-engineer": ["backend-patterns", "api-design", "tdd-workflow"],
            "qa-engineer": ["tdd-workflow"],
        },
    },
    "react-admin-web": {
        "id": "react-admin-web",
        "title": "React 管理后台画像",
        "stack": "react admin web",
        "summary": "适用于 React 管理后台项目，强调页面状态、权限模型、组件规范和可访问性。",
        "projects": ["管理后台工程"],
        "modules": ["React 工程", "路由与状态管理模块", "UI 组件库", "测试模块"],
        "rules": [
            "先定义页面清单、权限模型、导航结构和接口依赖，再进入页面实现。",
            "关键页面必须有直观可查看的设计交付物，不仅停留在文字说明。",
            "PR 评审时检查组件复用、状态管理、交互边界和回归测试。",
        ],
        "admin_requirements": [
            "明确后台菜单、页面、权限点和接口映射。",
            "明确管理端操作日志、异常反馈和数据导出等需求。",
        ],
        "commands": ["初始化 React 管理后台工程并登记页面/权限基线。"],
        "guides": [],
        "required_skills": ["frontend-patterns", "ui-ux-pro-max", "tdd-workflow"],
        "role_required_skills": {
            "ux-designer": ["ui-ux-pro-max", "frontend-patterns"],
            "frontend-engineer": ["frontend-patterns", "ui-ux-pro-max", "tdd-workflow"],
            "qa-engineer": ["tdd-workflow", "webapp-testing"],
        },
    },
    "golang-backend": {
        "id": "golang-backend",
        "title": "Golang 后端画像",
        "stack": "golang backend",
        "summary": "适用于 Go 后端项目，强调接口契约、并发安全、工程结构和测试。",
        "projects": ["业务后端服务工程"],
        "modules": ["Go 工程", "配置与日志模块", "测试模块"],
        "rules": [
            "进入实施前先明确包结构、依赖管理、配置方式和并发边界。",
            "当前全局无 Go 专用 skill 时，至少复用 API 设计、测试和通用后端约束。",
            "PR 评审时检查接口契约、错误处理、配置项和测试是否同步。",
        ],
        "admin_requirements": [],
        "commands": ["初始化 Go 服务工程并登记依赖、配置与启动方式。"],
        "guides": [],
        "required_skills": ["api-design", "tdd-workflow"],
        "role_required_skills": {
            "solution-architect": ["api-design"],
            "backend-engineer": ["api-design", "tdd-workflow"],
            "qa-engineer": ["tdd-workflow"],
        },
    },
    "python-backend": {
        "id": "python-backend",
        "title": "Python 后端画像",
        "stack": "python backend",
        "summary": "适用于 Python 服务端或 CLI/任务型工程，统一使用 uv 管理 Python 版本、虚拟环境、依赖、锁文件和工具执行，强调 pyproject、类型标注、测试与文档同步。",
        "projects": ["业务后端服务工程", "CLI/任务执行工程"],
        "modules": ["Python 3.11+", "uv", "pytest", "ruff", "mypy"],
        "rules": [
            "统一使用 uv 管理 Python 版本、虚拟环境、依赖、锁文件和工具执行，不把 pip、Poetry、Pipenv、requirements.txt 当作主工作流。",
            "项目元数据、依赖和工具配置统一收敛到 pyproject.toml，提交 uv.lock，不提交 .venv。",
            "新增或修改 Python 代码默认补类型标注，并通过 uv run ruff format、uv run ruff check、uv run mypy、uv run pytest 验证。",
            "接口、模块、配置或部署行为变更时，同时更新 technical-selection、backend-design、api-design、test-plan 和 deployment-guide。",
        ],
        "admin_requirements": [],
        "commands": [
            "优先执行 uv python install 与 uv sync，使用 uv add / uv add --dev 管理依赖。",
            "新项目优先建立 pyproject.toml、uv.lock、src/、tests/ 和 scripts/ 结构。",
        ],
        "guides": [
            "skills/python-uv-project/SKILL.md",
            "skills/python-uv-project/references/pyproject.template.toml",
        ],
        "required_skills": ["python-uv-project", "backend-patterns", "api-design", "tdd-workflow"],
        "role_required_skills": {
            "solution-architect": ["python-uv-project", "backend-patterns", "api-design"],
            "backend-engineer": ["python-uv-project", "backend-patterns", "api-design", "tdd-workflow"],
            "qa-engineer": ["python-uv-project", "tdd-workflow"],
        },
    },
    "stratix-admin": {
        "id": "stratix-admin",
        "title": "Stratix 后端 + 管理后台画像",
        "stack": "nodejs + stratix + admin-web",
        "summary": "适用于采用 Stratix 生态实现业务后端，并同步交付管理后台的项目。",
        "projects": [
            "业务后端服务工程",
            "管理后台工程",
        ],
        "modules": [
            "@stratix/core",
            "数据库访问能力模块（按项目实际驱动选型）",
            "测试与回归验证能力模块",
            "后台管理端基础工程模块",
        ],
        "rules": [
            "进入实施前，先明确 stratix.config.ts、自动发现、依赖注入和模块注册方案。",
            "后端代码按控制器、服务、仓储、执行器等 Stratix 约定分层，不直接把业务逻辑堆在路由层。",
            "新增模块、插件和后台管理端页面时，同时更新 technical-selection、backend-design、api-design 和 test-plan。",
            "管理后台不是可选附属物；若需求涉及运营配置、审核、统计或人工处理流程，必须明确后台范围、菜单、权限点和接口映射。",
            "PR 评审时必须检查 Stratix 约定、模块安装清单、环境变量和后台管理端联动是否完整。",
        ],
        "admin_requirements": [
            "明确后台管理端的仓库位置、技术栈和初始化方式。",
            "列出后台菜单、页面、权限点、接口依赖和联调顺序。",
            "为后台管理端补齐部署、使用和验收说明。",
        ],
        "commands": [
            "创建后端工程初始化清单，确认 Stratix 核心模块与插件选型。",
            "创建管理后台工程初始化清单，并登记环境变量、权限模型和菜单规划。",
        ],
        "guides": [],
        "required_skills": ["backend-patterns", "api-design", "frontend-patterns", "ui-ux-pro-max", "tdd-workflow"],
        "role_required_skills": {
            "solution-architect": ["backend-patterns", "api-design"],
            "ux-designer": ["ui-ux-pro-max", "frontend-patterns"],
            "backend-engineer": ["backend-patterns", "api-design", "tdd-workflow"],
            "frontend-engineer": ["frontend-patterns", "ui-ux-pro-max", "tdd-workflow"],
            "qa-engineer": ["tdd-workflow", "webapp-testing"],
        },
    },
}
STAGE_REFERENCE_DOCS = {
    "BRAINSTORM": [
        "docs/00-governance/project-charter.md",
        "docs/01-discovery/input.md",
        "docs/01-discovery/brainstorm-record.md",
    ],
    "REQUIREMENTS": [
        "docs/02-requirements/prd.md",
        "docs/02-requirements/requirements-analysis.md",
        "docs/02-requirements/requirements-verification.md",
    ],
    "ANALYSIS": [
        "docs/02-requirements/requirements-analysis.md",
        "docs/02-requirements/requirements-verification.md",
        "docs/traceability/requirements-matrix.md",
    ],
    "DESIGN": [
        "docs/03-solution/system-architecture.md",
        "docs/03-solution/technical-selection.md",
        "docs/03-solution/module-boundaries.md",
        "docs/03-solution/api-design.md",
        "docs/03-solution/backend-design.md",
        "docs/03-solution/database-design.md",
        "docs/03-solution/ux-ui-design.md",
    ],
    "PLAN": [
        "docs/03-solution/technical-selection.md",
        "docs/03-solution/module-boundaries.md",
        "docs/04-delivery/wbs.md",
        "docs/04-delivery/task-breakdown.md",
        "docs/04-delivery/implementation-plan.md",
    ],
    "IMPLEMENTATION": [
        "docs/03-solution/technical-selection.md",
        "docs/03-solution/module-boundaries.md",
        EXECUTION_LOG_RELATIVE,
        "docs/05-quality/test-plan.md",
    ],
    "TESTING": [
        "docs/05-quality/test-plan.md",
        "docs/05-quality/test-cases.md",
        "docs/05-quality/test-report.md",
    ],
    "ACCEPTANCE": [
        "docs/06-release/acceptance-checklist.md",
        "docs/06-release/delivery-package.md",
        STAGE_CHECK_REPORT_RELATIVE,
        QUALITY_CHECK_REPORT_RELATIVE,
    ],
    "RELEASE": [
        "docs/06-release/release-notes.md",
        "docs/06-release/delivery-package.md",
        "docs/07-operations/deployment-guide.md",
        "docs/08-handover/user-guide.md",
    ],
    "MAINTENANCE": [
        "docs/07-operations/operations-runbook.md",
        "docs/08-handover/user-guide.md",
        "docs/09-evolution/retrospective.md",
        "docs/traceability/requirements-matrix.md",
    ],
}
DEFAULT_ROLE_SPECS = (
    {
        "id": "coordinator",
        "title": "项目协调者",
        "aliases": ["项目经理", "会话协调者", "pm", "coordinator"],
        "description": "负责阶段推进、跨角色协作、审批门禁和交接节奏控制。",
        "stages": ["BRAINSTORM", "REQUIREMENTS", "ANALYSIS", "DESIGN", "PLAN", "IMPLEMENTATION", "TESTING", "ACCEPTANCE", "RELEASE", "MAINTENANCE"],
        "preferred_tools": ["codex", "gemini"],
        "skill_names": ["brainstorming", "document-templates", "doc-coauthoring"],
        "docs": [
        "docs/03-solution/technical-selection.md",
        MULTI_AGENT_BOARD_RELATIVE,
        ROLE_HANDOFFS_RELATIVE,
        EXECUTION_LOG_RELATIVE,
        CHAT_BOOTSTRAP_RELATIVE,
        ],
    },
    {
        "id": "requirements-analyst",
        "title": "需求分析师",
        "aliases": ["需求负责人", "ba", "analyst", "requirements"],
        "description": "负责澄清目标、拆解需求、补齐 REQ/NFR、维护需求一致性。",
        "stages": ["BRAINSTORM", "REQUIREMENTS", "ANALYSIS"],
        "preferred_tools": ["gemini", "codex"],
        "skill_names": ["brainstorming", "requirements-engineering", "document-templates", "doc-coauthoring"],
        "docs": [
            "docs/00-governance/project-charter.md",
            "docs/01-discovery/input.md",
            "docs/01-discovery/brainstorm-record.md",
            "docs/02-requirements/prd.md",
            "docs/02-requirements/requirements-analysis.md",
            "docs/02-requirements/requirements-verification.md",
            "docs/traceability/requirements-matrix.md",
        ],
    },
    {
        "id": "solution-architect",
        "title": "解决方案架构师",
        "aliases": ["架构负责人", "architect", "solution"],
        "description": "负责系统拆分、接口契约、后端边界和技术风险控制。",
        "stages": ["ANALYSIS", "DESIGN", "PLAN"],
        "preferred_tools": ["gemini", "codex"],
        "skill_names": ["api-design", "backend-patterns", "frontend-patterns", "doc-coauthoring"],
        "docs": [
            "docs/03-solution/technical-selection.md",
            "docs/03-solution/system-architecture.md",
            "docs/03-solution/module-boundaries.md",
            "docs/03-solution/api-design.md",
            "docs/03-solution/backend-design.md",
            "docs/03-solution/database-design.md",
            "docs/traceability/requirements-matrix.md",
        ],
    },
    {
        "id": "ux-designer",
        "title": "UX/UI 设计师",
        "aliases": ["设计负责人", "designer", "ux", "ui"],
        "description": "负责用户流程、界面结构、交互状态与体验一致性。",
        "stages": ["DESIGN", "PLAN"],
        "preferred_tools": ["gemini", "codex"],
        "skill_names": ["ui-ux-pro-max", "frontend-patterns", "doc-coauthoring"],
        "docs": [
            "docs/03-solution/technical-selection.md",
            "docs/03-solution/ux-ui-design.md",
            "docs/03-solution/assets/README.md",
            "docs/03-solution/system-architecture.md",
            "docs/03-solution/module-boundaries.md",
            "docs/04-delivery/wbs.md",
        ],
    },
    {
        "id": "backend-engineer",
        "title": "后端工程师",
        "aliases": ["后端负责人", "backend", "server", "codex-backend"],
        "description": "负责服务实现、接口落地、数据一致性和工程化执行。",
        "stages": ["PLAN", "IMPLEMENTATION", "TESTING"],
        "preferred_tools": ["codex", "gemini"],
        "skill_names": ["backend-patterns", "api-design", "tdd-workflow"],
        "docs": [
            "docs/03-solution/technical-selection.md",
            "docs/03-solution/module-boundaries.md",
        "docs/03-solution/backend-design.md",
        "docs/03-solution/api-design.md",
        "docs/04-delivery/implementation-plan.md",
        EXECUTION_LOG_RELATIVE,
        "docs/05-quality/test-plan.md",
        ],
    },
    {
        "id": "frontend-engineer",
        "title": "前端工程师",
        "aliases": ["前端负责人", "frontend", "web", "codex-frontend"],
        "description": "负责界面实现、交互联调、前端状态管理和可访问性。",
        "stages": ["PLAN", "IMPLEMENTATION", "TESTING"],
        "preferred_tools": ["codex", "gemini"],
        "skill_names": ["frontend-patterns", "ui-ux-pro-max", "tdd-workflow"],
        "docs": [
            "docs/03-solution/technical-selection.md",
        "docs/03-solution/ux-ui-design.md",
        "docs/03-solution/system-architecture.md",
        "docs/04-delivery/implementation-plan.md",
        EXECUTION_LOG_RELATIVE,
        "docs/05-quality/test-plan.md",
        ],
    },
    {
        "id": "qa-engineer",
        "title": "测试工程师",
        "aliases": ["质量负责人", "qa", "tester", "quality"],
        "description": "负责测试计划、回归验证、Gate 前检查和质量风险暴露。",
        "stages": ["IMPLEMENTATION", "TESTING", "ACCEPTANCE"],
        "preferred_tools": ["codex", "gemini"],
        "skill_names": ["tdd-workflow", "webapp-testing", "document-templates"],
        "docs": [
        "docs/05-quality/test-plan.md",
        "docs/05-quality/test-cases.md",
        "docs/05-quality/test-report.md",
        STAGE_CHECK_REPORT_RELATIVE,
        QUALITY_CHECK_REPORT_RELATIVE,
        "docs/traceability/requirements-matrix.md",
        ],
    },
    {
        "id": "release-manager",
        "title": "发布经理",
        "aliases": ["发布负责人", "release", "ops", "handover"],
        "description": "负责交付说明、部署运行、发布准备和交接闭环。",
        "stages": ["ACCEPTANCE", "RELEASE", "MAINTENANCE"],
        "preferred_tools": ["gemini", "codex"],
        "skill_names": ["document-templates", "doc-coauthoring"],
        "docs": [
            "docs/06-release/delivery-package.md",
            "docs/06-release/release-notes.md",
            "docs/07-operations/deployment-guide.md",
            "docs/08-handover/user-guide.md",
            "docs/08-handover/admin-guide.md",
        ],
    },
    {
        "id": "memory-manager",
        "title": "文档与记忆管理员",
        "aliases": ["memory", "ai-memory", "文档管理员", "记忆管理员"],
        "description": "负责人类文档与 AI 记忆同步、摘要收敛和项目上下文恢复。",
        "stages": ["BRAINSTORM", "REQUIREMENTS", "ANALYSIS", "DESIGN", "PLAN", "IMPLEMENTATION", "TESTING", "ACCEPTANCE", "RELEASE", "MAINTENANCE"],
        "preferred_tools": ["gemini", "codex"],
        "skill_names": ["document-templates", "doc-coauthoring"],
        "docs": [
            PROJECT_INDEX_RELATIVE,
            CURRENT_STATE_RELATIVE,
            TASKS_SUMMARY_RELATIVE,
            CHANGE_SUMMARY_RELATIVE,
            AGENT_SESSION_RELATIVE,
            DAILY_STATUS_RELATIVE,
            ROLE_HANDOFFS_RELATIVE,
            "docs/traceability/requirements-matrix.md",
        ],
    },
)


def normalize_key(value: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", value.lower())


def shared_skill_lookup(shared_skills: Sequence[dict] | dict) -> dict[str, dict]:
    source = shared_skills.get("shared_skills", []) if isinstance(shared_skills, dict) else shared_skills
    return {
        item.get("name", ""): item
        for item in source
        if isinstance(item, dict) and item.get("name")
    }


def build_default_roles(shared_skills: Sequence[dict] | dict) -> list[dict]:
    skill_map = shared_skill_lookup(shared_skills)
    roles: list[dict] = []
    for spec in DEFAULT_ROLE_SPECS:
        role = {
            "id": spec["id"],
            "title": spec["title"],
            "aliases": list(spec.get("aliases", [])),
            "description": spec["description"],
            "stages": list(spec.get("stages", [])),
            "preferred_tools": list(spec.get("preferred_tools", [])),
            "docs": list(spec.get("docs", [])),
            "skill_names": list(spec.get("skill_names", [])),
            "skills": [
                skill_map[name]
                for name in spec.get("skill_names", [])
                if name in skill_map
            ],
        }
        roles.append(role)
    return roles


def ensure_role_catalog(config: dict) -> list[dict]:
    roles = config.get("roles")
    if roles:
        return roles
    roles = build_default_roles(config.get("shared_skills", []))
    config["roles"] = roles
    return roles


def resolve_role(config: dict, query: str | None, default_id: str = "coordinator") -> dict:
    roles = ensure_role_catalog(config)
    normalized = normalize_key(query or default_id)
    for role in roles:
        candidates = [role.get("id", ""), role.get("title", ""), *role.get("aliases", [])]
        if normalized in {normalize_key(item) for item in candidates if item}:
            return role
    for role in roles:
        if role.get("id") == default_id:
            return role
    raise RuntimeError(f"未找到角色：{query or default_id}")


def active_roles_for_stage(config: dict, stage: str | None = None) -> list[dict]:
    roles = ensure_role_catalog(config)
    current_stage = stage or config.get("stage", "")
    active = [role for role in roles if current_stage in role.get("stages", [])]
    return active or roles


def selected_roles(config: dict, raw_roles: str | None = None, *, stage: str | None = None) -> list[dict]:
    requested = parse_list(raw_roles or "")
    if not requested:
        return active_roles_for_stage(config, stage)

    resolved: list[dict] = []
    seen = set()
    for query in requested:
        role = resolve_role(config, query)
        role_id = role.get("id", "")
        if role_id in seen:
            continue
        seen.add(role_id)
        resolved.append(role)
    return resolved


def role_titles(config: dict, stage: str | None = None) -> list[str]:
    return [role.get("title", role.get("id", "未知角色")) for role in active_roles_for_stage(config, stage)]


def ensure_role_assignment_state(config: dict) -> dict[str, dict]:
    assignments = config.get("current_role_assignments")
    if isinstance(assignments, dict):
        return assignments
    assignments = {}
    history = config.get("role_assignments", [])
    if isinstance(history, list):
        for entry in history:
            if not isinstance(entry, dict):
                continue
            role_id = entry.get("role")
            if role_id:
                assignments[role_id] = {
                    "owner": entry.get("owner", ""),
                    "tool": entry.get("tool", ""),
                    "items": list(entry.get("items", [])),
                    "status": entry.get("status", ""),
                    "focus": entry.get("focus", ""),
                    "note": entry.get("note", ""),
                    "assigned_at": entry.get("assigned_at", ""),
                }
    config["current_role_assignments"] = assignments
    return assignments


def current_role_assignment(config: dict, role_query: str | None) -> dict:
    role = resolve_role(config, role_query)
    return ensure_role_assignment_state(config).get(role["id"], {})


def role_default_owner(config: dict, role_query: str | None, assignment: dict | None = None) -> str:
    role = resolve_role(config, role_query)
    payload = assignment or current_role_assignment(config, role["id"])
    return payload.get("owner") or role.get("title", role.get("id", "未命名角色"))


def role_default_tool(config: dict, role_query: str | None, assignment: dict | None = None) -> str:
    role = resolve_role(config, role_query)
    payload = assignment or current_role_assignment(config, role["id"])
    if payload.get("tool"):
        return payload["tool"]
    preferred = role.get("preferred_tools", [])
    return preferred[0] if preferred else "shared"


def set_current_role_assignment(config: dict, role_query: str | None, payload: dict) -> dict:
    role = resolve_role(config, role_query)
    assignments = ensure_role_assignment_state(config)
    assignments[role["id"]] = payload
    config["current_role_assignments"] = assignments
    return assignments[role["id"]]


def role_workbench_relative(role_query: str | None, config: dict) -> str:
    role = resolve_role(config, role_query)
    return f"{ROLE_WORKBENCHES_RELATIVE}/{role['id']}.md"


def role_workbench_ai_relative(role_query: str | None, config: dict) -> str:
    role = resolve_role(config, role_query)
    return memory_file(f"role-workbench.{role['id']}.md")


def role_document_reads(project_root: Path, config: dict, role_query: str | None, *, include_ai: bool = True) -> list[str]:
    role = resolve_role(config, role_query)
    ordered = [
        ".factory/project.json",
        "AGENTS.md",
        "GEMINI.md",
        "docs/03-solution/technical-selection.md",
    ]
    if include_ai:
        ordered.extend(
            [
                PROJECT_INDEX_RELATIVE,
                CURRENT_STATE_RELATIVE,
                TASKS_SUMMARY_RELATIVE,
                CHANGE_SUMMARY_RELATIVE,
                AGENT_SESSION_RELATIVE,
                TECH_STACK_SUMMARY_RELATIVE,
                DESIGN_ASSETS_SUMMARY_RELATIVE,
                MOTIVATION_STATE_RELATIVE,
                AUTONOMY_RULES_RELATIVE,
                EVOLUTION_BASELINE_RELATIVE,
            ]
        )
    ordered.extend(stage_reference_docs(config.get("stage", "")))
    ordered.extend(
        [
            MULTI_AGENT_BOARD_RELATIVE,
            PULL_REQUESTS_RELATIVE,
            PR_BOARD_RELATIVE,
            PR_HANDOVERS_RELATIVE,
            REMOTE_PRS_RELATIVE,
            TEAM_SYNC_RELATIVE,
            TEAM_ENERGY_RELATIVE,
            AGENT_ACHIEVEMENTS_RELATIVE,
            TEAM_RETRO_RELATIVE,
            ROLE_ASSIGNMENTS_RELATIVE,
            ROLE_HANDOFFS_RELATIVE,
            ROLE_SYNC_RELATIVE,
            RECOVERY_REVIEW_RELATIVE,
            PATTERN_FIX_REPORT_RELATIVE,
            CHAT_BOOTSTRAP_RELATIVE,
            PR_CHECK_REPORT_RELATIVE,
            ROLE_REVIEWS_RELATIVE,
            ROLE_CLOSEOUTS_RELATIVE,
            TEAM_CLOSEOUTS_RELATIVE,
        ]
    )
    ordered.append(role_workbench_relative(role["id"], config))
    if include_ai:
        ordered.append(role_workbench_ai_relative(role["id"], config))
        ordered.append(PR_SUMMARY_RELATIVE)
        ordered.append(PR_BOARD_SUMMARY_RELATIVE)
        ordered.append(PR_CHECK_SUMMARY_RELATIVE)
        ordered.append(PR_HANDOVER_SUMMARY_RELATIVE)
        ordered.append(REMOTE_PR_SUMMARY_RELATIVE)
        ordered.append(RECOVERY_PLAYBOOK_RELATIVE)
        ordered.append(PATTERN_FIX_SUMMARY_RELATIVE)
    ordered.extend(role.get("docs", []))

    reads: list[str] = []
    seen = set()
    for relative in ordered:
        if relative in seen:
            continue
        seen.add(relative)
        if (project_root / relative).exists():
            reads.append(relative)
    return reads


def dispatch_command(project_root: Path, action: str, *extra_args: str) -> str:
    tokens = [
        "python3",
        str(Path(__file__).resolve().parent / "factory-dispatch"),
        action,
        "--project",
        str(project_root),
        *extra_args,
    ]
    return " ".join(shlex.quote(token) for token in tokens)


def role_recommended_commands(project_root: Path, config: dict, role_query: str | None, owner: str, focus: str = "") -> list[str]:
    role = resolve_role(config, role_query)
    role_id = role.get("id", "coordinator")
    stage = config.get("stage", "未知")
    commands: list[str] = [
        dispatch_command(project_root, "session", "--owner", owner, "--focus", focus or role.get("title", "当前角色")),
        dispatch_command(project_root, "workbench", "--role", role_id, "--owner", owner, "--focus", focus or role.get("title", "当前角色")),
    ]

    if role_id == "coordinator":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", "requirements-analyst", "--owner", owner),
                dispatch_command(project_root, "board", "--owner", owner, "--focus", focus or "刷新协作看板"),
                dispatch_command(project_root, "pr-board", "--owner", owner, "--focus", focus or "查看 PR 协作面"),
                dispatch_command(project_root, "pr-remote-sync", "--owner", owner),
                dispatch_command(project_root, "pr-check", "--owner", owner, "--mode", "review-ready"),
                dispatch_command(project_root, "doctor", "--owner", owner, "--scope", "full"),
                dispatch_command(project_root, "motivation", "--owner", owner, "--focus", focus or "刷新团队动能"),
                dispatch_command(project_root, "evolution", "--owner", owner, "--note", focus or "刷新项目基线"),
                dispatch_command(project_root, "profile", "pre-gate", "--owner", owner),
            ]
        )
        if stage == "BRAINSTORM":
            commands.append(dispatch_command(project_root, "prd-bootstrap", "--owner", owner))
    elif role_id == "requirements-analyst":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "prd-bootstrap", "--owner", owner),
                dispatch_command(project_root, "requirements-verify", "--owner", owner),
                dispatch_command(project_root, "motivation", "--role", role_id, "--owner", owner, "--focus", focus or "同步需求推进节奏"),
                dispatch_command(project_root, "doc", "--doc", "docs/02-requirements/prd.md", "--summary", "补充需求细节"),
                dispatch_command(project_root, "trace", "--source", "REQ-001", "--targets", "TASK-001,TC-001"),
            ]
        )
    elif role_id == "solution-architect":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "design", "--owner", owner),
                dispatch_command(project_root, "tech", "--preset", "stratix-admin", "--owner", owner),
                dispatch_command(project_root, "evolution", "--owner", owner, "--note", focus or "刷新设计与技术基线"),
                dispatch_command(project_root, "trace", "--source", "ARCH-001", "--targets", "API-001,TASK-001"),
                dispatch_command(project_root, "plan", "--iteration", "迭代 1", "--owner", owner),
            ]
        )
    elif role_id == "ux-designer":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "design", "--owner", owner),
                dispatch_command(project_root, "design-assets", "--title", "关键页面设计图", "--images", "/absolute/path/to/mockup.png", "--owner", owner),
                dispatch_command(project_root, "motivation", "--role", role_id, "--owner", owner, "--focus", focus or "保持设计协作动能"),
                dispatch_command(project_root, "doc", "--doc", "docs/03-solution/ux-ui-design.md", "--summary", "补充 UX/UI 设计"),
                dispatch_command(project_root, "board", "--owner", owner, "--focus", focus or "同步设计协作"),
            ]
        )
    elif role_id in {"backend-engineer", "frontend-engineer"}:
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "tech", "--owner", owner),
                dispatch_command(project_root, "plan", "--iteration", "迭代 1", "--owner", owner, "--create-items"),
                dispatch_command(project_root, "run", "--item", "TASK-001", "--work-block", "WB-001-01", "--status", "进行中", "--owner", owner),
                dispatch_command(project_root, "recovery", "--item", "TASK-001", "--owner", owner),
                dispatch_command(project_root, "pattern", "--item", "TASK-001", "--owner", owner),
                dispatch_command(project_root, "pr-start", "--item", "TASK-001", "--owner", owner),
                dispatch_command(project_root, "pr-remote-open", "--pr", "PR-001", "--owner", owner),
                dispatch_command(project_root, "merge-pr", "--pr", "PR-001", "--owner", owner),
            ]
        )
    elif role_id == "qa-engineer":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "stage", "--owner", owner),
                dispatch_command(project_root, "quality", "--owner", owner),
                dispatch_command(project_root, "pattern", "--item", "BUG-001", "--owner", owner),
                dispatch_command(project_root, "pr-remote-sync", "--owner", owner),
                dispatch_command(project_root, "pr-check", "--owner", owner, "--mode", "gate-ready"),
                dispatch_command(project_root, "workflow", "--workflow", "pre_gate", "--owner", owner),
            ]
        )
    elif role_id == "release-manager":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "pr-remote-merge", "--pr", "PR-001", "--owner", owner),
                dispatch_command(project_root, "pr-handover", "--owner", owner),
                dispatch_command(project_root, "release", "--owner", owner),
                dispatch_command(project_root, "handover", "--owner", owner),
                dispatch_command(project_root, "evolution", "--owner", owner, "--note", focus or "沉淀发布与交接基线"),
                dispatch_command(project_root, "snapshot", "--owner", owner),
            ]
        )
    elif role_id == "memory-manager":
        commands.extend(
            [
                dispatch_command(project_root, "assign", "--role", role_id, "--owner", owner),
                dispatch_command(project_root, "memory"),
                dispatch_command(project_root, "motivation", "--owner", owner, "--focus", focus or "刷新团队动能与记忆"),
                dispatch_command(project_root, "evolution", "--owner", owner, "--note", focus or "刷新最佳实践基线"),
                dispatch_command(project_root, "daily", "--owner", owner, "--focus", focus or "同步 AI 记忆"),
                dispatch_command(project_root, "doctor", "--owner", owner, "--scope", "memory"),
            ]
        )

    commands.append(dispatch_command(project_root, "role-review", "--role", role_id, "--reviewer", owner))

    deduped: list[str] = []
    seen = set()
    for item in commands:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped[:8]


def format_item_brief(item: dict) -> str:
    return f"- `{item['id']}` {item['title']} | 状态：{item['status']} | 负责人：{item['owner']}"


def collect_active_items(project_root: Path) -> list[dict]:
    items = collect_items(project_root)
    return [item for item in items if item["status"] not in CLOSED_STATUSES]


def infer_role_for_item(config: dict, item: dict) -> dict:
    item_id = item.get("id", "")
    assignments = ensure_role_assignment_state(config)
    for role_id, payload in assignments.items():
        if item_id in payload.get("items", []):
            return resolve_role(config, role_id)

    owner = item.get("owner", "")
    roles = ensure_role_catalog(config)
    normalized_owner = normalize_key(owner)
    if normalized_owner:
        for role in roles:
            candidates = [role.get("id", ""), role.get("title", ""), *role.get("aliases", [])]
            if normalized_owner in {normalize_key(candidate) for candidate in candidates if candidate}:
                return role

    stage = config.get("stage", "")
    links = normalize_key(item.get("links", ""))
    title = normalize_key(item.get("title", ""))

    if item_id.startswith(("CR-", "BUG-")):
        return resolve_role(config, "coordinator")
    if stage in {"BRAINSTORM", "REQUIREMENTS", "ANALYSIS"}:
        return resolve_role(config, "requirements-analyst")
    if stage == "DESIGN":
        if "ui" in links or "界面" in title:
            return resolve_role(config, "ux-designer")
        return resolve_role(config, "solution-architect")
    if stage in {"TESTING", "ACCEPTANCE"}:
        return resolve_role(config, "qa-engineer")
    if stage in {"RELEASE", "MAINTENANCE"}:
        return resolve_role(config, "release-manager")
    if "ui" in links or "前端" in title or "页面" in title:
        return resolve_role(config, "frontend-engineer")
    return resolve_role(config, "backend-engineer")


def group_items_by_role(config: dict, items: Sequence[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for role in ensure_role_catalog(config):
        grouped[role["id"]] = []
    grouped["unassigned"] = []

    role_ids = set(grouped.keys())
    for item in items:
        try:
            role = infer_role_for_item(config, item)
            role_id = role.get("id", "unassigned")
        except Exception:
            role_id = "unassigned"
        if role_id not in role_ids:
            role_id = "unassigned"
        grouped.setdefault(role_id, []).append(item)
    return grouped


def role_assigned_items(
    project_root: Path,
    config: dict,
    role_query: str | None,
    *,
    include_closed: bool = False,
) -> list[dict]:
    role = resolve_role(config, role_query)
    item_lookup = {item["id"]: item for item in collect_items(project_root)}
    assignment = current_role_assignment(config, role["id"])
    explicit_ids = list(assignment.get("items", []))
    explicit_items = [item_lookup[item_id] for item_id in explicit_ids if item_id in item_lookup]
    if "items" in assignment:
        if include_closed:
            return explicit_items
        return [item for item in explicit_items if item["status"] not in CLOSED_STATUSES]

    grouped = group_items_by_role(config, list(item_lookup.values()))
    if include_closed:
        return grouped.get(role["id"], [])
    return [item for item in grouped.get(role["id"], []) if item["status"] not in CLOSED_STATUSES]


def project_config_path(project_root: Path) -> Path:
    return project_root / PROJECT_CONFIG_RELATIVE


def project_lock_path(project_root: Path) -> Path:
    return project_root / PROJECT_LOCK_RELATIVE


def inspect_project_lock(project_root: Path) -> dict:
    lock_path = project_lock_path(project_root)
    payload = {}
    if lock_path.exists():
        raw = lock_path.read_text(encoding="utf-8").strip()
        if raw:
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {"raw": raw}

    lock_key = str(lock_path.resolve())
    inherited_lock = os.environ.get(PROJECT_LOCK_ENV)
    if inherited_lock == lock_key:
        return {
            "path": str(lock_path),
            "locked": True,
            "by_current_process": True,
            "payload": payload,
        }

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            locked = False
        except BlockingIOError:
            locked = True

    return {
        "path": str(lock_path),
        "locked": locked,
        "by_current_process": False,
        "payload": payload,
    }


@contextmanager
def project_lock(project_root: Path, *, timeout_seconds: float = DEFAULT_LOCK_TIMEOUT_SECONDS, reason: str = ""):
    lock_path = project_lock_path(project_root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_key = str(lock_path.resolve())

    inherited_lock = os.environ.get(PROJECT_LOCK_ENV)
    if inherited_lock == lock_key:
        yield lock_path
        return

    started_at = time.monotonic()
    previous_env = os.environ.get(PROJECT_LOCK_ENV)
    with lock_path.open("a+", encoding="utf-8") as handle:
        while True:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                waited = time.monotonic() - started_at
                if waited >= timeout_seconds:
                    raise RuntimeError(
                        f"等待项目锁超时：{lock_path}，原因：{reason or '未说明'}，已等待 {waited:.1f}s"
                    )
                time.sleep(0.1)

        handle.seek(0)
        handle.truncate()
        handle.write(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "reason": reason or "未说明",
                    "locked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        handle.flush()
        os.environ[PROJECT_LOCK_ENV] = lock_key

        try:
            yield lock_path
        finally:
            handle.seek(0)
            handle.truncate()
            handle.flush()
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            if previous_env is None:
                os.environ.pop(PROJECT_LOCK_ENV, None)
            else:
                os.environ[PROJECT_LOCK_ENV] = previous_env


def ensure_project(project_root: Path) -> None:
    if not project_root.exists():
        raise RuntimeError(f"项目目录不存在：{project_root}")
    config_path = project_config_path(project_root)
    if not config_path.exists():
        raise RuntimeError(f"未找到项目配置：{config_path}")


def load_project_config(project_root: Path) -> dict:
    ensure_project(project_root)
    return json.loads(project_config_path(project_root).read_text(encoding="utf-8"))


def save_project_config(project_root: Path, config: dict) -> None:
    ensure_project(project_root)
    project_config_path(project_root).write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def append_log_line(path: Path, line: str) -> None:
    if not path.exists():
        return
    current = path.read_text(encoding="utf-8").rstrip()
    if not current:
        path.write_text(line.rstrip() + "\n", encoding="utf-8")
        return
    path.write_text(current + "\n" + line.rstrip() + "\n", encoding="utf-8")


def parse_list(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def unique_preserve(values: Iterable[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        item = value.strip()
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def built_in_tech_presets() -> dict[str, dict]:
    return {name: dict(payload) for name, payload in TECH_PROFILE_PRESETS.items()}


def normalize_tech_preset(value: str | None) -> str:
    normalized = normalize_key(value or "")
    mapping = {
        "custom": "custom",
        "plain": "custom",
        "python": "python-backend",
        "py": "python-backend",
        "pythonbackend": "python-backend",
        "pythonservice": "python-backend",
        "fastapi": "python-backend",
        "stratix": "stratix-admin",
        "stratixadmin": "stratix-admin",
        "stratixnodejsbackend": "stratix-admin",
    }
    return mapping.get(normalized, normalized or "custom")


def tech_profile_state_path(project_root: Path) -> Path:
    return project_root / TECH_PROFILE_STATE_RELATIVE


def design_asset_state_path(project_root: Path) -> Path:
    return project_root / DESIGN_ASSET_STATE_RELATIVE


def build_tech_profile_from_preset(preset: str | None = None) -> dict:
    normalized = normalize_tech_preset(preset)
    if normalized in {"", "custom"}:
        return {
            "preset": "custom",
            "title": "自定义技术画像",
            "stack": "",
            "summary": "",
            "projects": [],
            "modules": [],
            "rules": [],
            "admin_requirements": [],
            "commands": [],
            "guides": [],
        }
    payload = TECH_PROFILE_PRESETS.get(normalized)
    if not payload:
        raise RuntimeError(f"未知技术画像预设：{preset}")
    result = dict(payload)
    result["preset"] = result.get("id", normalized)
    return result


def normalize_tech_profile_record(record: dict | None = None) -> dict:
    payload = dict(record or {})
    preset = normalize_tech_preset(payload.get("preset", "custom"))
    result = build_tech_profile_from_preset(preset)
    for key in ("title", "stack", "summary", "owner", "note", "applied_at"):
        if str(payload.get(key, "")).strip():
            result[key] = str(payload.get(key, "")).strip()
    for key in ("projects", "modules", "rules", "admin_requirements", "commands", "guides", "required_skills"):
        values = payload.get(key, [])
        if isinstance(values, str):
            values = parse_list(values)
        result[key] = unique_preserve(str(item) for item in values if str(item).strip())
    role_required = payload.get("role_required_skills", {})
    normalized_role_required: dict[str, list[str]] = {}
    if isinstance(role_required, dict):
        for role_id, names in role_required.items():
            if isinstance(names, str):
                names = parse_list(names)
            normalized_role_required[str(role_id)] = unique_preserve(str(item) for item in names if str(item).strip())
    result["role_required_skills"] = normalized_role_required
    result["preset"] = preset
    return result


def current_tech_profile(config: dict) -> dict:
    return normalize_tech_profile_record(config.get("technical_profile"))


def skill_records_by_names(config: dict, names: Sequence[str]) -> list[dict]:
    skill_map = shared_skill_lookup(config.get("shared_skills", []))
    records: list[dict] = []
    seen = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        if name in skill_map:
            records.append(dict(skill_map[name]))
        else:
            records.append(
                {
                    "name": name,
                    "path": "",
                    "purpose": "当前全局未安装该 skill，请补充对应 skill 或按技术画像规则手工执行。",
                    "missing": True,
                }
            )
    return records


def tech_required_skill_records(config: dict, role_query: str | None = None) -> list[dict]:
    profile = current_tech_profile(config)
    role_required = profile.get("role_required_skills", {})
    names: list[str]
    if role_query:
        role = resolve_role(config, role_query)
        names = role_required.get(role.get("id", ""), []) or profile.get("required_skills", [])
    else:
        names = profile.get("required_skills", [])
    return skill_records_by_names(config, names)


def save_tech_profile_state(project_root: Path, record: dict) -> None:
    write_text(tech_profile_state_path(project_root), json.dumps(normalize_tech_profile_record(record), ensure_ascii=False, indent=2))


def design_asset_records(config: dict) -> list[dict]:
    raw = config.get("design_assets", [])
    result: list[dict] = []
    if not isinstance(raw, list):
        return result
    for item in raw:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        normalized = dict(item)
        files = item.get("files", item.get("images", []))
        links = item.get("links", [])
        normalized["files"] = unique_preserve(str(path) for path in files if str(path).strip())
        normalized["links"] = unique_preserve(str(path) for path in links if str(path).strip())
        result.append(normalized)
    return result


def save_design_asset_state(project_root: Path, records: Sequence[dict]) -> None:
    write_text(design_asset_state_path(project_root), json.dumps(list(records), ensure_ascii=False, indent=2))


def slugify(value: str, fallback: str = "work") -> str:
    normalized = normalize_key(value)
    ascii_only = re.sub(r"[^0-9a-z]+", "-", normalized).strip("-")
    return ascii_only or fallback


def quantize_effort_days(value: float) -> float:
    quantized = math.ceil(max(float(value), MIN_EFFORT_DAYS) * 2 - 1e-9) / 2
    return max(MIN_EFFORT_DAYS, quantized)


def parse_effort_days(value: str | int | float) -> float:
    if isinstance(value, (int, float)):
        return quantize_effort_days(float(value))

    raw = str(value or "").strip()
    if not raw:
        return MIN_EFFORT_DAYS

    match = re.search(r"(\d+(?:\.\d+)?)", raw)
    if not match:
        return MIN_EFFORT_DAYS

    amount = float(match.group(1))
    normalized = raw.lower()
    if "小时" in raw or "工时" in raw or normalized.endswith("h") or "h" in normalized:
        return quantize_effort_days(amount / HOURS_PER_PERSON_DAY)
    return quantize_effort_days(amount)


def format_effort_days(value: str | int | float) -> str:
    days = parse_effort_days(value)
    if abs(days - round(days)) < 1e-9:
        return f"{int(round(days))}人天"
    return f"{days:.1f}人天"


def parse_hours_value(value: str | int | float) -> int:
    return max(1, int(round(parse_effort_days(value) * HOURS_PER_PERSON_DAY)))


def default_block_title(item_type: str, item_title: str = "") -> str:
    title = item_title.strip()
    if item_type == "task":
        return title or "完成任务主项"
    if item_type == "change":
        return title or "完成变更处理"
    return title or "完成问题修复"


def default_block_titles(item_type: str, count: int, item_title: str = "") -> list[str]:
    if count <= 1:
        return [default_block_title(item_type, item_title)]

    label_map = {
        "task": [
            "确认边界与实现方案",
            "完成核心实现",
            "联调、验证与同步收口",
        ],
        "change": [
            "分析影响与调整方案",
            "完成变更实现",
            "验证结果并同步收口",
        ],
        "bug": [
            "复现问题并确认根因",
            "完成修复实现",
            "验证结果并同步收口",
        ],
    }[item_type]

    titles = list(label_map[:count])
    while len(titles) < count:
        titles.append(f"补充分解 {len(titles) + 1}")
    return titles


def generate_work_blocks(
    total_hours: int | float | str,
    item_id: str,
    item_type: str,
    *,
    item_title: str = "",
    breakdown: Sequence[str | int | float] | None = None,
    block_titles: Sequence[str] | None = None,
) -> list[dict]:
    total_days = parse_effort_days(total_hours)
    if breakdown:
        chunk_days = [parse_effort_days(item) for item in breakdown]
        total_breakdown = round(sum(chunk_days), 4)
        if abs(total_breakdown - total_days) > 1e-6:
            raise RuntimeError(
                f"工作块拆分总和 {format_effort_days(total_breakdown)} 与任务总量 {format_effort_days(total_days)} 不一致。"
            )
    else:
        chunk_days = [total_days]

    total_blocks = len(chunk_days)
    item_no = item_id.split("-")[1]

    if block_titles:
        labels = [item.strip() for item in block_titles if str(item).strip()]
        if len(labels) != total_blocks:
            raise RuntimeError("工作块标题数量与拆分数量不一致。")
    else:
        labels = default_block_titles(item_type, total_blocks, item_title)

    blocks: list[dict] = []
    for index in range(total_blocks):
        blocks.append(
            {
                "id": f"WB-{item_no}-{index + 1:02d}",
                "title": labels[index],
                "hours": chunk_days[index],
                "status": "待开始",
            }
        )
    return blocks


def render_work_block_table(blocks: Sequence[dict]) -> list[str]:
    lines = [
        "| 工作块编号 | 内容 | 预估人天 | 状态 |",
        "|---|---|---:|---|",
    ]
    for block in blocks:
        lines.append(f"| {block['id']} | {block['title']} | {format_effort_days(block['hours'])} | {block['status']} |")
    return lines


def script_path(name: str) -> str:
    return str(Path(__file__).resolve().parent / name)


def run_step(command: Sequence[str], label: str, *, cwd: Path | None = None) -> dict:
    result = subprocess.run(list(command), capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    return {
        "label": label,
        "command": " ".join(command),
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def run_script(name: str, *arguments: str, label: str) -> dict:
    command = [sys.executable, script_path(name), *arguments]
    return run_step(command, label)


def command_available(name: str) -> bool:
    return shutil.which(name) is not None


def is_git_repo(project_root: Path) -> bool:
    if not command_available("git"):
        return False
    result = run_step(["git", "rev-parse", "--is-inside-work-tree"], "检查 git 仓库", cwd=project_root)
    return result["returncode"] == 0 and result["stdout"].strip() == "true"


def git_current_branch(project_root: Path) -> str:
    result = run_step(["git", "branch", "--show-current"], "读取当前分支", cwd=project_root)
    branch = result["stdout"].strip()
    if result["returncode"] == 0 and branch:
        return branch
    return "main"


def git_branch_exists(project_root: Path, branch: str) -> bool:
    result = run_step(["git", "rev-parse", "--verify", branch], f"检查分支 {branch}", cwd=project_root)
    return result["returncode"] == 0


def git_head_commit(project_root: Path) -> str:
    result = run_step(["git", "rev-parse", "HEAD"], "读取 HEAD", cwd=project_root)
    return result["stdout"].strip() if result["returncode"] == 0 else ""


def git_remote_url(project_root: Path, remote: str = "origin") -> str:
    result = run_step(["git", "remote", "get-url", remote], f"读取远端 {remote}", cwd=project_root)
    return result["stdout"].strip() if result["returncode"] == 0 else ""


def extract_first_url(text: str) -> str:
    match = re.search(r"https?://\S+", text or "")
    return match.group(0) if match else ""


def normalize_remote_tool(value: str | None) -> str:
    normalized = normalize_key(value or "")
    mapping = {
        "auto": "auto",
        "gh": "gh",
        "github": "gh",
        "github-cli": "gh",
        "glab": "glab",
        "gitlab": "glab",
        "gitlab-cli": "glab",
        "record-only": "record-only",
        "recordonly": "record-only",
        "manual": "record-only",
    }
    return mapping.get(normalized, normalized or "auto")


def remote_tool_command(tool: str) -> str:
    return {"gh": "gh", "glab": "glab"}.get(normalize_remote_tool(tool), "")


def remote_tool_available(tool: str) -> bool:
    command = remote_tool_command(tool)
    return bool(command) and command_available(command)


def infer_remote_tool(project_root: Path, preferred: str = "auto", remote_url: str = "") -> str:
    tool = normalize_remote_tool(preferred)
    if tool != "auto":
        return tool
    url = (remote_url or git_remote_url(project_root)).lower()
    if "gitlab" in url and remote_tool_available("glab"):
        return "glab"
    if "github" in url and remote_tool_available("gh"):
        return "gh"
    if remote_tool_available("gh"):
        return "gh"
    if remote_tool_available("glab"):
        return "glab"
    return "record-only"


def remote_tool_label(tool: str) -> str:
    return {
        "gh": "GitHub",
        "glab": "GitLab",
        "record-only": "手工记录",
    }.get(normalize_remote_tool(tool), tool or "")


def remote_state_text(value: str) -> str:
    normalized = normalize_key(value)
    mapping = {
        "open": "远端打开",
        "opened": "远端打开",
        "draft": "远端草稿",
        "merged": "远端已合并",
        "closed": "远端已关闭",
    }
    return mapping.get(normalized, value.strip() if value else "")


def parse_json_output(text: str) -> dict | list:
    payload = json.loads(text or "{}")
    if isinstance(payload, (dict, list)):
        return payload
    raise RuntimeError("命令未返回有效 JSON。")


def json_step(command: Sequence[str], label: str, *, cwd: Path | None = None) -> tuple[dict, dict | list]:
    step = run_step(command, label, cwd=cwd)
    if step["returncode"] != 0:
        raise RuntimeError(step["stderr"] or step["stdout"] or f"{label}失败")
    return step, parse_json_output(step["stdout"])


def remote_review_result_from_value(value: str, *, approved_count: int = 0) -> str:
    normalized = normalize_key(value)
    if normalized in {"approved", "approve", "通过"} or approved_count > 0:
        return "通过"
    if normalized in {"changesrequested", "changes_requested", "需修改"}:
        return "需修改"
    if normalized in {"blocked", "阻塞"}:
        return "阻塞"
    return "待评审"


def remote_checks_result_from_states(states: Sequence[str]) -> str:
    normalized = [normalize_key(state) for state in states if state]
    if not normalized:
        return "待检查"
    failed = {"failure", "failed", "error", "timedout", "timed_out", "actionrequired", "action_required", "cancelled", "canceled"}
    pending = {"pending", "queued", "inprogress", "in_progress", "requested", "waiting"}
    success = {"success", "succeeded", "skipped", "neutral", "passed", "pass"}
    if any(state in failed for state in normalized):
        return "失败"
    if any(state in pending for state in normalized):
        return "关注"
    if all(state in success for state in normalized):
        return "通过"
    return "关注"


def remote_status_from_state(value: str, *, draft: bool = False, review_result: str = "待评审") -> str:
    normalized = normalize_key(value)
    if normalized == "merged":
        return "merged"
    if normalized == "closed":
        return "blocked"
    if draft:
        return "draft"
    if review_result == "通过":
        return "approved"
    if review_result == "需修改":
        return "changes_requested"
    if review_result == "阻塞":
        return "blocked"
    return "open"


def pr_state_path(project_root: Path) -> Path:
    return project_root / PR_STATE_RELATIVE


def load_pr_records(project_root: Path) -> list[dict]:
    path = pr_state_path(project_root)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return list(payload.get("pull_requests", []))


def save_pr_records(project_root: Path, records: Sequence[dict]) -> None:
    write_text(pr_state_path(project_root), json.dumps(list(records), ensure_ascii=False, indent=2))


def next_sequence_id(records: Sequence[dict], prefix: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+)$")
    max_number = 0
    for record in records:
        value = str(record.get("id", "")).strip()
        match = pattern.match(value)
        if match:
            max_number = max(max_number, int(match.group(1)))
    return f"{prefix}{max_number + 1:03d}"


def normalize_pr_record(record: dict) -> dict:
    normalized = dict(record)
    normalized["items"] = list(record.get("items", []))
    normalized["docs"] = list(record.get("docs", []))
    normalized["tests"] = list(record.get("tests", []))
    normalized["code"] = list(record.get("code", []))
    normalized["reviewers"] = list(record.get("reviewers", []))
    normalized.setdefault("status", "open")
    normalized.setdefault("review_result", "待评审")
    normalized.setdefault("checks_result", "待检查")
    normalized.setdefault("merge_status", "未合并")
    normalized.setdefault("provider", "record-only")
    normalized.setdefault("base_branch", "main")
    normalized.setdefault("branch", "")
    normalized.setdefault("remote_provider", "")
    normalized.setdefault("remote_id", "")
    normalized.setdefault("remote_url", "")
    normalized.setdefault("remote_state", "")
    normalized.setdefault("remote_review_state", "")
    normalized.setdefault("remote_checks_state", "")
    normalized.setdefault("remote_branch", normalized.get("branch", ""))
    normalized.setdefault("remote_base_branch", normalized.get("base_branch", "main"))
    normalized.setdefault("remote_synced_at", "")
    return normalized


def find_pr_record(records: Sequence[dict], query: str) -> dict:
    normalized = normalize_key(query)
    for record in records:
        item = normalize_pr_record(record)
        candidates = [item.get("id", ""), item.get("title", ""), item.get("branch", "")]
        if normalized in {normalize_key(candidate) for candidate in candidates if candidate}:
            return item
    raise RuntimeError(f"未找到 PR 记录：{query}")


def linked_pr_records(records: Sequence[dict], item_id: str) -> list[dict]:
    linked = []
    for record in records:
        normalized = normalize_pr_record(record)
        if item_id in normalized.get("items", []):
            linked.append(normalized)
    return linked


def selected_pr_records(records: Sequence[dict], raw_prs: str | None = None, *, default_active: bool = False) -> list[dict]:
    normalized = [normalize_pr_record(record) for record in records]
    requested = parse_list(raw_prs or "")
    if not requested:
        return active_pr_records(normalized) if default_active else normalized

    selected: list[dict] = []
    seen = set()
    for query in requested:
        record = find_pr_record(normalized, query)
        if record["id"] in seen:
            continue
        seen.add(record["id"])
        selected.append(record)
    return selected


def active_pr_records(records: Sequence[dict]) -> list[dict]:
    return [normalize_pr_record(record) for record in records if normalize_pr_record(record).get("status") in ACTIVE_PR_STATUSES]


def merged_pr_records(records: Sequence[dict]) -> list[dict]:
    return [normalize_pr_record(record) for record in records if normalize_pr_record(record).get("status") in MERGED_PR_STATUSES]


def pr_status_text(record: dict) -> str:
    status = normalize_pr_record(record).get("status", "open")
    mapping = {
        "draft": "草稿",
        "open": "待评审",
        "reviewing": "评审中",
        "changes_requested": "需修改",
        "approved": "已批准待合并",
        "blocked": "阻塞",
        "merged": "已合并",
        "closed": "已关闭",
    }
    return mapping.get(status, status)


def pr_remote_text(record: dict) -> str:
    normalized = normalize_pr_record(record)
    tool = normalize_remote_tool(normalized.get("remote_provider", ""))
    remote_url = normalized.get("remote_url", "")
    remote_id = str(normalized.get("remote_id", "")).strip()
    remote_state = remote_state_text(normalized.get("remote_state", ""))
    label = remote_tool_label(tool) if tool else ""
    if label and remote_id:
        base = f"{label}#{remote_id}"
    elif label:
        base = label
    elif remote_url:
        base = remote_url
    else:
        base = ""
    if base and remote_state:
        return f"{base} {remote_state}"
    return base or remote_state


def pr_record_line(record: dict) -> str:
    normalized = normalize_pr_record(record)
    remote_text = pr_remote_text(normalized)
    return (
        f"- `{normalized['id']}` {normalized.get('title', '未命名 PR')} | 状态：{pr_status_text(normalized)} | "
        f"工作项：{'、'.join(normalized.get('items', [])) or '无'} | "
        f"分支：{normalized.get('branch', '无') or '无'} | "
        f"评审：{normalized.get('review_result', '待评审')} | "
        f"检查：{normalized.get('checks_result', '待检查')}"
        + (f" | 远端：{remote_text}" if remote_text else "")
    )


def merged_pr_line(record: dict) -> str:
    normalized = normalize_pr_record(record)
    remote_text = pr_remote_text(normalized)
    return (
        f"- `{normalized['id']}` {normalized.get('title', '未命名 PR')} | "
        f"合并时间：{normalized.get('merged_at', '未知')} | "
        f"工作项：{'、'.join(normalized.get('items', [])) or '无'}"
        + (f" | 远端：{remote_text}" if remote_text else "")
    )


def write_pr_tracker(
    project_root: Path,
    latest_header: str,
    latest_lines: Sequence[str],
    step_lines: Sequence[str],
    records: Sequence[dict],
    history_line: str,
) -> None:
    doc_path = project_root / PULL_REQUESTS_RELATIVE
    active_lines = [pr_record_line(record) for record in active_pr_records(records)] or ["- 当前无活跃 PR。"]
    merged_lines = [merged_pr_line(record) for record in merged_pr_records(records)[-10:]] or ["- 当前无已合并 PR。"]
    upsert_section(doc_path, latest_header, list(latest_lines), default_title="# PR 记录")
    upsert_section(doc_path, "## 活跃 PR", active_lines, default_title="# PR 记录")
    upsert_section(doc_path, "## 最近已合并", merged_lines, default_title="# PR 记录")
    upsert_section(doc_path, "## 步骤结果", list(step_lines) or ["- 无"], default_title="# PR 记录")
    prepend_history_entry(doc_path, "## 历史 PR 动作", history_line, default_title="# PR 记录")


def remote_pr_records(records: Sequence[dict]) -> list[dict]:
    result: list[dict] = []
    for record in records:
        normalized = normalize_pr_record(record)
        if normalized.get("remote_provider") or normalized.get("remote_url") or normalized.get("remote_id"):
            result.append(normalized)
    return result


def remote_pr_record_line(record: dict) -> str:
    normalized = normalize_pr_record(record)
    return (
        f"- `{normalized['id']}` {normalized.get('title', '未命名 PR')} | "
        f"远端：{pr_remote_text(normalized) or '未关联'} | "
        f"状态：{pr_status_text(normalized)} | "
        f"评审：{normalized.get('review_result', '待评审')} | "
        f"检查：{normalized.get('checks_result', '待检查')}"
    )


def write_remote_pr_tracker(
    project_root: Path,
    latest_header: str,
    latest_lines: Sequence[str],
    step_lines: Sequence[str],
    records: Sequence[dict],
    history_line: str,
) -> None:
    doc_path = project_root / REMOTE_PRS_RELATIVE
    remote_records = remote_pr_records(records)
    active_lines = [remote_pr_record_line(record) for record in remote_records if record.get("status") in ACTIVE_PR_STATUSES] or ["- 当前无活跃远端 PR。"]
    merged_lines = [remote_pr_record_line(record) for record in remote_records if record.get("status") in MERGED_PR_STATUSES][-10:] or ["- 当前无已合并远端 PR。"]
    upsert_section(doc_path, latest_header, list(latest_lines), default_title="# 远程 PR 协作")
    upsert_section(doc_path, "## 活跃远端 PR", active_lines, default_title="# 远程 PR 协作")
    upsert_section(doc_path, "## 最近已合并远端 PR", merged_lines, default_title="# 远程 PR 协作")
    upsert_section(doc_path, "## 步骤结果", list(step_lines) or ["- 无"], default_title="# 远程 PR 协作")
    prepend_history_entry(doc_path, "## 历史远端动作", history_line, default_title="# 远程 PR 协作")


def render_pr_summary(records: Sequence[dict]) -> str:
    normalized = [normalize_pr_record(record) for record in records]
    active = [record for record in normalized if record.get("status") in ACTIVE_PR_STATUSES]
    merged = [record for record in normalized if record.get("status") == "merged"]

    lines = [
        "# PR 摘要",
        "",
        f"- 活跃 PR：{len(active)}",
        f"- 已合并 PR：{len(merged)}",
        f"- 最近更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    if active:
        lines.extend(["## 活跃 PR", ""])
        for record in active[-10:]:
            lines.append(
                f"- `{record['id']}` {record.get('title', '未命名 PR')} | 状态：{pr_status_text(record)} | "
                f"工作项：{'、'.join(record.get('items', [])) or '无'} | 分支：{record.get('branch', '无') or '无'}"
            )
        lines.append("")

    if merged:
        lines.extend(["## 最近已合并", ""])
        for record in merged[-10:]:
            lines.append(
                f"- `{record['id']}` {record.get('title', '未命名 PR')} | 合并时间：{record.get('merged_at', '未知')} | "
                f"工作项：{'、'.join(record.get('items', [])) or '无'}"
            )
    elif not active:
        lines.append("暂无 PR 记录。")

    return "\n".join(lines).strip()


def render_remote_pr_summary(records: Sequence[dict]) -> str:
    remote_records = remote_pr_records(records)
    active = [record for record in remote_records if record.get("status") in ACTIVE_PR_STATUSES]
    merged = [record for record in remote_records if record.get("status") == "merged"]

    lines = [
        "# 远程 PR 摘要",
        "",
        f"- 活跃远端 PR：{len(active)}",
        f"- 已合并远端 PR：{len(merged)}",
        f"- 最近更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]

    if active:
        lines.extend(["## 活跃远端 PR", ""])
        lines.extend(remote_pr_record_line(record) for record in active[-10:])
        lines.append("")

    if merged:
        lines.extend(["## 最近已合并远端 PR", ""])
        lines.extend(remote_pr_record_line(record) for record in merged[-10:])
    elif not active:
        lines.append("暂无远端 PR 记录。")

    return "\n".join(lines).strip()


def find_item_file(project_root: Path, item_id: str, allowed_prefixes: Iterable[str] | None = None) -> Path:
    prefixes = set(allowed_prefixes or ITEM_FILE_LOCATIONS.keys())
    for prefix, relative in ITEM_FILE_LOCATIONS.items():
        if prefix not in prefixes:
            continue
        path = project_root / relative / f"{item_id}.md"
        if item_id.startswith(prefix) and path.exists():
            return path
    for prefix, relative in ITEM_FILE_LOCATIONS.items():
        if prefix not in prefixes:
            continue
        path = project_root / relative / f"{item_id}.md"
        if path.exists():
            return path
    raise RuntimeError(f"未找到工作项文件：{item_id}")


def replace_section(path: Path, header: str, content_lines: Sequence[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    try:
        start = lines.index(header)
    except ValueError as exc:
        raise RuntimeError(f"文件中缺少章节：{header}") from exc

    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break

    updated = lines[: start + 1] + [""] + list(content_lines) + [""] + lines[end:]
    write_text(path, "\n".join(updated))


def upsert_item_pr_section(project_root: Path, item_id: str, record: dict) -> None:
    item_path = find_item_file(project_root, item_id)
    normalized = normalize_pr_record(record)
    upsert_section(
        item_path,
        "## PR 关联",
        [
            f"- 最新 PR：{normalized.get('id', '未知')}",
            f"- 标题：{normalized.get('title', '未命名 PR')}",
            f"- 状态：{pr_status_text(normalized)}",
            f"- 分支：{normalized.get('branch', '无') or '无'}",
            f"- 目标分支：{normalized.get('base_branch', 'main') or 'main'}",
            f"- 审查结果：{normalized.get('review_result', '待评审')}",
            f"- 合并状态：{normalized.get('merge_status', '未合并')}",
        ],
    )


def upsert_section(path: Path, header: str, content_lines: Sequence[str], *, default_title: str | None = None) -> None:
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = [default_title, ""] if default_title else []

    if header in lines:
        start = lines.index(header)
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        lines = lines[: start + 1] + [""] + list(content_lines) + [""] + lines[end:]
    else:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend([header, "", *content_lines, ""])

    write_text(path, "\n".join(lines))


def prepend_history_entry(path: Path, header: str, line: str, *, default_title: str | None = None) -> None:
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = [default_title, ""] if default_title else []

    if header not in lines:
        if lines and lines[-1] != "":
            lines.append("")
        lines.extend([header, "", line, ""])
        write_text(path, "\n".join(lines))
        return

    start = lines.index(header)
    insert_at = start + 2 if start + 1 < len(lines) and lines[start + 1] == "" else start + 1
    if line not in lines:
        lines.insert(insert_at, line)
    write_text(path, "\n".join(lines))


def parse_work_item(path: Path, field_patterns: dict[str, re.Pattern[str]] | None = None) -> dict:
    patterns = field_patterns or DEFAULT_FIELD_PATTERNS
    result = {
        "id": path.stem,
        "title": path.stem,
        "status": "未知",
        "priority": "未知",
        "owner": "未知",
        "hours": "未知",
        "links": "无",
        "created_at": "",
        "path": path,
    }
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("# "):
        heading = lines[0][2:].strip()
        prefix = f"{path.stem} "
        result["title"] = heading[len(prefix) :] if heading.startswith(prefix) else heading

    captured = set()
    for line in lines:
        stripped = line.strip()
        for key, pattern in patterns.items():
            if key in captured:
                continue
            match = pattern.match(stripped)
            if match:
                result[key] = match.group(1).strip()
                captured.add(key)
    return result


def parse_work_blocks(path: Path) -> list[dict]:
    blocks: list[dict] = []
    in_table = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| 工作块编号 |"):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            break
        match = WORK_BLOCK_ROW_PATTERN.match(line.strip())
        if not match:
            continue
        blocks.append(
            {
                "id": match.group(1).strip(),
                "title": match.group(2).strip(),
                "hours": parse_effort_days(match.group(3)),
                "status": match.group(4).strip(),
            }
        )
    return blocks


def assess_work_block_quality(path: Path) -> dict:
    blocks = parse_work_blocks(path)
    placeholder = [block for block in blocks if WORK_BLOCK_PLACEHOLDER_PATTERN.match(block["title"])]
    if not blocks:
        status = "缺失"
        reason = "未找到工作块表格。"
    elif placeholder:
        ratio = len(placeholder) / max(1, len(blocks))
        if ratio >= 0.3:
            status = "占位"
            reason = f"工作块 {len(blocks)} 个，其中占位块 {len(placeholder)} 个。"
        else:
            status = "关注"
            reason = f"工作块 {len(blocks)} 个，其中占位块 {len(placeholder)} 个。"
    else:
        status = "就绪"
        reason = f"工作块 {len(blocks)} 个，未发现占位块。"
    return {
        "status": status,
        "reason": reason,
        "blocks": blocks,
        "placeholder_count": len(placeholder),
    }


def task_work_block_status(items: Sequence[dict], *, limit: int = 5) -> tuple[str, list[str]]:
    active_tasks = [item for item in items if item["id"].startswith("TASK-") and item["status"] not in CLOSED_STATUSES]
    if not active_tasks:
        return "就绪", ["- 当前无活跃实施任务。"]

    severities: list[str] = []
    lines: list[str] = []
    for item in active_tasks[:limit]:
        quality = assess_work_block_quality(item["path"])
        severities.append(quality["status"])
        lines.append(f"- `{item['id']}`：{quality['status']}，{quality['reason']}")
    for item in active_tasks[limit:]:
        quality = assess_work_block_quality(item["path"])
        severities.append(quality["status"])
    if len(active_tasks) > limit:
        lines.append(f"- 其余活跃任务：{len(active_tasks) - limit} 个，结果已计入统计。")

    if "缺失" in severities:
        return "缺失", lines
    if "占位" in severities:
        return "占位", lines
    if "关注" in severities:
        return "关注", lines
    return "就绪", lines


def collect_items(
    project_root: Path,
    relative_dir: str | None = None,
    prefix: str | None = None,
    *,
    specs: Sequence[tuple[str, str]] | None = None,
    field_patterns: dict[str, re.Pattern[str]] | None = None,
) -> list[dict]:
    if relative_dir and prefix:
        specs = [(relative_dir, prefix)]
    targets = specs or DEFAULT_ITEM_SPECS
    items: list[dict] = []
    for relative, current_prefix in targets:
        base = project_root / relative
        if not base.exists():
            continue
        for file_path in sorted(base.glob(f"{current_prefix}-*.md")):
            items.append(parse_work_item(file_path, field_patterns=field_patterns))
    return items


def file_readiness(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "缺失", "文件不存在"
    nonempty = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(nonempty) <= 2:
        return "占位", "仅有标题或占位描述"
    return "就绪", "已具备实质内容"


def read_recent_log_lines(project_root: Path, top: int, *, date_prefix: str | None = None) -> list[str]:
    path = project_root / EXECUTION_LOG_RELATIVE
    if not path.exists():
        return []
    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("- ")]
    if date_prefix:
        lines = [line for line in lines if line.startswith(f"- {date_prefix}:")]
    return lines[-top:]


def read_risks(project_root: Path) -> tuple[list[str], list[str]]:
    path = project_root / RISK_REGISTER_RELATIVE
    if not path.exists():
        return [], []
    open_risks: list[str] = []
    all_risks: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| RISK-"):
            parts = [part.strip() for part in line.split("|")]
            if len(parts) >= 8:
                item = f"`{parts[1]}` {parts[2]} | 等级：{parts[3]} | 状态：{parts[4]}"
                all_risks.append(f"- {item}")
                if parts[4] not in CLOSED_RISK_STATUSES:
                    open_risks.append(f"- {item}")
    return open_risks, all_risks


def active_items(items: Sequence[dict]) -> list[dict]:
    return [item for item in items if item.get("status") not in CLOSED_STATUSES]


def blocked_items(items: Sequence[dict]) -> list[dict]:
    return [item for item in active_items(items) if item.get("status") == "阻塞"]


def completed_items(items: Sequence[dict], *, top: int | None = None) -> list[dict]:
    records = [item for item in items if item.get("status") in CLOSED_STATUSES]
    if top is None:
        return records
    return records[-top:]


def item_link_ids(item: dict) -> list[str]:
    return parse_list(item.get("links", ""))


def autonomy_guardrails(stage: str) -> list[str]:
    defaults = {
        "BRAINSTORM": [
            "可主动扩展备选方案、风险和成功标准，但不得越过范围确认直接进入实现。",
            "方案分歧优先输出对比，而不是替用户隐式拍板。",
        ],
        "REQUIREMENTS": [
            "允许主动补齐 REQ/NFR、验收标准和依赖，但要保留编号和来源。",
            "提交需求前先做一致性校验，避免遗漏或重复。",
        ],
        "ANALYSIS": [
            "允许主动补足风险、流程和边界条件，但不能跳过设计澄清。",
            "分析结论必须可追溯到需求、约束或历史记录。",
        ],
        "DESIGN": [
            "允许主动补充技术画像、接口边界和设计交付物，但要与需求逐项对照。",
            "设计交付物优先可查看、可评审，而不是只写抽象描述。",
        ],
        "PLAN": [
            "允许主动调整任务顺序和依赖，但不得改写已批准范围。",
            "任务估算以真实人天为准，只有必要时才细化到 0.5 人天。",
        ],
        "IMPLEMENTATION": [
            "允许在已批准范围内自主完成实现、测试和文档同步。",
            "遇到阻塞时先切换路径并留下证据，不要无记录地空转。",
        ],
        "TESTING": [
            "允许主动补齐回归与缺陷验证，但结果必须可复现。",
            "发现模式性问题时，扩大扫描而不是只修表面个案。",
        ],
        "ACCEPTANCE": [
            "允许主动补验收证据和交付清单，但不得绕过未完成的门禁。",
            "所有结论必须能回链到文档、测试、PR 或运行记录。",
        ],
        "RELEASE": [
            "允许主动补齐发布、部署、交接信息，但必须保持正式文档一致。",
            "发布动作优先稳态执行，不在发布窗口发明新流程。",
        ],
        "MAINTENANCE": [
            "允许主动处理变更、修复和复盘，但要同步沉淀到基线。",
            "同类问题优先做模式级修复，而不是反复单点返工。",
        ],
    }
    return list(defaults.get(stage, defaults["IMPLEMENTATION"]))


def autonomy_budget(config: dict, role_query: str | None = None) -> str:
    role = resolve_role(config, role_query) if role_query else {"id": "coordinator"}
    stage = str(config.get("stage", "IMPLEMENTATION"))
    role_id = role.get("id", "coordinator")
    overrides = {
        "coordinator": "可以主动重排协作节奏、刷新看板、补齐门禁检查，但不得跳过审批和阶段切换条件。",
        "requirements-analyst": "可以主动补齐需求细节、缺失字段和追踪关系，但不得凭空新增未确认范围。",
        "solution-architect": "可以主动补齐技术规则、分层和接口边界，但不得绕过需求和 UX 约束独断改范围。",
        "ux-designer": "可以主动补齐页面状态、设计交付物和交互细节，但不得脱离需求主线发散新增页面。",
        "backend-engineer": "可以在批准范围内自主完成实现、测试、文档与 PR，同类问题应主动扩查。",
        "frontend-engineer": "可以在批准范围内自主完成界面实现、测试、文档与 PR，同类问题应主动扩查。",
        "qa-engineer": "可以主动补回归、补缺陷证据、扩大验证范围，但结论要可复现且可回链。",
        "release-manager": "可以主动补齐发布、交付、交接材料，但不能越过未完成的质量门禁。",
        "memory-manager": "可以主动刷新摘要、压缩入口和历史快照，但不得改写正式事实。",
    }
    base = overrides.get(role_id, "可以在当前职责范围内主动推进执行、验证和同步，但不能跳过事实校验与审批边界。")
    return f"{base} 当前阶段补充约束：{'；'.join(autonomy_guardrails(stage)[:2])}"


def infer_recovery_mode(
    item: dict | None = None,
    *,
    note: str = "",
    attempts: int = 0,
    blocked: bool | None = None,
) -> str:
    normalized = normalize_key(note)
    if "空转" in note or "原地打转" in note or "loop" in normalized or "spin" in normalized:
        return "looping"
    if "证据" in note or "验证" in note or "claim" in normalized:
        return "unverified"
    if "升级" in note or "求助" in note or "escalat" in normalized:
        return "premature-escalation"
    if blocked or (item and item.get("status") == "阻塞"):
        return "blocked"
    if attempts >= 3:
        return "path-exhausted"
    return "quality-drift"


def recovery_mode_guide(mode: str) -> dict:
    guides = {
        "blocked": {
            "title": "阻塞恢复",
            "signals": ["依赖未就绪", "权限/环境缺失", "外部输入未到位"],
            "actions": ["明确阻塞点和责任方", "并行推进不受阻的准备工作", "给出最小可继续路径"],
            "evidence": ["阻塞来源", "已排除路径", "下一次跟进时间"],
        },
        "looping": {
            "title": "空转恢复",
            "signals": ["重复尝试同一路径", "日志增长但无新证据", "连续多次回到同一错误"],
            "actions": ["停止重复路径", "改用不同层级的观察或工具", "先做最小复现或最小验证"],
            "evidence": ["已尝试路径列表", "新路径与旧路径的根本差异", "首个验证点"],
        },
        "unverified": {
            "title": "证据不足恢复",
            "signals": ["口头声称完成", "没有测试/截图/日志/文档回链", "结论无法复现"],
            "actions": ["把结论改写为待验证假设", "补最小证据链", "先验证再继续扩展"],
            "evidence": ["测试或运行结果", "文档更新位置", "代码/PR/日志引用"],
        },
        "premature-escalation": {
            "title": "过早升级恢复",
            "signals": ["尚未系统排查就求助", "未形成备选方案", "没有清晰已排除项"],
            "actions": ["补齐已排除路径", "列出 2 个备选方案", "只带着证据升级剩余阻塞"],
            "evidence": ["已排除项", "备选方案比较", "仍需外部协助的最小点"],
        },
        "path-exhausted": {
            "title": "路径耗尽恢复",
            "signals": ["尝试次数过多", "方案集已经穷尽", "存在返工疲劳"],
            "actions": ["回到目标与约束重新分解", "拆小问题并改变切入层级", "引入复盘与模式级修复"],
            "evidence": ["失败模式总结", "新分解结果", "替代路径优先级"],
        },
        "quality-drift": {
            "title": "质量漂移恢复",
            "signals": ["文档/测试/代码不同步", "需求映射模糊", "小问题反复出现"],
            "actions": ["先补同步闭环", "做同类问题扫描", "更新默认基线"],
            "evidence": ["已同步资产", "扫描范围", "新增基线或规则"],
        },
    }
    return guides.get(mode, guides["quality-drift"])


def related_item_candidates(items: Sequence[dict], source_item: dict, *, limit: int = 8) -> list[dict]:
    source_id = source_item.get("id", "")
    source_links = set(item_link_ids(source_item))
    source_owner = source_item.get("owner", "")
    source_title_key = normalize_key(source_item.get("title", ""))
    scored: list[tuple[int, dict]] = []
    for item in items:
        if item.get("id") == source_id:
            continue
        score = 0
        links = set(item_link_ids(item))
        if source_links and links.intersection(source_links):
            score += 3
        if source_owner and item.get("owner") == source_owner:
            score += 1
        title_key = normalize_key(item.get("title", ""))
        if source_title_key and title_key and title_key[:8] == source_title_key[:8]:
            score += 1
        if source_id[:4] == item.get("id", "")[:4]:
            score += 1
        if score > 0:
            scored.append((score, item))
    scored.sort(key=lambda pair: (-pair[0], pair[1].get("id", "")))
    return [item for _, item in scored[:limit]]


def latest_dir_id(project_root: Path, relative_dir: str, prefix: str) -> str:
    root = project_root / relative_dir
    if not root.exists():
        return "无"
    ids = sorted(path.name for path in root.iterdir() if path.is_dir() and path.name.startswith(prefix))
    return ids[-1] if ids else "无"


def stage_reference_docs(stage: str) -> list[str]:
    return list(STAGE_REFERENCE_DOCS.get(stage, []))


def next_dir_id(project_root: Path, relative_dir: str, prefix: str) -> str:
    root = project_root / relative_dir
    root.mkdir(parents=True, exist_ok=True)
    existing: list[int] = []
    for path in root.iterdir():
        if not path.is_dir() or not path.name.startswith(prefix):
            continue
        try:
            existing.append(int(path.name.split("-")[1]))
        except Exception:
            continue
    return f"{prefix}{max(existing, default=0) + 1:03d}"


def copy_relative_if_exists(project_root: Path, relative: str, target_dir: Path) -> list[str]:
    source = project_root / relative
    if not source.exists():
        return []
    target = target_dir / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return [relative]


def render_project_index(config: dict, task_count: int, change_count: int, bug_count: int, pr_count: int, merged_pr_count: int) -> str:
    active_role_text = "、".join(role_titles(config, config.get("stage", ""))) or "待确定"
    tech_profile = current_tech_profile(config)
    design_assets = design_asset_records(config)
    return textwrap.dedent(
        f"""
        # 项目索引

        - 项目名称：{config.get('project_name', '未命名项目')}
        - 当前模式：{config.get('active_mode', '未知')}
        - 当前阶段：{config.get('stage', '未知')}
        - 项目负责人：{config.get('owner', '未知')}
        - 技术栈：{config.get('stack', '未知')}
        - 当前技术画像：{tech_profile.get('title', '未设置') or '未设置'}
        - 设计交付物数：{len(design_assets)}
        - 当前阶段主要角色：{active_role_text}

        ## 项目创意摘要

        {config.get('idea', '待补充。')}

        ## 项目概况

        - 任务数：{task_count}
        - 变更数：{change_count}
        - 缺陷数：{bug_count}
        - 活跃 PR 数：{pr_count}
        - 已合并 PR 数：{merged_pr_count}
        - AI 入口：`/.factory/memory/runtime-brief.md`、`/.factory/memory/role-charter.project.md`、`/.factory/memory/current-state.md`、`/.factory/memory/doc-map.md`
        """
    ).strip()


def render_current_state(config: dict, tasks: list[dict], changes: list[dict], bugs: list[dict], prs: list[dict]) -> str:
    active_tasks = [item for item in tasks if item["status"] not in CLOSED_STATUSES]
    active_changes = [item for item in changes if item["status"] not in CLOSED_STATUSES]
    active_bugs = [item for item in bugs if item["status"] not in CLOSED_STATUSES]
    active_prs = active_pr_records(prs)

    def latest(items: list[dict]) -> str:
        if not items:
            return "无"
        return "、".join(item["id"] for item in items[-3:])

    active_role_text = "、".join(role_titles(config, config.get("stage", ""))) or "待确定"
    total_roles = len(ensure_role_catalog(config))
    tech_profile = current_tech_profile(config)
    design_assets = design_asset_records(config)

    return textwrap.dedent(
        f"""
        # 当前状态

        - 当前模式：{config.get('active_mode', '未知')}
        - 当前阶段：{config.get('stage', '未知')}
        - 活跃任务：{len(active_tasks)}
        - 活跃变更：{len(active_changes)}
        - 活跃缺陷：{len(active_bugs)}
        - 活跃 PR：{len(active_prs)}

        - 角色目录总数：{total_roles}
        - 当前阶段主要角色：{active_role_text}

        - 当前技术画像：{tech_profile.get('title', '未设置') or '未设置'}
        - 技术画像预设：{tech_profile.get('preset', 'custom')}
        - 关键工程规则数：{len(tech_profile.get('rules', []))}
        - 设计交付物数：{len(design_assets)}

        ## 最近条目

        - 任务：{latest(tasks)}
        - 变更：{latest(changes)}
        - 缺陷：{latest(bugs)}

        ## 下一步建议

        - 检查任务人天估算是否真实合理，仅在必要时再细化到 0.5 人天精度
        - 若进入设计或实施阶段，先确认 `docs/03-solution/technical-selection.md` 已明确框架、模块、后台范围和编码规则
        - 若 UX/UI 需要可视化评审，优先登记真实设计交付物而不是只写文字
        - 若工作项进入收尾，确认关联 PR 已完成评审并合并
        - 阶段切换前先更新正式文档，再刷新 `/.factory/memory/` 压缩记忆
        """
    ).strip()


def render_item_summary(title: str, items: list[dict]) -> str:
    lines = [f"# {title}", ""]
    if not items:
        lines.append("暂无记录。")
        return "\n".join(lines)

    for item in items:
        lines.append(f"- `{item['id']}` {item['title']}")
        lines.append(
            f"  状态：{item['status']} | 负责人：{item['owner']} | 预估：{item['hours']} | 关联：{item['links']}"
        )
    return "\n".join(lines)


def render_change_summary(changes: list[dict], bugs: list[dict]) -> str:
    lines = ["# 变更摘要", ""]
    if not changes and not bugs:
        lines.append("暂无变更或缺陷记录。")
        return "\n".join(lines)

    if changes:
        lines.append("## 需求变更")
        for item in changes:
            lines.append(f"- `{item['id']}` {item['title']} | 状态：{item['status']} | 关联：{item['links']}")
        lines.append("")
    if bugs:
        lines.append("## 缺陷修复")
        for item in bugs:
            lines.append(f"- `{item['id']}` {item['title']} | 状态：{item['status']} | 关联：{item['links']}")
    return "\n".join(lines).strip()


def render_technical_profile_summary(config: dict) -> str:
    profile = current_tech_profile(config)
    lines = [
        "# 技术画像摘要",
        "",
        f"- 当前画像：{profile.get('title', '未设置') or '未设置'}",
        f"- 预设：{profile.get('preset', 'custom')}",
        f"- 技术栈：{profile.get('stack') or config.get('stack', '未知')}",
        f"- 最近更新时间：{profile.get('applied_at', '未记录') or '未记录'}",
        "",
    ]
    if profile.get("summary"):
        lines.extend(["## 摘要", "", profile["summary"], ""])
    sections = [
        ("## 项目范围", profile.get("projects", [])),
        ("## 必装/必选模块", profile.get("modules", [])),
        ("## 关键工程规则", profile.get("rules", [])),
        ("## 管理后台要求", profile.get("admin_requirements", [])),
        ("## 强制技能", [item.get("name", "") for item in tech_required_skill_records(config)]),
        ("## 推荐初始化动作", profile.get("commands", [])),
        ("## 参考资料", profile.get("guides", [])),
    ]
    for header, values in sections:
        lines.extend([header, ""])
        if values:
            lines.extend(f"- {item}" for item in values)
        else:
            lines.append("- 暂无。")
        lines.append("")
    return "\n".join(lines).strip()


def render_design_assets_summary(config: dict) -> str:
    records = design_asset_records(config)
    lines = [
        "# 设计交付物摘要",
        "",
        f"- 交付物数：{len(records)}",
        f"- 最近更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if not records:
        lines.append("暂无已登记的设计交付物。")
        return "\n".join(lines)

    lines.extend(["## 最近交付物", ""])
    for record in records[-10:]:
        ui_text = record.get("ui_id", "") or "未绑定"
        kind = record.get("kind", "设计交付物")
        files = "、".join(record.get("files", [])) or "无"
        links = "、".join(record.get("links", [])) or "无"
        lines.append(
            f"- `{record['id']}` {record.get('title', '未命名交付物')} | 类型：{kind} | 关联 UI：{ui_text} | 文件：{files} | 链接：{links}"
        )
    return "\n".join(lines).strip()


def write_history_snapshot(project_root: Path, current_state: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    history_path = project_root / FACTORY_MEMORY_RELATIVE / "history" / f"{timestamp}-state.md"
    snapshot = textwrap.dedent(
        f"""
        # AI 记忆快照

        - 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        {current_state}
        """
    ).strip()
    write_text(history_path, snapshot)
    return history_path


def refresh_ai_memory(project_root: Path) -> Path:
    ensure_project(project_root)
    config = load_project_config(project_root)
    tasks = collect_items(project_root, workitems_file("implementation"), "TASK")
    changes = collect_items(project_root, workitems_file("changes"), "CR")
    bugs = collect_items(project_root, workitems_file("bugs"), "BUG")
    prs = load_pr_records(project_root)

    project_index = render_project_index(
        config,
        len(tasks),
        len(changes),
        len(bugs),
        len(active_pr_records(prs)),
        len(merged_pr_records(prs)),
    )
    current_state = render_current_state(config, tasks, changes, bugs, prs)
    task_summary = render_item_summary("任务摘要", tasks)
    change_summary = render_change_summary(changes, bugs)
    pr_summary = render_pr_summary(prs)
    remote_pr_summary = render_remote_pr_summary(prs)
    tech_summary = render_technical_profile_summary(config)
    design_assets_summary = render_design_assets_summary(config)

    write_text(project_root / PROJECT_INDEX_RELATIVE, project_index)
    write_text(project_root / CURRENT_STATE_RELATIVE, current_state)
    write_text(project_root / TASKS_SUMMARY_RELATIVE, task_summary)
    write_text(project_root / CHANGE_SUMMARY_RELATIVE, change_summary)
    write_text(project_root / PR_SUMMARY_RELATIVE, pr_summary)
    write_text(project_root / REMOTE_PR_SUMMARY_RELATIVE, remote_pr_summary)
    write_text(project_root / TECH_STACK_SUMMARY_RELATIVE, tech_summary)
    write_text(project_root / DESIGN_ASSETS_SUMMARY_RELATIVE, design_assets_summary)
    return write_history_snapshot(project_root, current_state)
