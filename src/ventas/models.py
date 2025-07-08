from django.db import models
from visor.models import Sucursal
from mermas.models import Sector

class VentaMensual(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    mes = models.CharField(max_length=6)  # Ej: "202001"
    unidades = models.FloatField()

    class Meta:
        unique_together = ("sucursal", "sector", "mes")
        ordering = ["mes"]
