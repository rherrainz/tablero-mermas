from django.contrib import admin
from .models import Sucursal

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('suc_id', 'nombre', 'zona', 'region')
    search_fields = ('nombre', 'zona', 'region')
