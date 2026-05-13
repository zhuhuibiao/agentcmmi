---
name: architect-task-list-design
description: 架构师任务清单生成子技能。生成前后端任务清单，设置检查点。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 任务清单 (PMC)

## 用途
生成前后端任务清单，设置检查点，确保任务项只覆盖目标工具模块。

## 输入
- 设计文档路径
- 测试文档路径
- 数据库设计结果

## 输出
```markdown
## 任务清单

### 前端任务
| 任务编号 | 任务名称 | 依赖 | 检查点 |
|---------|---------|------|--------|
| FE-1 | 注册工具入口 | 无 | ✓ |
| FE-2 | 创建路由文件 | FE-1 | ✓ |
| FE-3 | 实现API层 | 无 | ✓ |
| FE-4 | 实现页面组件 | FE-3 | ✓ |
| FE-5 | 生成Playwright测试 | FE-4 | ✓ |

### 后端任务
| 任务编号 | 任务名称 | 依赖 | 检查点 |
|---------|---------|------|--------|
| BE-1 | 创建数据模型 | 无 | ✓ |
| BE-2 | 实现API接口 | BE-1 | ✓ |
| BE-3 | 生成单元测试 | BE-2 | ✓ |

### 检查点
- Checkpoint 1: After FE-1, BE-1
  - [ ] 基础结构创建完成
- Checkpoint 2: After FE-3, BE-2
  - [ ] 核心功能实现完成
- Checkpoint 3: After FE-5, BE-3
  - [ ] 测试覆盖完成
```

## 执行步骤

```
1. [PMC-1] 读取设计文档和测试文档
2. [PMC-2] 识别前端任务项
3. [PMC-3] 识别后端任务项
4. [PMC-4] 确定任务依赖关系
5. [PMC-5] 设置检查点（每2-3个任务一个）
6. [PMC-6] 输出任务清单
```

## 任务拆分原则

### 垂直切片（正确）
- Task 1: 创建{资源}（schema + API + 前端页面）
- Task 2: 查询{资源}（query + API + 前端页面）
- Task 3: 编辑{资源}（update + API + 前端页面）

### 面切片（错误）
- Task 1: 全部数据库schema
- Task 2: 全部API
- Task 3: 全部前端

## 前端任务清单模板

| 任务 | 说明 | 产出物 |
|------|------|--------|
| FE-1 | 注册工具入口 | tool-navigation.tsx 修改 |
| FE-2 | 创建路由文件 | _layout/xxx.tsx |
| FE-3 | 创建工具目录 | frontend/src/tools/{group}/{tool-key}/ |
| FE-4 | 实现API层 | api.ts |
| FE-5 | 实现页面组件 | components/ |
| FE-6 | 实现hooks | hooks/ |
| FE-7 | 生成Playwright测试 | tests/{group}/{tool-key}/index.spec.ts |

## 后端任务清单模板

| 任务 | 说明 | 产出物 |
|------|------|--------|
| BE-1 | 创建数据模型 | models.py |
| BE-2 | 创建Schema | schemas.py |
| BE-3 | 实现Service层 | service.py |
| BE-4 | 实现Repository层 | repository.py |
| BE-5 | 实现Router层 | router.py |
| BE-6 | 生成单元测试 | tests/{group}/{tool-key}/index_test.py |

## 禁止行为
- 禁止在任务清单外增加无关模块
- 禁止拆分出XL级任务（>5个文件变更）
- 禁止任务项超过10个（拆分工具）