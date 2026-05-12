from django.contrib import admin
from .models import ApiLog

@admin.register(ApiLog)
class ApiLogadmin(admin.ModelAdmin):
    list_display=["id","user","endPoint","ipAddress","statusCode","methodType","responseTime","timeStamp"]