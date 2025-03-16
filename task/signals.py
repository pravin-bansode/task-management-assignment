from django.db.models.signals import post_save,post_delete

from django.dispatch import receiver
from django.core.cache import cache
from .models import TaskTable


TASK_CACHE_KEY='task_list'

@receiver([post_save,post_delete],sender = TaskTable)
def task_cache_validate(sender, instance,created,**kwargs):

    cache.delete(TASK_CACHE_KEY)