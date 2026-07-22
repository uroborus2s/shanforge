# TASK-REQ-006 R006 评审整改验证

## 候选文件 Hash

| 文件 | SHA-256 |
|---|---|
| R006 Markdown | `c1c38864f6fc4d307639877d2a6956c0ed0836c289cb3aad9fd858d5ec748f92` |
| R006 机器合同 | `92f4a73e85ae90c47dcfe24f55f425697242ed6d24e611e0a346309f386d6fa3` |
| R006 PM field map | `7169c619fa75e13e4fbeb06a8e803dd9555c8f377bade641cb05e123a0895c8c` |
| pinned R014 | `836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33` |

## 结构验证结果

```text
md_requirements=16
md_ac_total=64
contract_requirements=16
contract_ac=64
nfrs=11
core_tables=29
pm_tables=10
field_map=137
unique_fields=137
r014_pin_ok=true
map_pin_ok=true
transition_count=22
nonterminal_without_outgoing=[]
all_pm_tables_used=[]
```

## 命令结果

- `jq -e`：R006 contract、PM field map 和 R014 均通过。
- Python 只读一致性校验：退出码 0；Markdown REQ 顺序与机器合同一致，每项 AC=4；pin、表数、字段唯一性、状态机闭包全部断言通过。
- 评审整改只修改 `.factory/workitems/FLOW-CONTRACT-001/` 候选/评审材料和必要 Memory 摘要；没有修改正式 `docs` 或产品代码。
