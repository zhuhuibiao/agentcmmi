# AgentCMMI

> 企业级 AI Agent 开发框架 | CMMI L5 标准 | 开箱即用

[![CMMI L5](https://img.shields.io/badge/CMMI-L5%20Compliant-green.svg)](https://www.sei.cmu.edu/our-work/process-improvement-capability-improvement/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 是什么

AgentCMMI 是一个**企业级 AI Agent 开发框架**，为 AI Agent 提供标准化、可量化的开发流程规范。

解决的核心问题：**AI 开发时序乱、质量差、难复用**。

---

## 能做什么

| 角色 | 职责 |
|------|------|
| **架构师** | 需求分析 → 数据库设计 → API文档 → 测试文档 → 任务派发 |
| **后端开发** | TDD 红绿重构，多语言支持 (Python/Go/Java/Node.js) |
| **前端开发** | 精准实现设计稿，Playwright E2E 测试 |
| **UI 设计师** | 需求理解 → 信息架构 → 交互设计 → 视觉规范 |
| **测试工程师** | 接口测试、覆盖率审计、缺陷分析 |

---

## 核心特性

### 1. CMMI L5 流程合规
- **固定流程**：禁止跳步，确保每个阶段都有产出
- **前置条件**：条件不满足时禁止开工
- **禁止行为**：明确列出 AI 不应该做的事

### 2. 快速通道 (Fast Track)
| 类型 | 场景 | 时间 |
|------|------|------|
| XS | 1-5行 Bug修复 | 10分钟 |
| S | <50行新功能 | 30分钟 |
| M | 50-200行模块 | 2-4小时 |
| L/XL | >200行复杂功能 | 走完整流程 |

### 3. 标准化交接
- 架构师 → 开发者 交接模板
- 开发者 → 测试师 交接模板
- LLR 经验教训收集模板

### 4. 自动化 PPQA
```bash
# 代码质量检查
python scripts/ppqa-check.py

# 检查项: 公共API文档 | 无硬编码 | 错误处理 | 测试覆盖率≥80%

# 安全专项检查 (OWASP Top 10)
python scripts/ppqa-security-check.py .

# 检查项: SQL注入 | XSS | 命令注入 | 反序列化 | SSRF | 敏感信息
```

### 5. 安全审计 (OWASP Top 10)
| 漏洞类型 | 防护措施 | 验证工具 |
|----------|----------|----------|
| SQL注入 | 参数化查询 | ppqa-security-check.py |
| XSS | 输出编码 + CSP | security-coding.md |
| 命令注入 | 列表参数 | security-coding.md |
| 敏感信息泄露 | 环境变量 | ppqa-security-check.py |

### 6. 经验知识库
```bash
python scripts/llr-collect.py create <project>
python scripts/llr-collect.py search <keyword>
```

### 6. 多语言支持
| Python | Go | Java | Node.js |
|--------|-----|------|---------|
| FastAPI/Flask/Django | Gin/Fiber/Echo | Spring Boot | Express/NestJS |

---

## 优势对比

| 维度 | 其他 Skill | AgentCMMI |
|------|------------|----------|
| 流程规范 | 随意发挥 | 固定流程，禁止跳步 |
| 质量门禁 | 人工检查 | PPQA 自动化 |
| 安全审计 | 无 | OWASP Top 10 自动扫描 |
| 快速修复 | 走完整流程 | Hotfix 15分钟 |
| 经验复用 | 无积累 | LLR 知识库 |
| 交接规范 | 口头交接 | 标准模板 |
| 多语言 | 单一语言 | 4种语言 |
| 标准化 | 无 | **CMMI L5** |

---

## 目录结构

```
agentcmmi/
├── architect/               # 架构师
│   ├── SKILL.md
│   ├── tool-intake.md       # 需求接收
│   ├── db-design-intake.md  # 数据库设计
│   ├── api-design-doc.md    # API设计文档
│   ├── design-doc-storage.md
│   ├── test-doc-design.md
│   ├── test-doc-storage.md
│   ├── task-list-design.md
│   ├── task-list-storage.md
│   ├── dar.md               # 决策分析
│   └── car.md               # 根因分析
│
├── backend/                 # 后端开发
│   ├── SKILL.md
│   ├── requirements-clarify.md
│   ├── planning.md
│   ├── tdd.md
│   ├── ppqa.md
│   ├── metrics.md
│   ├── car.md
│   ├── security-coding.md    # 安全编码规范 ← 新增
│   └── languages/
│       ├── python.md
│       ├── go.md
│       ├── java.md
│       └── nodejs.md
│
├── frontend/               # 前端开发
│   ├── SKILL.md
│   ├── requirements-clarify.md
│   ├── planning.md
│   ├── implementation.md
│   ├── ppqa.md
│   ├── metrics.md
│   └── car.md
│
├── ui-designer/            # UI设计师
│   ├── SKILL.md
│   ├── requirements-understand.md
│   ├── information-architecture.md
│   ├── interaction-design.md
│   ├── visual-design.md
│   ├── component-spec.md
│   ├── design-review.md
│   └── output.md
│
├── testing/                # 测试工程师
│   ├── SKILL.md
│   ├── planning.md
│   ├── frontend-test.md
│   ├── backend-test.md
│   ├── api-test.md
│   ├── coverage-audit.md
│   ├── metrics.md
│   ├── car.md
│   └── security-audit.md    # 安全审计 ← 新增
│
├── FAST-TRACK.md           # 快速通道
├── rules/
│   ├── fast-track-rules.md
│   └── ppqa-checklist.md
├── handoff/
│   ├── architect-to-dev.md
│   ├── dev-to-tester.md
│   └── llr-template.md
├── scripts/
│   ├── ppqa-check.py
│   ├── ppqa-security-check.py  # OWASP安全扫描 ← 新增
│   └── llr-collect.py
└── docs/
    └── plans/
```

---

## 快速开始

### 1. 克隆使用
```bash
git clone https://github.com/your-repo/agentcmmi.git
cd agentcmmi
cat architect/SKILL.md      # 了解架构师流程
cat backend/SKILL.md       # 了解后端流程
```

### 2. 集成到 Claude Code
将 `agentcmmi/` 复制到项目的 `.claude/skills/` 目录

### 3. 运行自动化检查
```bash
python scripts/ppqa-check.py /path/to/project
python scripts/llr-collect.py create my-project
python scripts/llr-collect.py search backend
```

---

## 为什么选择 AgentCMMI

| 特性 | 说明 |
|------|------|
| **CMMI L5** | 全球首个 CMMI L5 标准的 AI Agent 开发框架 |
| **流程标准化** | 8步固定流程，禁止跳步 |
| **快速修复** | Hotfix 从 2-4小时缩短到 15分钟 |
| **自动化质量** | PPQA 自动化检查，100% 覆盖 |
| **经验复用** | LLR 知识库，避免重复踩坑 |
| **多语言支持** | Python / Go / Java / Node.js |

---

## 适用场景

- 企业级 AI Agent 开发团队
- 需要可量化质量指标的 AI 产品
- 多角色协作项目
- 高频 Hotfix 场景
- 需要经验知识沉淀

---

## 贡献

欢迎提交 Issue 和 PR！

1. Fork 仓库
2. 创建分支 (`git checkout -b feature/xxx`)
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 许可证

MIT - 详见 [LICENSE](LICENSE)