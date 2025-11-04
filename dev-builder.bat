@echo off
REM ============================================
REM ConnecMaq - Builder.io Dev Commands (Windows)
REM ============================================

setlocal enabledelayedexpansion

:menu
cls
echo ============================================
echo   ConnecMaq - Builder.io Dev Commands
echo ============================================
echo.
echo Comandos disponibles:
echo.
echo Configuracion:
echo   1. status     - Ver estado de la configuracion
echo   2. check      - Verificar API keys y conectividad
echo   3. config     - Ver configuracion actual
echo.
echo Desarrollo:
echo   4. preview    - Configurar preview URL local
echo   5. models     - Listar modelos configurados
echo   6. test       - Test de integracion
echo.
echo Documentacion:
echo   7. docs       - Abrir documentacion local
echo   8. help       - Ayuda rapida
echo.
echo Utilidades:
echo   9. logs       - Ver logs de webhooks
echo  10. clean      - Limpiar cache
echo.
echo   0. Salir
echo.

set /p choice="Selecciona una opcion: "

if "%choice%"=="1" goto status
if "%choice%"=="2" goto check
if "%choice%"=="3" goto config
if "%choice%"=="4" goto preview
if "%choice%"=="5" goto models
if "%choice%"=="6" goto test
if "%choice%"=="7" goto docs
if "%choice%"=="8" goto help
if "%choice%"=="9" goto logs
if "%choice%"=="10" goto clean
if "%choice%"=="0" goto exit

echo [ERROR] Opcion invalida
pause
goto menu

REM ============================================
REM 1. Ver estado
REM ============================================
:status
cls
echo ============================================
echo   Estado de Builder.io
echo ============================================
echo.

echo Estructura de archivos:
if exist "builder-config\" (
    echo [OK] builder-config\ existe
    
    if exist "builder-config\builder.config.json" (
        echo [OK] builder.config.json
    ) else (
        echo [ERROR] builder.config.json no encontrado
    )
    
    if exist "builder-config\README.md" (
        echo [OK] README.md
    ) else (
        echo [ERROR] README.md no encontrado
    )
    
    if exist "builder-config\webhooks\" (
        echo [OK] webhooks\
    ) else (
        echo [ERROR] webhooks\ no encontrado
    )
) else (
    echo [ERROR] builder-config\ no existe
    echo [!] Ejecuta: setup-builder.bat
)

echo.
echo Variables de entorno:
if exist "backend\.env" (
    findstr /C:"BUILDER_IO_API_KEY" backend\.env >nul
    if !errorlevel!==0 (
        echo [OK] BUILDER_IO_API_KEY configurado
    ) else (
        echo [ERROR] BUILDER_IO_API_KEY no encontrado
    )
    
    findstr /C:"BUILDER_IO_PRIVATE_KEY" backend\.env >nul
    if !errorlevel!==0 (
        echo [OK] BUILDER_IO_PRIVATE_KEY configurado
    ) else (
        echo [ERROR] BUILDER_IO_PRIVATE_KEY no encontrado
    )
) else (
    echo [ERROR] backend\.env no encontrado
)

echo.
echo Backend Django:
python --version >nul 2>&1
if !errorlevel!==0 (
    echo [OK] Python instalado
) else (
    echo [ERROR] Python no encontrado
)

if exist "backend\manage.py" (
    echo [OK] Django project encontrado
) else (
    echo [ERROR] Django project no encontrado
)

echo.
pause
goto menu

REM ============================================
REM 2. Verificar API keys
REM ============================================
:check
cls
echo ============================================
echo   Verificacion de Builder.io
echo ============================================
echo.

echo [INFO] Verificando conectividad con Builder.io...
echo.
echo [!] Verificacion manual requerida:
echo   1. Ve a https://builder.io
echo   2. Inicia sesion
echo   3. Ve a Settings -^> API Keys
echo   4. Verifica que tu API Key funcione
echo.

pause
goto menu

REM ============================================
REM 3. Ver configuracion
REM ============================================
:config
cls
echo ============================================
echo   Configuracion de Builder.io
echo ============================================
echo.

echo API Keys:
if exist "backend\.env" (
    for /f "tokens=2 delims==" %%a in ('findstr /C:"BUILDER_IO_API_KEY" backend\.env 2^>nul') do (
        if "%%a"=="your-builder-api-key-here" (
            echo   BUILDER_IO_API_KEY: [NO CONFIGURADO]
        ) else (
            echo   BUILDER_IO_API_KEY: %%a
        )
    )
    
    for /f "tokens=2 delims==" %%a in ('findstr /C:"BUILDER_IO_PRIVATE_KEY" backend\.env 2^>nul') do (
        echo   BUILDER_IO_PRIVATE_KEY: (oculto^)
    )
    
    for /f "tokens=2 delims==" %%a in ('findstr /C:"BUILDER_IO_SPACE_ID" backend\.env 2^>nul') do (
        echo   BUILDER_IO_SPACE_ID: %%a
    )
) else (
    echo [ERROR] backend\.env no encontrado
)

