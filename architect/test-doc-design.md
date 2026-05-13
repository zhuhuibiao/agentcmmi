---
name: architect-test-doc-design
description: 架构师测试文档生成子技能。生成完整测试用例文档（HTML table格式）。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 测试文档 (PPQA)

## 用途
生成完整测试用例文档，必须输出为HTML table格式，包含完整curl示例和预期结果。

## 输入
- API设计文档（来自 api-design-doc.md）
- 设计文档路径（已存储）

## 输出
HTML table格式的测试文档，包含：
- 接口名称
- curl 示例
- 预期成功响应
- 预期失败响应
- 测试覆盖场景

## 执行步骤

```
1. [PPQA-1] 读取API设计文档
2. [PPQA-2] 为每个API生成测试用例
3. [PPQA-3] 生成完整 curl 示例
4. [PPQA-4] 定义预期成功/失败响应
5. [PPQA-5] 覆盖成功/失败分支
6. [PPQA-6] 输出测试文档
```

## 测试文档格式

```markdown
## 测试文档: {工具名称}

### 接口测试用例

| 用例编号 | 接口 | 操作 | curl示例 | 预期成功响应 | 预期失败响应 |
|---------|------|------|---------|------------|------------|
| TC-001 | /api/v1/{group}/{tool-key} | GET | curl ... | {...} | {...} |
| TC-002 | /api/v1/{group}/{tool-key} | POST | curl ... | {...} | {...} |
```

## curl 示例格式

```bash
curl -X POST "http://{host}:{port}/api/v1/{group}/{tool-key}" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "request_id": "uuid",
    "ts": 1234567890,
    "payload": {
      "field1": "value1"
    }
  }'
```

## PPQA 合规检查清单

```
□ 完整 curl 示例（每个接口至少一个）
□ 预期结果明确（成功/失败）
□ 覆盖全部 API
□ 覆盖全部用户流程
□ 包含成功/失败分支
□ 包含权限分支测试
```

## 禁止行为
- 禁止遗漏API设计文档中的任何接口
- 禁止跳过失败分支的测试用例