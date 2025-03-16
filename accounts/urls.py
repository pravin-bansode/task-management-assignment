from rest_framework_simplejwt import views as jwt_views

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Set up the DRF router to automatically handle CRUD operations
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
   
   
    # path('/', include(router.urls)),
   # JWT Token Endpoints
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (Get access and refresh token)
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
] + router.urls
