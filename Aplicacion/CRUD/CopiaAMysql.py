import sqlite3
import pymysql
from django.http import HttpResponse
import os
from dotenv import load_dotenv

# Obtiene la ruta absoluta del directorio actual (donde se encuentra copiadeseguridad.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Retrocede dos niveles para llegar al directorio raíz del proyecto
project_dir = os.path.dirname(os.path.dirname(current_dir))

# Carga el archivo .env desde el directorio raíz del proyecto
load_dotenv(os.path.join(project_dir, '.env'))



import os
import sqlite3
import pymysql  # 🔄 Importación modificada
from django.http import HttpResponse

def import_data(request):
    try:
        # Conecta a la base de datos SQLite
        sqlite_connection = sqlite3.connect('Respaldo_MYSQL.sqlite3')
        sqlite_cursor = sqlite_connection.cursor()

        # Conecta a la base de datos MySQL usando PyMySQL
        mysql_connection = pymysql.connect(  # 🔄 Cambiado aquí
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port=int(os.environ.get('DB_PORT', 3306)),  # asegúrate de convertirlo a int
            charset='utf8mb4',
            autocommit=False,
            cursorclass=pymysql.cursors.Cursor
        )

        mysql_cursor = mysql_connection.cursor()
        mysql_cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')

        # Elimina registros duplicados en django_content_type
        sqlite_cursor.execute("""
            SELECT app_label, model, MIN(id)
            FROM django_content_type
            GROUP BY app_label, model
            HAVING COUNT(*) > 1;
        """)
        duplicate_records = sqlite_cursor.fetchall()

        for app_label, model, min_id in duplicate_records:
            sqlite_cursor.execute(
                "DELETE FROM django_content_type WHERE app_label = ? AND model = ? AND id <> ?",
                (app_label, model, min_id)
            )

        # Obtiene las tablas en SQLite
        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        sqlite_tables = [table[0] for table in sqlite_cursor.fetchall()]

        for table in sqlite_tables:
            sqlite_cursor.execute(f"PRAGMA table_info({table})")
            sqlite_columns = [column[1] for column in sqlite_cursor.fetchall()]

            # Crea tabla en MySQL si no existe
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    {', '.join([f'{col} TEXT' for col in sqlite_columns])}
                )
            """
            mysql_cursor.execute(create_table_query)

            # Transfiere los datos
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            records = sqlite_cursor.fetchall()

            for record in records:
                placeholders = ', '.join(['%s'] * len(record))
                update_clause = ', '.join([f"{col} = VALUES({col})" for col in sqlite_columns])
                insert_query = f"""
                    INSERT INTO {table} ({', '.join(sqlite_columns)})
                    VALUES ({placeholders})
                    ON DUPLICATE KEY UPDATE {update_clause}
                """
                mysql_cursor.execute(insert_query, record)

        mysql_connection.commit()
        mysql_cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
        mysql_connection.close()
        sqlite_connection.close()

        return HttpResponse('Datos importados exitosamente a MySQL.')

    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')
