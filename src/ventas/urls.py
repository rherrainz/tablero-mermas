from django.urls import path
from . import views

urlpatterns = [
    path("ver_ventas/", views.ver_ventas, name="ver_ventas"),
    path("cargar/", views.cargar_ventas, name="cargar_ventas"),
    path("comparar_sucursales/", views.comparar_sucursales, name="comparar_sucursales"), 
]
