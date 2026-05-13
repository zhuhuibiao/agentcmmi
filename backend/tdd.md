---
name: backend-tdd
description: 后端TDD执行子技能。红绿重构循环。触发条件：开发计划表已输出，按任务顺序执行。
version: 1.0.0
cmmi_process_area: VER
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# TDD 执行 (VER)

## 用途
TDD 红绿重构循环。

## 触发时机
开发计划表已输出，按任务顺序执行。

## TDD循环

```
    RED                GREEN              REFACTOR
 Write a test    → Write minimal code  → Clean up
 that fails         to make it pass
```

## 执行步骤

### RED: 写一个失败的测试
```
1. [TDD-1] 写一个失败的测试
   - 测试必须描述行为，不是实现细节
   - 使用公共API，不用mock内部实现
   - 参考对应语言的测试规范
```

### GREEN: 写最小代码让测试通过
```
2. [TDD-2] 写最小代码让测试通过
   - 不要过度工程
   - 问: "最简单的能工作的代码是什么?"
   - 遵循对应语言的代码规范
```

### REFACTOR: 重构
```
3. [TDD-3] 重构
   - 提取重复逻辑
   - 改善命名
   - 移除死代码
   - 每次重构后运行测试
```

## 每个任务的TDD流程

```
For each task in 开发计划表:
    RED  → GREEN → REFACTOR
    ↓        ↓        ↓
  写测试   通过测试   重构代码
    ↓        ↓        ↓
  (repeat for next task)
```

## 测试文件位置

| 语言 | 测试文件位置 | 主测试文件 |
|------|------------|-----------|
| Python | backend/tests/{group}/{tool-key}/ | test_{tool_key}.py |
| Go | backend/modules/{group}/{tool-key}/ | {tool_key}_test.go |
| Java | backend/src/test/java/com/{company}/... | {ToolKey}ServiceTest.java |
| Node.js | backend/src/modules/{group}/{tool-key}/ | {tool-key}.test.ts |

## PPQA 合规检查（持续进行）

- [PPQA-C1] 代码符合对应语言的代码规范
- [PPQA-C2] 公共API有文档注释
- [PPQA-C3] 无硬编码配置
- [PPQA-C4] 错误处理完善

## 自测试要求

- [ ] 必须生成本工具对应的后端测试文件
- [ ] 测试文件命名符合对应语言规范
- [ ] 发现测试失败时，必须继续修复，禁止带着失败结果提交

## 禁止行为
- 禁止提交无单元测试的函数
- 禁止跳过失败的测试继续开发
- 禁止写测试来验证实现细节