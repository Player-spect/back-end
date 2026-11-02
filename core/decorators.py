"""Decoradores de autorización basados en grupos/roles de Django."""

from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .roles import ROLES


def get_roles(user):
    """Devuelve el conjunto de nombres de grupos del usuario."""
    if not user.is_authenticated:
        return set()
    return set(user.groups.values_list('name', flat=True))


def role_required(*roles):
    """Permite el acceso solo a usuarios de los grupos indicados.

    Los superusuarios siempre tienen acceso.
    """
    roles_permitidos = set(roles) if roles else set(ROLES)

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            if get_roles(request.user) & roles_permitidos:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped
    return decorator
