
import django_filters
from .models import TaskTable

class TaskFilter(django_filters.FilterSet):
    # Filter for the priority, status, and due_date fields
    priority = django_filters.ChoiceFilter(choices=TaskTable.PRIORITY_CHOICE)
    status = django_filters.ChoiceFilter(choices=TaskTable.STATUS_CHOICE)
    
    # Use DateFilter directly with the lookup_expr to handle different types of date filtering
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact')  # exact match
    due_date_gte = django_filters.DateFilter(field_name='due_date', lookup_expr='gte')  # greater than or equal to
    due_date_gt = django_filters.DateFilter(field_name='due_date', lookup_expr='gt')  # greater than
    due_date_lte = django_filters.DateFilter(field_name='due_date', lookup_expr='lte')  # less than or equal to
    due_date_lt = django_filters.DateFilter(field_name='due_date', lookup_expr='lt')  # less than

    class Meta:
        model = TaskTable
        fields = ['priority', 'status', 'due_date', 
                  'due_date_gte', 'due_date_gt', 
                  'due_date_lte', 'due_date_lt']
        
        

