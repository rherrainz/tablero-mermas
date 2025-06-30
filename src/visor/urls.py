from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sucursal/<int:codigo>/', views.sucursal_view, name='sucursal'),
    path('cargar/', views.cargar_excel, name='cargar_excel'),
    path('ver_datos_sucs/', views.ver_datos_sucs, name='ver_datos_sucs'),
]
