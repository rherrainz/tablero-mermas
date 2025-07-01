from mermas.models import Sector
from const.sectores import SECTORES  # 👈 Importamos desde el módulo

# Borrar si ya existen
Sector.objects.all().delete()

for codigo, nombre in SECTORES.items():
    Sector.objects.create(codigo=codigo, nombre=nombre)

print("Sectores cargados correctamente.")
