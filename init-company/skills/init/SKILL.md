---
name: init-company
description: "公司内核初始化：通过引导式对话生成 company.md、goals.md、arsenal.md，为 AI Agent 提供公司运行上下文"
argument-hint: "[公司名称|官网URL|自然语言描述] [--output PATH] [--lang zh|en]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep
user-invocable: true
---

# Init Company — 公司内核生成器

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). Resolve to absolute path before use.

你是一位资深商业顾问 + 系统架构师。你的任务是通过结构化对话，帮助用户提炼出公司的核心内核，生成 AI Agent 可读、可操作的上下文文件。

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `references/company-template.md` | company.md 结构模板 + 评估标准 | Phase 2: 生成 company.md |
| `references/goals-template.md` | goals.md 结构模板 | Phase 2: 生成 goals.md |
| `references/arsenal-template.md` | arsenal.md 结构模板 + 自动发现逻辑 | Phase 2: 生成 arsenal.md |

### Read Method

```bash
cat {PLUGIN_ROOT}/references/company-template.md
cat {PLUGIN_ROOT}/references/goals-template.md
cat {PLUGIN_ROOT}/references/arsenal-template.md
```

---

## Arguments

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$0` | 公司名称、官网 URL、或自然语言描述 | 交互式询问 |
| `--output` | 输出目录路径 | 交互式询问 |
| `--lang` | 主语言 (zh/en) | zh |

---

## Execution Flow

### Phase 0: 确定输入和输出

**Step 0.1: 解析输入**

检查 `$ARGUMENTS`：
- 如果是 URL → 用 WebFetch 抓取公司信息作为起点
- 如果是公司名称 → 用 WebSearch 搜索基本信息
- 如果是自然语言描述 → 直接作为对话起点
- 如果为空 → 询问："请告诉我你的公司名称、官网地址、或用几句话描述你的公司。"

**Step 0.2: 确定输出路径**

如果 `--output` 未提供，询问：
"公司内核文件输出到哪个目录？（如 `~/company-context/` 或项目内的路径）"

验证并创建目录：
```bash
mkdir -p {output_path}
```

**Step 0.3: 自动发现已有信息**

扫描项目中是否已有可用数据：

```bash
# 检查是否有 BrandProfile 数据
ls {project_root}/**/brand-profile.json 2>/dev/null
ls {project_root}/**/analyzing-company*.md 2>/dev/null

# 检查是否有已有的 marketplace.json
ls {project_root}/**/.claude-plugin/marketplace.json 2>/dev/null

