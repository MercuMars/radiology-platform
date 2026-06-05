# 放射科专业病例阅片学习平台 - 安装指南

## 系统要求

### Windows 系统
1. **Docker Desktop for Windows**
   - 下载地址: https://www.docker.com/products/docker-desktop
   - 安装后需要重启电脑
   - 确保 Docker Desktop 正在运行

2. **Git (可选)**
   - 下载地址: https://git-scm.com/download/win

### macOS 系统
1. **Docker Desktop for Mac**
   - 下载地址: https://www.docker.com/products/docker-desktop

### Linux 系统
1. **Docker**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose

   # CentOS/RHEL
   sudo yum install docker docker-compose
   ```

## 安装步骤

### 1. 下载项目

将整个 `radiology-platform` 文件夹复制到您的电脑上。

### 2. 启动 Docker

确保 Docker Desktop 正在运行（Windows/macOS）或 Docker 服务已启动（Linux）。

### 3. 启动平台

#### Windows 用户
1. 打开命令提示符或 PowerShell
2. 进入项目目录：
   ```cmd
   cd D:\我的OneDrive\OneDrive - stu.hnucm.edu.cn\下载\桌面\radiology-platform
   ```
3. 运行启动脚本：
   ```cmd
   scripts\start.bat
   ```

#### macOS/Linux 用户
1. 打开终端
2. 进入项目目录：
   ```bash
   cd /path/to/radiology-platform
   ```
3. 添加执行权限并运行：
   ```bash
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

### 4. 等待服务启动

首次启动需要下载 Docker 镜像，可能需要几分钟时间。

### 5. 访问平台

启动成功后，在浏览器中访问：
- **主页面**: http://localhost
- **API 文档**: http://localhost/api/docs
- **Orthanc 管理**: http://localhost/orthanc/
- **OHIF Viewer**: http://localhost/viewer/

## 测试安装

### Windows 用户
```cmd
scripts\test.bat
```

### macOS/Linux 用户
```bash
chmod +x scripts/test.sh
./scripts/test.sh
```

## 常见问题

### 1. 端口被占用
如果端口 80、8000、8042 或 4242 被占用，可以修改 `docker-compose.yml` 中的端口映射。

### 2. Docker 未启动
确保 Docker Desktop 正在运行（Windows/macOS）或 Docker 服务已启动（Linux）。

### 3. 网络问题
如果下载镜像失败，可以尝试：
- 使用国内镜像源
- 检查网络连接
- 使用 VPN

### 4. 权限问题
在 Linux/macOS 上，如果遇到权限问题：
```bash
sudo usermod -aG docker $USER
```
然后重新登录。

## 停止服务

### Windows 用户
```cmd
docker-compose down
```

### macOS/Linux 用户
```bash
docker-compose down
```

## 重新构建

如果修改了代码，需要重新构建：
```bash
docker-compose up -d --build
```

## 清理数据

删除所有数据（包括数据库数据）：
```bash
docker-compose down -v
docker system prune -a
```

## 技术支持

如果遇到问题，请检查：
1. Docker 是否正常运行
2. 端口是否被占用
3. 网络连接是否正常
4. 查看日志: `docker-compose logs -f`

## 项目结构

```
radiology-platform/
├── docker-compose.yml          # Docker Compose 配置
├── nginx.conf                  # Nginx 配置
├── README.md                   # 项目说明
├── INSTALL.md                  # 安装指南
├── .env                        # 环境变量
├── .gitignore                  # Git 忽略文件
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
    ├── init-db.sql
    ├── start.sh
    ├── start.bat
    ├── test.sh
    └── test.bat
```
