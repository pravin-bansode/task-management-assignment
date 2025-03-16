from django.db import models

from django.contrib.auth.models import User

# Create your models here.



class TaskTable(models.Model):
    PRIORITY_CHOICE =[
         ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    STATUS_CHOICE  = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('ARCHIVED', 'Archived'),
    ]
   
    
    title= models.CharField(max_length=300)
    description = models.TextField()
    priority = models.CharField(
        max_length=15,
        choices=PRIORITY_CHOICE,  
         default='LOW'  
         # Set the default to 'L' for Low
    )    
    
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,
                                  related_name='created_tasks'
                                  )
    
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  # Set to NULL when the user is deleted
        null=True,  # Allow the field to be NULL
        blank=True  # Allow the field to be blank in forms
        , related_name='assigned_tasks'
        
    )
    
    status = models.CharField(
        max_length=15,
       
        choices=STATUS_CHOICE,  
         default='IN_PROGRESS'  
         # Set the default to 'L' for Low
    )    
    
    due_date = models.DateField()  # Store the due date of the task
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on task creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update on task modification


