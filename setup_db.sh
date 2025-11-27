#!/bin/bash

# Script para crear la base de datos SIGOT con PostGIS
# Uso: ./setup_db.sh

set -e

echo "🗄️  Configurando base de datos SIGOT..."

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Valores por defecto (puedes cambiarlos con variables de entorno)
DB_NAME=${DB_NAME:-sigot}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}

echo -e "${YELLOW}Configuración:${NC}"
echo "  Base de datos: $DB_NAME"
echo "  Usuario: $DB_USER"
echo "  Host: $DB_HOST"
echo "  Puerto: $DB_PORT"
echo ""

# Verificar si PostgreSQL está corriendo
if ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER > /dev/null 2>&1; then
    echo "❌ Error: PostgreSQL no está corriendo o no es accesible"
    echo "   Asegúrate de que PostgreSQL esté iniciado:"
    echo "   - macOS: brew services start postgresql"
    echo "   - Linux: sudo systemctl start postgresql"
    echo "   - Docker: docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgis/postgis"
    exit 1
fi

echo "✅ PostgreSQL está corriendo"

# Crear la base de datos (si no existe)
echo ""
echo "📦 Creando base de datos '$DB_NAME'..."

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres -c "CREATE DATABASE $DB_NAME;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Base de datos '$DB_NAME' creada${NC}"
else
    echo "⚠️  La base de datos ya existe o hubo un error"
fi

# Habilitar PostGIS
echo ""
echo "🗺️  Habilitando extensión PostGIS..."

PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -c "CREATE EXTENSION IF NOT EXISTS postgis;"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ PostGIS habilitado${NC}"
else
    echo "❌ Error al habilitar PostGIS"
    echo "   Asegúrate de que PostGIS esté instalado en PostgreSQL"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Base de datos configurada correctamente!${NC}"
echo ""
echo "Ahora puedes ejecutar:"
echo "  python manage.py migrate"
echo "  python manage.py runserver"


