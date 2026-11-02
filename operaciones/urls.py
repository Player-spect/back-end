from django.urls import path

from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/crear/', views.project_create, name='project_create'),
    path('projects/<int:pk>/editar/', views.project_update, name='project_update'),
    path('projects/<int:pk>/eliminar/', views.project_delete, name='project_delete'),
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/crear/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/editar/', views.assignment_update, name='assignment_update'),
    path('assignments/<int:pk>/eliminar/', views.assignment_delete, name='assignment_delete'),
]
