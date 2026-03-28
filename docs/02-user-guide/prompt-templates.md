# 历史项目标准提示词模板

**文档状态：** 已建立基线  
**主要读者：** 协作者 | 项目维护者 | 项目协调者  
**负责人：** 历史项目纳管负责人  
**关联 ID：** `REQ-006`, `REQ-007`  
**最后更新：** 2026-03-26

## 1. 用法说明

下面的模板都可以直接复制给 AI，再把方括号里的内容替换成你的项目事实。

建议原则：

- 不要先说“帮我修一下”，先说当前项目类型和当前目标
- 历史项目先纳管，再进入正式维护
- Bug 修复和新增需求分开表达
- `AGENTS.md` / `GEMINI.md` 只写稳定协作规则、读取顺序、边界和长期约束
- 安装结果、构建状态、测试结论、最新运行情况等易变事实，写入 `.factory/project.json`、`.factory/memory/current-state.md` 和 `docs/04-project-development/02-discovery/current-state-analysis.md`
- 能直接使用 `factory-dispatch historical-project-onboarding ...` 时，优先走自动化入口；提示词模板主要用于补充人类意图和约束

## 2. 模板 1：历史项目纳管启动

```text
这是一个已经开发完成、但不是用软件工厂完成的历史项目。
项目路径是：[项目路径]
项目名称是：[项目名称]
当前主要技术栈是：[技术栈]
当前已知运行方式是：[启动/构建/部署方式]
请先基于当前代码、配置、现有文档、最新发布结果和可用运行方式，梳理项目当前真实状态；
再补齐 AGENTS.md、GEMINI.md、docs/、.factory/ 和当前阶段基线。
其中请明确遵守：
1. `AGENTS.md` / `GEMINI.md` 只保留稳定协作规则、读取顺序、职责边界和长期约束
2. 当前安装、构建、测试、运行验证结论写入 `.factory/project.json`、`.factory/memory/current-state.md` 和 `docs/04-project-development/02-discovery/current-state-analysis.md`
3. 如果发现顶层入口文档里混入了瞬时状态，请迁移而不是继续复制
完成后，请告诉我：
1. 当前真实状态摘要
2. 建议的软件工厂当前阶段
3. 首批应创建的 BUG / CR / TASK
4. 下一步最合适的动作
```

## 3. 模板 2：历史项目纳管后开始修 Bug

```text
这个项目已经纳入软件工厂，请先读取 AGENTS.md、GEMINI.md、.factory/project.json、.factory/memory/current-state.md 和当前阶段正式文档。
现在要处理一个 Bug：
[Bug 描述]

请先判断影响范围，再创建或更新 BUG 工作项。
修复时同步更新：
- 代码
- 测试
- docs
- .factory/memory

最后告诉我：
1. 根因
2. 影响范围
3. 修复结果
4. 还需要补的验证
```

## 4. 模板 3：历史项目纳管后新增需求

```text
这个项目已经纳入软件工厂，请先读取当前正式状态。
现在有一个新增需求：
[需求描述]

请先按 CR 处理，不要直接开始编码。
先完成：
1. 影响分析
2. 需求与设计需要更新的地方
3. 首批工作项拆分
4. 再给出是否进入实现
```

## 5. 模板 4：先纳管，再立刻处理一个线上问题

```text
这是一个历史项目，还没有纳入软件工厂，但现在有一个高优先级线上问题：
[问题描述]

请分两段处理：
第一段，快速梳理当前真实状态并建立最小纳管基线；
第二段，在不跳过正式记录的前提下处理这个问题。

请优先告诉我：
1. 当前可确认的真实状态
2. 最小纳管动作
3. 是否需要先创建 BUG
4. 哪些信息还缺失
```

## 6. 模板 5：让 AI 只做纳管评估，不立刻改动

```text
这是一个历史项目，我还不想立刻让你改代码。
请先基于当前代码、配置、现有文档和发布状态，评估把它纳入软件工厂需要做哪些事。

输出请按下面结构给我：
1. 当前状态摘要
2. 缺失的治理资产
3. 建议补齐的 docs
4. 建议的软件工厂当前阶段
5. 纳管风险和注意事项
```

## 7. 模板 6：纳管完成后生成第一次会话入口

```text
这个历史项目已经完成纳管。
请先读取 AGENTS.md、GEMINI.md、.factory/project.json、.factory/memory/current-state.md、当前阶段 docs、活跃工作项和最近执行记录。
然后生成一次 agent session 和 state doctor，并告诉我：
1. 当前阶段
2. 阻塞项
3. 最推荐的下一步
4. 现在最应该优先处理的 BUG / CR / TASK
```

## 8. 模板 7：要求 AI 区分“纳管前事实”和“纳管后事实”

```text
在这个历史项目里，请你明确区分两类事实：
1. 纳管前：以当前代码、配置、现有文档和最新发布结果为准
2. 纳管后：
   - 协作入口：`AGENTS.md`、`GEMINI.md`
   - 事实来源：`.factory/project.json`、`.factory/memory/current-state.md`、正式 docs、活跃工作项和最近执行记录

如果你发现两类事实冲突，请先列出冲突，不要直接默认为旧文档是对的。
如果 `AGENTS.md` / `GEMINI.md` 与现状快照冲突，优先以后者为准，并修正入口文档。
```

## 9. 推荐搭配文档

- [历史项目纳管 checklist](../04-project-development/05-development-process/historical-project-onboarding-checklist.md)
- [历史项目现状基线模板](../04-project-development/02-discovery/current-state-analysis.md)
- [历史项目纳管自动化入口设计](../04-project-development/04-design/historical-project-onboarding-automation.md)

## 10. 变更记录

| 日期       | 变更内容                                 | 变更人 |
| ---------- | ---------------------------------------- | ------ |
| 2026-03-26 | 初始版本，补充历史项目纳管标准提示词模板 | Codex  |
| 2026-03-27 | 明确 `AGENTS.md` / `GEMINI.md` 与现状基线的分层边界，避免把瞬时状态写入顶层入口 | Codex |
