from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from rest_framework.exceptions import PermissionDenied


from .serializers import UserSerializer


# Pagination class (if you want to customize pagination behavior)
class UserPagination(PageNumberPagination):
    page_size = 10  # You can change this to any number
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
# ViewSet for CRUD operations on User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this API
    pagination_class = UserPagination  # Use the custom pagination class
    
    
    def perform_update(self, serializer):
        # Check if the user is updating their own data, or if they are a superuser
        if self.request.user != serializer.instance and not self.request.user.is_superuser:
            raise PermissionDenied("You can only update your own data.")
        serializer.save()

    def perform_partial_update(self, serializer):
        # Check if the user is updating their own data, or if they are a superuser
        if self.request.user != serializer.instance and not self.request.user.is_superuser:
            raise PermissionDenied("You can only partially update your own data.")
        serializer.save()