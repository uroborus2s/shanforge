# T01 清理与恢复清单

## 备份

- 文件：`/tmp/shanforge-model-routing-001-untracked-backup-20260823.tar.gz`
- 大小：23M（源目录约 95M）
- SHA-256：`d6f10dba59b29e050c58ac36c7b82f4ebb3a395d9dbf23c201e31f01e2aef840`
- 条目数：1806
- `gzip -t`：exit 0

## 已清理类别

- `FLOW-CONTRACT-001`：旧版本草稿、R020 候选、全量机器 payload、原始运行证据、
  多轮 review 过程材料和已被正式基线取代的 TaskCard。
- `PM-DASHBOARD-004`：已被 skill-first 边界取代的未跟踪计划、报告、证据和 review。
- `PM-DASHBOARD-005`：旧 UI 轮次截图、浏览器脚本、原始结果和多轮 review 过程材料。
- 保留 DOC 重构、FLOW 合同测试和 PM 第七轮人工 UI Gate 所需的最小审计资产。

完整逐文件清单由归档自身的 `tar -tzf` 确定；归档中包含清理前目录树，恢复时解压到
临时目录，不覆盖当前工作区。

## 最小恢复校验

从归档流式提取三个代表性保留文件，与当前文件 SHA-256 比较，三项完全一致：

| 文件 | SHA-256 |
|---|---|
| `drafts/docs-information-architecture.R019.json` | `a7993390236d63acf2122f3f5234b2020901ad6cf52f25bb4df397100a58c85b` |
| `evidence/FLOW-TASK-012-gate-smoke-transcript.v2.md` | `e76ac325d71d3c822c4f365e297a48395370397991fa0ff2cb421ff1b06393f1` |
| `evidence/TASK-SKILL-003-P001-black-box-transcript.md` | `c3e4380f4a660a34d42ac33ec3b5f89ae14ee62cc9aeea740181ef5d76084dd0` |
