"""Crea/actualiza los grupos y permisos del sistema.

Uso:
    python manage.py setup_roles
"""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from core.roles import ADMINISTRADOR, PERMISOS_POR_ROL, ROLES


class Command(BaseCommand):
    help = 'Crea los grupos Administrador, Supervisor y Administrativo con sus permisos.'

    def handle(self, *args, **options):
        for rol in ROLES:
            group, created = Group.objects.get_or_create(name=rol)
            permisos = PERMISOS_POR_ROL.get(rol, [])

            if permisos == '__all__':
                group.permissions.set(Permission.objects.all())
            else:
                codenames = [p.split('.', 1)[1] for p in permisos if '.' in p]
                group.permissions.set(
                    Permission.objects.filter(codename__in=codenames)
                )

            estado = 'creado' if created else 'actualizado'
            self.stdout.write(
                self.style.SUCCESS(f'Grupo {rol} {estado} con {group.permissions.count()} permisos.')
            )
