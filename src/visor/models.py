from django.db import models

class Sucursal(models.Model):
    suc_id = models.PositiveIntegerField(primary_key=True)  # Código de 3 dígitos
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.suc_id} - {self.nombre}"

class PlanMerma(models.Model):
    sucursal = models.CharField(max_length=10)
    sector = models.CharField(max_length=10)
    porcentaje = models.FloatField()  # guardamos el valor como -0.88, -1.50, etc.

    class Meta:
        unique_together = ("sucursal", "sector")

    def __str__(self):
        return f"{self.sucursal} - {self.sector}: {self.porcentaje}%"