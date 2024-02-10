from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('add_task/', views.add_task, name='add_task'),
    path('refresh/', views.refresh, name='refresh'),
    path('delete_task/<int:id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:id>/', views.edit_task, name='edit_task'),
]