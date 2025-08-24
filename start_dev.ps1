# 🚀 SCRIPT DE DESARROLLO AUTOMÁTICO - PowerShell
# Archivo: start_dev.ps1

param(
    [string]$Action = "start",
    [switch]$Server,
    [switch]$Test,
    [switch]$Clean
)

# Configuración
$ProjectPath = "D:\wamp64\www\conversational-adventure"
$VenvPath = "$ProjectPath\venv"
$RequirementsFile = "$ProjectPath\requirements.txt"

# Colores para output
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Info($Message) { Write-ColorOutput Cyan "ℹ️  $Message" }
function Write-Success($Message) { Write-ColorOutput Green "✅ $Message" }
function Write-Warning($Message) { Write-ColorOutput Yellow "⚠️  $Message" }
function Write-Error($Message) { Write-ColorOutput Red "❌ $Message" }

# Banner
Write-Host ""
Write-ColorOutput Magenta "========================================================"
Write-ColorOutput Magenta "🎮 ADVENTURE GAME - ENTORNO DE DESARROLLO AUTOMÁTICO"
Write-ColorOutput Magenta "========================================================"
Write-Host ""

# Cambiar al directorio del proyecto
Set-Location $ProjectPath
Write-Info "Directorio del proyecto: $ProjectPath"

# Verificar/Crear entorno virtual
if (-not (Test-Path "$VenvPath\Scripts\Activate.ps1")) {
    Write-Warning "Entorno virtual no encontrado"
    Write-Info "Creando entorno virtual..."
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Entorno virtual creado exitosamente"
    } else {
        Write-Error "Error creando entorno virtual"
        exit 1
    }
}

# Activar entorno virtual
Write-Info "Activando entorno virtual..."
& "$VenvPath\Scripts\Activate.ps1"

# Verificar dependencias
Write-Info "Verificando dependencias..."
$HasFastAPI = pip list | Select-String "fastapi"
if (-not $HasFastAPI) {
    Write-Warning "Dependencias faltantes detectadas"
    if (Test-Path $RequirementsFile) {
        Write-Info "Instalando dependencias desde requirements.txt..."
        pip install -r $RequirementsFile
    } else {
        Write-Info "Instalando dependencias básicas..."
        pip install fastapi uvicorn websockets aiohttp
    }
}

# Mostrar información del entorno
Write-Host ""
Write-Success "🎯 Entorno de desarrollo listo"
Write-Host "📁 Directorio: $(Get-Location)"
Write-Host "🐍 Python: $(python --version)"
Write-Host "📦 Pip: $(pip --version)"
Write-Host ""

# Ejecutar acción específica
switch ($Action.ToLower()) {
    "server" {
        Write-Info "🚀 Iniciando servidor de desarrollo..."
        python web_interface\backend\app\main.py
    }
    "test" {
        Write-Info "🧪 Ejecutando tests..."
        python -m pytest tests/ -v
    }
    "clean" {
        Write-Warning "🧹 Limpiando archivos temporales..."
        Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
        Write-Success "Limpieza completada"
    }
    default {
        Write-Host "💡 Comandos disponibles:"
        Write-Host "   • python main.py                    - Servidor principal"
        Write-Host "   • python test_*.py                  - Ejecutar tests"
        Write-Host "   • pip install [paquete]             - Instalar dependencias"
        Write-Host "   • deactivate                        - Salir del entorno virtual"
        Write-Host ""
        Write-Host "🔧 Opciones del script:"
        Write-Host "   • .\start_dev.ps1 -Action server   - Iniciar servidor automáticamente"
        Write-Host "   • .\start_dev.ps1 -Action test     - Ejecutar tests automáticamente"
        Write-Host "   • .\start_dev.ps1 -Action clean    - Limpiar archivos temporales"
    }
}

Write-Host ""
Write-ColorOutput Magenta "========================================================"
