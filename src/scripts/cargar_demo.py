from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
from django.conf import settings
from visor.models import Region, Zona, Sucursal
from mermas.models import Sector
from const.sectores import SECTORES

class Command(BaseCommand):
    help = 'Carga estructura local (regiones, zonas, sucursales) y sectores.'

    def handle(self, *args, **kwargs):
        archivo = Path(settings.BASE_DIR) / 'media' / 'estructura_local.xlsx'
        if not archivo.exists():
            self.stdout.write(self.style.ERROR(f"❌ Archivo no encontrado: {archivo}"))
            return

        # Leer Excel
        xls = pd.ExcelFile(archivo)
        df_regiones = pd.read_excel(xls, 'regiones')
        df_zonas = pd.read_excel(xls, 'zonas')
        df_sucs = pd.read_excel(xls, 'sucursales')

        # Regiones
        regiones = {}
        for _, f in df_regiones.iterrows():
            nombre, codigo = str(f['nombre']).strip(), int(f['codigo'])
            region, _ = Region.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre})
            regiones[nombre] = region

        # Zonas
        zonas = {}
        for _, f in df_zonas.iterrows():
            nombre, codigo = str(f['nombre']).strip(), int(f['codigo'])
            region = regiones.get(str(f['region']).strip())
            if region:
                zona, _ = Zona.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre, 'region': region})
                zonas[nombre] = zona

        # Sucursales
        for _, f in df_sucs.iterrows():
            nombre, codigo = str(f['nombre']).strip(), int(f['codigo'])
            zona = zonas.get(str(f['zona']).strip())
            if zona:
                Sucursal.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre, 'zona': zona})

        self.stdout.write(self.style.SUCCESS("✅ Estructura cargada"))

        # Sectores
        for codigo, nombre in SECTORES.items():
            Sector.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre})

        self.stdout.write(self.style.SUCCESS("✅ Sectores cargados"))
