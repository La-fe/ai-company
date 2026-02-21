# Arsenal Template

生成 `arsenal.md` 时按以下结构填充。一个文件列出所有可用能力。

---

## 结构定义

```markdown
# Arsenal（武器库）

> 更新: {YYYY-MM-DD}
> 能力总数: {N} 个

## Skills（Agent 技能）

| 技能 | 触发命令 | 描述 | 状态 |
|------|---------|------|------|
| 选题研究 | /find-topic | 病毒式选题挖掘 | active |
| 中文写作 | /write | 爆款长文创作 | active |
| 内容评估 | /eval | 7 维度质量评分 | active |
| ... | ... | ... | ... |

## APIs（外部接口）

| 服务 | 用途 | 状态 | 备注 |
|------|------|------|------|
| Twitter API | 内容发布 + 数据抓取 | active | |
| OpenAI API | 图片生成 | active | |
| ... | ... | ... | ... |

## SOPs（标准流程）

| 流程 | 描述 | 文件路径 | 状态 |
|------|------|---------|------|
| 内容发布流水线 | 从选题到多平台发布 | /article-pipeline | active |
| 冷启动方案 | 新渠道冷启动 | /sops/cold-start.md | draft |
| ... | ... | ... | ... |

## Tools（工具和服务）

| 工具 | 用途 | 类型 |
|------|------|------|
| GitHub | 代码管理 + Issue 跟踪 | platform |
| Claude Code | AI 编程 | tool |
| ... | ... | ... |
```

---

## 自动发现

如果用户项目中已有 `.claude-plugin/marketplace.json` 或 `skills/` 目录，优先从中提取 skill 列表，而非手动输入。

扫描路径：
1. 当前项目的 `.claude-plugin/marketplace.json`
2. `~/.claude/skills/` 目录
3. 项目内的 `**/skills/**/SKILL.md`

## 质量评估

| 标准 | 合格 | 不合格 |
|------|------|--------|
| 完整性 | 每个能力有描述和状态 | 只有名字没有说明 |
| 状态准确 | active/beta/deprecated 标注清楚 | 全标 active 但实际有不可用的 |
| 可发现 | 有触发命令或路径 | 只知道名字不知道怎么调用 |
