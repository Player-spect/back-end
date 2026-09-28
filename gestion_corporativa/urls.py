from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hr/', include('recursos_humanos.urls')),
    path('operations/', include('operaciones.urls')),
    path('', RedirectView.as_view(url='/hr/employees/', permanent=False)),
]
