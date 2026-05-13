---
name: testing-api-test
description: 测试工程师接口测试子技能。执行curl样例。触发条件：后端测试通过后。
version: 1.0.0
cmmi_process_area: VER
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 接口测试 (VER)

## 用途
执行curl样例。

## 触发时机
后端测试通过后。

## 输入
- 测试文档（包含curl示例）
- 后端服务运行状态

## 输出
```markdown
## 接口测试执行记录

### 测试结果
| 接口 | 方法 | 状态 | 备注 |
|------|------|------|------|
| /api/v1/xxx | GET | ✅ 通过 | - |
| /api/v1/xxx | POST | ✅ 通过 | - |
| /api/v1/xxx/{id} | PUT | ✅ 通过 | - |
| /api/v1/xxx/{id} | DELETE | ✅ 通过 | - |

### 失败项（如有）
| 接口 | 方法 | 失败原因 | 实际响应 |
|------|------|---------|---------|
| - | - | - | - |
```

## 执行步骤

```
1. [VER-1] 按测试文档中的完整 curl 逐条执行
2. [VER-2] 逐条对照测试文档中的预期结果检查关键返回字段和值
3. [VER-3] 禁止跳过测试文档中的任何一条测试样例
4. [VER-4] 记录通过/失败项
```

## curl 执行示例

```bash
# GET 请求
curl -X GET "http://localhost:8080/api/v1/{group}/{tool-key}" \
  -H "Authorization: Bearer {token}"

# POST 请求
curl -X POST "http://localhost:8080/api/v1/{group}/{tool-key}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "request_id": "uuid",
    "ts": 1234567890,
    "payload": {}
  }'
```

## 禁止行为
- 禁止跳过测试文档中的任何一条测试样例
- 禁止不验证返回字段值就判定通过