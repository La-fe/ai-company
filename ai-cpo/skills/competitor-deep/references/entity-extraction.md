# 竞品实体提取方法

> 本文档为 cpo-competitor-deep 的参考资料，在 Layer 2（数据模型）执行时加载。
> 提取自 `{PLUGIN_ROOT}/references/data-model-extraction.md` 的竞品实体提取部分。

---

## 为什么要提取数据模型？

竞品的功能列表容易抄，但数据模型反映了**业务本质**。通过提取竞品的实体关系模型，可以发现：
- **行业共识**: 所有竞品都有的实体 = 核心业务概念
- **空白机会**: 没有竞品建模的实体 = 差异化源
- **设计模式**: 实体间的关系反映了业务流程的设计选择

---

## 三种提取方法

### 方法 1: 从 API 文档提取

最准确的方法，适用于有公开 API 的竞品。

```
操作: WebSearch "{竞品名} API documentation" / "{竞品名} developer docs"
提取:
  - API 端点 → 实体名称（/users, /products, /orders → User, Product, Order）
  - 请求/响应字段 → 实体属性
  - 关联 ID 字段 → 实体关系（order.product_id → Order 属于 Product）
  - 批量操作端点 → 实体之间的聚合关系
  - 嵌套资源 → 包含关系（/stores/{id}/products → Store 包含 Product）
```

**提取技巧**：
- API 端点的名词部分 = 实体名称
- RESTful 嵌套层级 = 实体包含关系
- 查询参数中的 filter 字段 = 实体的重要属性
- Webhook 事件名 = 领域事件（order.created → Order 有生命周期）

### 方法 2: 从 UI 界面反推

适用于没有公开 API 的竞品。

```
操作: WebFetch 竞品主要页面 / Read 用户截图
提取:
  - 导航菜单项 → 一级实体（Dashboard, Products, Orders, Customers）
  - 页面中的表格/列表 → 实体属性（列名 = 属性）
  - 详情页中的关联链接 → 实体关系（订单详情页有"客户"链接 → Order 关联 Customer）
  - 表单字段 → 实体的可编辑属性
  - 筛选条件 → 实体的索引属性
  - 侧边栏/面包屑 → 实体层级关系
```

**提取技巧**：
- 顶部导航 = 一级限界上下文
- 左侧菜单 = 上下文内的实体
- 创建/编辑表单的字段 = 实体属性
- 表格列 = 实体的核心展示属性
- 筛选器选项 = 实体的枚举属性或关联实体

### 方法 3: 从定价页面推断

核心洞察：**收费的东西 = 核心实体**。

```
操作: WebFetch 竞品定价页
提取:
  - 套餐限额项 → 核心实体（"最多 10 个项目" → Project 是核心实体）
  - 按量计费项 → 高频实体（"$0.01/次调用" → API Call 是事务实体）
  - 功能差异项 → 增值实体（"高级分析" → Analytics 是增值实体）
  - 存储限额 → 资源实体（"5GB 存储" → File/Media 是资源实体）
  - 团队成员限制 → 协作实体（"最多 3 个成员" → TeamMember 是协作实体）
```

**提取技巧**：
- 定价页的每一行限制 = 一个实体或功能的边界
- "无限" = 不是差异化维度的实体
- "自定义" = 企业级需求的实体
- 价格跳跃最大的层级之间 = 核心付费壁垒

---

## 综合应用策略

通常三种方法组合使用：

```
1. 先查 API 文档（最准确）
   ├── 有 API → 从端点提取实体骨架
   └── 无 API → 跳到 UI 提取

2. 再从 UI 补充（最直观）
   ├── 验证 API 提取的实体是否在 UI 中可见
   └── 补充 API 未暴露的实体（如内部管理功能）

3. 最后用定价页校验（最关键）
   ├── 确认哪些实体在免费层
   ├── 确认哪些实体是付费壁垒
   └── 发现 API/UI 中未突显的实体（如存储、带宽）
```

---

## 实体分类标准

提取完实体后，按以下标准分类：

| 类型 | 定义 | 示例 |
|------|------|------|
| **核心实体** | 产品不能没有的实体，所有竞品都有 | User, Product, Order |
| **辅助实体** | 支撑核心实体运作但不直接面向用户 | Settings, Notification, Log |
| **价值实体** | 承载产品核心价值、用户愿意付费的实体 | AIStrategy, Report, Analytics |
| **事务实体** | 记录一次性交互/事件 | Transaction, Message, APICall |

---

## 实体关系图画法

使用 ASCII 画关系图，标注关系类型：

```
关系符号:
  -1:N->  一对多
  -N:N->  多对多
  ---->   包含/组合
  ....>   依赖/引用

示例:
  User -1:N-> Store -1:N-> Product
                |               |
                |          -1:N-> Variant
                |
           -1:N-> Order -N:N-> Product
                    |
               ---> Payment

  [AI 原生]
  User ----> AISession -1:N-> AIGeneration
                                   |
                              ....> Product (应用生成结果)
```

---

## 参考来源

- 方法论提取自 `data-model-extraction.md`
- DDD (Eric Evans / Martin Fowler)
- Competitive Analysis best practices
