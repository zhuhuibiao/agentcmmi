---
name: backend-java
description: Java后端代码规范。支持框架：Spring Boot。
version: 1.0.0
author: CMMI L5 Team
created_date: 2026-05-12
last_updated: 2026-05-12
---

# Java 代码规范

## 支持框架
- **Spring Boot** (推荐)
- Quarkus
- Micronaut

## 代码规范

### 1. 方法注释（必须）

```java
/**
 * 用户服务层
 * 负责处理用户相关的业务逻辑
 */
@Service
public class UserService {

    /**
     * 创建用户
     *
     * @param request 创建用户请求
     * @return 创建的用户ID
     * @throws UserAlreadyExistsException 用户名已存在时抛出
     */
    public Long createUser(CreateUserRequest request) {
        ...
    }
}
```

### 2. 类和字段注释

```java
/**
 * 用户创建请求
 */
public class CreateUserRequest {
    /**
     * 用户名，长度3-20字符
     */
    @NotBlank
    @Size(min = 3, max = 20)
    private String username;

    /**
     * 邮箱地址
     */
    @NotBlank
    @Email
    private String email;
}
```

### 3. 返回类型

```java
// ✅ 使用Optional或抛异常
public UserDTO getUser(Long id) {
    return userRepository.findById(id)
        .map(this::toDTO)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// ❌ 避免返回null
public UserDTO getUser(Long id) {
    return userRepository.findById(id).orElse(null); // 禁止
}
```

### 4. 异常处理

```java
// ✅ 统一异常处理
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserAlreadyExistsException.class)
    public ResponseEntity<ErrorResponse> handleUserExists(UserAlreadyExistsException ex) {
        return ResponseEntity
            .status(HttpStatus.CONFLICT)
            .body(new ErrorResponse(ex.getMessage()));
    }
}

// ❌ 禁止捕获Exception
try {
    ...
} catch (Exception e) { // 禁止
    ...
}
```

## 目录结构

```
backend/src/main/java/com/{company}/{group}/{tool-key}/
├── controller/
│   └── {ToolKey}Controller.java
├── service/
│   ├── {ToolKey}Service.java
│   └── impl/
│       └── {ToolKey}ServiceImpl.java
├── repository/
│   └── {ToolKey}Repository.java
├── model/
│   ├── entity/
│   │   └── {ToolKey}.java
│   └── dto/
│       ├── Create{ToolKey}Request.java
│       └── {ToolKey}Response.java
└── exception/
    └── {ToolKey}Exception.java

backend/src/test/java/com/{company}/{group}/{tool-key}/
└── {ToolKey}ServiceTest.java
```

## 测试规范

### 框架
- JUnit 5
- Mockito
- AssertJ

### 测试文件
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void createUser_success() {
        when(userRepository.save(any(User.class))).thenAnswer(i -> {
            User u = i.getArgument(0);
            u.setId(1L);
            return u;
        });

        CreateUserRequest request = new CreateUserRequest("test", "test@example.com");
        UserResponse response = userService.createUser(request);

        assertNotNull(response.getId());
        verify(userRepository).save(any(User.class));
    }
}
```

## 工具链

| 工具 | 用途 | 命令 |
|------|------|------|
| google-java-format | 格式化 | `google-java-format -i src/**/*.java` |
| Checkstyle | Linter | `mvn checkstyle:check` |
| SpotBugs | 检查 | `mvn spotbugs:check` |
| JaCoCo | 测试覆盖率 | `mvn jacoco:report` |

## 量化指标

| 指标 | 目标 |
|------|------|
| Checkstyle | 0 violations |
| SpotBugs | 0 issues |
| 测试覆盖率 | ≥ 80% |
| 方法长度最大 | ≤ 30行 |
| 类长度最大 | ≤ 500行 |

## 禁止行为

- 禁止公共方法无Javadoc
- 禁止返回null（使用Optional）
- 禁止捕获Exception
- 禁止硬编码配置（使用@Value或配置文件）
- 禁止循环依赖