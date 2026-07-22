# TASK-REQ-006 R007 反馈分诊（R008）

## `R007-I-001`

- 技术核实：正确。R007 作者计算把 `projection_sha256` 派生字段包含进 root，但文字更容易被解释为仅规范字段；两种前像都合理，合同不够明确。
- 决定：Fixed in R008。
- 修正：root 前像固定为仅含 `requirements` 与 `nfrs` 两个键的对象；数组按 Markdown 顺序；元素排除 `projection_sha256/status/markdown_section_id/schema` 等派生/envelope 字段。记录规范化字节长度 23717 和 SHA-256 `96be53fe…045e`；验证器必须同时比较字节长度与摘要。
