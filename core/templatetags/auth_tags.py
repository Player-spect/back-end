from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def has_group(context, *group_names):
    """Devuelve True si el usuario pertenece a alguno de los grupos dados."""
    user = context.get('user')
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name__in=group_names).exists()
