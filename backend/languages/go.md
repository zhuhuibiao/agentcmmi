---
name: backend-go
description: Go后端代码规范。支持框架：Gin / Fiber / Echo。
version: 1.0.0
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# Go 代码规范

## 支持框架
- **Gin** (推荐)
- Fiber
- Echo

## 代码规范

### 1. 错误处理（必须）

```go
// ✅ 必须有错误处理
func CreateUser(c *gin.Context) {
    user, err := service.CreateUser(req)
    if err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, user)
}

// ❌ 禁止忽略错误
func CreateUser(c *gin.Context) {
    user, _ := service.CreateUser(req) // 禁止
    c.JSON(200, user)
}
```

### 2. 文档注释（必须）

```go
// UserService 用户服务层
// 负责处理用户相关的业务逻辑
type UserService struct {
    repo Repository
}

// CreateUser 创建用户
// 参数:
//   - ctx: 上下文
//   - req: 创建用户请求
//
// 返回: 用户ID或错误
func (s *UserService) CreateUser(ctx context.Context, req *CreateUserRequest) (int64, error) {
    ...
}
```

### 3. 结构体标签

```go
type CreateUserRequest struct {
    Username string `json:"username" binding:"required,min=3,max=20"`
    Email    string `json:"email" binding:"required,email"`
}
```

### 4. Context传递

```go
// ✅ 使用context
func (s *UserService) CreateUser(ctx context.Context, req *CreateUserRequest) (int64, error) {
    user, err := s.repo.Create(ctx, req)
    if err != nil {
        return 0, err
    }
    return user.ID, nil
}

// ❌ 禁止不用context
func (s *UserService) CreateUser(req *CreateUserRequest) (int64, error) {
    ...
}
```

## 目录结构

```
backend/modules/<group>/<tool-key>/
├── handler.go   # 处理器层
├── service.go   # 服务层
├── repo.go      # 仓储层
├── model.go     # 数据模型
├── schema.go    # 请求/响应结构
├── errors.go    # 错误定义
└── {tool-key}_test.go
```

## 测试规范

### 框架
- testing (标准库)
- testify (断言)

### 测试文件
```go
// user_service_test.go
func TestCreateUser(t *testing.T) {
    svc := NewUserService(mockRepo)
    user, err := svc.CreateUser(context.Background(), &CreateUserRequest{
        Username: "test",
        Email:    "test@example.com",
    })
    assert.NoError(t, err)
    assert.True(t, user.ID > 0)
}
```

## 工具链

| 工具 | 用途 | 命令 |
|------|------|------|
| gofmt | 格式化 | `gofmt -w .` |
| goimports | 格式化+导入 | `goimports -w .` |
| golangci-lint | Linter | `golangci-lint run` |
| go vet | 检查 | `go vet ./...` |
| go test | 测试 | `go test -cover ./...` |

## 量化指标

| 指标 | 目标 |
|------|------|
| golangci-lint | 0 warnings |
| go vet | 0 errors |
| 测试覆盖率 | ≥ 80% |
| 函数长度最大 | ≤ 50行 |

## 禁止行为

- 禁止忽略错误（使用 `_` 接收）
- 禁止不使用context
- 公共函数无文档注释
- 禁止在生产代码中使用 `panic`
- 禁止硬编码配置