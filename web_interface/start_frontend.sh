#!/bin/bash

echo "🎨 ADVENTURE GAME - INSTALACIÓN FRONTEND REACT"
echo "=============================================="

# Cambiar al directorio del frontend
cd "$(dirname "$0")/frontend"

# Verificar si Node.js está instalado
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js/npm no está instalado"
    echo "💡 Instala Node.js desde: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js detectado: $(node --version)"
echo "✅ npm detectado: $(npm --version)"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo ""
echo "🚀 Iniciando servidor de desarrollo..."
echo "📊 Frontend se abrirá en: http://localhost:3000"
echo "🔌 Backend debe estar ejecutándose en: http://localhost:8001"
echo ""

# Iniciar servidor de desarrollo
npm run dev
