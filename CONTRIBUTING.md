# 贡献指南

感谢您对放射科专业病例阅片学习平台项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告 Bug

1. 使用 GitHub Issues 报告 Bug
2. 请使用 Bug 报告模板
3. 提供详细的复现步骤
4. 包含错误信息和日志
5. 说明您的运行环境

### 功能建议

1. 使用 GitHub Issues 提出功能建议
2. 请使用功能建议模板
3. 详细描述您想要的功能
4. 说明使用场景
5. 提供设计草图（如果可能）

### 代码贡献

1. Fork 项目
2. 创建功能分支
3. 编写代码
4. 编写测试
5. 更新文档
6. 提交 Pull Request

## 开发环境

### 前置要求

- Docker
- Docker Compose
- Git
- Python 3.11+（可选，用于本地开发）

### 本地开发

1. 克隆项目：
```bash
git clone https://github.com/your-username/radiology-platform.git
cd radiology-platform
```

2. 启动服务：
```bash
docker-compose up -d
```

3. 访问平台：
- 主页面: http://localhost
- API 文档: http://localhost/api/docs

### 代码规范

#### Python 代码

- 遵循 PEP 8 规范
- 使用类型注解
- 编写文档字符串
- 保持函数简洁

#### JavaScript 代码

- 使用 ES6+ 语法
- 遵循 Airbnb 风格指南
- 使用 JSDoc 注释
- 保持代码简洁

#### HTML/CSS 代码

- 使用语义化 HTML
- 遵循 BEM 命名规范
- 保持 CSS 简洁
- 响应式设计

## 提交规范

### 提交信息格式

```
<类型>(<范围>): <主题>

<正文>

<页脚>
```

### 类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建/工具相关

### 示例

```
feat(cases): 添加病例搜索功能

- 实现按标题搜索
- 实现按描述搜索
- 实现按影像类型筛选

Closes #123
```

## Pull Request 流程

### 1. 准备工作

- 确保代码符合规范
- 编写或更新测试
- 更新文档
- 检查代码风格

### 2. 创建 Pull Request

- 使用清晰的标题
- 详细描述更改内容
- 关联相关 Issue
- 添加标签

### 3. 代码审查

- 等待维护者审查
- 根据反馈修改代码
- 保持沟通

### 4. 合并

- 维护者合并代码
- 更新版本号
- 发布新版本

## 测试

### 运行测试

```bash
# 运行所有测试
docker-compose exec api pytest

# 运行特定测试
docker-compose exec api pytest tests/test_cases.py

# 运行带覆盖率的测试
docker-compose exec api pytest --cov=app
```

### 编写测试

- 为每个功能编写测试
- 测试边界条件
- 测试错误情况
- 保持测试简洁

## 文档

### 更新文档

- 更新 README.md
- 更新 INSTALL.md
- 更新 API 文档
- 更新 CHANGELOG.md

### 文档规范

- 使用清晰的语言
- 提供示例代码
- 保持文档最新
- 使用 Markdown 格式

## 版本发布

### 版本号规则

- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 发布流程

1. 更新版本号
2. 更新 CHANGELOG.md
3. 创建 Git 标签
4. 发布 GitHub Release
5. 部署到生产环境

## 行为准则

### 我们的承诺

为了营造一个开放和友好的环境，我们承诺：

- 尊重所有参与者
- 接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 我们的标准

积极行为包括：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

不可接受的行为包括：

- 使用性暗示的语言或图像
- 恶意评论或人身攻击
- 公开或私下骚扰
- 未经许可发布他人的私人信息
- 其他不道德或不专业的行为

## 联系方式

如有问题或建议，请通过以下方式联系我们：

- GitHub Issues
- 电子邮件
- 社交媒体

## 致谢

感谢所有为项目做出贡献的人！

## 许可证

本项目采用 MIT 许可证。详情请参阅 LICENSE 文件。
