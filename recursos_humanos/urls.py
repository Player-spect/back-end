from django.urls import path

from . import views

urlpatterns = [
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/crear/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/editar/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/eliminar/', views.employee_delete, name='employee_delete'),
    path('departments/', views.department_list, name='department_list'),
    path('departments/crear/', views.department_create, name='department_create'),
    path('departments/<int:pk>/editar/', views.department_update, name='department_update'),
    path('departments/<int:pk>/eliminar/', views.department_delete, name='department_delete'),
]
