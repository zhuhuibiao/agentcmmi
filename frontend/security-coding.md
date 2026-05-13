# 前端安全编码规范 (Frontend Security Coding Standards)

## 概述

本子技能为 Frontend 角色提供安全编码规范，涵盖 **OWASP Top 10 (2021)** 前端相关漏洞防护。

**CMMI 过程域：** PPQA (代码层安全)

**适用框架：** React / Vue / Angular / 原生 JavaScript

---

## 1. XSS 防护 (A03 - Injection)

### 1.1 React

```tsx
// ✅ 正确：使用 textContent 或 JSX 自动转义
const UserName = ({ name }: { name: string }) => (
  <span>{name}</span>  // 自动转义
);

// ❌ 错误：dangerouslySetInnerHTML
const BadComponent = ({ content }: { content: string }) => (
  <div dangerouslySetInnerHTML={{ __html: content }} />  // XSS风险!
);

// ✅ 正确：仅在确认安全时使用 sanitize-html
import DOMPurify from 'dompurify';

const SafeContent = ({ html }: { html: string }) => {
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong'],
    ALLOWED_ATTR: []
  });
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
};
```

### 1.2 Vue

```vue
<!-- ✅ 正确：默认自动转义 -->
<template>
  <span>{{ userName }}</span>
</template>

<!-- ❌ 错误：v-html -->
<template>
  <div v-html="userContent"></div>  <!-- XSS风险! -->
</template>

<!-- ✅ 正确：仅在确认安全时使用 -->
<template>
  <div v-html="sanitize(userContent)"></div>
</template>

<script>
import DOMPurify from 'dompurify';
export default {
  methods: {
    sanitize(html) {
      return DOMPurify.sanitize(html, { ALLOWED_TAGS: ['b', 'i'] });
    }
  }
}
</script>
```

### 1.3 原生 JavaScript

```javascript
// ❌ 错误：innerHTML 直接赋值
document.getElementById('output').innerHTML = userInput;  // XSS风险!

// ✅ 正确：textContent
document.getElementById('output').textContent = userInput;  // 安全

// ✅ 正确：textNode
const textNode = document.createTextNode(userInput);
element.appendChild(textNode);

// ✅ 正确：createElement + textContent
const div = document.createElement('div');
div.textContent = userInput;
document.body.appendChild(div);
```

---

## 2. CSRF 防护 (A01 - Broken Access Control)

### 2.1 前端 CSRF 令牌

```tsx
// React + Fetch API
const fetchWithCSRF = async (url: string, options: RequestInit = {}) => {
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'X-CSRFToken': csrfToken || '',
    },
    credentials: 'include'  // 发送 cookies
  });
};

// 使用
const response = await fetchWithCSRF('/api/data', {
  method: 'POST',
  body: JSON.stringify({ data: 'value' })
});
```

### 2.2 SameSite Cookie

```javascript
// 服务器端设置 (示例)
Set-Cookie: sessionid=abc123; SameSite=Strict; Secure; HttpOnly
```

---

## 3. 注入防护 (A03 - Injection)

### 3.1 URL 参数处理

```typescript
// ✅ 正确：使用 URLSearchParams
const params = new URLSearchParams();
params.append('search', userInput);
fetch(`/api/search?${params.toString()}`);

// ❌ 错误：字符串拼接
fetch(`/api/search?q=${userInput}`);  // URL注入风险!
```

### 3.2 DOM 操作

```typescript
// ✅ 正确：setAttribute + 白名单
element.setAttribute('data-id', sanitizeId(userInput));

// ❌ 错误：直接设置 src/href
element.setAttribute('src', userUrl);  // 可能被诱导到恶意URL
```

---

## 4. 敏感信息处理

### 4.1 前端存储

```typescript
// ❌ 错误：localStorage 存储敏感信息
localStorage.setItem('token', jwtToken);  // XSS可读取!

// ✅ 正确：仅存储非敏感数据，或使用 HttpOnly cookie
// 敏感数据应由服务器通过 HttpOnly Cookie 管理

// ✅ 正确：sessionStorage 用于临时存储
sessionStorage.setItem('draft', formData);
```

### 4.2 日志脱敏

```typescript
const sensitiveKeys = ['password', 'token', 'apiKey', 'ssn', 'creditCard'];

const sanitizeForLog = (data: any): any => {
  if (typeof data !== 'object') return data;

  const sanitized = { ...data };
  for (const key of sensitiveKeys) {
    if (key in sanitized) {
      sanitized[key] = '***REDACTED***';
    }
  }
  return sanitized;
};

console.log('User update:', sanitizeForLog(userData));
```

---

## 5. Content Security Policy (CSP)

### 5.1 CSP Header 配置

```html
<!-- index.html 或服务器配置 -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self' 'nonce-{random}';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data: https:;
               connect-src 'self' https://api.example.com;
               font-src 'self'">
```

### 5.2 React CSP 兼容

```tsx
// 使用 nonce 管理脚本
const Script = ({ nonce, src }: { nonce: string; src: string }) => (
  <script src={src} nonce={nonce} />
);
```

---

## 6. 输入验证

### 6.1 React 表单验证

```tsx
import { z } from 'zod';

const UserSchema = z.object({
  email: z.string().email('Invalid email format'),
  age: z.number().min(0).max(150),
  url: z.string().url().optional(),
});

const validateInput = (data: unknown) => {
  try {
    return { success: true, data: UserSchema.parse(data) };
  } catch (e) {
    return { success: false, error: e };
  }
};
```

---

## 7. 安全检查清单

### 开发前
- [ ] 无 dangerouslySetInnerHTML/v-html 使用（除非经 sanitize）
- [ ] 用户输入使用 textContent，不使用 innerHTML
- [ ] Cookie 设置 SameSite=Strict

### 开发中
- [ ] URL 参数使用 URLSearchParams
- [ ] 无 eval/new Function 处理用户输入
- [ ] CSP meta 标签已配置

### 开发后
- [ ] 运行 `ppqa-security-check.py` 无 XSS 报警
- [ ] 无敏感信息存储在 localStorage/sessionStorage
- [ ] 第三方依赖无已知漏洞 (`npm audit`)

---

## 8. OWASP Top 10 映射 (前端)

| 漏洞 | 防护措施 | 验证方法 |
|------|----------|----------|
| A01: Access Control | CSRF Token + SameSite Cookie | 接口测试 |
| A03: Injection | textContent + sanitize-html | ppqa-security-check.py |
| A05: Security Misconfiguration | CSP Header | 安全扫描 |
| A06: Vulnerable Components | npm audit | 依赖扫描 |

---

## 9. 禁止行为

- 禁止使用 dangerouslySetInnerHTML（除非经过 DOMPurify 净化）
- 禁止使用 innerHTML 处理用户输入
- 禁止在 URL 中直接拼接用户输入
- 禁止在 localStorage 存储 JWT/Token/Password
- 禁止使用 eval/new Function 处理数据