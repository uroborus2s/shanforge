# 设计文档

本目录负责把需求落成可实现、可测试、可交付的设计约束。

## 1. 阅读建议

先看总览、技术选型和系统架构，再进入模块、接口、后端、数据、部署和体验设计。

## 2. 推荐阅读顺序

1. [总体方案与协作总览](./solution-overview.md)
2. [技术选型与工程规则](./technical-selection.md)
3. [系统架构设计](./system-architecture.md)
4. [动作注册与分级自治策略设计](./action-registry-and-autonomy-policy.md)
5. [多前台适配与多代理协作设计](./frontend-adapters-and-multi-agent-coordination.md)
6. [Skill 进化机制设计](./skill-evolution-mechanism.md)
7. [模块边界文档](./module-boundaries.md)
8. [API 设计文档](./api-design.md)
9. [后端设计文档](./backend-design.md)
10. [数据库设计文档](./database-design.md)
11. [部署与 CI/CD 设计](./deployment-architecture.md)
12. [UX/UI 设计文档](./ux-ui-design.md)
13. [历史项目纳管自动化入口设计](./historical-project-onboarding-automation.md)

## 3. 使用规则

- 对外稳定接口说明同步到开发者指南
- 机器契约文件以仓内正式契约为准
- 设计变更后必须同步测试计划、发布说明和追踪矩阵
