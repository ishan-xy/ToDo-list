from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(null=True, blank=True)
    reminderTime = models.DateTimeField(null=True, blank=True)
    dueDate = models.DateField(null=True, blank=True)

    