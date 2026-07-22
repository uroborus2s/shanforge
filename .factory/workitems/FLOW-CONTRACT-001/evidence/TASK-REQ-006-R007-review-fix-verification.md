# TASK-REQ-006 R007 评审整改验证

## Hash

| 文件 | SHA-256 |
|---|---|
| R007 Markdown | `6d18a7f317a4a03862a3ca279e286a7f9722be3102500062f602e7fb5cc9ebe5` |
| R007 机器合同 | `7f4ddfdfc4a1ca1f463325abbf7ce4f243faa0cadebe4aed85eb86541cf6ade3` |
| R007 PM field map | `1b9f283483d03b63fea749c4cdda1fa918b20ed70e33f1f3ff114eb4765293f0` |
| pinned R014 | `836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33` |

## 真实结果

```text
requirements=16
acceptance_criteria=64
nfrs=11
projection_root=ee2fa8abb139705d4080d49a579e6a7291b9322d7fac57bf6d57d3e2a450829e
fields=137
row_models=13
transitions=50
nonterminal_states=10
all_reach_terminal=true
snapshot_schema=ProjectProgressSnapshot/v2
```

- 两个 R007 JSON 与 R014 均通过 `jq -e`。
- 独立解析 Markdown 后，REQ/NFR 对象与机器合同逐字段完全相等，逐节 Hash 和 root Hash 断言通过。
- 137 field ID、label、snapshot path、type 与 R014 一致，value Owner 为同一 v2 path，PM 不重派生。
- state-event 声明与 transition 精确一对一；所有成功发布 transition 的复合前置条件断言通过；所有非终态可达终态。
