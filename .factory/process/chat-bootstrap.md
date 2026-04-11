# 对话启动记录

## 最新启动入口

- 时间：2026-04-12 01:55:05
- 工具：OpenCode
- 角色：项目协调者
- 负责人：Codex
- 焦点：验证暂存区为空自动 git add
- 输出文件：`.factory/memory/chat-bootstrap.opencode.coordinator.md`
- 建议先读：`AGENTS.md 与 GEMINI.md`

## 推荐入口命令

- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch session --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证暂存区为空自动 git add'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch workbench --project /Users/uroborus/AiProject/shanforge --role coordinator --owner Codex --focus '验证暂存区为空自动 git add'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch assign --project /Users/uroborus/AiProject/shanforge --role requirements-analyst --owner Codex`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch board --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证暂存区为空自动 git add'`
- `python3 /Users/uroborus/AiProject/shanforge/scripts/factory-dispatch pr-board --project /Users/uroborus/AiProject/shanforge --owner Codex --focus '验证暂存区为空自动 git add'`

## 建议对话提示

- 读取 AGENTS.md、GEMINI.md、.factory/project.json 和 .factory/memory/agent-session.md，以项目协调者身份验证暂存区为空自动 git add。
- 当用户直接输入 /技能名 时，将其视为立即调用该 skill 的默认工作流，而不是展示技能定义；先确认当前阶段、宿主能力边界和推荐动作，再开始执行。若用户明确写出“提交 / commit / 执行提交”，则视为已授权执行本地提交，不要无故停在摘要阶段。
- 如果用户直接输入 `/技能名`，不要复述 skill 定义，直接执行该 skill 的默认工作流。
- 如果用户直接输入 `/gitcommitzh`，立即检查当前 Git 工作区与暂存区变化，输出结构化中文变更说明和中文提交信息草案；只有同条消息明确包含“提交”或“commit”时才继续执行本地提交。真正提交前，先显式列出“最终写入 Git 的提交信息原文”，提交时逐字复用这段原文；若用户已明确要求提交、暂存区为空、且未指定文件子集，则默认自动执行 `git add .` 纳入当前工作区改动，而不是中止。

## 历史启动记录

- 2026-04-12 01:55:05: 为 `OpenCode` 生成 `项目协调者` 对话入口，负责人：Codex。
- 2026-04-12 01:39:52: 为 `OpenCode` 生成 `项目协调者` 对话入口，负责人：Codex。
- 2026-04-12 01:27:51: 为 `通用 CLI 模型` 生成 `项目协调者` 对话入口，负责人：Codex。
- 2026-04-12 01:17:00: 为 `通用 CLI 模型` 生成 `项目协调者` 对话入口，负责人：Codex。
- 2026-04-07 22:46:47: 为 `通用 CLI 模型` 生成 `项目协调者` 对话入口，负责人：Codex。
