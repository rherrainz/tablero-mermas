from django.contrib import admin
from .models import Sucursal, PlanMerma, Zona, Region

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'zona', 'get_region']
    search_fields = ['codigo', 'nombre']
    list_filter = ['zona__region']

    @admin.display(description='Región')
    def get_region(self, obj):
        return obj.zona.region.nombre if obj.zona and obj.zona.region else '-'

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'region']
    search_fields = ['codigo', 'nombre']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(PlanMerma)
class PlanMermaAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'sector', 'porcentaje')
    search_fields = ('sucursal', 'sector')
    list_filter = ('sector',)

