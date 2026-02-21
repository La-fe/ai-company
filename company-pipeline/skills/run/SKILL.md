---
name: company-pipeline
description: "公司运营中心：日常任务管理 + 规划流水线 + 周期复盘 — 通过 tasks.jsonl + git 管理公司全生命周期"
argument-hint: "[公司名称|URL|目录] [--type cycle|initiative|request]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Company Pipeline — 公司运营中心

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). For sibling plugins: `{PLUGIN_ROOT}/../{plugin-name}/`. Resolve all `{PLUGIN_ROOT}` to absolute paths before executing commands.

日常运营的单一入口。打开即看今日任务，支持：更新任务状态、添加新想法、调整目标、启动规划流水线、周/月复盘。

所有任务统一存储在 `tasks.jsonl`，所有变更通过 git 自动追踪。

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `{PLUGIN_ROOT}/../shared/references/tasks-schema.md` | tasks.jsonl 格式定义 + 字段说明 | Phase 0: 首次操作 tasks.jsonl |
| `references/cycle-planning.md` | 周期规划方法论 + 周计划模板 | 操作 D: 新建规划 |
| `references/quantifiable-frameworks.md` | OKR/SMART/漏斗/ROI 等可量化框架 | 操作 D: CEO 任务拆解 |

---

## 核心数据

**tasks.jsonl** — 中央任务仓库，位于 `{company_dir}/tasks.jsonl`。

每行一个 JSON 对象，格式参考 `references/tasks-schema.md`。所有 CXO 技能共用此文件。

---

## 输出目录结构

```
{output_base}/{company}/                     # 独立 git 仓库
│
├── .git/                                # git 版本管理
├── .gitignore                           # 排除 *.bak, *.tmp, .DS_Store
├── tasks.jsonl                          # 中央任务仓库（跨 plan 共享）
│
├── context/                              # 共性层：公司 DNA
│   ├── company.md                        # 身份/产品/市场/定位（季度更新）
│   ├── arsenal.md                        # 武器库（新 skill 时更新）
│   └── competitors/                      # 竞品档案（持续积累）
│       └── {competitor}.md
│
├── plans/                                # 规划层：每个子目录 = 一个 plan
│   ├── 2026-03/                          # 月度周期
│   │   ├── plan.md                       # 元信息入口
│   │   ├── goals.md                      # 本周期目标
│   │   ├── prd.md                        # CPO PRD
│   │   ├── version-plan.md              # CPO 版本规划
│   │   ├── growth-plan.md               # CMO 增长策略
│   │   ├── roadmap.md                    # CEO Roadmap
│   │   └── weekly/
│   │       ├── week-1.md
│   │       ├── week-2.md
│   │       ├── week-3.md
│   │       └── week-4.md
│   │
│   ├── 2026-03-15-competitor-response/   # 临时计划
│   │   ├── plan.md
│   │   └── prd.md
│   │
│   └── 2026-03-20-new-feature/           # CXO 请求
│       ├── plan.md
│       └── prd.md
│
└── reviews/                              # 复盘记录
    ├── 2026-W10.md                       # 周复盘
    └── 2026-03-retro.md                  # 月度复盘
```

**路径变量**:
- `{company_dir}` = `{output_base}/{company}/`
- `{context_dir}` = `{company_dir}/context/`
- `{plan_dir}` = `{company_dir}/plans/{plan-name}/`
- `{tasks_file}` = `{company_dir}/tasks.jsonl`

---

## Git 安全写法

所有 git 操作使用以下模式，避免空提交报错：

```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "{message}"
fi
```

**Tag 约定**:
- `init` — 公司初始化完成
- `cycle/{YYYY-MM}` — 月度周期规划完成
- `review/{YYYY}-W{NN}` — 周复盘
- `retro/{YYYY-MM}` — 月度复盘

---

## Workflow

### Phase 0: 运营面板

**Step 0.1: 确定工作空间**

```bash
cat {PLUGIN_ROOT}/config.yaml
```

- Config 存在 → Step 0.2
- Config 不存在 → 询问 `output_base`，保存到 config.yaml

**Step 0.2: 选择公司**

```bash
ls {output_base}/*/context/company.md 2>/dev/null
```

- 已有公司 → 设 `company_dir`，Step 0.3
- 新建公司 → 询问名称，创建 `context/` 目录，进入操作 D

