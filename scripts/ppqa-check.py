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