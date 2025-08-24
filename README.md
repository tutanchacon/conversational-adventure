# 🎮 Adventure Game v2.0 - Sistema de Memoria Perfecta + Web Interface

Un juego de aventura conversacional profesional que implemen├── 🧠 Perfect Memory System (├── 🔗 MCP Integration (IMPLEMENTADO)
│   ├── 🌍 World Context Provider
│   ├── 📈 Player Analytics  
│   ├── 🎯 Smart Context Generation
│   └── 🔍 Semantic Search (ChromaDB) 1)
│   ├── 📊 SQLite Database (estado actual)
│   ├── 📝 Event Sourcing (historial completo)
│   ├── 🔍 Temporal Queries
│   ├── 🔍 Vector Search (ChromaDB + embeddings)
│   └── 💾 Automated Backup System
│       ├── ⏰ Scheduled backups (every 6h)
│       ├── 🗂️ Retention policy (48 backups)
│       ├── ✅ Integrity validation
│       └── 🔄 Restore capabilitiesistema de memoria perfecta** usando Event Sourcing y **una interfaz web completa** para administración. **La IA nunca olvida nada**: donde dejaste el martillo, hace cuánto tiempo, si se oxidó, etc.

## 🌟 Características Principales

### 🧠 **Memoria Perfecta (FASE 1 - COMPLETADA)**
- **Event Sourcing**: Cada acción queda registrada permanentemente
- **Versionado de objetos**: Los objetos evolucionan en el tiempo (oxidación, desgaste)
- **Búsqueda temporal**: Encuentra cualquier evento por fecha/contexto
- **Vector Search**: Búsqueda semántica con ChromaDB y embeddings
- **Persistencia garantizada**: El mundo persiste entre sesiones
- **Sistema de backups automáticos**: Respaldos cada 6 horas con retención de 48 backups
- **Integridad de datos**: Validación y verificación automática de backups

### 🌐 **Web Interface (FASE 2 - BACKEND + UI FUNCIONANDO)**
- **API REST completa**: FastAPI con documentación automática
- **Panel de administración visual**: Swagger UI funcionando en puerto 8001
- **Autenticación JWT**: Sistema de roles y permisos
- **WebSocket en tiempo real**: Actualizaciones live del estado del juego
- **Dashboard con métricas**: Visualización JSON de estadísticas del mundo
- **Gestión de backups**: Interfaz para crear, restaurar y gestionar respaldos
- **Documentación interactiva**: Interface visual para probar la API

### 🤖 **Integración MCP (Model Context Protocol) - IMPLEMENTADO**
- **Contexto completo del mundo**: Para la IA con memoria perfecta
- **Búsqueda semántica**: Vector search con ChromaDB implementado
- **Análisis de patrones**: De juego del jugador en tiempo real
- **Información histórica**: Acceso completo a eventos pasados

### 🎮 **Sistema de Juego**
- Mundo interactivo con múltiples ubicaciones
- Inventario persistente del jugador
- Objetos con propiedades dinámicas
- Comandos en lenguaje natural procesados por IA

## 🚀 Instalación y Configuración

### Opción 1: Instalación Automática
```bash
python game_installer.py
```

### Opción 2: Instalación Manual

1. **Crear entorno virtual**:
```bash
python -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac  
source venv/bin/activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Instalar y configurar Ollama**:
```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar servidor
ollama serve

# Instalar modelo (en otra terminal)
ollama pull llama3.2
```

## 🎯 Uso

### 🎮 Juego de Consola

#### Demo Rápido (sin IA)
```bash
python test_game.py
```

#### Demo Completo (con IA)
```bash
python demo_game.py
```

#### Juego Interactivo
```bash
python adventure_game.py
```

### 🌐 Web Interface (NUEVA!)

#### Iniciar servidor de desarrollo
```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Servidor demo en puerto 8001
python .\web_interface\backend\app\demo_server.py

