from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ApiLog
from rest_framework.permissions import BasePermission
from django.db.models import Count , Avg
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test

class IsAdminOrStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


class TopApiEndpointsView(APIView):
    permission_classes=[IsAdminOrStaff]
    def get(self,request):
        log=ApiLog.objects.all()
        try:
            limit=int(request.GET.get("limit",5))
        except ValueError:
            limit=5
        limit = min(limit,50)
        time_filter=request.GET.get("time")
        now=timezone.now()
        if time_filter=="1h":
            start_time=now-timedelta(hours=1)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="24h":
            start_time=now-timedelta(hours=24)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="7d":
            start_time=now-timedelta(days=7)
            log=log.filter(created_at__gte=start_time)
        else:
            log=ApiLog.objects.all()

        data=(
             log
              .values("endPoint")
              .annotate(total=Count("id"))
              .order_by("-total")[:limit]
              )
        return Response(data)

class SlowApiView(APIView):
    permission_classes=[IsAdminOrStaff]
    def get(self,request):
        log=ApiLog.objects.all()
        try:
            limit=int(request.GET.get("limit",5))
        except ValueError:
            limit=5
        limit = min(limit,50)
        time_filter=request.GET.get("time")
        now=timezone.now()
        if time_filter=="1h":
            start_time=now-timedelta(hours=1)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="24h":
            start_time=now-timedelta(hours=24)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="7d":
            start_time=now-timedelta(days=7)
            log=log.filter(created_at__gte=start_time)
        else:
            log=ApiLog.objects.all()
        data=log.values("endPoint").annotate(avg_time=Avg("responseTime")).order_by("-avg_time")[:limit]
        return Response(data)


class ErrorApiView(APIView):
    permission_classes=[IsAdminOrStaff]
    def get(self,request):
        log=ApiLog.objects.all()
        try:
            limit=int(request.GET.get("limit",5))
        except ValueError:
            limit=5
        limit = min(limit,50)
        try:
            time_filter=request.GET.get("time")
        except ValueError:
            time_filter="24h"

        now=timezone.now()
        if time_filter=="1h":
            start_time=now-timedelta(hours=1)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="24h":
            
            start_time=now-timedelta(hours=24)
            log=log.filter(created_at__gte=start_time)
        elif time_filter=="7d":
            
            start_time=now-timedelta(days=7)
            log=log.filter(created_at__gte=start_time)
        else:
            log=ApiLog.objects.all()
        data=log.filter(statusCode__gte=400).values("endPoint","statusCode")[:limit]
        return Response(data)

class alllogs(APIView):
    permission_classes=[IsAdminOrStaff]
    def get(self,request):
        search=request.GET.get("search")
        record=request.GET.get("record",100)
        daydata=request.GET.get("daydata")
        page=request.GET.get("page",1)
        log=ApiLog.objects.all()
        if search:
            log=log.filter(Q(ipAddress__icontains=search)|Q(endPoint__icontains=search))

        now = timezone.now()
        if daydata == "1h":
            log = log.filter(
                timeStamp__gte=now - timedelta(hours=1)
            )

        elif daydata == "24h":
            log = log.filter(
                timeStamp__gte=now - timedelta(hours=24)
            )

        elif daydata == "7d":
            log = log.filter(
                timeStamp__gte=now - timedelta(days=7)
            )
            
        paginator=Paginator(log.order_by("-timeStamp"),record)
        page_obj=paginator.get_page(page)

        data=list(page_obj.object_list.values(
            "endPoint",
            "ipAddress",
            "responseTime",
            "statusCode",
            "timeStamp",
            "methodType"
        ))
        return JsonResponse({
            "data":data,
            "has_next":page_obj.has_next()
        })
@user_passes_test(is_admin_or_staff)
def dashboard(request):
    return render(request,"api_tracker/dash4.html")