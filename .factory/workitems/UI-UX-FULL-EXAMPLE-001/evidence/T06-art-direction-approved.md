# T06 移动端高保真方向确认

## 用户确认

- 时间：2026-07-24
- 原文：选择以 B 为基础，吸收 A 的温暖摄影风格和 C 的少量材质感。
- 结果：美术方向 Gate 通过；进入资源清单确认 Gate。

## 落地结果

- `ui-ux-pro-max` 增加移动端高保真触发、按需 reference 和禁止把整张 AI 位图当最终 UI 的边界。
- 已确认方向写入 `design-assets/mobile-hifi/art-direction.md`。
- 三张确认来源写入 `approved/`：B 作为主参考，A/C 分别作为摄影和材质参考。
- 资源清单写入 `design-assets/mobile-hifi/sprite-spec.md`，当前状态为待用户确认。
- 未生成最终九张资源、`manifest.json` 或 Penpot 高保真画板。

## 来源完整性

| 来源 | SHA-256 |
|---|---|
| `approved/b-primary-ui-direction.png` | `4384b8ceebf47f919e6955e94b378ece638347da670930a6321ca359c4fc68c6` |
| `approved/a-warm-photography-reference.png` | `d118f83ce67ee9f651fcfb04f4b162b58566c1a959c1dba43864cb11f680916f` |
| `approved/c-material-reference.png` | `1f477e942d806723c3dd381bb43a4dc73181a49f0d8c7acddaabef41f036d44c` |

复制后的哈希与内置 `imagegen` 原始输出一致；主参考已使用 `view_image` 原始分辨率检查。

## 验证

- `uv run python .../quick_validate.py skills/ui-ux-pro-max`：`Skill is valid!`，exit code `0`。
- `uv run pytest tests/test_ui_ux_pro_max_skill.py -q`：`10 passed`，exit code `0`。
- `ui-ux-pro-max` 专业前缀哈希与冻结测试值一致。
- 资产检查：三个 `approved` 来源存在且被 `art-direction.md` 引用；资源清单存在；`tmp/`、`manifest.json` 不存在；5 项全部通过。
- `git diff --check`：exit code `0`。
- 组合所有权测试：`13 passed, 2 failed`；失败来自本任务外已修改的 `api-design` 哈希和 `writing-plans` 状态契约，未改动这些用户/其他任务文件。

## 状态

- status：`needs_user_input`
- completion_level：`task` 的美术方向阶段
- stop_reason：`human_gate`
- next：确认 `sprite-spec.md` 的九项资源清单后，才生产最终资源并升级 Penpot。
