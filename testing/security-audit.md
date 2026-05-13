# 安全审计子技能 (Security Audit)

## 概述

本子技能为 Testing 角色提供安全专项审计能力，覆盖 **OWASP Top 10 (2021)** 漏洞检测。

**CMMI 过程域：** PPQA + VER

**触发条件：**
- 后端代码交付前
- API 接口交付前
- 新增用户输入功能时
- 定期安全扫描时

---

## 1. OWASP Top 10 检查清单

| 序号 | 漏洞类型 | 严重度 | 检查方法 |
|------|----------|--------|----------|
| A01 | Broken Access Control | 🔴 高 | 权限边界测试 |
| A02 | Cryptographic Failures | 🔴 高 | 敏感数据检查 |
| A03 | Injection | 🔴 高 | SQL/XSS/命令注入测试 |
| A04 | Insecure Design | 🟡 中 | 威胁建模评审 |
| A05 | Security Misconfiguration | 🟡 中 | 配置审计 |
| A06 | Vulnerable Components | 🟡 中 | 依赖扫描 |
| A07 | Identification Failures | 🟡 中 | 认证测试 |
| A08 | Software Integrity Failures | 🟡 中 | 签名验证 |
| A09 | Logging Failures | 🟢 低 | 日志审计 |
| A10 | SSRF | 🟡 中 | URL 验证测试 |

---

## 2. SQL 注入检测 (A03-Injection)

### 2.1 高风险模式识别

```
🚨 SQL 注入高风险场景:
- 用户输入直接拼接入 SQL
- 未使用参数化查询的数据库操作
- ORDER BY、LIKE 等动态字段未校验
```

### 2.2 测试用例

```
### SQL 注入测试用例

#### TC-SQL-001: 基础注入测试
输入: ' OR '1'='1
预期: 查询失败或被转义，不返回额外数据

#### TC-SQL-002: UNION 注入测试
输入: ' UNION SELECT NULL--
预期: 查询失败，拒绝非法 UNION

#### TC-SQL-003: 布尔盲注测试
输入: ' AND 1=1 --
预期: 正常返回
输入: ' AND 1=2 --
预期: 无数据或错误（确认注入点）

#### TC-SQL-004: 时间盲注测试
输入: '; WAITFOR DELAY '00:00:05'--
预期: 响应延迟 >5秒则存在注入

#### TC-SQL-005: ORDER BY 注入测试
输入: 1; DROP TABLE users--
预期: 拒绝操作或查询失败
```

### 2.3 防御验证检查点

```
✅ 参数化查询 (Prepared Statements)
✅ ORM 框架的正确使用
✅ 输入类型校验（数字/字母/邮箱格式）
✅ 最小权限原则（数据库账户）
✅ 错误信息不泄露 SQL 结构
```

---

## 3. XSS 跨站脚本检测 (A03-Injection)

### 3.1 高风险模式识别

```
🚨 XSS 高风险场景:
- 用户输入未转义直接渲染到 HTML
- JavaScript 动态生成内容未编码
- 富文本编辑器输出未净化
```

### 3.2 测试用例

```
### XSS 测试用例

#### TC-XSS-001: 基础 Script 标签
输入: <script>alert('XSS')</script>
预期: 被转义或拒绝，不弹窗

#### TC-XSS-002: 事件处理器
输入: <img src=x onerror=alert('XSS')>
预期: 被转义，不执行

#### TC-XSS-003: JavaScript URL
输入: javascript:alert('XSS')
预期: 被转义或过滤

#### TC-XSS-004: SVG 标签
输入: <svg onload=alert('XSS')>
预期: 被转义，不执行

#### TC-XSS-005: 存储型 XSS
输入: <script>alert('stored')</script>
预期: 保存成功但读取时已转义
```

### 3.3 防御验证检查点

```
✅ 输出编码（HTML/URL/JS/CSSContext）
✅ Content-Security-Policy 头配置
✅ HttpOnly + Secure Cookie 属性
✅ 输入长度限制
✅ 白名单过滤（富文本）
```

---

## 4. 认证与授权测试 (A01 + A07)

### 4.1 认证测试

