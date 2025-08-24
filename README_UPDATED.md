# 🧠 Adventure Game v3.0 - AI Enhanced Multilingual System

Un sistema de aventura conversacional de última generación que combina **Inteligencia Artificial avanzada**, **memoria perfecta con Event Sourcing**, **búsqueda vectorial semántica**, **interfaz web profesional** y **soporte multilingüe**. El sistema nunca olvida nada y puede narrar aventuras en 6 idiomas diferentes usando IA local con Ollama.

## 🚀 **ESTADO ACTUAL: SISTEMA COMPLETO v3.0 - AI ENHANCED**

### 📊 **Arquitectura del Sistema**

```
🧠 Adventure Game v3.0 - AI ENHANCED + MULTILINGUAL
├── 🎯 FASE 1 - Perfect Memory System (COMPLETADO ✅)
│   ├── 📊 SQLite Database con Event Sourcing
│   ├── 🔍 Vector Search con ChromaDB
│   ├── 💾 Sistema de backups automático (cada 6h)
│   ├── 🔄 Búsquedas temporales y semánticas
│   └── 🔌 MCP (Model Context Protocol) integration
│
├── 🌐 FASE 2 - Web Interface Profesional (COMPLETADO ✅)
│   ├── 🎛️ Backend FastAPI (puerto 8001)
│   │   ├── 🔐 Autenticación JWT
│   │   ├── 📡 WebSocket tiempo real
│   │   ├── 📊 API REST completa
│   │   └── 🛠️ Panel de administración
│   └── ⚛️ Frontend React 18 (puerto 3000)
│       ├── 🎨 Material-UI Dashboard profesional
│       ├── 📊 Gráficos interactivos Chart.js
│       ├── 🔄 WebSocket live updates
│       └── 🗂️ Gestión visual de backups
│
└── 🧠 FASE 3 - AI Enhancement + Multilingual (COMPLETADO ✅)
    ├── 🤖 AI Engine Avanzado
    │   ├── 🔍 RAG (Retrieval-Augmented Generation)
    │   ├── 🔤 Procesamiento NLP con spaCy
    │   ├── 🎭 Smart Narrator multi-personalidad
    │   ├── 🔮 Motor predictivo inteligente
    │   └── 💾 Sistema de memoria perfecta
    ├── 🦙 Ollama Integration
    │   ├── 🏠 IA local con Llama 3.2
    │   ├── ⚡ Sin dependencia de APIs externas
    │   ├── 🔒 Privacidad total
    │   └── 🚀 Rendimiento optimizado
    └── 🌍 Sistema Multilingüe
        ├── 🇪🇸 Español (por defecto)
        ├── 🇺🇸 English
        ├── 🇫🇷 Français
        ├── 🇵🇹 Português
        ├── 🇮🇹 Italiano
        └── 🇩🇪 Deutsch
```

## 🎯 **CARACTERÍSTICAS PRINCIPALES**

### 🧠 **IA Avanzada**
- **🦙 Ollama + Llama 3.2**: IA local sin depender de APIs externas
- **🔍 RAG System**: Búsqueda semántica con memoria contextual
- **🎭 6 Personalidades**: Misterioso, Amigable, Dramático, Humorístico, Erudito, Aventurero
- **🔮 Motor Predictivo**: Analiza comportamiento y sugiere acciones
- **💭 Memoria Perfecta**: Recuerda cada acción, objeto y conversación

### 🌍 **Multilingüe Total**
- **6 Idiomas Soportados**: ES, EN, FR, PT, IT, DE
- **Traducción Inteligente**: Personalidades adaptadas por idioma
- **API Multilingüe**: Endpoints para cambiar idioma dinámicamente
- **Narrativa Localizada**: Responses de IA completamente localizadas

### 🎮 **Experiencia de Juego**
- **Comandos Naturales**: Habla normalmente, la IA entiende
- **Mundo Persistente**: Todo se guarda automáticamente
- **Búsqueda Semántica**: "busca algo útil para abrir puertas"
- **Interfaz Web**: Juega desde cualquier navegador
- **Real-time**: Updates instantáneos vía WebSocket

## 🚀 **QUICK START**

### **Prerrequisitos**
- Python 3.12+
- Node.js 18+ (para interfaz web v2.0)
- Ollama instalado y ejecutándose
- Git

### **1. Instalación Básica**
```bash
# Clonar repositorio
git clone https://github.com/tutanchacon/conversational-adventure.git
cd conversational-adventure

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias AI
pip install -r requirements_ai.txt
```

### **2. Configurar Ollama**
```bash
# Instalar modelo Llama 3.2 (una sola vez)
ollama pull llama3.2:latest

# Verificar que Ollama esté ejecutándose
ollama ps
```

### **3. Configurar Variables de Entorno**
```bash
# Editar .env (ya existe con configuración por defecto)
AI_DEFAULT_LANGUAGE=es        # Idioma por defecto
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
```

### **4. Ejecutar Sistema AI v3.0**
```bash
# Opción A: Script automático
python start_ai_game.py

# Opción B: Servidor directo  
python ai_web_server.py

# Abrir navegador: http://localhost:8091
```

### **5. Ejecutar Web Interface v2.0 (Opcional)**
```bash
# En terminal separada
.\start_complete_system.bat

# URLs disponibles:
# Frontend: http://localhost:3000
# Backend: http://localhost:8001
```

## 🎮 **CÓMO JUGAR**

### **Comandos en Español (Default)**
```
mirar alrededor
ir al norte
examinar la habitación cuidadosamente
buscar objetos útiles
tomar la espada
hablar con el personaje
```

### **Cambiar Idioma (API)**
```javascript
// Cambiar a inglés
fetch('/api/language', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({language: 'en'})
})

// Luego usar comandos en inglés
"look around"
"go north"  
"examine the room carefully"
```

