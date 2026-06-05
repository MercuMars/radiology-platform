@echo off
REM 放射科专业病例阅片学习平台 - 文件检查脚本 (Windows)

echo ==========================================
echo   放射科专业病例阅片学习平台 - 文件检查
echo ==========================================
echo.

setlocal enabledelayedexpansion

set "missing_count=0"

REM 检查必要文件
call :check_file "docker-compose.yml"
call :check_file "nginx.conf"
call :check_file "orthanc-config\orthanc.json"
call :check_file "backend\Dockerfile"
call :check_file "backend\requirements.txt"
call :check_file "backend\app\main.py"
call :check_file "backend\app\__init__.py"
call :check_file "backend\app\database.py"
call :check_file "backend\app\models.py"
call :check_file "backend\app\schemas.py"
call :check_file "backend\app\config.py"
call :check_file "backend\app\routers\__init__.py"
call :check_file "backend\app\routers\case.py"
call :check_file "backend\app\routers\image.py"
call :check_file "backend\app\routers\stats.py"
call :check_file "frontend\html\index.html"
call :check_file "frontend\ohif-config.js"
call :check_file "scripts\init-db.sql"
call :check_file "scripts\start.sh"
call :check_file "scripts\start.bat"
call :check_file "scripts\test.sh"
call :check_file "scripts\test.bat"
call :check_file ".env"
call :check_file ".gitignore"
call :check_file "README.md"
call :check_file "INSTALL.md"

echo.
echo ==========================================
echo   检查完成
echo ==========================================
echo.

if !missing_count! equ 0 (
    echo √ 所有必要文件都已存在
    echo.
    echo 可以运行以下命令启动平台：
    echo   scripts\start.bat
) else (
    echo X 发现 !missing_count! 个缺失文件
    echo.
    echo 请确保所有文件都已正确创建
)

echo.
pause
exit /b 0

:check_file
if exist "%~1" (
    echo √ %~1
) else (
    echo X %~1 (缺失)
    set /a missing_count+=1
)
exit /b 0
