---
name: ui-designer-visual-design
description: UI设计师视觉设计子技能。设计Token、布局、样式。触发条件：交互设计完成。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 视觉设计 (PPQA)

## 用途
设计Token、布局、样式。

## 触发时机
交互设计完成。

## 输入
- 交互设计方案
- 项目设计Token
- 已有组件库

## 输出
```markdown
## 视觉设计规范

### 设计 Token（严格使用项目已有值）
| Token | 值 | 用途 |
|-------|-----|------|
| 颜色.primary | #1890ff | 主按钮、重点强调 |
| 颜色.success | #52c41a | 成功状态 |
| 颜色.warning | #faad14 | 警告状态 |
| 颜色.error | #ff4d4f | 错误状态 |
| 颜色.text | #262626 | 主文本 |
| 颜色.textSecondary | #8c8c8c | 次要文本 |
| 间距.xs | 4px | 紧凑间距 |
| 间距.sm | 8px | 小间距 |
| 间距.md | 16px | 标准间距 |
| 间距.lg | 24px | 大间距 |
| 圆角.sm | 4px | 小组件圆角 |
| 圆角.md | 8px | 按钮/卡片圆角 |
| 字体大小.sm | 12px | 辅助文字 |
| 字体大小.md | 14px | 正文 |
| 字体大小.lg | 16px | 标题 |

### 组件使用
| 组件 | 来源 | 变体/状态 |
|------|------|---------|
| Button | Element Plus | primary/success/danger, default/disabled/loading |
| Table | Element Plus | stripe/border, pagination |
| Form | Element Plus | inline/vertical, validation |
| Modal | Element Plus | basic/confirm/alert |

### 页面设计（文字描述）
```markdown
## 页面A设计

### 布局
- 宽度: 100%, max-width 1200px, 居中
- 内边距: 24px
- 背景色: #f5f5f5

### 区块1: 标题栏
- 标题: h1, 24px, #262626
- 副标题: p, 14px, #8c8c8c
- 操作按钮: 右对齐, primary按钮
```
```

## 执行步骤

```
1. [PPQA-1] 应用项目设计 Token（颜色、字体、间距）
2. [PPQA-2] 选择合适的已有组件
3. [PPQA-3] 定义组件变体和状态样式
4. [PPQA-4] 进行视觉走查
5. [PPQA-5] 输出《视觉设计规范》
```

## 禁止行为
- 禁止使用项目已有的设计 Token 之外的颜色
- 禁止引入新的视觉语言