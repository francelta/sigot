# ⚡ Comandos Rápidos - ConnecMaq

Guía rápida de todos los comandos disponibles para trabajar con ConnecMaq.

---

## 🚀 Instalación Inicial

### Setup Automático (Recomendado)

**Unix/Mac/Linux:**
```bash
./setup.sh
```

**Windows:**
```batch
setup.bat
```

**Con Makefile:**
```bash
make setup
```

### Setup Manual

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
python manage.py migrate
python manage.py createsuperuser
python test_api.py
```

---

## 🔧 Comandos Make (Unix/Mac/Linux)

### Principales

```bash
make help              # Ver todos los comandos disponibles
make setup             # Setup completo (instalar + migrar + datos)
make install           # Solo instalar dependencias
make run               # Ejecutar servidor de desarrollo
make migrate           # Ejecutar migraciones
make test              # Ejecutar tests
```

### Desarrollo

```bash
make makemigrations    # Crear nuevas migraciones
make shell             # Abrir shell de Django
make dbshell           # Abrir shell de base de datos
make superuser         # Crear superusuario
make testdata          # Crear datos de prueba
make check             # Verificar proyecto (migraciones pendientes, etc)
```

### Limpieza

```bash
make clean             # Limpiar archivos temporales y caché
make clean-db          # Eliminar base de datos SQLite
make reset-db          # Resetear BD completa (eliminar + migrar + datos)
```

### Información

```bash
make info              # Mostrar información del proyecto
make version           # Mostrar versiones de dependencias
make showmigrations    # Ver estado de migraciones
```

---

## 🐍 Comandos Django (Manual)

### Servidor

```bash
# Activar entorno virtual (primero)
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate

# Ejecutar servidor
python manage.py runserver

# Servidor en otro puerto
python manage.py runserver 8001

# Servidor accesible desde la red
python manage.py runserver 0.0.0.0:8000
```

### Base de Datos

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Migrar app específica
python manage.py migrate api

# Ver SQL de migración
python manage.py sqlmigrate api 0001

# Ver estado de migraciones
python manage.py showmigrations

# Revertir migración
python manage.py migrate api 0001

# Flush DB (eliminar todos los datos)
python manage.py flush
```

### Usuarios

```bash
# Crear superusuario
python manage.py createsuperuser

# Cambiar password
python manage.py changepassword username
```

### Shell

```bash
# Shell de Django
python manage.py shell

# Shell Plus (si tienes django-extensions)
python manage.py shell_plus

# DB Shell
python manage.py dbshell
```

### Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app
python manage.py test api

# Tests específicos
python manage.py test api.tests.test_models

# Con pytest
pytest
pytest -v  # Verbose
pytest --cov=api  # Con coverage
pytest -k "test_machine"  # Tests que coincidan con el nombre
```

### Utilidades

```bash
# Verificar proyecto
python manage.py check

# Recolectar archivos estáticos
python manage.py collectstatic

# Limpiar sesiones expiradas
python manage.py clearsessions

# Crear datos de prueba (custom)
python test_api.py
```

---

## 📦 Comandos pip

```bash
# Instalar dependencias
pip install -r requirements.txt

# Actualizar pip
pip install --upgrade pip

# Instalar paquete específico
pip install nombre-paquete

# Actualizar paquete
pip install --upgrade nombre-paquete

# Listar paquetes instalados
pip list

# Mostrar info de paquete
pip show django

# Crear requirements.txt
pip freeze > requirements.txt

# Desinstalar paquete
pip uninstall nombre-paquete
```

---

## 🔍 Comandos Git

### Básicos

```bash
# Estado
git status

# Ver cambios
git diff

# Agregar archivos
git add .
git add archivo.py

# Commit
git commit -m "mensaje"

# Push
git push origin main

# Pull
git pull origin main

# Ver log
git log
git log --oneline
```

### Ramas

```bash
# Listar ramas
git branch

# Crear rama
git checkout -b feature/nueva-caracteristica

# Cambiar de rama
git checkout main

# Eliminar rama
git branch -d feature/nombre

# Merge
git merge feature/nombre
```

### Avanzado

```bash
# Ver remotes
git remote -v

# Agregar remote
git remote add upstream https://github.com/francelta/sigot.git

# Fetch de upstream
git fetch upstream

# Merge upstream
git merge upstream/main

# Stash cambios
git stash
git stash pop

# Revertir cambios
git checkout -- archivo.py
git reset HEAD archivo.py
```

---

## 🧪 Comandos de Testing

### Pytest

```bash
# Ejecutar tests
pytest

# Verbose
pytest -v

# Con coverage
pytest --cov=api

# Report de coverage
pytest --cov=api --cov-report=html

# Tests específicos
pytest api/tests/test_models.py
pytest api/tests/test_models.py::TestMachine
pytest -k "test_create"

