#!/bin/bash

# Script para ejecutar el servidor de desarrollo de ConnecMaq
# Usage: ./run_dev.sh

echo "🚀 Iniciando ConnecMaq Backend..."
echo ""

# Activar el entorno virtual
source venv/bin/activate

# Verificar que las migraciones estén aplicadas
echo "📋 Verificando migraciones..."
python manage.py migrate --check || {
    echo "⚠️  Hay migraciones pendientes. Aplicando..."
    python manage.py migrate
}

echo ""
echo "✅ Todo listo!"
echo ""
echo "📡 Servidor disponible en: http://localhost:8000"
echo "🔐 Admin panel en: http://localhost:8000/admin"
echo ""
echo "Para detener el servidor: Ctrl+C"
echo ""

# Ejecutar el servidor
python manage.py runserver

