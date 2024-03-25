from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template import loader
from datetime import date, datetime, timedelta
from itertools import groupby
from django.utils import timezone
from .googleCalender import create_event, update_event, delete_event
from .models import Task

def index(request):
    tasks = Task.objects.all().order_by('dueDate')
    tasks_by_date = {date: list(items) for date, items in groupby(tasks, key=lambda task: timezone.localtime(task.dueDate).date())}
    context = {
        'tasks': tasks,
        'today_date': datetime.now(),
        'tasks_by_date': tasks_by_date,
    }
    return render(request, 'home/index.html', context)

def add_task(request):
    if request.method == 'POST':
        title = request.POST['task']
        desc = request.POST['description']
        dateTime = request.POST['duedate']
        
        add_to_google_calendar = request.POST.get('addToGoogleCalendar')
        
        if title == "":
            return redirect('index')

        # Convert dateTime from string to datetime object
        dateTime = timezone.make_aware(datetime.strptime(dateTime, '%Y-%m-%dT%H:%M'))
        task = Task(task_title=title, dueDate=dateTime, description=desc)

        # Convert to string in the desired format
        formatted_date = timezone.localtime(dateTime).isoformat()
        
        if(add_to_google_calendar == 'on'):
            google_event_id = create_event(title, desc, formatted_date)
            task.google_event_id = google_event_id

        task.save()        

    return redirect('index')
    
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(task_id=id)
        if task.google_event_id:
            delete_event(task.google_event_id)
        task.delete()
    return redirect('index')
    

def edit_task(request, id):
    if request.method == 'POST':
        new_title = request.POST['newtask']
        if new_title == "":
            return redirect('index')
        
        task = Task.objects.get(task_id=id)
        task.task_title = new_title
        dateTime = task.dueDate
        formatted_date = timezone.localtime(dateTime).isoformat()
        if task.google_event_id:
            
            update_event(task.google_event_id, new_title, task.description, formatted_date)
        task.save()
    return redirect('index')