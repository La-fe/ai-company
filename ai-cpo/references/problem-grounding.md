# 问题锚定方法论参考手册

> 本文档为 AI CPO Feature Design 的参考资料，在 Phase 1（问题锚定）时加载。
> 来源: Clayton Christensen JTBD Theory, First Round Review, Product School

---

## JTBD 分层方法

### 从宏观到微观

JTBD（Jobs-to-be-Done）是产品设计的锚点。company.md 中通常定义了**宏观 JTBD**（用户雇佣产品的根本原因），但要设计 Feature，需要拆解为**微观 JTBD**（每个概念解决的具体任务）。

**拆解步骤：**

1. **提取宏观 JTBD**: 从 company.md 中找到核心 JTBD 定义
2. **按概念拆分**: 每个产品概念对应 1-3 个微观 JTBD
3. **三维度分析**: 每个微观 JTBD 从三个维度描述

### 三维度 JTBD

| 维度 | 定义 | 示例 |
|------|------|------|
| **功能性任务**（Practical） | 用户要完成的实际操作 | "快速搭建一个能收款的在线商店" |
| **情感性任务**（Emotional） | 用户想要的内在感受 | "感觉自己像个专业的企业主" |
| **社会性任务**（Social） | 用户想要的社会形象 | "让客户觉得我的品牌很正规" |

### 微观 JTBD 模板

```
当 [具体场景/触发条件]，
我想要 [具体行动/完成什么]，
以便 [期望的结果/价值]。

功能性: [实际要完成什么操作]
情感性: [想要什么内在感受]
社会性: [想要什么外在形象]
```

**示例：**

```
当 我决定把自己的技能变成数字产品在线销售，
我想要 快速搭建一个专业的在线商店，
以便 在本周就开始接受第一笔订单。

功能性: 零代码创建含商品展示、支付、交付的完整店铺
情感性: 不再为"我不会做网站"焦虑
社会性: 分享店铺链接时客户觉得很专业
```

---

## 挣扎时刻识别法

挣扎时刻（Struggling Moment）是用户**当前方案失败、放弃或寻找替代方案的时刻**——这是产品介入的最佳切入点。

### 4 种力量模型

用户在做切换决策时受四种力量影响：

```
                    促进切换
            ┌───────────────────┐
            │                   │
    Push（推力）           Pull（拉力）
    现有方案的痛苦          新方案的吸引力
            │                   │
            │     ← 对抗 →      │
            │                   │
    Anxiety（焦虑）        Inertia（惯性）
    对新方案的不确定        现有方案的习惯
            │                   │
            └───────────────────┘
                    阻止切换
```

### 挣扎时刻发现步骤

1. **列出当前替代方案**: 用户现在怎么解决这个问题？（包括"手动做"和"不做"）
2. **找 Push**: 现有方案哪里让用户痛苦/低效/沮丧？
3. **找 Pull**: 我们的方案哪里比现有方案明显更好？
4. **找 Anxiety**: 用户对我们的方案会担心什么？（"AI 不靠谱"、"迁移麻烦"、"太贵"）
5. **找 Inertia**: 什么习惯让用户不想切换？（"现在的方案虽然不好但还能用"）
6. **定义挣扎时刻**: Push + Pull 必须大于 Anxiety + Inertia 的具体场景

### 输出模板

```markdown
### 概念: {概念名称}

**挣扎时刻**: 当 {场景}，用户 {遇到的问题}，导致 {后果}。

| 力量 | 具体表现 | 强度 |
|------|---------|------|
| Push | {现有方案的痛点} | 强/中/弱 |
| Pull | {新方案的吸引力} | 强/中/弱 |
| Anxiety | {用户的担忧} | 强/中/弱 |
| Inertia | {切换阻力} | 强/中/弱 |

**切入策略**: {如何增强 Push/Pull，减弱 Anxiety/Inertia}
```

---

## 反定位验证

"不做什么"的清单与"做什么"同样重要。反定位帮助聚焦，避免范围蔓延。

### 判断标准

一个功能应该被放入"不做"清单，如果：

| 条件 | 说明 |
|------|------|
| **偏离核心 JTBD** | 用户雇佣我们不是为了做这件事 |
| **AI 不可靠** | AI 在这个任务上的可靠度 < 70%，且无法有效 fallback |
| **竞品壁垒太高** | 竞品在这个点上积累了 3+ 年的数据/网络效应 |
| **边际用户需求** | 只有 <10% 的 ICP 需要这个功能 |
| **经济不可行** | AI 成本 > 该功能带来的收入贡献 |

### 输出格式

```markdown
### 不做清单

| 功能/方向 | 为什么不做 | 什么情况下重新考虑 |
|-----------|-----------|-------------------|
| {功能A} | {原因} | {条件变化时} |
```

---

## 参考来源

- Christensen Institute: [Jobs to be Done](https://www.christenseninstitute.org/jobs-to-be-done/)
- First Round Review: [Know Your Customers' Jobs to Be Done](https://review.firstround.com/know-your-customers-jobs-to-be-done)
- Product School: [JTBD Framework](https://productschool.com/blog/product-strategy/jobs-to-be-done-framework)
- Intercom: [When Coffee and Kale Compete](https://www.intercom.com/resources/books/intercom-jobs-to-be-done)
