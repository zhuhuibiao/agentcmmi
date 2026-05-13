---
name: backend-ppqa
description: 后端PPQA验证子技能。合规性检查、质量审计。触发时机：代码实现完成，准备交付前。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# PPQA 验证

## 用途
合规性检查、质量审计。

## 触发时机
代码实现完成，准备交付前。

## 输入
- 源代码
- 语言代码规范
- 设计文档

## 输出
```markdown
## 质量审计报告

### 技术栈
- 语言: {语言}
- 框架: {框架}

### 合规性检查
| 检查项 | 状态 | 备注 |
|--------|------|------|
| 代码规范 | ✅ 通过 | {语言}规范 |
| 文档注释 | ✅ 通过 | 公共API 100% |
| 圈复杂度 | ✅ 通过 | 平均 3.2, 最大 8 |
| 测试覆盖率 | ✅ 通过 | 82% |
| Linter | ✅ 通过 | {工具} |
| 类型检查 | ✅ 通过 | {工具} |

### 未解决问题
- [无 / 列出问题及修复方案]
```

## 执行步骤

```
1. [PPQA-1] 执行合规性检查清单
2. [PPQA-2] 运行语言对应的linter/formatter
3. [PPQA-3] 运行语言对应的类型检查/编译检查
4. [PPQA-4] 检查测试覆盖率
5. [PPQA-5] 验证 API 契约与设计文档一致
6. [PPQA-6] 生成《质量审计报告》
```

## 合规性检查清单（通用）

```
□ 代码符合语言代码规范
□ 公共API有文档注释
□ 圈复杂度 ≤ 10 的函数占比 ≥ 90%
□ 测试覆盖率 ≥ 80%
□ Linter/Formatter 通过
□ 类型检查/编译通过
□ API URL 与设计文档完全一致（不含尾部斜杠依赖重定向）
□ 请求/响应字段与设计文档一致
```

## 语言工具对照

| 语言 | Linter | Formatter | 类型检查 | 测试覆盖率 |
|------|--------|-----------|---------|-----------|
| Python | pylint/ruff | black | mypy | pytest-cov |
| Go | golangci-lint | gofmt/goimports | go vet | go test -cover |
| Java | Checkstyle | google-java-format | - | JUnit + Jacoco |
| Node.js | ESLint | Prettier | tsc --strict | Jest --coverage |

## 禁止行为
- 禁止跳过任何检查项
- 禁止带着未解决的问题提交
- 禁止降低覆盖率标准（< 80%）