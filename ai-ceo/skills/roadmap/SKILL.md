---
name: ceo-roadmap
description: "CEO Roadmap 综合：对齐产品线(CPO)和增长线(CMO)，生成带时间线的 Roadmap，检测依赖冲突和资源超载"
argument-hint: "[公司上下文目录] [--output PATH] [--tasks PATH]"
allowed-tools: Read, Write, Edit, Glob, Grep
user-invocable: true
---

# CEO Roadmap — 综合路线图

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). Resolve to absolute path before use.

综合 CPO（产品线）和 CMO（增长线）的输出，生成带时间线的 Roadmap。

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 公司上下文目录路径 | 交互式询问 |
| `--output` | 输出目录（roadmap.md 写入位置） | 与 `$0` 相同 |
| `--tasks` | tasks.jsonl 路径 | `{$0}/../tasks.jsonl` |

---

## Phase 1: 加载所有输入

```
读取 {context_dir}/company.md
读取 {output_dir}/goals.md
读取 {tasks_file}（筛选当前 plan 的任务）
读取 {output_dir}/version-plan.md    # CPO 输出
读取 {output_dir}/growth-plan.md     # CMO 输出
```

如果缺少任何文件，提示用户先完成前置步骤。

---

## Phase 2: 时间线综合

**Step 2.1: 对齐节奏**

分析并对齐两条线的时间节奏：
- 产品版本节奏（version-plan.md 中的版本里程碑）
- 增长节奏（growth-plan.md 中的增长阶段）
- 确保产品 release 和增长 campaign 在时间上协调

**Step 2.2: 依赖识别**

跨维度依赖检查：
- 增长活动是否依赖产品功能就绪？
- 技术基建是否阻塞产品开发？
- 运营资源是否支持增长节奏？

**Step 2.3: 资源冲突检测**

检查同一时间段内是否有：
- 同一负责人承担过多 P0 任务
- 关键依赖任务的截止时间矛盾
- 资源（特别是人力）的超载

输出冲突列表和建议调整。

> ⏸️ WAIT — 展示时间线分析、依赖图、资源冲突，等待人类确认调整方案。

---

## Phase 3: 输出 Roadmap

**Step 3.1**: 生成 `{output_dir}/roadmap.md`：

包含：月度时间线表（产品/增长/技术/运营/关键里程碑）、关键依赖链路、风险点（概率/影响/应对方案）、资源分配表。

**Step 3.2**: 更新 `{tasks_file}` 中当前 plan 的任务：
- 更新 `deadline` 字段（基于 Roadmap 时间线）
- 更新 `dependencies` 字段（基于跨维度依赖分析）
- 更新 `updated` 字段为今天日期

---

## Output Format — roadmap.md

```markdown
# Roadmap

> 生成时间: {date}
> 覆盖周期: {start_month} - {end_month}

## 月度时间线

| 月份 | 产品 | 增长 | 技术 | 运营 | 关键里程碑 |
|------|------|------|------|------|-----------|

## 关键依赖链路
{跨维度的关键依赖关系}

## 风险点
| 风险 | 概率 | 影响 | 应对方案 |
|------|------|------|---------|

## 资源分配
| 角色 | M1 | M2 | M3 | ... |
|------|----|----|----|----|
```
