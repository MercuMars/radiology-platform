# 放射科专业病例阅片学习平台 - Makefile

.PHONY: help build up down restart logs test clean

# 默认目标
help:
	@echo "放射科专业病例阅片学习平台"
	@echo ""
	@echo "可用命令:"
	@echo "  make build    - 构建 Docker 镜像"
	@echo "  make up       - 启动所有服务"
	@echo "  make down     - 停止所有服务"
	@echo "  make restart  - 重启所有服务"
	@echo "  make logs     - 查看日志"
	@echo "  make test     - 运行测试"
	@echo "  make clean    - 清理所有数据"
	@echo "  make status   - 查看服务状态"
	@echo "  make db       - 初始化数据库"
	@echo "  make shell    - 进入 API 容器"

# 构建 Docker 镜像
build:
	docker-compose build

# 启动所有服务
up:
	docker-compose up -d

# 停止所有服务
down:
	docker-compose down

# 重启所有服务
restart:
	docker-compose restart

# 查看日志
logs:
	docker-compose logs -f

# 查看特定服务日志
logs-api:
	docker-compose logs -f api

logs-db:
	docker-compose logs -f db

logs-orthanc:
	docker-compose logs -f orthanc

# 运行测试
test:
	./scripts/test.sh

# 清理所有数据
clean:
	docker-compose down -v
	docker system prune -f

# 查看服务状态
status:
	docker-compose ps

# 初始化数据库
db:
	docker-compose exec db psql -U radio -d cases -f /docker-entrypoint-initdb.d/init.sql

# 进入 API 容器
shell:
	docker-compose exec api /bin/bash

# 进入数据库容器
db-shell:
	docker-compose exec db psql -U radio -d cases

# 查看 API 文档
docs:
	@echo "API 文档: http://localhost/api/docs"

# 检查文件
check:
	./scripts/check-files.sh

# 开发模式（本地运行）
dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 安装依赖
install:
	cd backend && pip install -r requirements.txt

# 代码格式化
format:
	cd backend && black app/
	cd backend && isort app/

# 代码检查
lint:
	cd backend && flake8 app/
	cd backend && mypy app/

# 运行测试（本地）
test-local:
	cd backend && pytest

# 生成 API 文档
api-docs:
	cd backend && python -m app.main
