# Enhanced Skills 完善计划

> **目标:** 解决 enhanced skills 在工程落地中的5个核心问题

**问题诊断:**
| 优先级 | 问题 | 当前影响 |
|--------|------|----------|
| P0 | 流程繁琐，小任务也走完整8步 | 用户等待时间长 |
| P1 | 无快速通道，hotfix 和新功能同流程 | 小改动成本过高 |
| P2 | 角色交接无标准模板 | 前后端协作摩擦 |
| P3 | Lessons Learned 无收集机制 | 经验无法复用 |
| P4 | PPQA 合规检查靠人工 | 质量门禁形同虚设 |

---

## 方案概述

### 新增文件清单
```
enhanced/
├── FAST-TRACK.md                          # [NEW] 快速通道总览
├── handoff/
│   ├── architect-to-dev.md                 # [NEW] 架构师→开发者交接模板
│   ├── dev-to-tester.md                    # [NEW] 开发者→测试师交接模板
│   └── llr-template.md                     # [NEW] 经验教训收集模板
├── rules/
│   ├── fast-track-rules.md                # [NEW] 简化流程判定规则
│   └── ppqa-checklist.md                  # [NEW] PPQA 自检清单
├── scripts/
│   ├── ppqa-check.py                      # [NEW] PPQA 自动化检查脚本
│   └── llr-collect.py                      # [NEW] LLR 收集脚本
└── docs/
    └── plans/
        └── 2026-05-26-enhanced-skills-v2.md  # 本计划

修改文件:
├── architect/SKILL.md                      # 增加快速通道入口
├── backend/SKILL.md                        # 增加简化流程条件
├── frontend/SKILL.md                        # 增加简化流程条件
├── ui-designer/SKILL.md                    # 增加简化流程条件
├── testing/SKILL.md                        # 增加简化流程条件
└── architect/car.md                        # 增加 hotfix 场景
```

---

## Task 1: 创建快速通道总览文档

**目标:** 新增 `FAST-TRACK.md`，定义何时走简化流程

### 步骤

- [ ] **Step 1: 创建 `enhanced/FAST-TRACK.md`**

```markdown
# 快速通道 (Fast Track)

## 目的
小任务走简化流程，大任务走完整流程。节省80%流程成本。

## 任务分类

| 类型 | 定义 | 流程 |
|------|------|------|
| **XS (Hotfix)** | 修复已知bug，1-5行代码 | → 快速通道 |
| **S (Small)** | 新增1个API/组件，<50行 | → 简化流程 |
| **M (Medium)** | 1个完整CRUD模块，50-200行 | → 完整流程 |
| **L (Large)** | 多模块/复杂业务，200-500行 | → 完整流程 |
| **XL (Epic)** | 跨工具/系统级，>500行 | → 拆分为M/L |

## 快速通道条件 (XS/S)

满足以下**所有条件**可走快速通道:
- [ ] 改动范围 ≤ 2个文件
- [ ] 无数据库 schema 变更
- [ ] 无新增 API 契约
- [ ] 无跨模块依赖
- [ ] 用户明确确认是小改动

## 快速通道路径

### Architect Fast Track (2步)
```
原始: Step1-8 (8个Step，2-4小时)
快速: F1-F2 (2个Step，10分钟)
```

```
F1: [RD] 确认需求 + 快速评估 → 输出 1页简化设计
F2: [PMC] 直接派发任务清单 → 交接给开发者
```

### Developer Fast Track (3步)
```
原始: Step0-4 (5个Step，4-8小时)
快速: F1-F3 (3个Step，30分钟)
```

```
F1: [RD] 需求确认 (5分钟)
F2: [PMC] 开发计划 (10分钟) → 输出简化开发计划表
F3: [VER+PPQA] 实现 + 自检 (15分钟)
```

### Tester Fast Track (2步)
```
原始: Step1-6 (6个Step，2-4小时)
快速: F1-F2 (2个Step，30分钟)
```

```
F1: [PMC] 测试确认 (10分钟)
F2: [VER] 执行关键测试 (20分钟)
```

## 质量门禁 (快速通道)

即使走快速通道，仍需满足:
- [ ] 代码可运行，无语法错误
- [ ] 有基本的单元测试
- [ ] 无明显的安全漏洞
- [ ] 提交信息标注 `[Fast-Track]`

## 决策流程图

```
用户请求
    ↓
