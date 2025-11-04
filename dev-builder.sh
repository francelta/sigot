#!/bin/bash

# ============================================
# ConnecMaq - Builder.io Dev Commands
# ============================================
# Script de comandos de desarrollo para Builder.io

set -e

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${MAGENTA}============================================${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${MAGENTA}============================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_info() {
    echo -e "${CYAN}→${NC} $1"
}

# Verificar que existe builder-config
check_builder_setup() {
    if [ ! -d "builder-config" ]; then
        print_error "Builder.io no está configurado."
        print_info "Ejecuta: ./setup-builder.sh"
        exit 1
    fi
}

# Cargar variables de entorno
load_env() {
    if [ -f "backend/.env" ]; then
        export $(grep -v '^#' backend/.env | grep BUILDER_IO | xargs)
    fi
}

# Función para mostrar el menú
show_menu() {
    print_header "ConnecMaq - Builder.io Dev Commands"
    
    echo "Comandos disponibles:"
    echo ""
    echo -e "${CYAN}Configuración:${NC}"
    echo "  1. status     - Ver estado de la configuración"
    echo "  2. check      - Verificar API keys y conectividad"
    echo "  3. config     - Ver configuración actual"
    echo ""
    echo -e "${CYAN}Desarrollo:${NC}"
    echo "  4. preview    - Configurar preview URL local"
    echo "  5. models     - Listar modelos configurados"
    echo "  6. test       - Test de integración"
    echo ""
    echo -e "${CYAN}Documentación:${NC}"
    echo "  7. docs       - Abrir documentación local"
    echo "  8. help       - Ayuda rápida"
    echo ""
    echo -e "${CYAN}Utilidades:${NC}"
    echo "  9. logs       - Ver logs de webhooks"
    echo " 10. clean      - Limpiar cache (si aplica)"
    echo ""
    echo "  0. Salir"
    echo ""
}

# 1. Ver estado de la configuración
cmd_status() {
    print_header "Estado de Builder.io"
    
    # Verificar estructura
    echo -e "${BLUE}Estructura de archivos:${NC}"
    
    if [ -d "builder-config" ]; then
        print_success "builder-config/ existe"
        
        [ -f "builder-config/builder.config.json" ] && print_success "builder.config.json" || print_error "builder.config.json no encontrado"
        [ -f "builder-config/README.md" ] && print_success "README.md" || print_error "README.md no encontrado"
        [ -d "builder-config/webhooks" ] && print_success "webhooks/" || print_error "webhooks/ no encontrado"
        [ -d "builder-config/templates" ] && print_success "templates/" || print_error "templates/ no encontrado"
    else
        print_error "builder-config/ no existe"
        print_warning "Ejecuta: ./setup-builder.sh"
    fi
    
    echo ""
    
    # Verificar variables de entorno
    echo -e "${BLUE}Variables de entorno:${NC}"
    
    load_env
    
    if [ -f "backend/.env" ]; then
        if grep -q "BUILDER_IO_API_KEY" backend/.env; then
            local api_key=$(grep BUILDER_IO_API_KEY backend/.env | cut -d'=' -f2)
            if [ "$api_key" = "your-builder-api-key-here" ] || [ -z "$api_key" ]; then
                print_warning "BUILDER_IO_API_KEY no configurado"
            else
                print_success "BUILDER_IO_API_KEY configurado"
            fi
        else
            print_error "BUILDER_IO_API_KEY no encontrado en .env"
        fi
        
        if grep -q "BUILDER_IO_PRIVATE_KEY" backend/.env; then
            local private_key=$(grep BUILDER_IO_PRIVATE_KEY backend/.env | cut -d'=' -f2)
            if [ "$private_key" = "your-builder-private-key-here" ] || [ -z "$private_key" ]; then
                print_warning "BUILDER_IO_PRIVATE_KEY no configurado"
            else
                print_success "BUILDER_IO_PRIVATE_KEY configurado"
            fi
        else
            print_error "BUILDER_IO_PRIVATE_KEY no encontrado en .env"
        fi
    else
        print_error "backend/.env no encontrado"
    fi
    
    echo ""
    
    # Estado del backend
    echo -e "${BLUE}Backend Django:${NC}"
    
    if command -v python3 &> /dev/null; then
        print_success "Python 3 instalado"
    else
        print_error "Python 3 no encontrado"
    fi
    
    if [ -f "backend/manage.py" ]; then
        print_success "Django project encontrado"
    else
        print_error "Django project no encontrado"
    fi
}

# 2. Verificar API keys y conectividad
cmd_check() {
    print_header "Verificación de Builder.io"
    
    load_env
    
    if [ -z "$BUILDER_IO_API_KEY" ] || [ "$BUILDER_IO_API_KEY" = "your-builder-api-key-here" ]; then
        print_error "API Key no configurado"
        print_info "Configura BUILDER_IO_API_KEY en backend/.env"
        return 1
    fi
    
    print_info "Verificando conectividad con Builder.io..."
    
    # Test de conexión simple
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        "https://cdn.builder.io/api/v2/content/page?apiKey=${BUILDER_IO_API_KEY}&url=/")
    
    if [ "$response" = "200" ]; then
        print_success "Conexión exitosa con Builder.io API"
        print_info "API Key válido y funcionando"
    else
        print_error "Error al conectar con Builder.io (HTTP $response)"
        print_warning "Verifica que tu API Key sea correcto"
    fi
}

