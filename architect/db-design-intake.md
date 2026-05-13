---
name: architect-db-design-intake
description: 架构师数据库设计检查子技能。检查现有数据库是否支撑新工具，如需新增表则输出设计方案。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 数据库设计检查 (PMC)

## 用途
检查现有数据库是否支撑新工具，如需新增表则输出设计方案。

## 输入
- 工具定义JSON（来自 tool-intake.md）
- 现有数据库 schema（如有）

## 输出
```json
{
  "existing_tables": [
    {"name": "表名", "usable": true/false, "note": "备注"}
  ],
  "new_tables": [
    {
      "name": "表名",
      "fields": [
        {"name": "字段名", "type": "类型", "nullable": true/false, "key": "PK/FK/..."}
      ]
    }
  ],
  "conclusion": "可落地 / 需补充信息",
  " blockers": ["阻塞问题1", "阻塞问题2"]
}
```

## 执行步骤

```
1. [PMC-1] 读取工具定义JSON，理解数据需求
2. [PMC-2] 检查现有数据库 schema
3. [PMC-3] 逐个功能分析所需数据模型
4. [PMC-4] 识别可复用的现有表
5. [PMC-5] 如需新增表，输出表结构设计
6. [PMC-6] 确认表字段定义明确
7. [PMC-7] 输出结论
```

## 数据库设计检查结果格式

```markdown
## 数据库设计检查结果

### 工具信息
- tool_key: {tool_key}
- tool_name: {tool_name}

### 现有表
| 表名 | 可用性 | 备注 |
|------|--------|------|
| existing_table | ✅ 可用 | 字段匹配 |
| existing_table | ❌ 需扩展 | 缺少字段: xxx |

### 需新增的表
| 表名 | 字段 | 类型 | 约束 |
|------|------|------|------|
| new_table | id | BIGINT | PK, AUTO_INCREMENT |
| new_table | name | VARCHAR(100) | NOT NULL |

### 结论
- [可落地 / 需补充信息]

### 阻塞问题（如有）
- [问题描述]
```

## 禁止行为
- 禁止在表字段定义不明确时输出"可落地"结论
- 禁止假设数据库结构而不做检查