┌─────────────────────────────────────┐
│ 改动范围评估                         │
│  - 几个文件？                        │
│  - 需要新增API吗？                   │
│  - 有数据库变更吗？                  │
└─────────────────────────────────────┘
    ↓
┌────────────────┐    否   ┌────────────────┐
│ XS/S + 无新API │ ──→    │ 走完整流程      │
│ + 无DB变更     │        │ (Step 1-8)     │
└────────────────┘        └────────────────┘
    ↓ 是
┌────────────────┐
│ 走快速通道     │
│ (见上方路径)   │
└────────────────┘
```

## 禁止行为
- 禁止将 L/XL 任务放入快速通道
- 禁止在快速通道中跳过自检
- 禁止将快速通道用于不熟悉的风险区域
```

---

## Task 2: 创建简化流程判定规则

**目标:** 新增 `rules/fast-track-rules.md`，明确定义何时可用简化流程

### 步骤

- [ ] **Step 1: 创建 `enhanced/rules/fast-track-rules.md`**

```markdown
# 快速通道判定规则

## 决策矩阵

| 条件 | XS (Hotfix) | S (Small) | M (Medium) | L/XL |
|------|-------------|-----------|------------|------|
| 文件数 | ≤1 | ≤2 | 3-5 | >5 |
| 代码增量 | ≤5行 | ≤50行 | 50-200行 | >200行 |
| 新增API | 无 | 无 | 1-3个 | >3个 |
| DB变更 | 无 | 无 | 可选 | 必须 |
| 跨模块 | 无 | 无 | 可选 | 必须 |
| 测试覆盖 | 可选 | 必须 | 必须 | 必须 |

## 详细判定标准

### XS (Hotfix) 判定

满足**所有**条件:
- [ ] 已知bug的修复
- [ ] 改动 ≤ 1个文件
- [ ] 改动 ≤ 5行代码
- [ ] 无新增函数/类
- [ ] 无API契约变更
- [ ] 无数据库变更
- [ ] 用户标注 "hotfix" 或 "bugfix"

**可省略:**
- 完整设计文档
- 任务清单
- 测试文档

**必须包含:**
- 修复代码
- 验证方式
- 提交信息标注 `[Hotfix]`

### S (Small) 判定

满足**所有**条件:
- [ ] 改动 ≤ 2个文件
- [ ] 改动 ≤ 50行代码
- [ ] 新增 ≤ 1个函数/API
- [ ] 无API契约破坏性变更
- [ ] 无数据库schema变更
- [ ] 用户标注 "small-change" 或同意简化流程

**可省略:**
- 完整设计文档 (用1页简化设计替代)
- 独立测试文档
- 详细任务清单 (用简化开发计划替代)

**必须包含:**
- 简化设计 (1页)
- 简化开发计划 (表格式)
- 基本单元测试

### M (Medium) 判定

满足**所有**条件:
- [ ] 改动 3-5个文件
- [ ] 改动 50-200行代码
- [ ] 新增 1-3个API
- [ ] 可能需要数据库变更
- [ ] 用户有明确需求

**流程:**
- 走完整流程，但可合并部分Step
- 设计文档可简化 (表格式API契约)
- 测试文档可简化 (关键路径覆盖)

### L/XL 禁止走快速通道

**必须走完整流程:**
- 改动 > 5个文件
- 改动 > 200行代码
- 新增 > 3个API
- 跨模块依赖
- 数据库schema变更
- 安全/权限相关变更

---

## 自动判定脚本 (可选)

```python
# scripts/check-fast-track.py
import sys