# 3. Ver configuración actual
cmd_config() {
    print_header "Configuración de Builder.io"
    
    load_env
    
    echo -e "${BLUE}API Keys:${NC}"
    if [ -n "$BUILDER_IO_API_KEY" ] && [ "$BUILDER_IO_API_KEY" != "your-builder-api-key-here" ]; then
        echo "  BUILDER_IO_API_KEY: ${BUILDER_IO_API_KEY:0:20}... (oculto)"
    else
        echo "  BUILDER_IO_API_KEY: ${RED}NO CONFIGURADO${NC}"
    fi
    
    if [ -n "$BUILDER_IO_PRIVATE_KEY" ] && [ "$BUILDER_IO_PRIVATE_KEY" != "your-builder-private-key-here" ]; then
        echo "  BUILDER_IO_PRIVATE_KEY: ${BUILDER_IO_PRIVATE_KEY:0:20}... (oculto)"
    else
        echo "  BUILDER_IO_PRIVATE_KEY: ${RED}NO CONFIGURADO${NC}"
    fi
    
    if [ -n "$BUILDER_IO_SPACE_ID" ] && [ "$BUILDER_IO_SPACE_ID" != "your-space-id" ]; then
        echo "  BUILDER_IO_SPACE_ID: $BUILDER_IO_SPACE_ID"
    else
        echo "  BUILDER_IO_SPACE_ID: ${YELLOW}NO CONFIGURADO${NC}"
    fi
    
    echo ""
    
    if [ -f "builder-config/builder.config.json" ]; then
        echo -e "${BLUE}Modelos configurados:${NC}"
        cat builder-config/builder.config.json | grep '"name"' | head -n 10
    fi
}

# 4. Configurar preview URL local
cmd_preview() {
    print_header "Preview URL Local"
    
    print_info "Para usar preview local en Builder.io:"
    echo ""
    echo "1. Inicia tu servidor Django:"
    echo -e "   ${CYAN}cd backend${NC}"
    echo -e "   ${CYAN}python manage.py runserver${NC}"
    echo ""
    echo "2. En Builder.io editor:"
    echo -e "   ${CYAN}Settings (⚙️) → Preview URLs${NC}"
    echo ""
    echo "3. Agrega estas URLs:"
    echo -e "   ${GREEN}http://localhost:8000${NC}"
    echo -e "   ${GREEN}http://127.0.0.1:8000${NC}"
    echo ""
    echo "4. Ahora puedes hacer preview en tiempo real"
    echo ""
    
    print_warning "Asegúrate que el servidor Django esté corriendo"
}

# 5. Listar modelos configurados
cmd_models() {
    print_header "Modelos de Builder.io"
    
    if [ -f "builder-config/builder.config.json" ]; then
        echo -e "${BLUE}Modelos disponibles:${NC}"
        echo ""
        
        # Parsear JSON simple
        cat builder-config/builder.config.json | grep -A 3 '"name"' | grep -v "^--$"
    else
        print_error "builder.config.json no encontrado"
        print_info "Ejecuta: ./setup-builder.sh"
    fi
}

# 6. Test de integración
cmd_test() {
    print_header "Test de Integración"
    
    load_env
    
    if [ -z "$BUILDER_IO_API_KEY" ] || [ "$BUILDER_IO_API_KEY" = "your-builder-api-key-here" ]; then
        print_error "API Key no configurado"
        return 1
    fi
    
    print_info "Testing API de Builder.io..."
    echo ""
    
    # Test 1: Listar contenido
    echo -e "${BLUE}Test 1: Listar contenido del modelo 'page'${NC}"
    response=$(curl -s "https://cdn.builder.io/api/v2/content/page?apiKey=${BUILDER_IO_API_KEY}&limit=5")
    
    if echo "$response" | grep -q '"results"'; then
        count=$(echo "$response" | grep -o '"results"' | wc -l)
        print_success "API responde correctamente"
        print_info "Contenido encontrado en modelo 'page'"
    else
        print_warning "No hay contenido en modelo 'page' (esto es normal si no has creado páginas aún)"
    fi
    
    echo ""
    
    # Test 2: Verificar modelos
    echo -e "${BLUE}Test 2: Verificar acceso a modelos${NC}"
    print_success "Modelos configurados localmente"
    
    echo ""
    
    # Test 3: Webhook endpoint
    echo -e "${BLUE}Test 3: Verificar webhook endpoint${NC}"
    if grep -q "builder_webhook" backend/config/urls.py 2>/dev/null; then
        print_success "Webhook endpoint configurado en Django"
    else
        print_warning "Webhook endpoint no configurado en urls.py"
        print_info "Agrega el endpoint según builder-config/README.md"
    fi
    
    echo ""
    print_success "Tests completados"
}

