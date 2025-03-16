from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
from .models import TaskTable
from django.conf import settings

# A function to generate message based on the condition
def generate_task_message(task, condition):
    """ Return the message based on the condition """
    if condition == 'task_assigned':
        return f"Task '{task.title}' has been assigned to you. Please take action!"
    elif condition == 'task_due':
        return f"Your task '{task.title}' is due soon. Please complete it within the next 24 hours!"
    return "You have a task that requires your attention."

# A function to create the dynamic context for the email
def create_email_context(task, condition):
    """ Create the context for the email template """
    # Prepare the dynamic message for the task
    task_message = generate_task_message(task, condition)
    
    # Create the context dictionary for the email template
    context = {
        'subject': f"Task Notification: {task.title}",
        'title': task.title,
        'created_by_name': task.created_by.username,
        'assigned_to_name': task.assigned_to.username if task.assigned_to else 'Unassigned',
        'created_at': task.created_at.strftime('%B %d, %Y'),
        'due_date': task.due_date.strftime('%B %d, %Y'),
        'description': task.description,
        'task_message': task_message,  # Dynamic message based on the condition
    }

    return context

# A function to send email with HTML template
def send_task_email(subject, task, recipient_email, condition):
    """ Send an email with dynamic content """
    # Create the context for the email
    context = create_email_context(task, condition)
    
    # Render the HTML content using the context
    html_message = render_to_string('task/task_email.html', context)

    # Send the email using the EmailMessage class for HTML content
    email = EmailMessage(
        subject,
        html_message,
        settings.DEFAULT_FROM_EMAIL,  # From email (configured in settings)
        [recipient_email],  # Recipient email
    )

    email.content_subtype = 'html'  # Set the content type to HTML
    email.send(fail_silently=False)  # Send the email and fail if there is an issue

# Send notification when a task is assigned or nearing deadline
@shared_task
def send_due_task_notifications():
    """ Task for sending email when a task is nearing its deadline """
    now = timezone.now()
    tasks_due_soon = TaskTable.objects.filter(
        due_date__lte=now + timedelta(days=1),
        due_date__gt=now,
        status='PENDING'
    )
    
    for task in tasks_due_soon:
        if task.assigned_to:
            send_task_email(
                f"Task Deadline Approaching: {task.title}",
                task,
                task.assigned_to.email,
                condition='task_due'  # Specify the condition for this email
            )




# Task triggered when a task is assigned
@shared_task
def send_task_assigned_email(task_id):
    """ Task for sending email when a task is assigned """
    task = TaskTable.objects.get(id=task_id)
    if task.assigned_to:
        send_task_email(
            f"Task Assigned: {task.title}",
            task,
            task.assigned_to.email,
            condition='task_assigned'  # Specify the condition for this email
        )
