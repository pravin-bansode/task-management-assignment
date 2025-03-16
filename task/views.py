from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import TaskTable
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly

from rest_framework import viewsets

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied


from django_filters.rest_framework import DjangoFilterBackend

from .filters import TaskFilter

from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status

# multi threding import
import concurrent.futures
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone


from task.tasks import send_task_assigned_email

# Pagination class (if you want to customize pagination behavior)
class TaskPagination(PageNumberPagination):
    page_size = 10  # You can change this to any number
    page_size_query_param = 'page_size'
    max_page_size = 20
    
    
    
    
    
    
# ViewSet for CRUD operations on User
class TaskViewSet(viewsets.ModelViewSet):
   
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Ensure only authenticated users can access this API
    pagination_class = TaskPagination  # Use the custom pagination class
    
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    
    def get_queryset(self):
        querry = TaskTable.objects.all().order_by('-created_at')
        cached_data_task_list = cache.get('task_list')
        if cached_data_task_list:
            # Return cached data
            # print('cache hit')
            return cached_data_task_list

        # If no cache, fetch data and cache it
        
        
        # Cache the response data
        cache.set('task_list',querry, timeout=60 * 60)  
        # 60 minutes cache
        # print("cache miss")
        return querry
    
    
    
    
    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the current authenticated user
        user = self.request.user  # Get the logged-in user from the request context
        task = serializer.save(created_by=user)  # Save the task with the current user as `created_by`

        if task.assigned_to:
            # Trigger Celery task for sending email when the task is assigned
            send_task_assigned_email.delay(task.id)
        
        channel_layer =  get_channel_layer()
        
        task_serializer = TaskSerializer(task)
        
        async_to_sync(channel_layer.group_send)(
            'task_tasks',
            {
                'action': 'creation',
                'type': 'task_create',
                'task': task_serializer.data
            }
        )
        
        
        
    def perform_update(self, serializer):
        # Check if the user is updating their own data, or if they are a superuser
        if self.request.user != serializer.instance.created_by  and not self.request.user.is_superuser:
            raise PermissionDenied("You can only update your own task data.")
        task = serializer.save()
        
        
        if task.assigned_to:
            # Trigger Celery task for sending email when the task is assigned
            send_task_assigned_email.delay(task.id)
        

        
        # Notify WebSocket clients about task update
        channel_layer = get_channel_layer()
        task_serializer = TaskSerializer(task)
        # Send message to WebSocket clients
        async_to_sync(channel_layer.group_send)(
            'task_tasks',
            {
                'action': 'update',
                'type': 'task_update',
                'task': task_serializer.data
            }
        )
      

    def perform_partial_update(self, serializer):
        # Check if the user is updating their own data, or if they are a superuser
        if self.request.user != serializer.instance.created_by  and not self.request.user.is_superuser:
            raise PermissionDenied("You can only partially update your own task data.")
        task = serializer.save()
        
        if task.assigned_to:
            # Trigger Celery task for sending email when the task is assigned
            send_task_assigned_email.delay(task.id)
        
       
        
        # Notify WebSocket clients about task update
        channel_layer = get_channel_layer()
        task_serializer = TaskSerializer(task)
        channel_layer.group_send(
            'task_tasks',  # Replace with appropriate group name
            {
                'action':'update',
                'type': 'task_update', #method name herre
                'task': task_serializer.data
            }
        )
        # print('vies update partial update')

        
    def perform_destroy(self, instance):
        # Notify WebSocket clients about task deletion
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'task_tasks',
            {
                'type': 'task_delete',
                'task_id': instance.id,
               
            }
        )
        instance.delete()
        
        
        



# MULTI THREDING HERE IN THIS 
class TaskReportView(APIView):
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def count_all_task(self, tasks):
        """ Count all the tasks form the db
        """
        
        return tasks.count()

    def count_completed(self, tasks):
        """
        Count the number of completed tasks.
        """
        return tasks.filter(status='COMPLETED').count()

    def count_pending(self, tasks):
        """
        Count the number of pending tasks.
        """
        return tasks.filter(status='PENDING').count()

    def categorize_by_priority(self, tasks):
        """
        Categorize tasks by priority.
        """
        priorities = ['LOW', 'MEDIUM', 'HIGH', 'URGENT']
        task_count_by_priority = {priority: tasks.filter(priority=priority).count() for priority in priorities}
        return task_count_by_priority

    def categorize_by_status(self, tasks):
        """
        Categorize tasks by their status.
        """
        statuses = ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'ARCHIVED']
        task_count_by_status = {status: tasks.filter(status=status).count() for status in statuses}
        return task_count_by_status

    def group_by_created_by_user(self, tasks):
        """
        Group tasks by the user they are created by user.
        """
        assigned_tasks = tasks.values('created_by__username').annotate(count=Count('created_by__username'))
        return {task['created_by__username']: task['count'] for task in assigned_tasks}
    
    
    def group_by_assigned_to_user(self, tasks):
        """
        Group tasks by the user they are assigned to user.
        """
        assigned_tasks = tasks.values('assigned_to__username').annotate(count=Count('assigned_to__username'))
        return {task['assigned_to__username']: task['count'] for task in assigned_tasks}

    def tasks_due_soon(self, tasks):
        """
        Count tasks that are due within the next 24 hours.
        """
        now = timezone.now()
        return tasks.filter(due_date__lte=now + timedelta(days=1), status='PENDING').count()
    

    def generate_report(self, tasks):
        """
        Use ThreadPoolExecutor to execute all the functions concurrently and generate the report.
        """
        # Create a thread pool to run each function concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            count_all_tasks = executor.submit(self.count_all_task, tasks)
            future_completed = executor.submit(self.count_completed, tasks)
            future_pending = executor.submit(self.count_pending, tasks)
            future_priority = executor.submit(self.categorize_by_priority, tasks)
            future_status = executor.submit(self.categorize_by_status, tasks)
            future_created = executor.submit(self.group_by_created_by_user, tasks)
            future_assigned = executor.submit(self.group_by_assigned_to_user, tasks)
            future_due_soon = executor.submit(self.tasks_due_soon, tasks)

            # Wait for all tasks to complete and get their results
            count_all = count_all_tasks.result()
            completed = future_completed.result()
            pending = future_pending.result()
            tasks_by_priority = future_priority.result()
            tasks_by_status = future_status.result()
            tasks_created = future_created.result()
            tasks_assigned = future_assigned.result()
            tasks_due_soon = future_due_soon.result()
           

        return {
            'total': count_all,
            'completed': completed,
            'pending': pending,
            'tasks_by_priority': tasks_by_priority,
            'tasks_by_status': tasks_by_status,
            'tasks_assigned': tasks_assigned,
            'tasks_created': tasks_created,
            'tasks_due_soon': tasks_due_soon,
        }

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to fetch a detailed report for all tasks.
        """
        # Fetch all tasks (or apply filtering as needed)
        tasks = TaskTable.objects.all().select_related('assigned_to','created_by').only(
            'priority',
            'status',
            'due_date',
            'created_at',
            'created_by__username',
            'assigned_to__username',
            
        )

        # Generate the detailed report using multi-threading
        report = self.generate_report(tasks)

        # Return the report as a JSON response
        return Response(report, status=status.HTTP_200_OK)