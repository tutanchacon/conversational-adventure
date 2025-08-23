# Adventure Game con Sistema de Memoria Perfecta y MCP

Un juego de aventura conversacional que implementa un sistema de memoria perfecta usando el Protocolo de Contexto de Modelo (MCP). **La IA nunca olvida nada**: donde dejaste el martillo, hace cuánto tiempo, si se oxidó, etc.

## 🌟 Características Principales

### 🧠 **Memoria Perfecta**
- **Event Sourcing**: Cada acción queda registrada permanentemente
- **Versionado de objetos**: Los objetos evolucionan en el tiempo (oxidación, desgaste)
- **Búsqueda temporal**: Encuentra cualquier evento por fecha/contexto
- **Persistencia garantizada**: El mundo persiste entre sesiones

### 🤖 **Integración MCP (Model Context Protocol)**
- Contexto completo del mundo para la IA
- Búsqueda semántica de eventos y objetos
- Análisis de patrones de juego del jugador
- Información histórica detallada

### 🎮 **Sistema de Juego**
- Mundo interactivo con múltiples ubicaciones
- Inventario persistente del jugador
- Objetos con propiedades dinámicas
- Comandos en lenguaje natural procesados por IA

## 🚀 Instalación Rápida

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

### Demo Rápido (sin IA)
```bash
python test_game.py
```

### Demo Completo (con IA)
```bash
python demo_game.py
```

### Juego Interactivo
```bash
python adventure_game.py
```

## 🏗️ Arquitectura del Sistema

```
🎮 Adventure Game
├── 🧠 Perfect Memory System
│   ├── 📊 SQLite Database (estado actual)
│   ├── 📝 Event Sourcing (historial completo)
│   └── 🔍 Temporal Queries
├── 🔗 MCP Integration
│   ├── 🌍 World Context Provider
│   ├── 📈 Player Analytics
│   └── 🎯 Smart Context Generation
└── 🤖 AI Integration (Ollama)
    ├── 🗣️ Natural Language Processing
    ├── 🎭 Immersive Responses
    └── 💭 Context-Aware Decisions
```

## 📊 Estructura de Base de Datos

### Tablas Principales
- **`locations`**: Ubicaciones del mundo con conexiones
- **`game_objects`**: Objetos con propiedades y versiones
- **`game_events`**: Eventos inmutables con timestamps
- **`world_snapshots`**: Snapshots para optimización

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

### Base de Datos Personalizada
```python
# Usar PostgreSQL en lugar de SQLite
memory = PerfectMemorySystem("postgresql://user:pass@localhost/gamedb")
```

## 🧪 Ejemplos de Comandos

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

## 📈 Estadísticas del Mundo

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

## 🚀 Próximas Características

- [ ] **Vector Search**: Embeddings para búsqueda semántica
- [ ] **Multi-jugador**: Memoria compartida entre jugadores  
- [ ] **Plugin System**: Extensiones modulares
- [ ] **Web Interface**: Interfaz web para administración
- [ ] **Analytics Dashboard**: Visualización de datos del mundo
- [ ] **Backup/Restore**: Sistema de respaldos automáticos

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Verificar que estás en el entorno virtual
pip list

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Ollama connection failed"
```bash
# Verificar que Ollama está ejecutándose
curl http://localhost:11434/api/version

# Si no responde, iniciar Ollama
ollama serve
```

### Base de datos corrupta
```bash
# Hacer backup
cp adventure_world.db adventure_world.db.backup

# Recrear mundo
rm adventure_world.db
python adventure_game.py
```

## 📄 Licencia

MIT License - Úsalo libremente para tus proyectos.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 👨‍💻 Autor

Desarrollado con ❤️ para demostrar el poder de la memoria perfecta en sistemas de IA.

---

**⚡ El martillo que dejes hoy, estará exactamente ahí en 6 meses - garantizado.**
