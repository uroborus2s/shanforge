# T01 同 Reviewer 复审（Iteration 2）

- reviewer：`/root/project_artifacts_t01_review`
- 状态：`changes_requested`
- 得分：`81 / 100`

## 剩余 Findings

- Critical：component states 会静默过滤非字符串且不拒绝重复，与 Schema 的 enum 和
  `uniqueItems` 不一致。
- Important：集成测试仍写入空 Token，但前次定向命令没有选中该测试。
- Important：Penpot、Token、export 的 Schema 路径正则仍允许 `..` 段。

`T01-I1`、`T01-I2`、`T01-I5`、`T01-M1` 已确认关闭；其余项按同范围继续整改。
