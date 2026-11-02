"""Vistas de autenticación, dashboards y gestión de usuarios."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from operaciones.models import Assignment, Project
from recursos_humanos.models import Department, Employee

from .decorators import get_roles, role_required
from .forms import UserCreateForm, UserUpdateForm
from .roles import ADMINISTRADOR, ADMINISTRATIVO, SUPERVISOR


@login_required
def dashboard(request):
    """Dashboard diferenciado según el rol del usuario."""
    roles = get_roles(request.user)
    if request.user.is_superuser:
        roles.add(ADMINISTRADOR)

    es_admin = ADMINISTRADOR in roles
    es_supervisor = SUPERVISOR in roles
    es_administrativo = ADMINISTRATIVO in roles

    context = {
        'roles': roles,
        'es_admin': es_admin,
        'es_supervisor': es_supervisor,
        'es_administrativo': es_administrativo,
    }

    if es_admin:
        context.update({
            'total_employees': Employee.objects.count(),
            'total_departments': Department.objects.count(),
            'total_projects': Project.objects.count(),
            'total_assignments': Assignment.objects.count(),
            'total_users': User.objects.count(),
            'proyectos_por_estado': Project.objects.values('status').annotate(
                total=Count('id')
            ),
            'ultimos_proyectos': Project.objects.order_by('-start_date')[:5],
        })
    elif es_supervisor:
        context.update({
            'total_projects': Project.objects.count(),
            'total_assignments': Assignment.objects.count(),
            'proyectos_activos': Project.objects.filter(status='ACTIVE'),
            'asignaciones_recientes': Assignment.objects.select_related(
                'employee', 'project'
            )[:5],
        })
    elif es_administrativo:
        context.update({
            'total_employees': Employee.objects.count(),
            'total_departments': Department.objects.count(),
            'empleados': Employee.objects.select_related('department')[:5],
        })

    return render(request, 'core/dashboard.html', context)


# ----------------------------- Gestión de usuarios -----------------------------

@role_required(ADMINISTRADOR)
def user_list(request):
    users = User.objects.prefetch_related('groups').order_by('username')
    return render(request, 'core/user_list.html', {'users': users})


@role_required(ADMINISTRADOR)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'core/user_form.html', {'form': form, 'titulo': 'Crear usuario'})


@role_required(ADMINISTRADOR)
def user_update(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=user_obj)
    return render(request, 'core/user_form.html', {
        'form': form,
        'titulo': f'Editar usuario: {user_obj.username}',
    })


@role_required(ADMINISTRADOR)
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if user_obj == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('user_list')
    if request.method == 'POST':
        user_obj.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('user_list')
    return render(request, 'core/user_confirm_delete.html', {'user_obj': user_obj})


# ----------------------------- Páginas de error -----------------------------

def error_404(request, exception):
    return render(request, '404.html', status=404)


def error_403(request, exception):
    return render(request, '403.html', status=403)


def error_500(request):
    return render(request, '500.html', status=500)
