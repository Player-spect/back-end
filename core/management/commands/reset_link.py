"""Genera y muestra un enlace de restablecimiento de contraseña.

Útil en desarrollo cuando el backend de correo es consola y el enlace
aparece cortado por el formato quoted-printable del email.

Uso:
    python manage.py reset_link <usuario_o_email> [--base-url http://127.0.0.1:8000]
"""

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.management.base import BaseCommand, CommandError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class Command(BaseCommand):
    help = 'Muestra un enlace válido para restablecer la contraseña de un usuario.'

    def add_arguments(self, parser):
        parser.add_argument('identificador', help='Username o email del usuario.')
        parser.add_argument(
            '--base-url',
            default='http://127.0.0.1:8000',
            help='URL base del sitio (por defecto http://127.0.0.1:8000).',
        )

    def handle(self, *args, **options):
        identificador = options['identificador']
        base_url = options['base_url'].rstrip('/')

        user = User.objects.filter(username=identificador).first()
        if user is None:
            user = User.objects.filter(email__iexact=identificador).first()
        if user is None:
            raise CommandError(f'No existe un usuario con "{identificador}".')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        enlace = f'{base_url}/password-reset/{uid}/{token}/'

        self.stdout.write(self.style.SUCCESS(f'Usuario: {user.username}'))
        self.stdout.write('Enlace de restablecimiento (válido una vez):')
        self.stdout.write(self.style.WARNING(enlace))
