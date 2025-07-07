import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, PlanMerma
from django.core.files.storage import default_storage
from django.contrib import messages
import pandas as pd
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from utils.plan_loader import cargar_plan_desde_excel
from pathlib import Path
from utils.mermas_loader import cargar_mermas_sucursal, cargar_mermas_zona
from mermas.models import MermaSucursal, MermaZona, Sector
from django.template.loader import get_template
from django.conf import settings
import pdfkit
from django.template.loader import render_to_string


def index(request):
    sucursales = Sucursal.objects.all().order_by('codigo')
    return render(request, 'visor/index.html', {'sucursales': sucursales})


def sucursal_view(request, codigo):
    return render(request, 'visor/sucursal.html', {'codigo': codigo})


def borrar_archivo_si_existe(nombre_archivo):
    path = os.path.join(settings.MEDIA_ROOT, nombre_archivo)
    if os.path.exists(path):
        os.remove(path)


def cargar_excel(request):
    if request.method == 'POST':
        if 'archivo_sucs' in request.FILES:
            borrar_archivo_si_existe('datos_sucs.xlsx')
            archivo = request.FILES['archivo_sucs']
            default_storage.save('datos_sucs.xlsx', archivo)
            messages.success(
                request, 'Archivo de sucursales cargado correctamente.')

        if 'archivo_zonas' in request.FILES:
            borrar_archivo_si_existe('datos_zonas.xlsx')
            archivo = request.FILES['archivo_zonas']
            default_storage.save('datos_zonas.xlsx', archivo)
            messages.success(
                request, 'Archivo de zonas cargado correctamente.')

        if 'archivo_plan' in request.FILES:
            borrar_archivo_si_existe('plan.xlsx')
            archivo = request.FILES['archivo_plan']
            default_storage.save('plan.xlsx', archivo)
            messages.success(
                request, 'Archivo de plan de mermas cargado correctamente.')
            path = Path(settings.MEDIA_ROOT) / 'plan.xlsx'
            cargar_plan_desde_excel(path)

        if 'archivo_mermas_sucs' in request.FILES:
            borrar_archivo_si_existe('archivo_mermas_sucs.xlsx')
            archivo = request.FILES['archivo_mermas_sucs']
            default_storage.save('archivo_mermas_sucs.xlsx', archivo)
            messages.success(
                request, 'Archivo de mermas por sucursal cargado correctamente.')
            path = Path(settings.MEDIA_ROOT) / 'archivo_mermas_sucs.xlsx'
            cargar_mermas_sucursal(path)

        if 'archivo_mermas_zonas' in request.FILES:
            borrar_archivo_si_existe('archivo_mermas_zonas.xlsx')
            archivo = request.FILES['archivo_mermas_zonas']
            default_storage.save('archivo_mermas_zonas.xlsx', archivo)
            messages.success(
                request, 'Archivo de mermas por zona cargado correctamente.')
            path = Path(settings.MEDIA_ROOT) / 'archivo_mermas_zonas.xlsx'
            cargar_mermas_zona(path)

        return redirect('cargar_excel')

    return render(request, 'visor/cargar_excel.html')


def ver_datos_sucs(request):
    ruta_excel = settings.MEDIA_ROOT / "datos_sucs.xlsx"

    # Leemos la hoja correspondiente
    df = pd.read_excel(ruta_excel, sheet_name=None)  # para ver las hojas
    hojas = list(df.keys())

    # Probamos con la hoja que contenga "sucs"
    hoja_sucs = next((h for h in hojas if "suc" in h.lower()), None)

    if not hoja_sucs:
        return JsonResponse({"error": "No se encontró la hoja de sucursales"})

    datos = pd.read_excel(ruta_excel, sheet_name=hoja_sucs, skiprows=6)

    # Filtramos las filas que tengan código de sucursal
    datos = datos[datos.iloc[:, 0].notna()]
    datos = datos.rename(columns={datos.columns[0]: "sucursal"})

    # Agrupamos por sucursal (solo para ver qué hay)
    sucursales = datos["sucursal"].unique().tolist()

    return JsonResponse({
        "hoja_detectada": hoja_sucs,
        "cantidad_registros": len(datos),
        "sucursales_detectadas": sucursales[:10],  # mostramos los primeros 10
    })

