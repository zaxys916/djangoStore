#!/bin/bash

echo "========================================="
echo "  Django 启动脚本"
echo "========================================="

# 等待 MySQL
echo "[1/4] 等待 MySQL..."
while ! nc -z $DB_HOST $DB_PORT; do
    echo "  等待 MySQL 就绪..."
    sleep 1
done
echo "  ✅ MySQL 已就绪"

# 等待 Redis
echo "[2/4] 等待 Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
    echo "  等待 Redis 就绪..."
    sleep 1
done
echo "  ✅ Redis 已就绪"

# 数据库迁移
echo "[3/4] 执行数据库迁移..."
python manage.py migrate --noinput

# 收集静态文件
echo "[4/4] 收集静态文件..."
python manage.py collectstatic --noinput

echo "========================================="
echo "  启动 Gunicorn..."
echo "========================================="

exec "$@"