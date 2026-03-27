# 历史项目纳管自动化入口设计

**文档状态：** MVP 已实现  
**主要读者：** 脚本维护者 | 架构师 | 项目维护者  
**负责人：** 仓库维护者  
**关联 ID：** `REQ-003`, `REQ-007`, `API-006`  
**最后更新：** 2026-03-26  

## 1. 设计目标

为“已经开发完成、但不是用软件工厂完成的历史项目”提供一个自动化入口，把纳管流程从主要依赖手工提示词，提升到“可重复、可检查、可逐步自动化”的标准入口。

当前仓库已经提供 MVP 实现：

- `scripts/factory-historical-project-onboarding`
- `scripts/factory-dispatch historical-project-onboarding`
- `scripts/factory-dispatch legacy-onboard`

## 2. 为什么需要新入口

现有命令并不能直接覆盖这个场景：

- `factory-init` 适合空目录或新项目初始化，不适合已有代码仓库
- `factory-requirements-upgrade` 更适合已有需求文档的结构升级，不等于完整纳管
- `factory-command-profiles` 依赖项目已经有 `.factory/project.json`
- `factory-agent-session` 和 `factory-state-doctor` 依赖项目已经有基本软件工厂状态

因此，历史项目纳管需要一个“先建立最小治理骨架，再接入现有高层入口”的新动作。

## 3. 目标与非目标

### 3.1 目标

- 非破坏性地把历史项目接入软件工厂
- 先建立当前真实状态基线，再建立软件工厂骨架
- 纳管完成后，能继续复用 `agent-session`、`state-doctor`、`dispatch`、`command-profiles`
- 把后续 Bug 修复和新增需求统一纳入 `BUG-*` / `CR-*`

### 3.2 非目标

- 不自动理解全部业务语义并生成完美 PRD
- 不自动修复所有历史技术债
- 不替代人工确认真实状态和维护目标
- 不要求第一次纳管就补齐全生命周期全部文档

## 4. 方案比较

### 方案 A：只靠标准提示词手工纳管

- 优点：现在就能用，不需要改脚本
- 缺点：可重复性差，质量依赖操作者经验

### 方案 B：在 `factory-command-profiles` 中新增 `historical-project-onboarding`

- 优点：用户入口统一，符合现有 profile 模型
- 缺点：profile 当前依赖项目已经存在 `.factory/project.json`，不适合作为第一入口

### 方案 C：新增专用入口 `factory-historical-project-onboarding`

- 优点：最贴合历史项目场景，可在“还没纳管”时工作
- 缺点：需要新增脚本，并在 `factory-dispatch` 中注册

### 当前落地方案

当前已按方案 C 落地，并提供：

- `factory-historical-project-onboarding`
- `factory-dispatch historical-project-onboarding`
- `factory-dispatch legacy-onboard`

纳管完成后，再引导用户继续使用 `factory-command-profiles` 或其他标准维护入口。

## 5. 推荐入口形态

### 5.1 当前命令

```text
factory-historical-project-onboarding --project <path> --owner <name> --goal "<maintenance goal>"
```

补充参数：

- `--name`：覆盖默认项目名
- `--stack`：覆盖自动识别的技术栈
- `--force`：允许覆盖软件工厂管理文件

### 5.2 当前 dispatch 别名

```text
factory-dispatch historical-project-onboarding --project <path> --owner <name> --goal "<maintenance goal>"
factory-dispatch legacy-onboard --project <path> --owner <name> --goal "<maintenance goal>"
```

## 6. 推荐执行流程

### 阶段 1：真实状态扫描

- 检测仓库是否已存在 `AGENTS.md`、`GEMINI.md`、`.factory/`
- 扫描主要语言、构建文件、运行入口、测试入口
- 读取已有 README、设计文档、接口说明、发布说明
- 记录最新发布和当前运行方式

输出：

