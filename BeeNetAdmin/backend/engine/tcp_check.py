"""TCP 检测"""
import socket
import time


class TCPChecker:
    """TCP 连接检测器"""

    def check(self, host, port=22, timeout=5):
        """
        TCP 连接检测
        返回 {is_alive, latency_ms}
        """
        start = time.time()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            latency = (time.time() - start) * 1000
            sock.close()
            return {
                'is_alive': result == 0,
                'latency_ms': round(latency, 2),
            }
        except Exception:
            return {
                'is_alive': False,
                'latency_ms': None,
            }
