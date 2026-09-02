# T10：补齐可执行性与真实样本验证

- task_card_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T10`
- wbs_id: `WBS-AUDIT-10`
- status: `completed`
- priority: `P0`
- task_scope: `system`
- owner: `/root/t10_executable_validation`
- depends_on: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001-T09`
- risk_level: `medium`
- execution_authorized: `true`
- current_gate: `closed`
- next_required_action: `activate_t11`
- write_policy: `source_or_test_write`
- control_model: `gpt-5.6-sol`
- task_complexity: `complex`
- execution_model: `gpt-5.6-terra`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- dispatched_to: `/root/t10_executable_validation`
- dispatch_id: `SOFTWARE-ENGINEERING-SKILL-AUDIT-CLOSURE-001:T10:terra-medium:v3`
- requested_reasoning_effort: `medium`
- fork_turns: `none`
- route_reason: `跨 DOCX/XLSX/资源验证的中风险 source/test 工作`
- allowed_paths: `skills/docx/SKILL.md`, `skills/docx/scripts/office/pack.py`, `skills/docx/scripts/office/unpack.py`, `skills/docx/scripts/office/validate.py`, `skills/xlsx/SKILL.md`, `skills/xlsx/scripts/office/pack.py`, `skills/xlsx/scripts/office/unpack.py`, `skills/xlsx/scripts/office/validate.py`, `skills/art-asset-pipeline/SKILL.md`, `skills/art-asset-pipeline/scripts/validate_manifest.py`, `skills/verification-before-completion/SKILL.md`, `skills/crawler4j-model-project/SKILL.md`, `skills/crawler4j-model-project/scripts/check_compatibility.py`, `skills/stratix-service/SKILL.md`, `skills/stratix-service/references/cli-workflow.md`, `skills/stratix-service/scripts/check_compatibility.py`, `skills/tdd-workflow/SKILL.md`, `skills/tdd-workflow/scripts/check_code_shape.py`, `tests/test_external_tool_skill_fallbacks.py`, `tests/test_office_skill_roundtrip.py`, `tests/test_art_asset_manifest_contract.py`, `tests/test_crawler4j_model_skill_integration.py`, `tests/test_stratix_service_skill.py`, `tests/test_stratix_service_framework_guide.py`, `tests/test_verification_debugging_workflow_skills.py`, `tests/test_code_shape_check.py`, `tests/test_writing_plans_skill.py`, `tests/test_using_shanforge_snapshot.py`
- forbidden_actions: 新增依赖、修改范围外 Skill、建立通用 OOXML 框架、函数套函数、单调用点无职责公共 helper、修改 memory/Git/远端

## 验收

- DOCX/XLSX 最小样本完成解包→打包→再次验证。
- manifest 样本通过所属 Skill 的真实脚本拒绝缺失文件和 `tmp/` 路径，测试内不得重写校验逻辑。
- Crawler4j/Stratix 有所属 Skill 的真实兼容检查脚本；兼容与不兼容 fixture 必须直接执行该脚本，不得只检查 Markdown 或手写字符串退出码。
- `code_shape_check` 有标准库机械入口，至少拒绝函数/方法内部命名函数并报告单调用 helper 候选。
- 正式计划模板、TaskCard、ledger 和 PM 快照有真实贯通测试。
- 只在失败测试证明需要时修改现有脚本。
- Office 生产脚本不得把 `defusedxml` 回退为标准 XML 解析器；缺失依赖只能由隔离测试能力或 blocked 合同处理。
- 新增 Python 不得留下无独立职责且只有一个调用点的公共函数。
- 返回 `code_shape_check: passed|failed`。
