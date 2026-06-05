@echo off
REM 放射科专业病例阅片学习平台测试脚本 (Windows)

echo ==========================================
echo   放射科专业病例阅片学习平台 - 测试
echo ==========================================
echo.

REM 等待服务启动
echo 等待服务启动...
timeout /t 10 /nobreak >nul

REM 测试 API 健康检查
echo 1. 测试 API 健康检查...
curl -s http://localhost/api/health | findstr "healthy" >nul
if errorlevel 1 (
    echo    X API 健康检查失败
) else (
    echo    √ API 健康检查通过
)

REM 测试病例列表
echo 2. 测试病例列表接口...
curl -s http://localhost/api/cases/ | findstr "[" >nul
if errorlevel 1 (
    echo    X 病例列表接口失败
) else (
    echo    √ 病例列表接口正常
)

REM 测试统计接口
echo 3. 测试统计接口...
curl -s http://localhost/api/stats/ | findstr "total_cases" >nul
if errorlevel 1 (
    echo    X 统计接口失败
) else (
    echo    √ 统计接口正常
)

REM 测试 Orthanc
echo 4. 测试 Orthanc 服务...
curl -s http://localhost/orthanc/system | findstr "Version" >nul
if errorlevel 1 (
    echo    X Orthanc 服务失败
) else (
    echo    √ Orthanc 服务正常
)

REM 测试前端页面
echo 5. 测试前端页面...
curl -s -o nul -w "%%{http_code}" http://localhost/ | findstr "200" >nul
if errorlevel 1 (
    echo    X 前端页面失败
) else (
    echo    √ 前端页面正常
)

echo.
echo ==========================================
echo   测试完成
echo ==========================================
echo.
echo 如果所有测试都通过，说明平台搭建成功！
echo.
echo 访问地址：
echo   - 主页面: http://localhost
echo   - API 文档: http://localhost/api/docs
echo   - Orthanc 管理: http://localhost/orthanc/
echo   - OHIF Viewer: http://localhost/viewer/
echo.
pause
