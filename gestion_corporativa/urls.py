from django.urls import include, path

urlpatterns = [
    # Django Admin deshabilitado: la operación del sistema se realiza
    # exclusivamente mediante las vistas y plantillas propias.
    path('hr/', include('recursos_humanos.urls')),
    path('operations/', include('operaciones.urls')),
    path('', include('core.urls')),
]

# Páginas de error propias (se usan cuando DEBUG=False).
handler403 = 'core.views.error_403'
handler404 = 'core.views.error_404'
handler500 = 'core.views.error_500'
