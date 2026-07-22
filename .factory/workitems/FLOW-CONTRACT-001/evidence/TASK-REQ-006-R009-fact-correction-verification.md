# TASK-REQ-006 R009 事实修正验证

## Hash

- R009 Markdown：`eacd27cf9beeee857d868d7856cb2a0cd275614fdb734b1c73d519039493ab7a`
- R009 contract：`53923f55c2bcc16bce6ad60ed1045c671dd490b6733885725641fe39e6859977`
- R009 field map：`17af8c254017bc60eb44e73b8e61322bc57eb577ffa6baa2711f100d48251055`
- R014 release manifest：`ea84805f62b9c20d17f625e0e4f68efcd510c19897cc1b5c8ebacf70a5bdef4e`

## 结果

```text
requirements=16
acceptance_criteria=64
nfrs=11
root_canonical_bytes=23720
root_sha256=d917dce3287bf004233f436fcb407fc7314a20845ac598dcb58711c1041dd5de
r014_embedded_internal_status=candidate_unapproved
r014_current_release_status=released
release_manifest_pin=true
fields=137
transitions=50
snapshot=ProjectProgressSnapshot/v2
```

R009 两个 JSON 与 release manifest 均通过 `jq -e`；Markdown/JSON 逐字段与 root 对账、R014 approved input Hash、field map pin、137 fields 和 50 transitions 断言通过。
