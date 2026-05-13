---
name: testing-backend-test
description: 测试工程师后端测试子技能。执行单元/集成测试。触发条件：前端测试通过后。
version: 1.0.0
cmmi_process_area: VER
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 后端测试 (VER)

## 用途
执行单元/集成测试。

## 触发时机
前端测试通过后。

## 输入
- 后端测试文件: backend/tests/<group>/<tool-key>/index_test.py
- 测试计划

## 输出
```markdown
## 后端测试执行记录

### 测试结果
| 测试项 | 状态 | 备注 |
|--------|------|------|
| API测试 | ✅ 通过 | - |
| Service测试 | ✅ 通过 | - |
| Repository测试 | ✅ 通过 | - |

### 失败项（如有）
| 测试名称 | 失败原因 | 错误日志 |
|---------|---------|---------|
| - | - | - |
```

## 执行步骤

```
1. [VER-1] 执行后端测试文件
2. [VER-2] 逐条执行测试
3. [VER-3] 记录通过/失败项
4. [VER-4] 如失败，记录失败信息
```

## 测试框架（按语言）

| 语言 | 测试框架 | 命令 |
|------|---------|------|
| Python | pytest | `pytest backend/tests/... -v` |
| Go | testing | `go test ./... -v` |
| Java | JUnit 5 | `mvn test` |
| Node.js | Jest | `jest backend/tests/...` |

## 禁止行为
- 禁止跳过后端测试文件中的任何测试