# T04 独立评审

- Work item: `PK-SOURCE-MIGRATION-001`
- Task: `PK-SOURCE-MIGRATION-001-T04`
- reviewer_type: `independent_subagent`
- reviewer_id: `/root/project_knowledge_review`
- reviewer_independence_evidence: 本 reviewer 未参与 T04 的设计、实现或文件修改；仅依据
  文件化 review input、task brief、实施报告、验证证据、限定 diff 及只读验证结果进行
  独立复核。
- review_status: `changes_requested`
- next_gate_status: `changes_requested`
- author_self_check_score: `n/a`
- review_score: `67`

评分：

- 需求符合度：`18 / 30`
- 架构一致性：`18 / 20`
- 测试充分性：`12 / 20`
- 代码质量：`14 / 20`
- 文档与记忆同步：`5 / 10`

## Findings

### Critical

- 无。

### Important

- `T04-I1`（`src/runtime/project_knowledge/extractors.py:74`）：任务简报识别和语义章节
  映射只接受有限的中文固定格式。只读语料验证中，注册路径下 138 份 task brief 仅
  75 份生成 `work_item`；其中仅 42 份提取到 `work_items`，5 份提取到
  `deliverables`。应覆盖仓内已登记的中英文、编号章节及既有稳定格式，并加入真实注册
  语料的覆盖或清单测试。
- `T04-I2`（`src/runtime/project_knowledge/site_renderer.py:1149`）：缺少正式语义时，
  renderer 会生成“完成某任务所描述的工作”等推测性文案，与“不猜测缺失说明”的
  设计冲突。应改为明确空态，或仅展示实际索引中存在的正式语义。
- `T04-I3`（`docs/05-design/data-design.md:8`、
  `docs/05-design/frontend-design.md:8`）：T04 尚处于评审时已写成新的正式版本，
  并保留已批准署名和仅已发布历史，提前宣告了尚未发生的人工批准。应在确认前保持
  候选状态，或延后正式版本和发布历史更新。

### Minor

- 无。

## Verification

- 目标测试：`64 passed in 0.99s`。
- Ruff：`All checks passed`。
- Mypy：`Success: no issues found in 279 source files`。
- 限定路径 `git diff --check`：退出码 `0`。
- 注册任务简报只读提取探针：
  `138 total / 75 work_item / 42 work_items / 5 deliverables`。

## Gate

`changes_requested`
