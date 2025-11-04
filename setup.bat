@echo off
REM ============================================
REM ConnecMaq - Script de Setup Automático (Windows)
REM ============================================

echo ============================================
echo   ConnecMaq - Setup Automatico
echo ============================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "backend\" (
    echo [ERROR] No se encontro el directorio 'backend'. Ejecuta este script desde la raiz del proyecto.
    exit /b 1
)

REM 1. Verificar Python
echo [PASO] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado. Por favor, instalalo primero.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% encontrado

REM 2. Crear entorno virtual
echo [PASO] Creando entorno virtual...
cd backend

if exist "venv\" (
    echo [!] El entorno virtual ya existe. Usando el existente...
) else (
    python -m venv venv
    echo [OK] Entorno virtual creado
)

REM 3. Activar entorno virtual
echo [PASO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM 4. Actualizar pip
echo [PASO] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado

REM 5. Instalar dependencias
echo [PASO] Instalando dependencias de requirements.txt...
pip install -r requirements.txt
echo [OK] Dependencias instaladas

REM 6. Crear archivo .env si no existe
echo [PASO] Configurando variables de entorno...
if not exist ".env" (
    if exist "env.example" (
        copy env.example .env
        echo [OK] Archivo .env creado desde env.example
        echo [!] Por favor, edita el archivo .env con tus configuraciones
    ) else (
        echo [!] Creando .env basico...
        (
            echo # Django
            echo SECRET_KEY=django-insecure-change-this-in-production-windows
            echo DEBUG=True
            echo ALLOWED_HOSTS=localhost,127.0.0.1
            echo.
            echo # Database (SQLite por defecto para desarrollo^)
            echo DATABASE_URL=sqlite:///db.sqlite3
            echo.
            echo # CORS
            echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
            echo.
            echo # Redis (para Channels - opcional en desarrollo^)
            echo REDIS_URL=redis://localhost:6379
        ) > .env
        echo [OK] Archivo .env basico creado
    )
) else (
    echo [OK] Archivo .env ya existe
)

REM 7. Ejecutar migraciones
echo [PASO] Ejecutando migraciones de base de datos...
python manage.py migrate
echo [OK] Migraciones completadas

REM 8. Crear superusuario (opcional)
echo [PASO] Quieres crear un superusuario ahora? (S/N^)
set /p CREATE_SUPER="Respuesta: "
if /i "%CREATE_SUPER%"=="S" (
    python manage.py createsuperuser
    echo [OK] Superusuario creado
) else (
    echo [!] Puedes crear un superusuario mas tarde con: python manage.py createsuperuser
)

REM 9. Crear datos de prueba (opcional)
echo [PASO] Quieres crear datos de prueba? (S/N^)
set /p CREATE_DATA="Respuesta: "
if /i "%CREATE_DATA%"=="S" (
    if exist "test_api.py" (
        python test_api.py
        echo [OK] Datos de prueba creados
    ) else (
        echo [!] No se encontro test_api.py
    )
) else (
    echo [!] Puedes crear datos de prueba mas tarde con: python test_api.py
)

REM 10. Resumen final
echo.
echo ============================================
echo   SETUP COMPLETADO EXITOSAMENTE
echo ============================================
echo.
echo Credenciales de prueba:
echo   Constructor: constructor@test.com / TestPass123!
echo   Proveedor:   provider@test.com / TestPass123!
echo.
echo Para ejecutar el servidor:
echo   cd backend
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Accede a:
echo   - API:   http://localhost:8000/api/
echo   - Admin: http://localhost:8000/admin/
echo.
echo ============================================

pause