# 7. Abrir documentación
cmd_docs() {
    print_header "Documentación"
    
    if [ -f "builder-config/README.md" ]; then
        print_info "Abriendo documentación local..."
        
        if command -v less &> /dev/null; then
            less builder-config/README.md
        else
            cat builder-config/README.md
        fi
    else
        print_error "README.md no encontrado"
        print_info "Ejecuta: ./setup-builder.sh"
    fi
}

# 8. Ayuda rápida
cmd_help() {
    print_header "Ayuda Rápida"
    
    echo -e "${BLUE}Primeros pasos:${NC}"
    echo "  1. Ejecutar setup:     ./setup-builder.sh"
    echo "  2. Crear cuenta:       https://builder.io"
    echo "  3. Obtener API key:    Builder.io → Settings → API Keys"
    echo "  4. Configurar .env:    backend/.env"
    echo "  5. Crear página:       Builder.io → Content → New"
    echo ""
    
    echo -e "${BLUE}Comandos útiles:${NC}"
    echo "  ./dev-builder.sh status    - Ver estado"
    echo "  ./dev-builder.sh check     - Verificar conexión"
    echo "  ./dev-builder.sh preview   - Configurar preview"
    echo "  ./dev-builder.sh test      - Test de integración"
    echo ""
    
    echo -e "${BLUE}Recursos:${NC}"
    echo "  Docs local:    builder-config/README.md"
    echo "  Docs online:   https://www.builder.io/c/docs"
    echo "  Support:       https://www.builder.io/c/support"
    echo ""
    
    echo -e "${BLUE}URLs importantes:${NC}"
    echo "  Dashboard:     https://builder.io/content"
    echo "  API Docs:      https://www.builder.io/c/docs/api"
    echo "  GitHub:        https://github.com/BuilderIO/builder"
}

# 9. Ver logs
cmd_logs() {
    print_header "Logs de Builder.io"
    
    print_info "Logs de webhooks (Django):"
    echo ""
    
    if [ -f "backend/logs/builder_webhooks.log" ]; then
        tail -n 50 backend/logs/builder_webhooks.log
    else
        print_warning "No hay logs de webhooks aún"
        print_info "Los logs aparecerán cuando recibas webhooks de Builder.io"
    fi
}

# 10. Limpiar cache
cmd_clean() {
    print_header "Limpiar Cache"
    
    print_info "Limpiando archivos temporales..."
    
    # Limpiar Python cache
    find builder-config -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find builder-config -type f -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Cache limpiado"
}

# Modo interactivo
interactive_mode() {
    while true; do
        show_menu
        read -p "Selecciona una opción: " choice
        
        case $choice in
            1) cmd_status ;;
            2) cmd_check ;;
            3) cmd_config ;;
            4) cmd_preview ;;
            5) cmd_models ;;
            6) cmd_test ;;
            7) cmd_docs ;;
            8) cmd_help ;;
            9) cmd_logs ;;
            10) cmd_clean ;;
            0) 
                echo ""
                print_info "¡Hasta luego!"
                exit 0
                ;;
            *)
                print_error "Opción inválida"
                ;;
        esac
        
        echo ""
        read -p "Presiona Enter para continuar..."
        clear
    done
}

# Modo comando directo
if [ $# -eq 0 ]; then
    # Sin argumentos = modo interactivo
    clear
    check_builder_setup
    interactive_mode
else
    # Con argumentos = ejecutar comando directo
    check_builder_setup
    
    case $1 in
        status) cmd_status ;;
        check) cmd_check ;;
        config) cmd_config ;;
        preview) cmd_preview ;;
        models) cmd_models ;;
        test) cmd_test ;;
        docs) cmd_docs ;;
        help) cmd_help ;;
        logs) cmd_logs ;;
        clean) cmd_clean ;;
        *)
            print_error "Comando desconocido: $1"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
fi

