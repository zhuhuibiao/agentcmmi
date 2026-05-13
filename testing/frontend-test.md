---
name: testing-frontend-test
description: 测试工程师前端测试子技能。执行Playwright测试。触发条件：测试计划完成。
version: 1.0.0
cmmi_process_area: VER
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# 前端测试 (VER)

## 用途
执行Playwright测试。

## 触发时机
测试计划完成。

## 输入
- 前端测试文件: frontend/tests/<group>/<tool-key>/index.spec.ts
- 测试计划

## 输出
```markdown
## 前端测试执行记录

### 测试结果
| 测试项 | 状态 | 备注 |
|--------|------|------|
| 工具入口 | ✅ 通过 | - |
| 核心成功流程 | ✅ 通过 | - |
| 失败分支 | ✅ 通过 | - |
| 状态分支 | ✅ 通过 | - |

### 失败项（如有）
| 测试名称 | 失败原因 | 错误日志 |
|---------|---------|---------|
| - | - | - |
```

## 执行步骤

```
1. [VER-1] 执行前端测试文件
2. [VER-2] 逐条执行测试
3. [VER-3] 记录通过/失败项
4. [VER-4] 如失败，记录:
   - 失败测试名称
   - 失败原因
   - 最后一段可用日志
```

## Playwright 执行模板

```powershell
$wd = "D:\document\projects\{project}\frontend"
$spec = "tests\<group>\<tool-key>\index.spec.ts"
$out = Join-Path $wd "playwright.out.log"
$err = Join-Path $wd "playwright.err.log"
if (Test-Path $out) { Remove-Item $out -Force }
if (Test-Path $err) { Remove-Item $err -Force }
$p = Start-Process -FilePath "cmd.exe" -ArgumentList "/d /s /c npx playwright test $spec --reporter=line" -WorkingDirectory $wd -RedirectStandardOutput $out -RedirectStandardError $err -PassThru
$deadline = (Get-Date).AddSeconds(600)
while (-not $p.HasExited) {
    Start-Sleep -Seconds 2
    $p.Refresh()
    if ((Get-Date) -ge $deadline) {
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        exit 124
    }
}
# ... 错误处理和日志输出
```

## 禁止行为
- 禁止跳过前端测试文件中的任何测试