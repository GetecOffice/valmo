import sqlite3
import mysql.connector
from django.http import HttpResponse
import os
from dotenv import load_dotenv

# Obtiene la ruta absoluta del directorio actual (donde se encuentra copiadeseguridad.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Retrocede dos niveles para llegar al directorio raíz del proyecto
project_dir = os.path.dirname(os.path.dirname(current_dir))

# Carga el archivo .env desde el directorio raíz del proyecto
load_dotenv(os.path.join(project_dir, '.env'))



def import_data(request):
    try:
        # Conecta a la base de datos SQLite
        sqlite_connection = sqlite3.connect('Respaldo_MYSQL.sqlite3')
        sqlite_cursor = sqlite_connection.cursor()

        # Desactiva las comprobaciones de clave externa en MySQL
        mysql_connection = mysql.connector.connect(
            database = os.environ.get('DB_NAME'),
            user = os.environ.get('DB_USER'),
            password = os.environ.get('DB_PASSWORD'),
            host = os.environ.get('DB_HOST'),
            port = os.environ.get('DB_PORT')
        )
        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')

        # Elimina registros duplicados en django_content_type
        sqlite_cursor.execute("SELECT app_label, model, MIN(id) FROM django_content_type GROUP BY app_label, model HAVING COUNT(*) > 1;")
        duplicate_records = sqlite_cursor.fetchall()

        for app_label, model, min_id in duplicate_records:
            sqlite_cursor.execute(f"DELETE FROM django_content_type WHERE app_label = ? AND model = ? AND id <> ?", (app_label, model, min_id))

        # Obtén la lista de tablas en SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        sqlite_tables = [table[0] for table in sqlite_cursor.fetchall()]

        for table in sqlite_tables:
            # Obtiene la estructura de la tabla en SQLite
            sqlite_cursor.execute(f"PRAGMA table_info({table})")
            sqlite_columns = [column[1] for column in sqlite_cursor.fetchall()]

            # Crea la tabla en MySQL con la misma estructura
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{column} TEXT' for column in sqlite_columns])})"
            mysql_cursor.execute(create_table_query)

            # Transfiere los datos desde SQLite a MySQL
            sqlite_cursor.execute(f'SELECT * FROM {table}')
            records = sqlite_cursor.fetchall()
            for record in records:
                placeholders = ', '.join(['%s'] * len(record))
                # Utiliza la columna "id" como clave primaria en ambas bases de datos
                # Y también actualiza otras columnas en caso de duplicado
                insert_query = f'INSERT INTO {table} ({", ".join(sqlite_columns)}) VALUES ({placeholders}) ON DUPLICATE KEY UPDATE {", ".join([f"{column} = VALUES({column})" for column in sqlite_columns])}'
                mysql_cursor.execute(insert_query, record)

        # Confirma los cambios en MySQL
        mysql_connection.commit()

        # Restaura las comprobaciones de clave externa en MySQL
        mysql_cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

        # Cierra las conexiones
        mysql_connection.close()
        sqlite_connection.close()

        return HttpResponse('Datos importados exitosamente a MySQL.')

    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
