# 🎮 PERFIL PERSONALIZADO DE POWERSHELL PARA ADVENTURE GAME
# Guarda este archivo como: $PROFILE (ejecuta echo $PROFILE para ver la ruta)

# Función para inicializar automáticamente el proyecto Adventure Game
function Start-AdventureGame {
    param(
        [switch]$Force,
        [string]$Action = "interactive"
    )
    
    $ProjectPath = "D:\wamp64\www\conversational-adventure"
    $VenvPath = "$ProjectPath\venv\Scripts\Activate.ps1"
    
    # Verificar si estamos en el directorio correcto
    $CurrentLocation = Get-Location
    $InProjectDir = $CurrentLocation.Path -like "*conversational-adventure*"
    
    if ($InProjectDir -or $Force) {
        Write-Host "🎮 Inicializando Adventure Game..." -ForegroundColor Magenta
        
        # Cambiar al directorio del proyecto
        if (-not $InProjectDir) {
            Set-Location $ProjectPath
            Write-Host "📁 Cambiado a: $ProjectPath" -ForegroundColor Green
        }
        
        # Activar entorno virtual si existe
        if (Test-Path $VenvPath) {
            & $VenvPath
            Write-Host "🐍 Entorno virtual activado" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Entorno virtual no encontrado en: $VenvPath" -ForegroundColor Yellow
        }
        
        # Mostrar información útil
        Write-Host ""
        Write-Host "🚀 Adventure Game - Entorno Listo" -ForegroundColor Cyan
        Write-Host "   📁 Proyecto: $ProjectPath" -ForegroundColor White
        Write-Host "   🐍 Python: $(python --version 2>$null)" -ForegroundColor White
        Write-Host ""
        Write-Host "💡 Comandos útiles:" -ForegroundColor Yellow
        Write-Host "   Start-Server    - Iniciar servidor de desarrollo"
        Write-Host "   Run-Tests       - Ejecutar tests"
        Write-Host "   Open-Project    - Abrir en VS Code"
        Write-Host ""
        
        return $true
    }
    
    return $false
}

# Función para iniciar el servidor
function Start-Server {
    param([string]$Port = "8000")
    
    if (Test-Path "web_interface\backend\app\main.py") {
        Write-Host "🚀 Iniciando servidor en puerto $Port..." -ForegroundColor Green
        python web_interface\backend\app\main.py
    } else {
        Write-Host "❌ Archivo main.py no encontrado" -ForegroundColor Red
    }
}

# Función para ejecutar tests
function Run-Tests {
    param([string]$Pattern = "test_*.py")
    
    Write-Host "🧪 Ejecutando tests: $Pattern" -ForegroundColor Cyan
    Get-ChildItem -Name $Pattern | ForEach-Object {
        Write-Host "📝 Ejecutando: $_" -ForegroundColor Yellow
        python $_
    }
}

# Función para abrir el proyecto en VS Code
function Open-Project {
    if (Get-Command code -ErrorAction SilentlyContinue) {
        code .
        Write-Host "📝 Abriendo proyecto en VS Code..." -ForegroundColor Green
    } else {
        Write-Host "❌ VS Code no encontrado en PATH" -ForegroundColor Red
    }
}

# Alias útiles
Set-Alias -Name ag -Value Start-AdventureGame
Set-Alias -Name server -Value Start-Server
Set-Alias -Name tests -Value Run-Tests
Set-Alias -Name proj -Value Open-Project

# Auto-inicialización cuando PowerShell se abre en el directorio del proyecto
$CurrentPath = Get-Location
if ($CurrentPath.Path -like "*conversational-adventure*") {
    Write-Host ""
    Write-Host "🎮 Directorio Adventure Game detectado" -ForegroundColor Magenta
    Write-Host "💡 Ejecuta 'ag' para inicializar el entorno automáticamente" -ForegroundColor Yellow
    Write-Host ""
}

# Mensaje de bienvenida personalizado
Write-Host "🎮 Adventure Game Profile Loaded" -ForegroundColor Magenta
Write-Host "   ag      - Inicializar Adventure Game" -ForegroundColor Cyan
Write-Host "   server  - Iniciar servidor" -ForegroundColor Cyan  
Write-Host "   tests   - Ejecutar tests" -ForegroundColor Cyan
Write-Host "   proj    - Abrir en VS Code" -ForegroundColor Cyan
