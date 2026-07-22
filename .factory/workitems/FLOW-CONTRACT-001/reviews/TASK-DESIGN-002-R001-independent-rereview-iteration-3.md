# TASK-DESIGN-002 R001 独立复审（iteration 3）

- Reviewer：`/root/design_plan_review`
- Reviewer 类型：独立子任务，未参与设计或实现
- 决定：`changes_requested`
- 评分：88 / 100
- Critical / Important / Minor：0 / 3 / 1
- 人工确认：不需要，均为已批准范围内机械性整改

## 独立性和验证

Reviewer 只读重新查阅文件化输入，运行 structure-check、SHA-256、`git diff --check` 与文本交叉检查，写集为空。

- structure-check exit code 0。
- 16 REQ、64 AC、11 NFR、29+10 表、2 FTS、137 唯一字段、13 row models、50 transitions 保持一致。
- Design、Plan 与 check-script Hash 与当时作者 evidence 一致。
- `git diff --check` exit code 0。

## Iteration 2 closure

`source_section_key` FK、PM 四态设计、正式 `project sync enqueue` CLI、独立 queue、axe 措辞、可执行 structure-check 和 prepare/activate 主顺序已建立。

## Important findings

1. 39 表字段表仍写 `section_key=<document_id>:<section_id>`，与 locator 章节的 JCS Hash 合同冲突。必须统一为 `"mdsec:" + sha256(JCS([document_id, section_id]))`，structure-check 应显式拒绝旧公式。
2. 四态测试门未同步到实施计划和 T04 brief。必须对 `known|unknown|not_registered|not_applicable` 逐项断言。
3. T05 prepare 仍允许写最终 Catalog 和 evidence manifest 目标，与 T06 activate 冲突。T05 只能写隔离 migration package/after-image，最终目标只能在 T06 验证后激活。

## Minor finding

- T05 brief 上游仍称“现有 durable system task foundation”，需改为 R009 独立 queue，不依赖冻结候选。

## 结论

核心方案已基本可实施，但上述 3 个 Important 直接影响无碰撞定位、四态硬门和 prepare/activate 边界，当前不批准。修正后交同一 reviewer 复审。
