# 通用 CLI 模型 对话启动入口

- 生成时间：2026-04-12 01:27:51
- 项目名称：shanforge
- 当前阶段：MAINTENANCE
- 角色：项目协调者
- 焦点：验证最终写入 Git 原文约束
- 优先规则文件：AGENTS.md 与 GEMINI.md

## 角色说明

- 描述：负责阶段推进、跨角色协作、审批门禁和交接节奏控制。
- 推荐工具：codex / gemini

## 必须先读

- `.factory/project.json`
- `AGENTS.md`
- `GEMINI.md`
- `.factory/memory/runtime-brief.md`
- `.factory/memory/role-charter.project.md`
- `.factory/memory/doc-map.md`
- `.factory/memory/project-index.md`
- `.factory/memory/current-state.md`

## 当前相关工作项

- 当前没有直接分配给该角色的活跃工作项。

## 共享核心能力

- `brainstorming`：在实施前探索产品意图、约束条件、备选方案，并完成设计确认。 (skills/brainstorming/SKILL.md)
- `document-templates`：初始化并维护标准的 docs/ 和 .factory/ 文档结构。 (skills/document-templates/SKILL.md)
- `doc-coauthoring`：通过迭代方式共同创作设计文档、提案和决策文档。 (skills/doc-coauthoring/SKILL.md)

## 当前技术画像强制技能

- 当前技术画像未额外要求专用 skills。

## 操作约束

- 人类文档与 `.factory/memory/` 记忆必须同步更新。
- 每个变更都要同步代码、文档、测试和追踪关系。
- 继续沿用单文件版本演化方式维护正式文档。
- 当前 V1 只支持本地 CLI 协作，不通过项目 API 平台执行。
- 当用户直接输入 `/技能名` 时，将其解释为立即调用该 skill 的默认工作流，而不是展示 skill 定义。
- slash 触发的 skill 禁止只回复“已收到 skill”之类的占位文本，必须直接进入首个可执行步骤。

## Slash 技能直调约定

- 通用展开：`/技能名` = 立即执行该 skill 的默认工作流。
- `gitcommitzh` 展开：先执行 Git 变更审查，输出结构化中文说明和中文提交信息草案；若同条消息明确包含“提交 / commit”，先展示“最终写入 Git 的提交信息原文”，再按这段原文执行本地提交。

## 推荐直接执行的命令

- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch session --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证最终写入 Git 原文约束'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch workbench --project /Users/uroborus/AiProject/shanforge --role coordinator --owner Codex --focus '验证最终写入 Git 原文约束'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch assign --project /Users/uroborus/AiProject/shanforge --role requirements-analyst --owner Codex`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch board --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证最终写入 Git 原文约束'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch pr-board --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证最终写入 Git 原文约束'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch pr-remote-sync --project /Users/uroborus/AiProject/shanforge --owner Codex`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch pr-check --project /Users/uroborus/AiProject/shanforge --owner Codex --mode review-ready`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch doctor --project /Users/uroborus/AiProject/shanforge --owner Codex --scope full`

## 可直接在对话里说

- 读取 AGENTS.md、GEMINI.md、.factory/project.json 和 .factory/memory/agent-session.md，以项目协调者身份验证最终写入 Git 原文约束。
- 当用户直接输入 /技能名 时，将其视为立即调用该 skill 的默认工作流，而不是展示技能定义；先确认当前阶段、角色职责和推荐动作，再开始执行。
- 如果用户直接输入 `/技能名`，不要复述 skill 定义，直接执行该 skill 的默认工作流。
- 如果用户直接输入 `/gitcommitzh`，立即检查当前 Git 工作区与暂存区变化，输出结构化中文变更说明和中文提交信息草案；只有同条消息明确包含“提交”或“commit”时才继续执行本地提交。真正提交前，先显式列出“最终写入 Git 的提交信息原文”，提交时逐字复用这段原文。
