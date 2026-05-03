"""AI 助手模型"""
from django.db import models


class AIConfig(models.Model):
    """AI 配置"""
    api_key = models.TextField('API Key（加密）')
    base_url = models.CharField('API地址', max_length=512, default='https://api.deepseek.com')
    model = models.CharField('模型', max_length=128, default='deepseek-chat')
    temperature = models.DecimalField('温度', max_digits=3, decimal_places=2, default=0.30)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'ai_config'
        verbose_name = 'AI配置'
