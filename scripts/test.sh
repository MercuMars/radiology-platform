#!/bin/bash

# 放射科专业病例阅片学习平台测试脚本

echo "=========================================="
echo "  放射科专业病例阅片学习平台 - 测试"
echo "=========================================="
echo ""

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 测试 API 健康检查
echo "1. 测试 API 健康检查..."
response=$(curl -s http://localhost/api/health)
if echo "$response" | grep -q "healthy"; then
    echo "   ✓ API 健康检查通过"
else
    echo "   ✗ API 健康检查失败"
    echo "   响应: $response"
fi

# 测试病例列表
echo "2. 测试病例列表接口..."
response=$(curl -s http://localhost/api/cases/)
if echo "$response" | grep -q "\["; then
    echo "   ✓ 病例列表接口正常"
else
    echo "   ✗ 病例列表接口失败"
    echo "   响应: $response"
fi

# 测试统计接口
echo "3. 测试统计接口..."
response=$(curl -s http://localhost/api/stats/)
if echo "$response" | grep -q "total_cases"; then
    echo "   ✓ 统计接口正常"
else
    echo "   ✗ 统计接口失败"
    echo "   响应: $response"
fi

# 测试 Orthanc
echo "4. 测试 Orthanc 服务..."
response=$(curl -s http://localhost/orthanc/system)
if echo "$response" | grep -q "Version"; then
    echo "   ✓ Orthanc 服务正常"
else
    echo "   ✗ Orthanc 服务失败"
    echo "   响应: $response"
fi

# 测试前端页面
echo "5. 测试前端页面..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/)
if [ "$response" = "200" ]; then
    echo "   ✓ 前端页面正常"
else
    echo "   ✗ 前端页面失败"
    echo "   HTTP 状态码: $response"
fi

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "如果所有测试都通过，说明平台搭建成功！"
echo ""
echo "访问地址："
echo "  - 主页面: http://localhost"
echo "  - API 文档: http://localhost/api/docs"
echo "  - Orthanc 管理: http://localhost/orthanc/"
echo "  - OHIF Viewer: http://localhost/viewer/"
echo ""
