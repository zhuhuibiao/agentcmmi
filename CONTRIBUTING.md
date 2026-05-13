# 贡献指南

感谢您对 Enhanced 项目的关注！我们欢迎各种形式的贡献。

## 如何贡献

### 报告问题

如果您发现问题或有改进建议，请：

1. 先搜索 [Issue 列表](https://github.com/your-repo/enhanced/issues) 确保问题未被报告
2. 创建新 Issue，包含：
   - 清晰的问题描述
   - 重现步骤
   - 环境信息 (Claude Code 版本等)
   - 预期 vs 实际行为

### 提交代码

#### 1. Fork 仓库

点击仓库页面右上角的 "Fork" 按钮。

#### 2. 克隆到本地

```bash
git clone https://github.com/your-username/enhanced.git
cd enhanced
```

#### 3. 创建功能分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

#### 4. 提交更改

```bash
git add .
git commit -m "feat: 添加 xxx 功能"
git commit -m "fix: 修复 xxx 问题"
git commit -m "docs: 更新 xxx 文档"
```

**提交消息规范：**

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更改 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构（不影响功能） |
| `test` | 测试相关 |
| `chore` | 构建/工具变更 |

#### 5. 推送分支

```bash
git push origin feature/your-feature-name
```

#### 6. 创建 Pull Request

1. 在 GitHub 页面点击 "New Pull Request"
2. 选择您的分支与主仓库的 main 分支对比
3. 填写 PR 描述：
   - 描述更改内容
   - 关联的 Issue 编号
   - 测试说明

## 分支管理

```
main          ← 生产环境，稳定版本
├── develop   ← 开发分支（如有）
├── feature/* ← 功能分支
└── fix/*     ← 修复分支
```

## 代码规范

### Skill 文件规范

- 使用 Markdown 格式
- Frontmatter 包含：`name`, `description`, `version`, `cmmi_process_area`
- 禁止行为用列表清晰列出
- 输入/输出标准用表格定义

### 脚本规范

- Python 脚本兼容 Python 3.8+
- 添加 Shebang (`#!/usr/bin/env python3`)
- 添加文档字符串

## 测试

提交前请确保：

```bash
# 运行 PPQA 检查
python scripts/ppqa-check.py /path/to/project

# 如果修改了脚本，运行测试
python -m pytest tests/
```

## 发布流程

1. Maintainers 审核 PR
2. 合并后更新版本号
3. 生成 CHANGELOG
4. 发布新版本

## 问题解答

| 问题 | 解答 |
|------|------|
| 贡献代码需要签署协议吗？ | 否，MIT 许可证无需签署 |
| 可以贡献哪些类型的文件？ | Skill 文件、脚本、文档、测试 |
| 如何联系维护团队？ | 通过 GitHub Issue 或 Discussion |

---

**再次感谢您的贡献！** 🎉
