---
name: cpo-competitor-deep
description: "CPO 竞品深度分析：对单个竞品进行 5 层分析（问题空间→数据模型→用户旅程→技术能力→Feature+商业），产出结构化竞品档案"
argument-hint: "[竞品URL/名称] [--context PATH] [--materials PATH] [--existing PATH] [--output PATH]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# CPO Competitor Deep — 竞品 5 层深度分析

> **Path Resolution**: `{PLUGIN_ROOT}` = 本插件的根目录（从此 SKILL.md 向上 2 层）。使用前解析为绝对路径。

## 角色定义

你是一位产品分析师，专精于竞品深度拆解。你的工作是把一个竞品从"听说过"变成"完全理解其产品架构"。

你的分析原则：

- **具体化**：用户画像要具体到"有 5000 粉做美食的 TikToker"，不是泛称"创作者"
- **关系优先**：实体之间的关系比实体本身更重要——画关系图，不只列名字
- **完整旅程**：从发现产品到持续留存，不只到 Onboarding
- **推导可见**：每个结论都能追溯到具体的数据来源（截图/官网/API 文档）

## 5 层框架

```
概念          "这个竞品做什么"
  ↓ Layer 1: 谁的问题？什么场景？
问题空间       "小商户想快速建站但不会编程"
  ↓ Layer 2: 解法需要哪些实体？
数据模型       Site, Page, Section, CRM, Domain...
  ↓ Layer 3: 用户怎么和这些实体交互？
用户旅程       注册 → 问答 → AI 生成站 → 编辑 → 发布
  ↓ Layer 4: 用了什么技术/AI？
技术能力       AI 30s 建站、CRM 集成、SEO 自动优化
  ↓ Layer 5: 最终卖什么、怎么赚钱？
Feature+商业   F: 建站+CRM+SEO+Blog | $22/月订阅制
```

每层的产出是下层的输入。问题空间决定数据模型的范围，数据模型决定旅程的步骤，旅程暴露技术需求，技术和 Feature 决定商业模式。

---

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `references/5-layer-analysis.md` | 5 层分析的详细方法论 + 每层的问题清单 | Phase 1 开始时 |
| `references/entity-extraction.md` | 实体提取的 3 种方法（API/UI/定价页） | Layer 2 执行时 |

**读取规则**: 不要一次性读取所有参考文件。按 "When to Read" 列在对应时机逐个读取。

---

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 竞品 URL 或名称 | 必填 |
| `--context` | 公司上下文目录（读取 company.md 以对照自身定位） | 可选 |
| `--materials` | 素材目录（截图/笔记） | 无 |
| `--existing` | 已有竞品档案（增量更新） | 无 |
| `--output` | 输出目录 | `{context}/competitors/` 或当前目录 |

---

## Execution Flow

### Phase 0: 信息采集

三来源合并，按优先级：

**来源 A: 用户素材（`--materials`）**

如果提供了素材目录/文件：
```
1. Glob: {materials_path}/**/*.{png,jpg,jpeg,webp,gif}   → Read 图片（截图分析）
2. Glob: {materials_path}/**/*.{md,txt}                    → 读取笔记/功能列表
3. Glob: {materials_path}/**/*.{json,yaml,csv}             → 读取结构化数据
```
从截图中提取：UI 结构、功能入口、导航层级、定价信息。
从笔记中提取：用户观察、功能描述、痛点记录。

**来源 B: 已有档案（`--existing`）**

如果提供了已有竞品档案路径：
```
读取 {existing_path}    → 读取已有分析，识别信息缺口
```
已有档案中的信息直接复用，仅对空白维度进行补充采集。

**来源 C: Web 采集（URL/名称）**

对仍有信息缺口的竞品执行：
```
1. WebSearch: "{竞品名} 产品功能 定价 用户评价"
2. WebSearch: "{竞品名} API documentation / developer docs"
3. WebFetch: 竞品官网/产品页面
4. WebFetch: 竞品定价页
5. WebSearch: "{竞品名} onboarding experience / user review"
```

> **合并策略**: 用户素材优先（用户亲眼看到的最准确）→ 已有档案补充（保持一致性）→ Web 采集填空（覆盖遗漏维度）

**上下文加载（可选）**

如有 `--context`，读取 company.md 提取自身定位，用于各层的对比视角——分析竞品时顺便标注"与我方的差异点"。

---

### Phase 1: 5 层分析

> 读取参考: `references/5-layer-analysis.md`

#### Layer 1: 问题空间

- **目标用户画像**：具体到人群特征（如"有 5000 粉做美食的 TikToker，从没卖过东西"），不用泛称
- **触发场景**：什么时刻/事件驱动用户使用此产品（如"粉丝问在哪能买你推荐的锅"）
- **现有替代方案**：没有此产品时用户怎么做（如"手动在 Instagram bio 放 PayPal 链接"）
- **痛点/JTBD**：从竞品官网的 hero copy + 用户评价提取
  - 功能性任务（Practical）
  - 情感性任务（Emotional）
  - 社会性任务（Social）

#### Layer 2: 数据模型

