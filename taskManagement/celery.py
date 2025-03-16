from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManagement.settings')

app = Celery('taskManagement')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Correct task autodiscovery path based on your project structure
app.autodiscover_tasks(['task.tasks'])  # Adjust this path if needed

# Celery configuration to use Redis as broker and backend
app.conf.update(
    broker_url='redis://redis:6379/3',
    result_backend='redis://redis:6379/3',
)