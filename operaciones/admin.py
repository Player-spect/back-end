from django.contrib import admin
from .models import Project, Assignment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name', 'status']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    search_fields = ['role', 'employee__name', 'project__name']