# Servidor completo en puerto 8001 (alternativo)
python .\web_interface\backend\app\main_dev.py
```

#### Acceder al panel web
- **Dashboard principal**: http://localhost:8001
- **Documentación API (Interface Visual)**: http://localhost:8001/docs
- **Métricas en tiempo real**: http://localhost:8001/api/demo/metrics
- **Gestión de backups**: http://localhost:8001/api/demo/backups

> 🎨 **NOTA**: La documentación API incluye una **interface visual completa** (Swagger UI) donde puedes probar todos los endpoints de forma interactiva.

#### 🎮 **Interface Visual Funcionando**
El servidor incluye **Swagger UI**, una interfaz gráfica completa que permite:
- ✅ **Explorar visualmente** todos los endpoints de la API
- ✅ **Probar requests** directamente desde el navegador  
- ✅ **Ver respuestas en tiempo real** con formato JSON
- ✅ **Documentación automática** de todos los parámetros
- ✅ **Autenticación visual** para endpoints protegidos

### 💾 Sistema de Backups

#### Crear backup manual
```bash
python adventure_game.py
# Usar comando: /backup create
```

#### Restaurar backup
```bash
python adventure_game.py
# Usar comando: /backup restore <backup_id>
```

#### Verificar backups automáticos
```bash
# Los backups se crean automáticamente cada 6 horas
# Se mantienen 48 backups (2 días de historia)
ls backups/
```

## 🏗️ Arquitectura del Sistema

```
🎮 Adventure Game v2.0
├── 🧠 Perfect Memory System (FASE 1)
│   ├── 📊 SQLite Database (estado actual)
│   ├── 📝 Event Sourcing (historial completo)
│   ├── 🔍 Temporal Queries
│   └── 💾 Automated Backup System
│       ├── ⏰ Scheduled backups (every 6h)
│       ├── 🗂️ Retention policy (48 backups)
│       ├── ✅ Integrity validation
│       └── � Restore capabilities
├── 🌐 Web Interface (FASE 2)
│   ├── 🎛️ FastAPI Backend
│   │   ├── 🔐 JWT Authentication
│   │   ├── 📡 WebSocket Support
│   │   ├── 📊 Real-time Metrics
│   │   └── 💾 Backup Management API
│   ├── ⚛️ React Frontend (planeado)
│   │   ├── 📈 Dashboard con gráficos
│   │   ├── 🎮 Control panel del juego
│   │   ├── 👥 Gestión de usuarios
│   │   └── 📋 Monitoreo del sistema
│   └── 🐳 Docker Deployment (planeado)
├── �🔗 MCP Integration
│   ├── 🌍 World Context Provider
│   ├── 📈 Player Analytics
│   └── 🎯 Smart Context Generation
└── 🤖 AI Integration (Ollama)
    ├── 🗣️ Natural Language Processing
    ├── 🎭 Immersive Responses
    └── 💭 Context-Aware Decisions
```

## 🗃️ Estructura del Proyecto

```
conversational-adventure/
├── 📁 adventure_game.py          # Juego principal
├── 📁 demo_game.py              # Demo con IA
├── 📁 game_installer.py         # Instalador automático
├── 📁 requirements.txt          # Dependencias del proyecto
├── 📁 backups/                  # Directorio de respaldos automáticos
│   ├── backup_YYYYMMDD_HHMMSS/  # Backups organizados por fecha
│   └── backup_index.json        # Índice de backups
├── 📁 web_interface/            # NUEVA: Interfaz web
│   ├── 📁 backend/             # Backend FastAPI
│   │   ├── 📁 app/
│   │   │   ├── main_dev.py     # Servidor de desarrollo
│   │   │   ├── demo_server.py  # Servidor demo simplificado
│   │   │   ├── auth.py         # Sistema de autenticación
│   │   │   └── models.py       # Modelos de datos
│   │   └── 📁 tests/           # Tests del backend
│   ├── 📁 frontend/            # Frontend React (planeado)
│   └── 📁 docs/               # Documentación técnica
├── 📁 FASE2_WEB_INTERFACE_PLAN.md # Plan detallado de la web interface
└── 📁 README.md               # Este archivo
```

## 📊 Estructura de Base de Datos

### Tablas Principales
- **`locations`**: Ubicaciones del mundo con conexiones
- **`game_objects`**: Objetos con propiedades y versiones
- **`game_events`**: Eventos inmutables con timestamps
- **`world_snapshots`**: Snapshots para optimización

### Sistema de Backups
- **Automáticos**: Cada 6 horas (configurable)
- **Retención**: 48 backups (2 días de historia)
- **Validación**: Verificación de integridad automática
- **Restauración**: Sistema completo de restore
- **Organización**: Backups organizados por fecha y tipo

### Ejemplo de Persistencia
```python
# El martillo se crea
martillo = await memory.create_object(
    "martillo del herrero",
    "Un pesado martillo con mango desgastado",
    "taller_id",
    properties={
        "material": "steel_wood",
        "condition": "used", 
        "rust_level": 0
    }
)

