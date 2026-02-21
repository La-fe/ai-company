# tasks.jsonl Schema

> 中央任务仓库格式定义。所有 CXO 技能共用此格式。

## 位置

`{company_dir}/tasks.jsonl` — 公司根目录，跨 plan 共享。

## 格式

每行一个 JSON 对象，每个对象代表一个任务或待办：

```jsonl
{"id":"G1-P-01","title":"完成落地页开发","type":"task","dimension":"product","priority":"P0","owner":"CPO","plan":"2026-03","goal":"G1","deadline":"2026-03-15","success_criteria":"页面上线，3 个核心 section 可访问","dependencies":[],"status":"pending","notes":"","created":"2026-03-01","updated":"2026-03-01"}
```

## 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 唯一标识。规划任务: `G{goal}-{D}-{seq}` (如 G1-P-01)；待办: `T-{seq}` (如 T-001) |
| `title` | string | 是 | 任务标题，动词开头 |
| `type` | string | 是 | `task`（规划任务）或 `todo`（日常杂事） |
| `dimension` | string | 是 | `product` / `growth` / `tech` / `ops` |
| `priority` | string | 是 | `P0`（必须做）/ `P1`（应该做）/ `P2`（可以做） |
| `owner` | string | 否 | 负责角色: CEO / CPO / CMO / CTO / COO |
| `plan` | string | 否 | 关联的 plan 名称（如 "2026-03"），null 表示不属于任何 plan |
| `goal` | string | 否 | 关联的目标 ID（如 "G1"），null 表示独立任务 |
| `deadline` | string | 是 | 截止日期，YYYY-MM-DD 格式 |
| `success_criteria` | string | 否 | 可衡量的成功标准 |
| `dependencies` | array | 是 | 依赖的任务 ID 列表，空数组 `[]` 表示无依赖 |
| `status` | string | 是 | `pending` / `in_progress` / `completed` / `blocked` / `cancelled` |
| `notes` | string | 否 | 备注（阻塞原因、进展记录等） |
| `created` | string | 是 | 创建日期 YYYY-MM-DD |
| `updated` | string | 是 | 最后更新日期 YYYY-MM-DD |

## ID 命名规则

**规划任务** (type=task):
- 格式: `G{goal_num}-{dimension_initial}-{seq}`
- dimension_initial: P(product) / G(growth) / T(tech) / O(ops)
- 示例: `G1-P-01`, `G2-G-03`, `G1-T-02`

**日常待办** (type=todo):
- 格式: `T-{seq}`
- 示例: `T-001`, `T-042`

## 状态流转

```
pending → in_progress → completed
                      → blocked → in_progress → completed
pending → cancelled
in_progress → cancelled
```

## 读取方法

AI Agent 读取 tasks.jsonl 时，逐行解析 JSON。常见过滤逻辑：

**今日任务**:
```
读取 tasks.jsonl，筛选: deadline <= 今天 且 status 为 pending 或 in_progress
按 priority 排序: P0 > P1 > P2
```

**本周任务**:
```
读取 tasks.jsonl，筛选: deadline 在本周范围内 且 status 不为 completed/cancelled
```

**某个 plan 的任务**:
```
读取 tasks.jsonl，筛选: plan == "{plan_name}"
```

**检查依赖解锁**:
```
当任务 X completed 时，找出所有 dependencies 包含 X.id 的任务
如果这些任务的 所有 dependencies 都已 completed → 该任务可以开始
```

## 写入方法

**追加新任务**: 在文件末尾新增一行 JSON

**更新任务**: 读取整个文件，修改目标行的字段（status/notes/updated/priority 等），重写整个文件

**批量写入**（CEO 任务拆解）: 一次追加多行，每行一个任务 JSON

## Git Commit 规范

每次修改 tasks.jsonl 后由 pipeline 统一 commit:

- 完成任务: `done: {task_id} {title}`
- 新增任务: `add: {task_id} {title}`
- 开始任务: `wip: {task_id} {title}`
- 阻塞: `blocked: {task_id} {title}`
- 取消: `cancel: {task_id} {title}`
- 批量操作: `ceo: goals + tasks — {plan_name}`
- 调整: `adjust: {description}`
