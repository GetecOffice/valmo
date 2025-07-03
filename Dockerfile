FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libffi-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ejecuta migraciones y arranca el servidor con Gunicorn
CMD python manage.py migrate && gunicorn Valmo.wsgi:application
# CMD ["sh", "-c", "python manage.py migrate && gunicorn Valmo.wsgi:application --bind 0.0.0.0:8080"]
