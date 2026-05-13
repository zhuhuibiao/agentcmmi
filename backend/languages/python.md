---
name: backend-python
description: Python后端代码规范。支持框架：FastAPI / Flask / Django。
version: 1.0.0
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# Python 代码规范

## 支持框架
- **FastAPI** (推荐)
- Flask
- Django

## 代码规范

### 1. 类型提示（必须）

```python
# ✅ 必须有类型提示
def create_user(username: str, email: str) -> dict[str, int]:
    ...

# ❌ 禁止无类型提示
def create_user(username, email):
    ...
```

### 2. 文档字符串（必须）

```python
class UserService:
    """用户服务层

    负责处理用户相关的业务逻辑，包括创建、查询、更新。

    Attributes:
        repository: 用户仓储层实例
    """

    def create_user(self, schema: UserCreateSchema) -> dict[str, int]:
        """创建用户

        根据提供的用户信息创建新用户。

        Args:
            schema: 用户创建请求 schema

        Returns:
            包含创建用户 ID 的字典

        Raises:
            ValueError: 用户名已存在时
        """
        ...
```

### 3. Pydantic Schema（FastAPI推荐）

```python
from pydantic import BaseModel, Field

class UserCreateSchema(BaseModel):
    """用户创建请求 schema"""
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: str = Field(..., description="邮箱地址")
```

### 4. 错误处理

```python
# ✅ 统一异常处理
class UserAlreadyExistsError(Exception):
    pass

async def create_user(user: UserCreateSchema) -> UserResponse:
    existing = await repository.get_by_username(user.username)
    if existing:
        raise UserAlreadyExistsError(f"用户名 {user.username} 已存在")
    return await repository.create(user)

# ❌ 禁止裸except + 隐藏错误
try:
    ...
except:
    pass  # 禁止
```

## 目录结构

```
backend/app/modules/<group>/<tool-key>/
├── __init__.py
├── router.py      # 路由层
├── service.py    # 服务层
├── repository.py  # 仓储层
├── schemas.py     # Pydantic模型
├── models.py     # ORM模型
└── tests/
    ├── __init__.py
    └── test_{tool_key}.py
```

## 测试规范

### 框架
- pytest
- pytest-asyncio（异步）

### 测试文件
```python
# tests/test_user.py
import pytest
from app.modules.user.service import UserService

@pytest.fixture
def user_service():
    return UserService(repository=MockRepository())

async def test_create_user(user_service):
    result = await user_service.create_user(UserCreateSchema(
        username="test",
        email="test@example.com"
    ))
    assert result["id"] > 0
```

## 工具链

| 工具 | 用途 | 命令 |
|------|------|------|
| black | 格式化 | `black .` |
| ruff | Linter | `ruff check .` |
| mypy | 类型检查 | `mypy .` |
| pytest-cov | 测试覆盖率 | `pytest --cov=app` |

## 量化指标

| 指标 | 目标 |
|------|------|
| pylint score | ≥ 8/10 |
| mypy | 0 errors |
| 测试覆盖率 | ≥ 80% |
| 函数长度最大 | ≤ 50行 |
| 类长度最大 | ≤ 200行 |

## 禁止行为

- 禁止无类型提示的函数
- 禁止公共API无文档字符串
- 禁止裸except
- 禁止硬编码配置（使用环境变量）
- 禁止在循环中执行数据库操作（批量处理）