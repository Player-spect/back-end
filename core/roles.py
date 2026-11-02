"""Definición central de roles (grupos de Django) del sistema."""

ADMINISTRADOR = 'Administrador'
SUPERVISOR = 'Supervisor'
ADMINISTRATIVO = 'Administrativo'

ROLES = [ADMINISTRADOR, SUPERVISOR, ADMINISTRATIVO]

# Permisos mínimos por rol para los modelos del sistema.
# Formato: "app_label.codename"
PERMISOS_POR_ROL = {
    ADMINISTRADOR: '__all__',
    SUPERVISOR: [
        # Puede ver y modificar información operativa, pero no eliminar.
        'recursos_humanos.view_department',
        'recursos_humanos.view_employee',
        'recursos_humanos.change_employee',
        'operaciones.view_project',
        'operaciones.change_project',
        'operaciones.view_assignment',
        'operaciones.add_assignment',
        'operaciones.change_assignment',
    ],
    ADMINISTRATIVO: [
        # Acceso de solo lectura a la información operativa.
        'recursos_humanos.view_department',
        'recursos_humanos.view_employee',
        'operaciones.view_project',
        'operaciones.view_assignment',
    ],
}
