from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_not_required
from django.urls import path

from . import views

# Rutas públicas: no requieren sesión iniciada.
# El resto queda protegido globalmente por LoginRequiredMiddleware.
urlpatterns = [
    path(
        'login/',
        login_not_required(
            auth_views.LoginView.as_view(template_name='core/login.html')
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Recuperación de contraseña (token seguro generado por Django)
    path(
        'password-reset/',
        login_not_required(
            auth_views.PasswordResetView.as_view(
                template_name='core/password_reset_form.html',
                email_template_name='core/password_reset_email.html',
                subject_template_name='core/password_reset_subject.txt',
                success_url='/password-reset/enviado/',
            )
        ),
        name='password_reset',
    ),
    path(
        'password-reset/enviado/',
        login_not_required(
            auth_views.PasswordResetDoneView.as_view(
                template_name='core/password_reset_done.html',
            )
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        login_not_required(
            auth_views.PasswordResetConfirmView.as_view(
                template_name='core/password_reset_confirm.html',
                success_url='/password-reset/completado/',
            )
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/completado/',
        login_not_required(
            auth_views.PasswordResetCompleteView.as_view(
                template_name='core/password_reset_complete.html',
            )
        ),
        name='password_reset_complete',
    ),

    path('', views.dashboard, name='dashboard'),
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/crear/', views.user_create, name='user_create'),
    path('usuarios/<int:pk>/editar/', views.user_update, name='user_update'),
    path('usuarios/<int:pk>/eliminar/', views.user_delete, name='user_delete'),
]
