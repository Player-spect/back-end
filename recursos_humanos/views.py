from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from core.roles import ADMINISTRADOR, SUPERVISOR

from .forms import DepartmentForm, EmployeeForm
from .models import Department, Employee

EDIT_ROLES = (ADMINISTRADOR, SUPERVISOR)


@login_required
def employee_list(request):
    employees = Employee.objects.select_related('department').all()
    q = request.GET.get('q', '').strip()
    if q:
        employees = employees.filter(
            rut__icontains=q
        ) | employees.filter(
            name__icontains=q
        ) | employees.filter(
            position__icontains=q
        ) | employees.filter(
            email__icontains=q
        )
    employees = employees.distinct().order_by('name')
    return render(request, 'recursos_humanos/employee_list.html', {
        'employees': employees,
        'q': q,
    })


@login_required
def department_list(request):
    departments = Department.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        departments = departments.filter(
            name__icontains=q
        ) | departments.filter(
            description__icontains=q
        )
    departments = departments.distinct().order_by('name')
    return render(request, 'recursos_humanos/department_list.html', {
        'departments': departments,
        'q': q,
    })


@role_required(*EDIT_ROLES)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado correctamente.')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'recursos_humanos/employee_form.html', {
        'form': form,
        'titulo': 'Crear empleado',
    })


@role_required(*EDIT_ROLES)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'recursos_humanos/employee_form.html', {
        'form': form,
        'titulo': f'Editar empleado: {employee.name}',
    })


@role_required(ADMINISTRADOR)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('employee_list')
    return render(request, 'recursos_humanos/employee_confirm_delete.html', {
        'employee': employee,
    })


@role_required(*EDIT_ROLES)
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado correctamente.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'recursos_humanos/department_form.html', {
        'form': form,
        'titulo': 'Crear departamento',
    })


@role_required(*EDIT_ROLES)
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado correctamente.')
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'recursos_humanos/department_form.html', {
        'form': form,
        'titulo': f'Editar departamento: {department.name}',
    })


@role_required(ADMINISTRADOR)
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Departamento eliminado correctamente.')
        return redirect('department_list')
    return render(request, 'recursos_humanos/department_confirm_delete.html', {
        'department': department,
    })
