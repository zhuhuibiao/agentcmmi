# 安全编码规范 (Security Coding Standards)

## 概述

本子技能为 Backend 角色提供安全编码规范，涵盖 **OWASP Top 10 (2021)** 防护措施。

**CMMI 过程域：** PPQA (代码层安全)

**适用语言：** Python / Go / Java / Node.js

---

## 1. SQL 注入防护 (A03 - Injection)

### 1.1 Python (FastAPI/Flask/Django)

```python
# ✅ 正确：参数化查询
from sqlalchemy import text

async def get_user(db, user_id: int):
    result = await db.execute(
        text("SELECT * FROM users WHERE id = :id"),
        {"id": user_id}
    )
    return result.fetchone()

# ❌ 错误：字符串拼接
async def get_user_bad(db, user_id: int):
    result = await db.execute(
        f"SELECT * FROM users WHERE id = {user_id}"  # SQL注入风险!
    )
    return result.fetchone()

# ✅ 正确：ORM 方式
from sqlalchemy import select
from models import User

async def get_user_orm(db, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
```

### 1.2 Go

```go
// ✅ 正确：参数化查询
func GetUser(db *sql.DB, userID int) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE id = ?", userID)
    var u User
    err := row.Scan(&u.ID, &u.Name, &u.Email)
    return &u, err
}

// ❌ 错误：fmt.Sprintf 拼接
func GetUserBad(db *sql.DB, userID int) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE id = %d", userID) // SQL注入风险!
    row := db.QueryRow(query)
    ...
}
```

### 1.3 Java (Spring Boot)

```java
// ✅ 正确：参数化查询
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    @Query("SELECT u FROM User u WHERE u.id = :id")
    Optional<User> findByIdParam(@Param("id") Long id);

    // 或使用内置方法
    Optional<User> findById(Long id);
}

// ❌ 错误：字符串拼接
@Query("SELECT u FROM User u WHERE u.id = " + userId)  // SQL注入风险!
```

### 1.4 Node.js

```javascript
// ✅ 正确：参数化查询
const getUser = async (db, userId) => {
  const [rows] = await db.execute(
    'SELECT * FROM users WHERE id = ?',
    [userId]
  );
  return rows[0];
};

// ❌ 错误：模板字符串拼接
const getUserBad = async (db, userId) => {
  const [rows] = await db.execute(
    `SELECT * FROM users WHERE id = ${userId}`  // SQL注入风险!
  );
  return rows[0];
};

// ✅ 正确：ORM 方式 (Sequelize)
const { User } = require('./models');
const user = await User.findByPk(userId);
```

---

## 2. XSS 防护 (A03 - Injection)

### 2.1 输出编码要求

```python
# Python (FastAPI + Jinja2)
from markupsafe import escape

# ✅ 正确：自动转义
@app.get("/user/{name}")
async def get_user(name: str):
    return templates.TemplateResponse("user.html", {"name": escape(name)})

# ❌ 错误： MarkupString 跳过转义
from markupsafe import Markup
dangerous = Markup(f"<b>Hello {name}</b>")  # XSS风险!
```

```javascript
// Node.js (Express + EJS)
 // ✅ 正确：默认自动转义
 app.get('/user/:name', (req, res) => {
     res.render('user', { name: req.params.name }); // 自动转义
 });

 // ❌ 错误： innerHTML 直接赋值
 document.getElementById('output').innerHTML = userInput;  // XSS风险!
```

### 2.2 Content Security Policy

```python
# Python FastAPI
@app.get("/")
async def home():
    response = Response(
        content="<h1>Welcome</h1>",
        media_type="text/html"
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response
```

```javascript
// Node.js Express - 安全中间件
const helmet = require('helmet');
app.use(helmet.contentSecurityPolicy({
    directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'"],
        styleSrc: ["'self'"],
    }
}));
```

---

## 3. 命令注入防护 (A03 - Injection)

### 3.1 Python

```python
# ❌ 错误：os.system / os.popen
import os
os.system(f"ls {user_input}")  # 命令注入风险!

# ❌ 错误：subprocess shell=True
import subprocess
subprocess.run(f"ls {user_input}", shell=True)  # 命令注入风险!

# ✅ 正确：subprocess list 方式
import subprocess
result = subprocess.run(
    ["ls", user_input],  # 安全：列表参数
    capture_output=True,
    text=True
)
```

### 3.2 Go

```go
// ❌ 错误：os/exec with string
import (
    "os/exec"
    "fmt"
)
func bad(userInput string) {
    cmd := exec.Command("sh", "-c", "ls "+userInput)  // 命令注入风险!
}

// ✅ 正确：参数列表
func good(userInput string) {
    cmd := exec.Command("ls", userInput)  // 安全：参数分离
}
```

### 3.3 Node.js

```javascript
// ❌ 错误：child_process exec with shell
const { exec } = require('child_process');
exec(`ls ${userInput}`, (err, stdout) => {});  // 命令注入风险!

// ✅ 正确：spawn 参数数组
const { spawn } = require('child_process');
spawn('ls', [userInput], { shell: false });  // 安全

// ✅ 正确：execFile
const { execFile } = require('child_process');
execFile('ls', [userInput], (err, stdout) => {});
```