### **Cambiar Personalidad**
```javascript
// Ver personalidades disponibles
fetch('/api/personalities').then(r => r.json())

// Cambiar personalidad
fetch('/api/ai/config', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({personality: 'mysterious'})
})
```

## 📊 **ARQUITECTURA TÉCNICA**

### **Stack Tecnológico**
- **Backend**: FastAPI + Python 3.12
- **Frontend**: React 18 + Material-UI
- **IA Local**: Ollama + Llama 3.2
- **Base de Datos**: SQLite + ChromaDB
- **Vector Search**: SentenceTransformers
- **NLP**: spaCy + Transformers
- **WebSocket**: FastAPI WebSocket
- **Autenticación**: JWT

### **Puertos del Sistema**
- **8091**: AI Enhanced Server (v3.0)
- **8001**: Backend API (v2.0)
- **3000**: React Frontend (v2.0)
- **11434**: Ollama Server

## 🔌 **API ENDPOINTS**

### **AI Enhanced (Puerto 8091)**
```
GET  /                     # Interface web AI
POST /api/command          # Enviar comando al juego
GET  /api/languages        # Idiomas disponibles
POST /api/language         # Cambiar idioma
GET  /api/personalities    # Personalidades disponibles
POST /api/ai/config        # Configurar AI
GET  /api/ai/insights      # Estadísticas AI
POST /api/ai/generate      # Generar contenido
```

### **Web Interface (Puerto 8001)**
```
GET  /docs                 # Swagger UI
POST /auth/login          # Autenticación
GET  /api/stats           # Estadísticas del sistema
GET  /api/backups         # Gestión de backups
WebSocket /ws             # Conexión tiempo real
```

## 🧪 **TESTING**

### **Probar Multilingüe**
```bash
# 1. Iniciar en español (default)
curl -X POST http://localhost:8091/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "mirar alrededor"}'

# 2. Cambiar a inglés
curl -X POST http://localhost:8091/api/language \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'

# 3. Comando en inglés
curl -X POST http://localhost:8091/api/command \
  -H "Content-Type: application/json" \
  -d '{"command": "look around"}'
```

### **Probar Personalidades**
```bash
# Ver personalidades disponibles
curl http://localhost:8091/api/personalities

# Cambiar a personalidad misteriosa
curl -X POST http://localhost:8091/api/ai/config \
  -H "Content-Type: application/json" \
  -d '{"personality": "mysterious"}'
```

## 📈 **RENDIMIENTO**

### **Métricas del Sistema**
- **Respuesta AI**: ~2.0-3.0s (CPU) / ~0.5-1.0s (GPU con CUDA)
- **Búsqueda Vectorial**: <100ms
- **WebSocket Latency**: <50ms
- **Memoria**: ~500MB-1GB RAM
- **Storage**: ~50MB base + embeddings

### **Optimizaciones**
- **Ollama Local**: Sin latencia de red
- **Vector Cache**: Búsquedas optimizadas
- **Memory Pool**: Reutilización de contexto
- **Batch Processing**: Múltiples requests eficientes

## 🛠️ **DESARROLLO**

### **Scripts Disponibles**
```bash
python start_ai_game.py          # AI Server v3.0
python ai_web_server.py          # Servidor directo
.\start_complete_system.bat      # Sistema completo v2.0
python setup_ai_environment.py   # Configuración automática
python test_vector_system.py     # Test búsqueda vectorial
```

### **Estructura del Proyecto**
```
conversational-adventure/
├── ai_engine.py              # Motor IA principal
├── ai_integration.py         # Integración IA-Game
├── ai_web_server.py          # Servidor AI v3.0
├── translations.py           # Sistema multilingüe
├── memory_system.py          # Memoria perfecta
├── backup_system.py          # Sistema de backups
├── web_interface/            # Interface web v2.0
│   ├── backend/             # FastAPI
│   └── frontend/            # React
├── vector_db/               # ChromaDB embeddings
├── requirements_ai.txt      # Dependencias IA
└── .env                     # Configuración
```

## 🌟 **ROADMAP**

### **✅ Completado**
- [x] Perfect Memory System (Fase 1)
- [x] Web Interface Profesional (Fase 2)  
- [x] AI Enhancement + Multilingüe (Fase 3)
- [x] Ollama Integration
- [x] 6 Idiomas soportados
- [x] Sistema de personalidades
- [x] API completa multilingüe

### **🔄 En Desarrollo**
- [ ] Interfaz web para selector de idioma
- [ ] Persistencia de preferencias de usuario
- [ ] Modo offline completo
- [ ] Optimizaciones CUDA/GPU

### **📋 Planeado (Fase 4+)**
- [ ] Multiplayer real-time mejorado
- [ ] Aplicación móvil
- [ ] Integración con más modelos LLM
- [ ] Sistema de plugins
- [ ] Editor de mundos visual
- [ ] Voice interaction

## 🤝 **CONTRIBUIR**

1. Fork el proyecto
2. Crea feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 **LICENCIA**

MIT License - ver archivo [LICENSE](LICENSE)

## 👥 **CRÉDITOS**

- **AI Engine**: Ollama + Llama 3.2
- **Vector Search**: ChromaDB + SentenceTransformers  
- **NLP**: spaCy + Transformers
- **Web**: FastAPI + React + Material-UI
- **Desarrollado por**: @tutanchacon

---

## 🎯 **¡PRUÉBALO AHORA!**

```bash
git clone https://github.com/tutanchacon/conversational-adventure.git
cd conversational-adventure
python start_ai_game.py
# Abre http://localhost:8091 y comienza tu aventura en IA! 🚀
```

**¿Listo para una aventura que nunca olvida y habla tu idioma?** 🌍🧠✨
