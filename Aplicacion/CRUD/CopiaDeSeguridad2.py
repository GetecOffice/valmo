import sqlite3
import os
from django.shortcuts import redirect
from django.contrib import messages
import mysql.connector
import pandas as pd
import csv
from django.http import HttpResponse
from django.utils import timezone
from Aplicacion.forms import *
from Aplicacion.models import *
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv

# Obtiene la ruta absoluta del directorio actual (donde se encuentra copiadeseguridad.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Retrocede dos niveles para llegar al directorio raíz del proyecto
project_dir = os.path.dirname(os.path.dirname(current_dir))

# Carga el archivo .env desde el directorio raíz del proyecto
load_dotenv(os.path.join(project_dir, '.env'))

@login_required
def copiaDeSeguridad(request):
    # Conexión a la base de datos MySQL
    mysql_conn = mysql.connector.connect(
        database=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )

    # Conexión a la base de datos SQLite3
    sqlite_conn = sqlite3.connect('Respaldo_MYSQL.sqlite3')

    FechaEditor_v = timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M')
    user = request.user
    # Acceder a los campos del usuario
    usuario = user.first_name + " " + user.last_name
    Movimiento = 'Actualización'
    configuracion_editor = tblConfiguracion.objects.get(ID=1)
    configuracion_editor.FechaActualizacion = FechaEditor_v
    configuracion_editor.Usuario = usuario
    configuracion_editor.BaseDeDatos = Movimiento
    configuracion_editor.save()

    # Función para exportar datos de MySQL a CSV
    def export_mysql_data_to_csv(mysql_conn, table_name):
        try:
            # Obtiene el directorio actual de trabajo
            current_directory = os.getcwd()

            # Cambia el directorio actual de trabajo a la ubicación de 'temp_csv_data'
            os.chdir(temp_dir)

            query = f"SELECT * FROM {table_name};"
            data = pd.read_sql_query(query, mysql_conn)
            data.to_csv(f'{table_name}.csv', index=False)
            messages.success(request, f'La exportación a CSV de la tabla {table_name} se ha actualizado exitosamente.')
        except mysql.connector.Error as err:
            messages.error(request, f"Error al exportar datos de {table_name}: {err}")
        finally:
            # Restaura el directorio actual de trabajo
            os.chdir(current_directory)

    # Directorio temporal para archivos CSV
    temp_dir = 'temp_csv_data'
    os.makedirs(temp_dir, exist_ok=True)

    # Función para importar datos desde CSV a SQLite3 y actualizar registros existentes
    def import_csv_to_sqlite(sqlite_conn, table_name):
        cursor = sqlite_conn.cursor()
        try:
            csv_filename = os.path.join(temp_dir, f'{table_name}.csv')

            # Inserta o actualiza registros
            with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)  # Lee la primera fila (cabecera)
                columns = ', '.join(header)
                placeholders = ', '.join(['?'] * len(header))
                for row in csv_reader:
                    # Preparar los valores para el comando de inserción
                    values = tuple(row)
                    # Construir la consulta de actualización
                    update_query = f"""
                        INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
                        ON CONFLICT(ID) DO UPDATE SET {', '.join([f'{col}=excluded.{col}' for col in header if col != 'ID'])};
                    """
                    cursor.execute(update_query, values)
            messages.success(request, f'La exportación a SQLITE3 de la tabla {table_name} se ha actualizado exitosamente.')
        except sqlite3.Error as err:
            messages.error(request, f"Error al importar datos a {table_name}: {err}")

    # Obtener la lista de tablas presentes en la base de datos MySQL
    cursor = mysql_conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]

    # Iterar sobre las tablas y realizar exportación e importación
    for table_name in tables:
        export_mysql_data_to_csv(mysql_conn, table_name)
        import_csv_to_sqlite(sqlite_conn, table_name)

    # Cierra las conexiones
    mysql_conn.close()
    sqlite_conn.commit()
    sqlite_conn.close()

    for csv_file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, csv_file)
        os.remove(file_path)

    os.rmdir(temp_dir)

    messages.success(request, f"Proceso de exportación e importación completado.")
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
