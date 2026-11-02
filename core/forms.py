"""Formularios de gestión de usuarios y grupos."""

from django import forms
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password

from .roles import ROLES
from .validators import validar_username_max


class UserCreateForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuario',
        max_length=32,
        validators=[validar_username_max],
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        help_text='Mínimo 8 caracteres.',
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput,
    )
    groups = forms.ModelMultipleChoiceField(
        label='Roles',
        queryset=Group.objects.filter(name__in=ROLES),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password:
            usuario = User(
                username=self.cleaned_data.get('username', ''),
                email=self.cleaned_data.get('email', ''),
                first_name=self.cleaned_data.get('first_name', ''),
                last_name=self.cleaned_data.get('last_name', ''),
            )
            validate_password(password, user=usuario)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            user.groups.set(self.cleaned_data.get('groups', []))
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='Usuario',
        max_length=32,
        validators=[validar_username_max],
    )
    groups = forms.ModelMultipleChoiceField(
        label='Roles',
        queryset=Group.objects.filter(name__in=ROLES),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set(self.cleaned_data.get('groups', []))
        return user
