"""Validadores del dominio de Recursos Humanos."""

from django.core.exceptions import ValidationError


def calcular_dv(cuerpo):
    """Calcula el dígito verificador de un RUT (algoritmo módulo 11)."""
    suma = 0
    factor = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * factor
        factor = 2 if factor == 7 else factor + 1

    resto = suma % 11
    resultado = 11 - resto
    if resultado == 11:
        return '0'
    if resultado == 10:
        return 'K'
    return str(resultado)


def validar_rut(value):
    """Valida un RUT chileno según el algoritmo módulo 11.

    Acepta formatos como ``12.345.678-5``, ``12345678-5`` o ``123456785``.
    """
    if not value:
        raise ValidationError('El RUT es obligatorio.')

    limpio = value.strip().upper().replace('.', '').replace('-', '').replace(' ', '')

    if len(limpio) < 2 or not limpio[:-1].isdigit():
        raise ValidationError('El RUT ingresado no es válido.')

    cuerpo, dv_ingresado = limpio[:-1], limpio[-1]
    dv_esperado = calcular_dv(cuerpo)

    if dv_ingresado != dv_esperado:
        raise ValidationError(
            f'RUT inválido.'
        )

    return value
