# 开发指南

本文档为放射科专业病例阅片学习平台的开发指南。

## 开发环境设置

### 前置要求

- Docker 和 Docker Compose
- Python 3.11+（可选，用于本地开发）
- Git
- 代码编辑器（推荐 VS Code）

### 本地开发环境

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/radiology-platform.git
cd radiology-platform
```

#### 2. 启动服务

```bash
# 使用开发配置启动
docker-compose up -d

# 或者使用 Makefile
make up
```

#### 3. 访问服务

- API 服务: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 数据库: localhost:5432
- Orthanc: http://localhost:8042

### 本地 Python 开发

如果您想在本地运行 Python 代码（不使用 Docker）：

#### 1. 创建虚拟环境

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

创建 `.env` 文件：

```bash
DATABASE_URL=postgresql://radio:radio123@localhost:5432/cases
```

#### 4. 运行应用

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 项目结构

### 后端结构

```
backend/
├── Dockerfile
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py             # 主应用入口
    ├── main_modular.py     # 模块化版本
    ├── config.py           # 配置管理
    ├── database.py         # 数据库连接
    ├── models.py           # SQLAlchemy 模型
    ├── schemas.py          # Pydantic 模型
    └── routers/
        ├── __init__.py
        ├── case.py         # 病例路由
        ├── image.py        # 影像路由
        └── stats.py        # 统计路由
```

### 前端结构

```
frontend/
├── html/
│   └── index.html          # 主页面
└── ohif-config.js          # OHIF 配置
```

## 数据库

### 数据库设计

#### 病例表 (cases)

```sql
CREATE TABLE cases (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    patient_id VARCHAR(100),
    modality VARCHAR(50),
    body_part VARCHAR(100),
    diagnosis TEXT,
    teaching_points TEXT,
    difficulty_level INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 影像表 (case_images)

```sql
CREATE TABLE case_images (
    id SERIAL PRIMARY KEY,
    case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
    dicom_instance_id VARCHAR(255),
    image_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 数据库操作

#### 连接数据库

```bash
# 使用 Docker
docker-compose exec db psql -U radio -d cases

# 使用本地 psql
psql -h localhost -U radio -d cases
```

#### 常用 SQL 命令

```sql
-- 查看所有病例
SELECT * FROM cases;

-- 查看所有影像
SELECT * FROM case_images;

-- 统计病例数量
SELECT COUNT(*) FROM cases;

-- 按影像类型统计
SELECT modality, COUNT(*) FROM cases GROUP BY modality;
```

## API 开发

### 添加新路由

1. 在 `backend/app/routers/` 创建新文件
2. 定义路由和端点
3. 在 `__init__.py` 中导出
4. 在 `main.py` 中包含

#### 示例：添加用户路由

```python
# backend/app/routers/user.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 实现创建用户逻辑
    pass

@router.get("/", response_model=list[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 实现获取用户列表逻辑
    pass
```

### 数据验证

使用 Pydantic 进行数据验证：

```python
from pydantic import BaseModel, EmailStr, validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('username')
    def username_must_be_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('用户名必须是字母数字')
        return v
```

### 错误处理

```python
from fastapi import HTTPException

@router.get("/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user
```

## 前端开发

### 添加新页面

1. 在 `frontend/html/` 创建新 HTML 文件
2. 在 `index.html` 中添加导航链接
3. 使用 Bootstrap 组件

### 添加新功能

1. 在 JavaScript 中添加函数
2. 调用 API 接口
3. 更新 DOM

#### 示例：添加搜索功能

```javascript
async function searchCases() {
    const searchTerm = document.getElementById('searchInput').value;
    try {
        const response = await fetch(`/api/cases/?search=${searchTerm}`);
        const cases = await response.json();
        displayCases(cases);
    } catch (error) {
        console.error('Error searching cases:', error);
    }
}
```

## 测试

### 运行测试

```bash
# 使用 Docker
docker-compose exec api pytest

# 使用本地环境
cd backend
pytest
```

### 编写测试

```python
# backend/tests/test_cases.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_case():
    response = client.post("/api/cases/", json={
        "title": "测试病例",
        "description": "测试描述",
        "modality": "CT"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "测试病例"

def test_read_cases():
    response = client.get("/api/cases/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

## 部署

### 生产环境配置

1. 修改环境变量
2. 配置 SSL 证书
3. 配置域名
4. 配置备份

### Docker 生产配置

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    image: your-registry/radiology-api:latest
    environment:
      - DATABASE_URL=postgresql://user:password@db/cases
      - DEBUG=False
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
    restart: always
```

## 调试

### 查看日志

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f db
```

### 调试 Python 代码

1. 在代码中添加 `breakpoint()`
2. 重启服务
3. 查看控制台输出

### 调试数据库

```bash
# 连接数据库
docker-compose exec db psql -U radio -d cases

# 查看表结构
\d cases
\d case_images

# 查看数据
SELECT * FROM cases LIMIT 10;
```

## 性能优化

### 数据库优化

1. 添加索引
2. 优化查询
3. 使用连接池
4. 配置缓存

### 应用优化

1. 使用异步处理
2. 配置缓存
3. 优化代码
4. 使用 CDN

## 安全

### 输入验证

1. 使用 Pydantic 验证输入
2. 防止 SQL 注入
3. 防止 XSS 攻击
4. 防止 CSRF 攻击

### 认证和授权

1. 实现用户认证
2. 实现权限控制
3. 使用 JWT
4. 配置 CORS

## 常见问题

### 1. 数据库连接失败

检查：
- 数据库是否启动
- 连接字符串是否正确
- 防火墙设置

### 2. API 无法访问

检查：
- 服务是否启动
- 端口是否正确
- 网络配置

### 3. 前端无法加载

检查：
- Nginx 配置
- 静态文件路径
- 浏览器控制台错误

## 贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
