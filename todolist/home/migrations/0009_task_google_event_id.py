# Generated by Django 5.0.2 on 2024-03-25 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_remove_task_remindertime_alter_task_duedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='google_event_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
