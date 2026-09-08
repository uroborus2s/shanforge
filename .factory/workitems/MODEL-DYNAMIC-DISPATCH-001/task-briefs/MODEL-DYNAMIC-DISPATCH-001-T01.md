# 动态子任务合同与正式说明

- work_item_id: MODEL-DYNAMIC-DISPATCH-001
- task_card_id: MODEL-DYNAMIC-DISPATCH-001-T01
- wbs_id: WBS-MODEL-DYNAMIC-01
- status: closed
- owner: dynamic_dispatch_contract
- priority: P1
- task_scope: system
- depends_on: MODEL-ORCHESTRATOR-SELECTION-001 已提交；T02 已记录 RED
- review_status: approved
- current_gate: closed
- next_required_action: none
- write_policy: source_or_test_write
- control_model: user_selected
- task_complexity: complex
- risk_level: medium
- reasoning_demand: judgment
- execution_model: gpt-6-astra
- requested_reasoning_effort: high
- execution_authorized: true
- dispatch_role: worker
- dispatch_required: true
- dispatch_mode: subagent
- fork_turns: none
- capability_source: current collaboration.spawn_agent schema
- route_reason: 跨 skill 合同、阶段、角色与能力边界需要工程判断；无生产或不可逆修改，选择 Astra/high。

## 精确写集

- AGENTS.md
- .codex/agents/task-reader.toml
- skills/using-shanforge/SKILL.md
- skills/using-shanforge/references/codex-tools.md
- skills/using-shanforge/references/black-box-flow-eval.md
- skills/using-shanforge/agents/openai.yaml
- skills/subagent-driven-development/SKILL.md
- skills/subagent-driven-development/references/status-handling-checklist.md
- skills/writing-plans/SKILL.md
- skills/writing-plans/references/task-brief-template.md
- docs/02-user-guide/user-guide.md
- docs/04-product/prd.md
- docs/05-design/workflow-execution-design.md

## 实施与验收

完整要求来自本工作项 brief 与 plan 共享合同。只改当前生效段落，不改历史版本表或历史 WorkItem。单一选档表位于 using-shanforge/SKILL.md，其他文档引用和简明说明；不复制同一矩阵多份。保持主会话用户选择、旧 preset 及并发配置；不写 .codex/config.toml。

新增 reasoning_demand 与 capability_source、沿用 route_reason，显式 model+reasoning_effort+fork_turns=none。派发回执仍只证明宿主接受请求，不宣称底层模型身份；把 role 不匹配和能力不支持并入既有失败关闭。升级必须新派发，followup_task 只限同模型/强度/角色；不伪造跟随调用可改配置。只读 analyst 不改变父阶段、不写文件、不自批，常规直接回答不强制派发。

task-reader.toml 用宿主原生 role 格式，只固定只读职责与 sandbox_mode=read-only，不固定模型/effort；当前会话未加载就明确不可用，不能冒充热更新，当前普通 reviewer 可用已暴露 Terra/high preset。角色与调用模型/强度矛盾时拒绝。

## 验证命令

- UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run pytest -q tests/test_dynamic_model_dispatch.py tests/test_model_tier_routing.py tests/test_black_box_workflow_eval.py tests/test_residual_audit_contracts.py
- UV_CACHE_DIR=/private/tmp/shanforge-uv-cache uv run python /Users/uroborus/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/using-shanforge
- git diff --check

T02 拥有测试，失败涉及测试更新请给父会话回报，不自行修改测试。受保护 .codex 写入若失败，提供精确完整内容交父会话走审批，不绕过保护。

## 禁令与返回

你不是唯一执行者，不回滚他人改动。不写测试、历史材料、.factory/、全局配置、并发数，不提交、不推送、不自批，不新增 runtime/依赖/调度脚本。按 skill-creator 保持中文简洁；返回 DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED、修改文件、验证命令/exit code/结果及 concerns。

## 本轮目录补充

实施目录为 /private/tmp/shanforge-dynamic-dispatch-01a07e6a；原精确相对写集映射至该目录。禁止改主工作区共享文件；合入由父会话在前置提交后组织。