**Step 0.3: 确保 Git 仓库**

```bash
cd {company_dir}
git rev-parse --git-dir 2>/dev/null || {
  git init
  printf "*.bak\n*.tmp\n.DS_Store\n" > .gitignore
  git add .gitignore && git commit -m "chore: init repo"
}
```

**Step 0.4: 展示运营面板**

读取 `{tasks_file}` 和 git 状态，展示：

```
{company_name} | {today_date} {weekday} | git: {commit_count} commits, tag: {latest_tag}

今日任务:
  P0: [{id}] {title} — {status} — deadline {deadline}
      依赖: {deps} | 阻塞: {blocked_by_this}
  P1: [{id}] {title} — {status} — deadline {deadline}

本周进度: {done}/{total} done ({percent}%) | {blocked} blocked

操作:
  A. 更新任务      B. 添加任务/想法    C. 调整优先级/目标
  D. 新建规划      E. 继续/调整已有规划
  F. 周复盘        G. 月度复盘
```

过滤逻辑：
- 今日任务 = tasks.jsonl 中 deadline <= 今天 且 status 为 pending/in_progress 的任务
- 本周进度 = 本周范围内所有任务的完成统计
- 如果 tasks.jsonl 不存在或为空，提示 "暂无任务，选择 D 开始规划"

**Step 0.5: 路由**

根据用户选择路由到对应操作。

---

### 操作 A: 更新任务

> 读取 `references/tasks-schema.md`

**Step A.1**: 列出 status 为 pending / in_progress / blocked 的任务，按 priority 排序。

**Step A.2**: 用户选择任务和新状态：
- `completed` — 标记完成
- `in_progress` — 开始执行
- `blocked` — 标记阻塞，询问原因写入 notes
- `cancelled` — 取消

**Step A.3**: 更新 tasks.jsonl 中该任务的 status 和 updated 字段。

**Step A.4**: 依赖检查：
- 如果任务 completed → 检查 tasks.jsonl 中所有 dependencies 包含此 task id 的任务
- 如果这些下游任务的所有 dependencies 都已 completed → 通知 "解锁: [{id}] {title} 现在可以开始"

**Step A.5**: Git commit：
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "{status_verb}: {task_id} {title}"
fi
```

status_verb 对照: completed→"done", in_progress→"wip", blocked→"blocked", cancelled→"cancel"

→ 返回运营面板

---

### 操作 B: 添加任务/想法

**Step B.1**: 询问用户：
```
描述你的任务/想法，我来结构化:
```

**Step B.2**: 基于描述自动填充字段：
- `id`: 自动生成（读取 tasks.jsonl 推断下一个序号）
- `type`: task 或 todo（根据是否关联 plan 判断）
- `dimension`: 从描述推断（product/growth/tech/ops）
- `priority`: 建议 P1（用户可调整）
- `plan`: 询问关联哪个 plan（可选 null）
- `deadline`: 从 plan 的时间范围推断（用户可调整）
- `status`: pending
- `created` / `updated`: 今天

**Step B.3**: 展示结构化结果，确认后追加到 tasks.jsonl。

**Step B.4**: Git commit：
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "add: {task_id} {title}"
fi
```

→ 返回运营面板

---

### 操作 C: 调整优先级/目标

**Step C.1**: 展示当前活跃目标和统计：
```
当前活跃目标:
  1. [G1] {goal_title} — {done}/{total} tasks done
  2. [G2] {goal_title} — {done}/{total} tasks done

独立待办: {pending_todos} 个

选择操作:
  1. 调整任务优先级
  2. 取消任务
  3. 修改目标
  4. 新增目标
```

**Step C.2**: 根据选择执行：

- **调优先级**: 选任务，改 priority 字段
- **取消任务**: 选任务，status→cancelled，检查下游依赖链
  - 如果有任务依赖此任务 → 提醒 "以下任务依赖 [{id}]，需要处理: [列表]"
  - 用户决定：也取消 / 改依赖 / 忽略
- **修改目标**: 编辑对应 plan 下的 goals.md，同步调整 tasks.jsonl 中相关任务的 goal/deadline
- **新增目标**: 在 goals.md 中追加，然后询问是否需要 CEO 拆解任务

