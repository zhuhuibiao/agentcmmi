# PPQA 自检清单

## 开发前 (编码规范)

- [ ] 理解对应语言的代码规范文件
- [ ] IDE 已配置格式化工具 (Prettier / Black / gofmt)
- [ ] ESLint / pylint 已配置

## 开发中 (持续自检)

### Python
```bash
# 格式化
black .

# Lint
pylint **/*.py --disable=C0114

# 类型检查
mypy .
```

### JavaScript/TypeScript
```bash
# 格式化
npx prettier --write .

# Lint
npx eslint . --fix

# 类型检查
npx tsc --noEmit
```

### Go
```bash
# 格式化
go fmt ./...

# Lint
golangci-lint run

# Vet
go vet ./...
```

## 开发后 (提交前)

### 代码质量检查
- [ ] 运行 `python scripts/ppqa-check.py` 无报错
- [ ] 公共 API 有文档注释
- [ ] 无硬编码配置 (密码、IP、连接字符串)
- [ ] 错误处理完善 (无裸露 except)
- [ ] 测试覆盖率 ≥ 80%
- [ ] 圈复杂度 ≤ 10

### 安全检查 (OWASP Top 10)
- [ ] 运行 `python scripts/ppqa-security-check.py` 无高风险报错
- [ ] **SQL 注入**: 无字符串拼接SQL，使用参数化查询
- [ ] **XSS**: 用户输入已转义，无 innerHTML/dangerouslySetInnerHTML
- [ ] **命令注入**: 无 os.system/popen/subprocess shell=True
- [ ] **反序列化**: 无 pickle.loads/yaml.load(非FullLoader)
- [ ] **SSRF**: URL 已校验，不允许内部IP访问
- [ ] **敏感信息**: 无密码/API Key/Token 硬编码

### 安全扫描命令

```bash
# 完整安全扫描
python scripts/ppqa-security-check.py . --report

# 分项检查
python scripts/ppqa-security-check.py . --check sql     # SQL注入
python scripts/ppqa-security-check.py . --check xss     # XSS
python scripts/ppqa-security-check.py . --check cmd     # 命令注入
python scripts/ppqa-security-check.py . --check deser   # 反序列化
python scripts/ppqa-security-check.py . --check ssrf   # SSRF
python scripts/ppqa-security-check.py . --check secrets # 敏感信息
```

## 自动触发

在 `.git/hooks/pre-commit` 中添加:

```bash
#!/bin/bash
echo "Running PPQA checks..."
python scripts/ppqa-check.py
if [ $? -ne 0 ]; then
    echo "PPQA check failed. Please fix issues before committing."
    exit 1
fi
echo "Running security checks..."
python scripts/ppqa-security-check.py .
if [ $? -ne 0 ]; then
    echo "Security check failed. Please fix high-risk issues before committing."
    exit 1
fi
```

## OWASP Top 10 检查映射

| OWASP Top 10 | PPQA 规则 | 检查脚本 |
|--------------|-----------|----------|
| A01: Broken Access Control | - | 手动测试 |
| A02: Cryptographic Failures | C10 | ppqa-security-check.py |
| A03: Injection | C5, C6, C7 | ppqa-security-check.py |
| A04: Insecure Design | - | 架构评审 |
| A05: Security Misconfiguration | - | 配置审计 |
| A06: Vulnerable Components | - | 依赖扫描 (npm audit / safety) |
| A07: Identification Failures | - | 认证测试 |
| A08: Software Integrity | C8 | ppqa-security-check.py |
| A09: Logging Failures | - | 日志审计 |
| A10: SSRF | C9 | ppqa-security-check.py |