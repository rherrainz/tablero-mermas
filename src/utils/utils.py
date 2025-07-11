from datetime import datetime

def get_limite_ventas():
    now = datetime.now()
    mes = now.month
    anio = now.year
    mes_cerrado = mes - 1 if mes > 1 else 12
    anio_cerrado = anio if mes > 1 else anio - 1
    return int(f"{anio_cerrado}{mes_cerrado:02}")