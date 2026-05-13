---
name: backend-nodejs
description: Node.js后端代码规范。支持框架：Express / NestJS。
version: 1.0.0
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# Node.js 代码规范

## 支持框架
- **Express** (推荐)
- NestJS
- Fastify

## 代码规范

### 1. JSDoc注释（必须）

```javascript
/**
 * 用户服务层
 * 负责处理用户相关的业务逻辑
 */
class UserService {
    /**
     * 创建用户
     * @param {CreateUserRequest} request - 创建用户请求
     * @returns {Promise<{id: number}>} 创建的用户ID
     * @throws {UserAlreadyExistsError} 用户名已存在时抛出
     */
    async createUser(request) {
        ...
    }
}
```

### 2. TypeScript类型定义（推荐）

```typescript
// ✅ 使用TypeScript
interface CreateUserRequest {
    username: string;  // 用户名，长度3-20字符
    email: string;     // 邮箱地址
}

interface CreateUserResponse {
    id: number;
}

// ❌ 避免使用any
function createUser(request: any) { // 禁止
    ...
}
```

### 3. 错误处理

```javascript
// ✅ 统一错误处理
class UserAlreadyExistsError extends Error {
    constructor(username) {
        super(`用户名 ${username} 已存在`);
        this.name = 'UserAlreadyExistsError';
    }
}

class UserService {
    async createUser(request) {
        const existing = await this.userRepo.findByUsername(request.username);
        if (existing) {
            throw new UserAlreadyExistsError(request.username);
        }
        return this.userRepo.create(request);
    }
}

// ❌ 禁止callback风格
callback((err, user) => { // 禁止
    ...
});
```

### 4. Async/Await

```javascript
// ✅ 使用async/await
async function getUser(id) {
    const user = await userRepository.findById(id);
    if (!user) {
        throw new UserNotFoundError(id);
    }
    return user;
}

// ❌ 禁止Promise.then链（除非有明确原因）
function getUser(id) {
    return userRepository.findById(id)
        .then(user => {
            if (!user) {
                throw new UserNotFoundError(id);
            }
            return user;
        });
}
```

## 目录结构

```
backend/src/modules/<group>/<tool-key>/
├── controller.ts      # 控制器
├── service.ts         # 服务层
├── repository.ts      # 仓储层
├── types.ts           # 类型定义
├── schemas.ts        # 验证schema (Zod/Joi)
├── errors.ts         # 错误定义
└── <tool-key>.test.ts
```

## 测试规范

### 框架
- Jest
- Supertest (API测试)

### 测试文件
```typescript
// user.service.test.ts
describe('UserService', () => {
    describe('createUser', () => {
        it('should create user successfully', async () => {
            const service = new UserService(mockRepository);
            const result = await service.createUser({
                username: 'test',
                email: 'test@example.com'
            });
            expect(result.id).toBeDefined();
        });

        it('should throw error if username exists', async () => {
            mockRepository.findByUsername.mockResolvedValue({ id: 1 });
            const service = new UserService(mockRepository);
            await expect(service.createUser({
                username: 'existing',
                email: 'test@example.com'
            })).rejects.toThrow(UserAlreadyExistsError);
        });
    });
});
```

## 工具链

| 工具 | 用途 | 命令 |
|------|------|------|
| Prettier | 格式化 | `prettier --write "src/**/*.ts"` |
| ESLint | Linter | `eslint "src/**/*.ts"` |
| TypeScript | 类型检查 | `tsc --noEmit` |
| Jest | 测试 | `jest --coverage` |

## TypeScript严格模式要求

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

## 量化指标

| 指标 | 目标 |
|------|------|
| ESLint | 0 errors (strict) |
| TypeScript | strict mode, 0 errors |
| 测试覆盖率 | ≥ 80% |
| 函数长度最大 | ≤ 50行 |

## 禁止行为

- 禁止使用any类型
- 禁止使用var（必须const/let）
- 禁止公共API无JSDoc
- 禁止callback风格（必须async/await）
- 禁止硬编码配置（使用环境变量）