def check_fast_track(file_count, code_lines, new_apis, db_changes, cross_module):
    if file_count <= 1 and code_lines <= 5 and new_apis == 0 and not db_changes:
        return "XS (Hotfix) - 走快速通道"
    elif file_count <= 2 and code_lines <= 50 and new_apis <= 1 and not db_changes:
        return "S (Small) - 可走简化流程"
    elif file_count <= 5 and code_lines <= 200:
        return "M (Medium) - 走完整流程(简化版)"
    else:
        return "L/XL - 必须走完整流程"

if __name__ == "__main__":
    print(check_fast_track(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), bool(sys.argv[4]), bool(sys.argv[5])))
```

**使用方式:**
```bash
python check-fast-track.py 2 30 0 False False
# 输出: S (Small) - 可走简化流程
```
```

---

## Task 3: 创建角色交接模板

**目标:** 新增 `handoff/` 目录，包含标准交接文档

### 步骤

- [ ] **Step 1: 创建 `enhanced/handoff/architect-to-dev.md`**

```markdown
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
```

- [ ] **Step 2: 创建 `enhanced/handoff/dev-to-tester.md`**

```markdown
# 交接文档: 开发者 → 测试工程师

## 交接信息

| 字段 | 内容 |
|------|------|
| 工具名称 | {tool_name} |
| 交接时间 | {timestamp} |
| 开发者 | {developer_name} |
| 测试工程师 | {tester_name} |
| 代码分支 | {branch_name} |
| 提交Hash | {commit_hash} |

## 实现摘要

### 新增/修改的文件

| 文件 | 操作 | 变更说明 |
|------|------|----------|
| {file_1} | 新增 | {description} |
| {file_2} | 修改 | {description} |

### API 清单

| 接口 | 方法 | 路径 | 状态 |
|------|------|------|------|
| {api_1} | GET | /api/xxx | 已实现 |
| {api_2} | POST | /api/yyy | 已实现 |

### 测试执行记录

| 测试文件 | 执行结果 | 覆盖率 |
|----------|----------|--------|
| {test_file_1} | 通过 | {coverage}% |
| {test_file_2} | 通过 | {coverage}% |

## 已知问题

| 问题ID | 描述 | 严重程度 | 备注 |
|--------|------|----------|------|
| {issue_1} | {description} | {高/中/低} | {note} |

## 测试重点

1. [ ] {test_focus_1}
2. [ ] {test_focus_2}

## 测试工程师确认

- [ ] 已阅读交接文档
- [ ] 理解实现内容
- [ ] 确认测试范围
- [ ] 无疑问

**测试工程师签名:** _________________**日期:** _____________
```

- [ ] **Step 3: 创建 `enhanced/handoff/llr-template.md`**

```markdown
# 经验教训收集模板 (LLR)

## 基本信息

| 字段 | 内容 |
|------|------|
| 项目/工具名称 | {project_name} |
| 完成日期 | {completion_date} |
| 收集人 | {author} |
| 参与角色 | {roles} |

## 做得好的 (What's Working)

### 流程方面
- [ ] {what_worked_1}
- [ ] {what_worked_2}

### 技术方面
- [ ] {technical_success_1}
- [ ] {technical_success_2}

### 协作方面
- [ ] {collaboration_success_1}
- [ ] {collaboration_success_2}

## 需要改进的 (What Needs Improvement)

### 流程方面
| 问题 | 影响 | 建议改进 |
|------|------|----------|
| {issue_1} | {impact_1} | {suggestion_1} |
| {issue_2} | {impact_2} | {suggestion_2} |

### 技术方面
| 问题 | 影响 | 建议改进 |
|------|------|----------|
| {issue_1} | {impact_1} | {suggestion_1} |

### 协作方面
| 问题 | 影响 | 建议改进 |
|------|------|----------|
| {issue_1} | {impact_1} | {suggestion_1} |

## 下次同类任务建议

1. {recommendation_1}
2. {recommendation_2}
3. {recommendation_3}

## 可复用资产

| 资产类型 | 名称 | 位置 | 适用场景 |
|----------|------|------|----------|
| 代码模板 | {template_name} | {path} | {use_case} |
| 设计模式 | {pattern_name} | {path} | {use_case} |
| 文档模板 | {doc_template} | {path} | {use_case} |

## 量化指标

| 指标 | 计划 | 实际 | 偏差 |
|------|------|------|------|
| 工时 (小时) | {planned_hours} | {actual_hours} | {variance}% |
| 代码行数 | {planned_loc} | {actual_loc} | {variance}% |
| 缺陷数 | - | {defect_count} | - |
| 测试覆盖率 | {planned_coverage}% | {actual_coverage}% | {variance}% |

---

**填写说明:**
1. 在项目/工具完成后1周内填写
2. 由主要参与者共同回顾
3. 提交到 `knowledge/llr/` 目录
4. 下次同类任务前查阅相关 LLR
```

