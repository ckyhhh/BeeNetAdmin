"""TextFSM 解析器"""
import os
import textfsm
from django.conf import settings


class TextFSMParser:
    """TextFSM 模板解析器"""

    def __init__(self):
        self.template_dir = os.path.join(settings.BASE_DIR.parent, 'templates', 'textfsm')

    def parse(self, vendor, template_name, raw_output):
        """加载 TextFSM 模板，解析原始输出"""
        template_path = self.get_template_path(vendor, template_name)
        if not os.path.exists(template_path):
            return [{'raw': raw_output}]

        with open(template_path) as f:
            fsm = textfsm.TextFSM(f)
            result = fsm.ParseText(raw_output)
            headers = fsm.header
            return [dict(zip(headers, row)) for row in result]

    def get_template_path(self, vendor, template_name):
        """获取模板文件路径"""
        if not template_name.endswith('.textfsm'):
            template_name += '.textfsm'
        return os.path.join(self.template_dir, vendor, template_name)
