import os
from django.shortcuts import render, redirect
from .models import Sucursal
from django.core.files.storage import default_storage
from django.contrib import messages
import pandas as pd
from django.conf import settings
from django.http import JsonResponse

def index(request):
    sucursales = Sucursal.objects.all().order_by('suc_id')
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
            messages.success(request, 'Archivo de sucursales cargado correctamente.')

        if 'archivo_zonas' in request.FILES:
            borrar_archivo_si_existe('datos_zonas.xlsx')
            archivo = request.FILES['archivo_zonas']
            default_storage.save('datos_zonas.xlsx', archivo)
            messages.success(request, 'Archivo de zonas cargado correctamente.')

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