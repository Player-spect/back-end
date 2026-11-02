from django import forms

from .models import Assignment, Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'start_date', 'status', 'budget']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def clean_budget(self):
        budget = self.cleaned_data['budget']
        if budget is not None and budget < 0:
            raise forms.ValidationError('El presupuesto no puede ser negativo.')
        return budget


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['employee', 'project', 'role']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        employee = cleaned.get('employee')
        project = cleaned.get('project')
        if employee and project:
            existen = Assignment.objects.filter(
                employee=employee, project=project
            )
            if self.instance.pk:
                existen = existen.exclude(pk=self.instance.pk)
            if existen.exists():
                raise forms.ValidationError(
                    'Este empleado ya está asignado a ese proyecto.'
                )
        return cleaned
