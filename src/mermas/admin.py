from django.contrib import admin
from mermas.models import Sector, MermaSucursal, MermaZona

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre")
    search_fields = ("codigo", "nombre")

@admin.register(MermaSucursal)
class MermaSucursalAdmin(admin.ModelAdmin):
    list_display = ("sucursal", "sector", "monto_mermas", "monto_venta", "porcentaje_mermas_sobre_venta")
    search_fields = ("sucursal__nombre", "sector__nombre")

@admin.register(MermaZona)
class MermaZonaAdmin(admin.ModelAdmin):
    list_display = ("zona", "sector", "monto_mermas", "monto_venta", "porcentaje_mermas_sobre_venta")
    search_fields = ("zona__nombre", "sector__nombre")
