import os
import pandas as pd
import csv
import mysql.connector
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from Aplicacion.models import tblConfiguracion
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

# Carga variables de entorno desde el archivo .env
load_dotenv()

@login_required
def copiaDeSeguridad(request):
    # Conexión a la base de datos MySQL origen
    mysql_conn_origen = mysql.connector.connect(
        database=os.environ.get('DB_ORIGEN_NAME'),
        user=os.environ.get('DB_ORIGEN_USER'),
        password='',
        host=os.environ.get('DB_ORIGEN_HOST'),
        port=os.environ.get('DB_ORIGEN_PORT')
    )

    # Conexión a la base de datos MySQL destino
    mysql_conn_destino = mysql.connector.connect(
        database=os.environ.get('DB_DESTINO_NAME'),
        user=os.environ.get('DB_DESTINO_USER'),
        password='',
        host=os.environ.get('DB_DESTINO_HOST'),
        port=os.environ.get('DB_DESTINO_PORT')
    )

    # # Actualiza el registro de configuración
    # FechaEditor_v = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    # user = request.user
    # usuario = f"{user.first_name} {user.last_name}"
    # Movimiento = 'Actualización'
    # configuracion_editor = tblConfiguracion.objects.get(ID=1)
    # configuracion_editor.FechaActualizacion = FechaEditor_v
    # configuracion_editor.Usuario = usuario
    # configuracion_editor.BaseDeDatos = Movimiento
    # configuracion_editor.save()

    # Directorio temporal para los CSV
    temp_dir = 'temp_csv_data'
    os.makedirs(temp_dir, exist_ok=True)

    def export_mysql_data_to_csv(mysql_conn, table_name):
        try:
            query = f"SELECT * FROM {table_name};"
            data = pd.read_sql_query(query, mysql_conn)
            data.to_csv(os.path.join(temp_dir, f'{table_name}.csv'), index=False)
            messages.success(request, f'Datos de {table_name} exportados a CSV.')
        except mysql.connector.Error as err:
            messages.error(request, f"Error al exportar datos de {table_name}: {err}")

    def import_csv_to_mysql(mysql_conn, table_name):
        cursor = mysql_conn.cursor()
        try:
            csv_filename = os.path.join(temp_dir, f'{table_name}.csv')
            with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                columns = ', '.join(header)
                placeholders = ', '.join(['%s'] * len(header))
                for row in csv_reader:
                    query = f"""
                        INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
                        ON DUPLICATE KEY UPDATE {', '.join([f'{col}=VALUES({col})' for col in header])};
                    """
                    cursor.execute(query, row)
            mysql_conn.commit()
            messages.success(request, f'Datos importados a {table_name} en la base destino.')
        except mysql.connector.Error as err:
            messages.error(request, f"Error al importar datos a {table_name}: {err}")

    # Obtener las tablas de la base de datos origen
    cursor_origen = mysql_conn_origen.cursor()
    cursor_origen.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor_origen.fetchall()]

    # Exportar e importar datos
    for table_name in tables:
        export_mysql_data_to_csv(mysql_conn_origen, table_name)
        import_csv_to_mysql(mysql_conn_destino, table_name)

    # Limpieza de archivos temporales
    for csv_file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, csv_file))
    os.rmdir(temp_dir)

    # Cerrar conexiones
    mysql_conn_origen.close()
    mysql_conn_destino.close()

    messages.success(request, "Proceso completado con éxito.")
    return redirect('Base-de-datos')



def descargar_backup(request):
    # Ruta al archivo backup.sqlite3
    ruta_archivo = 'Respaldo_MYSQL.sqlite3'
    copiaDeSeguridad(request)

    FechaEditor_v = timezone.localtime(
        timezone.now()).strftime('%Y-%m-%d %H:%M')
    user = request.user
    # Acceder a los campos del usuario
    usuario = user.first_name + " " + user.last_name
    Movimiento = 'Descarga'
    configuracion_editor = tblConfiguracion.objects.get(ID=1)
    configuracion_editor.FechaDescarga = FechaEditor_v
    configuracion_editor.Usuario = usuario
    configuracion_editor.BaseDeDatos = Movimiento
    configuracion_editor.save()

    # Verifica si el archivo existe
    if os.path.exists(ruta_archivo):
        # Abre el archivo para lectura binaria
        with open(ruta_archivo, 'rb') as archivo:
            response = HttpResponse(
                archivo.read(), content_type='application/x-sqlite3')
            response[
                'Content-Disposition'] = f'attachment; filename="{os.path.basename(ruta_archivo)}"'

            # Agrega un mensaje de éxito
            messages.success(
                request, f"Se ha descargado correctamente la copia de seguridad en formato SQLite3.")

            # Redirige a la página deseada
            return response
    else:
        # Si el archivo no existe, puedes manejarlo de acuerdo a tus necesidades, por ejemplo, mostrar un mensaje de error.
        messages.error(request, "El archivo no existe.")
        # O redirige a la página correspondiente
        return redirect('Base-de-datos')

