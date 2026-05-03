"""Redis 缓存管理器"""
import json
import redis
from django.conf import settings


class DeviceDataCache:
    """Redis 缓存管理器"""

    def __init__(self):
        self.redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.BEEADMIN_REDIS_DB_COLLECT,
            decode_responses=False,
        )
        self.alive_redis = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.BEEADMIN_REDIS_DB_ALIVE,
            decode_responses=False,
        )

    # ===== 连接锁 =====
    def acquire_device_lock(self, device_id, timeout=60):
        key = f'beeadmin:lock:collect:{device_id}'
        return self.redis.set(key, '1', nx=True, ex=timeout)

    def release_device_lock(self, device_id):
        self.redis.delete(f'beeadmin:lock:collect:{device_id}')

    # ===== 巡检采集缓存 =====
    def store_raw_output(self, result_id, device_id, command_alias, raw_output):
        key = f'beeadmin:collect:{result_id}:{device_id}:raw'
        self.redis.hset(key, command_alias, raw_output)
        self.redis.expire(key, 1800)  # 30 分钟

    def get_raw_outputs(self, result_id, device_id):
        key = f'beeadmin:collect:{result_id}:{device_id}:raw'
        return self.redis.hgetall(key)

    def delete_raw_outputs(self, result_id, device_id):
        self.redis.delete(f'beeadmin:collect:{result_id}:{device_id}:raw')

    # ===== 巡检解析缓存 =====
    def store_parsed_data(self, result_id, device_id, parsed_data):
        key = f'beeadmin:parse:{result_id}:{device_id}:parsed'
        self.redis.set(key, json.dumps(parsed_data, ensure_ascii=False, default=str), ex=1800)

    def get_parsed_data(self, result_id, device_id):
        key = f'beeadmin:parse:{result_id}:{device_id}:parsed'
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def delete_parsed_data(self, result_id, device_id):
        self.redis.delete(f'beeadmin:parse:{result_id}:{device_id}:parsed')

    # ===== 扫描缓存 =====
    def store_scan_raw(self, task_id, ip, raw_output):
        key = f'beeadmin:scan:{task_id}:{ip}:raw'
        self.redis.set(key, raw_output, ex=600)

    def get_scan_raw(self, task_id, ip):
        return self.redis.get(f'beeadmin:scan:{task_id}:{ip}:raw')

    # ===== 存活检测缓存 =====
    def store_alive_result(self, task_id, device_id, result):
        key = f'beeadmin:alive:{task_id}:{device_id}:result'
        self.alive_redis.set(key, json.dumps(result), ex=300)

    def get_alive_result(self, task_id, device_id):
        data = self.alive_redis.get(f'beeadmin:alive:{task_id}:{device_id}:result')
        return json.loads(data) if data else None

    # ===== 连接计数器 =====
    def incr_alive_connections(self):
        return self.alive_redis.incr('beeadmin:alive:active_connections')

    def decr_alive_connections(self):
        return self.alive_redis.decr('beeadmin:alive:active_connections')

    def get_alive_connections(self):
        val = self.alive_redis.get('beeadmin:alive:active_connections')
        return int(val) if val else 0
