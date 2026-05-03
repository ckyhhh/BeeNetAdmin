"""存活检测 Admin"""
from django.contrib import admin
from .models import AliveTask, AliveResult

admin.site.register(AliveTask)
admin.site.register(AliveResult)
