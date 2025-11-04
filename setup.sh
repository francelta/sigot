#!/bin/bash

# ============================================
# ConnecMaq - Script de Setup Automático
# ============================================

set -e  # Salir si hay algún error

echo "============================================"
echo "  ConnecMaq - Setup Automático"
echo "============================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_step() {
    echo -e "${BLUE}[PASO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -d "backend" ]; then
    print_error "No se encontró el directorio 'backend'. Ejecuta este script desde la raíz del proyecto."
    exit 1
fi

# 1. Verificar Python
print_step "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION encontrado"

# 2. Crear entorno virtual
print_step "Creando entorno virtual..."
cd backend

if [ -d "venv" ]; then
    print_warning "El entorno virtual ya existe. ¿Quieres recrearlo? (s/N)"
    read -r response
    if [[ "$response" =~ ^([sS])+$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Entorno virtual recreado"
    else
        print_success "Usando entorno virtual existente"
    fi
else
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# 3. Activar entorno virtual
print_step "Activando entorno virtual..."
source venv/bin/activate
print_success "Entorno virtual activado"

# 4. Actualizar pip
print_step "Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
print_success "pip actualizado"

# 5. Instalar dependencias
print_step "Instalando dependencias de requirements.txt..."
pip install -r requirements.txt
print_success "Dependencias instaladas"

# 6. Crear archivo .env si no existe
print_step "Configurando variables de entorno..."
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        cp env.example .env
        print_success "Archivo .env creado desde env.example"
        print_warning "Por favor, edita el archivo .env con tus configuraciones"
    else
        print_warning "No se encontró env.example, creando .env básico..."
        cat > .env << EOF
# Django
SECRET_KEY=django-insecure-change-this-in-production-$(openssl rand -base64 32)
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite por defecto para desarrollo)
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Redis (para Channels - opcional en desarrollo)
REDIS_URL=redis://localhost:6379
EOF
        print_success "Archivo .env básico creado"
    fi
else
    print_success "Archivo .env ya existe"
fi

# 7. Ejecutar migraciones
print_step "Ejecutando migraciones de base de datos..."
python manage.py migrate
print_success "Migraciones completadas"

# 8. Crear superusuario (opcional)
print_step "¿Quieres crear un superusuario ahora? (s/N)"
read -r response
if [[ "$response" =~ ^([sS])+$ ]]; then
    python manage.py createsuperuser
    print_success "Superusuario creado"
else
    print_warning "Puedes crear un superusuario más tarde con: python manage.py createsuperuser"
fi

# 9. Crear datos de prueba (opcional)
print_step "¿Quieres crear datos de prueba? (s/N)"
read -r response
if [[ "$response" =~ ^([sS])+$ ]]; then
    if [ -f "test_api.py" ]; then
        python test_api.py
        print_success "Datos de prueba creados"
    else
        print_warning "No se encontró test_api.py"
    fi
else
    print_warning "Puedes crear datos de prueba más tarde con: python test_api.py"
fi

# 10. Resumen final
echo ""
echo "============================================"
echo -e "${GREEN}  ✓ Setup Completado Exitosamente${NC}"
echo "============================================"
echo ""
echo "Credenciales de prueba:"
echo "  Constructor: constructor@test.com / TestPass123!"
echo "  Proveedor:   provider@test.com / TestPass123!"
echo ""
echo "Para ejecutar el servidor:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Accede a:"
echo "  - API:   http://localhost:8000/api/"
echo "  - Admin: http://localhost:8000/admin/"
echo ""
echo "Para ver más comandos útiles, ejecuta: make help"
echo "============================================"

