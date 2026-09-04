# UI-DESIGN-MASTER-001-T01：重构 UI 设计与美术资源职责

- work_item_id: `UI-DESIGN-MASTER-001`
- task_card_id: `UI-DESIGN-MASTER-001-T01`
- wbs_id: `WBS-UI-DESIGN-MASTER-01`
- current_gate: `closed`
- workflow_id: `execution-workflow`
- write_policy: `source_or_test_write`
- risk_level: `low`
- task_complexity: `standard`
- control_model: `gpt-5.6-sol`
- execution_model: `gpt-5.6-terra`
- requested_reasoning_effort: `medium`
- execution_authorized: `true`
- dispatch_role: `worker`
- dispatch_required: `true`
- dispatch_mode: `subagent`
- fork_turns: `none`

## 允许修改

- `skills/ui-ux-pro-max/SKILL.md`
- `skills/ui-ux-pro-max/agents/openai.yaml`
- `skills/ui-ux-pro-max/references/design-workflow-and-deliverables.md`
- `skills/ui-ux-pro-max/references/mobile-high-fidelity.md`
- `skills/art-asset-pipeline/SKILL.md`
- `skills/using-shanforge/SKILL.md`
- `tests/test_ui_ux_pro_max_skill.py`
- `tests/test_task_workflow_semantics.py`
- `tests/test_art_asset_manifest_contract.py`
- `.factory/workitems/UI-DESIGN-MASTER-001/`
- `.factory/memory/agent-session.md`
- `.factory/memory/current-state.md`
- `.factory/memory/skill-updates.summary.md`
- `.factory/memory/tasks.summary.md`
- `.factory/memory/tests.summary.md`
- `.factory/memory/review-ledger.jsonl`

## 禁止动作

- 不修改上述范围外文件。
- 不新增依赖、脚本、模板或设计资产。
- 不重命名 skill 目录或 frontmatter `name`。
- 不改变 `art-asset-pipeline/scripts/validate_manifest.py`。
- 不执行 Git commit、push、PR、发布、分支切换或历史改写。
- 实现者不得自批评审通过或修改 `.factory/memory/`。

## 实现要求

- `ui-ux-pro-max` 是 UI 唯一入口，完整覆盖 UI 设计和 UI 素材交付。
- `art-asset-pipeline` 只处理不属于 UI 项目流程的独立美术和游戏资源生产。
- 删除 UI skill 对 `art-asset-pipeline` 的调用要求；可以直接使用 `imagegen` 生成需要的位图素材。
- 保持双确认门：先确认美术方向，再确认资源清单，之后才生产正式 UI 素材。
- 交付规则明确但避免重复：可编辑设计源及版本是主交付，PNG/PDF 只作预览，正式素材进入 `assets/` 并附 manifest。
- 普通控件、真实文字、状态和通用图标由组件、平台能力或现有图标库实现，不烘焙进图片。
- 不得定义函数体内命名函数，不抽取单调用点公共 helper；本任务预计不修改 Python 实现。

## 验证

- 修改语义测试以锁定新的职责边界和交付要求。
- 运行 UI/UX、资源管线和流程路由相关定向测试。
- 运行两个 skill 的 `quick_validate.py`。
- 实现完成后由未参与实现的 Terra/high 中文语言专家只读评审。
