#!/usr/bin/env python3
"""
PPQA 安全专项检查脚本
覆盖 OWASP Top 10 (2021) 漏洞模式检测

检查项:
C5: SQL 注入模式
C6: XSS 注入模式
C7: 命令注入模式
C8: 反序列化漏洞模式
C9: SSRF 诱导模式
C10: 敏感信息泄露模式
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class SecurityIssue:
    rule: str
    file: str
    line: str
    code_snippet: str
    vulnerability_type: str
    severity: str
    message: str
    cwe: str


class PPSecurityChecker:
    # 支持的语言及对应注释模式
    COMMENT_PATTERNS = {
        '.py': ['#', '"""', "'''"],
        '.js': ['//', '/*', '*/'],
        '.ts': ['//', '/*', '*/'],
        '.java': ['//', '/*', '*/'],
        '.go': ['//', '/*', '*/'],
        '.sql': ['--', '/*', '*/'],
    }

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.issues: List[SecurityIssue] = []

        # SQL 注入高风险模式 (C5)
        self.sql_injection_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'execute\s*\(\s*f["\']', 'SQL注入: f-string动态SQL', 'CWE-89'),
            (r'execute\s*\(\s*["\'].*%s.*["\'].*%', 'SQL注入: 字符串格式化', 'CWE-89'),
            (r'cursor\.execute\s*\([^)]*format\s*\(', 'SQL注入: .format()拼接', 'CWE-89'),
            (r'cursor\.execute\s*\([^)]*\+[^)]+\)', 'SQL注入: 字符串拼接', 'CWE-89'),
            (r'select.*from.*where.*\+', 'SQL注入: SELECT动态拼接', 'CWE-89'),
            (r'insert\s+into.*\+', 'SQL注入: INSERT动态拼接', 'CWE-89'),
            (r'delete\s+from.*\+', 'SQL注入: DELETE动态拼接', 'CWE-89'),
            (r'update.*set.*\+', 'SQL注入: UPDATE动态拼接', 'CWE-89'),
            (r'\$\{.*\}', 'SQL注入: 模板字符串动态SQL', 'CWE-89'),
            (r'\.replace\s*\(\s*["\'];', 'SQL注入: 危险替换', 'CWE-89'),
            # Node.js / JavaScript patterns
            (r'mysql\.query\s*\([^)]*\+', 'SQL注入: mysql拼接', 'CWE-89'),
            (r'pool\.query\s*\([^)]*\+', 'SQL注入: pool拼接', 'CWE-89'),
            (r'`.*SELECT.*\$\{', 'SQL注入: 模板字符串SELECT', 'CWE-89'),
            (r'`.*INSERT.*\$\{', 'SQL注入: 模板字符串INSERT', 'CWE-89'),
        ]

        # XSS 高风险模式 (C6)
        self.xss_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'innerHTML\s*=\s*(?!.*(textContent|sanitize))', 'XSS: innerHTML直接赋值', 'CWE-79'),
            (r'dangerouslySetInnerHTML', 'XSS: React危险API', 'CWE-79'),
            (r'document\.write\s*\(', 'XSS: document.write', 'CWE-79'),
            (r'\.html\s*\(\s*\$(?!.*sanitize)', 'XSS: jQuery html()未净化', 'CWE-79'),
            (r'res\.send\s*\(\s*req\.query', 'XSS: 反射型XSS', 'CWE-79'),
            (r'res\.render\s*\([^,]+,\s*\{[^}]*req\.', 'XSS: 模板引擎未转义', 'CWE-79'),
            (r'templatestring.*\$\{', 'XSS: 模板字符串未转义', 'CWE-79'),
            (r'eval\s*\(\s*req\.', 'XSS: eval处理用户输入', 'CWE-94'),
            (r'new\s+Function\s*\([^)]*req\.', 'XSS: Function构造器危险', 'CWE-94'),
            # Python patterns
            (r'MarkupString\s*\(', 'XSS: MarkupString未净化', 'CWE-79'),
            (r'|safe\s*\}', 'XSS: Django模板|safe过滤器', 'CWE-79'),
            (r'auto_escape\s*=\s*False', 'XSS: Jinja2关闭自动转义', 'CWE-79'),
        ]

        # 命令注入模式 (C7)
        self.command_injection_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'os\.system\s*\(', '命令注入: os.system()', 'CWE-78'),
            (r'os\.popen\s*\(', '命令注入: os.popen()', 'CWE-78'),
            (r'subprocess\.call\s*\([^)]*shell\s*=\s*True', '命令注入: subprocess shell=True', 'CWE-78'),
            (r'subprocess\.run\s*\([^)]*shell\s*=\s*True', '命令注入: subprocess shell=True', 'CWE-78'),
            (r'subprocess\.Popen\s*\([^)]*shell\s*=\s*True', '命令注入: subprocess shell=True', 'CWE-78'),
            (r'exec\s*\([^)]*%', '命令注入: exec格式化', 'CWE-78'),
            (r'eval\s*\([^)]*request', '命令注入: eval处理请求', 'CWE-94'),
            (r'child_process\.exec\s*\(', '命令注入: Node.js exec()', 'CWE-78'),
            (r'child_process\.execSync\s*\(', '命令注入: Node.js execSync()', 'CWE-78'),
            (r'execa\s*\(.*shell', '命令注入: execa shell参数', 'CWE-78'),
            (r'shell\.exec\s*\(', '命令注入: shell.exec()', 'CWE-78'),
        ]

        # 反序列化漏洞模式 (C8)
        self.deserialization_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'pickle\.loads?\s*\(', '反序列化: Python pickle', 'CWE-502'),
            (r'yaml\.load\s*\(', '反序列化: PyYAML未安全加载', 'CWE-502'),
            (r'yaml\.unsafe_load\s*\(', '反序列化: YAML unsafe_load', 'CWE-502'),
            (r'json\.loads\s*\(', '反序列化: JSON未验证类型', 'CWE-502'),
            (r'unserialize\s*\(', '反序列化: PHP unserialize()', 'CWE-502'),
            (r'ObjectInputStream', '反序列化: Java ObjectInputStream', 'CWE-502'),
            (r'XMLDecoder', '反序列化: Java XMLDecoder', 'CWE-502'),
            (r'readObject\s*\(', '反序列化: Java readObject', 'CWE-502'),
            (r'yaml\.load\s*\([^,)]*Loader\s*=\s*yaml\.FullLoader', '反序列化: PyYAML FullLoader安全', 'CWE-502'),
        ]

        # SSRF 诱导模式 (C9)
        self.ssrf_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'requests\.get\s*\([^)]*url[^)]*\)', 'SSRF: requests.get动态URL', 'CWE-918'),
            (r'urllib\.request\.urlopen\s*\(', 'SSRF: urllib urlopen', 'CWE-918'),
            (r'http\.get\s*\([^)]*url[^)]*\)', 'SSRF: Node http.get', 'CWE-918'),
            (r'fetch\s*\([^)]*url[^)]*\)', 'SSRF: fetch API', 'CWE-918'),
            (r'axios\.get\s*\([^)]*url[^)]*\)', 'SSRF: axios.get', 'CWE-918'),
            (r'curl_easy_perform', 'SSRF: libcurl', 'CWE-918'),
        ]

        # 敏感信息泄露模式 (C10)
        self.sensitive_info_patterns: List[Tuple[str, str, str]] = [
            # (正则模式, 漏洞类型, CWE)
            (r'password\s*=\s*["\'][^$]', '敏感信息: 密码硬编码', 'CWE-798'),
            (r'api[_-]?key\s*=\s*["\'][^$]', '敏感信息: API Key硬编码', 'CWE-798'),
            (r'secret[_-]?key\s*=\s*["\'][^$]', '敏感信息: Secret Key硬编码', 'CWE-798'),
            (r'access[_-]?token\s*=\s*["\'][^$]', '敏感信息: Access Token硬编码', 'CWE-798'),
            (r'private[_-]?key\s*=\s*["\'][^$]', '敏感信息: Private Key硬编码', 'CWE-798'),
            (r'aws[_-]?access[_-]?key', '敏感信息: AWS Access Key', 'CWE-798'),
            (r'aws[_-]?secret[_-]?key', '敏感信息: AWS Secret Key', 'CWE-798'),
            (r'github[_-]?token', '敏感信息: GitHub Token', 'CWE-798'),
            (r'bearer\s+[A-Za-z0-9_-]{20,}', '敏感信息: Bearer Token泄露', 'CWE-200'),
            (r'basic\s+[A-Za-z0-9_-]{10,}', '敏感信息: Basic Auth泄露', 'CWE-200'),
            (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', '敏感信息: 私钥文件', 'CWE-798'),
            (r'xox[baprs]-([A-Za-z0-9]{10,48})', '敏感信息: Slack Token', 'CWE-798'),
        ]

        # 严重度等级
        self.severity_map = {
            'CWE-89': '🔴 高',
            'CWE-79': '🔴 高',
            'CWE-78': '🔴 高',
            'CWE-94': '🔴 高',
            'CWE-502': '🟡 中',
            'CWE-918': '🟡 中',
            'CWE-798': '🔴 高',
            'CWE-200': '🟡 中',
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """判断是否跳过文件"""
        skip_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env',
                     'dist', 'build', '.venv', '.env', 'vendor', 'test',
                     'tests', '.pytest_cache', 'coverage', 'htmlcov'}
        skip_patterns = {'.min.js', '.bundle.js', 'test_', '_test.'}

        # 跳过目录
        if any(d in file_path.parts for d in skip_dirs):
            return True
        # 跳过测试文件
        if any(pattern in file_path.name for pattern in skip_patterns):
            return True
        return False

    def check_patterns(self, file_path: Path, content: str,
                      patterns: List[Tuple[str, str, str]], rule_prefix: str):
        """检查一组模式"""
        for i, line in enumerate(content.split('\n'), 1):
            for pattern, vuln_type, cwe in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # 提取代码片段（当前行及前后2行）
                    lines = content.split('\n')
                    start = max(0, i - 3)
                    end = min(len(lines), i + 2)
                    context = '\n'.join(f"  {j}: {l}" for j, l in enumerate(lines[start:end], start + 1))

                    severity = self.severity_map.get(cwe, '🟡 中')

                    issue = SecurityIssue(
                        rule=f"PPQA-{rule_prefix}",
                        file=str(file_path),
                        line=str(i),
                        code_snippet=line.strip()[:100],
                        vulnerability_type=vuln_type,
                        severity=severity,
                        message=f"发现 {vuln_type} (CWE: {cwe})",
                        cwe=cwe
                    )
                    self.issues.append(issue)

    def check_all(self) -> bool:
        """执行所有安全检查"""
        print("=" * 60)
        print("PPQA 安全专项检查 - OWASP Top 10")
        print("=" * 60)

        # 收集所有源文件
        source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java',
                            '.go', '.php', '.rb', '.cs', '.sql'}

        source_files = []
        for ext in source_extensions:
            source_files.extend(self.root_dir.rglob(f"*{ext}"))

        print(f"\n📁 扫描文件数: {len(source_files)}")

        # 执行各项检查
        self.check_sql_injection(source_files)
        self.check_xss(source_files)
        self.check_command_injection(source_files)
        self.check_deserialization(source_files)
        self.check_ssrf(source_files)
        self.check_sensitive_info(source_files)

        self.print_summary()
        return len([i for i in self.issues if '🔴 高' in i.severity]) == 0

    def check_sql_injection(self, files: List[Path]):
        """SQL 注入检查 (C5)"""
        print("\n[PPQA-C5] SQL 注入模式检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.sql_injection_patterns, "C5")
            except Exception:
                pass

    def check_xss(self, files: List[Path]):
        """XSS 检查 (C6)"""
        print("[PPQA-C6] XSS 注入模式检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.xss_patterns, "C6")
            except Exception:
                pass

    def check_command_injection(self, files: List[Path]):
        """命令注入检查 (C7)"""
        print("[PPQA-C7] 命令注入模式检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.command_injection_patterns, "C7")
            except Exception:
                pass

    def check_deserialization(self, files: List[Path]):
        """反序列化漏洞检查 (C8)"""
        print("[PPQA-C8] 反序列化漏洞模式检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.deserialization_patterns, "C8")
            except Exception:
                pass

    def check_ssrf(self, files: List[Path]):
        """SSRF 检查 (C9)"""
        print("[PPQA-C9] SSRF 诱导模式检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.ssrf_patterns, "C9")
            except Exception:
                pass

    def check_sensitive_info(self, files: List[Path]):
        """敏感信息泄露检查 (C10)"""
        print("[PPQA-C10] 敏感信息泄露检测...")
        for f in files:
            if self.should_skip_file(f):
                continue
            try:
                with open(f, encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                self.check_patterns(f, content, self.sensitive_info_patterns, "C10")
            except Exception:
                pass

    def print_summary(self):
        """打印检查摘要"""
        print("\n" + "=" * 60)
        print("安全检查摘要")
        print("=" * 60)

        if not self.issues:
            print("✅ 所有安全检查通过！未发现 OWASP Top 10 漏洞模式。")
            return

        # 按严重度分组
        high_severity = [i for i in self.issues if '🔴 高' in i.severity]
        medium_severity = [i for i in self.issues if '🟡 中' in i.severity]

        print(f"\n🔴 高风险: {len(high_severity)} 个")
        print(f"🟡 中风险: {len(medium_severity)} 个")
        print(f"总计: {len(self.issues)} 个问题\n")

        # 按类型分组显示
        vuln_types = {}
        for issue in self.issues:
            key = issue.vulnerability_type.split(':')[0]
            vuln_types[key] = vuln_types.get(key, 0) + 1

        print("问题类型分布:")
        for vtype, count in sorted(vuln_types.items(), key=lambda x: -x[1]):
            print(f"  {vtype}: {count}")

        print("\n" + "-" * 60)
        print("详细问题列表 (高风险优先):")
        print("-" * 60)

        for issue in sorted(self.issues, key=lambda x: (0 if '🔴' in x.severity else 1, -x.line.__len__())):
            print(f"\n[{issue.rule}] {issue.severity} {issue.file}:{issue.line}")
            print(f"  类型: {issue.vulnerability_type}")
            print(f"  代码: {issue.code_snippet}")
            print(f"  CWE: {issue.cwe}")
            print(f"  建议: 请使用参数化查询/输入验证/白名单过滤")

        print("\n" + "=" * 60)
        if high_severity:
            print("❌ 安全检查未通过！存在高风险漏洞，必须修复后才能交付。")
        else:
            print("⚠️  存在中风险漏洞，建议修复。")
        print("=" * 60)

    def generate_report(self, output_file: str = "security-audit-report.md"):
        """生成 Markdown 格式的安全审计报告"""
        report_path = self.root_dir / output_file

        high = [i for i in self.issues if '🔴 高' in i.severity]
        medium = [i for i in self.issues if '🟡 中' in i.severity]

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 安全审计报告\n\n")
            f.write("| 检查项 | 规则 | 说明 |\n")
            f.write("|--------|------|------|\n")
            f.write("| C5 | SQL 注入 | 参数化查询检查 |\n")
            f.write("| C6 | XSS 注入 | 输出编码检查 |\n")
            f.write("| C7 | 命令注入 | subprocess/eval 检查 |\n")
            f.write("| C8 | 反序列化 | pickle/yaml 检查 |\n")
            f.write("| C9 | SSRF | URL 验证检查 |\n")
            f.write("| C10 | 敏感信息 | 密钥/Token 检查 |\n\n")

            f.write("## 风险汇总\n\n")
            f.write(f"- 🔴 高风险: {len(high)} 个\n")
            f.write(f"- 🟡 中风险: {len(medium)} 个\n\n")

            if self.issues:
                f.write("## 详细问题\n\n")
                for issue in sorted(self.issues, key=lambda x: (0 if '🔴' in x.severity else 1)):
                    f.write(f"### [{issue.severity}] {issue.vulnerability_type}\n\n")
                    f.write(f"- **文件**: `{issue.file}:{issue.line}`\n")
                    f.write(f"- **规则**: `{issue.rule}`\n")
                    f.write(f"- **CWE**: {issue.cwe}\n")
                    f.write(f"- **代码**: `{issue.code_snippet}`\n\n")

        print(f"\n📄 报告已生成: {report_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PPQA 安全专项检查 - OWASP Top 10")
    parser.add_argument("path", nargs="?", default=".", help="要扫描的目录路径")
    parser.add_argument("--report", action="store_true", help="生成 Markdown 报告")
    parser.add_argument("--output", default="security-audit-report.md", help="报告输出文件名")

    args = parser.parse_args()

    checker = PPSecurityChecker(args.path)
    success = checker.check_all()

    if args.report:
        checker.generate_report(args.output)

    # 退出码: 高风险漏洞存在返回1, 否则返回0
    sys.exit(1 if not success else 0)
