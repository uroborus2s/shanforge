---
title: shanforge
mkdocs:
  home_access: public
  nav:
    - title: 入门说明
      children:
        - title: 概览
          path: 01-getting-started/index.md
          access: public
        - title: 项目概览
          path: 01-getting-started/project-overview.md
          access: public
        - title: 快速开始
          path: 01-getting-started/quick-start.md
          access: public
        - title: 文档地图
          path: 01-getting-started/document-map.md
          access: public
    - title: 用户指南
      children:
        - title: 概览
          path: 02-user-guide/index.md
          access: public
        - title: 使用指南
          path: 02-user-guide/user-guide.md
          access: public
        - title: 提示词速查
          path: 02-user-guide/prompt-templates.md
          access: public
        - title: 命令速查
          path: 02-user-guide/command-cheatsheet.md
          access: public
    - title: 开发者指南
      children:
        - title: 概览
          path: 03-developer-guide/index.md
          access: public
        - title: 应用开发
          path: 03-developer-guide/application-development.md
          access: public
        - title: 开发环境
          path: 03-developer-guide/development-setup.md
          access: public
        - title: 函数说明
          path: 03-developer-guide/function-reference.md
          access: public
        - title: 接口说明
          path: 03-developer-guide/interface-reference.md
          access: public
        - title: 插件开发
          path: 03-developer-guide/plugin-development.md
          access: public
    - title: 项目开发文档（内）
      children:
        - title: 概览
          path: 04-project-development/index.md
          access: private
        - title: 项目治理
          children:
            - title: 概览
              path: 04-project-development/01-governance/index.md
              access: private
            - title: 项目章程
              path: 04-project-development/01-governance/project-charter.md
              access: private
        - title: 调研与决策
          children:
            - title: 概览
              path: 04-project-development/02-discovery/index.md
              access: private
            - title: 项目输入
              path: 04-project-development/02-discovery/input.md
              access: private
            - title: 头脑风暴记录
              path: 04-project-development/02-discovery/brainstorm-record.md
              access: private
            - title: 历史项目现状基线模板
              path: 04-project-development/02-discovery/current-state-analysis.md
              access: private
        - title: 需求
          children:
            - title: 概览
              path: 04-project-development/03-requirements/index.md
              access: private
            - title: 产品需求文档（PRD）
              path: 04-project-development/03-requirements/prd.md
              access: private
            - title: 需求分析文档
              path: 04-project-development/03-requirements/requirements-analysis.md
              access: private
            - title: 需求一致性校验报告
              path: 04-project-development/03-requirements/requirements-verification.md
              access: private
        - title: 设计文档
          children:
            - title: 概览
              path: 04-project-development/04-design/index.md
              access: private
            - title: 总体方案与协作总览
              path: 04-project-development/04-design/solution-overview.md
              access: private
            - title: 技术选型与工程规则
              path: 04-project-development/04-design/technical-selection.md
              access: private
            - title: 系统架构设计
              path: 04-project-development/04-design/system-architecture.md
              access: private
            - title: 模块边界文档
              path: 04-project-development/04-design/module-boundaries.md
              access: private
            - title: API 设计文档
              path: 04-project-development/04-design/api-design.md
              access: private
            - title: 后端设计文档
              path: 04-project-development/04-design/backend-design.md
              access: private
            - title: 数据库设计文档
              path: 04-project-development/04-design/database-design.md
              access: private
            - title: 部署与 CI/CD 设计
              path: 04-project-development/04-design/deployment-architecture.md
              access: private
            - title: UX/UI 设计文档
              path: 04-project-development/04-design/ux-ui-design.md
              access: private
            - title: 历史项目纳管自动化入口设计
              path: 04-project-development/04-design/historical-project-onboarding-automation.md
              access: private
            - title: 源文档标准升级分析
              path: 04-project-development/04-design/source-docs-standard-upgrade-analysis.md
              access: private
            - title: 动作注册与分级自治策略设计
              path: 04-project-development/04-design/action-registry-and-autonomy-policy.md
              access: private
            - title: 多前台适配与多代理协作设计
              path: 04-project-development/04-design/frontend-adapters-and-multi-agent-coordination.md
              access: private
            - title: Skill 进化机制设计
              path: 04-project-development/04-design/skill-evolution-mechanism.md
              access: private
        - title: 开发过程文档
          children:
            - title: 概览
              path: 04-project-development/05-development-process/index.md
              access: private
            - title: 历史项目纳管 Checklist
              path: 04-project-development/05-development-process/historical-project-onboarding-checklist.md
              access: private
            - title: 软件开发流程
              path: 04-project-development/05-development-process/software-development-process.md
              access: private
            - title: 实施计划
              path: 04-project-development/05-development-process/implementation-plan.md
              access: private
        - title: 测试与验证
          children:
            - title: 概览
              path: 04-project-development/06-testing-verification/index.md
              access: private
            - title: 测试计划
              path: 04-project-development/06-testing-verification/test-plan.md
              access: private
            - title: 测试报告
              path: 04-project-development/06-testing-verification/test-report.md
              access: private
        - title: 发布与交付
          children:
            - title: 概览
              path: 04-project-development/07-release-delivery/index.md
              access: private
            - title: 发布说明
              path: 04-project-development/07-release-delivery/release-notes.md
              access: private
        - title: 运维与维护
          children:
            - title: 概览
              path: 04-project-development/08-operations-maintenance/index.md
              access: private
            - title: 部署手册
              path: 04-project-development/08-operations-maintenance/deployment-guide.md
              access: private
            - title: 运维手册
              path: 04-project-development/08-operations-maintenance/operations-runbook.md
              access: private
        - title: 演进复盘
          children:
            - title: 概览
              path: 04-project-development/09-evolution/index.md
              access: private
            - title: Skill 进化方案
              path: 04-project-development/09-evolution/skill-evolution-plan.md
              access: private
            - title: Agent 高主动性与自进化集成方案
              path: 04-project-development/09-evolution/agent-motivation-autonomy-integration.md
              access: private
            - title: 纳管复盘与后续演进
              path: 04-project-development/09-evolution/retrospective.md
              access: private
        - title: 追踪矩阵
          children:
            - title: 概览
              path: 04-project-development/10-traceability/index.md
              access: private
            - title: 需求追踪矩阵
              path: 04-project-development/10-traceability/requirements-matrix.md
              access: private
            - title: 接口追踪矩阵
              path: 04-project-development/10-traceability/interface-matrix.md
              access: private
            - title: 文档索引
              path: 04-project-development/10-traceability/document-index.md
              access: private
