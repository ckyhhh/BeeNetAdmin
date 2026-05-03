"""通知 Admin"""
from django.contrib import admin
from .models import Notification, EmailConfig

admin.site.register(Notification)
admin.site.register(EmailConfig)
