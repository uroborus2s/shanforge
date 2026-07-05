# SF-SP-002 Review Brief

## Review 目标

确认 `project-memory` 首版是否满足 Superpowers 流程集成计划中 `SF-SP-002` 的交付范围。

## 输入

- `docs/04-project-development/05-development-process/superpowers-workflow-integration-plan.md`
- `skills/project-memory/SKILL.md`
- `skills/project-memory/references/*.md`
- `skills/project-memory/agents/openai.yaml`
- `tests/test_project_memory_skill.py`
- `.factory/workitems/SF-SP-002/evidence/test-report.md`

## Spec Review 检查

- 是否接管会话恢复、读取范围和 memory 同步。
- 是否明确 `factory-agent-session` 只是迁移来源。
- 是否禁止中心脚本主控。
- 是否提供会话启动、相关性判断、会话卡、ledger、current-state 更新 references。
- 是否没有把 `SF-SP-003` 的跨 skill 模板迁移伪装成已完成。

## Quality Review 检查

- `SKILL.md` 是否足够精简。
- references 是否承载长模板和固定方法。
- 测试是否锁定关键约束且不过度绑定措辞。
- `.factory/memory/` 是否只写真实发生的事实。
- evidence 是否包含新鲜验证结果和失败偏离说明。

## 输出

输出 `approved` 或 `changes_requested`。若发现阻塞问题，按文件和段落说明。
