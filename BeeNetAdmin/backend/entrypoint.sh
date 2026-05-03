#!/bin/bash
set -e

echo "等待 MySQL 就绪..."
python -c "
import time, os, MySQLdb
for i in range(30):
    try:
        MySQLdb.connect(
            host=os.environ.get('DB_HOST','localhost'),
            port=int(os.environ.get('DB_PORT',3306)),
            user=os.environ.get('DB_USER','beeadmin'),
            passwd=os.environ.get('DB_PASSWORD','beeadmin123'),
            db=os.environ.get('DB_NAME','beeadmin')
        )
        print('MySQL 已就绪')
        break
    except Exception:
        print(f'等待 MySQL... ({i+1}/30)')
        time.sleep(2)
"

echo "执行数据库迁移..."
python manage.py migrate --noinput

echo "收集静态文件..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "启动服务..."
exec "$@"
