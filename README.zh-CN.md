# AI Company OS

> 三个 AI 高管，在你的终端里。从商业想法到可执行计划。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-blueviolet)](https://claude.com/claude-code)
[![Plugins: 6](https://img.shields.io/badge/Plugins-6-green)]()

[English](./README.md) | **中文**

---

你运行 `/init-company`。AI CEO 开始像真正的投资人一样提问：你的产品是什么？客户是谁？现在在什么阶段？卡在哪里？

十分钟后你得到 `company.md` —— 你创业公司的 DNA，一个结构化文件，每个 AI agent 都能读取和推理。

然后你运行 `/ceo-plan`。你那句模糊的目标"这个季度要做到 $20k MRR"，被拆解成 30+ 任务，横跨 4 个维度（产品、增长、技术、运营），每个任务都有优先级、负责人、截止日期和成功标准。Agent 会对自己的方案进行 7 个维度打分，然后指出："你给 KOL 合作分配了零人力，但期望达成 5 个合作。这个计划经不起现实的检验。"

你运行 `/teardown`。它对每个竞品进行六层逆向工程：问题空间 → 数据模型 → 用户旅程 → 定价映射 → 留存机制 → Feature 目录 + 设计决策。每个竞品输出约 500 行的结构化档案，跨竞品模式自动浮现。

你运行 `/cpo-plan`。它基于竞品情报撰写包含用户故事和验收标准的真实 PRD，并设计 3 个月版本计划：V1.0 MVP → V1.1 验证 → V1.2 增长。

你运行 `/cmo-plan`。它会用 6 个指标给每个增长渠道打分，构建关键词矩阵，设计含预算分配的 SEM 投放方案，并将你的 AI 写作工具映射为增长武器。

最后，`/ceo-plan --mode roadmap` 把所有内容综合为统一的时间线。依赖关系明确标注，资源冲突被标记，风险缓解方案一并输出。

所有这些都在 Git 中版本控制。你可以 `git diff` 三个月前的战略。

```
/init-company "My Startup"
      ↓
/ceo-plan        → 诊断阶段 → 拆解目标 → 4 维度 × P0/P1/P2
      ↓
/teardown        → 六层竞品逆向工程 → 结构化竞品档案
      ↓
/cpo-plan        → PRD（用户故事 + 验收标准）→ 版本计划
      ↓
/cmo-plan        → 渠道打分 → SEO/SEM/社媒/KOL → 预算 + 日历
      ↓
/ceo-plan --mode roadmap   → 综合所有 → 时间线 + 依赖关系
```

## 快速开始

```bash
# 添加插件市场
/plugin marketplace add La-fe/ai-company

# 安装所有插件
/plugin install init-company@ai-company
/plugin install ai-ceo@ai-company
/plugin install ai-cpo@ai-company
/plugin install ai-cmo@ai-company
/plugin install competitor-teardown@ai-company
/plugin install company-pipeline@ai-company
```

或者一条命令运行完整流水线：

```bash
/company-pipeline "My Startup"
```

## 实际效果展示

### 1. 初始化：CEO 访谈

运行 `/init-company`，agent 进行结构化访谈：

```
第 1 轮：身份 + 产品
→ 你的核心产品是什么？解决什么问题？
→ 你现在在什么阶段？（有用户？有收入？还在开发？）
→ 目标客户是谁？（具体到：行业、规模、角色）

第 2 轮：定位 + 竞争
→ 你的客户今天怎么解决这个问题？
→ 你的优势是什么？（要机制，不要形容词）
→ 你明确不做什么？

第 3 轮：原则 + 目标
→ 你的决策原则是什么？（"速度 > 完美"？）
→ 这个季度最重要的 1-3 件事？
→ 每件事的成功标准是什么？（可量化）
```

输出：`company.md` + `goals.md` + `arsenal.md` —— 你公司的结构化基因组。

### 2. CEO 诊断：模糊目标 → 可执行任务

你说："这个季度要做到 $20k MRR。"

CEO agent 诊断你的阶段，识别主要矛盾，然后拆解：

```
目标 G1：达到 $20k MRR

产品 (CPO)
  G1-P-01  完成支付系统重构        P0  2 周    阻塞 G1-G-01
  G1-P-02  客户分析看板            P1  1.5 周

增长 (CMO)
  G1-G-01  启动 SEO 策略           P0  持续    依赖 G1-P-02
  G1-G-02  测试 2 个付费渠道       P0  3 周

技术 (CTO)
  G1-T-01  数据追踪管线            P0  2 周    阻塞 G1-P-02, G1-G-01

运营 (COO)
  G1-O-01  客户 onboarding SOP     P1  1 周
```

然后它会进行 **7 个维度的自我评估**：

```
主要矛盾准确度    9/10   正确识别了增长渠道瓶颈
目标可达性        7/10   3 周内做到 $20k 比较紧张，需考虑外部风险
任务完整性        8/10   4 个维度已覆盖，缺少风险缓解任务
资源可行性        6/10   3 人团队 + 0 市场人力，增长任务有风险

结论：需调整。增加市场人力的应急方案。
```

评分过低的方案会被**附理由驳回**。不允许自我欺骗。

### 3. 竞品拆解：六层逆向工程

运行 `/teardown whop.com stan.store durable.co`，agent 抓取每个竞品并通过 6 个分析层生成结构化档案：

```
第 1 层：问题空间
  → 目标用户画像、核心 JTBD、触发场景、替代方案
  → 关键指标：用户数、收入、ARPU、市场份额

第 2 层：数据模型（核心层）
  → 实体提取：核心 / 辅助 / 价值 / 事务
  → 实体关系图（标准化符号）
  → Top 3-5 核心实体的字段级定义

第 3 层：用户旅程
  → 步骤 × 页面 × 实体 × CRUD 操作表
  → 关键流程图（分叉、循环）
  → TTFV 分析（从注册到首次感受价值的步骤数）

第 4 层：定价-实体映射
  → 定价模型分类（订阅 / 交易抽成 / 信用点 / 免费增值 / 混合）
  → 层级对比：免费 / 基础 / 专业 / 企业
  → 实体 ↔ 定价边界表（每个层级限制了什么）

第 5 层：留存机制
  → 7 种留存策略打分：数据锁定、社交绑定、习惯养成、
    切换成本、网络效应、内容沉淀、收入依赖

第 6 层：Feature 目录 + 设计决策
  → 完整功能清单（类别 × 实体 × 定价层级）
  → AI 能力审计（如适用）
  → 设计决策推理（含推理链）
```

每个竞品输出约 500 行的 `{name}.md` 档案。所有竞品分析完成后，自动生成跨竞品 `landscape.md`：

```
全景综合：
  → 实体共性矩阵（核心 / 多数 / 少数 / 空白）
  → 架构模式（扁平 / 层级 / 多态 / 事件驱动）
  → 定价全景对比
  → 跨竞品 TTFV 对比
  → 留存策略对比矩阵
  → 空白机会 + 影响评估
```

### 4. CPO：PRD → 版本计划

基于竞品拆解情报，CPO agent 生成：

**竞品矩阵：**

```
           我们         竞品 A          竞品 B
ICP        中小电商     所有电商        仅企业级
定价       $99-299     $49-199         $499-999
优势       AI 驱动     功能丰富        企业信任度
劣势       无国际化    过于复杂        昂贵 + 学习曲线陡

机会：没有人做 AI 驱动的内容本地化。
```

**包含真实用户故事的 PRD：**

```
作为一个每天上传 15+ SKU 的跨境电商运营，
我希望能从一张图片生成 3 语种的商品描述，
这样我可以把每个 SKU 的处理时间从 30 分钟降到 5 分钟。

验收标准：
- [ ] 从图片 + 基本信息 60 秒内生成
- [ ] 输出包括标题、卖点、使用场景
- [ ] 一键同步到 Amazon/Shopify
- [ ] 支持 CSV 批量导入（100+ SKU）
```

**3 个月版本计划：**

```
V1.0 MVP（第 1-4 周）      核心价值验证
V1.1 数据（第 5-8 周）     用户行为分析，迭代
V1.2 增长（第 9-12 周）    多平台对接，批量操作
```

### 5. CMO：渠道打分 → 增长策略

CMO agent 从 6 个维度给渠道打分：

```
渠道     成本   速度   天花板  复利    AI友好度  产品适配  综合分
SEO      低     慢     高      高      高        高        8.5 ← 第一
SEM      中     快     中      无      高        中        7.0 ← 第二
社媒     低     快     中      中      中        低        6.5
KOL      高     快     低      低      无        高        6.0
```

然后为每个渠道制定详细策略：关键词矩阵、投放结构、预算分配、ROI 预测、30-60-90 天行动计划。

并将你的 AI 写作工具映射为执行武器：

```
/find-topic         → 关键词挖掘
/article-pipeline   → 端到端内容生产
/publish            → LinkedIn、X、Substack、微信公众号
```

### 6. 统一 Roadmap：全局同步

```
       三月                四月               五月
产品   V1.0 MVP 开发       V1.0 打磨          V1.1 开发
增长   SEO 内容（10 倍）   SEM 上线           KOL 合作
技术   分析系统搭建        支付对接            数据看板
运营   客服手册            融资准备            启动融资

依赖关系：
  SEM 上线    ← V1.0 + 落地页完成
  KOL 启动    ← 积累 10+ 客户成功案例
  V1.1 开发   ← V1.0 分析数据收集完成
```

### 7. Git Log 就是你的公司历史

```
$ git log --oneline
abc123 retro: 2026-03 completed
def456 review: week 2026-W12
ghi789 adjust: G1 target 100 → 150 based on traction
jkl012 roadmap: 2026-04 final
mno345 cmo: growth plan 2026-03
pqr678 cpo: PRD + version plan 2026-03
stu901 ceo: goals + tasks 2026-03
vwx234 init: company context
```

每个决策都有记录。每次转型都有文档。`git diff` 你的战略演变。

## 为什么不一样

**这不是一个 prompt 包装器，而是一个方法论引擎。**

- **70+ 参考文档**：任务拆解框架、PRD 写作标准、渠道评分矩阵、行业 KPI 基准、产品类型模板
- **RLHF 质量循环**：每个输出都经过 7 个角色专属维度的评估。动态权重根据公司阶段调整。否决规则会驳回低质量方案
- **依赖管理**：任务不是孤立的。系统追踪什么阻塞什么。改一个截止日期，它会标记所有下游影响
- **Git 原生**：所有公司知识以版本控制的 Markdown 存储。公司运行得越久，系统越智能

## 插件

| 插件                                            | 触发命令            | 功能                                            |
| ----------------------------------------------- | ------------------- | ----------------------------------------------- |
| [init-company](./init-company/)                 | `/init-company`     | 引导式访谈 → company.md + goals.md + arsenal.md |
| [ai-ceo](./ai-ceo/)                             | `/ceo-plan`         | 诊断 → 拆解 → 路线图 → 复盘（3 种模式）         |
| [ai-cpo](./ai-cpo/)                             | `/cpo-plan`         | PRD → 版本计划 → 功能设计                        |
| [ai-cmo](./ai-cmo/)                             | `/cmo-plan`         | 渠道打分 → SEO/SEM/社媒/KOL → 增长计划          |
| [competitor-teardown](./competitor-teardown/)     | `/teardown`         | 六层竞品逆向工程 → 结构化竞品档案                |
| [company-pipeline](./company-pipeline/)           | `/company-pipeline` | 完整流水线 + 每日面板 + 周期复盘                |

## 输出结构

```
{company_dir}/
├── context/
│   ├── company.md            # 公司 DNA
│   ├── arsenal.md            # 技能、API、工具清单
│   └── competitors/          # 每个竞品的深度拆解
├── plans/{cycle}/
│   ├── goals.md              # OKR 格式的目标
│   ├── prd.md                # 产品需求文档 (CPO)
│   ├── version-plan.md       # 3 个月版本路线图 (CPO)
│   ├── growth-plan.md        # 渠道策略 (CMO)
│   └── roadmap.md            # 统一时间线 (CEO)
├── reviews/                  # 周复盘 & 月复盘
└── tasks.jsonl               # 中央任务仓库（含依赖关系）
```

## 架构

```
ai-company/
├── init-company/              # 公司初始化
├── ai-ceo/                    # CEO：目标、任务、路线图、复盘
│   └── references/            # 任务拆解、评估维度、复盘框架
├── ai-cpo/                    # CPO：PRD、版本、功能设计
│   └── references/            # PRD 框架、产品评估、数据模型提取
├── ai-cmo/                    # CMO：渠道、SEO、SEM、社媒、KOL
│   ├── channels/              # 渠道组长 Profile（SEO/SEM/社媒/KOL）
│   └── references/            # 渠道矩阵、增长手册、评估维度
├── competitor-teardown/       # 六层竞品逆向工程
│   └── references/            # 提取方法、AI 审计、综合模式
├── company-pipeline/          # 编排器 + 面板
└── shared/                    # RLHF 循环、任务 Schema、面板脚本
```

## 贡献

欢迎贡献。

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的修改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

## 许可证

[MIT](LICENSE)