echo.
if exist "builder-config\builder.config.json" (
    echo Modelos configurados:
    findstr /C:"name" builder-config\builder.config.json
)

echo.
pause
goto menu

REM ============================================
REM 4. Preview URL
REM ============================================
:preview
cls
echo ============================================
echo   Preview URL Local
echo ============================================
echo.
echo Para usar preview local en Builder.io:
echo.
echo 1. Inicia tu servidor Django:
echo    cd backend
echo    python manage.py runserver
echo.
echo 2. En Builder.io editor:
echo    Settings (configuracion^) -^> Preview URLs
echo.
echo 3. Agrega estas URLs:
echo    http://localhost:8000
echo    http://127.0.0.1:8000
echo.
echo 4. Ahora puedes hacer preview en tiempo real
echo.
echo [!] Asegurate que el servidor Django este corriendo
echo.
pause
goto menu

REM ============================================
REM 5. Listar modelos
REM ============================================
:models
cls
echo ============================================
echo   Modelos de Builder.io
echo ============================================
echo.

if exist "builder-config\builder.config.json" (
    echo Modelos disponibles:
    echo.
    type builder-config\builder.config.json | findstr /C:"name" /C:"kind" /C:"description"
) else (
    echo [ERROR] builder.config.json no encontrado
    echo [!] Ejecuta: setup-builder.bat
)

echo.
pause
goto menu

REM ============================================
REM 6. Test de integracion
REM ============================================
:test
cls
echo ============================================
echo   Test de Integracion
echo ============================================
echo.

echo Test 1: Verificar estructura
if exist "builder-config\" (
    echo [OK] Estructura de Builder.io existe
) else (
    echo [ERROR] Estructura no encontrada
    goto test_end
)

echo.
echo Test 2: Verificar configuracion
if exist "backend\.env" (
    echo [OK] Archivo .env existe
) else (
    echo [ERROR] Archivo .env no encontrado
    goto test_end
)

echo.
echo Test 3: Verificar webhook endpoint
findstr /C:"builder_webhook" backend\config\urls.py >nul 2>&1
if !errorlevel!==0 (
    echo [OK] Webhook endpoint configurado
) else (
    echo [!] Webhook endpoint no configurado
    echo [INFO] Agrega el endpoint segun builder-config\README.md
)

:test_end
echo.
echo Tests completados
echo.
pause
goto menu

REM ============================================
REM 7. Documentacion
REM ============================================
:docs
cls
if exist "builder-config\README.md" (
    type builder-config\README.md | more
) else (
    echo [ERROR] README.md no encontrado
    echo [!] Ejecuta: setup-builder.bat
)

echo.
pause
goto menu

REM ============================================
REM 8. Ayuda
REM ============================================
:help
cls
echo ============================================
echo   Ayuda Rapida
echo ============================================
echo.
echo Primeros pasos:
echo   1. Ejecutar setup:     setup-builder.bat
echo   2. Crear cuenta:       https://builder.io
echo   3. Obtener API key:    Builder.io -^> Settings -^> API Keys
echo   4. Configurar .env:    backend\.env
echo   5. Crear pagina:       Builder.io -^> Content -^> New
echo.
echo Comandos utiles:
echo   dev-builder.bat        - Menu interactivo
echo.
echo Recursos:
echo   Docs local:    builder-config\README.md
echo   Docs online:   https://www.builder.io/c/docs
echo   Support:       https://www.builder.io/c/support
echo.
echo URLs importantes:
echo   Dashboard:     https://builder.io/content
echo   API Docs:      https://www.builder.io/c/docs/api
echo.
pause
goto menu

REM ============================================
REM 9. Logs
REM ============================================
:logs
cls
echo ============================================
echo   Logs de Builder.io
echo ============================================
echo.

if exist "backend\logs\builder_webhooks.log" (
    echo Ultimos logs:
    echo.
    type backend\logs\builder_webhooks.log
) else (
    echo [!] No hay logs de webhooks aun
    echo [INFO] Los logs apareceran cuando recibas webhooks de Builder.io
)

echo.
pause
goto menu

REM ============================================
REM 10. Limpiar cache
REM ============================================
:clean
cls
echo ============================================
echo   Limpiar Cache
echo ============================================
echo.

echo Limpiando archivos temporales...

REM Limpiar Python cache
for /d /r "builder-config" %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q "builder-config\*.pyc" 2>nul

echo [OK] Cache limpiado

echo.
pause
goto menu

REM ============================================
REM Salir
REM ============================================
:exit
echo.
echo Hasta luego!
exit /b 0