- `docs/01-discovery/current-state-analysis.md`
- 自动识别的技术与命令线索
- 纳管报告中的事实来源列表

### 阶段 2：非破坏性骨架补齐

- 创建缺失的 `AGENTS.md`
- 创建缺失的 `GEMINI.md`
- 创建缺失的 `docs/`
- 创建缺失的 `.factory/`
- 初始化 `.factory/project.json`

约束：

- `AGENTS.md` / `GEMINI.md` 只承担协作协议层职责：
  - 读取顺序
  - 稳定规则
  - 角色边界
  - 长期约束
- 当前安装状态、构建结果、测试结果、最新运行结论等瞬时事实必须写入：
  - `.factory/project.json`
  - `.factory/memory/current-state.md`
  - `docs/01-discovery/current-state-analysis.md`
- 不要把一次扫描得到的临时结论直接固化到 `AGENTS.md` / `GEMINI.md`

默认建议：

- 项目阶段先设为 `MAINTENANCE`
- 如果当前主要目标是重构或大改造，可在纳管报告中提示回到 `ANALYSIS` / `REQUIREMENTS`

### 阶段 3：正式文档基线生成

- 基于现状生成需求现状文档
- 生成技术选型、架构、模块边界、接口设计基线
- 标出“当前事实”和“后续改造项”

### 阶段 4：维护入口初始化

- 生成一次 `factory-agent-session`
- 生成一次 `factory-state-doctor`
- 输出纳管报告和下一步建议

## 7. 建议产物

执行完成后，当前 MVP 至少应得到：

- `AGENTS.md`
- `GEMINI.md`
- `docs/01-discovery/current-state-analysis.md`
- `.factory/project.json`
- `.factory/memory/current-state.md`
- `.factory/memory/agent-session.md`
- `.factory/process/state-doctor-report.md`
- `.factory/process/historical-project-onboarding-report.md`
- `.factory/memory/graph/traceability.json`

## 8. 安全与幂等要求

- 不覆盖已有正式文档，除非用户确认
- 对已存在的 `docs/` 和 `.factory/` 采取补齐而不是重建
- 若检测到项目已经纳管，应退出到“诊断/修复现有状态”而不是再次初始化
- 自动化入口应输出“事实来源列表”，便于人工复核
- 自动化入口应检查 `AGENTS.md` / `GEMINI.md` 是否被瞬时状态污染；若发现污染，应提示迁移到现状快照层

## 9. 与现有脚本的衔接建议

建议复用现有能力：

- `factory-project-rules-refresh`
- `factory-requirements-upgrade`
- `factory-agent-session`
- `factory-state-doctor`
- `factory-dispatch`

但不建议直接复用为第一步：

- `factory-init`
- `factory-command-profiles`

因为它们都更适合已经具备软件工厂骨架的项目。

## 10. MVP 范围

当前版本已经实现这些：

- 识别是否为未纳管历史项目
- 扫描当前真实状态
- 补齐最小治理骨架
- 生成现状基线与纳管报告
- 生成一次 `agent-session` 和 `state-doctor`

当前仍未做：

- 深度代码语义理解
- 自动需求拆分到非常细的任务
- 自动创建首批 `BUG-*` / `CR-*` / `TASK-*`
- 自动生成完整测试资产
- 自动推送远端 PR 或自动部署

## 11. 对用户的呈现建议

在用户指南中应明确：

- 这是“历史项目纳管”入口，不是“新项目初始化”入口
- 它的第一目标是建立当前状态基线，而不是立刻改代码
- 纳管完成后，后续维护统一回到标准软件工厂流程

## 12. 变更记录

| 日期 | 变更内容 | 变更人 |
|---|---|---|
| 2026-03-26 | 初始版本，提出历史项目纳管自动化入口设计 | Codex |
| 2026-03-26 | 将文档状态更新为 MVP 已实现，并登记真实命令入口与实现范围 | Codex |
