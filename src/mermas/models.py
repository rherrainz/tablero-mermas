from django.db import models
from visor.models import Zona, Sucursal

class Sector(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class MermaSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    cantidad_mermas = models.FloatField()
    monto_mermas = models.FloatField()
    unidades_vendidas = models.IntegerField()
    monto_venta = models.FloatField()
    porcentaje_mermas_sobre_venta = models.FloatField()
    monto_ajuste = models.FloatField()
    porcentaje_ajuste_sobre_merma = models.FloatField()
    monto_mermas_no_ajustadas = models.FloatField()
    porcentaje_mermas_no_ajustadas = models.FloatField()

    def __str__(self):
        return f"{self.sucursal} - {self.sector}"

class MermaZona(models.Model):
    zona = models.ForeignKey(Zona, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    cantidad_mermas = models.FloatField()
    monto_mermas = models.FloatField()
    unidades_vendidas = models.IntegerField()
    monto_venta = models.FloatField()
    porcentaje_mermas_sobre_venta = models.FloatField()
    monto_ajuste = models.FloatField()
    porcentaje_ajuste_sobre_merma = models.FloatField()
    monto_mermas_no_ajustadas = models.FloatField()
    porcentaje_mermas_no_ajustadas = models.FloatField()

    def __str__(self):
        return f"{self.zona} - {self.sector}"