**Step C.3**: Git commit：
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "adjust: {description}"
fi
```

→ 返回运营面板

---

### 操作 D: 新建规划

> 读取 `references/cycle-planning.md`

**Step D.1**: 选择规划类型：

| 类型 | 说明 |
|------|------|
| cycle | 月度周期，全流程 CEO→CPO→CMO→Roadmap→周计划 |
| initiative | 临时计划，事件驱动，按需选择 CXO |
| request | CXO 请求，单个 CXO 处理单个任务 |

**Step D.2**: 初始化 plan 目录：

```bash
mkdir -p {plan_dir}
mkdir -p {plan_dir}/weekly  # 仅 cycle 类型
mkdir -p {company_dir}/reviews
```

生成 `plan.md`：

```markdown
# Plan — {名称}

> 类型: cycle | initiative | request
> 创建: YYYY-MM-DD
> 状态: planning
> 紧急度: P0

## 目标
{一句话}

## 触发
{什么事件/输入触发了这个计划}

## CXO 处理链
- [ ] CEO: 目标拆解
- [ ] CPO: PRD 生成
- [ ] CMO: 增长策略
```

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "plan: create {plan_name}"
fi
```

然后按类型进入对应流程。

---

#### Cycle 流程 (D → Phase 1-7)

##### Phase 1: 公司初始化 — `/init-company`

> 仅在 `{context_dir}/company.md` 不存在时执行

**Case A — 已有上下文**: 展示摘要，选择跳过/补充/重新生成。

**Case B — 无上下文**: 调用 `/init-company {$ARGUMENTS} --output {context_dir}`

**⏸️ WAIT**: "公司上下文已就绪。"

更新 `plan.md`: Phase 1 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "init: company context"
fi
git tag -f "init" -m "company core initialized"
```

##### Phase 2: CEO 目标诊断

> 读取 `references/quantifiable-frameworks.md`

调用:
```
/ceo-plan {context_dir} --output {plan_dir} --tasks {tasks_file} --mode plan
```

CEO 读取 context，输出 goals.md 到 plan_dir，追加任务到 tasks.jsonl。

**⏸️ WAIT**: 人工确认主要矛盾 + 评审任务拆解。

更新 `plan.md`: Phase 2 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "ceo: goals + tasks — {plan_name}"
fi
```

**收集竞品信息**（为 Phase 3 准备）:
```
CPO 即将进行竞品分析。请提供：
1. 竞品 URL 或名称
2. 你的产品体验/行业洞察
3. 跳过
```

##### Phase 3: CPO 产品拆解

调用:
```
/cpo-plan {context_dir} {competitors} --output {plan_dir} --tasks {tasks_file} --depth deep
```

CPO 读取公司上下文 + tasks.jsonl 中的任务，输出 prd.md + version-plan.md 到 plan_dir。

竞品分析同步到 `{context_dir}/competitors/`

更新 `plan.md`: Phase 3 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "cpo: PRD + version — {plan_name}"
fi
```

##### Phase 4: CMO 增长策略

调用:
```
/cmo-plan {context_dir} --output {plan_dir} --channel all
```

CMO 读取公司上下文 + version-plan.md，输出 growth-plan.md 到 plan_dir。

更新 `plan.md`: Phase 4 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "cmo: growth plan — {plan_name}"
fi
```

##### Phase 5: CEO Roadmap 综合

调用:
```
/ceo-plan {context_dir} --output {plan_dir} --tasks {tasks_file} --mode roadmap
```

CEO 综合所有产出，生成 roadmap.md，更新 tasks.jsonl 中的 deadline 和 dependencies。

更新 `plan.md`: Phase 5 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "ceo: roadmap — {plan_name}"
fi
```

##### Phase 6: 周计划生成（仅 cycle 类型）

> 读取 `references/cycle-planning.md` + `references/quantifiable-frameworks.md`

基于 `roadmap.md` + tasks.jsonl 生成 4 周计划。

**Week 1 — 详细执行（日级别）**:

```markdown
# Week 1 — {日期范围}

## 本周关键指标
- [ ] {指标 1}: 基线 → 目标值

## Day 1 — {日期}
**核心目标**: {最重要的 1 件事}
| 任务 | 维度 | 时长 | 产出物 | 完成标准 |
|------|------|------|--------|---------|
```

规则: 每天 P0 ≤ 2，按 6 小时算，高认知上午

**Week 2-4 — 指标 + 里程碑**:

```markdown
# Week {N} — {日期范围}

