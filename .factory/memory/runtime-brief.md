# 项目压缩运行卡

- 生成时间：2026-09-08
- 项目：`shanforge`
- 当前模式：`codex_desktop`
- 产品边界：`skill-first` 工程协作资产
- 技术栈：Markdown Skills / Python 3 / uv / pytest / Git
- 当前工作项：`MODEL-DYNAMIC-DISPATCH-001`
- 阻塞项：0

## 最小读取顺序

1. `.factory/memory/agent-session.md`
2. 上下文不足再读本文件、current-state.md、doc-map.md和当前工作项ledger
3. 仅按doc-map对相关正式文档单文件回源

## 当前事实

- Shanforge不提供仓内src平台runtime；确定性辅助能力属于所属skill/scripts。
- using-shanforge拥有流程判断和唯一子模型决策表；工作skill仅执行和回写。
- 主会话模型由用户选择；子任务显式指定model、reasoning_effort、fork_turns=none，不继承父配置。
- 本任务v5终审及完整420项测试、11项子测试通过，进入提交；task-reader宿主新会话加载未实测，未暴露时不能使用。
- 历史证据、review、ledger保持不可变；当前候选和本批证据分别保存。

## 唯一下一动作

- `create_exact_local_commit`

## 禁止动作

- 不恢复旧中心命令、factory-*、全局流程脚本或模型网关。
- 不执行未经授权的远端、部署或生产动作。
