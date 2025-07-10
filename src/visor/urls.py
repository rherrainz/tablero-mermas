from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index_tablero/', views.index_tablero, name='index_tablero'),
    path('sucursal/<int:codigo>/', views.sucursal_view, name='sucursal'),
    path('cargar/', views.cargar_excel, name='cargar_excel'),
    path('ver_datos_sucs/', views.ver_datos_sucs, name='ver_datos_sucs'),
    path('tablero/<str:codigo>/', views.tablero_sucursal, name='tablero_sucursal'),
    path("tablero/pdf/<str:codigo>/", views.tablero_pdf, name="tablero_pdf"),
    path("comparar-sucursales/", views.comparar_mermas_sucursales, name="comparar_mermas_sucursales"),
    path("comparar-zonas/", views.comparar_mermas_zonas, name="comparar_mermas_zonas"),
]