## 周目标
{一句话}

## 关键指标
- [ ] {指标}: 当前值 → 目标值

## 里程碑
- [ ] {里程碑} — 负责人 — 截止日

## 风险预判
- {可能阻塞的事项}
```

**⏸️ WAIT**: 确认第一周计划

输出到 `{plan_dir}/weekly/week-1~4.md`
更新 `plan.md`: Phase 6 ✅

**Git Checkpoint**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "weekly: 4-week plan — {plan_name}"
fi
```

##### Phase 7: 总结

```markdown
## 规划完成 — {company} / {plan_name}

### 文件清单
| 层级 | 文件 | 内容 |
|------|------|------|
| 共性 | context/company.md | 公司 DNA |
| 共性 | context/arsenal.md | 武器库 |
| 共性 | context/competitors/*.md | 竞品档案 |
| 任务 | tasks.jsonl | 所有任务（跨 plan） |
| 规划 | plans/{name}/plan.md | 规划入口 |
| 规划 | plans/{name}/goals.md | 目标 |
| 规划 | plans/{name}/prd.md | PRD |
| 规划 | plans/{name}/growth-plan.md | 增长策略 |
| 规划 | plans/{name}/roadmap.md | Roadmap |
| 周级 | plans/{name}/weekly/* | 周计划 |

### 下一步
1. 按 `weekly/week-1.md` 执行
2. 每天: `/company-pipeline` → A. 更新任务
3. 每周: `/company-pipeline` → F. 周复盘
4. 月底: `/company-pipeline` → G. 月度复盘
```

