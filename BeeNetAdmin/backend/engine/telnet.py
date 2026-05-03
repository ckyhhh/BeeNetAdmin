"""Telnet 客户端"""
import telnetlib
import time
import re


class TelnetClient:
    """Telnet 连接客户端"""

    def __init__(self):
        self.tn = None
        self.prompt = None

    def connect(self, host, port=23, username='admin', password='', timeout=30):
        """建立 Telnet 连接"""
        self.tn = telnetlib.Telnet(host, port, timeout=timeout)

        # 等待用户名提示
        idx, m, text = self.tn.expect([b'[Uu]sername:', b'[Ll]ogin:'], timeout=timeout)
        if idx >= 0:
            self.tn.write(username.encode('ascii') + b'\n')

        # 等待密码提示
        idx, m, text = self.tn.expect([b'[Pp]assword:'], timeout=timeout)
        if idx >= 0:
            self.tn.write(password.encode('ascii') + b'\n')

        # 等待提示符
        time.sleep(2)
        self._detect_prompt()

    def execute(self, command, timeout=30):
        """执行单条命令"""
        if not self.tn:
            raise RuntimeError('Telnet 未连接')

        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(1)

        output = b''
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                chunk = self.tn.read_very_eager()
                if chunk:
                    output += chunk
                    # 处理分页
                    if b'--More--' in output or b' ---- More ----' in output:
                        self.tn.write(b' ')
                        output = output.replace(b'--More--', b'').replace(b' ---- More ----', b'')
                        continue
                    # 检查提示符
                    decoded = output.decode('utf-8', errors='replace')
                    if self.prompt and self.prompt in decoded:
                        break
                else:
                    time.sleep(0.2)
            except EOFError:
                break

        result = output.decode('utf-8', errors='replace')
        # 去掉命令回显和提示符
        lines = result.split('\n')
        if lines and command in lines[0]:
            lines = lines[1:]
        if lines and self.prompt and self.prompt in lines[-1]:
            lines = lines[:-1]
        return '\n'.join(lines).strip()

    def execute_batch(self, commands, timeout=30):
        """逐条执行命令"""
        results = {}
        for cmd_info in commands:
            alias = cmd_info.get('alias', '')
            cmd = cmd_info.get('cmd', '')
            try:
                results[alias] = self.execute(cmd, timeout=timeout)
            except Exception as e:
                results[alias] = f'ERROR: {e}'
        return results

    def _detect_prompt(self):
        """自动检测提示符"""
        self.tn.write(b'\n')
        time.sleep(1)
        try:
            raw = self.tn.read_very_eager().decode('utf-8', errors='replace')
            lines = raw.strip().split('\n')
            if lines:
                self.prompt = lines[-1].strip()
        except Exception:
            self.prompt = '#'

    def close(self):
        """关闭连接"""
        if self.tn:
            try:
                self.tn.close()
            except Exception:
                pass
            self.tn = None
