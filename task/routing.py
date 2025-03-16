from django.urls import re_path
from . import consumers  # Import your WebSocket consumer

websocket_urlpatterns = [
    re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),  # Example WebSocket endpoint
]