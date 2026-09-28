from django.shortcuts import render
from .models import Employee, Department

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'recursos_humanos/employee_list.html', {'employees': employees})

def department_list(request):
    departments = Department.objects.all()
    return render(request, 'recursos_humanos/department_list.html', {'departments': departments})