# Competitor Teardown

竞品深度拆解插件 — 从公开信息逆向工程竞品的产品架构。

## 两个 Skill

| Skill | 命令 | 职责 | 输出 |
|-------|------|------|------|
| **teardown** | `/teardown` | 逐竞品五层深度分析 | `competitors/{name}.md` |
| **landscape** | `/teardown-landscape` | 跨竞品模式提炼（≥2 竞品时） | `landscape.md` |

典型工作流：

```
/teardown whop.com stan.store durable.co --output ~/analysis/
# 每竞品 5 层分析完成后 →
/teardown-landscape --input ~/analysis/ --concept "我的产品概念"
# 综合分析完成后 →
/cpo-feature-design ~/project/context/ --mode design
```

## 快速开始

单竞品：

```bash
/teardown whop.com --output ~/analysis/
```

多竞品 + 综合：

```bash
/teardown whop.com stan.store durable.co --output ~/analysis/
/teardown-landscape --input ~/analysis/
```

## 参数

### /teardown

| 参数 | 说明 |
|------|------|
| `$1..N` | 竞品 URL 或名称 |
| `--materials PATH` | 截图/笔记素材目录 |
| `--existing PATH...` | 已有竞品档案 |
| `--output PATH` | 输出目录 |
| `--skip-ai` | 跳过 AI 合约提取 |

### /teardown-landscape

| 参数 | 说明 |
|------|------|
| `--input PATH` | 竞品档案目录（含 competitors/*.md） |
| `--concept TEXT` | 产品概念（用于输出"对自身启示"） |
| `--output PATH` | 输出目录 |

## 分析深度

每个竞品 5 层分析（`/teardown`）：

1. **问题空间** — 具体用户画像、JTBD、触发场景、替代方案、关键指标
2. **数据模型** — 实体四类分类 + 标准化关系图 + 3-5核心实体字段定义
3. **用户旅程** — 旅程表(步骤×实体×CRUD) + ASCII流程图(分叉/循环) + TTFV
4. **AI合约** — 逐AI功能合约提取(输入/输出/质量线/降级) + HITL设计 + 确认点密度
5. **Feature+商业** — Feature目录 + 定价模型(模式+层级+实体边界) + 留存机制 + 设计决策推理

跨竞品综合（`/teardown-landscape`）：

- 实体共性矩阵 + 架构模式 + AI合约对比 + 定价/留存对比 + 空白机会
- 可选：带 `--concept` 输出对自身产品的结构化启示

## 与 cpo 的关系

| 维度 | `/teardown` | `/teardown-landscape` | `/cpo-feature-design` |
|------|-------------|----------------------|-----------------------|
| 职责 | 逐竞品拆解 | 跨竞品综合 | 自身产品设计 |
| 输入 | 竞品 URL/素材 | competitors/*.md | competitors/*.md + landscape.md |
| 输出 | competitors/{name}.md | landscape.md | feature-spec.md |

`competitors/*.md` + `landscape.md` 是 `cpo-feature-design` Phase 3 的直接输入。
