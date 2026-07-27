# T06 资源包检查点验证

- 时间：2026-07-27
- 交付层级：`T06_asset_pack_checkpoint`
- 结果：`passed`
- WorkItem 完成：`false`

## 新鲜验证

- 在 `/tmp/shanforge-t06-verify.*` 临时副本运行
  `tools/build_assets.sh`：`asset_build=passed files=9`。
- 按 `manifest.json` 逐项回算：9/9 文件存在，9/9 SHA-256 匹配，
  `tmp/` 引用为 0，资源包内不存在 `tmp/`。
- `pytest -q tests/test_ui_ux_pro_max_skill.py`：`10 passed in 0.21s`。
- Ruff：`All checks passed!`。
- Skill validator：`Skill is valid!`。
- WorkItem ledger：20 行 JSONL 可解析；E019 为独立复审
  `approved / 100 / C0-I0-M0`，E020 保持 Penpot 外部连接 Gate。
- 限定 `git diff --check`：通过。

## 视觉检查

- 用 `view_image` 复看首页主视觉和移动端整包预览截图。
- 9 项资源在移动预览中分组、文件名、尺寸和用途可读；未见文字水印、
  品牌标记或明显裁切破损。
- 当前已打开的 `file://` 预览未由浏览器控制重新读取：浏览器安全策略拒绝
  本地文件 URL，未绕过该限制；既有 E016/E019 浏览器证据保持有效。

## 边界

- 本检查点只固化已批准资源包与当前完整样例候选。
- 未同步 Penpot，未完成管理后台元数据同步，未进行完整 WorkItem 终审。
- 下一动作仍是用户在目标 Penpot 文件中打开 MCP 插件并点击 Connect。

## 暂存区快照

- 快照内 9 个不依赖 `.git` 的 UI/UX 定向测试通过，1 个调用
  `git ls-files` 的测试因导出目录不是 Git 仓库而改用原仓索引等价检查。
- 索引 `git ls-files skills/ui-ux-pro-max`：126 个文件；三个禁止生成物均不存在。
- `ui-ux-pro-max` 专业前缀 SHA-256 与暂存哈希注册表一致：
  `c1251201eed9cd7e6ce251c788722c257f4cbaf735b76173c719f01b2fdc82ef`。
- 隔离套件另发现 HEAD 已存在的 `document-templates` 哈希不一致；已证明该失败
  在本提交前存在，相关 hunk 未进入本检查点。
