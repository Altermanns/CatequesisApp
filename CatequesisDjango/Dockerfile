# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Establecer variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . /app/

# Crear carpeta para archivos estáticos
RUN mkdir -p staticfiles

# Dar permisos al script de entrada (lo crearemos a continuación)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Puerto que usará la app (Render asigna uno por defecto, pero Gunicorn escuchará aquí)
EXPOSE 8000

# Usar el script de entrada para arrancar
ENTRYPOINT ["/entrypoint.sh"]
