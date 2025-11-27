# 🐍 Guía de Inicio del Backend Django

Esta guía te ayudará a iniciar el servidor backend de SIGOT.

## ⚠️ Error Común: `ERR_CONNECTION_REFUSED`

Si ves este error en el frontend:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
```

**Significa que el backend Django no está corriendo.** Sigue estos pasos para iniciarlo.

---

## 📋 Prerrequisitos

1. **Python 3.10+** instalado
2. **PostgreSQL con PostGIS** corriendo (o usar Docker)
3. **Redis** corriendo (opcional, para Channels)

---

## 🚀 Inicio Rápido

### Opción 1: Con Docker (Recomendado)

Si tienes `docker-compose.yml` configurado:

```bash
# Iniciar todos los servicios (PostgreSQL, Redis, Django)
docker-compose up
```

### Opción 2: Manual

#### 1. Crear y activar entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate
```

#### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 3. Configurar base de datos

**Opción A: Script automático (Recomendado)**

```bash
# Con Python (requiere psycopg2)
python setup_db.py

# O con Bash (requiere psql en PATH)
./setup_db.sh
```

**Opción B: Manual**

Asegúrate de que PostgreSQL esté corriendo y crea la base de datos:

```bash
# Conectarse a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE sigot;
\c sigot
CREATE EXTENSION postgis;
\q
```

#### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

#### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

#### 6. Iniciar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

---

## ✅ Verificar que el Backend está Corriendo

Abre en tu navegador:
- **API Root:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/

Si ves respuestas (aunque sean errores 404), el servidor está corriendo correctamente.

---

## 🔧 Configuración de CORS

El backend ya está configurado para permitir peticiones desde el frontend (`localhost:3000`).

Si necesitas cambiar los orígenes permitidos, edita `sigot/boot/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'django'"
- **Solución:** Activa el entorno virtual e instala dependencias: `pip install -r requirements.txt`

### Error: "could not connect to server"
- **Solución:** Verifica que PostgreSQL esté corriendo:
  ```bash
  # macOS/Linux
  brew services start postgresql
  
  # O con Docker
  docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgis/postgis
  ```

### Error: "relation does not exist"
- **Solución:** Ejecuta las migraciones: `python manage.py migrate`

### Error: CORS bloqueado en el navegador
- **Solución:** Verifica que `django-cors-headers` esté instalado y configurado en `settings.py`

---

## 📝 Variables de Entorno (Opcional)

Puedes crear un archivo `.env` en la raíz del proyecto:

```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
DB_NAME=sigot
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379
```

---

## 🎯 Próximos Pasos

Una vez que el backend esté corriendo:

1. Inicia el frontend: `cd frontend && npm run dev`
2. Abre http://localhost:3000
3. Prueba el registro y login

---

## 📚 Comandos Útiles

```bash
# Ver logs del servidor
python manage.py runserver --verbosity 2

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Shell de Django
python manage.py shell

# Ejecutar tests
pytest
```

