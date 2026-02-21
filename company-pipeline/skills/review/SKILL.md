---
name: company-review
description: "周复盘与月度复盘：收集 git 历史 + tasks 统计，调用 CEO 复盘生成报告，git tag 标记里程碑"
argument-hint: "[公司目录] [--type weekly|monthly]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Company Review — 复盘

> **Path Resolution**: `{PLUGIN_ROOT}` = this plugin's root directory (2 levels up from this SKILL.md). For sibling plugins: `{PLUGIN_ROOT}/../{plugin-name}/`. For shared: `{PLUGIN_ROOT}/../shared/`. Resolve all to absolute paths before executing commands.

周复盘和月度复盘。收集 git 历史和任务统计，调用 CEO 复盘模式生成报告。

## Scripts

| Script | Usage | When |
|--------|-------|------|
| `{PLUGIN_ROOT}/../shared/scripts/tasks-crud.py` | `python tasks-crud.py stats <tasks_file>` | 统计任务数据 |
| `{PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh` | `bash git-safe-commit.sh <dir> <msg> [tag]` | 复盘完成后 |

## 路径变量

- `{company_dir}` = `{output_base}/{company}/`
- `{context_dir}` = `{company_dir}/context/`
- `{plan_dir}` = `{company_dir}/plans/{plan-name}/`
- `{tasks_file}` = `{company_dir}/tasks.jsonl`

---

## 操作 F: 周复盘

**Step F.1**: 选择要复盘的 plan（默认最新的活跃 plan）。

**Step F.2**: 收集 git 历史：

```bash
cd {company_dir}
git tag -l "review/*" --sort=-creatordate | head -1
git log --oneline {last_review_tag}..HEAD
git diff {last_review_tag}..HEAD --stat
```

如果没有之前的 review tag，用 `cycle/{plan_name}` 或 `init` tag 作为基准。

**Step F.3**: 读取 tasks.jsonl，统计本周变化：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py stats {tasks_file} --plan {plan_name}
```

补充统计：本周完成的任务、本周新增的任务、当前阻塞的任务、总体进度。

**Step F.4**: 调用 CEO 复盘：

```
/ceo-review {context_dir} --output {plan_dir} --tasks {tasks_file}
```

CEO 生成复盘报告到 `{company_dir}/reviews/{YYYY}-W{NN}.md`。

**Step F.5**: Git commit + tag：

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "review: week {YYYY}-W{NN}" "review/{YYYY}-W{NN}" "weekly review"
```

→ 返回运营面板

---

## 操作 G: 月度复盘

**Step G.1**: 选择要复盘的周期（默认上一个 cycle tag）。

**Step G.2**: 收集月度统计：

```bash
cd {company_dir}
git diff {prev_cycle_tag}..HEAD --stat
git log --oneline {prev_cycle_tag}..HEAD
```

**Step G.3**: 读取 tasks.jsonl，统计整月数据：

```bash
python {PLUGIN_ROOT}/../shared/scripts/tasks-crud.py stats {tasks_file} --plan {plan_name}
```

补充统计：任务完成率、目标达成率、各维度进度。

**Step G.4**: 调用 CEO 复盘（月度模式）：

```
/ceo-review {context_dir} --output {plan_dir} --tasks {tasks_file}
```

生成 `{company_dir}/reviews/{YYYY-MM}-retro.md`。

**Step G.5**: Git commit + tag：

```bash
bash {PLUGIN_ROOT}/../shared/scripts/git-safe-commit.sh {company_dir} "retro: {YYYY-MM}" "retro/{YYYY-MM}" "monthly retrospective"
```

→ 返回运营面板

---

## Usage Examples

### Example 1: 周复盘

```
User: /company-review
Agent: [git log + tasks 统计 → CEO review → reviews/2026-W11.md → git tag]
```

### Example 2: 月度复盘

```
User: /company-review --type monthly
Agent: [月度 git diff + tasks 统计 → CEO review → reviews/2026-03-retro.md → git tag]
```
