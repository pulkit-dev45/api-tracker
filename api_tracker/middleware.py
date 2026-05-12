import time
from django.contrib.auth.models import User
from .models import ApiLog
from django.conf import settings
ignore_paths=getattr(settings,"API_TRACKER",{}).get("IGNORE_PATHS",[])

class ApiLoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def get_user_ip(self,request):
        x_forwarded_for=request.META.get("HTTP_X_FORWAREDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    
    def __call__(self,request):
        if any(request.path.startswith(path)for path in ignore_paths):
            return self.get_response(request)
        user=request.user if request.user.is_authenticated else None
        start_time=time.time()
        response=self.get_response(request)
        end_time=time.time()
        ipaddress=self.get_user_ip(request)
        responsTime=(end_time-start_time)*1000

        ApiLog.objects.create(
            user=user,
            endPoint=request.path,
            ipAddress=ipaddress,
            statusCode=response.status_code,
            methodType=request.method,
            responseTime=round(responsTime,2)
        )
        return response