---
name: architect-tool-intake
description: 架构师需求接收子技能。接收产品需求，提取工具定义，输出工具定义JSON。触发条件：收到新工具需求时。
version: 1.0.0
cmmi_process_area: RD
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 需求接收 (RD)

## 用途
接收产品需求，提取工具定义，输出工具定义JSON。

## 输入
- 产品需求描述（用户/产品提供）

## 输出
```json
{
  "tool_key": "工具英文标识",
  "tool_name": "工具中文名称",
  "group": "工具组英文标识",
  "features": ["功能1", "功能2", ...],
  "assumptions": ["假设1", "假设2"],
  "open_questions": ["问题1", "问题2"]
}
```

## 执行步骤

```
1. [RD-1] 读取产品需求描述
2. [RD-2] 提取工具基本信息:
   - tool_key: 工具英文标识（kebab-case）
   - tool_name: 工具中文名称
   - group: 工具组英文标识
3. [RD-3] 列出假设条件:
   ASSUMPTIONS I'M MAKING:
   1. [假设1]
   2. [假设2]
   → Correct me now or I'll proceed with these.
4. [RD-4] 追问最必要的问题（不超过3个）
5. [RD-5] 提取功能列表
6. [RD-6] 输出工具定义JSON
```

## 需求澄清纪要格式

```markdown
## 需求澄清纪要

### 工具定义
- tool_key: [工具英文标识]
- tool_name: [工具中文名称]
- group: [工具组英文标识]
- features: [功能列表]

### 假设确认
- [假设1]: [已确认/待确认]
- [假设2]: [已确认/待确认]

### Open Questions
- [问题1]: [待用户确认]
```

## 命名规则

| 字段 | 规则 | 示例 |
|------|------|------|
| tool_key | kebab-case，英文+数字 | weekly-report-assistant |
| tool_name | 中文，2-10字符 | 周报助手 |
| group | kebab-case，英文+数字 | collaboration-tools |

## 禁止行为
- 禁止跳过假设确认直接输出定义
- 禁止创造需求中不存在的功能