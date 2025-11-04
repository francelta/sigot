# ============================================
# ConnecMaq - Makefile
# ============================================

.PHONY: help setup install run migrate test clean superuser testdata shell setup-builder builder-docs builder-install-deps builder-dev builder-status builder-check builder-test

# Variables
PYTHON := python3
PIP := pip
MANAGE := cd backend && $(PYTHON) manage.py
VENV := backend/venv
ACTIVATE := . $(VENV)/bin/activate

# Colores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# ============================================
# Comandos Principales
# ============================================

help: ## Mostrar esta ayuda
	@echo ""
	@echo "$(BLUE)============================================$(NC)"
	@echo "$(BLUE)  ConnecMaq - Comandos Disponibles$(NC)"
	@echo "$(BLUE)============================================$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Ejecutar setup completo (instalar + migrar + datos de prueba)
	@echo "$(BLUE)[SETUP]$(NC) Ejecutando setup completo..."
	@chmod +x setup.sh
	@./setup.sh

install: ## Instalar dependencias
	@echo "$(BLUE)[INSTALL]$(NC) Instalando dependencias..."
	@cd backend && $(PYTHON) -m venv venv
	@$(ACTIVATE) && cd backend && $(PIP) install --upgrade pip
	@$(ACTIVATE) && cd backend && $(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

run: ## Ejecutar servidor de desarrollo
	@echo "$(BLUE)[RUN]$(NC) Iniciando servidor..."
	@$(ACTIVATE) && $(MANAGE) runserver

runserver: run ## Alias para 'run'

migrate: ## Ejecutar migraciones
	@echo "$(BLUE)[MIGRATE]$(NC) Ejecutando migraciones..."
	@$(ACTIVATE) && $(MANAGE) migrate
	@echo "$(GREEN)✓ Migraciones completadas$(NC)"

makemigrations: ## Crear nuevas migraciones
	@echo "$(BLUE)[MAKEMIGRATIONS]$(NC) Creando migraciones..."
	@$(ACTIVATE) && $(MANAGE) makemigrations
	@echo "$(GREEN)✓ Migraciones creadas$(NC)"

superuser: ## Crear superusuario
	@echo "$(BLUE)[SUPERUSER]$(NC) Creando superusuario..."
	@$(ACTIVATE) && $(MANAGE) createsuperuser

testdata: ## Crear datos de prueba
	@echo "$(BLUE)[TESTDATA]$(NC) Creando datos de prueba..."
	@$(ACTIVATE) && cd backend && $(PYTHON) test_api.py
	@echo "$(GREEN)✓ Datos de prueba creados$(NC)"

shell: ## Abrir shell de Django
	@echo "$(BLUE)[SHELL]$(NC) Abriendo shell..."
	@$(ACTIVATE) && $(MANAGE) shell

dbshell: ## Abrir shell de base de datos
	@echo "$(BLUE)[DBSHELL]$(NC) Abriendo shell de BD..."
	@$(ACTIVATE) && $(MANAGE) dbshell

test: ## Ejecutar tests
	@echo "$(BLUE)[TEST]$(NC) Ejecutando tests..."
	@$(ACTIVATE) && cd backend && pytest
	@echo "$(GREEN)✓ Tests completados$(NC)"

# ============================================
# Limpieza y Mantenimiento
# ============================================

clean: ## Limpiar archivos temporales y caché
	@echo "$(BLUE)[CLEAN]$(NC) Limpiando archivos temporales..."
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name '.DS_Store' -delete
	@rm -rf backend/.pytest_cache
	@echo "$(GREEN)✓ Limpieza completada$(NC)"

clean-db: ## Eliminar base de datos SQLite
	@echo "$(YELLOW)[CLEAN-DB]$(NC) Eliminando base de datos..."
	@rm -f backend/db.sqlite3
	@echo "$(GREEN)✓ Base de datos eliminada$(NC)"

reset-db: clean-db migrate testdata ## Resetear base de datos completa
	@echo "$(GREEN)✓ Base de datos reseteada$(NC)"

# ============================================
# Desarrollo
# ============================================

check: ## Verificar código (migraciones pendientes, etc)
	@echo "$(BLUE)[CHECK]$(NC) Verificando proyecto..."
	@$(ACTIVATE) && $(MANAGE) check
	@$(ACTIVATE) && $(MANAGE) makemigrations --check --dry-run
	@echo "$(GREEN)✓ Verificación completada$(NC)"

collectstatic: ## Recolectar archivos estáticos
	@echo "$(BLUE)[COLLECTSTATIC]$(NC) Recolectando estáticos..."
	@$(ACTIVATE) && $(MANAGE) collectstatic --noinput
	@echo "$(GREEN)✓ Estáticos recolectados$(NC)"

showmigrations: ## Mostrar estado de migraciones
	@echo "$(BLUE)[MIGRATIONS]$(NC) Estado de migraciones:"
	@$(ACTIVATE) && $(MANAGE) showmigrations

# ============================================
# Builder.io Integration
# ============================================

setup-builder: ## Setup de Builder.io (Visual Headless CMS)
	@echo "$(BLUE)[BUILDER.IO]$(NC) Configurando Builder.io..."
	@chmod +x setup-builder.sh
	@./setup-builder.sh
	@echo "$(GREEN)✓ Builder.io configurado$(NC)"

builder-docs: ## Ver documentación de Builder.io
	@echo "$(BLUE)[BUILDER.IO]$(NC) Abriendo documentación..."
	@cat builder-config/README.md

builder-install-deps: ## Instalar dependencias Python para Builder.io
	@echo "$(BLUE)[BUILDER.IO]$(NC) Instalando dependencias..."
	@$(ACTIVATE) && cd backend && $(PIP) install requests
	@echo "$(GREEN)✓ Dependencias instaladas$(NC)"

builder-dev: ## Abrir herramientas de desarrollo de Builder.io
	@chmod +x dev-builder.sh
	@./dev-builder.sh

builder-status: ## Ver estado de configuración de Builder.io
	@chmod +x dev-builder.sh
	@./dev-builder.sh status

builder-check: ## Verificar API keys y conectividad
	@chmod +x dev-builder.sh
	@./dev-builder.sh check

builder-test: ## Test de integración con Builder.io
	@chmod +x dev-builder.sh
	@./dev-builder.sh test

# ============================================
# Git y Deployment
# ============================================

git-status: ## Ver estado de git
	@git status

git-push: ## Hacer push a GitHub
	@echo "$(BLUE)[GIT]$(NC) Haciendo push..."
	@git push origin main

# ============================================
# Información
# ============================================

info: ## Mostrar información del proyecto
	@echo ""
	@echo "$(BLUE)============================================$(NC)"
	@echo "$(BLUE)  ConnecMaq - Información del Proyecto$(NC)"
	@echo "$(BLUE)============================================$(NC)"
	@echo ""
	@echo "$(GREEN)Backend:$(NC)"
	@echo "  Framework: Django 5.0+"
	@echo "  API: Django Rest Framework"
	@echo "  Base de datos: SQLite (dev) / PostgreSQL (prod)"
	@echo "  Autenticación: JWT"
	@echo "  WebSockets: Django Channels"
	@echo ""
	@echo "$(GREEN)Ubicaciones:$(NC)"
	@echo "  API:   http://localhost:8000/api/"
	@echo "  Admin: http://localhost:8000/admin/"
	@echo ""
	@echo "$(GREEN)Credenciales de prueba:$(NC)"
	@echo "  Constructor: constructor@test.com / TestPass123!"
	@echo "  Proveedor:   provider@test.com / TestPass123!"
	@echo ""
	@echo "$(GREEN)Comandos útiles:$(NC)"
	@echo "  make setup      - Setup completo"
	@echo "  make run        - Ejecutar servidor"
	@echo "  make test       - Ejecutar tests"
	@echo "  make help       - Ver todos los comandos"
	@echo ""

version: ## Mostrar versión de dependencias
	@echo "$(BLUE)[VERSION]$(NC) Versiones instaladas:"
	@$(ACTIVATE) && $(PYTHON) --version
	@$(ACTIVATE) && cd backend && $(PIP) list | grep -E "Django|djangorestframework|channels"

# Default target
.DEFAULT_GOAL := help

