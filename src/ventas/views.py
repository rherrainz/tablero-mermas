from django.shortcuts import render, redirect
from ventas.models import VentaMensual
from visor.models import Sucursal
from mermas.models import Sector
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
from pathlib import Path
from utils.ventas_loader import cargar_ventas_desde_excel
from datetime import datetime

MESES = {
    "01": "Enero", "02": "Febrero", "03": "Marzo",
    "04": "Abril", "05": "Mayo", "06": "Junio",
    "07": "Julio", "08": "Agosto", "09": "Septiembre",
    "10": "Octubre", "11": "Noviembre", "12": "Diciembre",
}

def cargar_ventas(request):
    if request.method == "POST":
        if 'archivo_ventas' in request.FILES:
            archivo = request.FILES['archivo_ventas']
            nombre = 'ventas.xlsx'
            path = Path(settings.MEDIA_ROOT) / nombre

            if default_storage.exists(nombre):
                default_storage.delete(nombre)
            default_storage.save(nombre, archivo)

            cargar_ventas_desde_excel(path)

            messages.success(request, "Archivo de ventas cargado correctamente.")
            return redirect("cargar_ventas")

    return render(request, "ventas/cargar_ventas.html")

def ver_ventas(request):
    sucursales = sorted(Sucursal.objects.all(), key=lambda s: int(s.codigo))
    selected_sucursal = request.GET.get("sucursal") or sucursales[0].codigo

    now = datetime.now()
    mes_actual = now.month
    ano_actual = now.year
    ultimo_mes_cerrado = mes_actual - 1 if mes_actual > 1 else 12
    selected_mes = request.GET.get("mes") or f"{ultimo_mes_cerrado:02}"
    selected_mes_int = int(selected_mes)

    if selected_mes_int <= ultimo_mes_cerrado:
        anio_max = ano_actual
    else:
        anio_max = ano_actual - 1

    anos = list(range(anio_max - 4, anio_max + 1))
    selected_sucursal_obj = Sucursal.objects.get(codigo=selected_sucursal)

    sectores = Sector.objects.all().order_by("codigo")
    tabla = []
    for sector in sectores:
        fila = {"sector": sector.nombre, "codigo": sector.codigo, "valores": []}
        valores = []
        for ano in anos:
            mes_str = f"{ano}{selected_mes}"
            venta = VentaMensual.objects.filter(
                sucursal=selected_sucursal_obj, sector=sector, mes=mes_str
            ).first()
            unidades = venta.unidades if venta else 0
            fila[ano] = unidades
            valores.append(unidades)

        fila["valores"] = valores
        fila["max_valor"] = max(valores)
        fila["min_valor"] = min(valores)

        fila["var_ult_anio"] = (
            ((valores[-1] - valores[-2]) / valores[-2]) * 100 if valores[-2] != 0 else None
        )
        max_val_prev = max(valores[:-1]) if len(valores) > 1 else 0
        fila["var_vs_mejor"] = (
            ((valores[-1] - max_val_prev) / max_val_prev) * 100 if max_val_prev != 0 else None
        )

        tabla.append(fila)

    # Datos para gráfico
    ultimo_ano_cerrado = now.year if now.month > 1 else now.year - 1
    limite_yyyymm = int(f"{ultimo_ano_cerrado}{ultimo_mes_cerrado:02}")
    ventas_validas = VentaMensual.objects.filter(
        sucursal=selected_sucursal_obj,
        mes__lte=limite_yyyymm
    ).order_by("mes")

    labels = sorted(set(v.mes for v in ventas_validas))

    def mes_legible(m):
        return f"{MESES[m[4:]]} {m[:4]}"

    labels_legibles = [mes_legible(m) for m in labels]

    series = []
    for sector in sectores:
        hidden = sector.codigo == "TOT"
        valores = []
        for m in labels:
            venta = ventas_validas.filter(sector=sector, mes=m).first()
            valores.append(venta.unidades if venta else 0)

        series.append({
            "label": f"{sector.codigo} - {sector.nombre}",
            "data": valores,
            "hidden": hidden
        })

    context = {
        "sucursales": sucursales,
        "selected_sucursal": selected_sucursal,
        "selected_mes": selected_mes,
        "mes_nombre": MESES[selected_mes],
        "anos": anos,
        "tabla": tabla,
        "meses": MESES.items(),
        "chart_labels": labels_legibles,
        "chart_series": series,
    }

    return render(request, "ventas/ver_ventas.html", context)