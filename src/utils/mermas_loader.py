import pandas as pd
from mermas.models import MermaSucursal, MermaZona, Sector
from visor.models import Sucursal, Zona

def cargar_mermas_sucursal(path):
    columnas = [
        "Sucursal", "Sector", "Cantidad Mermas", "$ Mermas", "Unidades Vendidas",
        "$ Venta s/IVA", "% Mermas s/Ventas", "$ Total AJU", "% de $ AJU / $ Mermas",
        "$ Mermas - No AJU", "% $ No AJU / $ Mermas"
    ]

    # Leer todo sin encabezado

    df_crudo = pd.read_excel(path, header=None)

    # Buscamos la primera fila donde la columna 0 contenga un número (código de sucursal)
    fila_inicio = df_crudo[df_crudo.iloc[:, 0].astype(str).str.match(r"^\d+$")].index[0]

    # Leemos a partir de esa fila
    df = pd.read_excel(path, skiprows=fila_inicio, header=None)

    # Leer desde esa fila como encabezado

    df = df[df.iloc[:, 0].notna()]
    df.columns = columnas

    for _, row in df.iterrows():
        try:
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
        except Sucursal.DoesNotExist:
            print("❌ No se encontró la sucursal con código:", repr(sucursal_codigo))
            print("👉 Fila del Excel:", row.to_dict())
        except Exception as e:
            print(f"⚠️ Error inesperado con fila {row.to_dict()}: {e}")


def cargar_mermas_zona(path):
    
    # Leemos sin encabezado para buscar la fila de inicio
    df_crudo = pd.read_excel(path, header=None)

    # Detectar la primera fila donde aparece una zona no vacía
    fila_inicio = df_crudo[df_crudo.iloc[:, 0].notna()].index[0]

    # Ahora leemos desde esa fila con nombres de columnas
    df = pd.read_excel(path, skiprows=fila_inicio, header=None)

    columnas = [
        "Zona", "Sector", "Cantidad Mermas", "$ Mermas", "Unidades Vendidas",
        "$ Venta s/IVA", "% Mermas s/Ventas", "$ Total AJU", "% de $ AJU / $ Mermas",
        "$ Mermas - No AJU", "% $ No AJU / $ Mermas"
    ]
    df.columns = columnas

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
                    "porcentaje_ajuste_sobre_merma": float(row["% de $ AJU / $ Mermas"]) if not pd.isna(row["% de $ AJU / $ Mermas"]) else 0.0,
                    "monto_mermas_no_ajustadas": float(row["$ Mermas - No AJU"]),
                    "porcentaje_mermas_no_ajustadas": float(row["% $ No AJU / $ Mermas"]) if not pd.isna(row["% $ No AJU / $ Mermas"]) else 0.0,
                }
            )
        except (Zona.DoesNotExist, Sector.DoesNotExist) as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"⚠️ Error inesperado con fila:\n{row}\n{e}")