---

## Task 4: 创建 PPQA 自动化检查脚本

**目标:** 新增 `scripts/ppqa-check.py`，自动检查代码规范

### 步骤

- [ ] **Step 1: 创建 `enhanced/scripts/ppqa-check.py`**

```python
#!/usr/bin/env python3
"""
PPQA 合规性自动检查脚本
检查项:
1. 公共API有文档注释
2. 无硬编码配置
3. 错误处理完善
4. 测试覆盖率 ≥ 80%
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict

class PPQAChecker:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.issues: List[Dict] = []

    def check_all(self) -> bool:
        """执行所有检查"""
        print("=" * 50)
        print("PPQA 合规性检查")
        print("=" * 50)

        self.check_public_api_docs()
        self.check_no_hardcoded_config()
        self.check_error_handling()
        self.check_test_coverage()

        self.print_summary()
        return len(self.issues) == 0

    def check_public_api_docs(self):
        """检查公共API是否有文档注释"""
        print("\n[PPQA-C1] 公共API文档注释检查...")

        for py_file in self.root_dir.rglob("*.py"):
            if "test" in py_file.name:
                continue

            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # 查找公共函数/类 (非下划线开头)
            public_defs = re.findall(r"^(async\s+)?def\s+([a-zA-Z_]\w*)\s*\(", content, re.MULTILINE)

            for is_async, func_name in public_defs:
                if func_name.startswith("_"):
                    continue

                # 检查是否有文档字符串
                pattern = rf"def\s+{func_name}\s*\([^)]*\).*?(?=\n    \w|\nclass|\Z)"
                matches = re.findall(pattern, content, re.DOTALL | re.MULTILINE)

                if matches:
                    doc = matches[0]
                    if '"""' not in doc and "'''" not in doc:
                        self.issues.append({
                            "rule": "PPQA-C1",
                            "file": str(py_file),
                            "func": func_name,
                            "message": f"公共函数 {func_name} 缺少文档注释"
                        })

    def check_no_hardcoded_config(self):
        """检查是否有硬编码配置"""
        print("[PPQA-C2] 硬编码配置检查...")

        patterns = [
            (r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "IP地址硬编码"),
            (r"password\s*=\s*['\"][^$]", "密码硬编码"),
            (r"api[_-]?key\s*=\s*['\"][^$]", "API Key硬编码"),
            (r"conn.*=['\"]\s*postgresql.*://", "数据库连接硬编码"),
        ]

        for py_file in self.root_dir.rglob("*.py"):
            if "test" in py_file.name:
                continue

            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            for pattern, desc in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.issues.append({
                        "rule": "PPQA-C2",
                        "file": str(py_file),
                        "message": f"发现硬编码: {desc}"
                    })

    def check_error_handling(self):
        """检查错误处理完善性"""
        print("[PPQA-C3] 错误处理检查...")

        for py_file in self.root_dir.rglob("*.py"):
            if "test" in py_file.name:
                continue

            with open(py_file, encoding="utf-8") as f:
                content = f.read()

            # 检查是否有裸露的 except
            bare_excepts = re.findall(r"except\s*:", content)
            if bare_excepts:
                self.issues.append({
                    "rule": "PPQA-C3",
                    "file": str(py_file),
                    "message": f"发现 {len(bare_excepts)} 处裸露的 except:，应指定异常类型"
                })

    def check_test_coverage(self):
        """检查测试覆盖率"""
        print("[PPQA-C4] 测试覆盖率检查...")

        # 假设使用 pytest + coverage
        coverage_file = self.root_dir / "htmlcov" / "coverage.txt"

        if coverage_file.exists():
            with open(coverage_file) as f:
                for line in f:
                    if line.startswith("TOTAL"):
                        coverage = float(line.split()[2].replace("%", ""))
                        if coverage < 80:
                            self.issues.append({
                                "rule": "PPQA-C4",
                                "file": "coverage",
                                "message": f"测试覆盖率 {coverage}% < 80%"
                            })
        else:
            print("  (跳过: 未找到覆盖率报告)")

    def print_summary(self):
        """打印检查摘要"""
        print("\n" + "=" * 50)
        print("检查摘要")
        print("=" * 50)

        if self.issues:
            print(f"❌ 发现 {len(self.issues)} 个问题:\n")
            for issue in self.issues:
                print(f"  [{issue['rule']}] {issue['file']}")
                print(f"    → {issue['message']}\n")
        else:
            print("✅ 所有检查通过!")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    checker = PPQAChecker(root)
    success = checker.check_all()
    sys.exit(0 if success else 1)
```

