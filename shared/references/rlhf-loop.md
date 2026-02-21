# RLHF — 规划质量进化循环（通用框架）

> 每一轮规划都是一次学习机会。通过结构化评估 → 反馈 → 进化，让每一轮的规划质量递增。
> 本文档是 CEO / CPO / CMO 共享的 RLHF 通用框架，角色特定的评估维度和评估报告模板由各角色的 `*-eval-dimensions.md` 定义。

---

## 核心理念

规划不是一次性动作，而是持续进化的过程。RLHF 循环将每次规划的结果转化为可量化的信号，驱动规则和策略的迭代升级。

核心假设：
- 规划质量可以通过多维度评分客观衡量
- 用户反馈（+ 实际执行数据）是最有价值的奖励信号
- 规则的有效性可以通过累积应用数据验证
- 低质量规则应该被自动弱化，高质量规则应该被自动强化

---

## 5 阶段循环

```
┌─────────────┐
│  Phase 1    │
│  Generate   │──→ 按标准流程生成规划产物
└──────┬──────┘
       ▼
┌─────────────┐
│  Phase 2    │
│  Evaluate   │──→ 多维度评估打分（读取角色专属 eval-dimensions）
└──────┬──────┘
       ▼
┌─────────────┐
│  Phase 3    │
│  Feedback   │──→ ⏸️ 等待用户反馈（+ 执行数据）
└──────┬──────┘
       ▼
┌─────────────┐
│  Phase 4    │
│  Update     │──→ 更新规则置信度
└──────┬──────┘
       ▼
┌─────────────┐
│  Phase 5    │
│  Consolidate│──→ 固化经验，淘汰弱规则
└──────┬──────┘
       │
       └──→ 回到 Phase 1（下一轮规划）
```

---

### Phase 1: Generate — 生成规划

按标准流程生成规划产物，同时记录决策元数据。

**执行要求**：
- 按角色标准流程生成规划产物
- 记录生成过程中的关键决策点和所依赖的假设
- 标注哪些规则被应用了（用于后续追踪规则有效性）

**记录格式**：

```markdown
## 决策日志

### 应用的规则
- rule_id: {prefix}-001 — "{规则描述}"

### 关键假设
1. 假设: [描述] — 验证方式: [如何验证]

### 决策取舍
- 选择了 X 而非 Y，因为 [原因]
```

### Phase 2: Evaluate — 多维度评估

**执行流程**：
1. 读取角色专属评估维度定义（如 `plan-eval-dimensions.md`）
2. 确定当前公司阶段 / 产品类型，应用动态权重调整
3. 对规划逐维度打分（1-10 分）
4. 检查否决规则（Veto Rules）
5. 生成评估报告

**评估约束**：
- 打分必须给出具体理由，不允许笼统评价
- 每个维度至少列出 1 个扣分项或加分项
- 否决规则优先于总分判断

### Phase 3: Feedback — 人工反馈

**⏸️ WAIT — 必须暂停等待用户输入。**

**展示内容**：
1. 评估报告摘要（总分 + 各维度分数）
2. 关键风险点（评分最低的 2 个维度）
3. 改善建议（Top 3）

**收集内容**：
- 用户对每个维度评分的同意/调整
- 用户修改意见及原因（最重要的奖励信号）
- 用户对规划的整体判断: 通过 / 微调 / 重做

**反馈记录格式**：

```markdown
## 用户反馈

### 维度评分调整
| 维度 | AI 评分 | 用户评分 | 差异 | 用户说明 |
|------|--------|---------|------|---------|

### 整体判断
- 决定: [通过 / 微调 / 重做]
- 理由: ...

### 关键修改意见
1. [具体修改内容及原因]
```

### Phase 4: Update — 规则更新

基于反馈信号更新规则的置信度。

**更新公式**：

```
Score = Σ(applied_count × feedback_signal) / total_applications
Confidence = 1 - 1/(applied_count + 1)
```

其中:
- `applied_count`: 该规则被应用的次数
- `feedback_signal`: +1（正面反馈）/ 0（中性）/ -1（负面反馈）
- `total_applications`: 所有规则的总应用次数

