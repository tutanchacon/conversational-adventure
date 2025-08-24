# 🎨 Adventure Game - Frontend React

Frontend React profesional para el Adventure Game Web Interface.

## 🚀 Características

- ⚛️ **React 18** con Vite
- 🎨 **Material-UI** para componentes
- 📊 **Chart.js** para gráficos en tiempo real
- 🔌 **WebSocket** para actualizaciones live
- 📱 **Responsive Design**
- 🌙 **Tema Dark Mode** personalizado

## 📦 Instalación

### Windows
```bash
# Ejecutar el script de instalación
.\start_frontend.bat
```

### Linux/Mac
```bash
# Hacer ejecutable y ejecutar
chmod +x start_frontend.sh
./start_frontend.sh
```

### Manual
```bash
# Instalar dependencias
cd frontend
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 🌐 URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001

## 📊 Páginas Implementadas

- ✅ **Dashboard**: Métricas y gráficos en tiempo real
- ✅ **Backup Manager**: Gestión visual de backups
- 🚧 **System Logs**: Logs del sistema (próximamente)
- 🚧 **Analytics**: Analíticas avanzadas (próximamente)
- 🚧 **Settings**: Configuración (próximamente)

## 🔧 Desarrollo

```bash
# Modo desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

## 📁 Estructura

```
frontend/
├── src/
│   ├── components/          # Componentes reutilizables
│   │   └── Sidebar.jsx     # Sidebar de navegación
│   ├── pages/              # Páginas principales
│   │   ├── Dashboard.jsx   # Dashboard principal
│   │   ├── BackupManager.jsx # Gestión de backups
│   │   ├── SystemLogs.jsx  # Logs del sistema
│   │   ├── Analytics.jsx   # Analíticas
│   │   └── Settings.jsx    # Configuración
│   ├── services/           # Servicios de API
│   │   ├── api.js         # Cliente HTTP
│   │   └── websocket.js   # Cliente WebSocket
│   ├── App.jsx            # Componente principal
│   └── main.jsx           # Punto de entrada
├── package.json           # Dependencias
└── vite.config.js        # Configuración de Vite
```

## 🎯 Estado Actual

✅ **COMPLETADO**:
- Dashboard con métricas en tiempo real
- Gestión visual de backups
- WebSocket para actualizaciones live
- Tema dark profesional
- Navegación responsive

🔄 **EN DESARROLLO**:
- Sistema de logs
- Analíticas avanzadas
- Configuración del sistema

## 💡 Próximas Mejoras

- [ ] Autenticación visual
- [ ] Más tipos de gráficos
- [ ] Filtros avanzados
- [ ] Exportación de datos
- [ ] Notificaciones push
- [ ] Modo offline

## 🐛 Troubleshooting

### Error: Cannot connect to backend
- Verificar que el backend esté ejecutándose en puerto 8001
- Ejecutar: `python .\web_interface\backend\app\demo_server.py`

### Error: npm command not found
- Instalar Node.js desde: https://nodejs.org/

### Error: WebSocket connection failed
- Verificar configuración de proxy en `vite.config.js`
- Comprobar que no haya firewall bloqueando puertos

---

**Adventure Game v2.0 - Frontend React Dashboard** 🎨✨
