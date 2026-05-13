# 更新日志

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-05-26

### 新增

#### 快速通道体系
- `FAST-TRACK.md` - 快速通道总览文档
  - XS/Hotfix: 10分钟流程
  - S/Small: 30分钟流程
  - M/L/XL: 完整流程

#### 规则引擎
- `rules/fast-track-rules.md` - 快速通道判定规则
  - 决策矩阵 (XS/S/M/L/XL)
  - 详细判定标准
  - 自动判定脚本

- `rules/ppqa-checklist.md` - PPQA 自检清单
  - 开发前/中/后检查项
  - 多语言 lint 命令
  - pre-commit hook 示例

#### 交接模板
- `handoff/architect-to-dev.md` - 架构师→开发者交接模板
- `handoff/dev-to-tester.md` - 开发者→测试师交接模板
- `handoff/llr-template.md` - 经验教训收集模板

#### 自动化脚本
- `scripts/ppqa-check.py` - PPQA 自动化检查脚本
  - C1: 公共API文档注释检查
  - C2: 硬编码配置检查
  - C3: 错误处理完善性检查
  - C4: 测试覆盖率检查

- `scripts/llr-collect.py` - LLR 经验收集脚本
  - 创建 LLR 文档
  - 搜索已有 LLR
  - JSON 索引更新

#### 角色增强
- 所有角色 SKILL.md 新增"快速通道"入口
- `architect/car.md` 新增"快速 CAR (Hotfix 场景)"
  - 15分钟简化根因分析流程
  - Hotfix 教训记录模板

### 改进

- 后端 SKILL.md 新增"新增禁止行为"规则
- 前端 SKILL.md 同步更新
- UI 设计师 SKILL.md 同步更新
- 测试工程师 SKILL.md 同步更新

---

## [1.0.0] - 2026-05-11

### 新增

#### 核心角色
- `architect/SKILL.md` - 架构师主流程 (CMMI L5)
- `backend/SKILL.md` - 后端开发主流程 (多语言)
- `frontend/SKILL.md` - 前端开发主流程
- `ui-designer/SKILL.md` - UI 设计师主流程
- `testing/SKILL.md` - 测试工程师主流程

#### 架构师子技能
- `tool-intake.md` - 需求接收
- `db-design-intake.md` - 数据库设计检查
- `api-design-doc.md` - API 设计文档
- `design-doc-storage.md` - 设计文档存储
- `test-doc-design.md` - 测试文档
- `test-doc-storage.md` - 测试文档存储
- `task-list-design.md` - 任务清单
- `task-list-storage.md` - 任务清单存储
- `dar.md` - 决策分析与决议
- `car.md` - 因果分析与决议

#### 后端子技能
- `requirements-clarify.md` - 需求澄清
- `planning.md` - 项目策划 (PMC)
- `tdd.md` - TDD 红绿重构
- `ppqa.md` - PPQA 质量审计
- `metrics.md` - OPP 量化指标
- `car.md` - Bug 根因分析

#### 多语言规范
- `languages/python.md` - Python 代码规范
- `languages/go.md` - Go 代码规范
- `languages/java.md` - Java 代码规范
- `languages/nodejs.md` - Node.js 代码规范

#### 前端子技能
- `requirements-clarify.md`
- `planning.md`
- `implementation.md`
- `ppqa.md`
- `metrics.md`
- `car.md`

#### UI 设计师子技能
- `requirements-understand.md`
- `information-architecture.md`
- `interaction-design.md`
- `visual-design.md`
- `component-spec.md`
- `design-review.md`
- `output.md`

#### 测试工程师子技能
- `planning.md`
- `frontend-test.md`
- `backend-test.md`
- `api-test.md`
- `coverage-audit.md`
- `metrics.md`
- `car.md`

---

## 旧版本

- [1.0.0] - 初始版本

[2.0.0]: https://github.com/your-repo/enhanced/releases/tag/v2.0.0
[1.0.0]: https://github.com/your-repo/enhanced/releases/tag/v1.0.0