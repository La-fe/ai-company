# Tech Teardown

技术架构深度拆解插件 — 从公开信息逆向工程产品技术架构，或基于概念研究设计技术方案。

## 核心能力

| 模式 | 命令 | 职责 | 输出 |
|------|------|------|------|
| **teardown** | `/tech-teardown url --mode teardown` | 逐竞品 6 层技术拆解 | `competitors/{name}-tech.md` |
| **design** | `/tech-teardown "概念" --mode design` | 基于概念的架构设计 | `design-{concept}.md` |
| **both** | `/tech-teardown url --concept "..." --mode both` | 拆解 + 设计一体化 | 两者皆输出 |

典型工作流：

```
/tech-teardown whop.com stan.store --mode teardown --output ~/analysis/tech/
# 技术拆解完成后 →
/tech-teardown --mode design --concept "我的产品" --output ~/analysis/tech/
```

## 快速开始

拆解竞品技术架构：

```bash
/tech-teardown whop.com --output ~/analysis/tech/
```

基于概念设计技术方案：

```bash
/tech-teardown "AI驱动的内容创作平台" --mode design --output ~/project/tech/
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `$1..N` | 竞品 URL/名称 或 概念描述 | 交互式询问 |
| `--mode` | teardown / design / both | 自动推断 |
| `--concept` | 产品概念（design/both 模式下引导设计） | 无 |
| `--output` | 输出目录 | 交互式询问 |
| `--skip-ai` | 跳过 Layer 6 AI 管线分析 | false |

## 分析深度

6 层分析（teardown 模式）：

1. **问题空间** — 目标用户、JTBD、技术需求、非功能性约束
2. **架构研究** — 技术栈识别、架构模式判断、部署拓扑推测
3. **方案调研** — 搜索已有开源方案/SaaS/SDK，评估 Build vs Buy
4. **系统组件** — 核心组件拆解（职责、接口、依赖）+ 组件交互图
5. **技术流程** — 关键数据流 + 控制流 ASCII 图、性能瓶颈识别
6. **AI 管线** — AI 功能管线拆解（模型选型、输入输出、质量线、降级方案）

## 与其他插件的关系

| 维度 | `/tech-teardown` | `/teardown`（competitor） | `/cpo-feature-design` |
|------|-------------------|---------------------------|----------------------|
| 视角 | 技术架构 | 产品/商业 | 自身产品设计 |
| 输入 | 竞品 URL / 概念 | 竞品 URL / 素材 | 竞品档案 + landscape |
| 输出 | 技术架构档案 | 产品竞品档案 | feature-spec.md |

技术拆解档案可作为 `cpo-feature-design` 的技术约束输入，与产品竞品档案互补。
