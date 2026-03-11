# GCC AI Agent Hackathon Submission

## 项目名称
GCC Impact Copilot

## 参赛赛道
影响力评估（Impact Evaluation）

## 项目简介（TL;DR）
我们构建了一个面向 GCC 资助组合的 Impact Monitoring Agent，用公开可验证的项目活动信号替代滞后的季度人工追踪。它会自动抓取 GitHub 活跃度、发版节奏、官网可用性和项目里程碑配置，生成可审计的项目健康报告，并把项目分为 healthy / watch / at-risk 三类，帮助 reviewer 优先处理真正需要跟进的项目。这个工具不替代人工判断，而是把重复、低效、容易遗漏的“追进展”工作自动化，让 GCC 可以更早发现风险、也更快发现值得支持的正向信号。

## 要解决的真实问题
GCC 这类公共物品资助体系在 impact evaluation 上会天然遇到几个问题：第一，项目更新通常分散在 GitHub、官网、社媒、文档、链上活动等不同渠道，很难持续追踪；第二，很多项目只在季度节点提交一次汇报，导致 reviewer 很难及时发现停滞、偏离目标或值得加大支持的项目；第三，人工逐个检查 portfolio 的信息非常费时，而且不同 reviewer 的关注点不一致，难以形成稳定、可复用的流程。结果就是 impact evaluation 往往滞后、主观、缺少统一证据链。GCC Impact Copilot 要解决的，就是把这些公开信号变成结构化、可复查、可持续运行的监控层，让影响力评估从“季度追着问”变成“持续可观测”。

## 方案与技术实现
当前原型采用一个可扩展的 agent workflow：首先读取 portfolio manifest（项目名称、GitHub repo、官网、预期里程碑等）；然后通过 GitHub API 拉取公开信号，包括最近 push 时间、release 发布时间、open issues 数量、stars 等；同时检查官网可访问性，并把声明的 milestones 纳入上下文；最后使用一套显式的评分规则生成 JSON 报告和 Markdown 报告，并输出 healthy / watch / at-risk 状态和 follow-up risk 列表。现阶段它是一个可直接运行的 CLI 原型，适合作为 GCC 内部 agent 的“观测引擎”。下一步会扩展到 RSS / blog / X / 链上地址 / milestone evidence adapter，并接入自动周报、reviewer override 和 evidence links。技术上刻意保持可审计：每个分数都能追溯到具体的公开信号，避免黑箱判断。

## 代码仓库链接
https://github.com/Sipeng2024/gcc-impact-copilot

## Demo 视频链接
https://github.com/Sipeng2024/gcc-impact-copilot/blob/main/DEMO_WALKTHROUGH.md

## 公共物品属性
这个项目天然适合开放和复用。它不依赖 GCC 私有数据，核心设计就是围绕公开信号做 impact monitoring，因此任何 grant DAO、基金会、公共物品社区、黑客松资助计划都可以复用相同的工作流。项目将以 MIT License 开源，评分逻辑、数据源适配器、报告模板都可扩展；社区可以根据不同项目类型定义自己的 rubric，而不是绑定单一组织。换句话说，这不是只给 GCC 的内部小工具，而是一类 grant portfolio observability 工具的开源起点。

## 风险与依赖
当前原型主要依赖公开数据源，因此第一类风险是公开信号并不总能完整反映真实进展，例如研究型项目或线下社区型项目，GitHub activity 不能代表全部影响；对应策略是把它明确定位为“优先级排序和风险提示层”，不替代人工 review。第二类风险是不同项目的 impact 维度差异很大，单一评分模型可能失真；对应策略是下一步引入项目类型化 rubric 和人工 override。第三类风险是 GitHub API、网站可用性等外部依赖会带来噪声；对应策略是保留原始 evidence 和抓取状态，并为关键决策保留人工复核。第四类风险是当前 demo 仍偏 CLI / backend prototype；下一阶段会补齐 reviewer-facing digest 和 dashboard。

## 联系邮箱
99victorxie99@altiuslabs.xyz

## 收款地址
0x000000000000000000000000000000000000dEaD