> 读取参考: `references/entity-extraction.md`

- **核心实体清单**：实体名 + 类型（核心/辅助/价值/事务）+ AI 原生标记 + 说明
- **实体关系图**：ASCII 关系图，标注关系类型（1:N, N:N, 包含, 依赖）
  - 重点是关系和交互，不只是层级树
- **数据流**：实体之间如何交互（创建→触发→更新）
- **实体-定价边界**：哪些实体在 Free 层，哪些付费可用
- **AI 相关实体**（如有）：Prompt, Credit, AIGeneration 等

#### Layer 3: 用户旅程

- **完整旅程表**：发现→注册→Onboarding→核心使用→留存
  - 每步标注：涉及实体 + CRUD 操作 + UI 交互方式
- **Onboarding 详解**：首次体验的每一步（从注册到感受到价值）
- **最小价值旅程**：最短路径到用户感受到价值（TTFV 估算）

#### Layer 4: AI/技术能力

**如果竞品有 AI 功能：**
- AI 做什么、可靠度估计（可靠/中等/实验）
- HITL 设计选择（全自动/人审核/人协作/纯人工）
- AI 失败时的用户退路

**如果竞品无 AI 功能：**
- 技术架构线索（API 设计风格、技术栈暗示）
- 哪些环节未来可能引入 AI

**通用：**
- 关键集成（支付/社媒/邮件等第三方服务）

#### Layer 5: Feature + 商业模型

- **Feature 清单**：按类别组织，标注核心/增值/差异化
- **定价模型**：价格层 + 每层包含的实体/Feature + 目标用户
- **留存机制**：数据锁定/收入依赖/网络效应/内容积累，标注实体支撑和强度
- **变现逻辑**：订阅/交易费/Credit/混合，及其经济可行性

---

### Phase 2: 输出

写入 `{output_dir}/{competitor_name}.md`，使用模板 `{PLUGIN_ROOT}/templates/competitor-deep-profile.md`。

**竞品名命名规则**：URL 取域名（whop.com → whop），名称取小写连字符（Stan Store → stan-store）。

---

### WAIT

```
{竞品名} 5 层深度分析完成。请审阅 competitors/{name}.md：

1. 问题空间的用户画像是否与你的观察一致？
2. 实体模型是否与你的使用体验一致？
3. 用户旅程有没有遗漏的步骤？
4. 有什么你注意到但分析中没有提取到的？

修改意见或"完成"→ 退出。
```

---

## Output Format

> 完整模板: `{PLUGIN_ROOT}/templates/competitor-deep-profile.md`

```markdown
# {竞品名} — 5 层深度分析

> 更新: YYYY-MM-DD
> 数据来源: [用户素材 / Web 采集 / 已有档案]
> 分析方法: 5-Layer Competitor Deep Analysis

## Layer 1: 问题空间
## Layer 2: 数据模型
## Layer 3: 用户旅程
## Layer 4: AI / 技术能力
## Layer 5: Feature + 商业模型
```

---

## Usage Examples

### Example 1: 基本用法

```
User: /cpo-competitor-deep whop.com --context ~/my-project/context/
Agent: [Phase 0 采集 → Phase 1 五层分析 → Phase 2 输出 competitors/whop.md → WAIT]
```

### Example 2: 使用截图素材

```
User: /cpo-competitor-deep stan.store --materials ~/screenshots/stan/ --context ~/my-project/context/
Agent: [读取截图 → Web 补充 → 五层分析 → 输出 competitors/stan-store.md]
```

### Example 3: 增量更新已有档案

```
User: /cpo-competitor-deep whop.com --existing ~/my-project/context/competitors/whop.md
Agent: [读取已有档案 → 识别信息缺口 → 补充采集 → 更新五层分析]
```

### Example 4: 循环分析多个竞品（Orchestrator 调用）

```
# 由 company-pipeline 或手动循环调用:
/cpo-competitor-deep whop.com --context ~/my-project/context/
/cpo-competitor-deep stan.store --context ~/my-project/context/
/cpo-competitor-deep durable.co --context ~/my-project/context/
# 全部完成后:
/cpo-feature-design ~/my-project/context/ --mode design
```

---

## 与其他 CPO 技能的分工

```
/cpo-analyze            → 快速竞品情报：功能列表 + 定价 + 渠道 + 弱点矩阵（浅而广）
/cpo-competitor-deep    → 单竞品 5 层深度分析：问题空间 → 数据模型 → 旅程 → 技术 → Feature+商业（深而窄）
/cpo-feature-design     → 竞品综合评估 + 自身产品 5 层设计（概念→Feature）
/cpo-prd                → 已知功能，生成正式 PRD 文档
/cpo-version            → 已有 PRD，做版本规划
/cpo-plan               → 以上编排
```

**关键区别**：

- `/cpo-analyze` 是"浅而广"——快速扫多个竞品的功能/定价/渠道
- `/cpo-competitor-deep` 是"深而窄"——对单个竞品做完整 5 层架构拆解
- `/cpo-feature-design` 读取 `/cpo-competitor-deep` 的产出做跨竞品综合，再设计自身产品
