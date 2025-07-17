from mermas.models import Sector
from const.sectores import SECTORES

for codigo, nombre in SECTORES.items():
    Sector.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre})

print("✅ Sectores cargados (sin borrar los existentes)")
