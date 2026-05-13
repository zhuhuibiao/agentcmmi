---
name: testing-planning
description: 测试工程师测试计划子技能。测试范围、顺序、检查点。触发条件：接收测试任务。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 测试计划 (PMC)

## 用途
测试范围、顺序、检查点。

## 触发时机
接收测试任务。

## 输入
- 设计文档
- 测试文档
- 前端AI报告
- 后端AI报告

## 输出
```markdown
## 测试计划

### 测试范围
- 前端测试: frontend/tests/<group>/<tool-key>/index.spec.ts
- 后端测试: backend/tests/<group>/<tool-key>/index_test.py
- 接口测试: 测试文档中的 curl 示例

### 测试顺序
1. 前端单元测试（本地）
2. 后端单元测试（本地）
3. 接口测试（按测试文档执行 curl）
4. 集成测试（前后端联调）

### 检查点
- [ ] 前端测试全部通过
- [ ] 后端测试全部通过
- [ ] 接口测试全部通过
- [ ] 覆盖率达标
```

## 执行步骤

```
1. [PMC-1] 读取设计文档，理解API契约
2. [PMC-2] 读取测试文档，理解验收标准
3. [PMC-3] 读取前端AI和后端AI的报告
4. [PMC-4] 识别测试范围和依赖
5. [PMC-5] 制定测试计划
```

## 禁止行为
- 禁止遗漏任何测试文件