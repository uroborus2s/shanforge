# 历史证据边界修正

- 问题：旧新鲜性测试把已关闭 WorkItem 的候选 manifest 当作当前输入缓存，导致后续合法合同变更要求改写历史哈希。
- 根因：测试混淆“当时被评审的候选内容”和“当前工作树内容”。
- 修正：精确恢复四条原始 digest；用 review brief 记录的 manifest SHA-256 验证历史清单未变，同时只对当前 raw inputs 与 observation evidence 做当前文件一致性检查。
- 原 manifest SHA-256：`3e86f667d21da7aac61aaa388fd9f642a233e3d12714ae47ea7a761c074ae4dc`。
- 边界：没有重跑、替换或重新解释旧 v3 observations；当前合同的模型 owner 语义由本 WorkItem 的独立 review 和现行回归覆盖。