# Meses después, el martillo se oxida
await memory.modify_object_properties(
    martillo.id,
    {"rust_level": 3, "condition": "rusty"},
    actor="time"
)

# El jugador lo mueve
await memory.move_object(martillo.id, "nueva_ubicacion", actor="player")

# 6 MESES DESPUÉS: el martillo sigue ahí, oxidado
objetos = await memory.get_objects_in_location("nueva_ubicacion")
# ✅ El martillo está exactamente donde lo dejaste

# BACKUP AUTOMÁTICO: Todo queda respaldado
backup_status = await backup_system.get_latest_backup_status()
# ✅ Backup automático completado hace 2 horas
```

## 🔧 Configuración Avanzada

### Personalizar Modelos de IA
```python
# En adventure_game.py
game = IntelligentAdventureGame(
    memory_db_path="mi_mundo.db",
    model="llama3.2"  # o "mistral", "codellama", etc.
)
```

### Configurar Sistema de Backups
```python
# Configuración personalizada de backups
backup_config = {
    "interval_hours": 6,      # Backup cada 6 horas
    "max_backups": 48,        # Mantener 48 backups
    "backup_dir": "backups/", # Directorio de backups
    "compression": True,      # Comprimir backups
    "verify_integrity": True  # Verificar integridad
}
```

### Web Interface Settings
```python
# Configuración del servidor web
web_config = {
    "host": "0.0.0.0",
    "port": 8001,            # Puerto alternativo (8000 puede estar ocupado)
    "debug": True,           # Modo desarrollo
    "cors_origins": ["*"],   # CORS para desarrollo
    "jwt_secret": "your-secret-key",
    "session_timeout": 24    # Horas
}
```

### Base de Datos Personalizada
```python
# Usar PostgreSQL en lugar de SQLite
memory = PerfectMemorySystem("postgresql://user:pass@localhost/gamedb")
```

## 🧪 Ejemplos de Comandos

### 🎮 Comandos del Juego
```
🗣️ Jugador: "mirar alrededor"
🎮 IA: Te encuentras en la entrada del castillo. Una llave oxidada yace en el suelo...

🗣️ Jugador: "tomar la llave oxidada"  
🎮 IA: Tomas la llave. Sientes su peso y la textura rugosa del óxido entre tus dedos...

🗣️ Jugador: "ir al norte"
🎮 IA: Caminas hacia el hall principal. Tus pasos resuenan en las piedras antiguas...

🗣️ Jugador: "dejar la llave en el banco"
🎮 IA: Colocas cuidadosamente la llave sobre el banco de madera...

# 6 MESES DESPUÉS...
🗣️ Jugador: "mirar el banco"
🎮 IA: Sobre el banco de madera ves una llave oxidada, exactamente donde la dejaste hace meses. 
El óxido ha avanzado ligeramente...
```

### 💾 Comandos de Backup
```
🗣️ Jugador: "/backup create"
🎮 Sistema: ✅ Backup creado: backup_20250823_203916 (109,408 bytes)

