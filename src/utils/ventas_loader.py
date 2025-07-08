from django.db import transaction
import pandas as pd
from ventas.models import VentaMensual
from visor.models import Sucursal
from mermas.models import Sector

def cargar_ventas_desde_excel(path):
    df = pd.read_excel(path)

    # Limpieza básica
    df = df[df["Sucursal"].notna() & df["Sector"].notna() & df["Mes"].notna()]

    # Normalización
    df["Sucursal"] = df["Sucursal"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()
    df["Mes"] = df["Mes"].astype(int).astype(str)
    df["Unidades Vendidas"] = df["Unidades Vendidas"].astype(str).str.replace(",", "").astype(float)

    with transaction.atomic():
        for _, row in df.iterrows():
            try:
                sucursal_codigo = row["Sucursal"].lstrip("0")  # '004' -> '4'
                sucursal = Sucursal.objects.get(codigo=sucursal_codigo)
                sector = Sector.objects.get(codigo=row["Sector"])
                mes = row["Mes"]
                unidades = row["Unidades Vendidas"]

                VentaMensual.objects.update_or_create(
                    sucursal=sucursal,
                    sector=sector,
                    mes=mes,
                    defaults={"unidades": unidades}
                )
            except (Sucursal.DoesNotExist, Sector.DoesNotExist) as e:
                print(f"❌ No se encontró sucursal o sector: {e}")
                print(f"👉 Fila conflictiva: {row.to_dict()}")
            except Exception as e:
                print(f"⚠️ Error inesperado en fila {row.to_dict()}:\n{e}")

    # Agregamos totales por sucursal y mes (sector = "TOT")
    print("🧮 Generando totales por sucursal y mes...")
    agrupados = df.groupby(["Sucursal", "Mes"])["Unidades Vendidas"].sum().reset_index()

    with transaction.atomic():
        for _, row in agrupados.iterrows():
            try:
                sucursal_codigo = str(row["Sucursal"]).lstrip("0")
                sucursal = Sucursal.objects.get(codigo=sucursal_codigo)
                mes = str(row["Mes"])
                unidades = row["Unidades Vendidas"]

                VentaMensual.objects.update_or_create(
                    sucursal=sucursal,
                    sector=Sector.objects.get(codigo="TOT"),
                    mes=mes,
                    defaults={"unidades": unidades}
                )
            except Exception as e:
                print(f"⚠️ Error al guardar total de sucursal {sucursal_codigo} mes {mes}:\n{e}")

    for _, row in agrupados.iterrows():
        try:
            sucursal = Sucursal.objects.get(codigo=str(row["Sucursal"]).zfill(3).strip())
            mes = str(int(row["Mes"]))
            unidades = float(str(row["Unidades Vendidas"]).replace(",", "").strip())

            # Usamos el sector virtual 'TOT'
            sector_tot, _ = Sector.objects.get_or_create(codigo="TOT", defaults={"nombre": "Total General"})

            VentaMensual.objects.update_or_create(
                sucursal=sucursal,
                sector=sector_tot,
                mes=mes,
                defaults={"unidades": unidades}
            )
        except Exception as e:
            print(f"⚠️ Error al generar total para sucursal {row['Sucursal']} mes {row['Mes']}: {e}")
