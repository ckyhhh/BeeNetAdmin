"""SSH 客户端"""
import paramiko
import time


class SSHClient:
    """SSH 连接客户端"""

    def __init__(self):
        self.client = None
        self.shell = None

    def connect(self, host, port=22, username='admin', password=None, key=None, timeout=30):
        """建立 SSH 连接"""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = {
            'hostname': host,
            'port': port,
            'username': username,
            'timeout': timeout,
            'look_for_keys': False,
            'allow_agent': False,
        }

        if key:
            connect_kwargs['pkey'] = paramiko.RSAKey.from_private_key_string(key)
        elif password:
            connect_kwargs['password'] = password

        self.client.connect(**connect_kwargs)
        self.shell = self.client.invoke_shell()
        time.sleep(1)
        # 清空欢迎信息
        if self.shell.recv_ready():
            self.shell.recv(65536)

    def execute(self, command, timeout=30):
        """执行单条命令，返回输出文本"""
        if not self.shell:
            raise RuntimeError('SSH 未连接')

        self.shell.send(command + '\n')
        output = ''
        end_time = time.time() + timeout

        while time.time() < end_time:
            if self.shell.recv_ready():
                chunk = self.shell.recv(65536).decode('utf-8', errors='replace')
                output += chunk
                # 检查是否到达提示符
                if self._is_prompt(chunk):
                    break
            else:
                time.sleep(0.1)

        # 去掉命令回显和提示符
        lines = output.split('\n')
        if lines and command in lines[0]:
            lines = lines[1:]
        if lines and self._is_prompt(lines[-1]):
            lines = lines[:-1]
        return '\n'.join(lines).strip()

    def execute_batch(self, commands, timeout=30):
        """逐条执行命令，返回 {alias: output} 字典"""
        results = {}
        for cmd_info in commands:
            alias = cmd_info.get('alias', '')
            cmd = cmd_info.get('cmd', '')
            try:
                results[alias] = self.execute(cmd, timeout=timeout)
            except Exception as e:
                results[alias] = f'ERROR: {e}'
        return results

    def _is_prompt(self, text):
        """判断是否为命令提示符"""
        prompts = ['#', '>', '$', ']', ':~#', ':~$']
        last_line = text.strip().split('\n')[-1].strip() if text.strip() else ''
        return any(last_line.endswith(p) for p in prompts)

    def close(self):
        """关闭连接"""
        if self.shell:
            try:
                self.shell.close()
            except Exception:
                pass
        if self.client:
            try:
                self.client.close()
            except Exception:
                pass
        self.shell = None
        self.client = None
