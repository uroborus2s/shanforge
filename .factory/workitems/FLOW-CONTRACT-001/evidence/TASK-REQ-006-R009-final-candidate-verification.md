# TASK-REQ-006 R009 最终候选验证

- Manifest：`.factory/workitems/FLOW-CONTRACT-001/evidence/TASK-REQ-006-R009-final-candidate-manifest.json`
- Manifest SHA-256：`8be9d829ea2a895eae043eaf054914cb03b7457a43d51c142cc4ad7f41f577ae`
- Candidate root SHA-256：`ce079fcd80c4e5e7a58e68103e8f225d2b90cdfea703c12adde88f95b3f0df68`
- Artifact 数量：6。
- Root 前像：按路径排序的 `path + NUL + sha256 + LF`，936 bytes。

验证器逐个回读 6 个 Artifact，文件大小和 SHA-256 全部与 Manifest 一致；重算 candidate root 与 Manifest 一致。R009 独立复审为 `approved / 99 / C0-I0-M0`。当前 `design_or_implementation_authorized=false`，只有 `uroborus` 对精确 Manifest SHA-256 的确认才能打开下一 Gate。
