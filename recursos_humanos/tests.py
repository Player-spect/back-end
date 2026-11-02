from django.core.exceptions import ValidationError
from django.test import TestCase

from .forms import EmployeeForm
from .validators import calcular_dv, validar_rut


class RutValidatorTests(TestCase):
    def test_dv_calculation(self):
        self.assertEqual(calcular_dv('12345678'), '5')
        self.assertEqual(calcular_dv('11111111'), '1')

    def test_valid_ruts_accepted(self):
        for rut in ('12.345.678-5', '12345678-5', '123456785', '11.111.111-1'):
            validar_rut(rut)

    def test_invalid_ruts_rejected(self):
        for rut in ('12.345.678-9', '12345678-4', 'abcdefgh-1', '123', ''):
            with self.assertRaises(ValidationError):
                validar_rut(rut)

    def test_form_rejects_invalid_rut(self):
        from .models import Department
        dept = Department.objects.create(name='TI', description='Tecnología')
        form = EmployeeForm(data={
            'rut': '12.345.678-9',
            'name': 'Test',
            'position': 'Dev',
            'email': 'test@test.cl',
            'department': dept.pk,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('rut', form.errors)

    def test_form_accepts_valid_rut(self):
        from .models import Department
        dept = Department.objects.create(name='TI', description='Tecnología')
        form = EmployeeForm(data={
            'rut': '12.345.678-5',
            'name': 'Test',
            'position': 'Dev',
            'email': 'test@test.cl',
            'department': dept.pk,
        })
        self.assertTrue(form.is_valid(), form.errors)
