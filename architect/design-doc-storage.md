---
name: architect-design-doc-storage
description: 架构师设计文档存储子技能。将API设计文档写入目标路径。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 设计文档存储 (PMC)

## 用途
将API设计文档写入目标路径，记录文档版本。

## 输入
- API设计文档（来自 api-design-doc.md）
- 目标存储路径

## 输出
- 设计文档文件（写入指定路径）
- 文档版本记录

## 执行步骤

```
1. [PMC-1] 确定目标存储路径
2. [PMC-2] 检查目录是否存在，不存在则创建
3. [PMC-3] 写入设计文档文件
4. [PMC-4] 记录文档版本（文件名包含版本号或日期）
5. [PMC-5] 确认写入成功
```

## 存储路径规范

```
docs/
└── {group}/
    └── {tool-key}/
        └── {tool-key}-api-design-{version}.md
```

示例：
```
docs/
└── collaboration-tools/
    └── weekly-report-assistant/
        └── weekly-report-assistant-api-design-v1.0.md
```

## 版本命名规则

```
{tool-key}-api-design-v{主版本}.{次版本}.md

示例：
weekly-report-assistant-api-design-v1.0.md
weekly-report-assistant-api-design-v1.1.md
```

## 禁止行为
- 禁止覆盖未备份的已有文档
- 禁止写入未授权的路径