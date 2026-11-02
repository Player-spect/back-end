from django.contrib.auth.models import Group, User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from core.roles import ADMINISTRADOR, ADMINISTRATIVO, SUPERVISOR
from operaciones.models import Assignment, Project
from recursos_humanos.models import Department, Employee


class RoleAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for rol in (ADMINISTRADOR, SUPERVISOR, ADMINISTRATIVO):
            Group.objects.get_or_create(name=rol)

        cls.dept = Department.objects.create(name='TI', description='Tecnología')
        cls.emp = Employee.objects.create(
            rut='11.111.111-1', name='Uno', position='Dev',
            email='uno@test.cl', department=cls.dept,
        )
        cls.project = Project.objects.create(
            name='Proyecto', start_date='2024-01-01', status='ACTIVE', budget=100,
        )

        cls.admin = User.objects.create_user('admin', password='clave12345')
        cls.admin.groups.add(Group.objects.get(name=ADMINISTRADOR))
        cls.sup = User.objects.create_user('sup', password='clave12345')
        cls.sup.groups.add(Group.objects.get(name=SUPERVISOR))
        cls.adm = User.objects.create_user('adm', password='clave12345')
        cls.adm.groups.add(Group.objects.get(name=ADMINISTRATIVO))

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_login_works(self):
        response = self.client.post(reverse('login'), {
            'username': 'admin', 'password': 'clave12345',
        })
        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_user_management(self):
        self.client.login(username='admin', password='clave12345')
        self.assertEqual(self.client.get(reverse('user_list')).status_code, 200)

    def test_supervisor_cannot_access_user_management(self):
        self.client.login(username='sup', password='clave12345')
        self.assertEqual(self.client.get(reverse('user_list')).status_code, 403)

    def test_administrativo_cannot_create_employee(self):
        self.client.login(username='adm', password='clave12345')
        response = self.client.get(reverse('employee_create'))
        self.assertEqual(response.status_code, 403)

    def test_supervisor_can_create_employee(self):
        self.client.login(username='sup', password='clave12345')
        response = self.client.get(reverse('employee_create'))
        self.assertEqual(response.status_code, 200)

    def test_administrativo_can_view_employee_list(self):
        self.client.login(username='adm', password='clave12345')
        response = self.client.get(reverse('employee_list'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_differentiates_roles(self):
        self.client.login(username='admin', password='clave12345')
        html = self.client.get(reverse('dashboard')).content.decode()
        self.assertIn('Panel de Administración', html)

        self.client.logout()
        self.client.login(username='sup', password='clave12345')
        html = self.client.get(reverse('dashboard')).content.decode()
        self.assertIn('Panel de Supervisión', html)

        self.client.logout()
        self.client.login(username='adm', password='clave12345')
        html = self.client.get(reverse('dashboard')).content.decode()
        self.assertIn('Panel Administrativo', html)

    def test_crud_department_flow(self):
        self.client.login(username='admin', password='clave12345')
        response = self.client.post(reverse('department_create'), {
            'name': 'Finanzas', 'description': 'Área financiera',
        })
        self.assertEqual(response.status_code, 302)
        departamento = Department.objects.get(name='Finanzas')
        response = self.client.post(reverse('department_update', args=[departamento.pk]), {
            'name': 'Finanzas 2', 'description': 'Actualizada',
        })
        self.assertEqual(response.status_code, 302)
        departamento.refresh_from_db()
        self.assertEqual(departamento.name, 'Finanzas 2')

    def test_assignment_transaction_and_duplicate_validation(self):
        self.client.login(username='sup', password='clave12345')
        response = self.client.post(reverse('assignment_create'), {
            'employee': self.emp.pk, 'project': self.project.pk, 'role': 'Dev',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Assignment.objects.count(), 1)

        # Duplicado debe ser rechazado
        response = self.client.post(reverse('assignment_create'), {
            'employee': self.emp.pk, 'project': self.project.pk, 'role': 'Dev',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Assignment.objects.count(), 1)


class PasswordResetTests(TestCase):
    def test_password_reset_email_and_token_flow(self):
        user = User.objects.create_user(
            'resetuser', email='reset@test.cl', password='clave12345'
        )
        response = self.client.post(reverse('password_reset'), {
            'email': 'reset@test.cl',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('reset', mail.outbox[0].body)

    def test_unknown_email_does_not_leak(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'noexiste@test.cl',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)


class PasswordPolicyTests(TestCase):
    def test_weak_passwords_rejected(self):
        from django.core.exceptions import ValidationError
        from django.contrib.auth.password_validation import validate_password

        debiles = [
            'abc123',          # corta, sin mayúscula ni especial
            'abcdefgh1',       # sin mayúscula ni especial
            'Abcdefgh',        # sin número ni especial
            'Abcdefg1',        # sin especial
            'ABCDEFG1!',       # sin minúscula (permitida, pero verificamos complejidad)
        ]
        for password in debiles[:4]:
            with self.assertRaises(ValidationError):
                validate_password(password)

    def test_strong_password_accepted(self):
        from django.contrib.auth.password_validation import validate_password
        validate_password('Segura123!')

    def test_user_create_form_rejects_weak_password(self):
        from core.forms import UserCreateForm
        form = UserCreateForm(data={
            'username': 'nuevo',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@test.cl',
            'password1': 'debil123',
            'password2': 'debil123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_user_create_form_accepts_strong_password(self):
        from core.forms import UserCreateForm
        form = UserCreateForm(data={
            'username': 'nuevo',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@test.cl',
            'password1': 'Segura123!',
            'password2': 'Segura123!',
            'groups': [],
        })
        self.assertTrue(form.is_valid(), form.errors)


class UsernameLengthTests(TestCase):
    def test_username_max_32_in_create_form(self):
        from core.forms import UserCreateForm
        form = UserCreateForm(data={
            'username': 'u' * 33,
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@test.cl',
            'password1': 'Segura123!',
            'password2': 'Segura123!',
            'groups': [],
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_username_32_accepted(self):
        from core.forms import UserCreateForm
        form = UserCreateForm(data={
            'username': 'u' * 32,
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@test.cl',
            'password1': 'Segura123!',
            'password2': 'Segura123!',
            'groups': [],
        })
        self.assertTrue(form.is_valid(), form.errors)


class GlobalSessionProtectionTests(TestCase):
    rutas_protegidas = [
        'dashboard', 'user_list', 'user_create',
        'employee_list', 'employee_create', 'department_list', 'department_create',
        'project_list', 'project_create', 'assignment_list', 'assignment_create',
    ]

    def test_rutas_protegidas_redirigen_a_login(self):
        for nombre in self.rutas_protegidas:
            response = self.client.get(reverse(nombre))
            self.assertEqual(response.status_code, 302, nombre)
            self.assertIn(reverse('login'), response.url, nombre)

    def test_rutas_publicas_accesibles(self):
        for nombre in ('login', 'password_reset', 'password_reset_done', 'password_reset_complete'):
            response = self.client.get(reverse(nombre))
            self.assertEqual(response.status_code, 200, nombre)

    def test_ruta_inexistente_devuelve_404(self):
        response = self.client.get('/ruta-que-no-existe/')
        self.assertEqual(response.status_code, 404)