**突变策略**：

| 条件 | 动作 | 说明 |
|------|------|------|
| score > 0.7 且 confidence > 0.7 | 强化规则 | 提升权重，标记为"已验证" |
| 0.3 < score < 0.7 | 保持观察 | 不调整，继续收集数据 |
| score < 0.3 且 confidence > 0.5 | 弱化或废弃 | 降低权重，3 次连续低分则废弃 |
| confidence < 0.3 | 探索性调整 | 数据不足，保留但标记"待验证" |

**规则状态流转**：

```
candidate → active → verified → core_rule
                   ↘ deprecated → removed
```

### Phase 5: Consolidate — 固化经验

将本轮学习成果固化为持久化知识。

**固化规则**：
- 高分规则（score > 0.7 且 confidence > 0.7）→ 固化为 SOP 级别规则
- 低分规则（score < 0.3 且 confidence > 0.5）→ 标记为 deprecated，准备废弃
- 新发现的模式 → 生成新的 candidate 规则
- 反复出现的用户反馈主题 → 生成新的评估 checklist 条目

**输出产物**：
- 更新 `evolution-state.yaml`（如存在）
- 记录本轮进化日志
- 如有 SOP 级别规则变更，更新相关 reference 文件

**进化日志格式**：

```markdown
## 进化日志 — {date}

### 规则变更
| rule_id | 变更类型 | 变更前 | 变更后 | 原因 |
|---------|---------|--------|--------|------|

### 累积统计
- 总规则数: X
- 活跃规则: X
- 已验证规则: X
- 废弃规则: X
- 本轮新增: X
- 本轮废弃: X
```

---

## 决策分层（通用）

| 总分区间 | 决策 | 后续动作 |
|---------|------|---------|
| >= 8.0 | 通过（Execute） | 直接执行，记录正向反馈 |
| 7.0 - 7.9 | 微调（Adjust） | 针对低分维度修改后重新评估 |
| 6.0 - 6.9 | 重大修改（Rethink） | 返回核心阶段重新审视 |
| < 6.0 | 重做（Redo） | 回到起点重新规划 |

---

## 数据结构

### 规则结构

```yaml
- id: {role}_rule_001
  category: {维度名}
  content: "{规则描述}"
  applies_to: [all]
  priority: high
  score: 0.85
  confidence: 0.91
  applied_count: 12
  positive_feedback: 9
  negative_feedback: 1
  neutral: 2
  created_at: YYYY-MM-DD
  last_applied: YYYY-MM-DD
  parent_rule: null
  child_rules: []
  conditions: []
  examples:
    good: ["..."]
    bad: ["..."]
```

### Episode 记录

```yaml
- episode_id: {role}_ep_001
  date: YYYY-MM-DD
  type: {规划类型}
  rules_applied: [rule_001, rule_003]
  eval_scores: { ... }
  veto_triggered: false
  decision: minor_revision
  feedback:
    user_signal: +0.5
    data_signal: null
```

---

## 冷启动策略

没有历史数据时：
1. **加载默认规则集**：来自各角色 reference 文件的核心原则
2. **前 3 次规划强制完整评估**：即使直接通过，也执行全量 7 维度评估
3. **第 3 次后启用完整 RLHF Loop**：规则得分和置信度开始生效
4. **第 5 次后启用 Consolidate**：开始规则整合优化

---

## 角色特化指引

| 角色 | 评估维度文件 | 评估对象 | 额外反馈源 |
|------|------------|---------|-----------|
| CEO | `plan-eval-dimensions.md` | tasks / roadmap / 复盘 | — |
| CPO | `product-eval-dimensions.md` | PRD / 版本计划 | CEO 审批信号、上线数据 |
| CMO | `growth-eval-dimensions.md` | growth-plan | ROI 数据、渠道表现数据 |

各角色的评估维度、否决规则、动态权重、评估报告模板均定义在各自的 `*-eval-dimensions.md` 中。本文档仅提供通用框架。
