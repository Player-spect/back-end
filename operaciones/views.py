from django.shortcuts import render
from .models import Project, Assignment

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'operaciones/project_list.html', {'projects': projects})

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'operaciones/assignment_list.html', {'assignments': assignments})