# Stop en primer error
pytest -x

# Mostrar prints
pytest -s
```

---

## 📊 Comandos de Base de Datos

### SQLite (Desarrollo)

```bash
# Abrir base de datos
sqlite3 db.sqlite3

# En SQLite shell:
.tables                    # Ver tablas
.schema api_machine        # Ver schema de tabla
SELECT * FROM api_user;    # Query
.exit                      # Salir
```

### PostgreSQL (Producción)

```bash
# Conectar a PostgreSQL
psql -U usuario -d nombre_bd

# En psql:
\dt                        # Ver tablas
\d api_machine             # Describir tabla
SELECT * FROM api_user;    # Query
\q                         # Salir
```

---

## 🐳 Comandos Docker (Futuro)

```bash
# Build
docker-compose build

# Up
docker-compose up
docker-compose up -d  # Detached

# Down
docker-compose down

# Logs
docker-compose logs
docker-compose logs -f api  # Follow logs

# Ejecutar comando
docker-compose exec api python manage.py migrate

# Shell
docker-compose exec api python manage.py shell
```

---

## 🔥 Comandos One-Liner Útiles

### Setup Completo en Un Comando

**Unix/Mac:**
```bash
./setup.sh && cd backend && source venv/bin/activate && python manage.py runserver
```

**Windows:**
```batch
setup.bat && cd backend && venv\Scripts\activate && python manage.py runserver
```

### Reset Completo

```bash
cd backend && rm -f db.sqlite3 && python manage.py migrate && python test_api.py && python manage.py runserver
```

### Actualizar Proyecto

```bash
git pull origin main && cd backend && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate
```

### Ver Info Rápida

```bash
python manage.py showmigrations && python manage.py check && pip list | grep Django
```

---

## 📡 Comandos API (curl)

### Login

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "provider@test.com",
    "password": "TestPass123!"
  }'
```

### Listar Recursos

```bash
# Proveedores
curl http://localhost:8000/api/providers/

# Máquinas
curl http://localhost:8000/api/machines/

# Con autenticación
curl -H "Authorization: Bearer TU_TOKEN" \
  http://localhost:8000/api/machines/
```

### Crear Recurso

```bash
curl -X POST http://localhost:8000/api/machines/ \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Excavadora CAT",
    "category": "excavator",
    "price_per_hour": 50000
  }'
```

---

## 🎯 Atajos de Teclado (Útiles)

### En el Shell de Django

```python
Ctrl + D          # Salir
Ctrl + L          # Limpiar pantalla
Ctrl + C          # Interrumpir
↑ / ↓             # Historial de comandos
```

### En Terminal

```bash
Ctrl + C          # Detener proceso
Ctrl + Z          # Suspender proceso
Ctrl + R          # Buscar en historial
clear / Ctrl + L  # Limpiar pantalla
```

---

## 📝 Alias Útiles (Opcional)

Agrega estos a tu `~/.bashrc` o `~/.zshrc`:

```bash
# ConnecMaq aliases
alias cm='cd /ruta/a/sigot'
alias cmb='cd /ruta/a/sigot/backend'
alias cma='cd /ruta/a/sigot/backend && source venv/bin/activate'
alias cmrun='cd /ruta/a/sigot/backend && source venv/bin/activate && python manage.py runserver'
alias cmtest='cd /ruta/a/sigot/backend && source venv/bin/activate && pytest'
alias cmmigrate='cd /ruta/a/sigot/backend && source venv/bin/activate && python manage.py migrate'
alias cmshell='cd /ruta/a/sigot/backend && source venv/bin/activate && python manage.py shell'
```

Luego:
```bash
source ~/.bashrc  # o ~/.zshrc
cm                # Ve al proyecto
cmrun             # Ejecuta el servidor
```

---

## 💡 Tips

### Ver Todos los Comandos Make

```bash
make help
```

### Ver Endpoints de la API

```bash
# En el navegador:
http://localhost:8000/api/

# O con curl:
curl http://localhost:8000/api/
```

### Recargar Servidor Automáticamente

Django recarga automáticamente con cambios, pero si no:

```bash
# Linux/Mac
touch backend/config/wsgi.py

# O reinicia manualmente
Ctrl + C
python manage.py runserver
```

---

## 📚 Referencias Rápidas

- **Documentación:** Ver archivos `.md` en la raíz
- **API Endpoints:** `backend/API_ENDPOINTS.md`
- **Instalación:** `INSTALL.md`
- **Contribuir:** `CONTRIBUTING.md`

---

**¿Buscas algo específico?**

```bash
# Buscar en la documentación
grep -r "palabra" *.md

# Buscar comando make
make help | grep palabra
```

---

¡Guarda esta guía para referencia rápida! 🚀

