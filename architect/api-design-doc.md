---
name: architect-api-design-doc
description: 架构师API设计文档生成子技能。生成结构化接口设计文档（HTML table格式）。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# API 设计文档 (PPQA)

## 用途
生成结构化接口设计文档，必须输出为HTML table格式。

## 输入
- 工具定义JSON（来自 tool-intake.md）
- 数据库设计结果（来自 db-design-intake.md）

## 输出
HTML table格式的API设计文档，包含：
- 工具名称
- API地址
- 请求方式 (GET/POST/PUT/DELETE)
- Path参数、Query参数、Body参数
- Header参数（Authorization等）
- 权限要求
- 成功返回（字段级）
- 失败返回（字段级）
- 备注

## 执行步骤

```
1. [PPQA-1] 读取工具定义，理解API需求
2. [PPQA-2] 读取数据库设计，理解数据模型
3. [PPQA-3] 推导当前工具需要的接口列表
4. [PPQA-4] 推导每个接口的请求参数与返回结构
5. [PPQA-5] 整理设计文档草稿
6. [PPQA-6] 展示给用户审核
7. [PPQA-7] 用户确认后输出最终设计文档
```

## 统一协议结构（新建工具必须使用）

### 请求结构
```
request_id: string (UUID)
ts: number (Unix timestamp)
payload: object (业务数据)
```

### 成功响应结构
```
version: string
success: boolean (true)
code: string
message: string
request_id: string
ts: number
data: object | array
```

### 失败响应结构
```
version: string
success: boolean (false)
code: string
message: string
request_id: string
ts: number
error.details: object
```

## 设计文档格式要求

- 必须输出为 HTML table
- 同一工具下多个接口时，工具名称列使用 rowspan 合并
- Body参数按统一请求结构展开

## PPQA 合规检查清单

```
□ 工具名称正确填写
□ API地址格式正确 (/api/v1/{group}/{tool-key})
□ 请求方式与接口动作匹配
□ 参数定义完整（Path/Query/Body/Header）
□ 权限要求明确
□ 成功返回字段级展开
□ 失败返回字段级展开
□ 新建工具使用统一协议结构
□ HTML table格式正确
```

## 禁止行为
- 禁止在用户确认前输出"最终"文档
- 禁止补充输入不支持的接口