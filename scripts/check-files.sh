#!/bin/bash

# 放射科专业病例阅片学习平台 - 文件检查脚本

echo "=========================================="
echo "  放射科专业病例阅片学习平台 - 文件检查"
echo "=========================================="
echo ""

# 检查必要文件
files=(
    "docker-compose.yml"
    "nginx.conf"
    "orthanc-config/orthanc.json"
    "backend/Dockerfile"
    "backend/requirements.txt"
    "backend/app/main.py"
    "backend/app/__init__.py"
    "backend/app/database.py"
    "backend/app/models.py"
    "backend/app/schemas.py"
    "backend/app/config.py"
    "backend/app/routers/__init__.py"
    "backend/app/routers/case.py"
    "backend/app/routers/image.py"
    "backend/app/routers/stats.py"
    "frontend/html/index.html"
    "frontend/ohif-config.js"
    "scripts/init-db.sql"
    "scripts/start.sh"
    "scripts/start.bat"
    "scripts/test.sh"
    "scripts/test.bat"
    ".env"
    ".gitignore"
    "README.md"
    "INSTALL.md"
)

missing_files=()

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "✗ $file (缺失)"
        missing_files+=("$file")
    fi
done

echo ""
echo "=========================================="
echo "  检查完成"
echo "=========================================="
echo ""

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✓ 所有必要文件都已存在"
    echo ""
    echo "可以运行以下命令启动平台："
    echo "  Windows: scripts\\start.bat"
    echo "  Linux/macOS: ./scripts/start.sh"
else
    echo "✗ 发现 ${#missing_files[@]} 个缺失文件："
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
    echo "请确保所有文件都已正确创建"
fi

echo ""
