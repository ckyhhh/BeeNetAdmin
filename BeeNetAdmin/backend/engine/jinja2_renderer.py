"""Jinja2 渲染器"""
import os
from jinja2 import Environment, FileSystemLoader
from django.conf import settings


class Jinja2Renderer:
    """Jinja2 模板渲染器"""

    def __init__(self):
        template_dir = os.path.join(settings.BASE_DIR.parent, 'templates', 'jinja2')
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name, context):
        """渲染 Jinja2 模板"""
        template = self.env.get_template(template_name)
        return template.render(**context)
