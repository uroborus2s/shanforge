# WRITING-PLANS-SIMPLE-GATE-001-T01

- 状态：`approved_ready_for_local_commit`
- 目标：为简单局部改动增加 `not_applicable / simple_change` 快速退出。
- 允许路径：
  - `skills/writing-plans/SKILL.md`
  - `skills/writing-plans/agents/openai.yaml`
  - `tests/test_writing_plans_skill.py`
  - `tests/test_work_skill_status_envelope_ownership.py` 的 writing-plans 状态行、
    writing-plans 候选哈希，以及已落库但陈旧的 HEAD Skill 哈希行
  - `.factory/workitems/WRITING-PLANS-SIMPLE-GATE-001/**`
- 验收：
  - 简单任务不生成 plan、task brief 或计划评审。
  - 明确正式计划请求覆盖简单任务判定。
  - 公共接口、跨层、schema、迁移、依赖、安全、外部系统和发布变化不得走简单路径。
  - 专属测试、相邻流程测试、共享状态节点、Ruff、format、Skill validator 通过。
- 禁止：产品代码、其他 Skill 语义、远端、发布和部署。
