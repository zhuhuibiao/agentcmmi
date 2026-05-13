# 交接文档: 架构师 → 开发者

## 交接信息

| 字段 | 内容 |
|------|------|
| 工具名称 | {tool_name} |
| 交接时间 | {timestamp} |
| 架构师 | {architect_name} |
| 开发者 | {developer_name} |
| 任务类型 | {XS/S/M/L} |

## 设计文档摘要

### API 契约

| 接口 | 方法 | 路径 | 输入 | 输出 |
|------|------|------|------|------|
| {api_name} | {GET/POST} | {/api/path} | {schema} | {schema} |

### 数据库变更 (如有)

```sql
-- {table_name}
{ddl_statements}
```

### 关键约束

- [ ] {constraint_1}
- [ ] {constraint_2}

## 技术要求

| 项目 | 要求 |
|------|------|
| 语言 | {language} |
| 框架 | {framework} |
| 代码规范 | {规范文件名} |
| 测试覆盖率 | ≥ {percentage}% |

## 风险提示

| 风险 | 等级 | 缓解措施 |
|------|------|----------|
| {risk_1} | {高/中/低} | {mitigation} |

## 验收标准

1. [ ] {acceptance_criterion_1}
2. [ ] {acceptance_criterion_2}
3. [ ] {acceptance_criterion_3}

## 开发者确认

- [ ] 已阅读设计文档
- [ ] 理解 API 契约
- [ ] 确认开发计划
- [ ] 无疑问

**开发者签名:** _________________**日期:** _____________
