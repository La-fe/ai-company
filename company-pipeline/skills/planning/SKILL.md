---
name: company-planning
description: "规划流水线：新建/继续月度周期、临时计划、CXO 请求 — CEO→CPO→CMO→Roadmap 编排引擎"
argument-hint: "[公司目录] [--type cycle|initiative|request]"
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Company Planning — 规划流水线

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). For sibling plugins: `{PLUGIN_ROOT}/../{plugin-name}/`. For shared: `{PLUGIN_ROOT}/../shared/`. Resolve all to absolute paths before executing commands.

规划编排引擎。支持三种规划类型：月度周期（cycle）、临时计划（initiative）、CXO 请求（request）。

## Progressive Loading

| File                                                  | Content                         | When to Read              |
| ----------------------------------------------------- | ------------------------------- | ------------------------- |
| `{PLUGIN_ROOT}/references/cycle-planning.md`          | 周期规划方法论 + 周计划模板     | 新建 cycle 规划时         |
| `{PLUGIN_ROOT}/references/quantifiable-frameworks.md` | OKR/SMART/漏斗/ROI 等可量化框架 | CEO 任务拆解 + 周计划生成 |

## Scripts

| Script                                               | Usage                                       | When              |
| ---------------------------------------------------- | ------------------------------------------- | ----------------- |
| `{PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh` | `bash git-safe-commit.sh <dir> <msg> [tag]` | 每个 Phase 结束后 |

## 路径变量

- `{company_dir}` = `{output_base}/{company}/`
- `{context_dir}` = `{company_dir}/context/`
- `{plan_dir}` = `{company_dir}/plans/{plan-name}/`
- `{tasks_file}` = `{company_dir}/tasks.jsonl`

---

## 操作 D: 新建规划

**Step D.1**: 选择规划类型：

| 类型       | 说明                                         |
| ---------- | -------------------------------------------- |
| cycle      | 月度周期，全流程 CEO→CPO→CMO→Roadmap→ 周计划 |
| initiative | 临时计划，事件驱动，按需选择 CXO             |
| request    | CXO 请求，单个 CXO 处理单个任务              |

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

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "plan: create {plan_name}"
```

然后按类型进入对应流程。

---

### Cycle 流程 (Phase 1-7)

#### Phase 1: 公司初始化 — `/init-company`

> 仅在 `{context_dir}/company.md` 不存在时执行

**Case A — 已有上下文**: 展示摘要，选择跳过/补充/重新生成。

**Case B — 无上下文**: 调用 `/init-company {$ARGUMENTS} --output {context_dir}`

**⏸️ WAIT**: "公司上下文已就绪。"

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "init: company context" "init" "company core initialized"
```

#### Phase 2: CEO 目标诊断

> 读取 `references/quantifiable-frameworks.md`

调用:

```
/ceo-diagnose {context_dir} --output {plan_dir} --tasks {tasks_file}
```

CEO 读取 context，输出 goals.md 到 plan_dir，追加任务到 tasks.jsonl。

**⏸️ WAIT**: 人工确认主要矛盾 + 评审任务拆解。

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "ceo: goals + tasks — {plan_name}"
```

**收集竞品信息**（为 Phase 3 准备）:

```
CPO 即将进行竞品分析。请提供：
1. 竞品 URL 或名称
2. 你的产品体验/行业洞察
3. 跳过
```

#### Phase 3: CPO 产品拆解

调用（依次执行 3 个 CPO 子技能）:

```
/cpo-analyze {context_dir} {competitors} --output {plan_dir} --depth deep
/cpo-prd {context_dir} --output {plan_dir} --tasks {tasks_file}
/cpo-version {context_dir} --output {plan_dir}
```

CPO 读取公司上下文 + tasks.jsonl 中的任务，输出 prd.md + version-plan.md 到 plan_dir。

竞品分析同步到 `{context_dir}/competitors/`

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "cpo: PRD + version — {plan_name}"
```

