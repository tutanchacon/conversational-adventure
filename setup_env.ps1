# 🔧 CONFIGURACIÓN DE VARIABLES DE ENTORNO
# Archivo: setup_env.ps1

param([switch]$Permanent)

$ProjectPath = "D:\wamp64\www\conversational-adventure"
$VenvPath = "$ProjectPath\venv\Scripts"

Write-Host "🔧 Configurando variables de entorno..." -ForegroundColor Cyan

if ($Permanent) {
    # Configuración permanente (requiere permisos de administrador)
    Write-Host "⚠️  Configuración permanente - Requiere permisos de administrador" -ForegroundColor Yellow
    
    # Agregar al PATH del sistema
    $CurrentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($CurrentPath -notlike "*$VenvPath*") {
        [Environment]::SetEnvironmentVariable("PATH", "$CurrentPath;$VenvPath", "User")
        Write-Host "✅ Entorno virtual agregado al PATH del usuario" -ForegroundColor Green
    }
    
    # Crear variable para el proyecto
    [Environment]::SetEnvironmentVariable("ADVENTURE_GAME_PATH", $ProjectPath, "User")
    Write-Host "✅ Variable ADVENTURE_GAME_PATH configurada" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🔄 Reinicia PowerShell para aplicar los cambios" -ForegroundColor Yellow
    
} else {
    # Configuración temporal para la sesión actual
    $env:PATH = "$env:PATH;$VenvPath"
    $env:ADVENTURE_GAME_PATH = $ProjectPath
    Set-Location $ProjectPath
    
    # Activar entorno virtual
    & "$VenvPath\Activate.ps1"
    
    Write-Host "✅ Variables configuradas para la sesión actual" -ForegroundColor Green
    Write-Host "📁 Directorio cambiado a: $ProjectPath" -ForegroundColor Green
    Write-Host "🐍 Entorno virtual activado" -ForegroundColor Green
}

Write-Host ""
Write-Host "💡 Uso:" -ForegroundColor Cyan
Write-Host "   .\setup_env.ps1           - Configuración temporal"
Write-Host "   .\setup_env.ps1 -Permanent - Configuración permanente"
