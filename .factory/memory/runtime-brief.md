# 项目压缩运行卡

- 生成时间：2026-08-23 10:16 +0800
- 项目：`shanforge`
- 当前模式：`codex_desktop`
- 产品边界：`skill-first` 软件工厂资产
- 技术栈：Markdown Skills / Python 3 / uv / pytest / Git
- 活跃工作项：`MODEL-ROUTING-001`
- 阻塞项：0

## 最小读取顺序

1. `.factory/memory/runtime-brief.md`
2. `.factory/memory/role-charter.project.md`
3. `.factory/memory/doc-map.md`
4. `.factory/memory/current-state.md`
5. 当前 work item 的 brief、plan、task brief 和 ledger
6. 仅在摘要不足时按 `doc-map.md` 单文件回源正式文档

## 当前事实

- Shanforge 不提供 `src/` 平台运行时；确定性辅助能力放在所属 skill 的 `scripts/`。
- `using-shanforge` 是唯一流程控制面，专项 skill 只执行本职工作并回写状态。
- 当前先闭合事实源、工作区和干净克隆测试，再增加 Sol/Terra/Luna 路由合同。
- 历史草稿、候选、原始证据和截图不进入 Git；当前最小审计资产和测试夹具保留。

## 唯一下一动作

- 完成 `MODEL-ROUTING-001-T01` 验证；通过后执行 T02 模型路由。

## 禁止动作

- 不恢复旧中心命令、动作注册表、`factory-*` 或全局流程脚本。
- 不新增模型网关、服务、数据库或仓内平台运行时。
- 不执行未经授权的远端、部署或生产动作。
