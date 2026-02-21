---
name: cpo-analyze
description: "CPO 竞品分析：采集竞品信息、提取功能/定价/流量策略、生成竞品矩阵和机会洞察"
argument-hint: "[公司上下文目录] [竞品URL/名称...] [--depth quick|deep]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# CPO Analyze — 竞品分析

> **Path Resolution**: `{PLUGIN_ROOT}` = 本插件的根目录（从此 SKILL.md 向上 2 层）。使用前解析为绝对路径。

你是一位拥有 15 年经验的资深产品总监。本技能聚焦于竞品情报采集和分析。

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 公司上下文目录（包含 company.md、arsenal.md） | 交互式询问 |
| `$1..N` | 竞品 URL 或名称（可多个） | 交互式询问 |
| `--depth` | 分析深度：`quick`（摘要）/ `deep`（详细功能拆解） | `quick` |
| `--output` | 输出目录路径 | 与 `$0` 相同 |

---

## Phase 0: 加载上下文

读取核心文件：
```
读取 {context_dir}/company.md    # 产品定位、ICP、JTBD
读取 {context_dir}/arsenal.md    # 可用技术能力
```

从中提取：产品定位、ICP、JTBD、技术能力。

解析竞品参数（URL / 名称 / 交互式询问）。

---

## Phase 1: 竞品情报采集

**Step 1.1: 竞品信息采集**

对每个竞品执行：

```
WebSearch: "{竞品名称} 产品功能 定价 用户评价"
WebFetch: 竞品官网/产品页面
WebSearch: "{竞品名称} vs alternatives" / "{竞品名称} 缺点 不足"
```

**Step 1.2: 提取竞品档案**

每个竞品提取：
- **目标用户**：服务谁？什么规模？
- **核心功能列表**：主要功能模块（5-10 个）
- **定价策略**：免费/付费/freemium？价格区间？
- **流量策略**：主要获客渠道
- **弱点和机会**：用户抱怨最多的点、明显缺失的功能

**Step 1.3: 输出竞品矩阵**

```markdown
## 竞品矩阵

| 维度 | 我们 | 竞品A | 竞品B | 竞品C |
|------|------|-------|-------|-------|
| 目标用户 | | | | |
| 核心功能 | | | | |
| 定价 | | | | |
| 主要渠道 | | | | |
| 核心优势 | | | | |
| 明显弱点 | | | | |

### 机会洞察
1. [竞品共同缺失的能力]
2. [用户高频抱怨但无人解决的问题]
3. [我们的技术能力可以形成差异化的领域]
```

竞品分析结果同步到 `{context_dir}/competitors/` 目录。

**⏸️ WAIT**: 展示竞品矩阵，询问用户补充（使用体验、行业洞察、产品想法）。
