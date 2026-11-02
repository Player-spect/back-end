import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_corporativa.settings')
django.setup()

from recursos_humanos.models import Employee, Department
from operaciones.models import Project, Assignment  # Se importan los nuevos modelos

with open('data.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# 1. Crear Departamentos
for item in datos['departamentos']:
    Department.objects.update_or_create(
        name=item['nombre'],
        defaults={'description': item['descripcion']}
    )
    print(f"Departamento procesado: {item['nombre']}")

# 2. Crear Empleados
for item in datos['empleados']:
    departamento_obj = Department.objects.get(name=item['departamento'])
    
    Employee.objects.update_or_create(
        rut=item['rut'], 
        defaults={
            'name': item['nombre'],
            'position': item['cargo'],
            'email': item['email'],
            'department': departamento_obj
        }
    )
    print(f"Empleado procesado: {item['nombre']}")

# 3. Crear Proyectos
for item in datos['proyectos']:
    Project.objects.update_or_create(
        name=item['nombre'],
        defaults={
            'start_date': item['fecha_inicio'],
            'status': item['estado'],
            'budget': item['presupuesto']
        }
    )
    print(f"Proyecto procesado: {item['nombre']}")

# 4. Crear Asignaciones (relacionando Empleado y Proyecto)
for item in datos['asignaciones']:
    empleado_obj = Employee.objects.get(rut=item['empleado_rut'])
    proyecto_obj = Project.objects.get(name=item['proyecto_nombre'])
    
    Assignment.objects.update_or_create(
        employee=empleado_obj,
        project=proyecto_obj,
        defaults={'role': item['rol']}
    )
    print(f"Asignación creada: {empleado_obj.name} -> {proyecto_obj.name}")

print("\n¡Datos importados con éxito a la base de datos!")
