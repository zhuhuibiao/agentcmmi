---
name: frontend-ppqa
description: 前端PPQA验证子技能。合规性检查、质量审计。触发时机：代码实现完成，准备交付前。
version: 1.0.0
cmmi_process_area: PPQA
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# PPQA 验证

## 用途
合规性检查、质量审计。

## 触发时机
代码实现完成，准备交付前。

## 输入
- 源代码
- 设计文档
- UI设计文档

## 输出
```markdown
## 质量审计报告

### 合规性检查
| 检查项 | 状态 | 备注 |
|--------|------|------|
| API地址一致性 | ✅ 通过 | 全部匹配 |
| 请求字段一致性 | ✅ 通过 | 全部匹配 |
| 响应字段一致性 | ✅ 通过 | 全部匹配 |
| 权限控制 | ✅ 通过 | 与设计文档一致 |
| 页面风格 | ✅ 通过 | 与当前系统一致 |
| Build | ✅ 通过 | 无错误 |
| Playwright | ✅ 通过 | 全部通过 |

### 未解决问题
- [无 / 列出问题及修复方案]
```

## 执行步骤

```
1. [PPQA-1] 执行合规性检查清单
2. [PPQA-2] 运行 linter (ESLint)
3. [PPQA-3] 运行类型检查 (TypeScript)
4. [PPQA-4] 执行 npm run build
5. [PPQA-5] 执行 Playwright 测试
6. [PPQA-6] 验证 API 契约与设计文档一致
7. [PPQA-7] 生成《质量审计报告》
```

## 合规性检查清单

```
□ 设计文档中的API地址全部实现
□ 请求URL与后端路由完全一致（不含尾部斜杠依赖）
□ 请求字段与设计文档一致
□ 响应字段与设计文档一致
□ 权限控制与设计文档一致
□ 页面风格与当前系统一致
□ 测试覆盖设计文档定义的全部功能
□ Build 成功
□ Playwright 测试通过
□ 复用现有组件，不引入新的视觉语言
```

## Playwright 测试执行模板

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
- 禁止跳过任何合规检查项
- 禁止带着失败的测试提交
- 禁止引入新的视觉语言