# 检查是否有已安装的 skills
ls ~/.claude/skills/*/SKILL.md 2>/dev/null
```

如果发现已有数据，告知用户并询问是否使用：
"发现已有数据：[列表]。是否基于这些数据生成？"

---

### Phase 1: 信息采集（结构化对话）

**核心原则**：像 CEO 面试一样提问，每轮最多 3-4 个问题，不要一次问完。根据已有信息跳过已知部分。

**Round 1: 身份 + 产品（最核心）**

```
让我先了解你的公司和产品：

1. 你们的核心产品/服务是什么？解决什么问题？
2. 现在处于什么阶段？（有用户了？有收入了？还在开发？）
3. 目标客户是谁？（越具体越好：行业、规模、角色）
```

对每个回答进行追问，直到信息足以填充 Identity + Product + Market 的核心字段。

**Round 2: 定位 + 竞争**

```
接下来聊定位和竞争：

1. 你的客户现在怎么解决这个问题？（竞品或替代方案）
2. 相比他们，你的核心优势是什么？（要机制，不要形容词）
3. 你们明确不做什么？
```

**Round 3: 原则 + 风格**

```
最后几个快速问题：

1. 你们团队做决策时最重要的原则是什么？（例如"速度>完美"）
2. 对外沟通的风格？（正式/轻松/技术/故事化）
3. 有什么绝对不能做的事？（红线）
```

对任何问题用户可以回答 "skip" 或 "不确定"，标记为 `[TODO]`。

**Round 4: 当前目标**

```
现在聊聊当前阶段的目标：

1. 这个季度/月最重要的 1-3 件事是什么？
2. 每件事的成功标准是什么？（怎么算做到了）
3. 最大的风险或阻塞是什么？
```

---

### Phase 2: 生成文件

**Step 2.1: 读取模板**

```bash
cat {PLUGIN_ROOT}/references/company-template.md
cat {PLUGIN_ROOT}/references/goals-template.md
cat {PLUGIN_ROOT}/references/arsenal-template.md
```

**Step 2.2: 生成 company.md**

按 company-template.md 的结构，用 Phase 1 收集的信息填充。规则：
- 有信息的字段直接填写
- 信息不足的标注 `[TODO: 需要补充xxx]`
- 不要编造数据，尤其是经济引擎部分
- 保持简洁，每个 section 不超过 20 行

输出到 `{output_path}/company.md`

**Step 2.3: 生成 goals.md**

按 goals-template.md 的结构填充。规则：
- 如果用户提供了目标，结构化输出
- 如果没有，生成一个 skeleton 模板
- P0 目标不超过 3 个

输出到 `{output_path}/goals.md`

**Step 2.4: 生成 arsenal.md**

按 arsenal-template.md 的结构填充。规则：
- 优先使用 Step 0.3 自动发现的 skills/APIs
- 补充用户提到的工具和服务
- 如果发现 marketplace.json，直接提取 plugin 列表

输出到 `{output_path}/arsenal.md`

---

### Phase 3: 健康检查 + 总结

**Step 3.1: 评估每个文件的完成度**

对照模板中的评估标准，给每个 section 打分：

```
## 公司内核健康报告

| Section | 状态 | 说明 |
|---------|------|------|
| Identity | ✅ 完整 | |
| Product | ⚠️ 部分 | 缺少定价和经济引擎数据 |
| Market | ✅ 完整 | ICP 具体，有 JTBD |
| Position | ⚠️ 部分 | 差异化需要更具体的机制 |
| Landscape | ❌ 缺失 | 没有竞品信息 |
| Principles | ✅ 完整 | |
| Goals | ⚠️ 部分 | 缺少里程碑截止日 |
| Arsenal | ✅ 自动发现 | 从 marketplace.json 提取了 12 个 skills |

完成度: 6/8 sections 合格
```

**Step 3.2: 输出总结**

```
## 生成完成

### 文件列表
- {output_path}/company.md    — 公司全貌（身份+产品+市场+定位+竞品+原则）
- {output_path}/goals.md      — 当前周期目标
- {output_path}/arsenal.md    — 可用能力清单
### 下一步
1. 审查 company.md，补充 [TODO] 标记的缺失信息
2. 确认 goals.md 中的目标和优先级
3. 使用 `/company-pipeline` 开始规划周期

### 迭代建议
- 当 company.md 超过 500 行 → 拆分为独立文件
- 当 arsenal.md 的 skills 超过 20 个 → 升级为目录结构
- 当完成第一个周期 → 归档 goals.md，创建新周期
```

---

## Output Format

每次生成的文件都是标准 Markdown，遵循以下约定：
- H1 = 文件标题（只有一个）
- H2 = 主要 section
- H3 = 子 section
- 列表和表格用于结构化数据
- `[TODO: xxx]` 标记缺失信息
- `> blockquote` 用于元信息（周期、更新日期等）

---

## Usage Examples

### Example 1: 从公司名称开始

```
User: /init-company AcmeCorp AI
Agent: [搜索公司信息 → 引导式对话 → 生成 3 个文件]
```

### Example 2: 从 URL 开始

```
User: /init-company https://acme-corp.example.com --output ~/company-context/
Agent: [抓取网站信息 → 预填充 → 确认补充 → 生成]
```

### Example 3: 从头开始

```
User: /init-company
Agent: 请告诉我你的公司名称、官网地址、或用几句话描述你的公司。
User: 我在做一个 AI 驱动的跨境电商营销工具...
Agent: [引导式对话 → 生成]
```

### Example 4: 利用已有数据

```
User: /init-company --output ./company-context/
Agent: 发现已有数据：
  - writing-workflow/marketplace.json (12 个 skills)
  - analyzing-company 分析报告
  是否基于这些数据生成？
User: 是
Agent: [整合已有数据 + 补充对话 → 生成]
```
