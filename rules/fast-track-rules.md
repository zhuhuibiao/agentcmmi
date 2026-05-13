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
