---
name: frontend-planning
description: 前端项目策划子技能。任务分解、开发计划表。触发条件：所有输入物已满足，必须先输出开发计划表。
version: 1.0.0
cmmi_process_area: PMC
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 项目策划 (PMC)

## 用途
任务分解、开发计划表。

## 触发时机
所有输入物已满足，必须先输出《开发计划表》。

## 输入
- 设计文档
- UI设计文档
- 任务清单

## 输出
```markdown
## 开发计划表

| 任务编号 | 任务名称 | 依赖关系 | 工时(小时) | 风险 | 检查点 |
|---------|---------|---------|-----------|------|--------|
| Task 1 | 注册工具入口 | 无 | 0.5 | 无 | ✓ |
| Task 2 | 创建路由文件 | Task 1 | 0.5 | 无 | ✓ |
| Task 3 | 创建工具目录 | Task 2 | 0.5 | 无 | ✓ |
| Task 4 | 实现API层 | Task 3 | 1 | 无 | ✓ |
| Task 5 | 实现页面组件 | Task 4 | 2 | 无 | ✓ |
| Task 6 | 生成Playwright测试 | Task 5 | 1 | 无 | ✓ |

### 检查点: After Tasks 1-3
- [ ] 工具入口已注册
- [ ] 路由文件已创建
- [ ] 目录结构符合规范
```

## 执行步骤

```
1. [PMC-1] 读取设计文档，提取工具名称、API地址、请求方式
2. [PMC-2] 确定 tool-key 和前端路由路径
3. [PMC-3] 识别与现有代码的集成点
4. [PMC-4] 进行任务分解
5. [PMC-5] 估算工作量
6. [PMC-6] 识别风险点
7. [PMC-7] 输出《开发计划表》
8. [PMC-8] 设置检查点
```

## 固定开发顺序（来自现有规则）

1. 读取设计文档中的工具信息
2. 确定 tool-key
3. 确定前端路由路径
4. 在 tool-navigation.tsx 注册入口
5. 在 _layout/ 下创建路由文件
6. 创建工具目录 frontend/src/tools/<group>/<tool-key>/
7. 实现 API 调用层 (api.ts)
8. 实现页面组件 (components/)
9. 实现页面状态 (hooks/)
10. 生成前端测试文件
11. 补充前端测试
12. 执行前端构建校验
13. 执行 Playwright 测试
14. 输出前端报告

## 目录结构规范

```
frontend/src/tools/<group>/<tool-key>/
├── api.ts          # API调用层
├── types.ts        # 类型定义
├── schemas.ts      # 验证schema
├── components/    # 组件
│   ├── index.tsx
│   └── ...
├── hooks/         # 自定义hooks
│   └── index.ts
└── index.ts       # 导出

frontend/tests/<group>/<tool-key>/
├── index.spec.ts   # 主测试文件
└── ...
```

## 禁止行为
- 禁止在开发计划表输出前开始编码
- 禁止改变现有系统的整体视觉风格