---

## 4. 认证与授权 (A01 + A07)

### 4.1 密码存储

```python
# ✅ 正确：bcrypt 哈希
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

```javascript
// ✅ 正确：bcrypt (Node.js)
const bcrypt = require('bcrypt');
const hashPassword = async (password) => {
    const salt = await bcrypt.genSalt(10);
    return bcrypt.hash(password, salt);
};
const verifyPassword = async (password, hash) => {
    return bcrypt.compare(password, hash);
};
```

### 4.2 JWT 安全

```python
# Python (PyJWT)
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here"  # 从环境变量读取
ALGORITHM = "HS256"

def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
```

### 4.3 权限检查装饰器

```python
# Python FastAPI
from functools import wraps
from fastapi import HTTPException, status

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user = request.state.user
            if permission not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator

@app.get("/admin")
@require_permission("admin:access")
async def admin_panel(request: Request):
    return {"message": "Admin panel"}
```

---

## 5. 敏感信息管理

### 5.1 环境变量

```python
# ✅ 正确：从环境变量读取
import os
from pydantic import BaseModel

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")
    api_key: str = os.getenv("API_KEY")
    secret_key: str = os.getenv("SECRET_KEY")

# ❌ 错误：硬编码
DATABASE_URL = "postgresql://user:password@localhost/db"  # 禁止!
API_KEY = "sk-1234567890"  # 禁止!
```

### 5.2 日志脱敏

```python
import logging

class SensitiveFilter(logging.Filter):
    SENSITIVE_KEYS = ['password', 'token', 'api_key', 'secret', 'authorization']

    def filter(self, record):
        for key in self.SENSITIVE_KEYS:
            if key.lower() in record.msg.lower():
                record.msg = record.msg.replace(
                    self.mask_value(record.msg, key),
                    f"{key}=***REDACTED***"
                )
        return True

logging.basicConfig(level=logging.INFO)
logging.getLogger().addFilter(SensitiveFilter())
```

---

## 6. 输入验证

### 6.1 类型校验

```python
# Python Pydantic
from pydantic import BaseModel, Field, validator

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    age: int = Field(..., ge=0, le=150)

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
```

### 6.2 SQL 注入特殊字符校验

```python
import re

def validate_safe_input(user_input: str) -> bool:
    # 禁止的字符模式
    dangerous_patterns = [
        r"(\bOR\b|\bAND\b).*=.*",  # OR 1=1 模式
        r";\s*(DROP|DELETE|INSERT|UPDATE)",  # SQL 命令
        r"(--|#|\/\*)",  # SQL 注释
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False
    return True
```

---

## 7. 安全响应头

```python
# Python FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 安全配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # 明确指定
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # 只允许必要方法
    allow_headers=["Authorization"],  # 只允许必要头
)

@app.get("/")
async def root():
    response = {"message": "OK"}
    # 安全头在中间件或 reverse proxy 配置
    return response
```

---

## 8. 安全检查清单

### 开发前
- [ ] 使用参数化查询，不用字符串拼接 SQL
- [ ] 用户输入必须验证类型和范围
- [ ] 敏感配置从环境变量读取

### 开发中
- [ ] 输出到 HTML 前进行转义
- [ ] 不使用 eval/Function 处理用户输入
- [ ] 命令执行使用列表参数，不使用 shell=True

### 开发后
- [ ] 运行 `ppqa-security-check.py` 无高风险报警
- [ ] 确认无硬编码密码/API Key
- [ ] 安全头已配置 (CSP, X-Frame-Options, etc)

---

## 9. OWASP Top 10 映射

| 漏洞 | 防护措施 | 验证方法 |
|------|----------|----------|
| A01: Access Control | 权限装饰器 + 中间件 | 越权测试 |
| A02: Cryptographic Failures | 密码 bcrypt + 环境变量 | 代码审计 |
| A03: Injection | 参数化查询 + 转义 | ppqa-security-check.py |
| A04: Insecure Design | 威胁建模 | 架构评审 |
| A05: Security Misconfiguration | 安全头 + 最小权限 | 配置审计 |
| A07: Identification Failures | JWT + 强度校验 | 认证测试 |
| A08: Software Integrity | 签名验证 | 依赖扫描 |

---

## 10. 违规示例与修复对照

| 违规类型 | 错误示例 | 正确修复 |
|----------|----------|----------|
| SQL注入 | `f"SELECT * FROM t WHERE id={uid}"` | `text("SELECT * FROM t WHERE id=:id")` |
| XSS | `innerHTML = userInput` | `textContent = userInput` |
| 命令注入 | `os.system(cmd + user_input)` | `subprocess.run([cmd, user_input])` |
| 密码硬编码 | `password = "123456"` | `os.getenv("PASSWORD")` |
| JWT密钥硬编码 | `jwt.encode(payload, "secret")` | `jwt.encode(payload, os.getenv("SECRET"))` |
| CORS全开 | `allow_origins=["*"]` | `allow_origins=["https://domain.com"]` |
| 无输入验证 | `def get_user(id):` | `def get_user(id: int) -> User:` |