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