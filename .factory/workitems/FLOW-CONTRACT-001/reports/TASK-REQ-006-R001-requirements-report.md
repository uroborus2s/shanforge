# TASK-REQ-006 R002 需求编制报告

## 结果

- 场景：`change_requirement`。
- 状态：`R002_ready_for_independent_review`。
- 候选集合：R001 基础 + R002 生成视图增量；R001 单独评审目标已失效。
- 新增稳定变更 ID：`REQ-CHANGE-PROJECT-KNOWLEDGE-001`。
- 需求：`REQ-PKI-001..008`。
- 非功能需求：`NFR-PKI-001..007`。
- 复用 Workflow Owner：`WF-CTL-001/009/010`、`WF-BASE-008`。

## 用户要求覆盖

1. 固定命令组装项目进度：`REQ-PKI-001/008`。
2. `docs` 仅人类文档、按项目画像最小创建：`REQ-PKI-002/007`。
3. `.factory` 的单一当前记忆点和受控读取：`REQ-PKI-003/006`。
4. SQLite 文档、记忆、代码和追踪索引：`REQ-PKI-004`。
5. cache/generated 有界清理：`REQ-PKI-005`。
6. 压缩时机：事件驱动隔离任务为主，计划维护兜底，会话内不定时重压缩：`REQ-PKI-006`。
7. 命令生成离线文档 HTML：`REQ-PKI-007/008`。
8. PM 不保存事实、代码判定刷新、每个权限视图只保留最新 HTML：`REQ-PKI-009`。

## 未执行

- 未修改正式 PRD、需求矩阵、设计或文档索引。
- 未迁移 `docs` 中机器文件。
- 未修改产品代码、测试、Skill 或现有实现候选。
- 未执行 Git、远端、发布或部署。

## 验证

- JSON 合同：`python3 -m json.tool` 通过。
- 稳定 ID：8 条 REQ、7 条 NFR 与合同逐项一致。
- 候选中无 `TODO/TBD/待定`。
- Hash 和完整检查见 `evidence/TASK-REQ-006-R001-author-verification.md` 与 `evidence/TASK-REQ-006-R002-author-verification.md`。
