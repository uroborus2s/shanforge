# 独立评审输入

- 评审对象：6 个目标 ledger 的新增提交回执，以及本 WorkItem 的 brief、task brief、报告和 ledger。
- 核对重点：
  1. commit SHA 是否真实存在且为当前 `HEAD` 祖先；
  2. commit 是否包含对应目标 WorkItem；
  3. 关闭状态是否越过仍开放的 EAD、PM Gate；
  4. 写集是否严格限定为 task brief 中的允许路径；
  5. 所有 ledger 是否为合法 JSONL。
- `FLOW-CONTRACT-001/ledger.jsonl` 明确排除，避免混入其已有并行改动。
- 评审者不得修改文件或 Git index。