- [ ] **Step 2: 创建 `enhanced/rules/ppqa-checklist.md`**

```markdown
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
```

---

## Task 5: 修改各角色 SKILL.md 添加快速通道

**目标:** 在 architect/backend/frontend/ui-designer/testing 的 SKILL.md 中添加简化流程入口

### 步骤

- [ ] **Step 1: 修改 `enhanced/architect/SKILL.md`** - 在执行流程后添加快速通道说明

在 "执行流程" 章节后添加:

```markdown
### 快速通道 (Fast Track)

**适用条件:** XS/S 任务且满足以下所有条件:
- [ ] 改动 ≤ 2个文件
- [ ] 无新增 API 契约
- [ ] 无数据库 schema 变更
- [ ] 用户明确同意简化流程

**快速通道路径:**
```
F1: [RD] 需求确认 (5分钟) → 1页简化设计
F2: [PMC] 直接派发任务清单 (5分钟)
```

**详细规则见:** `../FAST-TRACK.md`

---

### 禁止行为 (新增)
- 禁止将 L/XL 任务放入快速通道
- 禁止在快速通道中跳过交接确认
```

- [ ] **Step 2: 修改 `enhanced/backend/SKILL.md`** - 添加简化流程条件

在 "禁止行为" 章节添加:

```markdown
### 新增禁止行为
- 禁止在简化流程中跳过自检
- 禁止使用快速通道处理 L/XL 任务
```

在 "执行流程" 章节修改:

```markdown
### 固定流程

```
Step 0: [RD]   执行 requirements-clarify.md  → 需求澄清（如需要）
Step 1: [PMC]  执行 planning.md             → 输出开发计划表
Step 2: [VER]  执行 tdd.md                  → TDD 红→绿→重构 循环
Step 3: [PPQA] 执行 ppqa.md                 → 合规性检查 + 质量审计
Step 4: [OPP]  执行 metrics.md             → 量化指标报告
```

### 简化流程 (Fast Track - S任务)

当任务类型为 S (Small) 时，可简化为:
```
F1: [RD] 需求确认 (5分钟)
F2: [PMC] 简化开发计划 (10分钟)
F3: [VER+PPQA] 实现 + 自检 (15分钟)
F4: [OPP] 简化指标报告 (5分钟)
```

**判定规则见:** `../rules/fast-track-rules.md`
```

- [ ] **Step 3: 类似修改** `frontend/SKILL.md`, `ui-designer/SKILL.md`, `testing/SKILL.md`

---

## Task 6: 创建 LLR 收集脚本

