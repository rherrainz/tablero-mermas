from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from visor import views as visor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('visor.urls')),
    path("ventas/", include("ventas.urls")),
    path('acerca/', visor.about_panel, name='about_panel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
