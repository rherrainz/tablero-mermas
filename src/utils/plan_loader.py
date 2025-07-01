import pandas as pd
from pathlib import Path
from visor.models import PlanMerma
from const.sectores import SECTORES  # Importación correcta

def cargar_plan_desde_excel(ruta_excel: Path):
    df = pd.read_excel(ruta_excel)
    df.columns = [col.strip().lower() for col in df.columns]

    PlanMerma.objects.all().delete()

    errores = 0
    for index, fila in df.iterrows():
        try:
            sucursal = str(fila['sucursal']).strip()
            sector = str(fila['sector']).strip().upper()
            plan = float(fila['plan'])

            # Permitimos 'TOT' explícitamente
            if sector != 'TOT' and sector not in SECTORES:
                print(f"⚠️  Sector inválido en fila {index + 2}: '{sector}' no está en SECTORES")
                errores += 1
                continue

            # Ampliamos el rango permitido
            if not -50.0 <= plan <= 50.0:
                print(f"⚠️  Porcentaje fuera de rango en fila {index + 2}: {plan}")
                errores += 1
                continue

            PlanMerma.objects.create(
                sucursal=sucursal,
                sector=sector,
                porcentaje=plan
            )

        except Exception as e:
            print(f"❌ Error en fila {index + 2}: {e}")
            errores += 1

    if errores == 0:
        print("✅ Plan cargado correctamente sin errores.")
    else:
        print(f"⚠️  Plan cargado con {errores} fila(s) con errores.")
