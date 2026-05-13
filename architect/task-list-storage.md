---
name: architect-task-list-storage
description: 架构师任务清单存储子技能。将任务清单写入目标路径。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 任务清单存储 (PMC)

## 用途
将任务清单写入目标路径。

## 输入
- 任务清单（来自 task-list-design.md）
- 目标存储路径

## 输出
- 任务清单文件（写入指定路径）

## 执行步骤

```
1. [PMC-1] 确定目标存储路径
2. [PMC-2] 检查目录是否存在，不存在则创建
3. [PMC-3] 写入任务清单文件
4. [PMC-4] 确认写入成功
```

## 存储路径规范

```
docs/
└── {group}/
    └── {tool-key}/
        └── {tool-key}-task-list-v{version}.md
```

示例：
```
docs/
└── collaboration-tools/
    └── weekly-report-assistant/
        └── weekly-report-assistant-task-list-v1.0.md
```

## 版本命名规则

```
{tool-key}-task-list-v{主版本}.{次版本}.md
```

## 派发任务时必须提供的信息

### 后端任务派发
```
- 设计文档路径
- 测试文档路径
- 任务清单路径
- 目标模块路径: backend/app/modules/{group}/{tool-key}/
- 允许修改文件范围: [列表]
- 禁止修改文件范围: [列表]
```

### 前端任务派发
```
- 设计文档路径
- 测试文档路径
- 任务清单路径
- 工具组英文标识: {group}
- 工具英文标识: {tool-key}
```

## 禁止行为
- 禁止覆盖未备份的已有任务清单
- 禁止写入未授权的路径