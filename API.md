# API 文档

放射科专业病例阅片学习平台 API 文档。

## 基础信息

- **Base URL**: `http://localhost/api`
- **认证**: 暂无（MVP 版本）
- **内容类型**: `application/json`

## 响应格式

### 成功响应

```json
{
  "id": 1,
  "title": "病例标题",
  "description": "病例描述",
  ...
}
```

### 错误响应

```json
{
  "detail": "错误信息"
}
```

## 病例管理

### 创建病例

**请求**

```http
POST /api/cases/
Content-Type: application/json

{
  "title": "肺部CT扫描示例",
  "description": "55岁男性，长期吸烟史，咳嗽咳痰3个月",
  "patient_id": "P001",
  "modality": "CT",
  "body_part": "胸部",
  "diagnosis": "右肺上叶占位性病变，考虑肺癌可能",
  "teaching_points": "1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移",
  "difficulty_level": 3
}
```

**响应**

```json
{
  "id": 1,
  "title": "肺部CT扫描示例",
  "description": "55岁男性，长期吸烟史，咳嗽咳痰3个月",
  "patient_id": "P001",
  "modality": "CT",
  "body_part": "胸部",
  "diagnosis": "右肺上叶占位性病变，考虑肺癌可能",
  "teaching_points": "1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移",
  "difficulty_level": 3,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 获取病例列表

**请求**

```http
GET /api/cases/
GET /api/cases/?skip=0&limit=100
GET /api/cases/?modality=CT
GET /api/cases/?body_part=胸部
GET /api/cases/?difficulty_level=3
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| skip | integer | 否 | 跳过记录数 |
| limit | integer | 否 | 返回记录数 |
| modality | string | 否 | 影像类型筛选 |
| body_part | string | 否 | 检查部位筛选 |
| difficulty_level | integer | 否 | 难度等级筛选 |

**响应**

```json
[
  {
    "id": 1,
    "title": "肺部CT扫描示例",
    "description": "55岁男性，长期吸烟史，咳嗽咳痰3个月",
    "patient_id": "P001",
    "modality": "CT",
    "body_part": "胸部",
    "diagnosis": "右肺上叶占位性病变，考虑肺癌可能",
    "teaching_points": "1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移",
    "difficulty_level": 3,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### 获取单个病例

**请求**

```http
GET /api/cases/{case_id}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | integer | 是 | 病例ID |

**响应**

```json
{
  "id": 1,
  "title": "肺部CT扫描示例",
  "description": "55岁男性，长期吸烟史，咳嗽咳痰3个月",
  "patient_id": "P001",
  "modality": "CT",
  "body_part": "胸部",
  "diagnosis": "右肺上叶占位性病变，考虑肺癌可能",
  "teaching_points": "1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移",
  "difficulty_level": 3,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**错误响应**

```json
{
  "detail": "病例未找到"
}
```

### 更新病例

**请求**

```http
PUT /api/cases/{case_id}
Content-Type: application/json

{
  "title": "更新后的病例标题",
  "description": "更新后的描述"
}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | integer | 是 | 病例ID |

**响应**

```json
{
  "id": 1,
  "title": "更新后的病例标题",
  "description": "更新后的描述",
  "patient_id": "P001",
  "modality": "CT",
  "body_part": "胸部",
  "diagnosis": "右肺上叶占位性病变，考虑肺癌可能",
  "teaching_points": "1. 注意观察肺窗和纵隔窗\n2. 测量病灶大小\n3. 观察有无淋巴结转移",
  "difficulty_level": 3,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 删除病例

**请求**

```http
DELETE /api/cases/{case_id}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | integer | 是 | 病例ID |

**响应**

```json
{
  "message": "病例已删除"
}
```

## 影像管理

### 添加病例影像

**请求**

```http
POST /api/case-images/
Content-Type: application/json

{
  "case_id": 1,
  "dicom_instance_id": "abc123",
  "image_type": "axial",
  "description": "轴位影像"
}
```

**响应**

```json
{
  "id": 1,
  "case_id": 1,
  "dicom_instance_id": "abc123",
  "image_type": "axial",
  "description": "轴位影像",
  "created_at": "2024-01-01T00:00:00"
}
```

### 获取影像列表

**请求**

```http
GET /api/case-images/
GET /api/case-images/?case_id=1
GET /api/case-images/?skip=0&limit=100
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | integer | 否 | 病例ID筛选 |
| skip | integer | 否 | 跳过记录数 |
| limit | integer | 否 | 返回记录数 |

**响应**

```json
[
  {
    "id": 1,
    "case_id": 1,
    "dicom_instance_id": "abc123",
    "image_type": "axial",
    "description": "轴位影像",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### 获取单个影像

**请求**

```http
GET /api/case-images/{image_id}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | integer | 是 | 影像ID |

**响应**

```json
{
  "id": 1,
  "case_id": 1,
  "dicom_instance_id": "abc123",
  "image_type": "axial",
  "description": "轴位影像",
  "created_at": "2024-01-01T00:00:00"
}
```

### 删除影像

**请求**

```http
DELETE /api/case-images/{image_id}
```

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_id | integer | 是 | 影像ID |

**响应**

```json
{
  "message": "影像已删除"
}
```

## 统计接口

### 获取统计数据

**请求**

```http
GET /api/stats/
```

**响应**

```json
{
  "total_cases": 10,
  "total_images": 50,
  "available_modalities": ["CT", "MRI", "X-Ray"]
}
```

## 健康检查

### 服务健康检查

**请求**

```http
GET /api/health
```

**响应**

```json
{
  "status": "healthy",
  "message": "放射科专业病例阅片学习平台 API 运行正常"
}
```

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求错误 |
| 404 | 资源未找到 |
| 422 | 验证错误 |
| 500 | 服务器错误 |

## 示例代码

### Python

```python
import requests

# 创建病例
response = requests.post("http://localhost/api/cases/", json={
    "title": "肺部CT扫描示例",
    "description": "55岁男性，长期吸烟史",
    "modality": "CT"
})
print(response.json())

# 获取病例列表
response = requests.get("http://localhost/api/cases/")
print(response.json())
```

### JavaScript

```javascript
// 创建病例
fetch("http://localhost/api/cases/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: "肺部CT扫描示例",
        description: "55岁男性，长期吸烟史",
        modality: "CT"
    })
})
.then(response => response.json())
.then(data => console.log(data));

// 获取病例列表
fetch("http://localhost/api/cases/")
    .then(response => response.json())
    .then(data => console.log(data));
```

### cURL

```bash
# 创建病例
curl -X POST http://localhost/api/cases/ \
  -H "Content-Type: application/json" \
  -d '{"title": "肺部CT扫描示例", "description": "55岁男性，长期吸烟史", "modality": "CT"}'

# 获取病例列表
curl http://localhost/api/cases/

# 获取单个病例
curl http://localhost/api/cases/1

# 更新病例
curl -X PUT http://localhost/api/cases/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "更新后的标题"}'

# 删除病例
curl -X DELETE http://localhost/api/cases/1
```

## 交互式文档

启动服务后，可以通过以下地址访问交互式 API 文档：

- **Swagger UI**: http://localhost/api/docs
- **ReDoc**: http://localhost/api/redoc

## 限制

- 暂无认证机制（MVP 版本）
- 暂无分页限制
- 暂无速率限制

## 更新日志

请参阅 [CHANGELOG.md](CHANGELOG.md) 了解 API 更新历史。
