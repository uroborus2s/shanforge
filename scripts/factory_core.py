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
import uuid
from contextlib import contextmanager
from datetime import datetime
from functools import lru_cache
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

import fcntl


FACTORY_DIR_RELATIVE = ".factory"
FACTORY_MEMORY_RELATIVE = f"{FACTORY_DIR_RELATIVE}/memory"
FACTORY_PROCESS_RELATIVE = f"{FACTORY_DIR_RELATIVE}/process"
FACTORY_WORKITEMS_RELATIVE = f"{FACTORY_DIR_RELATIVE}/workitems"
INTENT_APPROVAL_ROOT_ENV = "SHANFORGE_INTENT_APPROVAL_ROOT"
DOCS_STRATEGO_PACKAGE_SPEC_ENV = "DOCS_STRATEGO_PACKAGE_SPEC"
DEFAULT_UV_CACHE_DIR = "/tmp/uv-cache"


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
RUNTIME_BRIEF_RELATIVE = memory_file("runtime-brief.md")
ROLE_CHARTER_PROJECT_RELATIVE = memory_file("role-charter.project.md")
DOC_MAP_RELATIVE = memory_file("doc-map.md")
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
        "modules": ["Python 3.14+", "uv", "pytest", "ruff", "mypy"],
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
    "crawler4j-model": {
        "id": "crawler4j-model",
        "title": "Crawler4j Model 项目画像",
        "stack": "python + crawler4j sdk cli + model/module project",
        "summary": "适用于使用 crawler4j SDK CLI 创建和维护标准 model/模块项目，强调 `module.yaml` 契约、CLI 脚手架、DevLink/ATM 调试和 zip 安装验收。",
        "projects": ["Crawler4j 标准模块项目", "Crawler4j Core 模块开发与验证"],
        "modules": ["Python 3.12+", "uv", "crawler4j-sdk CLI", "module.yaml", "TaskScript / TaskFlow", "DevLink / ATM 调试链路"],
        "rules": [
            "创建或补齐模块骨架时优先使用 `crawler4j init-model`、`crawler4j new`、`crawler4j add-workflow`、`crawler4j add-ui`，不要先手写脚手架。",
            "模块运行契约以 `module.yaml` 和模块根 `__init__.py` 为准，不把 wheel 元数据当成 Core 加载依据。",
            "新增运行时依赖时，同时确认宿主 `crawler4j` 环境可用；不要只改模块项目 `pyproject.toml`。",
            "调试与验收优先走 DevLink / ATM 调试与 zip 安装 smoke，避免依赖旧版临时调试脚本。",
            "改动 SDK CLI、模板、模块契约或 Core 集成行为时，同时更新模块开发文档与回归测试。",
        ],
        "admin_requirements": [],
        "commands": [
            "优先执行 `uvx --from crawler4j-sdk crawler4j init-model <module_name>` 创建模块项目，默认使用 PyPI 最新发布版本；脚本化场景加 `--defaults --no-git --no-install`。",
            "进入模块项目后优先执行 `uv run crawler4j new <task_name>`、`uv run crawler4j add-workflow <workflow_name>`、`uv run crawler4j add-ui`。",
            "在 crawler4j Core 源码仓验证本地 CLI 时，优先执行 `uv run python -m crawler4j_sdk.cli.commands --help`。",
        ],
        "guides": [
            "skills/crawler4j-model-project/SKILL.md",
            "skills/crawler4j-model-project/references/cli-workflow.md",
            "skills/crawler4j-model-project/references/module-structure.md",
            "skills/crawler4j-model-project/references/core-integration.md",
        ],
        "required_skills": ["crawler4j-model-project", "python-uv-project", "tdd-workflow"],
        "role_required_skills": {
            "solution-architect": ["crawler4j-model-project", "python-uv-project"],
            "backend-engineer": ["crawler4j-model-project", "python-uv-project", "tdd-workflow"],
            "frontend-engineer": ["crawler4j-model-project"],
            "qa-engineer": ["crawler4j-model-project", "python-uv-project", "tdd-workflow"],
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
        "docs/04-project-development/01-governance/project-charter.md",
        "docs/04-project-development/02-discovery/input.md",
        "docs/04-project-development/02-discovery/brainstorm-record.md",
    ],
    "REQUIREMENTS": [
        "docs/04-project-development/03-requirements/prd.md",
        "docs/04-project-development/03-requirements/requirements-analysis.md",
        "docs/04-project-development/03-requirements/requirements-verification.md",
    ],
    "ANALYSIS": [
        "docs/04-project-development/03-requirements/requirements-analysis.md",
        "docs/04-project-development/03-requirements/requirements-verification.md",
        "docs/04-project-development/10-traceability/requirements-matrix.md",
    ],
    "DESIGN": [
        "docs/04-project-development/04-design/system-architecture.md",
        "docs/04-project-development/04-design/technical-selection.md",
        "docs/04-project-development/04-design/module-boundaries.md",
        "docs/04-project-development/04-design/api-design.md",
        "docs/04-project-development/04-design/backend-design.md",
        "docs/04-project-development/04-design/database-design.md",
        "docs/04-project-development/04-design/ux-ui-design.md",
    ],
    "PLAN": [
        "docs/04-project-development/04-design/technical-selection.md",
        "docs/04-project-development/04-design/module-boundaries.md",
        "docs/04-project-development/05-development-process/wbs.md",
        "docs/04-project-development/05-development-process/task-breakdown.md",
        "docs/04-project-development/05-development-process/implementation-plan.md",
    ],
    "IMPLEMENTATION": [
        "docs/04-project-development/04-design/technical-selection.md",
        "docs/04-project-development/04-design/module-boundaries.md",
        EXECUTION_LOG_RELATIVE,
        "docs/04-project-development/06-testing-verification/test-plan.md",
    ],
    "TESTING": [
        "docs/04-project-development/06-testing-verification/test-plan.md",
        "docs/04-project-development/06-testing-verification/test-cases.md",
        "docs/04-project-development/06-testing-verification/test-report.md",
    ],
    "ACCEPTANCE": [
        "docs/04-project-development/07-release-delivery/acceptance-checklist.md",
        "docs/04-project-development/07-release-delivery/delivery-package.md",
        STAGE_CHECK_REPORT_RELATIVE,
        QUALITY_CHECK_REPORT_RELATIVE,
    ],
    "RELEASE": [
        "docs/04-project-development/07-release-delivery/release-notes.md",
        "docs/04-project-development/07-release-delivery/delivery-package.md",
        "docs/04-project-development/08-operations-maintenance/deployment-guide.md",
        "docs/02-user-guide/user-guide.md",
    ],
    "MAINTENANCE": [
        "docs/04-project-development/08-operations-maintenance/operations-runbook.md",
        "docs/02-user-guide/user-guide.md",
        "docs/04-project-development/09-evolution/retrospective.md",
        "docs/04-project-development/10-traceability/requirements-matrix.md",
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
        "docs/04-project-development/04-design/technical-selection.md",
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
            "docs/04-project-development/01-governance/project-charter.md",
            "docs/04-project-development/02-discovery/input.md",
            "docs/04-project-development/02-discovery/brainstorm-record.md",
            "docs/04-project-development/03-requirements/prd.md",
            "docs/04-project-development/03-requirements/requirements-analysis.md",
            "docs/04-project-development/03-requirements/requirements-verification.md",
            "docs/04-project-development/10-traceability/requirements-matrix.md",
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
            "docs/04-project-development/04-design/technical-selection.md",
            "docs/04-project-development/04-design/system-architecture.md",
            "docs/04-project-development/04-design/module-boundaries.md",
            "docs/04-project-development/04-design/api-design.md",
            "docs/04-project-development/04-design/backend-design.md",
            "docs/04-project-development/04-design/database-design.md",
            "docs/04-project-development/10-traceability/requirements-matrix.md",
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
            "docs/04-project-development/04-design/technical-selection.md",
            "docs/04-project-development/04-design/ux-ui-design.md",
            "docs/04-project-development/04-design/system-architecture.md",
            "docs/04-project-development/04-design/module-boundaries.md",
            "docs/04-project-development/05-development-process/wbs.md",
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
            "docs/04-project-development/04-design/technical-selection.md",
            "docs/04-project-development/04-design/module-boundaries.md",
        "docs/04-project-development/04-design/backend-design.md",
        "docs/04-project-development/04-design/api-design.md",
        "docs/04-project-development/05-development-process/implementation-plan.md",
        EXECUTION_LOG_RELATIVE,
        "docs/04-project-development/06-testing-verification/test-plan.md",
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
            "docs/04-project-development/04-design/technical-selection.md",
        "docs/04-project-development/04-design/ux-ui-design.md",
        "docs/04-project-development/04-design/system-architecture.md",
        "docs/04-project-development/05-development-process/implementation-plan.md",
        EXECUTION_LOG_RELATIVE,
        "docs/04-project-development/06-testing-verification/test-plan.md",
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
        "docs/04-project-development/06-testing-verification/test-plan.md",
        "docs/04-project-development/06-testing-verification/test-cases.md",
        "docs/04-project-development/06-testing-verification/test-report.md",
        STAGE_CHECK_REPORT_RELATIVE,
        QUALITY_CHECK_REPORT_RELATIVE,
        "docs/04-project-development/10-traceability/requirements-matrix.md",
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
            "docs/04-project-development/07-release-delivery/delivery-package.md",
            "docs/04-project-development/07-release-delivery/release-notes.md",
            "docs/04-project-development/08-operations-maintenance/deployment-guide.md",
            "docs/02-user-guide/user-guide.md",
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
            "docs/04-project-development/10-traceability/requirements-matrix.md",
        ],
    },
)

