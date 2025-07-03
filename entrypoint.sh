#!/bin/sh

echo "Aplicando migraciones..."
python manage.py migrate

echo "Levantando Gunicorn..."
gunicorn Valmo.wsgi:application --bind 0.0.0.0:$PORT