---

# 山海工枢（shanforge）

这是 `山海工枢（shanforge）` 的正式项目文档源。当前仓库已经按 4 大模块完成单轴重构，其中 `项目开发文档（内）` 承载治理、需求、设计、测试、发布、运维和追踪矩阵等过程性文档；对外阅读入口和开发者稳定说明不再与内部过程文档混写。

## 适用范围

- 根 `docs/index.md` 的 front matter 是目录树、页面路径和访问级别的唯一事实源。
- Markdown 页面、OpenAPI 契约和 MCP tools 快照统一作为正式页面资产维护。
- 契约文件必须放在真实文档目录下，并与所在目录的 `index.md` 配套。

## 维护规则

- 只有根 `docs/index.md` 声明全站 `mkdocs.nav`、页面路径和页面权限。
- 子目录 `index.md` 只作为正文首页和资源权限锚点，不再承担导航声明职责。
- 页面、图片和附件跟随所属目录维护；资源文件放在当前目录或当前目录的 `assets/` 下，`assets/` 不承载 Markdown 页面或契约文件。
- 仓内链接统一使用相对路径，不写机器绝对路径。
- 新增、删除或移动 Markdown 页面或契约文件后，同步刷新根 `docs/index.md` 的目录树；子目录 `index.md` 只保留正文概览。
