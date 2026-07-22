# TASK-REQ-006 R005 评审整改响应（R006）

## Fixed

### `R005-C-001`

R006 将发布分为 `local-owner` 与 `shared-restricted`：前者生成 0700/0600 的本地静态站点并明确已打开/复制件不可撤回；后者离线只含公开/脱敏字段，受限详情必须由 `--serve` 每次重新鉴权，撤权后托管 cache 清除且读取 fail-closed。

### `R005-I-001`

R014 被准确标注为 `candidate_unapproved`，并绑定 contract ID、revision、whole-file SHA-256 `836fadc2…8d33` 和 field catalog SHA-256 `658f8d80…4313`。R006 不替代 R014 独立批准。

### `R005-I-002`

新增 `REQ-CHANGE-PROJECT-KNOWLEDGE-001.pm-field-map.R006.json`，对 137 个 field ID 逐项登记目标表/DTO、列/JSON Pointer、行模型、主/外键、基数、reducer 与历史策略。`ProjectProgressSnapshot/v1` 明确为非持久化 DTO，Manifest Owner 为 `pk_render_view`。

### `R005-I-003`

页面只显示由事实高水位决定的固定 `as_of`；墙钟 `built_at` 只进入 receipt/Manifest 非内容区，不进入页面正文、页面 Hash 或 `RenderFingerprint`。

### `R005-I-004`

代码实体身份改为独立 `symbol_id`，qualified name/signature 只是当前 locator。模块/文件移动、重命名、签名调整需要显式 alias/迁移；拆分、合并和歧义只生成待确认诊断。

### `R005-I-005`

R006 JSON 将 16 个 REQ、64 个稳定 AC ID、11 个 NFR 指标与验证方法全部对象化，并要求最终 Manifest 绑定 Markdown、机器合同、field map、R014 pin 和 review。

### `R005-I-006`

异步合同增加 22 条 transition、guard、3 个终态、5 次重试、300 秒退避上限和单调 fencing token。维护提交是可选分支；无授权时 `html_published -> commit_not_authorized -> integrated -> done` 正常收敛。

## 验证

- Markdown/机器合同：16 REQ、每项 4 AC、总 64 AC、11 NFR 一致。
- Schema：29 core + 10 PM = 39；所有 PM 表至少有一个字段 Owner。
- Field map：137 条映射、137 个唯一 field ID，R014 与 field map pin 均匹配实际 SHA-256。
- 状态机：22 条转移，所有非终态至少一条出边。
- JSON：R006 contract、PM field map 和 R014 均通过 `jq -e`。

## 下一 Gate

七项 Finding 均已在原范围内整改，进入同一独立 Reviewer 复审。尚未人工批准，不得进入正式设计或实现。
