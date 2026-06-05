@echo off
REM 放射科专业病例阅片学习平台启动脚本 (Windows)

echo ==========================================
echo   放射科专业病例阅片学习平台
echo ==========================================
echo.

REM 检查 Docker 是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Docker，请先安装 Docker Desktop
    pause
    exit /b 1
)

REM 检查 Docker Compose 是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Docker Compose，请先安装 Docker Compose
    pause
    exit /b 1
)

echo 正在启动服务...
echo.

REM 启动所有服务
docker-compose up -d

if errorlevel 1 (
    echo.
    echo 错误: 服务启动失败，请检查日志
    echo 查看日志: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   服务启动成功！
echo ==========================================
echo.
echo 访问地址：
echo   - 主页面: http://localhost
echo   - API 文档: http://localhost/api/docs
echo   - Orthanc 管理: http://localhost/orthanc/
echo   - OHIF Viewer: http://localhost/viewer/
echo.
echo 查看日志: docker-compose logs -f
echo 停止服务: docker-compose down
echo.
pause
