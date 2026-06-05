# 放射科专业病例阅片学习平台

一个基于 FastAPI + PostgreSQL + Orthanc + OHIF Viewer + Nginx 的放射科病例学习平台 MVP 版本。

## 系统架构

- **FastAPI**: 后端 API 服务
- **PostgreSQL**: 数据库存储
- **Orthanc**: DICOM 影像服务器
- **OHIF Viewer**: 医学影像查看器
- **Nginx**: 反向代理和静态文件服务

## 快速开始

### 前置要求

- Docker
- Docker Compose

### 启动服务

1. 克隆或下载项目到本地

2. 进入项目目录：
```bash
cd radiology-platform
```

3. 启动所有服务：
```bash
docker-compose up -d
```

4. 访问平台：
- 主页面: http://localhost
- API 文档: http://localhost/api/docs
- Orthanc 管理: http://localhost/orthanc/
- OHIF Viewer: http://localhost/viewer/

### 停止服务

```bash
docker-compose down
```

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f orthanc
```

## 功能特性

### 病例管理
- 创建、查看、编辑、删除病例
- 病例信息包括：标题、描述、患者ID、影像类型、检查部位、诊断结果、教学要点
- 难度等级分类（1-5星）

### 影像查看
- 集成 OHIF Viewer 查看 DICOM 影像
- 支持多种影像类型：CT、MRI、X光、超声、PET
- 多平面重建（MPR）支持

### 学习功能
- 教学要点展示
- 学习笔记记录
- 病例搜索功能

### 统计功能
- 病例总数统计
- 影像数量统计
- 影像类型分布

## 项目结构

```
radiology-platform/
├── docker-compose.yml          # Docker Compose 配置
├── nginx.conf                  # Nginx 配置
├── README.md                   # 项目说明
├── orthanc-config/            # Orthanc 配置
│   └── orthanc.json
├── backend/                    # FastAPI 后端
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── main.py
├── frontend/                   # 前端文件
│   ├── html/
│   │   └── index.html
│   └── ohif-config.js
└── scripts/                    # 脚本文件
    └── init-db.sql
```

## API 接口

### 病例管理

- `POST /api/cases/` - 创建新病例
- `GET /api/cases/` - 获取病例列表
- `GET /api/cases/{id}` - 获取单个病例
- `PUT /api/cases/{id}` - 更新病例
- `DELETE /api/cases/{id}` - 删除病例

### 影像管理

- `POST /api/case-images/` - 添加病例影像
- `GET /api/case-images/` - 获取影像列表
- `GET /api/case-images/{id}` - 获取单个影像
- `DELETE /api/case-images/{id}` - 删除影像

### 统计接口

- `GET /api/stats/` - 获取平台统计数据

### 健康检查

- `GET /api/health` - 服务健康检查

## 数据库配置

默认数据库配置：
- 用户名: radio
- 密码: radio123
- 数据库: cases

可以在 `docker-compose.yml` 中修改这些配置。

## Orthanc 配置

Orthanc DICOM 服务器配置位于 `orthanc-config/orthanc.json`，主要配置：
- DICOM AET: RADIOLOGY
- HTTP 端口: 8042
- DICOM 端口: 4242

## 开发说明

### 后端开发

1. 进入 backend 目录
2. 安装依赖：`pip install -r requirements.txt`
3. 运行开发服务器：`uvicorn app.main:app --reload`

### 前端开发

前端文件位于 `frontend/html/` 目录，可以直接编辑 HTML 文件。

## 故障排查

### 常见问题

1. **端口冲突**
   - 检查 80、8000、8042、4242 端口是否被占用
   - 修改 `docker-compose.yml` 中的端口映射

2. **数据库连接失败**
   - 确保 PostgreSQL 容器已启动
   - 检查数据库配置是否正确

3. **Orthanc 无法访问**
   - 检查 Orthanc 容器日志
   - 确认配置文件路径正确

4. **OHIF Viewer 无法加载影像**
   - 检查 Orthanc 中是否有 DICOM 数据
   - 确认 OHIF 配置正确

### 查看容器状态

```bash
docker-compose ps
```

### 重启服务

```bash
docker-compose restart
```

### 清理数据

```bash
# 停止并删除所有容器、网络、卷
docker-compose down -v

# 删除所有数据（包括数据库数据）
docker system prune -a
```

## 许可证

本项目为放射科专业病例阅片学习平台 MVP 版本。

## 联系方式

如有问题或建议，请联系项目维护者。
