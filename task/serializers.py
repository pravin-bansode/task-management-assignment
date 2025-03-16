from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TaskTable

class TaskSerializer(serializers.ModelSerializer):
    created_by=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),required=False,)
    # priority = serializers.CharField(source='get_priority',read_only=True)
    # status = serializers.CharField(source='get_status',read_only=True)
    
    
    class Meta:
        model= TaskTable
        fields="__all__"
        
    
    
    def create(self, validated_data):
        # Automatically set the `created_by` to the current authenticated user
        user = self.context['request'].user  # Get the logged-in user from the request context
        validated_data['created_by'] = user  # Set the `created_by` field to the current user
        return TaskTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # The `created_by` field should not be updated (it remains the same)
        validated_data.pop('created_by', None)
        return super().update(instance, validated_data)
    
    