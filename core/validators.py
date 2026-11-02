"""Validadores de contraseña y datos de usuario."""

from django.core.exceptions import ValidationError


def validar_username_max(value):
    """El nombre de usuario no puede superar los 32 caracteres."""
    if len(value) > 32:
        raise ValidationError(
            'El nombre de usuario no puede tener más de 32 caracteres.'
        )


class ComplexPasswordValidator:
    """Exige mínimo 8 caracteres, una mayúscula, un número y un carácter especial."""

    def validate(self, password, user=None):
        errores = []
        if len(password) < 8:
            errores.append('La contraseña debe tener al menos 8 caracteres.')
        if not any(c.isupper() for c in password):
            errores.append('La contraseña debe contener al menos una letra mayúscula.')
        if not any(c.isdigit() for c in password):
            errores.append('La contraseña debe contener al menos un número.')
        if not any(not c.isalnum() for c in password):
            errores.append('La contraseña debe contener al menos un carácter especial.')

        if errores:
            raise ValidationError(errores)

    def get_help_text(self):
        return (
            'La contraseña debe tener al menos 8 caracteres e incluir '
            'una mayúscula, un número y un carácter especial.'
        )
