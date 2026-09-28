from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    # Relacion de uno a muchos
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.position}"