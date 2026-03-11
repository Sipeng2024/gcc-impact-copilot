# GCC AI Agent Hackathon Submission

## 项目名称
GCC Impact Copilot

## 参赛赛道
影响力评估（Impact Evaluation）

## 项目简介（TL;DR）
我们构建了一个面向 GCC reviewer 的 Impact Review Copilot，把分散的公开进展信号整理成结构化、可审计的 follow-up 输入。它会读取项目的 GitHub 活跃度、发版节奏、官网可用性和里程碑上下文，输出健康状态、风险提示和待人工跟进事项，帮助 grant manager 更快判断“该看什么、该问什么、下一步跟谁跟进”。这个工具不是 crawler，也不是自动裁决器；它的定位是 reviewer workbench，用来辅助 impact evaluation，而不是替代人工判断。

## 要解决的真实问题
GCC 这类公共物品资助体系在 impact evaluation 上会天然遇到几个问题：第一，项目更新通常分散在 GitHub、官网、社媒、文档、链上活动等不同渠道，很难持续追踪；第二，很多项目只在季度节点提交一次汇报，导致 reviewer 很难及时发现停滞、偏离目标或值得加大支持的项目；第三，人工逐个检查 portfolio 的信息非常费时，而且不同 reviewer 的关注点不一致，难以形成稳定、可复用的流程。结果就是 impact evaluation 往往滞后、主观、缺少统一证据链。GCC Impact Copilot 要解决的，就是把分散证据变成 reviewer 可直接消费的审查输入，让影响力评估从“季度追着问”变成“持续有线索可查、有人可跟进”。

## 方案与技术实现
当前原型采用 reviewer-facing workflow：首先读取 portfolio manifest（项目名称、GitHub repo、官网、预期里程碑等）；然后拉取公开可验证的信号，包括最近 push 时间、release 发布时间、open issues 数量、stars 和官网可访问性；接着把这些证据整理为健康状态、风险提示和 follow-up 列表，生成 JSON 报告和 Markdown 报告，供 reviewer 审阅。这个原型刻意不把自己定位成通用爬虫层，而是一个“审查台”：读证据、对里程碑、解释风险、支持人工复核。下一步会优先补 evidence trace（每个判断可回链原始证据）、milestone mapping（证据如何对应交付）和 human-in-the-loop（reviewer comment / override / follow-up state）。技术上保持可审计：每条结论都应能追溯到明确的公开信号，而不是黑箱打分。

## 代码仓库链接
https://github.com/Sipeng2024/gcc-impact-copilot

## Demo 视频链接
https://github.com/Sipeng2024/gcc-impact-copilot/blob/main/DEMO_WALKTHROUGH.md

## 公共物品属性
这个项目适合开放和复用。它不依赖 GCC 私有数据，核心是把 grant review 里的公开证据整理成可复核的工作流，因此任何 grant DAO、基金会、公共物品社区、黑客松资助计划都可以复用相同的 reviewer workflow。项目将以 MIT License 开源，证据适配器、里程碑映射、报告模板和 reviewer 状态机都可扩展。它不是只给 GCC 的内部小工具，而是一类公共物品资助“审查台”工具的开源起点。

## 风险与依赖
当前原型主要依赖公开数据源，因此第一类风险是公开信号并不总能完整反映真实进展，例如研究型项目或线下社区型项目，GitHub activity 不能代表全部影响；对应策略是把它明确定位为“审查输入和优先级排序层”，不替代人工 review。第二类风险是不同项目的 impact 维度差异很大，单一评分模型可能失真；对应策略是下一步引入项目类型化 rubric、里程碑映射和 reviewer override。第三类风险是 GitHub API、网站可用性等外部依赖会带来噪声；对应策略是保留原始 evidence 和抓取状态，并为关键判断保留人工复核。第四类风险是当前 demo 仍偏 CLI / backend prototype；下一阶段会补齐 reviewer-facing follow-up UI 和 evidence trace。

## 联系邮箱
99victorxie99@altiuslabs.xyz

## 收款地址
0x000000000000000000000000000000000000dEaD
