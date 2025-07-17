import os
import django
import pandas as pd
from django.conf import settings
from pathlib import Path
from visor.models import Region, Zona, Sucursal


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tablero.settings')  # <--- nombre del proyecto, ajustalo si es distinto
django.setup()


archivo = Path(settings.BASE_DIR) / 'media' / 'estructura_local.xlsx'
if not archivo.exists():
    raise FileNotFoundError(f"Archivo no encontrado: {archivo}")

# Cargar hojas
xls = pd.ExcelFile(archivo)
df_regiones = pd.read_excel(xls, 'regiones')
df_zonas = pd.read_excel(xls, 'zonas')
df_sucs = pd.read_excel(xls, 'sucursales')

# Limpiar tablas para evitar duplicados (opcional, si estás seguro)
Sucursal.objects.all().delete()
Zona.objects.all().delete()
Region.objects.all().delete()

# Crear regiones
regiones = {}
for _, fila in df_regiones.iterrows():
    nombre = str(fila['nombre']).strip()
    codigo = int(fila['codigo'])  # <-- línea agregada
    region = Region.objects.create(nombre=nombre, codigo=codigo)
    regiones[nombre] = region

# Crear zonas
zonas = {}
for _, fila in df_zonas.iterrows():
    nombre = str(fila['nombre']).strip()
    codigo = int(fila['codigo'])
    region_nombre = str(fila['region']).strip()
    region = regiones.get(region_nombre)
    if not region:
        print(f"Región no encontrada para zona '{nombre}': {region_nombre}")
        continue

    zona, _ = Zona.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': nombre, 'region': region}
    )
    zonas[nombre] = zona

# Crear sucursales
for _, fila in df_sucs.iterrows():
    codigo = int(fila['codigo'])
    nombre = str(fila['nombre']).strip()
    zona_nombre = str(fila['zona']).strip()
    zona = zonas.get(zona_nombre)
    if not zona:
        print(f"Zona no encontrada para sucursal '{nombre}': {zona_nombre}")
        continue

    Sucursal.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': nombre, 'zona': zona}
    )

print("Estructura local cargada correctamente.")
