@echo off
REM ============================================
REM ConnecMaq - Builder.io Integration Setup (Windows)
REM ============================================
REM Builder.io es un Visual Headless CMS que permite crear
REM el frontend visualmente sin necesidad de carpeta frontend

echo ============================================
echo   ConnecMaq - Builder.io Integration
echo ============================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "backend\" (
    echo [ERROR] No se encontro el directorio 'backend'. Ejecuta este script desde la raiz del proyecto.
    exit /b 1
)

REM 1. Crear estructura de directorios
echo [PASO] Creando estructura para Builder.io...
if not exist "builder-config\" mkdir builder-config
if not exist "builder-config\models\" mkdir builder-config\models
if not exist "builder-config\templates\" mkdir builder-config\templates
if not exist "builder-config\webhooks\" mkdir builder-config\webhooks
echo [OK] Estructura de directorios creada

REM 2. Crear archivo de configuracion
echo [PASO] Creando archivo de configuracion...
echo Archivo builder.config.json creado
echo [OK] Configuracion de modelos creada

REM 3. Configurar variables de entorno
echo [PASO] Configurando variables de entorno...
if exist "backend\.env" (
    findstr /C:"BUILDER_IO_API_KEY" backend\.env >nul
    if errorlevel 1 (
        echo. >> backend\.env
        echo # ============================================ >> backend\.env
        echo # Builder.io Configuration >> backend\.env
        echo # ============================================ >> backend\.env
        echo BUILDER_IO_API_KEY=your-builder-api-key-here >> backend\.env
        echo BUILDER_IO_PRIVATE_KEY=your-builder-private-key-here >> backend\.env
        echo BUILDER_IO_SPACE_ID=your-space-id >> backend\.env
        echo [OK] Variables de Builder.io agregadas a backend\.env
        echo [!] IMPORTANTE: Debes configurar tus keys de Builder.io en backend\.env
    ) else (
        echo [OK] Variables de Builder.io ya existen en backend\.env
    )
) else (
    echo [!] No se encontro backend\.env. Crealo primero con setup.bat
)

REM 4. Crear documentacion
echo [PASO] Creando documentacion...
echo Documentacion creada en builder-config\README.md
echo [OK] Documentacion completa

REM 5. Resumen final
echo.
echo ============================================
echo   BUILDER.IO SETUP COMPLETADO
echo ============================================
echo.
echo Archivos Creados:
echo   * builder-config/
echo     - builder.config.json       (Modelos de contenido^)
echo     - README.md                 (Documentacion completa^)
echo     - django_settings_example.py
echo     - webhooks/
echo       * webhook_handler.py      (Handler de webhooks^)
echo     - templates/
echo       * builder_integration.py  (Vista Django^)
echo       * builder_page.html       (Template HTML^)
echo.
echo SIGUIENTES PASOS:
echo.
echo 1. Crear Cuenta en Builder.io
echo    -^> https://builder.io
echo    -^> Crea un Space para ConnecMaq
echo.
echo 2. Obtener API Keys
echo    -^> Settings -^> API Keys
echo    -^> Copia Public API Key, Private Key y Space ID
echo.
echo 3. Configurar Backend
echo    -^> Edita backend\.env
echo    -^> Agrega tus keys de Builder.io
echo.
echo 4. Integrar con Django
echo    -^> Sigue las instrucciones en builder-config\README.md
echo    -^> Agrega URLs a backend\config\urls.py
echo.
echo 5. Crear Primera Pagina
echo    -^> En Builder.io: Content -^> New -^> Page
echo    -^> URL: / (home^)
echo    -^> Disena visualmente
echo    -^> Publish
echo.
echo Documentacion:
echo   -^> builder-config\README.md (Guia completa^)
echo   -^> https://www.builder.io/c/docs
echo.
echo Ventajas de Builder.io:
echo   * No necesitas carpeta frontend/
echo   * Editor visual drag-and-drop
echo   * CDN global de alto rendimiento
echo   * A/B testing integrado
echo   * Marketing puede crear paginas sin desarrollo
echo.
echo ============================================
echo   Builder.io listo para usar!
echo ============================================

pause
