from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('assignments/', views.assignment_list, name='assignment_list'),
]