🗣️ Jugador: "/backup list"
🎮 Sistema: 📋 Backups disponibles:
- backup_20250823_203916 (109KB) - hace 5 minutos
- backup_20250823_194635 (108KB) - hace 2 horas  
- backup_20250823_134521 (107KB) - hace 8 horas

🗣️ Jugador: "/backup restore backup_20250823_194635"
🎮 Sistema: 🔄 Restaurando backup... ✅ Mundo restaurado exitosamente

🗣️ Jugador: "/backup verify"
🎮 Sistema: ✅ Todos los backups verificados - integridad perfecta
```

### 🌐 API Web Examples
```bash
# Obtener estado del sistema
curl http://localhost:8001/api/health

# Ver métricas en tiempo real
curl http://localhost:8001/api/demo/metrics

# Listar backups via API
curl http://localhost:8001/api/demo/backups

# Crear backup via API (próximamente)
curl -X POST http://localhost:8001/api/backup/create
```

## 📈 Estadísticas del Mundo

### 🎮 En el Juego
```python
stats = await game.get_world_stats()
print(stats)
```

Salida:
```
🌍 ESTADÍSTICAS DEL MUNDO:
- Ubicaciones: 15
- Objetos: 47  
- Eventos registrados: 1,247
- Integridad de memoria: PERFECT - Nothing is ever forgotten
- Primer evento: 2025-01-15T10:30:45+00:00
- Último evento: 2025-08-23T19:41:36+00:00

💾 ESTADO DE BACKUPS:
- Total de backups: 23
- Último backup: backup_20250823_203916 (hace 15 minutos)
- Próximo backup: en 5h 45m
- Espacio usado: 2.4 MB
- Integridad: ✅ PERFECTA
```

### 🌐 En la Web Interface
Accede a http://localhost:8001/api/demo/metrics para ver:
```json
{
  "uptime": "2h 15m 30s",
  "requests_count": 142,
  "active_sessions": 3,
  "system_health": "excellent",
  "backup_count": 23,
  "events_count": 1247,
  "last_backup": "2025-08-23T20:39:16",
  "memory_usage": "42.3 MB",
  "api_version": "2.0.0-demo"
}
```

## 🛠️ Desarrollo y Extensión

### Añadir Nuevas Ubicaciones
```python
nueva_ubicacion = await memory.create_location(
    "Torre del Mago",
    "Una torre llena de libros y artefactos mágicos",
    connections={"abajo": "biblioteca"},
    properties={"magic_level": "high", "lighting": "mystical"}
)
```

### Crear Objetos Especiales
```python
espada_magica = await memory.create_object(
    "Espada de las Estrellas",
    "Una espada que brilla con luz estelar",
    ubicacion_id,
    properties={
        "damage": 50,
        "enchantment": "star_light",
        "durability": 100,
        "special_ability": "blind_enemies"
    }
)
```

### Eventos Personalizados
```python
await memory._record_event(
    event_type="spell_cast",
    actor="player",
    action="cast fireball spell",
    target="dragon",
    location_id=current_location,
    context={"spell_power": 75, "mana_cost": 30}
)
```

## 🔍 Análisis de Memoria

### Buscar en Historial
```python
# Buscar todos los eventos relacionados con "martillo"
eventos = await memory.search_events_by_content("martillo")

# Obtener historial completo de un objeto
historial = await memory.get_object_history(object_id)

