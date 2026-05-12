from . import views
from django.urls import path
urlpatterns = [
    path("top/",views.TopApiEndpointsView.as_view()),
    path("slow/",views.SlowApiView.as_view()),
    path("error/",views.ErrorApiView.as_view()),
    path("alllogs/",views.alllogs.as_view()),
    path("dashboard/",views.dashboard),
]