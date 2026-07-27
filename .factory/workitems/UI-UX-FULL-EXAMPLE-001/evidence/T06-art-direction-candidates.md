# T06 移动端高保真方向样张证据

## 生成与检查

| 候选 | 预览输出 | 尺寸 | `view_image` 检查 |
|---|---|---:|---|
| A 温润生活方式 | `call_Hq1uEdkpDZzbxMjo1b1cXS4o.png` | 1536×1024 | 高保真成立；服务、价格、状态、主操作清晰；气质偏温暖居家和疗愈。 |
| B 现代城市服务 | `call_FaeTKteo7vQCia8Gm9WEhyqL.png` | 1672×941 | 层级最清楚、信息效率最高；适合城市综合服务；正式组件稿需重排生成图中的小字。 |
| C 东方疗愈轻奢 | `call_TTcKOlU5XgtENFT0XCEtqjo6.png` | 1536×1024 | 品牌辨识度和材质感最强；需防止产品被误解为理疗或 SPA 专门应用。 |

- 工具：内置 `imagegen`，分类 `ui-mockup`。
- 检查：三个输出均用 `view_image` 原始分辨率检查，并用 `file`、`sips` 验证 PNG 和像素尺寸。
- 候选图已在当前会话展示；它们不是仓内最终资源，也不作为可直接开发的组件稿。
- 可复现方向和共同约束见 `design-assets/mobile-hifi/art-direction-candidates.md`。

## Gate

- 状态：`needs_user_input`
- 需要：用户选择 A、B、C，或明确组合方式和需要重做的具体部分。
- 未执行：没有覆盖 Penpot，没有写入 `approved/`，没有生成 `manifest.json` 或最终资源包。
- 清理：仓内 `tmp/` 候选副本在本轮结束前删除。

## 完成前验证

- 时间：2026-07-24 16:07 +08:00
- 声明范围：只验证“三套候选已生成和人工检查、可复现定义已保存、未确认资产已清理、人工 Gate 已建立”。
- 结构检查：Node 读取 12 条 JSONL 事件并检查 T06 brief、A/B/C 方向、`tmp/`、`approved/`、`manifest.json`；exit code `0`，7 项均为 `true`。
- 格式检查：`git diff --check`；exit code `0`。
- 失败 `0`，错误 `0`，跳过 `0`。
- 未运行：Penpot 重画、最终资源验证、应用 UI 测试；这些动作位于人工选择之后，本轮不得运行。
- 完成层级：`task` 的候选方向阶段，结论 `partial`；停止原因 `human_gate`。
