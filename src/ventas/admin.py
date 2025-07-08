from django.contrib import admin
from .models import VentaMensual

@admin.register(VentaMensual)
class VentaMensualAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'sector', 'mes', 'unidades')
    search_fields = ('sucursal__codigo', 'sector__nombre', 'mes')
    list_filter = ('sucursal__zona__region', 'sector')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('sucursal', 'sector')