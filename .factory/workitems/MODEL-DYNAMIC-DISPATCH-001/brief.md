# GPT-6 动态子任务派发

- 授权：2026-09-08 用户明确要求重建合同，主会话按任务选择子模型及推理强度，不继承主会话配置。
- 依赖：MODEL-ORCHESTRATOR-SELECTION-001 已提交 1b64734 / 242af89，共享文件与 memory 交接完成。
- 当前范围：Shanforge 本地合同、模板、用户指南、模型角色和相关测试；本地中文提交，不推送，不安装全局技能。
- 架构：skill-first；复用宿主 spawn_agent，不新增调度 runtime、依赖或全局配置。

## 验收

1. 主会话模型保持用户选择。每次子任务按复杂度、风险、不确定性和职责独立选择模型与强度；记录理由与能力来源。
2. 默认选择满足任务的最低档：局部清楚且低风险 Luna/low，日常实现 Terra/medium，需要设计判断或跨模块 Astra/high，深度排查或高风险 Astra/xhigh；单个困难问题有证据才 Astra/max。普通独立 review 至少 Terra/high，深度或高风险 review 选 Astra/xhigh。
3. 显式传入 model、reasoning_effort、fork_turns=none；role 固定设置与选择不符即拒绝，不通过省略参数实现动态选择。模型相同也必须是本任务独立选择。
4. API effort 与 Codex/Work Ultra 区分；以当前工具暴露能力检查可调用组合，不把官网支持当成本会话已可用。Ultra 是编排模式，不作为普通子任务默认 effort。
5. worker、只读分析子任务、独立 reviewer 分工清楚；不让分析子任务取得项目写权限。实现者不自批 review。
6. 阶段或风险变化由父会话重评。两轮失败先补复现/证据、收窄任务，再考虑升档；变更模型或强度须新 dispatch_id 和新 spawn，保留旧回执；不虚构 followup_task 可改配置。
7. 不可用或回执不完整时失败关闭。父会话可在同一授权范围内重新选择受支持组合并创建新路由，不能静默降级、越过风险/质量下限或代写。
8. 更新当前合同、必要正式事实和测试；保留历史回执。验证需覆盖不同任务路由、缺参/继承/不兼容组合拒绝、失败与重派，并进行独立前向试用和评审。

## 能力核对

2026-09-08 已读取 OpenAI 官方文档：
- https://developers.openai.com/api/docs/models/gpt-6-astra ：API low/medium/high/xhigh/max。
- https://developers.openai.com/api/docs/guides/latest-model ：明确派发时机；测试范围与变更匹配。
- https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning ：模型/effort 省略时继承；客户端 Ultra 需模型/账号支持。

当前 collaboration.spawn_agent 显式暴露 Astra、Sol、Terra、Luna 及对应 effort；fork_turns=all 不接受 overrides。当前预设 terra-reviewer 固定 Terra/high/read-only；新 role 文件是否被宿主重新加载必须分开验证，不能宣称热更新成功。
