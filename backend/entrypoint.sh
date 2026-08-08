#!/bin/sh
set -e

echo "=== [1/5] 检测并安装 Python 依赖 ==="
pip install --no-cache-dir -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ || \
pip install --no-cache-dir -r /app/requirements.txt

echo "=== [2/5] 等待数据库就绪 ==="
while ! nc -z "${DB_HOST:-mysql}" "${DB_PORT:-3306}"; do
    echo "等待数据库 ${DB_HOST:-mysql}:${DB_PORT:-3306} ..."
    sleep 2
done
echo "数据库已就绪"

echo "=== [3/5] 执行数据库迁移 ==="
python manage.py migrate --noinput

echo "=== [4/5] 收集静态文件 ==="
python manage.py collectstatic --noinput

echo "=== [5/5] 启动 Django ==="
python manage.py runserver 0.0.0.0:8000
