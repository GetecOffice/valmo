FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto a Docker
COPY . /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python desde el archivo requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ejecutar las migraciones antes de iniciar la aplicación
CMD python manage.py migrate && gunicorn Valmo.wsgi:application