**目标:** 新增 `scripts/llr-collect.py`，辅助收集和检索经验教训

### 步骤

- [ ] **Step 1: 创建 `enhanced/scripts/llr-collect.py`**

```python
#!/usr/bin/env python3
"""
LLR (Lessons Learned Report) 收集脚本
功能:
1. 创建新的 LLR 文档
2. 搜索已有的 LLR
3. 推荐相关经验
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

LLR_DIR = Path("knowledge/llr")

class LLRCollector:
    def __init__(self):
        self.llr_dir = LLR_DIR
        self.llr_dir.mkdir(parents=True, exist_ok=True)

    def create_llr(self, project_name: str, author: str, data: Dict):
        """创建新的 LLR 文档"""
        filename = f"{datetime.now().strftime('%Y-%m-%d')}-{project_name}.md"
        filepath = self.llr_dir / filename

        content = self._generate_llr_content(project_name, author, data)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        # 同时生成 JSON 索引
        self._update_index(project_name, filename, data)

        print(f"✅ LLR 已创建: {filepath}")
        return filepath

    def search_llr(self, keyword: str) -> List[Dict]:
        """搜索相关 LLR"""
        results = []
        index_file = self.llr_dir / "index.json"

        if not index_file.exists():
            print("⚠️ 未找到索引文件，请先创建 LLR")
            return results

        with open(index_file) as f:
            index = json.load(f)

        keyword_lower = keyword.lower()
        for item in index.get("items", []):
            if (keyword_lower in item.get("project", "").lower() or
                keyword_lower in item.get("tags", [])):
                results.append(item)

        return results

    def _generate_llr_content(self, project_name: str, author: str, data: Dict) -> str:
        """生成 LLR Markdown 内容"""
        return f"""# 经验教训报告: {project_name}

## 基本信息

| 字段 | 内容 |
|------|------|
| 项目名称 | {project_name} |
| 完成日期 | {datetime.now().strftime('%Y-%m-%d')} |
| 收集人 | {author} |
| 参与角色 | {data.get('roles', 'N/A')} |

## 做得好的

{self._format_list(data.get('what_worked', []))}

## 需要改进的

{self._format_improvements(data.get('improvements', []))}

## 下次同类任务建议

{self._format_list(data.get('recommendations', []))}

## 量化指标

| 指标 | 值 |
|------|------|
| 工时 (小时) | {data.get('hours', 'N/A')} |
| 缺陷数 | {data.get('defects', 'N/A')} |
| 测试覆盖率 | {data.get('coverage', 'N/A')} |

## 标签

{', '.join(data.get('tags', []))}
"""

    def _format_list(self, items: List[str]) -> str:
        if not items:
            return "- (无)"
        return "\n".join(f"- {item}" for item in items)

    def _format_improvements(self, items: List[Dict]) -> str:
        if not items:
            return "- (无)"
        result = ""
        for item in items:
            result += f"- **{item.get('issue', 'N/A')}** (影响: {item.get('impact', 'N/A')})\n"
            result += f"  建议: {item.get('suggestion', 'N/A')}\n"
        return result

    def _update_index(self, project_name: str, filename: str, data: Dict):
        """更新 LLR 索引"""
        index_file = self.llr_dir / "index.json"

        if index_file.exists():
            with open(index_file) as f:
                index = json.load(f)
        else:
            index = {"items": []}

        index["items"].append({
            "project": project_name,
            "filename": filename,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tags": data.get("tags", []),
            "summary": data.get("summary", "")
        })

        with open(index_file, "w") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  创建 LLR: python llr-collect.py create <project_name>")
        print("  搜索 LLR: python llr-collect.py search <keyword>")
        return

    command = sys.argv[1]

    if command == "create":
        project = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        collector = LLRCollector()

        # 示例数据，实际使用时应交互式收集
        data = {
            "roles": sys.argv[3] if len(sys.argv) > 3 else "N/A",
            "what_worked": ["流程清晰", "分工明确"],
            "improvements": [
                {"issue": "交接文档不完整", "impact": "中", "suggestion": "使用标准模板"}
            ],
            "recommendations": ["下次加强交接检查"],
            "hours": "8",
            "defects": "2",
            "coverage": "85%",
            "tags": ["backend", "fastapi"],
            "summary": "项目顺利完成，交接环节需改进"
        }

        collector.create_llr(project, "System", data)

    elif command == "search":
        keyword = sys.argv[2] if len(sys.argv) > 2 else ""
        collector = LLRCollector()
        results = collector.search_llr(keyword)

        if results:
            print(f"找到 {len(results)} 条相关记录:\n")
            for r in results:
                print(f"  [{r['date']}] {r['project']}")
                print(f"    标签: {', '.join(r.get('tags', []))}\n")
        else:
            print("未找到相关记录")

    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
```