def get_context_tablero_sucursal(codigo):
    sucursal = get_object_or_404(Sucursal, codigo=codigo)
    zona = sucursal.zona

    mermas_suc = MermaSucursal.objects.filter(sucursal=sucursal)
    mermas_zona = MermaZona.objects.filter(zona=zona)

    SECTORES_EXCLUIDOS = ["INSUMOS", "PANADERIA", "ROTISERIA Y PASTAS"]
    sectores_data = []
    for merma_s in mermas_suc:
        sector = merma_s.sector
        merma_z = mermas_zona.filter(sector=sector).first()
        plan = PlanMerma.objects.filter(sucursal=sucursal.codigo, sector=sector.codigo).first()
        presupuesto = plan.porcentaje if plan else 0
        diferencia_porcentual = merma_s.porcentaje_mermas_sobre_venta * 100 - presupuesto
        diferencia_monetaria = merma_s.monto_mermas - (presupuesto * merma_s.monto_venta / 100)
        es_oculto = sector.nombre.upper() in SECTORES_EXCLUIDOS

        sectores_data.append({
            'nombre': sector.nombre,
            'monto_mermas': merma_s.monto_mermas,
            'porc_aju': merma_s.porcentaje_ajuste_sobre_merma * 100,
            'porc_no_aju': merma_s.porcentaje_mermas_no_ajustadas * 100,
            'porc_merma_venta': merma_s.porcentaje_mermas_sobre_venta * 100,
            'presupuesto': presupuesto,
            'dif_porc': diferencia_porcentual,
            'dif_monto': diferencia_monetaria,
            'desvio_presupuestario': presupuesto * merma_s.monto_venta / 100,
            'alerta_merma': (
                "success" if diferencia_porcentual >= 0
                else "warning" if diferencia_porcentual >= -0.2
                else "danger"
            ),
            'es_oculto': es_oculto,
        })

    mermas_suc_filtradas = [
        m for m in mermas_suc if m.sector.nombre.upper() not in SECTORES_EXCLUIDOS]
    mermas_zona_filtradas = [
        m for m in mermas_zona if m.sector.nombre.upper() not in SECTORES_EXCLUIDOS]

    total_ventas_suc = sum(m.monto_venta for m in mermas_suc)
    total_ventas_zona = sum(m.monto_venta for m in mermas_zona)
    total_merma_suc = sum(m.monto_mermas for m in mermas_suc_filtradas)
    total_merma_zona = sum(m.monto_mermas for m in mermas_zona_filtradas)
    total_merma_suc_pct = (total_merma_suc / total_ventas_suc) * 100 if total_ventas_suc else 0
    total_merma_zona_pct = (total_merma_zona / total_ventas_zona) * 100 if total_ventas_zona else 0
    total_aju_suc = sum(m.monto_ajuste for m in mermas_suc_filtradas)
    total_no_aju_suc = sum(m.monto_mermas_no_ajustadas for m in mermas_suc_filtradas)
    porc_aju = (total_aju_suc / total_merma_suc) * 100 if total_merma_suc else 0
    porc_no_aju = (total_no_aju_suc / total_merma_suc) * 100 if total_merma_suc else 0

    total_presupuesto_valorado = 0
    for m in mermas_suc_filtradas:
        plan = PlanMerma.objects.filter(sucursal=sucursal.codigo, sector=m.sector.codigo).first()
        if plan:
            total_presupuesto_valorado += plan.porcentaje * m.monto_venta / 100
    presupuesto_total_pct = (total_presupuesto_valorado / total_ventas_suc) * 100 if total_ventas_suc else 0
    diferencia_total_pct = presupuesto_total_pct - total_merma_suc_pct

    if diferencia_total_pct <= 0:
        alerta_merma_pct = "success"
    elif diferencia_total_pct <= -0.2:
        alerta_merma_pct = "warning"
    else:
        alerta_merma_pct = "danger"

    sucursales = sorted(Sucursal.objects.all(), key=lambda s: int(s.codigo))

    return {
        'sucursal': sucursal,
        'zona': zona,
        'sectores': sectores_data,
        'merma_total_sucursal': total_merma_suc,
        'merma_total_sucursal_pct': total_merma_suc_pct,
        'presupuesto_total': presupuesto_total_pct,
        'merma_total_zona': total_merma_zona,
        'merma_total_zona_pct': total_merma_zona_pct,
        'porcentaje_aju': porc_aju,
        'porcentaje_no_aju': porc_no_aju,
        'alerta_merma_pct': alerta_merma_pct,
        'sucursales': sucursales,
    }


def tablero_sucursal(request, codigo):
    context = get_context_tablero_sucursal(codigo)
    return render(request, "visor/tablero.html", context)


def tablero_pdf(request, codigo):
    contexto = get_context_tablero_sucursal(codigo)
    return render(request, "visor/tablero_pdf.html", contexto)