from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'dueDate', 'description']
        widgets = {
            'dueDate': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }