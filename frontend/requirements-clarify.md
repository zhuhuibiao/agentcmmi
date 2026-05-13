---
name: frontend-requirements-clarify
description: 前端需求澄清子技能。确认假设、明确验收标准。触发条件：设计文档存在模糊或假设未声明时。
version: 1.0.0
cmmi_process_area: RD
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 需求澄清 (RD)

## 用途
确认假设、明确验收标准。

## 触发时机
设计文档存在模糊或假设未声明时。

## 输入
- 设计文档
- UI设计文档
- 工具组英文标识

## 输出
```markdown
## 需求澄清纪要

### 确认信息
- API地址: [地址]
- 工具组标识: [组名]
- 请求/响应字段: [字段列表]

### 验收标准
- [标准1]: 具体可测试条件
- [标准2]: 具体可测试条件

### Open Questions
- [问题1]: [待用户确认]
```

## 执行步骤

```
1. [RD-1] 列出当前假设:
   ASSUMPTIONS I'M MAKING:
   1. API返回字段与设计文档一致
   2. 工具组英文标识为 {group}
   → Correct me now or I'll proceed with these.

2. [RD-2] 追问最必要的问题（不超过3个）
3. [RD-3] 将设计文档翻译为验收标准
4. [RD-4] 输出《需求澄清纪要》
```

## 禁止行为
- 禁止跳过假设确认直接开工
- 禁止创造设计文档不存在的API假设