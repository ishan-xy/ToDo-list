from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from datetime import date, datetime, timedelta
from django.db.models import Prefetch
from itertools import groupby
from operator import attrgetter
from .googleCalender import create_event, update_event, delete_event
from .models import Task

def index(request):
    template = loader.get_template('home/index.html')
    tasks = Task.objects.all().order_by('dueDate')
    tasks_by_date = {date: list(items) for date, items in groupby(tasks, key=lambda task: task.dueDate.date())}
    context = {
        'tasks': tasks,
        'today_date': datetime.now(),
        'tasks_by_date': tasks_by_date,
    }
    return HttpResponse(template.render(context, request))

def refresh(request):
    return redirect(reverse('index'))

def add_task(request):
    if request.method == 'POST':
        title = request.POST['task']
        desc = request.POST['description']
        dateTime = request.POST['duedate']
        
        add_to_google_calendar = request.POST.get('addToGoogleCalendar')
        
        if title == "":
            return redirect(reverse('refresh'))

        # Convert dateTime from string to datetime object
        dateTime = datetime.strptime(dateTime, '%Y-%m-%dT%H:%M')
        task = Task(task_title=title, dueDate=dateTime, description=desc)
        # Convert to IST (UTC+5:30)
        # IST_offset = timedelta(hours=5, minutes=30)
        # dateTime = dateTime + IST_offset

        

        # Convert to string in the desired format
        formatted_date = dateTime.strftime('%Y-%m-%dT%H:%M:%S')
        
        if(add_to_google_calendar == 'on'):
            google_event_id = create_event(title, desc, formatted_date)
            task.google_event_id = google_event_id

        task.save()        

    return redirect(reverse('refresh'))
    
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(task_id=id)
        print(f"Task's google_event_id: {task.google_event_id}")
        if task.google_event_id:
            delete_event(task.google_event_id)
        task.delete()
    return redirect(reverse('refresh'))

def edit_task(request, id):
    if request.method == 'POST':
        new_title = request.POST['newtask']
        if new_title == "":
            return redirect(reverse('refresh'))
        
        task = Task.objects.get(task_id=id)
        task.task_title = new_title
        if task.google_event_id:
            formatted_date = task.dueDate.strftime('%Y-%m-%dT%H:%M:%S')
            update_event(task.google_event_id, new_title, task.description, formatted_date)
        task.save()
    return redirect(reverse('refresh'))

def set_reminder(request, id):
    if request.method == 'POST':
        time = request.POST['remindertime']
        task = Task.objects.get(task_id=id)
        task.reminderTime = time
        task.save()
    return redirect(reverse('refresh'))