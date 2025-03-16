import os
import django  # Import django first
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Ensure DJANGO_SETTINGS_MODULE is set before any Django-related imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskManagement.settings')

# Explicitly set up Django
django.setup()

import task.routing  # Now you can import the routing after Django is set up

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests (via runserver)
    "websocket": AuthMiddlewareStack(  # Handles WebSocket connections
        URLRouter(
            task.routing.websocket_urlpatterns  # Your WebSocket routes
        )
    ),
})
