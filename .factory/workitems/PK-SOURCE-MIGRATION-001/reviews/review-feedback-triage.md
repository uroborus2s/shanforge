# 计划评审反馈分类

| Finding | 判断 | 处理 |
|---|---|---|
| I1 语义等价与历史身份门不足 | 成立。数量无法证明正文等价，且 R009 family 中 PM map 仍是有效机器配置。 | 增加三文件 Hash 不变量、逐字段等价测试和精确 include 移除规则。 |
| I2 warm migration 与逐项绑定不足 | 成立。当前真实升级不是只有冷重建。 | 增加 warm→cold after-image 等价、逐 ID section 和 AC parent/order/status 断言。 |
| I3 缺追踪矩阵 | 成立。示例深链不能证明完整声明。 | 在计划冻结 9 个 Task 的显式多对多矩阵，并逐边检查声明/SQLite/双方路由。 |
| I4 Markdown 安全合同不足 | 成立。仅转义不足以定义读取和解释边界。 | 限定 Markdown 子集；禁止解释链接/图片/raw HTML；补 symlink、逃逸、Hash、大小、权限负例。 |
| I5 缓存与正式设计同步不足 | 成立。renderer 输入语义变化必须失效旧页。 | bump renderer version，验证 miss→stable hit，并原位更新 data/frontend design。 |

所有 Finding 均属于用户已批准范围，不需要新增产品取舍或授权。