# Analizar estilo de juego del jugador
contexto_jugador = await mcp.get_player_context("player")
```

## 🎯 Casos de Uso

### ✅ **Perfecto para:**
- Juegos de rol con mundos persistentes
- Sistemas de crafting complejos
- Simulaciones de vida artificial
- Narrativas interactivas largas
- Mundos compartidos multijugador

### 🔧 **Ejemplos de Implementación:**
1. **Granja Virtual**: Los cultivos crecen en tiempo real
2. **Taller de Alquimia**: Las pociones envejecen y cambian
3. **Ciudad Simulada**: Los NPCs recuerdan tus acciones
4. **Exploración Espacial**: Las naves se deterioran en el tiempo

## 🚀 Roadmap y Desarrollo

### ✅ **FASE 1 - COMPLETADA (Sistema de Memoria Perfecta)**
- [x] Event Sourcing con SQLite
- [x] Persistencia de objetos y eventos
- [x] Sistema de búsqueda temporal
- [x] Versionado de objetos
- [x] **Sistema de backups automáticos**
- [x] **Validación de integridad**
- [x] **Restauración completa**
- [x] **Retención automática de backups**

### 🌐 **FASE 2 - Web Interface (BACKEND + UI VISUAL)**
- [x] **Planificación completa** (FASE2_WEB_INTERFACE_PLAN.md)
- [x] **Backend FastAPI** con autenticación JWT
- [x] **API REST** con documentación automática
- [x] **Servidor de desarrollo** funcionando en puerto 8001
- [x] **WebSocket support** para tiempo real
- [x] **Sistema de roles** y permisos
- [x] **Interface visual Swagger UI** - Panel interactivo funcionando
- [x] **Dashboard con datos JSON** - Métricas en tiempo real
- [ ] **Frontend React customizado** (Semana 2-3)
- [ ] **Dashboard con gráficos** (Material-UI)
- [ ] **Gestión visual avanzada de backups**
- [ ] **Monitoreo en tiempo real con charts**

### 🎯 **FASE 3 - PLANEADA (Características Avanzadas)**
- [ ] **Multi-jugador**: Memoria compartida entre jugadores  
- [ ] **Plugin System**: Extensiones modulares
- [ ] **Analytics Dashboard**: BI completo del mundo
- [ ] **Mobile App**: Aplicación móvil
- [ ] **Cloud Deployment**: Despliegue en la nube
- [ ] **Vector Search Avanzado**: Embeddings más sofisticados y búsqueda por similitud

### 🔧 **FASE 4 - FUTURO (Escalabilidad)**
- [ ] **Microservicios**: Arquitectura distribuida
- [ ] **Message Queues**: Redis/RabbitMQ
- [ ] **Load Balancing**: Nginx + múltiples instancias
- [ ] **Database Sharding**: Particionado horizontal
- [ ] **Kubernetes**: Orquestación de contenedores
- [ ] **Monitoring**: Prometheus + Grafana

## 💡 Características Implementadas por Fase

### 📊 **FASE 1 - Memoria Perfecta + Vector Search**
```
✅ Event Sourcing              ✅ Backup automático cada 6h
✅ SQLite con eventos          ✅ Retención de 48 backups  
✅ Búsqueda temporal           ✅ Validación de integridad
✅ Versionado de objetos       ✅ Restauración completa
✅ Persistencia garantizada    ✅ Comandos /backup en juego
✅ Vector Search (ChromaDB)    ✅ Búsqueda semántica
✅ Embeddings automáticos      ✅ MCP integration
```

### 🌐 **FASE 2 - Web Interface**
```
✅ FastAPI backend             ✅ Swagger UI interface visual
✅ Autenticación JWT           ✅ Panel interactivo funcionando  
✅ API REST completa           ✅ Documentación visual automática
✅ WebSocket support           ✅ Dashboard JSON con métricas
✅ Documentación automática    🔄 React frontend customizado (planeado)
✅ CORS configurado            🔄 Gráficos y charts (planeado)
✅ Servidor en puerto 8001     🔄 Mobile responsive (planeado)
```

## 🐛 Troubleshooting

### ❌ Error: "Module not found"
```bash
# Verificar que estás en el entorno virtual
pip list

# Reinstalar dependencias
pip install -r requirements.txt

# Para web interface, verificar dependencias adicionales
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] websockets
```

### ❌ Error: "Ollama connection failed"
```bash
# Verificar que Ollama está ejecutándose
curl http://localhost:11434/api/version

# Si no responde, iniciar Ollama
ollama serve

# Verificar modelo instalado
ollama list
```

### ❌ Error: "Port already in use" (Web Interface)
```bash
# El puerto 8000 está ocupado, usar puerto alternativo
python .\web_interface\backend\app\demo_server.py  # Usa puerto 8001

