# 📦 Guía de Instalación - ConnecMaq

Esta guía te llevará paso a paso por la instalación completa del proyecto **ConnecMaq**.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Instalación Automática](#-instalación-automática)
- [Instalación Manual](#-instalación-manual)
- [Verificación](#-verificación)
- [Problemas Comunes](#-problemas-comunes)

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Obligatorio
- **Python 3.10+** ([Descargar](https://www.python.org/downloads/))
- **Git** ([Descargar](https://git-scm.com/downloads))

### Opcional (para producción)
- **PostgreSQL 13+** ([Descargar](https://www.postgresql.org/download/))
- **Redis** (para WebSocket chat) ([Descargar](https://redis.io/download))

### Verificar Instalación

```bash
# Verificar Python
python3 --version  # Debe ser 3.10 o superior

# Verificar Git
git --version

# Verificar pip
pip --version
```

---

## 🚀 Instalación Automática

### Opción 1: Script de Setup (Recomendado)

**Para Unix/Mac/Linux:**
```bash
# 1. Clonar el repositorio
git clone https://github.com/francelta/sigot.git
cd sigot

# 2. Dar permisos de ejecución
chmod +x setup.sh

# 3. Ejecutar setup
./setup.sh
```

**Para Windows:**
```batch
REM 1. Clonar el repositorio
git clone https://github.com/francelta/sigot.git
cd sigot

REM 2. Ejecutar setup
setup.bat
```

El script automáticamente:
- ✅ Crea el entorno virtual
- ✅ Instala todas las dependencias
- ✅ Configura el archivo `.env`
- ✅ Ejecuta las migraciones
- ✅ Opcionalmente crea superusuario
- ✅ Opcionalmente crea datos de prueba

### Opción 2: Usando Makefile (Unix/Mac/Linux)

```bash
# Clonar repositorio
git clone https://github.com/francelta/sigot.git
cd sigot

# Setup completo
make setup

# O paso por paso
make install
make migrate
make testdata
```

---

## 🛠️ Instalación Manual

Si prefieres hacerlo paso a paso manualmente:

### 1. Clonar el Repositorio

```bash
git clone https://github.com/francelta/sigot.git
cd sigot
```

### 2. Crear Entorno Virtual

**Unix/Mac/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```batch
cd backend
python -m venv venv
venv\Scripts\activate
```

### 3. Actualizar pip

```bash
pip install --upgrade pip
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

**Unix/Mac/Linux:**
```bash
cp env.example .env
nano .env  # O usa tu editor preferido
```

**Windows:**
```batch
copy env.example .env
notepad .env
```

**Configuración mínima del `.env`:**
```env
# Django
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite por defecto)
DATABASE_URL=sqlite:///db.sqlite3

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Redis (opcional para desarrollo)
REDIS_URL=redis://localhost:6379
```

### 6. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 7. Crear Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla.

### 8. Crear Datos de Prueba (Opcional)

```bash
python test_api.py
```

Esto crea:
- 2 usuarios (constructor y proveedor)
- Perfiles completos
- 3 máquinas de ejemplo
- 1 ChatRoom de prueba

### 9. Ejecutar Servidor

```bash
python manage.py runserver
```

---

## ✅ Verificación

### 1. Verificar que el servidor está corriendo

Abre tu navegador en:
- **API:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/

Deberías ver:
- La página de la API de Django REST Framework
- El panel de administración de Django

### 2. Probar Autenticación

**Usando curl:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "provider@test.com",
    "password": "TestPass123!"
  }'
```

**Usando Postman:**
1. POST a `http://localhost:8000/api/token/`
2. Body (JSON):
   ```json
   {
     "email": "provider@test.com",
     "password": "TestPass123!"
   }
   ```
3. Deberías recibir tokens JWT

### 3. Credenciales de Prueba

Si ejecutaste `test_api.py`, tienes estas credenciales:

| Tipo | Email | Password |
|------|-------|----------|
| Constructor | constructor@test.com | TestPass123! |
| Proveedor | provider@test.com | TestPass123! |

### 4. Verificar Endpoints

**Listar Proveedores:**
```bash
curl http://localhost:8000/api/providers/
```

**Listar Máquinas:**
```bash
curl http://localhost:8000/api/machines/
```

---

## 🔍 Problemas Comunes

### Error: "No module named 'django'"

**Solución:**
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate  # Unix/Mac
# o
venv\Scripts\activate  # Windows

# Reinstala dependencias
pip install -r requirements.txt
```

### Error: "SECRET_KEY not found"

**Solución:**
```bash
# Verifica que existe el archivo .env
ls -la .env

# Si no existe, créalo
cp env.example .env

# Edita y agrega tu SECRET_KEY
```

### Error: "Table doesn't exist"

**Solución:**
```bash
# Ejecuta las migraciones
python manage.py migrate
```

### Error: "Address already in use"

**Solución:**
```bash
# El puerto 8000 está ocupado. Usa otro puerto:
python manage.py runserver 8001
```

### Error al instalar Pillow (Windows)

**Solución:**
1. Descarga Visual C++ Build Tools
2. O instala Pillow desde binarios:
   ```bash
   pip install --upgrade Pillow
   ```

### Error: "Permission denied" (setup.sh)

**Solución:**
```bash
chmod +x setup.sh
```

---

## 🎯 Siguientes Pasos

Una vez instalado, puedes:

1. **Explorar la API:** http://localhost:8000/api/
2. **Acceder al Admin:** http://localhost:8000/admin/
3. **Leer la Documentación:**
   - [BACKEND_COMPLETO.md](BACKEND_COMPLETO.md)
   - [API_ENDPOINTS.md](backend/API_ENDPOINTS.md)
   - [PERFILES_COMPLETO.md](PERFILES_COMPLETO.md)
4. **Ejecutar Tests:**
   ```bash
   pytest
   # o
   make test
   ```

---

## 📞 Soporte

Si encuentras problemas:

1. **Revisa la documentación:** Todos los archivos `.md`
2. **Busca en Issues:** https://github.com/francelta/sigot/issues
3. **Crea un Issue:** Si no encuentras solución

---

## 🔄 Actualizar el Proyecto

Para obtener las últimas actualizaciones:

```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
```

---

## 🧹 Desinstalación

Para eliminar completamente el proyecto:

```bash
# Desactivar entorno virtual
deactivate

# Eliminar directorio
cd ..
rm -rf sigot
```

---

**¿Listo para empezar?** 🚀

```bash
# Opción rápida
./setup.sh && cd backend && source venv/bin/activate && python manage.py runserver
```

¡Disfruta desarrollando con ConnecMaq! 🏗️

