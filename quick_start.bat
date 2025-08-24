@echo off
REM 🎮 ACCESO DIRECTO INTELIGENTE PARA ADVENTURE GAME
REM Este archivo debe guardarse con extensión .bat

REM Configuración
set PROJECT_PATH=D:\wamp64\www\conversational-adventure
set VENV_PATH=%PROJECT_PATH%\venv\Scripts

REM Banner
echo.
echo ========================================================
echo 🎮 ADVENTURE GAME - ACCESO DIRECTO INTELIGENTE
echo ========================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%PROJECT_PATH%"
echo 📁 Directorio: %CD%

REM Activar entorno virtual
if exist "%VENV_PATH%\activate.bat" (
    echo 🐍 Activando entorno virtual...
    call "%VENV_PATH%\activate.bat"
    echo ✅ Entorno virtual activado
) else (
    echo ⚠️  Entorno virtual no encontrado
    echo 🔧 ¿Deseas crearlo? (S/N)
    set /p CREATE_VENV=
    if /i "%CREATE_VENV%"=="S" (
        echo 🔄 Creando entorno virtual...
        python -m venv venv
        call "%VENV_PATH%\activate.bat"
        echo 📦 Instalando dependencias...
        pip install -r requirements.txt
        echo ✅ Entorno configurado
    )
)

echo.
echo 💡 Opciones disponibles:
echo    1. Iniciar servidor de desarrollo
echo    2. Ejecutar tests
echo    3. Terminal interactivo
echo    4. Abrir en VS Code
echo    5. Salir
echo.

:MENU
set /p CHOICE=🎯 Selecciona una opción (1-5): 

if "%CHOICE%"=="1" (
    echo 🚀 Iniciando servidor...
    python web_interface\backend\app\main.py
    goto MENU
)

if "%CHOICE%"=="2" (
    echo 🧪 Ejecutando tests...
    for %%f in (test_*.py) do (
        echo 📝 Ejecutando: %%f
        python %%f
    )
    pause
    goto MENU
)

if "%CHOICE%"=="3" (
    echo 💻 Abriendo terminal interactivo...
    echo 💡 El entorno virtual ya está activado
    echo 💡 Usa 'deactivate' para salir del entorno virtual
    cmd /k
)

if "%CHOICE%"=="4" (
    echo 📝 Abriendo en VS Code...
    code .
    goto MENU
)

if "%CHOICE%"=="5" (
    echo 👋 ¡Hasta luego!
    exit /b
)

echo ❌ Opción no válida
goto MENU
