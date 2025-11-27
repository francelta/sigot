# Dockerfile para SIGOT Backend (Django + GeoDjango + Channels)
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema para GeoDjango (GDAL, GEOS, PROJ)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Colectar archivos estáticos
RUN python manage.py collectstatic --noinput || true

# Puerto por defecto
EXPOSE 8000

# Comando de arranque (Daphne para ASGI/Channels)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sigot.boot.asgi:application"]

