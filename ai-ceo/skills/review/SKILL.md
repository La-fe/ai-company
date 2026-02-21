---
name: ceo-review
description: "CEO 复盘评估：对照 Roadmap 和 tasks 评估进度、识别风险、输出调整建议，生成周/月复盘报告"
argument-hint: "[公司上下文目录] [--output PATH] [--tasks PATH]"
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# CEO Review — 复盘评估

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). Resolve to absolute path before use.

对照 Roadmap 和 tasks，评估进度，识别风险，输出调整建议。

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `{PLUGIN_ROOT}/references/review-framework.md` | 复盘框架：周/月复盘模板 + 风险评估 + 偏差分析 | Phase 2: 开始复盘评估时 |

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 公司上下文目录路径 | 交互式询问 |
| `--output` | 输出目录 | 与 `$0` 相同 |
| `--tasks` | tasks.jsonl 路径 | `{$0}/../tasks.jsonl` |

---

## Phase 1: 加载当前状态

```
读取 {tasks_file}（筛选当前 plan 的任务）
读取 {output_dir}/roadmap.md
读取 {output_dir}/goals.md
```

> 读取 `{PLUGIN_ROOT}/references/review-framework.md`

---

## Phase 2: 评估与分析

**Step 2.1: 逐任务评估**

对 tasks.jsonl 中当前 plan 每个 in_progress 和 pending 的任务评估状态：

| 状态 | 定义 |
|------|------|
| on_track | 按计划推进，无风险 |
| at_risk | 有延期风险，但可控 |
| blocked | 被阻塞，需要外部介入 |
| completed | 已完成，待验证成功标准 |

**Step 2.2: Roadmap 偏差分析**

对比 roadmap.md 的时间线与实际进度：
- 哪些里程碑已达成？
- 哪些里程碑偏离计划？偏离多少？
- 偏差的根因是什么？

**Step 2.3: 风险评估**

识别当前的 Top 3 风险（概率 x 影响评估 + 应对方案）。

输出复盘报告（进度总览表 + Roadmap 偏差表 + Top 3 风险 + 建议调整）。

> ⏸️ WAIT — 展示复盘报告，等待人类确认调整方案。

---

## Phase 3: 更新文件

根据人类确认的调整方案：

**Step 3.1**: 更新 `{tasks_file}` 中相关任务的 status / priority / deadline / notes / updated 字段

**Step 3.2**: 更新 `{output_dir}/roadmap.md` 的时间线、里程碑、风险列表

**Step 3.3**: 更新 `{output_dir}/goals.md` 的目标完成进度（如有目标需要调整，标注变更原因）

**Step 3.4**: 生成复盘报告
- 周复盘 → `{context_dir}/../reviews/{YYYY}-W{NN}.md`
- 月度复盘 → `{context_dir}/../reviews/{YYYY-MM}-retro.md`

---

## Output Format — 复盘报告

```markdown
## 复盘报告

### 进度总览
| 状态 | 数量 | 占比 |
|------|------|------|

### Roadmap 偏差
| 里程碑 | 计划时间 | 实际状态 | 偏差 | 根因 |
|--------|---------|---------|------|------|

### Top 3 风险
1. [风险描述] — 概率: 高 | 影响: 高 | 应对: ...

### 建议调整
- [具体的调整建议]
```
