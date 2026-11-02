from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core.decorators import role_required
from core.roles import ADMINISTRADOR, SUPERVISOR

from .forms import AssignmentForm, ProjectForm
from .models import Assignment, Project

EDIT_ROLES = (ADMINISTRADOR, SUPERVISOR)


@login_required
def project_list(request):
    projects = Project.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        projects = projects.filter(
            name__icontains=q
        ) | projects.filter(
            status__icontains=q
        )
    projects = projects.distinct().order_by('-start_date')
    return render(request, 'operaciones/project_list.html', {
        'projects': projects,
        'q': q,
    })


@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related('employee', 'project').all()
    q = request.GET.get('q', '').strip()
    if q:
        assignments = assignments.filter(
            role__icontains=q
        ) | assignments.filter(
            employee__name__icontains=q
        ) | assignments.filter(
            project__name__icontains=q
        )
    assignments = assignments.distinct()
    return render(request, 'operaciones/assignment_list.html', {
        'assignments': assignments,
        'q': q,
    })


@role_required(*EDIT_ROLES)
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto creado correctamente.')
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'operaciones/project_form.html', {
        'form': form,
        'titulo': 'Crear proyecto',
    })


@role_required(*EDIT_ROLES)
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proyecto actualizado correctamente.')
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'operaciones/project_form.html', {
        'form': form,
        'titulo': f'Editar proyecto: {project.name}',
    })


@role_required(ADMINISTRADOR)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Proyecto eliminado correctamente.')
        return redirect('project_list')
    return render(request, 'operaciones/project_confirm_delete.html', {
        'project': project,
    })


@role_required(*EDIT_ROLES)
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación registrada correctamente.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'operaciones/assignment_form.html', {
        'form': form,
        'titulo': 'Nueva asignación',
    })


@role_required(*EDIT_ROLES)
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación actualizada correctamente.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'operaciones/assignment_form.html', {
        'form': form,
        'titulo': 'Editar asignación',
    })


@role_required(ADMINISTRADOR)
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Asignación eliminada correctamente.')
        return redirect('assignment_list')
    return render(request, 'operaciones/assignment_confirm_delete.html', {
        'assignment': assignment,
    })