# O matar proceso en puerto 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### ❌ Base de datos corrupta
```bash
# Restaurar desde backup automático
python adventure_game.py
# Usar comando: /backup list
# Usar comando: /backup restore <backup_id>

# Si no hay backups, recrear mundo
mv adventure_world.db adventure_world.db.corrupted
python adventure_game.py
```

### ❌ Error: "Backup verification failed"
```bash
# Verificar integridad de todos los backups
python adventure_game.py
# Usar comando: /backup verify

# Limpiar backups corruptos
python adventure_game.py  
# Usar comando: /backup clean
```

### ❌ Web Interface no carga
```bash
# Verificar que el servidor está ejecutándose
curl http://localhost:8001/api/health

# Ver logs del servidor
python .\web_interface\backend\app\demo_server.py

# Verificar firewall/antivirus
# Asegurarse de que el puerto 8001 no esté bloqueado
```

### 🔧 Comandos de Diagnóstico

#### Verificar estado completo del sistema
```bash
# En el juego
/system info
/backup status
/memory stats

# Via web API
curl http://localhost:8001/api/health
curl http://localhost:8001/api/demo/metrics
```

#### Logs y debugging
```bash
# Habilitar logs detallados
python adventure_game.py --debug

# Ver logs del servidor web
python .\web_interface\backend\app\demo_server.py --log-level debug
```

## 🤝 Contribuir

### 🔄 Proceso de Contribución
1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### 🎯 Áreas donde contribuir
- **Frontend React**: Implementar componentes del dashboard
- **Visualizaciones**: Gráficos y métricas avanzadas
- **Testing**: Tests automatizados para backend y frontend
- **Documentación**: Mejoras en docs y ejemplos
- **Performance**: Optimizaciones de base de datos
- **Plugins**: Sistema de extensiones modulares

### 🧪 Testing
```bash
# Tests del backend
cd web_interface/backend
pytest tests/

# Tests del sistema de memoria
python -m pytest test_memory_system.py

# Tests de integración
python test_game.py --test-mode
```

## 📊 Métricas del Proyecto

### 📈 **Líneas de Código (estimado)**
- **Backend Python**: ~3,500 líneas
- **Web Interface**: ~2,000 líneas  
- **Sistema de Memoria**: ~1,500 líneas
- **Documentación**: ~1,000 líneas
- **Total**: **~8,000 líneas**

### 🏗️ **Arquitectura**
- **Lenguajes**: Python 3.12, JavaScript (React), SQL
- **Frameworks**: FastAPI, React, Material-UI
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción)
- **Deployment**: Docker, Kubernetes (planeado)

### ⏱️ **Tiempo de Desarrollo**
- **Fase 1** (Memoria): ~2 semanas
- **Fase 2** (Web): ~3-4 semanas (en progreso)
- **Fase 3** (Avanzado): ~4-6 semanas (planeado)
- **Total estimado**: **~3-4 meses**

## � Licencia

MIT License - Úsalo libremente para tus proyectos.

## �👨‍💻 Autor

Desarrollado con ❤️ para demostrar el poder de la **memoria perfecta** en sistemas de IA y la importancia de una **arquitectura web robusta**.

### 🎯 **Filosofía del Proyecto**
> "La persistencia perfecta no es solo una característica técnica, es la base de la confianza entre el jugador y el mundo virtual. Cada objeto, cada decisión, cada momento debe ser recordado para siempre."

---

## 🚀 **¡INICIO RÁPIDO PARA DESARROLLADORES!**

```bash
# 1. Clonar y configurar
git clone <repo-url>
cd conversational-adventure
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Instalar todo
pip install -r requirements.txt

# 3. Probar el juego
python demo_game.py

# 4. Lanzar web interface
python .\web_interface\backend\app\demo_server.py

# 5. Abrir navegador
# http://localhost:8001/docs
```

**⚡ El martillo que dejes hoy, estará exactamente ahí en 6 meses - garantizado.**
**🌐 Ahora con panel web profesional - gestiona tu mundo desde cualquier navegador.**
