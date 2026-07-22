# TASK-REQ-006 R007 复审整改响应（R008）

Fixed `R007-I-001`。R008 使用 `RequirementProjectionRoot/v1` 明确 root 前像的精确 JSON shape、字段、顺序和排除项。独立重提取得到 16 REQ、64 AC、11 NFR；逐字段/逐节 Hash 一致；root canonical bytes 为 23717，SHA-256 为 `96be53fe34052219ae3ac01326797c8e60234d7eae12f26ce5f070ac11a3045e`。

R007 PM field map 未变化，R008 复用精确 SHA-256 `1b9f2834…93f0`，避免为未变化机器合同新建副本。
