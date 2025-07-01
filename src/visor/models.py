from django.db import models

class Region(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Zona(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Sucursal(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    zona = models.ForeignKey(Zona, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class PlanMerma(models.Model):
    sucursal = models.CharField(max_length=10)
    sector = models.CharField(max_length=10)
    porcentaje = models.FloatField()  # guardamos el valor como -0.88, -1.50, etc.

    class Meta:
        unique_together = ("sucursal", "sector")

    def __str__(self):
        return f"{self.sucursal} - {self.sector}: {self.porcentaje}%"