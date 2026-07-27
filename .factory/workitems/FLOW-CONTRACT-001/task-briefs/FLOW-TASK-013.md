# FLOW-TASK-013 增加项目级测试治理

## 工作项

- 工作项：`FLOW-CONTRACT-001`
- 任务：`FLOW-TASK-013`
- 状态：`completed_independently_approved`
- 上游计划：`.factory/workitems/FLOW-CONTRACT-001/plan.md`
- 流水账：`.factory/workitems/FLOW-CONTRACT-001/ledger.jsonl`

## 目标

建立整体黑盒测试、UI 测试、接口测试、发布回归和测试环境基线的文档与 skill 规则。

## 输入

- `docs/04-product/prd.md`
- `docs/05-design/workflow-execution-design.md`
- `docs/06-delivery/test-plan.md`
- `skills/verification-before-completion/SKILL.md`
- `skills/webapp-testing/SKILL.md`
- `skills/api-design/SKILL.md`

## 允许修改

- `skills/verification-before-completion/SKILL.md`
- `skills/webapp-testing/SKILL.md`
- `skills/api-design/SKILL.md`
- `skills/document-templates/SKILL.md`
- `skills/document-templates/references/test-environment-template.md`
- `docs/06-delivery/test-plan.md`
- 相关测试。

## 禁止修改

- 与测试治理无关的 workflow skill。
- 旧中心脚本。

## 验证命令

```bash
.venv/bin/python -m pytest -q tests/test_project_test_governance.py
```

期望输出：

```text
9 passed；同步执行相邻 Skill 与项目管理测试。
```

## 完成口径

实现者只能写 `ready_for_review`。测试环境规则必须说明启动命令、端口、健康检查和关闭方式。