DOCS_STRATEGO_TOP_LEVEL_ORDER = [
    "01-getting-started",
    "02-user-guide",
    "03-developer-guide",
    "04-project-development",
]
DOCS_STRATEGO_DIRECTORY_SPECS = {
    "01-getting-started": {
        "title": "入门说明",
        "root_access": "public",
        "description": "本目录收纳产品定位、快速开始、阅读路径和文档地图等入门材料。",
        "order": [
            "project-overview.md",
            "quick-start.md",
            "document-map.md",
        ],
    },
    "02-user-guide": {
        "title": "用户指南",
        "root_access": "public",
        "description": "本目录收纳面向最终用户和协作者的使用指南、提示词速查和命令速查。",
        "order": [
            "user-guide.md",
            "prompt-templates.md",
            "command-cheatsheet.md",
        ],
    },
    "03-developer-guide": {
        "title": "开发者指南",
        "root_access": "public",
        "description": "本目录收纳 module 开发、调试、交付与排错等面向开发者的正式指南内容。",
        "order": [
            "01-concepts",
            "02-quickstart",
            "03-project-structure",
            "04-development",
            "05-debugging",
            "06-delivery",
            "07-troubleshooting",
        ],
    },
    "03-developer-guide/01-concepts": {
        "title": "01 概念与约束",
        "description": "本目录收纳系统地图、术语和真实约束等开发前必读内容。",
        "order": [
            "01-system-map.md",
            "02-real-constraints.md",
        ],
    },
    "03-developer-guide/02-quickstart": {
        "title": "02 快速开始",
        "description": "本目录收纳环境准备和创建首个模块的最小路径。",
        "order": [
            "01-environment-setup.md",
            "02-create-first-module.md",
        ],
    },
    "03-developer-guide/03-project-structure": {
        "title": "03 项目结构与契约",
        "description": "本目录收纳目录布局、入口和 `module.yaml` 契约说明。",
        "order": [
            "01-layout-and-entrypoints.md",
            "02-module-manifest.md",
        ],
    },
    "03-developer-guide/04-development": {
        "title": "04 模块开发",
        "description": "本目录收纳 TaskScript、Workflow、CLI/UI 配置和 Core 能力说明。",
        "order": [
            "01-taskscript.md",
            "02-workflow.md",
            "03-cli-and-ui.md",
            "04-core-capabilities.md",
        ],
    },
    "03-developer-guide/05-debugging": {
        "title": "05 调试",
        "description": "本目录收纳 DevLink 与真实调试链路说明。",
        "order": [
            "01-devlink-and-debug.md",
        ],
    },
    "03-developer-guide/06-delivery": {
        "title": "06 交付与验收",
        "description": "本目录收纳 zip 安装、交付和验收清单。",
        "order": [
            "01-zip-installation.md",
            "02-acceptance-checklist.md",
        ],
    },
    "03-developer-guide/07-troubleshooting": {
        "title": "07 排错",
        "description": "本目录收纳常见问题、排错路径和已知坑位。",
        "order": [
            "01-common-pitfalls.md",
        ],
    },
    "04-project-development": {
        "title": "项目开发文档（内）",
        "root_access": "private",
        "description": "本目录收纳内部项目治理、需求、设计、过程控制、测试、发布、运维和追踪矩阵等正式开发文档。",
        "order": [
            "01-governance",
            "02-discovery",
            "03-requirements",
            "04-design",
            "05-development-process",
            "06-testing-verification",
            "07-release-delivery",
            "08-operations-maintenance",
            "09-evolution",
            "10-traceability",
        ],
    },
    "04-project-development/01-governance": {
        "title": "项目治理",
        "description": "本目录收纳项目目标、边界、角色分工和治理约束。",
        "order": [
            "project-charter.md",
            "stakeholders-raci.md",
            "risk-register.md",
            "glossary.md",
            "roadmap.md",
        ],
    },
    "04-project-development/02-discovery": {
        "title": "调研与决策",
        "description": "本目录收纳调研输入、现状分析、头脑风暴和问题空间澄清结果。",
        "order": [
            "input.md",
            "brainstorm-record.md",
            "business-flow.md",
            "scope-outline.md",
        ],
    },
    "04-project-development/03-requirements": {
        "title": "需求",
        "description": "本目录收纳需求、需求分析、校验和变更控制文档。",
        "order": [
            "prd.md",
            "requirements-analysis.md",
            "requirements-verification.md",
            "changelog.md",
            "nfr-catalog.md",
            "acceptance-criteria.md",
            "change-requests.md",
        ],
    },
    "04-project-development/04-design": {
        "title": "设计文档",
        "description": "本目录收纳总体设计、详细设计、UX/UI 设计、接口设计、部署与 CI/CD 设计等方案文档。",
        "order": [
            "solution-overview.md",
            "technical-selection.md",
            "system-architecture.md",
            "module-boundaries.md",
            "api-design.md",
            "backend-design.md",
            "database-design.md",
            "security-design.md",
            "deployment-architecture.md",
            "ux-ui-design.md",
            "source-docs-standard-upgrade-analysis.md",
            "assets",
            "adr",
            "contracts",
            "private-design",
        ],
    },
    "04-project-development/05-development-process": {
        "title": "开发过程文档",
        "description": "本目录收纳实施计划、任务拆分、执行节奏和交付组织材料。",
        "order": [
            "software-development-process.md",
            "wbs.md",
            "implementation-plan.md",
            "task-breakdown.md",
            "iteration-plan.md",
            "migration-plan.md",
            "execution-log.md",
            "daily-status.md",
            "risk-register.md",
            "multi-agent-board.md",
            "role-assignments.md",
            "role-handoffs.md",
            "role-sync.md",
            "team-sync.md",
            "chat-bootstrap.md",
            "pull-requests.md",
            "pr-board.md",
            "pr-handovers.md",
            "remote-prs.md",
            "role-retrospectives",
            "team-retro.md",
            "dev-setup.md",
        ],
    },
    "04-project-development/06-testing-verification": {
        "title": "测试与验证",
        "description": "本目录收纳测试策略、测试用例、执行结果和质量结论。",
        "order": [
            "test-strategy.md",
            "test-plan.md",
            "test-cases.md",
            "test-data.md",
            "defect-log.md",
            "test-report.md",
            "uat-report.md",
        ],
    },
    "04-project-development/07-release-delivery": {
        "title": "发布与交付",
        "description": "本目录收纳验收、发布、交付和回滚相关文档。",
        "order": [
            "acceptance-checklist.md",
            "pr-check-report.md",
            "stage-check-report.md",
            "quality-check-report.md",
            "state-doctor-report.md",
            "delivery-package.md",
            "release-checklist.md",
            "release-notes.md",
            "rollback-plan.md",
            "production-readiness-review.md",
            "role-reviews.md",
            "role-closeouts.md",
            "team-closeouts.md",
        ],
    },
    "04-project-development/08-operations-maintenance": {
        "title": "运维与维护",
        "description": "本目录收纳部署、运行、监控、故障处理和支持手册。",
        "order": [
            "deployment-guide.md",
            "operations-runbook.md",
            "monitoring-alerting.md",
            "incident-playbook.md",
            "backup-dr.md",
            "support-handbook.md",
            "configuration-matrix.md",
        ],
    },
    "04-project-development/09-evolution": {
        "title": "演进复盘",
        "description": "本目录收纳复盘、问题模式和后续演进决策。",
        "order": [
            "skill-evolution-plan.md",
            "retrospective.md",
            "postmortem.md",
            "deprecation-plan.md",
            "agent-motivation-autonomy-integration.md",
        ],
    },
    "04-project-development/10-traceability": {
        "title": "追踪矩阵",
        "description": "本目录收纳跨阶段的矩阵、索引和覆盖关系。",
        "order": [
            "requirements-matrix.md",
            "interface-matrix.md",
            "document-index.md",
        ],
    },
}
DOCS_STRATEGO_DIRECTORY_TITLE_OVERRIDES = {
    "adr": "架构决策记录",
    "contracts": "接口契约",
    "api": "API 契约",
    "openapi": "OpenAPI 契约",
    "events": "事件契约",
    "internal": "内部接口",
    "schemas": "数据 Schema",
    "tools": "工具契约（MCP）",
    "private-design": "内部专题",
    "role-retrospectives": "角色复盘",
}
DOCS_STRATEGO_OPENAPI_SUFFIXES = (
    ".openapi.yaml",
    ".openapi.yml",
    ".openapi.json",
)
DOCS_STRATEGO_MCP_TOOLS_SUFFIXES = (
    ".mcp-tools.yaml",
    ".mcp-tools.yml",
    ".mcp-tools.json",
)
DOCS_STRATEGO_CONTRACT_SUFFIXES = DOCS_STRATEGO_OPENAPI_SUFFIXES + DOCS_STRATEGO_MCP_TOOLS_SUFFIXES
DOCS_STRATEGO_PAGE_SUFFIXES = (".md", *DOCS_STRATEGO_CONTRACT_SUFFIXES)
DOCS_STRATEGO_ACCESS_LEVELS = {"public", "private"}
DOCS_PROFILE_TOP_LEVEL_ALIASES = {
    "01-getting-started": "01-getting-started",
    "getting-started": "01-getting-started",
    "getting_started": "01-getting-started",
    "入门说明": "01-getting-started",
    "02-user-guide": "02-user-guide",
    "user-guide": "02-user-guide",
    "user_guide": "02-user-guide",
    "用户指南": "02-user-guide",
    "03-developer-guide": "03-developer-guide",
    "developer-guide": "03-developer-guide",
    "developer_guide": "03-developer-guide",
    "开发者指南": "03-developer-guide",
    "04-project-development": "04-project-development",
    "project-development": "04-project-development",
    "project_development": "04-project-development",
    "项目开发文档（内）": "04-project-development",
    "项目开发文档": "04-project-development",
}
DOCS_PROFILE_STATES = {"required", "optional", "omit"}
DOCS_PROFILE_SCAN_SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
}
DOCS_PROFILE_INTERESTING_FILENAMES = {
    "readme.md",
    "readme",
    "mkdocs.yml",
    "mkdocs.yaml",
    "pyproject.toml",
    "package.json",
    "module.yaml",
    "openapi.yaml",
    "openapi.yml",
    "openapi.json",
    "asyncapi.yaml",
    "asyncapi.yml",
    "asyncapi.json",
    "mcp-tools.yaml",
    "mcp-tools.yml",
    "mcp-tools.json",
}
DOCS_MACHINE_PATH_PATTERN = re.compile(r"/Users/|/absolute/path")
MARKDOWN_LINK_PATTERN = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target>[^)]+)(?P<suffix>\))")
EXPLICIT_HTML_ANCHOR_PATTERN = re.compile(
    r"<(?:a|span|div)\b[^>]*\bid=(?:\"([^\"]+)\"|'([^']+)')[^>]*>",
    re.IGNORECASE,
)
LEGACY_DOCS_DIRECTORY_MAP = {
    "00-governance": "04-project-development/01-governance",
    "01-discovery": "04-project-development/02-discovery",
    "02-requirements": "04-project-development/03-requirements",
    "03-solution": "04-project-development/04-design",
    "04-delivery": "04-project-development/05-development-process",
    "05-quality": "04-project-development/06-testing-verification",
    "06-release": "04-project-development/07-release-delivery",
    "07-operations": "04-project-development/08-operations-maintenance",
    "08-handover": "02-user-guide",
    "09-evolution": "04-project-development/09-evolution",
    "traceability": "04-project-development/10-traceability",
}


def docs_profile_base() -> dict:
    return {
        "project_kind": "application",
        "audiences": ["maintainer"],
        "surfaces": {
            "end_user_usage": True,
            "public_api": False,
            "sdk": False,
            "plugin_extensibility": False,
            "secondary_development": False,
            "self_hosted": False,
        },
        "modules": {
            "01-getting-started": "required",
            "02-user-guide": "required",
            "03-developer-guide": "omit",
            "04-project-development": "required",
        },
        "reasons": {},
    }


def docs_profile_module_key(value: str | None) -> str | None:
    if not value:
        return None
    candidate = value.strip()
    if candidate in DOCS_PROFILE_TOP_LEVEL_ALIASES:
        return DOCS_PROFILE_TOP_LEVEL_ALIASES[candidate]
    return DOCS_PROFILE_TOP_LEVEL_ALIASES.get(normalize_key(candidate))


def normalize_docs_profile(raw: dict | None) -> dict:
    profile = docs_profile_base()
    if not isinstance(raw, dict):
        return profile

    project_kind = str(raw.get("project_kind", "")).strip()
    if project_kind:
        profile["project_kind"] = project_kind

    audiences = raw.get("audiences", [])
    if isinstance(audiences, list):
        profile["audiences"] = unique_preserve(str(item) for item in audiences if str(item).strip()) or ["maintainer"]

    surfaces = raw.get("surfaces", {})
    if isinstance(surfaces, dict):
        normalized_surfaces = dict(profile["surfaces"])
        for key in normalized_surfaces:
            if key in surfaces:
                normalized_surfaces[key] = bool(surfaces[key])
        profile["surfaces"] = normalized_surfaces

    modules = raw.get("modules", {})
    if isinstance(modules, dict):
        normalized_modules = dict(profile["modules"])
        for raw_key, raw_state in modules.items():
            module_key = docs_profile_module_key(str(raw_key))
            state = str(raw_state).strip()
            if not module_key or state not in DOCS_PROFILE_STATES:
                continue
            normalized_modules[module_key] = state
        profile["modules"] = normalized_modules

    reasons = raw.get("reasons", {})
    if isinstance(reasons, dict):
        normalized_reasons: dict[str, str] = {}
        for raw_key, value in reasons.items():
            module_key = docs_profile_module_key(str(raw_key))
            if module_key and str(value).strip():
                normalized_reasons[module_key] = str(value).strip()
        profile["reasons"] = normalized_reasons

    for field in ["detected_at", "source"]:
        if str(raw.get(field, "")).strip():
            profile[field] = str(raw[field]).strip()

    return profile


def docs_profile_module_state(docs_profile: dict | None, module_key: str) -> str:
    profile = normalize_docs_profile(docs_profile)
    return str(profile.get("modules", {}).get(module_key, "omit"))


def docs_profile_module_enabled(docs_profile: dict | None, module_key: str, docs_root: Path | None = None) -> bool:
    state = docs_profile_module_state(docs_profile, module_key)
    if state == "required":
        return True
    if state == "optional" and docs_root is not None:
        return (docs_root / module_key).exists()
    return False


def docs_profile_enabled_top_levels(docs_profile: dict | None, docs_root: Path | None = None) -> list[str]:
    profile = normalize_docs_profile(docs_profile)
    return [
        module_key
        for module_key in DOCS_STRATEGO_TOP_LEVEL_ORDER
        if docs_profile_module_enabled(profile, module_key, docs_root)
    ]


def docs_profile_required_top_levels(docs_profile: dict | None) -> list[str]:
    profile = normalize_docs_profile(docs_profile)
    return [
        module_key
        for module_key in DOCS_STRATEGO_TOP_LEVEL_ORDER
        if docs_profile_module_state(profile, module_key) == "required"
    ]


def docs_relative_path_enabled(relative_path: str, docs_profile: dict | None, docs_root: Path | None = None) -> bool:
    relative = normalize_posix_relative(relative_path)
    if relative.startswith("docs/"):
        relative = relative[5:]
    top_level = relative.split("/", 1)[0] if relative else ""
    if top_level not in DOCS_STRATEGO_TOP_LEVEL_ORDER:
        return True
    return docs_profile_module_enabled(docs_profile, top_level, docs_root)


def filter_relative_doc_paths(paths: Sequence[str], docs_profile: dict | None, docs_root: Path | None = None) -> list[str]:
    return [item for item in paths if docs_relative_path_enabled(item, docs_profile, docs_root)]


