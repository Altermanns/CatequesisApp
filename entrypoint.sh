#!/bin/sh

# Salir inmediatamente si un comando falla
set -e

echo "Ejecutando migraciones de Django (SQLite para sesiones/auth)..."
python manage.py migrate --noinput

echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput

# En Render, la variable PORT es asignada automáticamente
PORT=${PORT:-8000}

echo "Iniciando Gunicorn en el puerto $PORT..."
exec gunicorn CatequesisDjango.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --threads 2 \
    --access-logfile -
