"""巡检 Admin"""
from django.contrib import admin
from .models import InspectionTemplate, InspectionTask, InspectionResult

admin.site.register(InspectionTemplate)
admin.site.register(InspectionTask)
admin.site.register(InspectionResult)