def contains_any_keyword(text: str, keywords: Sequence[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def collect_docs_profile_signals(project_root: Path, *, project_name: str = "", idea: str = "", stack: str = "") -> dict:
    lower_name = project_name.lower()
    lower_idea = idea.lower()
    lower_stack = stack.lower()
    file_names: list[str] = []
    content_chunks: list[str] = []
    scanned_files = 0

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [
            item
            for item in dirs
            if item not in DOCS_PROFILE_SCAN_SKIP_DIRS and not item.startswith(".codex")
        ]
        for filename in files:
            scanned_files += 1
            if scanned_files > 2000:
                break
            path = Path(root) / filename
            try:
                relative = path.relative_to(project_root).as_posix()
            except ValueError:
                continue
            lower_relative = relative.lower()
            file_names.append(lower_relative)
            if (
                filename.lower() in DOCS_PROFILE_INTERESTING_FILENAMES
                or lower_relative.startswith("docs/")
                or lower_relative.endswith((".md", ".yaml", ".yml", ".toml", ".json"))
            ):
                try:
                    text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
                except Exception:
                    text = ""
                if text:
                    content_chunks.append(text.lower())
            if len(content_chunks) >= 40:
                continue
        if scanned_files > 2000:
            break

    signal_text = "\n".join([lower_name, lower_idea, lower_stack, *file_names, *content_chunks])
    return {
        "text": signal_text,
        "files": file_names,
    }


def detect_docs_profile(project_root: Path, *, project_name: str = "", idea: str = "", stack: str = "") -> dict:
    signals = collect_docs_profile_signals(project_root, project_name=project_name, idea=idea, stack=stack)
    text = signals["text"]
    files = signals["files"]
    docs_root = project_root / "docs"
    existing_modules = {
        module_key
        for module_key in DOCS_STRATEGO_TOP_LEVEL_ORDER
        if (docs_root / module_key).exists()
    }

    has_docs_site = contains_any_keyword(
        text,
        [
            "章略·墨衡",
            "docs-stratego",
            "mkdocs",
            "文档站点",
            "documentation site",
            "docs site",
        ],
    )
    negative_secondary_dev = contains_any_keyword(
        text,
        [
            "不提供 sdk",
            "不提供sdk",
            "不提供插件",
            "不提供对外 api",
            "不提供对外api",
            "不提供公共 api",
            "不提供公共api",
            "without sdk",
            "without plugin",
            "no public api",
            "no sdk",
            "no plugin",
        ],
    )
    has_public_api = any(
        name.endswith(("openapi.yaml", "openapi.yml", "openapi.json", "asyncapi.yaml", "asyncapi.yml", "asyncapi.json"))
        or name.endswith(DOCS_STRATEGO_OPENAPI_SUFFIXES)
        for name in files
    ) or (
        not negative_secondary_dev
        and contains_any_keyword(text, ["openapi", "asyncapi", "graphql", "public api", "对外接口", "rest api"])
    )
    has_mcp_tools = any(name.endswith(DOCS_STRATEGO_MCP_TOOLS_SUFFIXES) for name in files) or (
        not negative_secondary_dev
        and contains_any_keyword(text, ["mcp tools", "agent tools", "mcp 工具", "工具契约"])
    )
    has_plugin = any(part in name for name in files for part in ("plugin", "plugins/", "module.yaml", "extension", "extensions")) or (
        not negative_secondary_dev
        and contains_any_keyword(text, ["插件开发", "plugin", "hook", "扩展点", "extension"])
    )
    has_sdk = not negative_secondary_dev and contains_any_keyword(
        text,
        [" sdk", "sdk ", "client library", "开发包", "framework", "library", "二次开发"],
    )
    has_secondary_development = has_public_api or has_mcp_tools or has_plugin or has_sdk or contains_any_keyword(
        text,
        ["开发者指南", "developer guide", "集成指南", "integration", "二次开发", "开发者"],
    )
    has_end_user_usage = contains_any_keyword(
        text,
        [
            "用户指南",
            "user guide",
            "安装",
            "配置",
            "使用说明",
            "usage",
            "quick start",
            "cli",
            "command",
            "命令",
        ],
    ) or any(name.startswith("scripts/") for name in files)
    has_self_hosted = contains_any_keyword(
        text,
        ["docker", "docker-compose", "helm", "kubernetes", "部署", "运维", "self-hosted"],
    ) or any(
        name.endswith(("docker-compose.yml", "docker-compose.yaml", "helmfile.yaml", "helmfile.yml"))
        for name in files
    )

    if has_docs_site and not has_secondary_development:
        project_kind = "docs_site"
    elif has_sdk and not has_end_user_usage:
        project_kind = "sdk_or_framework"
    elif contains_any_keyword(text, ["cli", "命令行", "tooling", "脚本工具"]) and not has_secondary_development:
        project_kind = "cli_tool"
    else:
        project_kind = "application"

    profile = docs_profile_base()
    profile["project_kind"] = project_kind
    profile["surfaces"] = {
        "end_user_usage": bool(has_end_user_usage or has_docs_site),
        "public_api": bool(has_public_api),
        "sdk": bool(has_sdk),
        "plugin_extensibility": bool(has_plugin),
        "secondary_development": bool(has_secondary_development),
        "self_hosted": bool(has_self_hosted),
    }

    audiences = ["maintainer"]
    if has_docs_site:
        audiences.extend(["reader", "operator"])
    if has_end_user_usage or has_docs_site:
        audiences.append("user")
    if has_secondary_development:
        audiences.extend(["developer", "integrator"])
    profile["audiences"] = unique_preserve(audiences)

    if existing_modules:
        user_guide_state = "required" if "02-user-guide" in existing_modules else "omit"
        developer_guide_state = "required" if "03-developer-guide" in existing_modules else "omit"
        getting_started_state = "required" if "01-getting-started" in existing_modules else "omit"
        project_development_state = "required" if "04-project-development" in existing_modules else "omit"
    else:
        user_guide_state = "required" if (has_end_user_usage or has_docs_site or project_kind in {"application", "cli_tool"}) else "omit"
        developer_guide_state = "required" if (has_secondary_development or project_kind in {"application", "sdk_or_framework"}) else "omit"
        getting_started_state = "required"
        project_development_state = "required"
    profile["modules"] = {
        "01-getting-started": getting_started_state,
        "02-user-guide": user_guide_state,
        "03-developer-guide": developer_guide_state,
        "04-project-development": project_development_state,
    }
    profile["reasons"] = {
        "01-getting-started": (
            "检测到现有顶层目录，沿用当前项目已经启用的入门说明模块。"
            if existing_modules
            else "任何项目都需要根入口、阅读路径和文档地图。"
        ),
        "02-user-guide": (
            "检测到现有顶层目录，沿用当前项目已经启用的用户指南模块。"
            if existing_modules
            else "检测到最终用户、CLI 使用路径或文档站点阅读场景，需要保留用户指南。"
            if user_guide_state == "required"
            else "未检测到面向最终用户或操作者的稳定使用面，可省略用户指南。"
        ),
        "03-developer-guide": (
            "检测到现有顶层目录，沿用当前项目已经启用的开发者指南模块。"
            if existing_modules
            else "检测到公共 API、SDK、插件扩展点或稳定二次开发面，需要保留开发者指南。"
            if developer_guide_state == "required"
            else "未检测到稳定二次开发、SDK、插件或公共集成面，可省略开发者指南。"
        ),
        "04-project-development": (
            "检测到现有顶层目录，沿用当前项目已经启用的内部项目文档模块。"
            if existing_modules
            else "软件项目的需求、设计、测试、发布和追踪过程文档统一落在内部模块中。"
        ),
    }
    profile["source"] = "auto-detect"
    profile["detected_at"] = datetime.utcnow().isoformat() + "Z"
    return normalize_docs_profile(profile)


def resolve_project_docs_profile(project_root: Path, *, project_name: str = "", idea: str = "", stack: str = "") -> dict:
    config_path = project_config_path(project_root)
    if config_path.exists():
        try:
            config = normalize_project_config(json.loads(config_path.read_text(encoding="utf-8")))
        except Exception:
            config = {}
        raw_profile = config.get("docs_profile")
        if raw_profile:
            return normalize_docs_profile(raw_profile)
        return detect_docs_profile(
            project_root,
            project_name=project_name or str(config.get("project_name", "")).strip(),
            idea=idea or str(config.get("idea", "")).strip(),
            stack=stack or str(config.get("stack", "")).strip(),
        )
    return detect_docs_profile(project_root, project_name=project_name, idea=idea, stack=stack)
LEGACY_DOCS_FILE_MAP = {
    "README.md": "01-getting-started/project-overview.md",
    "08-handover/historical-project-prompt-templates.md": "02-user-guide/prompt-templates.md",
}
MODERN_DOCS_BOOTSTRAP_PAGES = {
    "01-getting-started/project-overview.md": textwrap.dedent(
        """
        # 项目概览

        ## 1. 文档用途

        用于说明项目定位、适用范围、目标读者、核心能力和推荐阅读顺序。

        ## 2. 建议填写内容

        - 项目名称、定位和一句话目标
        - 面向的用户或团队
        - 当前阶段和主要交付边界
        - 相关系统、仓库或运行环境

        ## 3. 推荐正文结构

        ### 3.1 项目定位

        说明项目解决什么问题、不解决什么问题，以及与其他系统的边界。

        ### 3.2 主要读者

        列出最终用户、协作者、开发者、运维或管理者各自应该从哪里开始阅读。

        ### 3.3 推荐阅读顺序

        用 3 到 5 条链接给出最常见的阅读路径。

        ### 3.4 阅读边界

        明确人类默认只从 `docs/` 进入项目；AI 内部控制面不作为人类阅读目录。

        ## 4. 变更记录

        | 日期 | 变更内容 | 变更人 |
        |---|---|---|
        | YYYY-MM-DD | 初始化模板 | 文档管理员 |
        """
    ).strip()
    + "\n",
    "01-getting-started/quick-start.md": textwrap.dedent(
        """
        # 快速开始

        ## 1. 适用对象

        说明首次接触项目的读者应该先完成哪些最小动作。

        ## 2. 最小启动步骤

        1. 获取仓库或部署环境访问权限。
        2. 阅读入门说明和当前阶段文档，不把 AI 内部控制面列成人类先读清单。
        3. 准备本地工具链或运行环境。
        4. 执行最小验证动作并确认结果。

        ## 3. 常用命令

        用代码块列出最常用的 3 到 8 条命令，并说明用途。

        ## 4. 常见入口

        - 正式文档入口
        - 核心脚本入口
        - 对话或自动化入口

        不要把 `AGENTS.md`、`GEMINI.md` 或 `.factory/*` 写成人类默认阅读路径。
        """
    ).strip()
    + "\n",
    "01-getting-started/document-map.md": textwrap.dedent(
        """
        # 文档地图

        ## 1. 四大模块

        逐项说明“入门说明、用户指南、开发者指南、项目开发文档（内）”分别服务谁、解决什么问题。

        ## 2. 阅读建议

        - 第一次接触项目：先看入门说明
        - 需要使用系统：看用户指南
        - 需要开发或集成：看开发者指南
        - 需要参与需求、设计、测试、发布和运维：看项目开发文档（内）

        ## 3. 内部模块说明

        对 `项目开发文档（内）` 下的治理、调研、需求、设计、过程、测试、发布、运维、演进、追踪矩阵给出一句话解释。
        """
    ).strip()
    + "\n",
    "02-user-guide/user-guide.md": textwrap.dedent(
        """
        # 使用指南

        ## 1. 这篇文档回答什么

        面向第一次接触项目的软件工厂使用者，说明：

        - 使用前需要什么准备
        - 如何判断项目类型
        - 第一轮会话应该怎么开始
        - AI 做完后要检查什么

        ## 2. 建议正文结构

        ### 2.1 使用前准备

        写清工具、权限、仓库、目录和最小可用性校验。

        ### 2.2 项目类型判断

        明确区分：

        - 空目录新项目
        - 历史项目纳管
        - 已纳入软件工厂的项目
        - 半初始化项目

        ### 2.3 第一轮会话怎么开始

        说明“先读什么、先做什么、不要做什么”，并明确人类默认不阅读 AI 内部控制面。

        ### 2.4 日常使用节奏

        说明会话开始、中途、结束时的推荐动作。

        ## 3. 关联文档

        - [提示词速查](./prompt-templates.md)
        - [命令速查](./command-cheatsheet.md)

        这类文档默认不要把 `AGENTS.md`、`GEMINI.md` 或 `.factory/*` 写成人类先读清单。
        """
    ).strip()
    + "\n",
    "02-user-guide/prompt-templates.md": textwrap.dedent(
        """
        # 提示词速查

        ## 1. 这篇文档回答什么

        面向实际会发 Prompt 给 AI 的使用者，提供：

        - 各种项目状态下的直接可复制 Prompt
        - 每种 Prompt 的使用时机
        - 每种 Prompt 的预期结果

        ## 2. 建议正文结构

        ### 2.1 场景总表

        用表格列出“场景、推荐第一动作、模板位置、预期结果”。

        ### 2.2 详细模板

        至少覆盖：

        - 空目录新项目初始化
        - 历史项目纳管
        - 半初始化项目补齐规则入口
        - 已纳入软件工厂后继续工作
        - 需求阶段
        - 设计阶段
        - OpenAPI 契约生成
        - 任务拆分
        - BUG / CR / 发布 / 交接

        ## 3. 要求

        每个模板都要明确：

        - 什么时候用
        - Prompt 正文
        - 预期结果

        不要要求人类手工指定 `AGENTS.md`、`GEMINI.md` 或 `.factory/*` 作为阅读清单；这属于 AI 自行处理的控制面。
        """
    ).strip()
    + "\n",
    "02-user-guide/command-cheatsheet.md": textwrap.dedent(
        """
        # 命令速查

        ## 1. 这篇文档回答什么

        面向已经会用自然语言，但需要下钻到命令层的使用者，说明：

        - 每个命令怎么调用
        - 它解决什么问题
        - 什么时候使用
        - 运行后的预期结果

        ## 2. 建议正文结构

        ### 2.1 先讲高层入口

        优先说明：

        - `factory-dispatch`
        - `factory-command-profiles`
        - `factory-workflow-runner`

        ### 2.2 再按类别列命令

        推荐分类：

        - 初始化与结构修复
        - 需求、设计与计划
        - 工作项与追踪
        - PR 与发布
        - 会话入口与诊断
        - 角色与团队协作
        - 恢复与自进化

        ## 3. 每个命令至少要写清楚

        - 常见写法
        - 作用
        - 什么时候使用
        - 预期
        """
    ).strip()
    + "\n",
    "03-developer-guide/01-concepts/01-system-map.md": textwrap.dedent(
        """
        # 1.1 系统地图与术语

        ## 1. 系统地图

        概述宿主、模块、CLI、调试链路和交付产物之间的关系。

        ## 2. 关键术语

        列出模块、任务、工作流、DevLink、ATM 等术语和统一口径。

        ## 3. 阅读提示

        初次接手时先统一术语，再进入结构、开发和调试章节。
        """
    ).strip()
    + "\n",
    "03-developer-guide/01-concepts/02-real-constraints.md": textwrap.dedent(
        """
        # 1.2 当前真实约束

        ## 1. 环境与依赖约束

        说明语言版本、宿主能力、外部依赖和不能跳过的运行前提。

        ## 2. 契约约束

        说明 `module.yaml`、入口文件、命令约定和兼容边界。

        ## 3. 交付约束

        说明调试、打包、验收和发布时必须满足的最小要求。
        """
    ).strip()
    + "\n",
    "03-developer-guide/02-quickstart/01-environment-setup.md": textwrap.dedent(
        """
        # 2.1 开发前准备

        ## 1. 工具链准备

        说明本地开发需要的语言版本、工具链、依赖和初始化动作。

        ## 2. 推荐校验

        用命令或步骤说明如何确认环境可用，例如 CLI help、最小 smoke 或单元测试。

        ## 3. 常见问题

        说明高频环境问题、依赖冲突、权限问题和本地恢复方式。
        """
    ).strip()
    + "\n",
    "03-developer-guide/02-quickstart/02-create-first-module.md": textwrap.dedent(
        """
        # 2.2 创建第一个模块

        ## 1. 初始化路径

        说明推荐脚手架命令、目录约定和首次创建后的必要检查。

        ## 2. 最小骨架

        说明任务、工作流、UI 和清单文件的最小可运行组合。

        ## 3. 首次验证

        给出最小运行、调试和打包验收路径。
        """
    ).strip()
    + "\n",
    "03-developer-guide/03-project-structure/01-layout-and-entrypoints.md": textwrap.dedent(
        """
        # 3.1 目录结构与入口

        ## 1. 目录布局

        说明源码、资源、测试、打包和文档目录的职责边界。

        ## 2. 运行入口

        说明宿主加载入口、任务入口和工作流入口的定位方式。

        ## 3. 禁止事项

        说明不允许耦合、绕过清单或直接依赖宿主私有实现的场景。
        """
    ).strip()
    + "\n",
    "03-developer-guide/03-project-structure/02-module-manifest.md": textwrap.dedent(
        """
        # 3.2 `module.yaml` 清单契约

        ## 1. 契约目标

        说明 `module.yaml` 是模块元数据、能力声明和加载约束的事实源。

        ## 2. 必填字段

        说明模块标识、版本、入口、命令、依赖和兼容范围。

        ## 3. 变更要求

        契约字段变化时，同步更新代码、调试说明、验收说明和发布信息。
        """
    ).strip()
    + "\n",
    "03-developer-guide/04-development/01-taskscript.md": textwrap.dedent(
        """
        # 4.1 编写 TaskScript

        ## 1. 适用范围

        说明哪些自动化任务适合用 TaskScript 实现，哪些应抽离为公共能力。

        ## 2. 建议正文结构

        说明输入、执行步骤、错误处理、日志输出和可观测性要求。

        ## 3. 测试要求

        说明最小单测、集成验证和失败回放方式。
        """
    ).strip()
    + "\n",
    "03-developer-guide/04-development/02-workflow.md": textwrap.dedent(
        """
        # 4.2 编写 Workflow

        ## 1. 目标与边界

        说明工作流负责的编排职责，以及与 TaskScript 的分工。

        ## 2. 关键要素

        说明状态流转、节点编排、输入输出契约和异常分支。

        ## 3. 验证方式

        说明最小 happy path、失败分支和回归检查方法。
        """
    ).strip()
    + "\n",
    "03-developer-guide/04-development/03-cli-and-ui.md": textwrap.dedent(
        """
        # 4.3 CLI 命令与 UI 配置

        ## 1. 暴露面设计

        说明命令入口、参数设计、UI 配置和用户可见行为的一致性要求。

        ## 2. 兼容策略

        说明新增命令、参数变更、默认值变化和弃用策略。

        ## 3. 验收建议

        说明 help、最小交互路径和截图或录屏等验证要求。
        """
    ).strip()
    + "\n",
    "03-developer-guide/04-development/04-core-capabilities.md": textwrap.dedent(
        """
        # 4.4 Core 提供的能力清单

        ## 1. 可复用能力

        列出宿主已经提供的运行时、配置、日志、存储和调试能力。

        ## 2. 接入方式

        说明推荐调用方式、依赖边界和禁止复制粘贴实现的场景。

        ## 3. 扩展原则

        缺少能力时先补齐公共能力，再决定是否在模块内局部实现。
        """
    ).strip()
    + "\n",
    "03-developer-guide/05-debugging/01-devlink-and-debug.md": textwrap.dedent(
        """
        # 5.1 DevLink 与真实调试链路

        ## 1. 调试入口

        说明 DevLink、本地联调和真实环境验证的使用顺序。

        ## 2. 证据要求

        说明日志、截图、输出产物和异常定位所需的最小证据。

        ## 3. 常见偏差

        说明开发态与打包态、联调态与正式安装态之间的差异。
        """
    ).strip()
    + "\n",
    "03-developer-guide/06-delivery/01-zip-installation.md": textwrap.dedent(
        """
        # 6.1 zip 打包与正式安装

        ## 1. 打包产物

        说明交付包结构、版本信息、依赖约束和命名规则。

        ## 2. 安装验证

        说明安装后的入口、命令、页面或任务如何确认可用。

        ## 3. 升级与回滚

        说明升级兼容、回滚策略和旧文件清理注意项。
        """
    ).strip()
    + "\n",
    "03-developer-guide/06-delivery/02-acceptance-checklist.md": textwrap.dedent(
        """
        # 6.2 最小验收清单

        ## 1. 功能验收

        列出必须成功的核心流程和关键异常分支。

        ## 2. 文档验收

        列出需要同步完成的用户说明、开发说明和发布说明。

        ## 3. 交付结论

        明确通过条件、阻塞项和遗留风险登记方式。
        """
    ).strip()
    + "\n",
    "03-developer-guide/07-troubleshooting/01-common-pitfalls.md": textwrap.dedent(
        """
        # 7.1 常见问题与坑位

        ## 1. 高发问题

        汇总环境、契约、调试、安装和兼容问题的典型症状。

        ## 2. 排查顺序

        说明先查入口、再查契约、再查依赖和运行时状态的建议路径。

        ## 3. 升级条件

        当问题无法通过模块内修复解决时，明确何时回到 Core 或内部设计文档处理。
        """
    ).strip()
    + "\n",
    "04-project-development/04-design/backend-design.md": textwrap.dedent(
        """
        # 后端设计文档

        ## 1. 文档目标

        说明服务分层、模块职责、任务执行、状态流转和错误处理策略。

        ## 2. 建议正文结构

        ### 2.1 分层设计

        描述控制层、服务层、仓储层、执行器、任务或工作流的职责分工。

        ### 2.2 核心流程

        按关键业务流程说明输入、处理、状态变化和输出。

        ### 2.3 依赖与风险

        说明外部依赖、降级策略、超时重试和可观测性要求。
        """
    ).strip()
    + "\n",
    "04-project-development/04-design/database-design.md": textwrap.dedent(
        """
        # 数据库设计文档

        ## 1. 文档目标

        说明实体、关系、索引、约束、迁移和数据生命周期。

        ## 2. 建议正文结构

        - 核心实体和字段说明
        - 关系与数据所有权
        - 索引与性能考虑
        - 迁移、回填和回滚策略
        - 数据保留、归档和删除规则
        """
    ).strip()
    + "\n",
    "04-project-development/04-design/deployment-architecture.md": textwrap.dedent(
        """
        # 部署与 CI/CD 设计

        ## 1. 文档目标

        说明环境拓扑、构建发布链路、门禁、回滚和职责边界。

        ## 2. 建议正文结构

        - 环境分层与网络边界
        - 构建产物与发布步骤
        - CI/CD 触发条件和检查点
        - 发布审批、回滚和应急处理
        - 日志、监控和审计要求
        """
    ).strip()
    + "\n",
    "04-project-development/04-design/ux-ui-design.md": textwrap.dedent(
        """
        # UX/UI 设计文档

        ## 1. 文档目标

        说明用户角色、任务路径、关键页面、组件状态和可生产化界面要求。

        ## 2. 建议正文结构

        - 用户角色与场景
        - 关键旅程与页面流
        - 页面状态与交互反馈
        - 视觉规范、可访问性和响应式要求
        - 设计稿、原型或静态资源引用
        """
    ).strip()
    + "\n",
    "04-project-development/05-development-process/software-development-process.md": textwrap.dedent(
        """
        # 软件开发流程

        ## 1. 流程目标

        说明需求、设计、开发、测试、发布、运维和复盘在当前项目中的正式推进顺序。

        ## 2. 推荐流程

        1. 调研与问题澄清
        2. 需求确认与验收标准固化
        3. 设计和接口约束成文
        4. 任务拆解与开发实施
        5. 测试与验证
        6. 发布与交付
        7. 运维与维护
        8. 复盘与演进

        ## 3. 每阶段至少写清楚

        - 输入文档
        - 输出文档
        - 准入准出条件
        - 主要责任人
        - 变更触发和回写要求
        """
    ).strip()
    + "\n",
    "04-project-development/06-testing-verification/test-plan.md": textwrap.dedent(
        """
        # 测试计划

        ## 1. 文档目标

        说明测试范围、层次、责任、风险重点和准入准出标准。

        ## 2. 建议正文结构

        - 范围与不测范围
        - 单元、集成、端到端和回归策略
        - 环境、数据和依赖
        - 风险重点和优先级
        - 发布前质量门槛
        """
    ).strip()
    + "\n",
    "04-project-development/06-testing-verification/test-report.md": textwrap.dedent(
        """
        # 测试报告

        ## 1. 文档目标

        汇总已执行测试、失败项、风险残留和是否具备发布条件。

        ## 2. 建议正文结构

        - 测试批次和执行范围
        - 通过率与失败项
        - 高风险缺陷和处理状态
        - 回归结果
        - 发布建议结论
        """
    ).strip()
    + "\n",
    "04-project-development/07-release-delivery/release-notes.md": textwrap.dedent(
        """
        # 发布说明

        ## 1. 文档目标

        汇总本次发布的新增能力、修复项、影响范围、升级说明和已知问题。

        ## 2. 建议正文结构

        - 发布版本和发布日期
        - 主要变更
        - 受影响模块或接口
        - 升级与兼容提醒
        - 已知问题和回滚入口
        """
    ).strip()
    + "\n",
    "04-project-development/08-operations-maintenance/deployment-guide.md": textwrap.dedent(
        """
        # 部署手册

        ## 1. 文档目标

        说明环境前提、部署步骤、验证方式和失败回滚方法。

        ## 2. 建议正文结构

        - 前置条件和权限要求
        - 构建与部署步骤
        - 部署后验证
        - 回滚路径
        - 常见故障排查
        """
    ).strip()
    + "\n",
    "04-project-development/08-operations-maintenance/operations-runbook.md": textwrap.dedent(
        """
        # 运维手册

        ## 1. 文档目标

        说明启停、巡检、监控、异常处理和升级路径。

        ## 2. 建议正文结构

        - 日常巡检项
        - 监控与告警
        - 典型故障处理流程
        - 升级、恢复和应急联系人
        - 责任边界和升级路径
        """
    ).strip()
    + "\n",
    "04-project-development/09-evolution/skill-evolution-plan.md": textwrap.dedent(
        """
        # Skill 进化方案

        ## 1. 文档目标

        说明 skill 从生成、检查、修复到自进化的阶段目标和验收标准。

        ## 2. 建议正文结构

        - 当前痛点和目标能力
        - 生成类、检查类、修复类能力拆分
        - 依赖数据、追踪矩阵和反馈闭环
        - 验收标准和下一轮里程碑
        """
    ).strip()
    + "\n",
    "04-project-development/10-traceability/interface-matrix.md": textwrap.dedent(
        """
        # 接口追踪矩阵

        ## 1. 文档目标

        把接口与需求、模块、提供方、消费方、版本和测试覆盖关系对应起来。

        ## 2. 建议字段

        | 接口编号 | 类型 | 提供方 | 消费方 | 关联需求 | 契约文件 | 版本策略 | 测试覆盖 | 负责人 |
        |---|---|---|---|---|---|---|---|---|
        | API-001 | 外部 REST | 待补充 | 待补充 | REQ-001 | openapi.yaml | 待补充 | TC-001 | 待补充 |
        """
    ).strip()
    + "\n",
    "04-project-development/10-traceability/document-index.md": textwrap.dedent(
        """
        # 文档索引

        ## 1. 文档目标

        集中登记项目正式文档、负责人、状态、主要读者和关联追踪 ID。

        ## 2. 建议字段

        | 文档路径 | 文档类型 | 主要读者 | 负责人 | 状态 | 关联编号 |
        |---|---|---|---|---|---|
        | `docs/04-project-development/03-requirements/prd.md` | 需求文档 | 产品、研发、测试 | 待补充 | 草稿 | REQ-* |
        """
    ).strip()
    + "\n",
}


def normalize_posix_relative(value: str) -> str:
    parts: list[str] = []
    for part in PurePosixPath(value.replace("\\", "/")).parts:
        if part in {"", "."}:
            continue
        if part == "..":
            if parts and parts[-1] != "..":
                parts.pop()
            else:
                parts.append(part)
            continue
        parts.append(part)
    return "/".join(parts)


def canonical_docs_relative_path(relative_path: str) -> str:
    relative = normalize_posix_relative(relative_path.strip())
    if relative.startswith("docs/"):
        relative = relative[5:]
    if relative in LEGACY_DOCS_FILE_MAP:
        return LEGACY_DOCS_FILE_MAP[relative]
    for old_prefix, new_prefix in LEGACY_DOCS_DIRECTORY_MAP.items():
        if relative == old_prefix:
            return new_prefix
        if relative.startswith(f"{old_prefix}/"):
            suffix = relative[len(old_prefix) + 1 :]
            return f"{new_prefix}/{suffix}"
    return relative


def legacy_docs_relative_path(relative_path: str) -> str:
    relative = normalize_posix_relative(relative_path.strip())
    reverse_file_map = {new: old for old, new in LEGACY_DOCS_FILE_MAP.items()}
    if relative in reverse_file_map:
        return reverse_file_map[relative]
    reverse_dir_map = {new: old for old, new in LEGACY_DOCS_DIRECTORY_MAP.items()}
    for new_prefix, old_prefix in reverse_dir_map.items():
        if relative == new_prefix:
            return old_prefix
        if relative.startswith(f"{new_prefix}/"):
            suffix = relative[len(new_prefix) + 1 :]
            return f"{old_prefix}/{suffix}"
    return relative


def canonical_docs_reference(value: str) -> str:
    raw = value.strip().replace("\\", "/")
    if not raw:
        return raw
    candidate = raw[5:] if raw.startswith("docs/") else raw
    top_level = candidate.split("/", 1)[0]
    if raw.startswith("docs/") or candidate in LEGACY_DOCS_FILE_MAP or top_level in LEGACY_DOCS_DIRECTORY_MAP or top_level in DOCS_STRATEGO_TOP_LEVEL_ORDER:
        return f"docs/{canonical_docs_relative_path(candidate)}"
    return raw


def canonical_docs_project_path(project_root: Path, relative_path: str) -> Path:
    relative = canonical_docs_reference(relative_path)
    if relative.startswith("docs/"):
        return project_root / relative
    return project_root / "docs" / canonical_docs_relative_path(relative)


def relative_path_from_doc(current_doc_relative: str, target_relative: str) -> str:
    current_parts = normalize_posix_relative(current_doc_relative).split("/")
    target_parts = normalize_posix_relative(target_relative).split("/")
    current_parent = current_parts[:-1]
    common = 0
    max_common = min(len(current_parent), len(target_parts))
    while common < max_common and current_parent[common] == target_parts[common]:
        common += 1
    upward = [".."] * (len(current_parent) - common)
    downward = target_parts[common:]
    result = "/".join([*upward, *downward])
    return result or Path(target_relative).name


def rewrite_markdown_doc_links(text: str, *, old_current_relative: str, new_current_relative: str) -> str:
    old_parent = normalize_posix_relative(str(PurePosixPath(old_current_relative).parent))

    def replace(match: re.Match[str]) -> str:
        target = match.group("target").strip()
        if not target or target.startswith("#"):
            return match.group(0)
        if any(target.startswith(prefix) for prefix in ("http://", "https://", "mailto:", "tel:", "data:", "file://")):
            return match.group(0)

        target_path, hash_mark, anchor = target.partition("#")
        raw_target = target_path.strip()
        if not raw_target:
            return match.group(0)

        if raw_target.startswith("docs/"):
            old_target_relative = normalize_posix_relative(raw_target[5:])
        else:
            old_target_relative = normalize_posix_relative(f"{old_parent}/{raw_target}" if old_parent else raw_target)
            if old_target_relative.startswith(".."):
                return match.group(0)

        new_target_relative = canonical_docs_relative_path(old_target_relative)
        if new_target_relative == old_target_relative:
            return match.group(0)

        rewritten_target = relative_path_from_doc(new_current_relative, new_target_relative)
        if hash_mark:
            rewritten_target = f"{rewritten_target}#{anchor}"
        return f"{match.group('prefix')}{rewritten_target}{match.group('suffix')}"

    return MARKDOWN_LINK_PATTERN.sub(replace, text)


def update_publication_policy_for_modern_docs(project_root: Path, docs_profile: dict | None = None) -> None:
    path = project_root / "docs" / "publication-policy.json"
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    else:
        payload = {}
    profile = normalize_docs_profile(docs_profile or resolve_project_docs_profile(project_root))
    docs_root = project_root / "docs"
    public_include = [
        canonical_docs_reference(item)
        for item in payload.get("public_include", [])
        if isinstance(item, str)
    ]
    private_include = [
        canonical_docs_reference(item)
        for item in payload.get("private_include", [])
        if isinstance(item, str)
    ]
    managed_public_patterns = {f"docs/{module_key}/**" for module_key in DOCS_STRATEGO_TOP_LEVEL_ORDER}
    public_include = [item for item in public_include if item not in managed_public_patterns]
    if "docs/index.md" not in public_include:
        public_include.insert(0, "docs/index.md")
    for module_key in docs_profile_enabled_top_levels(profile, docs_root):
        if module_key == "04-project-development":
            continue
        item = f"docs/{module_key}/**"
        if item not in public_include:
            public_include.append(item)
    if "docs/**" not in private_include:
        private_include.insert(0, "docs/**")
    if ".factory/memory/**" not in private_include:
        private_include.append(".factory/memory/**")
    write_text(path, json.dumps({"public_include": public_include, "private_include": private_include}, ensure_ascii=False, indent=2))


def docs_structure_migration_needed(project_root: Path) -> bool:
    docs_root = project_root / "docs"
    if not docs_root.exists():
        return False
    legacy_roots = [docs_root / "README.md", *(docs_root / item for item in LEGACY_DOCS_DIRECTORY_MAP)]
    return any(path.exists() for path in legacy_roots)


def migrate_docs_structure(project_root: Path, project_name: str, *, force: bool = False) -> dict[str, list[str]]:
    raise RuntimeError(
        "`migrate_docs_structure` 已退场；请直接使用 `document-templates` skill 手工重构文档，再执行 `docs-stratego source validate`。"
    )


def docs_stratego_directory_spec(relative_dir: str) -> dict | None:
    return DOCS_STRATEGO_DIRECTORY_SPECS.get(relative_dir)


def docs_stratego_top_level_spec(relative_dir: str) -> dict | None:
    top_level = relative_dir.split("/", 1)[0] if relative_dir else ""
    return DOCS_STRATEGO_DIRECTORY_SPECS.get(top_level)


def strip_markdown_front_matter(markdown_text: str) -> str:
    if not markdown_text.startswith("---\n"):
        return markdown_text
    marker = "\n---\n"
    end_index = markdown_text.find(marker, 4)
    if end_index == -1:
        return markdown_text
    return markdown_text[end_index + len(marker) :]


def markdown_h1_title(path: Path) -> str:
    body = strip_markdown_front_matter(path.read_text(encoding="utf-8", errors="ignore"))
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("# "):
            return line[2:].strip()
    stem = path.stem.replace("-", " ").replace("_", " ").strip()
    return stem or path.name


def docs_stratego_trim_scalar(value: str) -> str:
    text = value.strip()
    if " #" in text:
        text = text.split(" #", 1)[0].strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {"'", '"'}:
        text = text[1:-1].strip()
    return text


def is_docs_markdown_page(path: Path | str) -> bool:
    candidate = path.name if isinstance(path, Path) else str(path)
    return candidate.lower().endswith(".md")


def is_docs_openapi_contract(path: Path | str) -> bool:
    candidate = path.name if isinstance(path, Path) else str(path)
    return candidate.lower().endswith(DOCS_STRATEGO_OPENAPI_SUFFIXES)


def is_docs_mcp_tools_contract(path: Path | str) -> bool:
    candidate = path.name if isinstance(path, Path) else str(path)
    return candidate.lower().endswith(DOCS_STRATEGO_MCP_TOOLS_SUFFIXES)


def is_docs_contract_file(path: Path | str) -> bool:
    return is_docs_openapi_contract(path) or is_docs_mcp_tools_contract(path)


def is_docs_stratego_page_file(path: Path | str) -> bool:
    return is_docs_markdown_page(path) or is_docs_contract_file(path)


def docs_stratego_display_name_from_file(path: Path) -> str:
    lower_name = path.name.lower()
    stem = path.name
    for suffix in DOCS_STRATEGO_CONTRACT_SUFFIXES:
        if lower_name.endswith(suffix):
            stem = path.name[: -len(suffix)]
            break
    stem = stem.replace("-", " ").replace("_", " ").strip()
    return stem or path.name


def load_json_document(path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def factory_workspace_root() -> Path:
    return Path(__file__).resolve().parent.parent


def intent_control_root() -> Path:
    override = os.environ.get(INTENT_APPROVAL_ROOT_ENV, "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return factory_workspace_root()


def action_registry_path() -> Path:
    return factory_workspace_root() / "config" / "action-registry.json"


def autonomy_policy_path() -> Path:
    return factory_workspace_root() / "config" / "autonomy-policy.json"


def reply_policy_path() -> Path:
    return factory_workspace_root() / "config" / "reply-policy.json"


def intent_approval_state_path() -> Path:
    return intent_control_root() / FACTORY_PROCESS_RELATIVE / "intent-approvals.json"


def intent_approval_report_path() -> Path:
    return intent_control_root() / FACTORY_PROCESS_RELATIVE / "intent-approvals.md"


def intent_approval_summary_path() -> Path:
    return intent_control_root() / FACTORY_MEMORY_RELATIVE / "intent-approvals.summary.md"


def frontend_profiles_dir() -> Path:
    return factory_workspace_root() / "config" / "frontends"


@lru_cache(maxsize=4)
def load_json_config(path: str | Path) -> dict:
    payload = load_json_document(Path(path))
    if not isinstance(payload, dict):
        raise RuntimeError(f"配置文件不是有效对象：{path}")
    return payload


@lru_cache(maxsize=1)
def load_action_registry() -> dict[str, dict]:
    payload = load_json_config(action_registry_path())
    actions = payload.get("actions", {})
    if not isinstance(actions, dict):
        raise RuntimeError("action-registry.json 的 `actions` 必须是对象。")

    normalized: dict[str, dict] = {}
    for action_id, raw in actions.items():
        if not isinstance(raw, dict):
            raise RuntimeError(f"动作 `{action_id}` 的定义必须是对象。")
        script_name = str(raw.get("script_name", "")).strip()
        description = str(raw.get("description", "")).strip()
        risk_level = str(raw.get("risk_level", "")).strip() or "L3"
        aliases = [str(alias).strip() for alias in raw.get("aliases", []) if str(alias).strip()]
        if not script_name or not description:
            raise RuntimeError(f"动作 `{action_id}` 缺少 `script_name` 或 `description`。")
        normalized[str(action_id).strip()] = {
            "id": str(action_id).strip(),
            "script_name": script_name,
            "description": description,
            "aliases": aliases,
            "risk_level": risk_level,
            "purpose": str(raw.get("purpose", "")).strip(),
            "preconditions": list(raw.get("preconditions", [])),
            "frontend_requirements": list(raw.get("frontend_requirements", [])),
            "artifacts": list(raw.get("artifacts", [])),
            "success_criteria": list(raw.get("success_criteria", [])),
            "verification": list(raw.get("verification", [])),
            "recovery_hints": list(raw.get("recovery_hints", [])),
            "subtargets": dict(raw.get("subtargets", {})) if isinstance(raw.get("subtargets"), dict) else {},
        }
    return normalized


@lru_cache(maxsize=1)
def load_autonomy_policy() -> dict:
    payload = load_json_config(autonomy_policy_path())
    risk_levels = payload.get("risk_levels", {})
    default_unregistered = payload.get("default_unregistered", {})
    if not isinstance(risk_levels, dict):
        raise RuntimeError("autonomy-policy.json 的 `risk_levels` 必须是对象。")
    if not isinstance(default_unregistered, dict):
        raise RuntimeError("autonomy-policy.json 的 `default_unregistered` 必须是对象。")
    return payload


@lru_cache(maxsize=1)
def load_reply_policy() -> dict:
    payload = load_json_config(reply_policy_path())
    actions = payload.get("actions", {})
    skill_changes = payload.get("skill_changes", {})
    if not isinstance(actions, dict):
        raise RuntimeError("reply-policy.json 的 `actions` 必须是对象。")
    if not isinstance(skill_changes, dict):
        raise RuntimeError("reply-policy.json 的 `skill_changes` 必须是对象。")
    return payload


def nested_value(payload: dict, dotted_path: str, default: object = "") -> object:
    current: object = payload
    for part in str(dotted_path or "").split("."):
        key = part.strip()
        if not key:
            continue
        if not isinstance(current, dict):
            return default
        current = current.get(key, default)
        if current is default:
            return default
    return current


def action_reply_contract(action_id: str) -> dict:
    contract = load_reply_policy().get("actions", {}).get(str(action_id or "").strip(), {})
    return dict(contract) if isinstance(contract, dict) else {}


def build_reply_summary(action_id: str, payload: dict, *, extra: dict | None = None) -> dict:
    contract = action_reply_contract(action_id)
    items = []
    for raw in contract.get("fields", []):
        if not isinstance(raw, dict):
            continue
        path = str(raw.get("path", "")).strip()
        label = str(raw.get("label", path)).strip() or path
        if not path:
            continue
        value = nested_value(payload, path, "")
        if value in ("", None, [], {}):
            continue
        items.append({"label": label, "path": path, "value": value})
    summary = {
        "action": str(action_id or "").strip(),
        "required": bool(contract.get("required", False)),
        "mode": str(contract.get("mode", "manager_brief")).strip() or "manager_brief",
        "items": items,
    }
    if extra:
        summary.update(extra)
    return summary


def skill_change_governance() -> dict:
    contract = load_reply_policy().get("skill_changes", {})
    return dict(contract) if isinstance(contract, dict) else {}


def action_policy(action_id: str) -> dict:
    policy = load_autonomy_policy()
    default_policy = dict(policy.get("default_unregistered", {}))
    registry = load_action_registry()
    spec = registry.get(action_id)
    if spec is None:
        result = dict(default_policy)
        result.setdefault("risk_level", "L3")
        result["registered"] = False
        return result

    risk_level = str(spec.get("risk_level", "")).strip() or str(default_policy.get("risk_level", "")).strip() or "L3"
    risk_policy = policy.get("risk_levels", {}).get(risk_level, {})
    if not isinstance(risk_policy, dict):
        raise RuntimeError(f"自治策略中风险等级 `{risk_level}` 不是对象。")

    result = dict(default_policy)
    result.update(risk_policy)
    result["risk_level"] = risk_level
    result["registered"] = True
    return result


def resolve_registered_action(raw: str) -> str:
    action = str(raw or "").strip()
    if not action:
        return ""
    registry = load_action_registry()
    if action in registry:
        return action
    for action_id, spec in registry.items():
        if action in spec.get("aliases", []):
            return action_id
    return ""


def effective_action_policy(action_id: str, *, selected_profile: str = "", selected_workflow: str = "") -> dict:
    policy = action_policy(action_id)
    registry = load_action_registry()
    spec = registry.get(action_id)
    if spec is None:
        return policy

    subtargets = spec.get("subtargets", {})
    if not isinstance(subtargets, dict):
        return policy
    selected = str(selected_profile or selected_workflow or "").strip()
    if not selected:
        return policy

    override = subtargets.get(selected, {})
    if not isinstance(override, dict):
        return policy
    override_risk = str(override.get("risk_level", "")).strip()
    if not override_risk:
        return policy

    risk_policy = load_autonomy_policy().get("risk_levels", {}).get(override_risk, {})
    if not isinstance(risk_policy, dict):
        return policy

    merged = dict(policy)
    merged.update(risk_policy)
    merged["risk_level"] = override_risk
    merged["registered"] = True
    return merged


def load_intent_approval_records() -> list[dict]:
    payload = load_json_document(intent_approval_state_path())
    if not isinstance(payload, dict):
        return []
    records = payload.get("records", [])
    if not isinstance(records, list):
        return []
    return [dict(item) for item in records if isinstance(item, dict)]


def save_intent_approval_records(records: Sequence[dict]) -> None:
    payload = {
        "version": 1,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "records": list(records),
    }
    write_text(intent_approval_state_path(), json.dumps(payload, ensure_ascii=False, indent=2))


def new_intent_approval_id(action_id: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    short = uuid.uuid4().hex[:6]
    action_key = normalize_key(action_id or "intent")[:12] or "intent"
    return f"IA-{stamp}-{action_key}-{short}"


def render_intent_approval_report(records: Sequence[dict]) -> str:
    ordered = sorted(records, key=lambda item: str(item.get("created_at", "")), reverse=True)
    pending = [item for item in ordered if item.get("status") == "pending"]
    recent = [item for item in ordered if item.get("status") != "pending"][:10]
    lines = [
        "# Intent 审批记录",
        "",
        f"- 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 待审批票据：{len(pending)}",
        f"- 全部票据：{len(ordered)}",
        "",
        "## 待审批",
        "",
    ]
    if pending:
        for item in pending:
            ownership = item.get("ownership") or {}
            conflicts = item.get("ownership_conflicts") or []
            lines.extend(
                [
                    f"- `{item.get('id', '')}` | 动作：`{item.get('action', '')}` | 审批：`{item.get('approval', '')}` | 项目：`{item.get('project_path', '')}`",
                    f"  - 意图：{item.get('intent', '')}",
                    f"  - 理由：{'；'.join(item.get('reasons', [])) or '无'}",
                    f"  - ownership：`{ownership.get('role_title', ownership.get('role_id', '未声明'))}` | 写集：`{', '.join(ownership.get('write_targets', [])) or '无'}` | 冲突：{len(conflicts)}",
                ]
            )
    else:
        lines.append("- 当前没有待审批票据。")
    lines.extend(["", "## 最近已处理", ""])
    if recent:
        for item in recent:
            lines.append(
                f"- `{item.get('id', '')}` | 状态：`{item.get('status', '')}` | 动作：`{item.get('action', '')}` | 审批人：{item.get('decision_owner', '无') or '无'}"
            )
    else:
        lines.append("- 当前还没有已处理票据。")
    return "\n".join(lines).rstrip() + "\n"


def write_intent_approval_views(records: Sequence[dict]) -> None:
    pending = [item for item in records if item.get("status") == "pending"]
    write_text(intent_approval_report_path(), render_intent_approval_report(records))
    write_text(
        intent_approval_summary_path(),
        "\n".join(
            [
                "# Intent 审批摘要",
                "",
                f"- 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"- 待审批：{len(pending)}",
                f"- 全部票据：{len(records)}",
            ]
        ),
    )


def default_frontend_profile() -> dict:
    return {
        "id": "generic",
        "label": "通用 CLI 模型",
        "aliases": [],
        "status": "fallback",
        "family": "cli",
        "primary_rule_files": ["AGENTS.md", "GEMINI.md"],
        "capabilities": {
            "file_read": True,
            "file_write": True,
            "command_exec": True,
            "tool_call": False,
            "context_compaction": False,
            "subagent": False,
            "mcp": False,
            "stream_observation": False,
            "approval_hook": False,
        },
        "fallbacks": {
            "subagent": "退化为单代理串行执行。",
            "mcp": "退化为本地文件和脚本路径。",
            "context_compaction": "依赖最小上下文包和压缩记忆。",
        },
        "bootstrap_prompts": [
            "读取 AGENTS.md、GEMINI.md、.factory/project.json 和 .factory/memory/agent-session.md，以{role_title}身份{current_focus}。",
            "当用户直接输入 /技能名 时，将其视为立即调用该 skill 的默认工作流，而不是展示技能定义；先确认当前阶段、角色职责和推荐动作，再开始执行。若用户明确写出“提交 / commit / 执行提交”，则视为已授权执行本地提交，不要无故停在摘要阶段。"
        ],
    }


def load_frontend_profiles() -> dict[str, dict]:
    profiles: dict[str, dict] = {}
    config_dir = frontend_profiles_dir()
    if not config_dir.exists():
        return profiles
    for path in sorted(config_dir.glob("*.json")):
        payload = load_json_document(path)
        if not isinstance(payload, dict):
            raise RuntimeError(f"前台画像文件无效：{path}")
        frontend_id = str(payload.get("id", "")).strip()
        label = str(payload.get("label", "")).strip()
        if not frontend_id or not label:
            raise RuntimeError(f"前台画像缺少 `id` 或 `label`：{path}")
        capabilities = payload.get("capabilities", {})
        if not isinstance(capabilities, dict):
            raise RuntimeError(f"前台画像的 `capabilities` 必须是对象：{path}")
        profile = dict(payload)
        profile["id"] = frontend_id
        profile["label"] = label
        profile["aliases"] = [str(alias).strip() for alias in payload.get("aliases", []) if str(alias).strip()]
        profile["primary_rule_files"] = [
            str(item).strip() for item in payload.get("primary_rule_files", []) if str(item).strip()
        ] or ["AGENTS.md", "GEMINI.md"]
        profile["bootstrap_prompts"] = [
            str(item).strip() for item in payload.get("bootstrap_prompts", []) if str(item).strip()
        ]
        profile["fallbacks"] = dict(payload.get("fallbacks", {}))
        profile["path"] = str(path)
        profiles[frontend_id] = profile
    return profiles


def resolve_frontend_profile(query: str, default_id: str = "generic") -> dict:
    profiles = load_frontend_profiles()
    normalized = normalize_key(query or default_id)
    if normalized in {"", "generic"}:
        return default_frontend_profile()

    for profile in profiles.values():
        candidates = [profile.get("id", ""), profile.get("label", ""), *profile.get("aliases", [])]
        if normalized in {normalize_key(candidate) for candidate in candidates if candidate}:
            return profile

    if default_id in profiles:
        return profiles[default_id]
    return default_frontend_profile()


def frontend_prompt_examples(tool: str, role_title: str, focus: str) -> list[str]:
    current_focus = focus or "继续当前项目阶段工作"
    profile = resolve_frontend_profile(tool, default_id="generic")
    prompts = []
    for template in profile.get("bootstrap_prompts", []):
        try:
            prompts.append(template.format(role_title=role_title, current_focus=current_focus))
        except Exception:
            prompts.append(template)
    prompts.append("如果用户直接输入 `/技能名`，不要复述 skill 定义，直接执行该 skill 的默认工作流。")
    prompts.append(
        "如果用户直接输入 `/gitcommitzh`，立即检查当前 Git 工作区与暂存区变化，输出结构化中文变更说明和中文提交信息草案；只有同条消息明确包含“提交”或“commit”时才继续执行本地提交。真正提交前，先显式列出“最终写入 Git 的提交信息原文”，提交时逐字复用这段原文；若用户已明确要求提交、暂存区为空、且未指定文件子集，则默认自动执行 `git add .` 纳入当前工作区改动，而不是中止。"
    )
    prompts.append(
        "如果 `gitcommitzh` 已经成功提交，必须再读取一次 Git 中实际写入的提交信息，并把完整标题和完整正文回显给用户，不能只返回提交号和标题。"
    )
    prompts.append(
        "只有在拿到真实 commit short hash 之后，才能把状态写成“已提交”；禁止用 `[正在执行提交...]` 或其他占位文本冒充提交号。"
    )
    prompts.append(
        "如果用户原始消息已经明确要求提交，则在同一轮内完成提交和回显；不要先输出一轮中间态摘要，再等待用户下一轮重复说“提交”。"
    )
    if prompts:
        return prompts
    fallback = []
    for template in default_frontend_profile()["bootstrap_prompts"]:
        try:
            fallback.append(template.format(role_title=role_title, current_focus=current_focus))
        except Exception:
            fallback.append(template)
    return fallback


def parse_openapi_contract_metadata(path: Path) -> dict[str, str]:
    if path.suffix.lower() == ".json":
        payload = load_json_document(path)
        if not isinstance(payload, dict):
            return {"openapi": "", "title": "", "version": ""}
        info = payload.get("info")
        if not isinstance(info, dict):
            info = {}
        return {
            "openapi": str(payload.get("openapi", "")).strip(),
            "title": str(info.get("title", "")).strip(),
            "version": str(info.get("version", "")).strip(),
        }

    text = path.read_text(encoding="utf-8", errors="ignore")
    openapi = ""
    title = ""
    version = ""
    in_info = False
    info_indent = -1
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if not openapi:
            match = re.match(r"^\s*openapi:\s*(.+?)\s*$", raw)
            if match:
                openapi = docs_stratego_trim_scalar(match.group(1))
                continue
        if re.match(r"^\s*info:\s*$", raw):
            in_info = True
            info_indent = indent
            continue
        if in_info:
            if indent <= info_indent and stripped:
                in_info = False
            else:
                if not title:
                    match = re.match(r"^\s*title:\s*(.+?)\s*$", raw)
                    if match:
                        title = docs_stratego_trim_scalar(match.group(1))
                        continue
                if not version:
                    match = re.match(r"^\s*version:\s*(.+?)\s*$", raw)
                    if match:
                        version = docs_stratego_trim_scalar(match.group(1))
                        continue
        if openapi and title and version:
            break
    return {"openapi": openapi, "title": title, "version": version}


def openapi_contract_title(path: Path) -> str:
    metadata = parse_openapi_contract_metadata(path)
    return metadata["title"] or docs_stratego_display_name_from_file(path)


def parse_mcp_tools_contract_metadata(path: Path) -> dict[str, object]:
    if path.suffix.lower() == ".json":
        payload = load_json_document(path)
        if not isinstance(payload, dict):
            return {"tool_count": 0, "title": "", "valid": False}
        tools = payload.get("tools")
        if not isinstance(tools, list):
            result = payload.get("result")
            tools = result.get("tools") if isinstance(result, dict) else None
        if not isinstance(tools, list):
            return {"tool_count": 0, "title": "", "valid": False}
        title = ""
        if len(tools) == 1 and isinstance(tools[0], dict):
            title = str(tools[0].get("title") or tools[0].get("name") or "").strip()
        valid = len(tools) > 0 and all(
            isinstance(tool, dict)
            and str(tool.get("name", "")).strip()
            and str(tool.get("description", "")).strip()
            and "inputSchema" in tool
            for tool in tools
        )
        return {"tool_count": len(tools), "title": title, "valid": valid}

    text = path.read_text(encoding="utf-8", errors="ignore")
    has_tools = bool(re.search(r"(?m)^\s*tools:\s*$", text))
    has_nested_tools = bool(re.search(r"(?m)^\s*result:\s*$", text) and re.search(r"(?m)^\s*tools:\s*$", text))
    tool_count = len(re.findall(r"(?m)^\s*-\s+(?:title|name):\s*", text))
    inline_title = ""
    title_match = re.search(r"(?m)^\s*-\s+title:\s*(.+?)\s*$", text)
    if title_match:
        inline_title = docs_stratego_trim_scalar(title_match.group(1))
    if not inline_title:
        name_match = re.search(r"(?m)^\s*-\s+name:\s*(.+?)\s*$", text)
        if name_match and tool_count == 1:
            inline_title = docs_stratego_trim_scalar(name_match.group(1))
    valid = (
        (has_tools or has_nested_tools)
        and tool_count > 0
        and bool(re.search(r"(?m)^\s*-\s+name:\s*.+$", text))
        and bool(re.search(r"(?m)^\s+description:\s*.+$", text))
        and bool(re.search(r"(?m)^\s+inputSchema:\s*$", text))
    )
    return {"tool_count": tool_count, "title": inline_title, "valid": valid}


def mcp_tools_contract_title(path: Path) -> str:
    metadata = parse_mcp_tools_contract_metadata(path)
    title = str(metadata.get("title", "")).strip()
    return title or docs_stratego_display_name_from_file(path)


def fallback_directory_title(name: str) -> str:
    if name in DOCS_STRATEGO_DIRECTORY_TITLE_OVERRIDES:
        return DOCS_STRATEGO_DIRECTORY_TITLE_OVERRIDES[name]
    text = name.replace("-", " ").replace("_", " ").strip()
    return text or name


def docs_stratego_directory_title(relative_dir: str, project_name: str) -> str:
    if not relative_dir:
        return project_name
    spec = docs_stratego_directory_spec(relative_dir)
    if spec:
        return spec["title"]
    return fallback_directory_title(Path(relative_dir).name)


def docs_stratego_page_access(relative_path: str, existing_page_meta: dict[str, dict[str, str]] | None = None) -> str:
    if existing_page_meta:
        access = str(existing_page_meta.get(relative_path, {}).get("access", "")).strip()
        if access in DOCS_STRATEGO_ACCESS_LEVELS:
            return access
    child = Path(relative_path).parts[0] if relative_path else ""
    spec = DOCS_STRATEGO_DIRECTORY_SPECS.get(child)
    return str(spec.get("root_access", "public")) if spec else "public"


def docs_stratego_child_paths(directory: Path, project_root: Path, docs_profile: dict | None = None) -> list[Path]:
    children: list[Path] = []
    docs_root = project_root / "docs"
    profile = normalize_docs_profile(docs_profile or resolve_project_docs_profile(project_root))
    for child in directory.iterdir():
        if child.name.startswith(".") or child.name == "index.md" or child.name == "assets":
            continue
        if directory == docs_root and not docs_profile_module_enabled(profile, child.name, docs_root):
            continue
        if child.is_dir() or (child.is_file() and is_docs_stratego_page_file(child)):
            children.append(child)
    return children


def docs_stratego_ordered_children(directory: Path, relative_dir: str, project_root: Path, docs_profile: dict | None = None) -> list[Path]:
    profile = normalize_docs_profile(docs_profile or resolve_project_docs_profile(project_root))
    docs_root = project_root / "docs"
    if not relative_dir:
        preferred = docs_profile_enabled_top_levels(profile, docs_root)
    else:
        spec = docs_stratego_directory_spec(relative_dir)
        preferred = list(spec.get("order", [])) if spec else []
    order_map = {name: index for index, name in enumerate(preferred)}
    return sorted(
        docs_stratego_child_paths(directory, project_root, profile),
        key=lambda child: (0 if child.name in order_map else 1, order_map.get(child.name, 999), child.name),
    )


def docs_stratego_nav_title(
    child: Path,
    docs_root: Path,
    project_name: str,
    existing_page_meta: dict[str, dict[str, str]] | None = None,
) -> str:
    if child.is_dir():
        relative_dir = child.relative_to(docs_root).as_posix()
        return docs_stratego_directory_title(relative_dir, project_name)
    relative_path = child.relative_to(docs_root).as_posix()
    if existing_page_meta:
        title = str(existing_page_meta.get(relative_path, {}).get("title", "")).strip()
        if title:
            return title
    if is_docs_markdown_page(child):
        return markdown_h1_title(child)
    if is_docs_openapi_contract(child):
        return openapi_contract_title(child)
    if is_docs_mcp_tools_contract(child):
        return mcp_tools_contract_title(child)
    return docs_stratego_display_name_from_file(child)


def docs_stratego_directory_heading(title: str) -> str:
    return title if title.endswith("概览") else f"{title}概览"


def docs_stratego_recommendation_lines(project_root: Path, project_name: str, relative_dir: str) -> list[str]:
    docs_root = project_root / "docs"
    directory = docs_root / relative_dir
    docs_profile = resolve_project_docs_profile(project_root, project_name=project_name)
    ordered = [
        docs_stratego_nav_title(child, docs_root, project_name)
        for child in docs_stratego_ordered_children(directory, relative_dir, project_root, docs_profile)
    ]
    if not ordered:
        return ["当前目录暂无子页面；后续补充内容时，继续保持仓内相对路径和目录命名一致。"]
    return [
        "建议阅读顺序：",
        "",
        *[f"{index}. {name}" for index, name in enumerate(ordered, start=1)],
    ]


def docs_stratego_directory_body(project_root: Path, relative_dir: str, title: str, project_name: str) -> list[str]:
    if not relative_dir:
        return [
            f"这是 `{project_name}` 的正式项目文档源。AI 软件工厂在项目仓库内直接维护这些文档，`docs-stratego` 通过 Git 子模块或等价的仓级挂载方式聚合展示，但不反向改写源文档。",
            "",
            "## 适用范围",
            "",
            "- 根 `docs/index.md` 的 front matter 是目录树、页面路径和访问级别的唯一事实源。",
            "- Markdown 页面、OpenAPI 契约和 MCP tools 快照统一作为正式页面资产维护。",
            "- 契约文件必须放在真实文档目录下，并与所在目录的 `index.md` 配套。",
            "",
            "## 维护规则",
            "",
            "- 只有根 `docs/index.md` 声明全站 `mkdocs.nav`、页面路径和页面权限。",
            "- 子目录 `index.md` 只作为正文首页和资源权限锚点，不再承担导航声明职责。",
            "- 页面、图片和附件跟随所属目录维护；资源文件放在当前目录或当前目录的 `assets/` 下，`assets/` 不承载 Markdown 页面或契约文件。",
            "- 仓内链接统一使用相对路径，不写机器绝对路径。",
            "- 新增、删除或移动 Markdown 页面或契约文件后，同步刷新根 `docs/index.md` 的目录树；子目录 `index.md` 只保留正文概览。",
        ]
    name = Path(relative_dir).name
    if name == "openapi":
        return [
            "本目录收纳当前边界下可独立联调、独立评审和独立渲染的 OpenAPI 契约。",
            "",
            "- 面向对象：集成方、研发、测试与技术评审者。",
            "- 维护规则：每份契约对应一个稳定 API 面，命名统一使用 `*.openapi.yaml|yml|json`。",
            "- 权限规则：访问级别只看根 `docs/index.md` 对应页面节点的 `access`，目录名不参与权限判断。",
        ]
    if name == "tools":
        return [
            "本目录收纳当前边界下的 MCP tools 快照，用于静态展示 Agent 可调用工具的输入输出契约。",
            "",
            "- 面向对象：Agent 集成方、研发、运维与自动化维护者。",
            "- 维护规则：每份快照对应一组稳定工具暴露面，命名统一使用 `*.mcp-tools.yaml|yml|json`。",
            "- 权限规则：访问级别只看根 `docs/index.md` 对应页面节点的 `access`，目录名不参与权限判断。",
        ]
    spec = docs_stratego_directory_spec(relative_dir)
    description = spec["description"] if spec else f"本目录收纳与“{title}”相关的页面和子目录。"
    return [
        description,
        "",
        "- 本页是该目录的正文首页，用于说明范围、读者和维护边界。",
        "- 目录树、页面路径和访问级别统一由根 `docs/index.md` 声明，这里不重复维护页面清单。",
        "- 本目录下的 Markdown 页面、契约文件和资源文件应随内容变更一起演进。",
    ]


def docs_stratego_nav_nodes(
    directory: Path,
    docs_root: Path,
    project_name: str,
    relative_dir: str = "",
    existing_page_meta: dict[str, dict[str, str]] | None = None,
) -> list[dict]:
    nodes: list[dict] = []
    docs_profile = resolve_project_docs_profile(docs_root.parent, project_name=project_name)
    for child in docs_stratego_ordered_children(directory, relative_dir, docs_root.parent, docs_profile):
        child_relative = child.relative_to(docs_root).as_posix()
        if child.is_dir():
            nodes.append(
                {
                    "type": "directory",
                    "title": docs_stratego_nav_title(child, docs_root, project_name, existing_page_meta),
                    "relative_dir": child_relative,
                    "children": [
                        {
                            "type": "page",
                            "title": "概览",
                            "path": f"{child_relative}/index.md",
                            "access": docs_stratego_page_access(f"{child_relative}/index.md", existing_page_meta),
                        },
                        *docs_stratego_nav_nodes(child, docs_root, project_name, child_relative, existing_page_meta),
                    ],
                }
            )
            continue
        nodes.append(
            {
                "type": "page",
                "title": docs_stratego_nav_title(child, docs_root, project_name, existing_page_meta),
                "path": child_relative,
                "access": docs_stratego_page_access(child_relative, existing_page_meta),
            }
        )
    return nodes


def append_docs_stratego_nav_lines(lines: list[str], nodes: list[dict], indent: int) -> None:
    prefix = " " * indent
    for node in nodes:
        lines.append(f"{prefix}- title: {node['title']}")
        if node["type"] == "directory":
            lines.append(f"{prefix}  children:")
            append_docs_stratego_nav_lines(lines, node["children"], indent + 4)
            continue
        lines.append(f"{prefix}  path: {node['path']}")
        lines.append(f"{prefix}  access: {node['access']}")


def clone_docs_nav_node(node: dict) -> dict:
    if node.get("type") == "directory":
        cloned = {
            "type": "directory",
            "title": node.get("title", ""),
            "children": [clone_docs_nav_node(child) for child in node.get("children", [])],
        }
        if node.get("relative_dir"):
            cloned["relative_dir"] = node["relative_dir"]
        return cloned
    return {
        "type": "page",
        "title": node.get("title", ""),
        "path": node.get("path", ""),
        "access": node.get("access", "public"),
    }


def render_docs_stratego_root_index(
    project_root: Path,
    project_name: str,
    existing_page_meta: dict[str, dict[str, str]] | None = None,
    home_access: str = "public",
    nav_nodes: list[dict] | None = None,
) -> str:
    docs_root = project_root / "docs"
    effective_nav_nodes = nav_nodes or docs_stratego_nav_nodes(
        docs_root,
        docs_root,
        project_name,
        existing_page_meta=existing_page_meta,
    )
    effective_home_access = home_access if home_access in DOCS_STRATEGO_ACCESS_LEVELS else "public"
    lines = [
        "---",
        f"title: {project_name}",
        "mkdocs:",
        f"  home_access: {effective_home_access}",
        "  nav:",
    ]
    append_docs_stratego_nav_lines(lines, effective_nav_nodes, 4)
    lines.extend(
        [
            "---",
            f"# {project_name}",
            "",
            *docs_stratego_directory_body(project_root, "", project_name, project_name),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def render_docs_stratego_directory_index(project_root: Path, project_name: str, relative_dir: str) -> str:
    title = docs_stratego_directory_title(relative_dir, project_name)
    heading = docs_stratego_directory_heading(title)
    lines = [
        f"# {heading}",
        "",
        *docs_stratego_directory_body(project_root, relative_dir, title, project_name),
    ]
    return "\n".join(lines).rstrip() + "\n"


def split_markdown_front_matter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "".join(lines[: index + 1]), "".join(lines[index + 1 :])
    return None, text


def extract_docs_nav_lines(text: str) -> tuple[list[str], int] | None:
    front_matter, _ = split_markdown_front_matter(text)
    if not front_matter:
        return None
    lines = front_matter.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "nav:":
            continue
        indent = len(line) - len(line.lstrip(" "))
        return lines[index + 1 :], indent + 2
    return None


def infer_docs_nav_directory_relative_dir(node: dict) -> str:
    if node.get("type") != "directory":
        return ""
    for child in node.get("children", []):
        if child.get("type") == "page":
            path = str(child.get("path", "")).strip()
            if path.endswith("/index.md"):
                return PurePosixPath(path).parent.as_posix()
    return ""


def annotate_docs_nav_directory_relative_dirs(nodes: list[dict]) -> None:
    for node in nodes:
        if node.get("type") != "directory":
            continue
        annotate_docs_nav_directory_relative_dirs(node.get("children", []))
        relative_dir = infer_docs_nav_directory_relative_dir(node)
        if relative_dir:
            node["relative_dir"] = relative_dir


def parse_docs_nav_nodes_from_lines(lines: list[str], start_index: int, item_indent: int) -> tuple[list[dict], int]:
    nodes: list[dict] = []
    index = start_index
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent < item_indent:
            break
        if indent != item_indent or not stripped.startswith("- title:"):
            break

        node: dict = {
            "title": docs_stratego_trim_scalar(stripped.split(":", 1)[1]),
        }
        index += 1
        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            if not stripped:
                index += 1
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent <= item_indent:
                break
            if indent == item_indent + 2 and stripped == "children:":
                children, next_index = parse_docs_nav_nodes_from_lines(lines, index + 1, item_indent + 4)
                node["type"] = "directory"
                node["children"] = children
                index = next_index
                continue
            if indent == item_indent + 2 and stripped.startswith("path:"):
                node["type"] = "page"
                node["path"] = docs_stratego_trim_scalar(stripped.split(":", 1)[1])
                index += 1
                continue
            if indent == item_indent + 2 and stripped.startswith("access:"):
                node["access"] = docs_stratego_trim_scalar(stripped.split(":", 1)[1])
                index += 1
                continue
            index += 1
        if node.get("type") == "page" and node.get("path"):
            node.setdefault("access", "public")
            nodes.append(node)
            continue
        if node.get("type") == "directory":
            node.setdefault("children", [])
            nodes.append(node)
    return nodes, index


def extract_docs_nav_tree(text: str) -> list[dict] | None:
    result = extract_docs_nav_lines(text)
    if not result:
        return None
    lines, item_indent = result
    nodes, _ = parse_docs_nav_nodes_from_lines(lines, 0, item_indent)
    if not nodes:
        return None
    annotate_docs_nav_directory_relative_dirs(nodes)
    return nodes


def extract_docs_home_access(text: str) -> str | None:
    front_matter, _ = split_markdown_front_matter(text)
    if not front_matter:
        return None
    match = re.search(r"(?m)^\s*home_access:\s*(.+?)\s*$", front_matter)
    return match.group(1).strip() if match else None


def extract_docs_nav_page_meta(text: str) -> dict[str, dict[str, str]]:
    nav_tree = extract_docs_nav_tree(text)
    if nav_tree:
        nav: dict[str, dict[str, str]] = {}

        def collect(nodes: list[dict]) -> None:
            for node in nodes:
                if node.get("type") == "page":
                    path = str(node.get("path", "")).strip()
                    if not path:
                        continue
                    nav[path] = {
                        "title": str(node.get("title", "")).strip(),
                        "access": str(node.get("access", "")).strip(),
                    }
                    continue
                collect(node.get("children", []))

        collect(nav_tree)
        return nav

    front_matter, _ = split_markdown_front_matter(text)
    if not front_matter:
        return {}

    title_pattern = re.compile(r"^\s*-\s*title:\s*(.+?)\s*$")
    path_pattern = re.compile(r"^\s*path:\s*(.+?)\s*$")
    access_pattern = re.compile(r"^\s*access:\s*(.+?)\s*$")
    nav: dict[str, dict[str, str]] = {}
    current_title = ""
    pending_path: str | None = None
    for line in front_matter.splitlines():
        title_match = title_pattern.match(line)
        if title_match:
            current_title = title_match.group(1).strip()
            pending_path = None
            continue
        path_match = path_pattern.match(line)
        if path_match:
            pending_path = path_match.group(1).strip()
            nav.setdefault(pending_path, {})
            if current_title:
                nav[pending_path]["title"] = current_title
            continue
        access_match = access_pattern.match(line)
        if access_match and pending_path:
            nav.setdefault(pending_path, {})
            nav[pending_path]["access"] = access_match.group(1).strip()
            pending_path = None
    return nav


def merge_docs_nav_nodes(existing_nodes: list[dict], generated_nodes: list[dict]) -> list[dict]:
    generated_pages = {
        str(node.get("path", "")).strip(): node
        for node in generated_nodes
        if node.get("type") == "page" and str(node.get("path", "")).strip()
    }
    generated_directories = {
        str(node.get("relative_dir", "")).strip(): node
        for node in generated_nodes
        if node.get("type") == "directory" and str(node.get("relative_dir", "")).strip()
    }
    consumed_pages: set[str] = set()
    consumed_directories: set[str] = set()
    merged: list[dict] = []

    for existing in existing_nodes:
        if existing.get("type") == "page":
            path = str(existing.get("path", "")).strip()
            generated = generated_pages.get(path)
            if not generated:
                continue
            merged.append(
                {
                    "type": "page",
                    "title": str(existing.get("title", "")).strip() or str(generated.get("title", "")).strip(),
                    "path": path,
                    "access": str(existing.get("access", "")).strip() or str(generated.get("access", "public")).strip(),
                }
            )
            consumed_pages.add(path)
            continue

        if existing.get("type") != "directory":
            continue
        relative_dir = str(existing.get("relative_dir", "")).strip()
        generated = generated_directories.get(relative_dir) if relative_dir else None
        if not generated:
            continue
        merged_children = merge_docs_nav_nodes(existing.get("children", []), generated.get("children", []))
        if not merged_children:
            continue
        merged.append(
            {
                "type": "directory",
                "title": str(existing.get("title", "")).strip() or str(generated.get("title", "")).strip(),
                "relative_dir": relative_dir,
                "children": merged_children,
            }
        )
        consumed_directories.add(relative_dir)

    for generated in generated_nodes:
        if generated.get("type") == "page":
            path = str(generated.get("path", "")).strip()
            if path and path not in consumed_pages:
                merged.append(clone_docs_nav_node(generated))
            continue
        if generated.get("type") == "directory":
            relative_dir = str(generated.get("relative_dir", "")).strip()
            if relative_dir and relative_dir not in consumed_directories:
                merged.append(clone_docs_nav_node(generated))

    return merged


def extract_docs_nav_access_map(text: str) -> dict[str, str | None]:
    return {
        path: meta.get("access")
        for path, meta in extract_docs_nav_page_meta(text).items()
    }


def extract_explicit_anchor_ids(text: str) -> set[str]:
    anchors: set[str] = set()
    for match in EXPLICIT_HTML_ANCHOR_PATTERN.finditer(text):
        anchor = (match.group(1) or match.group(2) or "").strip()
        if anchor:
            anchors.add(anchor)
    return anchors


def extract_self_anchor_targets(text: str) -> set[str]:
    anchors: set[str] = set()
    for match in MARKDOWN_LINK_PATTERN.finditer(text):
        target = match.group("target").strip()
        if not target.startswith("#"):
            continue
        anchor = target[1:].strip()
        if anchor:
            anchors.add(anchor)
    return anchors


def merge_docs_stratego_root_index(project_root: Path, project_name: str, existing_text: str | None = None) -> str:
    if not existing_text:
        return render_docs_stratego_root_index(project_root, project_name)

    existing_page_meta = extract_docs_nav_page_meta(existing_text)
    home_access = extract_docs_home_access(existing_text) or "public"
    existing_nav_tree = extract_docs_nav_tree(existing_text)
    generated_nav_tree = docs_stratego_nav_nodes(
        project_root / "docs",
        project_root / "docs",
        project_name,
        existing_page_meta=existing_page_meta,
    )
    merged_nav_tree = (
        merge_docs_nav_nodes(existing_nav_tree, generated_nav_tree)
        if existing_nav_tree
        else generated_nav_tree
    )
    generated = render_docs_stratego_root_index(
        project_root,
        project_name,
        existing_page_meta=existing_page_meta,
        home_access=home_access,
        nav_nodes=merged_nav_tree,
    )
    generated_front_matter, generated_body = split_markdown_front_matter(generated)
    if not generated_front_matter:
        return generated

    _, existing_body = split_markdown_front_matter(existing_text)
    preserved_body = existing_body.lstrip("\n")
    if not preserved_body.strip():
        preserved_body = generated_body.lstrip("\n")
    return f"{generated_front_matter}\n{preserved_body.rstrip()}\n"


def looks_like_generated_directory_index(text: str) -> bool:
    stripped = text.strip()
    if not stripped or stripped.startswith("---"):
        return False
    if "\n## " in text or "\n### " in text:
        return False
    first_nonempty = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_nonempty.startswith("# "):
        return False
    return (
        "本目录收纳" in text
        or "目录树、页面路径和访问级别统一由根 `docs/index.md` 声明" in text
        or "建议阅读顺序：" in text
    )


def should_rewrite_directory_index(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.strip():
        return True
    return "mkdocs:" in text or looks_like_generated_directory_index(text)


def docs_stratego_directories(project_root: Path, docs_profile: dict | None = None) -> list[str]:
    docs_root = project_root / "docs"
    directories: list[str] = []
    if not docs_root.exists():
        return directories
    profile = normalize_docs_profile(docs_profile or resolve_project_docs_profile(project_root))
    for directory in sorted(docs_root.rglob("*")):
        if not directory.is_dir():
            continue
        relative_dir = directory.relative_to(docs_root)
        if not relative_dir.parts:
            continue
        if "assets" in relative_dir.parts or any(part.startswith(".") for part in relative_dir.parts):
            continue
        if not docs_relative_path_enabled(relative_dir.as_posix(), profile, docs_root):
            continue
        directories.append(relative_dir.as_posix())
    return directories


def build_docs_stratego_indexes(project_root: Path, project_name: str) -> dict[str, str]:
    docs_root = project_root / "docs"
    if not docs_root.exists():
        return {}
    docs_profile = resolve_project_docs_profile(project_root, project_name=project_name)
    outputs = {"docs/index.md": render_docs_stratego_root_index(project_root, project_name)}
    for relative_dir in docs_stratego_directories(project_root, docs_profile):
        outputs[f"docs/{relative_dir}/index.md"] = render_docs_stratego_directory_index(project_root, project_name, relative_dir)
    return outputs


def write_docs_stratego_indexes(project_root: Path, project_name: str) -> list[str]:
    raise RuntimeError(
        "`write_docs_stratego_indexes` 已退场；根 `docs/index.md` 与顶层模块 `index.md` 由文档模板和人工维护。"
    )


def upgrade_docs_source_standard(project_root: Path, project_name: str, *, force: bool = False) -> dict[str, object]:
    raise RuntimeError(
        "`upgrade_docs_source_standard` 已退场；请使用 `document-templates` skill 重构文档，并以 `docs-stratego source validate` 作为收口。"
    )


def docs_stratego_valid_relative_page_path(relative_path: str) -> bool:
    raw = relative_path.strip()
    if not raw or raw.startswith("/"):
        return False
    pure_path = PurePosixPath(raw)
    parts = pure_path.parts
    if any(part == ".." for part in parts):
        return False
    if "assets" in parts:
        return False
    return is_docs_stratego_page_file(raw)


def docs_stratego_contract_validation_errors(path: Path) -> list[str]:
    if is_docs_openapi_contract(path):
        metadata = parse_openapi_contract_metadata(path)
        errors: list[str] = []
        if not metadata["openapi"]:
            errors.append("缺少 `openapi` 版本声明")
        if not metadata["title"]:
            errors.append("缺少 `info.title`")
        if not metadata["version"]:
            errors.append("缺少 `info.version`")
        return errors
    if is_docs_mcp_tools_contract(path):
        metadata = parse_mcp_tools_contract_metadata(path)
        if metadata.get("valid"):
            return []
        return ["缺少非空 `tools` 列表，或工具条目未声明 `name` / `description` / `inputSchema`"]
    return []


def docs_stratego_source_status(project_root: Path, project_name: str) -> tuple[str, list[str]]:
    return docs_stratego_validate_status(project_root)


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
                    "write_targets": list(entry.get("write_targets", [])),
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


def normalize_write_targets(project_root: Path, raw_targets: str | Sequence[str] | None) -> list[str]:
    if isinstance(raw_targets, str):
        source = parse_list(raw_targets)
    else:
        source = [str(item).strip() for item in (raw_targets or []) if str(item).strip()]
    normalized: list[str] = []
    seen = set()
    project_root = project_root.expanduser().resolve()
    for item in source:
        text = str(item).strip().replace("\\", "/")
        if not text:
            continue
        if text in {"*", ".", "./"}:
            candidate = "."
        else:
            try:
                path = Path(text).expanduser()
                if path.is_absolute():
                    candidate = Path(os.path.relpath(path.resolve(), project_root)).as_posix()
                else:
                    candidate = PurePosixPath(text).as_posix()
            except Exception:
                candidate = PurePosixPath(text).as_posix()
            candidate = candidate.strip("/")
            if not candidate or candidate == ".":
                candidate = "."
        if candidate in seen:
            continue
        seen.add(candidate)
        normalized.append(candidate)
    return normalized


def assignment_write_targets(project_root: Path, assignment: dict | None) -> list[str]:
    if not assignment:
        return []
    return normalize_write_targets(project_root, assignment.get("write_targets", []))


def write_targets_overlap(left: str, right: str) -> bool:
    left_target = (left or "").strip().strip("/")
    right_target = (right or "").strip().strip("/")
    if not left_target or not right_target:
        return False
    if left_target in {".", "*"} or right_target in {".", "*"}:
        return True
    left_parts = PurePosixPath(left_target).parts
    right_parts = PurePosixPath(right_target).parts
    if left_parts == right_parts:
        return True
    if len(left_parts) < len(right_parts):
        return right_parts[: len(left_parts)] == left_parts
    return left_parts[: len(right_parts)] == right_parts


def role_assignment_conflicts(
    project_root: Path,
    config: dict,
    *,
    include_completed: bool = False,
    candidate_role_id: str = "",
    candidate_assignment: dict | None = None,
) -> list[dict]:
    ensure_role_catalog(config)
    assignments = ensure_role_assignment_state(config)
    stage_roles = {
        role.get("id", ""): role
        for role in active_roles_for_stage(config, config.get("stage", ""))
    }
    records: list[dict] = []
    for role_id, payload in assignments.items():
        if not isinstance(payload, dict):
            continue
        if not include_completed and payload.get("status") == "已完成":
            continue
        if not assignment_write_targets(project_root, payload):
            continue
        records.append(
            {
                "role_id": role_id,
                "role_title": stage_roles.get(role_id, resolve_role(config, role_id)).get("title", role_id),
                "assignment": payload,
                "write_targets": assignment_write_targets(project_root, payload),
            }
        )
    if candidate_role_id and candidate_assignment:
        records = [item for item in records if item["role_id"] != candidate_role_id]
        if include_completed or candidate_assignment.get("status") != "已完成":
            candidate_targets = assignment_write_targets(project_root, candidate_assignment)
            if candidate_targets:
                candidate_role = resolve_role(config, candidate_role_id)
                records.append(
                    {
                        "role_id": candidate_role_id,
                        "role_title": candidate_role.get("title", candidate_role_id),
                        "assignment": candidate_assignment,
                        "write_targets": candidate_targets,
                    }
                )

    conflicts: list[dict] = []
    for index, left in enumerate(records):
        for right in records[index + 1 :]:
            overlaps: list[tuple[str, str]] = []
            for left_target in left["write_targets"]:
                for right_target in right["write_targets"]:
                    if write_targets_overlap(left_target, right_target):
                        overlaps.append((left_target, right_target))
            if not overlaps:
                continue
            conflicts.append(
                {
                    "roles": [left["role_id"], right["role_id"]],
                    "role_titles": [left["role_title"], right["role_title"]],
                    "owners": [
                        left["assignment"].get("owner", "") or left["role_title"],
                        right["assignment"].get("owner", "") or right["role_title"],
                    ],
                    "targets": [
                        sorted({item[0] for item in overlaps}),
                        sorted({item[1] for item in overlaps}),
                    ],
                    "overlaps": [f"{item[0]} <-> {item[1]}" for item in overlaps],
                }
            )
    return conflicts


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
    ]
    if include_ai:
        ordered.extend(
            [
                RUNTIME_BRIEF_RELATIVE,
                ROLE_CHARTER_PROJECT_RELATIVE,
                DOC_MAP_RELATIVE,
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


def role_recommended_commands(
    project_root: Path,
    config: dict,
    role_query: str | None,
    owner: str,
    focus: str = "",
    *,
    limit: int | None = 8,
) -> list[str]:
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
                dispatch_command(project_root, "doc", "--doc", "docs/04-project-development/03-requirements/prd.md", "--summary", "补充需求细节"),
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
                dispatch_command(project_root, "design-assets", "--title", "关键页面设计图", "--images", "./docs/04-project-development/04-design/assets/mockup.png", "--owner", owner),
                dispatch_command(project_root, "motivation", "--role", role_id, "--owner", owner, "--focus", focus or "保持设计协作动能"),
                dispatch_command(project_root, "doc", "--doc", "docs/04-project-development/04-design/ux-ui-design.md", "--summary", "补充 UX/UI 设计"),
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
    if limit is None:
        return deduped
    return deduped[: max(1, limit)]


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


def normalize_project_config(config: dict) -> dict:
    normalized = dict(config)
    if not normalized.get("stage") and normalized.get("current_stage"):
        normalized["stage"] = normalized["current_stage"]
    if not normalized.get("active_mode"):
        legacy_mode = normalized.get("current_mode") or normalized.get("default_active_mode")
        if legacy_mode:
            normalized["active_mode"] = legacy_mode
    normalized["docs_profile"] = normalize_docs_profile(normalized.get("docs_profile"))
    return normalized


def load_project_config(project_root: Path) -> dict:
    ensure_project(project_root)
    return normalize_project_config(json.loads(project_config_path(project_root).read_text(encoding="utf-8")))


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
        "crawler4j": "crawler4j-model",
        "crawler4jmodel": "crawler4j-model",
        "crawler4jmodule": "crawler4j-model",
        "crawler4jcoremodel": "crawler4j-model",
        "crawler4jmodelproject": "crawler4j-model",
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


def run_step(
    command: Sequence[str],
    label: str,
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> dict:
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        list(command),
        capture_output=True,
        text=True,
        cwd=str(cwd) if cwd else None,
        env=merged_env,
    )
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


def docs_stratego_package_spec() -> str:
    return os.environ.get(DOCS_STRATEGO_PACKAGE_SPEC_ENV, "").strip() or "docs-stratego"


def docs_stratego_validate_status(project_root: Path, docs_dir: str = "docs") -> tuple[str, list[str]]:
    args = ["source", "validate", "--repo-path", str(project_root), "--docs-dir", docs_dir]
    attempts: list[tuple[list[str], dict[str, str] | None]] = []
    package_spec = docs_stratego_package_spec()
    uv_env = {"UV_CACHE_DIR": os.environ.get("UV_CACHE_DIR", DEFAULT_UV_CACHE_DIR)}

    if command_available("uvx"):
        attempts.append((["uvx", "--from", package_spec, "docs-stratego", *args], uv_env))
    elif command_available("uv"):
        attempts.append((["uv", "tool", "run", "--from", package_spec, "docs-stratego", *args], uv_env))

    if not attempts:
        return (
            "缺失",
            [
                "- 未找到可执行的 `uvx` / `uv`，无法调用 PyPI 已发布的 `docs-stratego` CLI。",
                "- 请先安装 `uv`，再执行 `uvx --from docs-stratego docs-stratego ...`。",
            ],
        )

    failures: list[str] = []
    for command, env in attempts:
        result = run_step(command, "docs-stratego source validate", cwd=project_root, env=env)
        if result["returncode"] == 0:
            summary = result["stdout"] or result["stderr"] or "校验通过。"
            return (
                "就绪",
                [
                    f"- 已执行 `{' '.join(command)}`。",
                    f"- {summary}",
                ],
            )
        detail = result["stderr"] or result["stdout"] or "无输出"
        failures.append(f"- `{' '.join(command)}` 失败：{detail}")

    return ("异常", failures)


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
        - 若进入设计或实施阶段，先确认 `docs/04-project-development/04-design/technical-selection.md` 已明确框架、模块、后台范围和编码规则
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
