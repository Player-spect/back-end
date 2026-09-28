from django.db import models
from recursos_humanos.models import Employee


class Project(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('FINISHED', 'Finished'),
    ]

    name = models.CharField(max_length=150)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    budget = models.IntegerField()

    def __str__(self):
        return self.name


class Assignment(models.Model):
    # Relacion Employee a Proyect
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.employee.name} -> {self.project.name}"