# TASK-REQ-006 R002 Feedback Triage for R003

## `R002-I-001`

- 来源：独立需求评审。
- Severity：Important。
- 技术要求：把稳定 view scope 与易变 input fingerprint 分开，机器合同按稳定 scope 强制唯一文件槽。
- 是否清楚：yes。
- 技术核实：正确。R002 JSON 的 `latest_files_per_cache_key=1` 可被实现为每个易变快照一个文件，不能证明用户要求。
- 与用户决策冲突：no。
- 处理：Fixed in R003。

## `R002-M-001`

- 来源：独立需求评审。
- Severity：Minor。
- 技术要求：Markdown 与机器合同都无条件禁止跨 `authorization_digest` 复用。
- 是否清楚：yes。
- 技术核实：正确。按“是否敏感”增加分支会把权限判断重新交给实现临场解释。
- 与用户决策冲突：no。
- 处理：Fixed in R003。