---

## Task 7: 更新 Architect CAR.md 增加 Hotfix 场景

**目标:** 在 architect/car.md 中增加快速根因分析流程

### 步骤

- [ ] **Step 1: 读取并更新 `enhanced/architect/car.md`**

在文件末尾添加:

```markdown
---

## 快速 CAR (Hotfix 场景)

当问题为 Hotfix (已知bug快速修复) 时，可使用简化 CAR:

### 简化流程 (15分钟)

```
F1: 确认问题 (2分钟)
    → 重现步骤是什么？
    → 根本原因是否已知？

F2: 如果原因已知 → 直接修复 + 验证
    如果原因未知 → 走完整 CAR

F3: 记录教训 (5分钟)
    → 写1句话: 这次学到了什么？

F4: 更新知识库 (3分钟)
    → 如果是新类型问题，加入 known-issues.md
```

### 简化模板

```markdown
## Hotfix 教训记录

| 字段 | 内容 |
|------|------|
| 问题 | {problem_one_liner} |
| 根因 | {root_cause} |
| 修复 | {fix_description} |
| 学到 | {lesson_learned} |
| 日期 | {date} |
```
```

---

## 验证清单

完成上述所有 Task 后，验证以下文件存在且正确:

- [ ] `enhanced/FAST-TRACK.md` - 快速通道总览
- [ ] `enhanced/rules/fast-track-rules.md` - 判定规则
- [ ] `enhanced/rules/ppqa-checklist.md` - PPQA 自检清单
- [ ] `enhanced/handoff/architect-to-dev.md` - 交接模板
- [ ] `enhanced/handoff/dev-to-tester.md` - 交接模板
- [ ] `enhanced/handoff/llr-template.md` - LLR 模板
- [ ] `enhanced/scripts/ppqa-check.py` - PPQA 检查脚本
- [ ] `enhanced/scripts/llr-collect.py` - LLR 收集脚本
- [ ] `enhanced/architect/SKILL.md` - 已更新(含快速通道)
- [ ] `enhanced/backend/SKILL.md` - 已更新(含简化流程)
- [ ] `enhanced/architect/car.md` - 已更新(含 Hotfix 场景)
```

---

## 执行建议

| 顺序 | Task | 预计工时 | 依赖 |
|------|------|----------|------|
| 1 | Task 1 | 30分钟 | 无 |
| 2 | Task 2 | 45分钟 | Task 1 |
| 3 | Task 3 | 60分钟 | Task 1 |
| 4 | Task 4 | 90分钟 | Task 2 |
| 5 | Task 5 | 30分钟 | Task 1-2 |
| 6 | Task 6 | 45分钟 | Task 3 |
| 7 | Task 7 | 20分钟 | 无 |

**总计:** 约 5 小时

---

## 预期收益

| 改进点 | 改进前 | 改进后 |
|--------|--------|--------|
| 小任务流程时间 | 2-4小时 | 30分钟 |
| 交接文档完整性 | 依赖人工 | 模板强制 |
| PPQA 检查 | 人工检查 | 脚本自动 |
| 经验复用 | 无 | 可搜索知识库 |
| Hotfix 处理 | 走完整CAR | 15分钟 |
