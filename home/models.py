from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    dueDate = models.DateTimeField(null=True, blank=True)
    google_event_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.task_title

     