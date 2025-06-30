import pandas as pd
from visor.models import Sucursal

# Elegí uno de los dos:
CSV_PATH = "sucursales.csv"
# EXCEL_PATH = "sucursales.xlsx"

def run():
    # Para CSV
    df = pd.read_csv(CSV_PATH)

    # # Para Excel
    # df = pd.read_excel(EXCEL_PATH)

    for _, row in df.iterrows():
        sucursal, created = Sucursal.objects.update_or_create(
            suc_id=row['suc_id'],
            defaults={
                'nombre': row['nombre'],
                'zona': row['zona'],
                'region': row['region'],
            }
        )
        if created:
            print(f"✔ Sucursal creada: {sucursal}")
        else:
            print(f"↺ Sucursal actualizada: {sucursal}")
