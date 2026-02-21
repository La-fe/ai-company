# 经验库 (Knowledge Base)

跨角色共享的经验积累系统。每个子目录对应一类经验，按固定格式持续积累。

---

## 目录结构

```
knowledge-base/
├── decision-patterns/       # CEO 决策模式
│   └── {YYYY-MM-DD}-{slug}.md
├── review-learnings/        # 复盘经验教训
│   └── {YYYY-MM-DD}-{slug}.md
└── industry-benchmarks/     # 行业基准数据
    └── {industry}-{dimension}.md
```

---

## 积累时机

| 目录 | 触发者 | 触发时机 | 条件 |
|------|--------|---------|------|
| `decision-patterns/` | CEO (review) | 每次复盘后 | 发现可复用的决策模式（如"冷启动期聚焦 PMF"） |
| `review-learnings/` | CEO (review) | 周/月复盘后 | 出现 Roadmap 偏差 > 30% 或阻塞 > 2 天的经验教训 |
| `industry-benchmarks/` | CMO (strategy) | 市场调研后 | 获取到行业 CPC/CAC/转化率等硬数据 |

---

## 文件格式

### decision-patterns/{date}-{slug}.md

```markdown
# {模式名称}

**适用阶段**: [冷启动 / 增长期 / 成熟期]
**来源**: {哪次复盘/规划发现的}
**置信度**: [低 / 中 / 高]（随应用次数提升）

## 模式描述
{一句话总结}

## 适用条件
- 条件 1
- 条件 2

## 不适用条件
- 条件 1

## 执行要点
1. ...
2. ...

## 应用记录
| 日期 | 公司/项目 | 结果 | 备注 |
|------|----------|------|------|
```

### review-learnings/{date}-{slug}.md

```markdown
# {经验标题}

**严重程度**: [提示 / 警告 / 教训]
**来源**: {YYYY}-W{NN} 或 {YYYY-MM} 复盘
**关联任务**: [{task_id}]

## 发生了什么
{事实描述}

## 根因分析
{为什么发生}

## 经验教训
{下次应该怎么做}

## 预防措施
- [ ] {具体的规则/检查项}
```

### industry-benchmarks/{industry}-{dimension}.md

```markdown
# {行业} — {维度} 基准数据

**最后更新**: {date}
**数据来源**: {来源说明}

| 指标 | 低 | 中位 | 高 | 数据源 |
|------|-----|------|-----|--------|

## 趋势
{季度/年度趋势说明}

## 注意事项
{数据解读的注意事项}
```

---

## 使用方式

各角色 SKILL.md 在相关阶段按需读取：

- **CEO diagnose**: 读取 `decision-patterns/` 辅助判断公司阶段和主要矛盾
- **CEO review**: 读取 `review-learnings/` 对照历史经验评估风险；复盘后写入新经验
- **CMO strategy**: 读取 `industry-benchmarks/` 辅助渠道评估和 ROI 预估；调研后写入新数据
- **CPO prd**: 读取 `decision-patterns/` 中产品相关模式辅助功能优先级决策

## 维护原则

1. **只增不删**: 经验条目只追加不删除（废弃的标记 `deprecated`）
2. **有出处**: 每条经验必须关联到具体的复盘/调研
3. **可验证**: 基准数据必须标注数据源和更新时间
4. **轻量优先**: 每条经验 < 50 行，保持可快速扫描
