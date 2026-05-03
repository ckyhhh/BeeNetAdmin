"""设备检测器"""
import re


class DeviceDetector:
    """自动识别设备厂商/型号/OS"""

    def detect(self, connection):
        """通过连接自动识别设备"""
        raw = connection.execute('show version', timeout=15)
        if not raw:
            raw = connection.execute('display version', timeout=15)
        return self.parse(raw or '')

    def parse(self, raw_output):
        """从 version 输出解析设备信息"""
        info = {
            'vendor': '',
            'model': '',
            'os_version': '',
            'hostname': '',
            'serial_number': '',
        }

        # Cisco IOS
        if 'Cisco IOS' in raw_output or 'cisco' in raw_output.lower():
            info['vendor'] = 'Cisco'
            m = re.search(r'Version\s+(\S+)', raw_output)
            if m:
                info['os_version'] = m.group(1)
            m = re.search(r'Model number\s*:\s*(\S+)', raw_output)
            if m:
                info['model'] = m.group(1)
            m = re.search(r'Processor board ID\s+(\S+)', raw_output)
            if m:
                info['serial_number'] = m.group(1)
            m = re.search(r'^(\S+)\s+uptime is', raw_output, re.MULTILINE)
            if m:
                info['hostname'] = m.group(1)

        # Huawei VRP
        elif 'Huawei' in raw_output or 'HUAWEI' in raw_output or 'VRP' in raw_output:
            info['vendor'] = 'Huawei'
            m = re.search(r'VERSION\s*:\s*(\S+)', raw_output, re.IGNORECASE)
            if m:
                info['os_version'] = m.group(1)
            m = re.search(r'Model\s*:\s*(\S+)', raw_output, re.IGNORECASE)
            if m:
                info['model'] = m.group(1)
            m = re.search(r'Serial Number\s*:\s*(\S+)', raw_output, re.IGNORECASE)
            if m:
                info['serial_number'] = m.group(1)
            m = re.search(r'<(\S+)>', raw_output)
            if m:
                info['hostname'] = m.group(1)

        # H3C Comware
        elif 'H3C' in raw_output or 'Comware' in raw_output:
            info['vendor'] = 'H3C'
            m = re.search(r'Version\s+(\S+)', raw_output)
            if m:
                info['os_version'] = m.group(1)
            m = re.search(r'Product\s*:\s*(.+)', raw_output)
            if m:
                info['model'] = m.group(1).strip()

        return info
