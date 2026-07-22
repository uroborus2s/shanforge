# TASK-REQ-006 R008 Root 前像验证

## Hash

| 文件 | SHA-256 |
|---|---|
| R008 Markdown | `148df85fa317880e561885cda8319c195416047562c05404bf944a5df56a5803` |
| R008 机器合同 | `15944679ce1ce9b366925c1333006333fef6cd489bbe94d62f506615eb0897c5` |
| 复用 R007 PM field map | `1b9f283483d03b63fea749c4cdda1fa918b20ed70e33f1f3ff114eb4765293f0` |
| pinned R014 | `836fadc2c214ef2f56b2a21ef2fb705445a58ca7ddb0047f3b638292ba578d33` |

## 独立重算

```text
requirements=16
acceptance_criteria=64
nfrs=11
root_preimage_keys=[requirements,nfrs]
root_excludes=[schema_id,projection_sha256,status,markdown_section_id,all_other_derived_or_envelope_fields]
root_canonical_bytes=23717
root_sha256=96be53fe34052219ae3ac01326797c8e60234d7eae12f26ce5f070ac11a3045e
fields=137
state_transitions=50
snapshot_schema=ProjectProgressSnapshot/v2
```

- R008 JSON `jq -e` 通过。
- Markdown 重提取对象与 JSON 逐字段相等；逐节 Hash、root 字节长度和 root SHA-256 全部断言通过。
- R007 已通过的 PM identity、137 字段、状态事件和 Snapshot v2 合同无回归。
