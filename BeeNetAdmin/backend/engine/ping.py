"""Ping 检测"""
import subprocess
import re
import platform


class PingChecker:
    """Ping 检测器"""

    def ping(self, host, count=3, timeout=5):
        """
        执行 Ping 检测
        返回 {success, latency_ms, packet_loss}
        """
        try:
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout_param = '-w' if platform.system().lower() == 'windows' else '-W'
            cmd = ['ping', param, str(count), timeout_param, str(timeout), host]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)

            output = result.stdout
            success = result.returncode == 0

            # 解析延迟
            latency = None
            m = re.search(r'time[=<](\d+\.?\d*)', output)
            if m:
                latency = float(m.group(1))

            # 解析丢包率
            loss = 0.0
            m = re.search(r'(\d+)%\s*(?:packet\s*)?loss', output)
            if m:
                loss = float(m.group(1))

            return {
                'success': success,
                'latency_ms': latency,
                'packet_loss': loss,
            }
        except Exception:
            return {
                'success': False,
                'latency_ms': None,
                'packet_loss': 100.0,
            }
