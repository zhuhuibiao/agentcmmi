---
name: ui-designer-component-spec
description: UI设计师组件规范子技能。组件Props、States、代码示例。触发条件：视觉设计完成。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 组件规范 (PPQA)

## 用途
组件Props、States、代码示例。

## 触发时机
视觉设计完成。

## 输入
- 视觉设计规范
- 已有组件库文档

## 输出
```markdown
## 组件规范

### 新增/修改组件

#### XxxCard 卡片组件

**使用场景:**
{描述在什么场景下使用}

**Props:**
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| title | string | - | 卡片标题 |
| extra | slot | - | 标题右侧扩展区 |
| loading | boolean | false | 加载状态 |

**States:**
| State | 视觉表现 |
|-------|---------|
| default | 白色背景，1px边框 #f0f0f0 |
| hover | 边框颜色加深 #d9d9d9 |
| loading | 显示骨架屏 |
| empty | 显示空状态插画 |

**代码示例:**
```vue
<XxxCard title="数据统计" :loading="false">
  <template #extra>
    <el-button size="small">查看更多</el-button>
  </template>
  <!-- 卡片内容 -->
</XxxCard>
```

**禁止事项:**
- 禁止修改卡片内部结构
- 禁止添加与设计文档不一致的样式
```

## 执行步骤

```
1. [PPQA-1] 梳理需要的新组件或组件变体
2. [PPQA-2] 定义组件规范（Props、States、用法）
3. [PPQA-3] 编写组件规范文档
4. [PPQA-4] 更新设计系统文档
```

## 禁止行为
- 禁止定义项目中已有组件的重复变体（除非有明确理由）
- 禁止使用项目组件库不支持的Props