from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from datetime import date, datetime
from .googleCalender import create_event
from .models import Task
# Create your views here.
def index(request):
    template = loader.get_template('home/index.html')
    all_tasks = Task.objects.all().values()
    context = {
        'tasks': all_tasks,
        'today_date': date.today()
        
    }
    return HttpResponse(template.render(context, request))
    

def refresh(request):
    return redirect(reverse('index'))

def add_task(request):
    if request.method == 'POST':
        title = request.POST['task']
        desc = request.POST['description']
        date = request.POST['duedate']
        add_to_google_calendar = request.POST.get('addToGoogleCalendar')
        
        if title == "":
            return redirect(reverse('refresh'))
        task = Task(task_title=title, dueDate=date, description=desc)
        
        task.save()        
        
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%dT%H:%M:%S+05:30')
        
        if(add_to_google_calendar == 'on'):
            create_event(title, desc, date) 
        
    return redirect(reverse('refresh'))
    
def delete_task(request, id):
    if request.method == 'POST':
        id = Task.objects.filter(task_id=id)
        id.delete()
    return redirect(reverse('refresh'))

def edit_task(request, id):
    if request.method == 'POST':
        requestValue = request.POST['newtask']
        if requestValue == "":
            return redirect(reverse('refresh'))
        
        id = Task.objects.filter(task_id=id)
        id.update(task_title=requestValue)
    return redirect(reverse('refresh'))

# def due_date(request, id):
#     if request.method == 'POST':
#         # id = request.POST['id']
#         date = request.POST['duedate']
#         task = Task.objects.filter(task_id=id)
#         task.update(dueDate=date)
#     return redirect(reverse('refresh'))

def set_reminder(request, id):
    if request.method == 'POST':
        # id = request.POST['id']
        time = request.POST['remindertime']
        task = Task.objects.filter(task_id=id)
        task.update(reminderTime=time)
    return redirect(reverse('refresh'))