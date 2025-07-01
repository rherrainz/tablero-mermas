from django.db import models

class Sector(models.Model):
    codigo = models.CharField(max_length=10,unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class MermaSucursal(models.Model):
    sucursal = models.ForeignKey("visor.Sucursal", on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    cantidad_mermas = models.PositiveIntegerField()
    monto_mermas = models.DecimalField(max_digits=12, decimal_places=2)
    unidades_vendidas = models.PositiveIntegerField()
    venta_sin_iva = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_mermas_ventas = models.DecimalField(max_digits=5, decimal_places=2)
    monto_ajuste = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_ajuste_sobre_merma = models.DecimalField(max_digits=5, decimal_places=2)
    monto_merma_no_ajustada = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_no_ajustada_sobre_merma = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField()


class MermaZona(models.Model):
    zona = models.ForeignKey("visor.Zona", on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    cantidad_mermas = models.PositiveIntegerField()
    monto_mermas = models.DecimalField(max_digits=12, decimal_places=2)
    unidades_vendidas = models.PositiveIntegerField()
    venta_sin_iva = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_mermas_ventas = models.DecimalField(max_digits=5, decimal_places=2)
    monto_ajuste = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_ajuste_sobre_merma = models.DecimalField(max_digits=5, decimal_places=2)
    monto_merma_no_ajustada = models.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_no_ajustada_sobre_merma = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField()
