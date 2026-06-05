# 放射科专业病例阅片学习平台 - 项目概览

## 项目简介

这是一个基于现代 Web 技术栈构建的放射科病例学习平台，旨在为放射科医生和医学生提供一个真实病例学习和阅片训练的环境。

## 核心功能

### 1. 病例管理
- 创建、编辑、删除病例
- 病例信息管理（标题、描述、患者ID、影像类型、检查部位、诊断结果、教学要点）
- 难度等级分类（1-5星）
- 病例搜索和筛选

### 2. 影像查看
- 集成 OHIF Viewer 查看 DICOM 影像
- 支持多种影像类型：CT、MRI、X光、超声、PET
- 多平面重建（MPR）支持
- 影像标注和测量工具

### 3. 学习功能
- 教学要点展示
- 学习笔记记录
- 病例收藏和标记
- 学习进度跟踪

### 4. 统计分析
- 病例总数统计
- 影像数量统计
- 影像类型分布
- 学习进度统计

## 技术架构

### 后端技术栈
- **FastAPI**: 高性能 Python Web 框架
- **PostgreSQL**: 关系型数据库
- **SQLAlchemy**: ORM 框架
- **Pydantic**: 数据验证
- **Uvicorn**: ASGI 服务器

### 前端技术栈
- **HTML5/CSS3/JavaScript**: 前端基础
- **Bootstrap 5**: UI 框架
- **Font Awesome**: 图标库
- **OHIF Viewer**: 医学影像查看器

### 基础设施
- **Docker**: 容器化部署
- **Docker Compose**: 多容器编排
- **Nginx**: 反向代理和静态文件服务
- **Orthanc**: DICOM 影像服务器

## 项目结构

```
radiology-platform/
├── docker-compose.yml          # Docker Compose 配置
├── nginx.conf                  # Nginx 配置
├── README.md                   # 项目说明
├── INSTALL.md                  # 安装指南
├── PROJECT_OVERVIEW.md         # 项目概览
├── .env                        # 环境变量
├── .gitignore                  # Git 忽略文件
├── build_task.md               # 构建任务说明
├── orthanc-config/            # Orthanc 配置
│   └── orthanc.json
├── backend/                    # FastAPI 后端
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py             # 主应用文件
│       ├── main_modular.py     # 模块化主应用
│       ├── config.py           # 配置文件
│       ├── database.py         # 数据库连接
│       ├── models.py           # 数据库模型
│       ├── schemas.py          # Pydantic 模型
│       └── routers/
│           ├── __init__.py
│           ├── case.py         # 病例路由
│           ├── image.py        # 影像路由
│           └── stats.py        # 统计路由
├── frontend/                   # 前端文件
│   ├── html/
│   │   └── index.html          # 主页面
│   └── ohif-config.js          # OHIF 配置
└── scripts/                    # 脚本文件
    ├── init-db.sql             # 数据库初始化
    ├── start.sh                # Linux/macOS 启动脚本
    ├── start.bat               # Windows 启动脚本
    ├── test.sh                 # Linux/macOS 测试脚本
    ├── test.bat                # Windows 测试脚本
    ├── check-files.sh          # 文件检查脚本
    └── check-files.bat         # Windows 文件检查脚本
```

## 数据库设计

### 病例表 (cases)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键 |
| title | VARCHAR(255) | 病例标题 |
| description | TEXT | 病例描述 |
| patient_id | VARCHAR(100) | 患者ID |
| modality | VARCHAR(50) | 影像类型 |
| body_part | VARCHAR(100) | 检查部位 |
| diagnosis | TEXT | 诊断结果 |
| teaching_points | TEXT | 教学要点 |
| difficulty_level | INTEGER | 难度等级(1-5) |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 影像表 (case_images)
| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键 |
| case_id | INTEGER | 病例ID(外键) |
| dicom_instance_id | VARCHAR(255) | Orthanc实例ID |
| image_type | VARCHAR(50) | 影像类型 |
| description | TEXT | 影像描述 |
| created_at | TIMESTAMP | 创建时间 |

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

## 部署说明

### 开发环境
1. 安装 Docker 和 Docker Compose
2. 克隆项目到本地
3. 运行 `docker-compose up -d`
4. 访问 http://localhost

### 生产环境
1. 配置环境变量
2. 配置 SSL 证书（可选）
3. 配置域名和反向代理
4. 配置数据库备份
5. 配置日志收集

## 扩展功能

### 短期扩展
- 用户认证和授权
- 病例分类和标签
- 影像标注工具
- 学习进度跟踪

### 中期扩展
- 多用户协作
- 病例讨论区
- 学习报告生成
- 移动端适配

### 长期扩展
- AI 辅助诊断
- 远程会诊功能
- 教学课程管理
- 考核评估系统

## 性能优化

### 数据库优化
- 索引优化
- 查询优化
- 连接池配置
- 读写分离

### 应用优化
- 缓存策略
- 异步处理
- 负载均衡
- CDN 加速

### 前端优化
- 资源压缩
- 懒加载
- 服务端渲染
- PWA 支持

## 安全考虑

### 数据安全
- 数据库加密
- 传输加密（HTTPS）
- 访问控制
- 数据备份

### 应用安全
- 输入验证
- SQL 注入防护
- XSS 防护
- CSRF 防护

### 网络安全
- 防火墙配置
- DDoS 防护
- 入侵检测
- 安全审计

## 监控和维护

### 监控指标
- 系统资源使用率
- 应用性能指标
- 数据库性能指标
- 用户行为分析

### 维护任务
- 定期备份
- 日志清理
- 性能优化
- 安全更新

## 贡献指南

### 开发流程
1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

### 代码规范
- 遵循 PEP 8 规范
- 编写文档字符串
- 编写单元测试
- 代码审查

## 许可证

本项目为放射科专业病例阅片学习平台 MVP 版本。

## 联系方式

如有问题或建议，请联系项目维护者。
