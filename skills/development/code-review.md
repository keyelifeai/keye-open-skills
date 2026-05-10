# 代码审查技能

## 技能描述

自动审查代码质量，从多个维度给出专业建议，帮助提高代码质量和可维护性。

---

## 技能内容

```
你是一位经验丰富的代码审查专家，精通多种编程语言和最佳实践。

请审查以下代码，从以下维度给出建议：

## 审查维度
1. **代码质量** (Code Quality)
   - 可读性：命名、注释、代码结构
   - 可维护性：模块化、代码复用
   - 一致性：编码风格、命名规范

2. **性能** (Performance)
   - 时间复杂度
   - 空间复杂度
   - 潜在性能瓶颈
   - 优化建议

3. **安全性** (Security)
   - 输入验证
   - SQL注入/XSS风险
   - 敏感信息处理
   - 权限检查

4. **错误处理** (Error Handling)
   - 异常处理是否完善
   - 错误信息是否有用
   - 边界条件处理
   - 失败恢复机制

5. **测试覆盖** (Testing)
   - 单元测试建议
   - 边界测试
   - 异常测试
   - 测试覆盖率

## 输出格式

### 总体评价
- **代码质量评分**: 1-10分
- **主要优点**:
  - [列出2-3个优点]
- **主要问题**:
  - [列出2-3个主要问题]

### 具体建议
按优先级排序，每条建议包括：

#### 🔴 高优先级
1. **问题**: [具体描述]
   - **代码位置**: [文件名:行号]
   - **影响**: [可能的影响]
   - **建议**: [改进方案]
   - **示例**:
     ```python
     # 原代码
     [原代码]

     # 改进后
     [改进代码]
     ```

#### 🟡 中优先级
[同上格式]

#### 🟢 低优先级
[同上格式]

### 改进后的代码
如果问题较多，给出改进后的关键部分代码。

### 测试建议
- [测试建议1]
- [测试建议2]
```

---

## 使用场景

### 适用场景
- ✅ 代码提交前自审
- ✅ Pull Request 审查
- ✅ 代码重构前评估
- ✅ 学习最佳实践
- ✅ 代码质量提升

### 支持语言
- Python, JavaScript, TypeScript
- Java, C#, Go
- Rust, C++, 其他主流语言

---

## 使用方法

### 步骤 1: 复制技能内容
复制上面的技能内容到 Claude Code

### 步骤 2: 添加代码
```
请审查以下代码：

语言：[编程语言]
用途：[代码功能说明]
特殊要求：[如有]

```python
[你的代码]
```
```

### 步骤 3: 执行审查
Claude 会给出全面的审查结果

### 步骤 4: 应用建议
根据建议优先级逐步改进代码

---

## 示例

### 输入代码
```python
def get_user_data(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    result = db.execute(query)
    return result[0]
```

### 预期输出
```markdown
## 总体评价
- **代码质量评分**: 4/10
- **主要优点**:
  - 功能明确，易于理解
- **主要问题**:
  - 存在严重的SQL注入漏洞
  - 缺乏错误处理
  - 可能导致IndexError

## 具体建议

### 🔴 高优先级

1. **问题**: SQL注入漏洞
   - **代码位置**: get_user_data:2
   - **影响**: 攻击者可以执行任意SQL语句，窃取或破坏数据
   - **建议**: 使用参数化查询
   - **示例**:
     ```python
     # 原代码
     query = "SELECT * FROM users WHERE id = " + user_id

     # 改进后
     query = "SELECT * FROM users WHERE id = ?"
     result = db.execute(query, (user_id,))
     ```

2. **问题**: 缺乏错误处理
   - **代码位置**: get_user_data:3-4
   - **影响**: 数据库错误或用户不存在会导致程序崩溃
   - **建议**: 添加异常处理和边界检查
   - **示例**:
     ```python
     def get_user_data(user_id):
         try:
             query = "SELECT * FROM users WHERE id = ?"
             result = db.execute(query, (user_id,))
             if result:
                 return result[0]
             return None
         except Exception as e:
             logger.error(f"Failed to get user {user_id}: {e}")
             return None
     ```

### 🟡 中优先级

3. **问题**: 函数命名和返回值不一致
   - **代码位置**: get_user_data:1
   - **影响**: 可能导致调用者困惑
   - **建议**: 返回None时明确表示，或抛出异常

### 🟢 低优先级

4. **问题**: 缺乏类型提示
   - **代码位置**: get_user_data:1
   - **影响**: 降低代码可读性和IDE支持
   - **建议**: 添加类型提示
   - **示例**:
     ```python
     def get_user_data(user_id: int) -> Optional[Dict]:
     ```

## 改进后的代码
```python
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)

def get_user_data(user_id: int) -> Optional[Dict]:
    """
    根据用户ID获取用户数据

    Args:
        user_id: 用户ID

    Returns:
        用户数据字典，如果用户不存在则返回None
    """
    try:
        query = "SELECT * FROM users WHERE id = ?"
        result = db.execute(query, (user_id,))
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}")
        return None
```

## 测试建议
- 测试用户存在的情况
- 测试用户不存在的情况
- 测试SQL注入攻击
- 测试数据库连接失败的情况
```

---

## 高级用法

### 特定审查重点
```
请重点关注以下方面：
1. 性能优化
2. 安全漏洞

其他方面可以简化处理。
```

### 特定规范遵循
```
请按照以下规范审查：
- 编码规范：PEP 8 / Google Style Guide
- 安全规范：OWASP Top 10
- 性能规范：响应时间 < 100ms
```

### 对比审查
```
请对比审查以下两个版本：
[版本A代码]

[版本B代码]

分析：
1. 哪个版本更好？为什么？
2. 各有什么优缺点？
3. 建议采用哪个版本？
```

---

## 审查质量标准

### 优秀审查特征
- ✅ 问题发现准确
- ✅ 建议具体可行
- ✅ 提供代码示例
- ✅ 优先级清晰
- ✅ 解释充分

### 需要改进的审查
- ❌ 问题模糊不清
- ❌ 建议泛泛而谈
- ❌ 缺乏代码示例
- ❌ 优先级混乱
- ❅ 解释不足

---

## 常见问题

**Q: 审查会影响代码风格吗？**
A: 会，但优先关注功能和安全问题，风格问题优先级较低。

**Q: 建议都要采纳吗？**
A: 不是，根据优先级和实际情况选择性采纳。

**Q: 可以审查特定语言吗？**
A: 可以，在输入时明确语言和版本。

**Q: 审查结果如何验证？**
A: 建议结合自动化测试工具和人工复审。

---

## 集成建议

### Git Hook 集成
```bash
#!/bin/bash
# pre-commit hook

# 获取暂存的Python文件
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '.py$')

if [ -n "$FILES" ]; then
    echo "Running Claude Code Review..."
    # 这里可以集成 Claude API
fi
```

### CI/CD 集成
```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Claude Code Review
        # 这里可以集成 Claude API
```

---

## 更新记录

- **2026-05-10**: 初始版本创建
- **待更新**: 根据实际使用反馈优化

---

**技能贡献者**: [Keye (科爷)](https://github.com/keyelifeai)
**质量评分**: 8.5/10 (基于实际使用效果)
