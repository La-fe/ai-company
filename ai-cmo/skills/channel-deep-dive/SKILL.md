---
name: cmo-channel-deep-dive
description: "CMO 单渠道深度策略：加载渠道组长 profile，生成定制化执行方案、内容日历、KPI 追踪体系"
argument-hint: "[公司上下文目录] --channel seo|sem|social|kol [--budget 渠道预算]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# CMO Channel Deep Dive — 单渠道深度策略

> **Path Resolution**: `{PLUGIN_ROOT}` = 此插件的根目录（从本 SKILL.md 向上 2 级）。使用前解析为绝对路径。

你是对应渠道的增长专家。本技能对单个渠道进行深度策略设计，包含内容日历、KPI 体系、A/B 测试计划。

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `{PLUGIN_ROOT}/channels/{channel}/profile.md` | 渠道组长 profile（特性/最佳实践/KPI 基准） | Phase 1: 必读 |
| `{PLUGIN_ROOT}/references/growth-playbook.md` | 增长方法论和通用 KPI 基准 | Phase 2: 策略细化 |

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 公司上下文目录路径 | 交互式询问 |
| `--channel` | 渠道类型 (seo\|sem\|social\|kol) | 必填 |
| `--budget` | 渠道月预算 | 交互式询问 |
| `--output` | 输出目录 | 与 `$0` 相同 |

---

## Phase 0: 加载上下文

```
读取 {context_dir}/company.md           # ICP、产品特性
读取 {context_dir}/arsenal.md            # 内容创作工具
读取 {output_dir}/growth-plan.md         # 整体策略（如有）
```

---

## Phase 1: 渠道 Profile 加载

> 读取 `{PLUGIN_ROOT}/channels/{channel}/profile.md`

从 profile 中提取：
- 渠道特性和适用场景
- 行业 KPI 基准线
- 最佳实践和常见陷阱
- 工具推荐

---

## Phase 2: 深度策略设计

根据不同渠道类型生成定制化策略：

### SEO 渠道
- 关键词研究（核心词 + 长尾词矩阵）
- 内容规划（SEO 友好内容主题 x 页面类型）
- 技术 SEO 检查清单
- 外链建设策略

### SEM 渠道
- 关键词分组（品牌词/品类词/竞品词/长尾词）
- 出价策略和预算分配
- 广告文案 A/B 测试计划
- 着陆页优化建议

### Social 渠道
- 平台选择和定位（基于 ICP 活跃平台）
- 内容日历（主题/形式/发布频率/最佳时间）
- 社群运营策略
- 用户互动规则

### KOL 渠道
- KOL 筛选标准和合作模式
- 内容共创方案
- 效果追踪和 ROI 计算
- 长期合作 vs 单次合作策略

---

## Phase 3: 输出

生成渠道深度策略文档：`{output_dir}/channel-{channel}-strategy.md`

**⏸️ WAIT**: 展示策略，收集修改意见。

---

## Output Format

```markdown
# {Channel} 深度策略 — {公司名称}

## 渠道概况
## 目标与 KPI
| KPI | 基线 | 30天目标 | 60天目标 | 90天目标 |
|-----|------|---------|---------|---------|

## 执行计划
### 第 1-2 周: 基建搭建
### 第 3-4 周: 内容启动
### 第 5-8 周: 规模化
### 第 9-12 周: 优化

## 内容日历（首月）
## 预算明细
## A/B 测试计划
## 工具清单
## 风险和应对
```
