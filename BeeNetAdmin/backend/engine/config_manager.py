"""配置管理器"""
import difflib


class ConfigManager:
    """设备配置管理"""

    def get_running_config(self, client, vendor):
        """获取运行配置"""
        commands = {
            'cisco': 'show running-config',
            'huawei': 'display current-configuration',
            'h3c': 'display current-configuration',
        }
        cmd = commands.get(vendor.lower(), 'show running-config')
        return client.execute(cmd, timeout=60)

    def get_startup_config(self, client, vendor):
        """获取启动配置"""
        commands = {
            'cisco': 'show startup-config',
            'huawei': 'display saved-configuration',
            'h3c': 'display saved-configuration',
        }
        cmd = commands.get(vendor.lower(), 'show startup-config')
        return client.execute(cmd, timeout=60)

    def diff_configs(self, running, startup):
        """计算两个配置的差异"""
        running_lines = (running or '').splitlines()
        startup_lines = (startup or '').splitlines()
        return list(difflib.unified_diff(startup_lines, running_lines, lineterm=''))

    def format_diff_html(self, running, startup):
        """格式化为 HTML diff"""
        running_lines = (running or '').splitlines()
        startup_lines = (startup or '').splitlines()
        diff = difflib.HtmlDiff()
        return diff.make_table(startup_lines, running_lines, '启动配置', '运行配置')
