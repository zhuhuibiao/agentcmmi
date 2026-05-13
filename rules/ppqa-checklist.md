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

- [ ] 运行 `python scripts/ppqa-check.py` 无报错
- [ ] 公共 API 有文档注释
- [ ] 无硬编码配置 (密码、IP、连接字符串)
- [ ] 错误处理完善 (无裸露 except)
- [ ] 测试覆盖率 ≥ 80%
- [ ] 圈复杂度 ≤ 10

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
```