**Git Tag**:
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "complete: {plan_name} planning"
fi
git tag "cycle/{plan_name}" -m "planning complete"
```

---

#### Initiative 流程

不需要跑全套，按需选择 CXO：

```
Step 1: 用户描述背景 + 目标
Step 2: 选择需要的 CXO
Step 3: 按选择依次执行（传入正确的 --output 和 --tasks）
Step 4: 如果多个 CXO → CEO 综合
Step 5: Git commit + 更新 plan.md 状态
```

#### Request 流程

单个 CXO 处理单个任务：

```
Step 1: 用户输入想法/需求
Step 2: 路由到指定 CXO
Step 3: CXO 处理 → 输出到 plan_dir
Step 4: Git commit + 更新 plan.md 状态
```

---

### 操作 E: 继续/调整已有规划

扫描已有 plans：
```bash
ls -d {company_dir}/plans/*/ 2>/dev/null
```

展示：
```
已有规划:
  1. 2026-03 (cycle) — roadmap ✅ prd ✅ growth-plan ❌
  2. 2026-03-15-competitor-response (initiative) — prd ✅

操作:
  1. 继续未完成的规划 — 检测缺失文件，从下一阶段恢复
  2. 调整已有阶段 — git commit 快照当前状态，重跑指定阶段
```

**调整流程**:
1. `git commit` 快照当前状态：`"checkpoint: before adjust {phase}"`
2. 重跑指定阶段
3. 不满意 → `git revert HEAD` 回滚

---

### 操作 F: 周复盘

**Step F.1**: 选择要复盘的 plan（默认最新的活跃 plan）。

**Step F.2**: 收集 git 历史：

```bash
cd {company_dir}
# 找最近的 review tag
git tag -l "review/*" --sort=-creatordate | head -1
# 从上次 review 到现在的变更
git log --oneline {last_review_tag}..HEAD
git diff {last_review_tag}..HEAD --stat
```

如果没有之前的 review tag，用 `cycle/{plan_name}` 或 `init` tag 作为基准。

**Step F.3**: 读取 tasks.jsonl，统计本周变化：
- 本周完成的任务
- 本周新增的任务
- 当前阻塞的任务
- 总体进度

**Step F.4**: 调用 CEO 复盘：
```
/ceo-plan {context_dir} --output {plan_dir} --tasks {tasks_file} --mode review
```

CEO 生成复盘报告到 `{company_dir}/reviews/{YYYY}-W{NN}.md`。

**Step F.5**: Git commit + tag：
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "review: week {YYYY}-W{NN}"
fi
git tag "review/{YYYY}-W{NN}" -m "weekly review"
```

→ 返回运营面板

---

### 操作 G: 月度复盘

**Step G.1**: 选择要复盘的周期（默认上一个 cycle tag）。

**Step G.2**: 收集月度统计：

```bash
cd {company_dir}
git diff {prev_cycle_tag}..HEAD --stat
git log --oneline {prev_cycle_tag}..HEAD
```

**Step G.3**: 读取 tasks.jsonl，统计整月数据：
- 任务完成率
- 目标达成率
- 各维度进度

**Step G.4**: 调用 CEO 复盘（月度模式）：
```
/ceo-plan {context_dir} --output {plan_dir} --tasks {tasks_file} --mode review
```

生成 `{company_dir}/reviews/{YYYY-MM}-retro.md`。

**Step G.5**: Git commit + tag：
```bash
cd {company_dir}
if [ -n "$(git status --porcelain)" ]; then
  git add -A && git commit -m "retro: {YYYY-MM}"
fi
git tag "retro/{YYYY-MM}" -m "monthly retrospective"
```

→ 返回运营面板

---

## 阶段裁剪（Initiative / Request）

| 模式 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|------|---------|---------|---------|---------|---------|---------|
| **cycle** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **initiative** | 跳过 | ✅ 按需 | ✅ 按需 | ✅ 按需 | ✅ 如果多 CXO | 跳过 |
| **request** | 跳过 | 跳过 | ✅ 单 CXO | ✅ 单 CXO | 跳过 | 跳过 |

---

## Usage Examples

### Example 1: 每日检查（最常用）

```
User: /company-pipeline
Agent:
  AcmeCorp | 2026-03-15 周六 | git: 18 commits, tag: cycle/2026-02

  今日任务:
    P0: [G1-P-01] 完成落地页开发 — in_progress — deadline 今天
    P1: [G1-T-02] 配置 CI/CD — pending — deadline 3/17

  本周进度: 5/12 done (42%) | 2 blocked

  操作: A-G
User: A
Agent: [更新任务 → G1-P-01 completed → 解锁 G1-G-01 → git commit]
```

### Example 2: 加新想法

```
User: /company-pipeline → B
Agent: 描述任务:
User: 做一个用户反馈弹窗
Agent: 已创建 [G1-P-04] 用户反馈弹窗 | P1 | product | plan: 2026-03
       → git commit: "add: G1-P-04 用户反馈弹窗"
```

### Example 3: 调整方向

```
User: /company-pipeline → C
Agent: 当前目标: G1 (8/15 done), G2 (2/8 done)
User: G2 目标改为 50 注册，取消 G2-G-03
Agent: 更新 goals.md, tasks.jsonl
       依赖提醒: G2-G-04 依赖 G2-G-03
       → git commit: "adjust: G2 target 100->50, cancel G2-G-03"
```

### Example 4: 月度周期（从零开始）

```
User: /company-pipeline → D → cycle
Agent: [Phase 1→7 全流程，每步 git commit，最后 git tag]
```

### Example 5: 调整已有规划

```
User: /company-pipeline → E
Agent: 选择 2026-03 → 调整 Phase 4 CMO
       git commit 快照
       [重跑 CMO → 重跑 Roadmap]
       （不满意？git revert HEAD 回滚）
```

### Example 6: 周复盘

```
User: /company-pipeline → F
Agent: [git log + tasks 统计 → CEO review → reviews/2026-W11.md → git tag]
```

---

## Notes

1. **tasks.jsonl 是唯一事实来源**: 所有任务状态都在这一个文件中，CXO 技能读写同一个文件
2. **context/ 跨规划持久化**: company.md 和 arsenal.md 不属于任何规划，所有规划共享
3. **competitors/ 持续积累**: CPO 每次竞品分析的结果同步到 context/competitors/
4. **每个 plan 是一个文件夹**: plans/ 下每个子目录是一个独立规划单元
5. **reviews/ 独立于 plan**: 方便跨周期对比
6. **Git 管理**: 公司目录是独立 git 仓库，每次操作自动 commit，里程碑打 tag。`git log --oneline` = 公司运营日志
7. **CXO 路径分离**: 所有 CXO 技能通过 `--output` 分离读（context/）和写（plans/），通过 `--tasks` 共享 tasks.jsonl
