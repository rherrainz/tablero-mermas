# Panel de Control de Operaciones

El **Panel de Control de Operaciones** es una aplicación web desarrollada en **Django** y **Bootstrap** que permite centralizar información operativa clave de una cadena de supermercados. Reemplaza múltiples archivos Excel dispersos con una interfaz web amigable, adaptable a distintos dispositivos y enfocada en la toma de decisiones basadas en datos.

## Funcionalidades principales

- 📊 **Tablero de Mermas**

  - Visualización por sucursal, zona y sector
  - Comparativa contra presupuestos
  - Desvíos en pesos y porcentaje
  - Exportación a PDF en formato A3 horizontal
- 📈 **Evolución de Ventas**

  - Carga y visualización de ventas históricas por sector y sucursal (últimos 5 años)
  - Tablas con totales y variaciones interanuales
  - Gráficos de líneas comparativos por sector
- 🗃️ **Carga de Datos vía Excel**

  - Plan de mermas
  - Datos reales por sucursal y zona
  - Ventas históricas
  - Formatos preestablecidos para facilitar la carga
- 📱 **Diseño Responsive**

  - Interfaz optimizada para PC, tablets y dispositivos móviles/PDA
- 🌱 **Compromiso con el Triple Impacto**

  - Acceso inmediato a información clave
  - Reducción de impresiones y uso de papel

## Tecnologías utilizadas

- **Backend:** Django, SQLite/PostgreSQL
- **Frontend:** Bootstrap, HTML, JS, html2pdf.js
- **Visualización:** Matplotlib (gráficos en backend), Recharts (si se conecta con frontend React en el futuro)
- **Otros:** Pandas (procesamiento de datos), openpyxl (carga de Excel)

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/rherrainz/tablero-mermas.git
   cd tablero-mermas
   ```
2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # o venv\Scripts\activate en Windows
   ```
3. Instalar dependencias:

   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar migraciones:

   ```bash
   python manage.py migrate
   ```
5. Cargar estructura inicial (regiones, zonas, sucursales y sectores):

   ```bash
   python manage.py shell
   >>> exec(open('scripts/cargar_estructura_local.py').read())
   >>> exec(open('scripts/cargar_sectores.py').read())
   ```
6. Iniciar el servidor:

   ```bash
   python manage.py runserver
   ```

## Contribuciones

Este proyecto está en evolución. Si querés colaborar o sugerir mejoras, ¡sos bienvenido!

## Licencia

MIT

---

Desarrollado por [Rodrigo Herrainz](https://github.com/rherrainz) 🧠💻
