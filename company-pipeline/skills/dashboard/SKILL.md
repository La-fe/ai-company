---
name: company-dashboard
description: "公司运营面板：展示今日任务、更新任务状态、添加想法、调整优先级 — 日常运营的单一入口"
argument-hint: "[公司名称|目录]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Company Dashboard — 运营面板

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). For sibling plugins: `{PLUGIN_ROOT}/../{plugin-name}/`. For shared: `{PLUGIN_ROOT}/../shared/`. Resolve all to absolute paths before executing commands.

日常运营的单一入口。打开即看今日任务，支持：更新任务状态、添加新想法、调整优先级/目标。

所有任务统一存储在 `tasks.jsonl`，所有变更通过 git 自动追踪。

## Progressive Loading

| File | Content | When to Read |
|------|---------|-------------|
| `{PLUGIN_ROOT}/../shared/references/tasks-schema.md` | tasks.jsonl 格式定义 + 字段说明 | 首次操作 tasks.jsonl |

## Scripts

| Script | Usage | When |
|--------|-------|------|
| `{PLUGIN_ROOT}/../shared/scripts/dashboard.py` | `python dashboard.py {company_dir}` | Phase 0: 渲染面板 |
| `{PLUGIN_ROOT}/../shared/scripts/tasks-crud.py` | `python tasks-crud.py <cmd> <tasks_file> [args]` | 操作 A/B/C: 任务 CRUD |
| `{PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh` | `bash git-safe-commit.sh <dir> <msg> [tag]` | 每次变更后 |

---

## 路径变量

- `{company_dir}` = `{output_base}/{company}/`
- `{context_dir}` = `{company_dir}/context/`
- `{tasks_file}` = `{company_dir}/tasks.jsonl`

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
- 新建公司 → 询问名称，创建 `context/` 目录，提示使用 `/company-planning` 新建规划

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

```bash
python {PLUGIN_ROOT}/../shared/scripts/dashboard.py {company_dir}
```

如果 tasks.jsonl 不存在或为空，提示 "暂无任务，使用 `/company-planning` 开始规划"

**Step 0.5: 路由**

| 操作 | 说明 | 路由 |
|------|------|------|
| A | 更新任务 | 本 skill |
| B | 添加任务/想法 | 本 skill |
| C | 调整优先级/目标 | 本 skill |
| D | 新建规划 | → `/company-planning` |
| E | 继续/调整已有规划 | → `/company-planning` |
| F | 周复盘 | → `/company-review` |
| G | 月度复盘 | → `/company-review` |

---

### 操作 A: 更新任务

**Step A.1**: 列出活跃任务：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py list {tasks_file} --status pending,in_progress,blocked
```

**Step A.2**: 用户选择任务和新状态：
- `completed` — 标记完成
- `in_progress` — 开始执行
- `blocked` — 标记阻塞，询问原因写入 notes
- `cancelled` — 取消

**Step A.3**: 更新任务：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py update {tasks_file} --id {task_id} --field status --value {new_status}
```

**Step A.4**: 依赖检查（任务 completed 时）：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py deps {tasks_file} --id {task_id}
```

**Step A.5**: Git commit：

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "{status_verb}: {task_id} {title}"
```

status_verb: completed→"done", in_progress→"wip", blocked→"blocked", cancelled→"cancel"

→ 返回运营面板

---

### 操作 B: 添加任务/想法

**Step B.1**: 询问用户描述任务/想法。

**Step B.2**: 基于描述自动填充字段：
- `id`: 自动生成
- `type`: task 或 todo（根据是否关联 plan 判断）
- `dimension`: 从描述推断（product/growth/tech/ops）
- `priority`: 建议 P1（用户可调整）
- `plan`: 询问关联哪个 plan（可选 null）
- `deadline`: 从 plan 的时间范围推断（用户可调整）
- `status`: pending
- `created` / `updated`: 今天

**Step B.3**: 展示结构化结果，确认后：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py add {tasks_file} --json '{...}'
```

**Step B.4**: Git commit：

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "add: {task_id} {title}"
```

→ 返回运营面板

---

### 操作 C: 调整优先级/目标

**Step C.1**: 展示当前活跃目标和统计：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py stats {tasks_file}
```

选择操作: 1. 调整任务优先级 / 2. 取消任务 / 3. 修改目标 / 4. 新增目标

**Step C.2**: 根据选择执行：

- **调优先级**: 选任务，改 priority 字段
- **取消任务**: 选任务，status→cancelled，检查下游依赖链
  - 如果有任务依赖此任务 → 提醒 "以下任务依赖 [{id}]，需要处理: [列表]"
  - 用户决定：也取消 / 改依赖 / 忽略
- **修改目标**: 编辑对应 plan 下的 goals.md，同步调整 tasks.jsonl 中相关任务
- **新增目标**: 在 goals.md 中追加，然后询问是否需要 CEO 拆解任务

**Step C.3**: Git commit：

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "adjust: {description}"
```

→ 返回运营面板

---

## Usage Examples

### Example 1: 每日检查

```
User: /company-dashboard
Agent: [渲染面板 → 展示今日任务 → 等待操作选择]
User: A
Agent: [列出任务 → 更新 G1-P-01 completed → 解锁 G1-G-01 → git commit]
```

### Example 2: 加新想法

```
User: /company-dashboard → B
Agent: 描述任务:
User: 做一个用户反馈弹窗
Agent: 已创建 [G1-P-04] 用户反馈弹窗 | P1 | product | plan: 2026-03
       → git commit: "add: G1-P-04 用户反馈弹窗"
```

### Example 3: 调整方向

```
User: /company-dashboard → C
Agent: 当前目标: G1 (8/15 done), G2 (2/8 done)
User: G2 目标改为 50 注册，取消 G2-G-03
Agent: 更新 goals.md, tasks.jsonl → git commit
```