```
### 认证测试用例

#### TC-AUTH-001: 密码强度
输入: 123456
预期: 拒绝，提示密码强度不足

#### TC-AUTH-002: 暴力防护
操作: 连续5次错误登录
预期: 账户锁定或 CAPTCHA 触发

#### TC-AUTH-003: Session 安全
检查: Session ID 随机性、HttpOnly、Secure、SameSite
预期: 符合安全配置

#### TC-AUTH-004: 密码找回流程
检查: 重置链接是否一次性、过期时间
预期: 安全流程设计合理
```

### 4.2 授权测试

```
### 授权测试用例

#### TC-AUTH-005: 垂直越权
操作: 低权限用户访问高权限 API
预期: 403 Forbidden

#### TC-AUTH-006: 水平越权
操作: 用户A访问用户B的数据
预期: 403 Forbidden 或 404 Not Found

#### TC-AUTH-007: IDOR 诱导
操作: 替换资源 ID 参数
预期: 拒绝未授权访问
```

---

## 5. 其他常见漏洞测试

### 5.1 命令注入 (A03-Injection)

```
### 命令注入测试用例

#### TC-CMD-001: 命令分隔
输入: ; ls -la
预期: 拒绝或无输出

#### TC-CMD-002: 管道注入
输入: | cat /etc/passwd
预期: 拒绝或无输出

#### TC-CMD-003: 反引号注入
输入: `whoami`
预期: 拒绝执行
```

### 5.2 反序列化漏洞 (A08)

```
### 反序列化测试用例

#### TC-DES-001: Python pickle 反序列化
输入: 恶意 pickle 对象（模拟）
预期: 拒绝反序列化或抛出异常

#### TC-DES-002: JSON 反序列化
输入: {"__type__": "注入内容"}
预期: 被拒绝或安全处理
```

### 5.3 SSRF 服务端请求伪造 (A10)

```
### SSRF 测试用例

#### TC-SSRF-001: 内部 IP 访问
输入: http://169.254.169.254/ (AWS metadata)
预期: 拒绝访问内部端点

#### TC-SSRF-002: 本地主机访问
输入: http://127.0.0.1:port/admin
预期: 拒绝或返回 404
```

---

## 6. 安全测试执行流程

```
Step 1: [PPQA] 代码静态分析
   ↓
   ├─ 运行 ppqa-security-check.py
   ├─ 检查 SQL 注入模式
   └─ 检查 XSS 注入模式

Step 2: [VER] 动态测试
   ↓
   ├─ 执行 API 安全测试用例
   ├─ 执行认证授权测试
   └─ 执行边界值测试

Step 3: [PPQA] 报告输出
   ↓
   └─ 输出《安全审计报告》
```

---

## 7. 安全审计报告模板

```markdown
# 安全审计报告

## 基本信息
- 项目名称: {name}
- 审计时间: {date}
- 审计范围: {scope}
- 审计方法: {静态分析/动态测试/代码审计}

## OWASP Top 10 检查结果

| 序号 | 漏洞类型 | 发现数量 | 严重度 | 状态 |
|------|----------|----------|--------|------|
| A01 | Broken Access Control | 0 | - | ✅ |
| A02 | Cryptographic Failures | 0 | - | ✅ |
| A03 | Injection | 0 | - | ✅ |
| ... | ... | ... | ... | ... |

## 详细发现

### [A03] SQL 注入
| 文件 | 位置 | 描述 | 严重度 | 修复建议 |
|------|------|------|--------|----------|
| - | - | - | - | - |

### [A03] XSS
| 文件 | 位置 | 描述 | 严重度 | 修复建议 |
|------|------|------|--------|----------|
| - | - | - | - | - |

## 风险汇总
- 🔴 高风险: {n}
- 🟡 中风险: {n}
- 🟢 低风险: {n}

## 修复验证
- [ ] A01 修复验证 ✅/❌
- [ ] A03 SQL 修复验证 ✅/❌
- [ ] A03 XSS 修复验证 ✅/❌
- ...

## 结论
- [ ] 通过安全审计，可以交付
- [ ] 需要修复 {n} 个问题后重新审计
```

---

## 8. 禁止行为

- 禁止在未执行安全测试前交付代码
- 禁止跳过 A01 (Access Control) 和 A03 (Injection) 的测试
- 禁止将未修复的高风险漏洞标记为通过
- 禁止使用生产环境数据进行安全测试

---

## 9. 参考标准

- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE Top 25](https://cwe.mitre.org/top25/)