---
name: frontend-metrics
description: 前端OPP量化评估子技能。量化指标报告。触发时机：交付前。
version: 1.0.0
cmmi_process_area: OPP
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# OPP 量化评估

## 用途
量化指标报告。

## 触发时机
交付前。

## 输入
- 源代码
- 测试覆盖率报告

## 输出
```markdown
## 性能指标评估报告 (OPP)

### 量化指标
| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 组件数量 | - | X | - |
| 代码行数 | - | X | - |
| 测试覆盖率 | ≥80% | 85% | ✅ |
| Playwright测试 | 100%通过 | 100% | ✅ |

### 技术债
- [无 / 列出发现的潜在问题]
```

## 执行步骤

```
1. [OPP-1] 统计组件复杂度
2. [OPP-2] 统计代码行数
3. [OPP-3] 统计测试覆盖率
4. [OPP-4] 生成《性能指标评估报告》
```

## OPP 量化指标

| 指标 | 目标 | 测量方法 |
|------|------|---------|
| Playwright测试覆盖率 | ≥80% | Playwright HTML Report |
| Bundle size | ≤500KB | webpack build analysis |
| 首屏加载时间 | ≤3s | Lighthouse |
| 组件复用率 | ≥70% | 代码分析 |

## 禁止行为
- 禁止不统计就输出"无问题"
- 禁止忽略性能超标项