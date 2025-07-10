from django.contrib import admin

from mermas.models import Sector, MermaSucursal, MermaZona


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre")
    search_fields = ("codigo", "nombre")


@admin.register(MermaSucursal)
class MermaSucursalAdmin(admin.ModelAdmin):
    list_display = ("sucursal", "sector", "mes", "valor")
    search_fields = ("sucursal__nombre", "sector__nombre", "mes")


@admin.register(MermaZona)
class MermaZonaAdmin(admin.ModelAdmin):
    list_display = ("zona", "sector", "mes", "valor")
    search_fields = ("zona__nombre", "sector__nombre", "mes")