#### Phase 4: CMO 增长策略

调用:

```
/cmo-strategy {context_dir} --output {plan_dir} --channel all
```

CMO 读取公司上下文 + version-plan.md，输出 growth-plan.md 到 plan_dir。

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "cmo: growth plan — {plan_name}"
```

#### Phase 5: CEO Roadmap 综合

调用:

```
/ceo-roadmap {context_dir} --output {plan_dir} --tasks {tasks_file}
```

CEO 综合所有产出，生成 roadmap.md，更新 tasks.jsonl 中的 deadline 和 dependencies。

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "ceo: roadmap — {plan_name}"
```

#### Phase 6: 周计划生成（仅 cycle 类型）

> 读取 `references/cycle-planning.md` + `references/quantifiable-frameworks.md`

基于 `roadmap.md` + tasks.jsonl 生成 4 周计划。

**Week 1 — 详细执行（日级别）**: 每天 P0 ≤ 2，按 6 小时算，高认知上午。包含任务/维度/时长/产出物/完成标准表格。

**Week 2-4 — 指标 + 里程碑**: 周目标、关键指标（当前值 → 目标值）、里程碑、风险预判。

**⏸️ WAIT**: 确认第一周计划

输出到 `{plan_dir}/weekly/week-1~4.md`

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "weekly: 4-week plan — {plan_name}"
```

#### Phase 7: 总结

展示文件清单（context/_.md, tasks.jsonl, plans/{name}/_.md, weekly/\*），提示下一步操作。

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "complete: {plan_name} planning" "cycle/{plan_name}" "planning complete"
```

---

### Initiative 流程

不需要跑全套，按需选择 CXO：

```
Step 1: 用户描述背景 + 目标
Step 2: 选择需要的 CXO
Step 3: 按选择依次执行（传入正确的 --output 和 --tasks）
Step 4: 如果多个 CXO → CEO 综合
Step 5: Git commit + 更新 plan.md 状态
```

### Request 流程

单个 CXO 处理单个任务：

```
Step 1: 用户输入想法/需求
Step 2: 路由到指定 CXO
Step 3: CXO 处理 → 输出到 plan_dir
Step 4: Git commit + 更新 plan.md 状态
```

---

### 阶段裁剪

| 模式           | Phase 1 | Phase 2 | Phase 3   | Phase 4   | Phase 5       | Phase 6 |
| -------------- | ------- | ------- | --------- | --------- | ------------- | ------- |
| **cycle**      | ✅      | ✅      | ✅        | ✅        | ✅            | ✅      |
| **initiative** | 跳过    | ✅ 按需 | ✅ 按需   | ✅ 按需   | ✅ 如果多 CXO | 跳过    |
| **request**    | 跳过    | 跳过    | ✅ 单 CXO | ✅ 单 CXO | 跳过          | 跳过    |

---

## 操作 E: 继续/调整已有规划

扫描已有 plans：

```bash
ls -d {company_dir}/plans/*/ 2>/dev/null
```

展示各规划状态（检测 plan.md / prd.md / growth-plan.md / roadmap.md 是否存在）。

**继续**: 检测缺失文件，从下一阶段恢复。

**调整**:

1. `bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "checkpoint: before adjust {phase}"`
2. 重跑指定阶段
3. 不满意 → `git revert HEAD` 回滚

---

## Usage Examples

### Example 1: 月度周期

```
User: /company-planning → cycle
Agent: [Phase 1→7 全流程，每步 git commit，最后 git tag]
```

### Example 2: 临时计划

```
User: /company-planning → initiative
Agent: 描述背景 → 选择 CPO+CMO → 依次执行 → CEO 综合
```

### Example 3: 调整已有规划

```
User: /company-planning → E
Agent: 选择 2026-03 → 调整 Phase 4 CMO → git checkpoint → 重跑
```
