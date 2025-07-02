import pandas as pd
from mermas.models import MermaSucursal, MermaZona, Sector
from visor.models import Sucursal, Zona

def cargar_mermas_sucursal(path):
    columnas = [
        "Sucursal", "Sector", "Cantidad Mermas", "$ Mermas", "Unidades Vendidas",
        "$ Venta s/IVA", "% Mermas s/Ventas", "$ Total AJU", "% de $ AJU / $ Mermas",
        "$ Mermas - No AJU", "% $ No AJU / $ Mermas"
    ]

    df = pd.read_excel(path, sheet_name=0, skiprows=6, header=None)
    df = df[df.iloc[:, 0].notna()]
    df.columns = columnas

    for _, row in df.iterrows():
        try:
            # Cast a str y strip para evitar errores con enteros
            sucursal_codigo = str(row["Sucursal"]).strip()
            sector_codigo = str(row["Sector"]).strip()

            sucursal = Sucursal.objects.get(codigo=sucursal_codigo)
            sector = Sector.objects.get(codigo=sector_codigo)

            MermaSucursal.objects.update_or_create(
                sucursal=sucursal,
                sector=sector,
                defaults={
                    "cantidad_mermas": float(row["Cantidad Mermas"]),
                    "monto_mermas": float(row["$ Mermas"]),
                    "unidades_vendidas": int(row["Unidades Vendidas"]),
                    "monto_venta": float(row["$ Venta s/IVA"]),
                    "porcentaje_mermas_sobre_venta": float(row["% Mermas s/Ventas"]),
                    "monto_ajuste": float(row["$ Total AJU"]),
                    "porcentaje_ajuste_sobre_merma": float(row["% de $ AJU / $ Mermas"]) if not pd.isna(row["% de $ AJU / $ Mermas"]) else 0.0,
                    "monto_mermas_no_ajustadas": float(row["$ Mermas - No AJU"]),
                    "porcentaje_mermas_no_ajustadas": float(row["% $ No AJU / $ Mermas"]) if not pd.isna(row["% $ No AJU / $ Mermas"]) else 0.0,
                }
            )
        except (Sucursal.DoesNotExist, Sector.DoesNotExist) as e:
            print(f"❌ No se encontró: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado con fila {row.to_dict()}: {e}")

def cargar_mermas_zona(path):
    import pandas as pd
    from mermas.models import Zona, Sector, MermaZona

    df = pd.read_excel(path)  # encabezado en la primera fila
    df.columns = [str(c).strip() for c in df.columns]  # limpia espacios
    df = df[df["Zona"].notna()]  # elimina filas vacías

    for _, row in df.iterrows():
        try:
            zona = Zona.objects.get(nombre=str(row["Zona"]).strip())
            sector = Sector.objects.get(codigo=str(row["Sector"]).strip())

            MermaZona.objects.update_or_create(
                zona=zona,
                sector=sector,
                defaults={
                    "cantidad_mermas": float(row["Cantidad Mermas"]),
                    "monto_mermas": float(row["$ Mermas"]),
                    "unidades_vendidas": int(row["Unidades Vendidas"]),
                    "monto_venta": float(row["$ Venta s/IVA"]),
                    "porcentaje_mermas_sobre_venta": float(row["% Mermas s/Ventas"]),
                    "monto_ajuste": float(row["$ Total AJU"]),
                    "porcentaje_ajuste_sobre_merma": float(row["% de $ AJU / $ Mermas"]),
                    "monto_mermas_no_ajustadas": float(row["$ Mermas - No AJU"]),
                    "porcentaje_mermas_no_ajustadas": float(row["% $ No AJU / $ Mermas"]),
                }
            )
        except (Zona.DoesNotExist, Sector.DoesNotExist) as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado con fila:\n{row}\n{e}")
