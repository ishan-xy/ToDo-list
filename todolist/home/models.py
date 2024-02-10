from django.db import models

# Create your models here.
class Task(models.Model):
    task_title = models.CharField(max_length=100)
    task_id = models.AutoField(primary_key=True)
    