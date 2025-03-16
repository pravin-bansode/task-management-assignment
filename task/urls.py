
from django.contrib import admin
from django.urls import path,include
from .views import TaskViewSet,TaskReportView
from rest_framework.routers import DefaultRouter

# Set up the DRF router to automatically handle CRUD operations
router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
urlpatterns = [
   
    # multi-threding to url
    path('task-report-insight/', TaskReportView.as_view()),
   
]+ router.urls
