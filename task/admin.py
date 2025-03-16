from django.contrib import admin

# Register your models here.
from .models import TaskTable

admin.site.register(TaskTable)