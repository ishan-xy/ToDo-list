from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from .models import Task
# Create your views here.
def index(request):
    # all_tasks = Task.objects.values_list('task_title', flat=True)
    # all_taskIDs = Task.objects.values_list('task_id', flat=True)
    # return render(request, 'home/index.html', {'tasks': all_tasks}, {'taskID': all_taskIDs})
    template = loader.get_template('home/index.html')
    all_tasks = Task.objects.all().values()
    context = {
        'tasks': all_tasks
    }
    return HttpResponse(template.render(context, request))
    

def refresh(request):
    return redirect(reverse('index'))

def add_task(request):
    if request.method == 'POST':
        title = request.POST['task']
        if title == "":
            return redirect(reverse('refresh'))
        task = Task(task_title=title)
        task.save()        
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