# Generador de paquete completo de documentación
import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_documentation_package():
    """Crea un paquete ZIP con toda la documentación del proyecto"""
    
    # Nombre del archivo ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"Adventure_Game_MCP_Documentation_{timestamp}.zip"
    
    print("📦 CREANDO PAQUETE DE DOCUMENTACIÓN")
    print("=" * 50)
    print(f"📁 Archivo: {zip_filename}")
    
    # Archivos a incluir en el paquete
    files_to_include = [
        # Documentación principal
        ("ANALISIS_COMPLETO_MCP.md", "📊 Análisis técnico completo"),
        ("RESUMEN_EJECUTIVO_MCP.md", "📋 Resumen ejecutivo"),
        ("README.md", "📖 Guía de usuario"),
        
        # Código fuente principal
        ("memory_system.py", "🧠 Sistema de memoria perfecta"),
        ("mcp_integration.py", "🔗 Integración MCP"),
        ("adventure_game.py", "🎮 Motor del juego"),
        
        # Scripts de demo y utilidades
        ("demo_game.py", "🎯 Demo interactivo"),
        ("test_game.py", "🧪 Pruebas del sistema"),
        ("final_demo.py", "🏆 Demostración final"),
        ("setup_complete.py", "⚙️ Instalador automático"),
        ("create_documents.py", "📄 Generador de documentos"),
        ("generate_pdf.py", "📑 Generador de PDF"),
        
        # Configuración
        ("requirements.txt", "📦 Dependencias"),
        (".gitignore", "🚫 Configuración Git"),
    ]
    
    # Crear archivo ZIP
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # Agregar archivos principales
        total_files = 0
        total_size = 0
        
        for filename, description in files_to_include:
            if Path(filename).exists():
                file_info = zipf.write(filename)
                file_size = Path(filename).stat().st_size
                total_size += file_size
                total_files += 1
                print(f"   ✅ {description:<30} ({file_size:,} bytes)")
            else:
                print(f"   ⚠️ {description:<30} (archivo no encontrado)")
        
        # Agregar archivo de índice
        index_content = f"""# 🎮 ADVENTURE GAME CON MEMORIA PERFECTA
## Paquete de Documentación Completa

**Generado:** {datetime.now().strftime("%d de %B, %Y a las %H:%M:%S")}  
**Versión:** 1.0.0  
**Archivos incluidos:** {total_files}  
**Tamaño total:** {total_size:,} bytes  

---

## 📚 DOCUMENTACIÓN

### 📊 Análisis Técnico
- **ANALISIS_COMPLETO_MCP.md** - Análisis completo del sistema MCP
- **RESUMEN_EJECUTIVO_MCP.md** - Resumen para ejecutivos y stakeholders
- **README.md** - Guía de instalación y uso

### 🔧 Código Fuente

#### Core System
- **memory_system.py** - Sistema de memoria perfecta con Event Sourcing
- **mcp_integration.py** - Integración del Protocolo de Contexto de Modelo  
- **adventure_game.py** - Motor principal del juego

#### Demos y Utilidades
- **demo_game.py** - Demo interactivo del sistema
- **test_game.py** - Pruebas sin dependencias externas
- **final_demo.py** - Demostración completa de memoria perfecta
- **setup_complete.py** - Instalador automático completo

#### Herramientas
- **create_documents.py** - Generador de documentación
- **generate_pdf.py** - Conversor Markdown a PDF
- **requirements.txt** - Lista de dependencias Python

---

## 🚀 INICIO RÁPIDO

### 1. Extracción
```bash
# Extraer archivos del ZIP
unzip Adventure_Game_MCP_Documentation_*.zip
cd adventure-game-mcp/
```

### 2. Instalación
```bash
# Opción A: Instalación automática
python setup_complete.py

# Opción B: Instalación manual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
```

### 3. Demo Rápido
```bash
# Demo sin dependencias externas
python test_game.py

# Demo completo (requiere Ollama)
python demo_game.py

# Demostración de memoria perfecta
python final_demo.py
```

---

## 🎯 CARACTERÍSTICAS PRINCIPALES

### ✅ Memoria Perfecta
- **Event Sourcing:** Cada acción registrada permanentemente
- **Versionado de objetos:** Evolución temporal realística
- **Búsqueda temporal:** Encontrar estado en cualquier momento
- **Persistencia garantizada:** Funciona después de meses

### 🤖 Integración MCP
- **Contexto completo:** La IA conoce todo el estado del mundo
- **Búsqueda semántica:** Encontrar información por contenido
- **Análisis de patrones:** Entender comportamiento del jugador
- **Respuestas contextuales:** IA siempre consistente con la realidad

### 🎮 Experiencia de Juego
- **Comandos naturales:** Interfaz en lenguaje humano
- **Mundo persistente:** Estado se mantiene entre sesiones
- **Evolución realística:** Objetos se oxidan, degradan, cambian
- **Continuidad perfecta:** Retomar después de meses sin pérdida

---

## 📊 DEMOSTRACIÓN: EL MARTILLO IMMORTAL

```python
# Día 1: Crear martillo
martillo = await memory.create_object(
    "martillo del herrero",
    "Un pesado martillo con mango desgastado",
    "taller_id", 
    properties={"rust_level": 0, "condition": "good"}
)

# Día 30: Jugador lo mueve
await game.process_command_async("tomar el martillo")
await game.process_command_async("ir a la biblioteca")
await game.process_command_async("dejar el martillo en el banco")

# Día 180: Evolución natural
await memory.modify_object_properties(
    martillo.id,
    {"rust_level": 3, "condition": "rusty"},
    actor="time"
)

# Día 365: ¡SIGUE AHÍ!
objetos = await memory.get_objects_in_location("biblioteca_id")
# ✅ Martillo encontrado, oxidado, exactamente donde se dejó
```

---

## 🏗️ ARQUITECTURA

```
🎮 Adventure Game
├── 🧠 Perfect Memory System
│   ├── SQLite + Event Sourcing
│   ├── Versionado automático
│   └── Búsqueda temporal
├── 🔗 MCP Integration  
│   ├── Contexto para IA
│   ├── Análisis de patrones
│   └── Búsqueda semántica
├── 🤖 AI Engine
│   ├── Ollama + LLM local
│   ├── Comandos naturales
│   └── Respuestas inmersivas
└── 🎯 Game Engine
    ├── Mundo persistente
    ├── Inventario dinámico
    └── Evolución temporal
```

---

## 💡 CASOS DE USO

### ✅ Para Desarrolladores
- Arquitectura de referencia para Event Sourcing
- Implementación completa de MCP
- Sistema de persistencia robusto
- Integración IA + Base de datos

### ✅ Para Investigadores
- Estudio de memoria perfecta en IA
- Análisis de comportamiento de usuario
- Evolución temporal de sistemas
- Protocolo de Contexto de Modelo

### ✅ Para Empresas
- Base para juegos persistentes
- Sistema de recomendaciones con memoria
- Plataforma de simulación avanzada
- Framework de IA contextual

---

## 📞 SOPORTE

### Documentación
- **README.md** - Guía completa de instalación
- **Análisis MCP** - Documentación técnica detallada
- **Código fuente** - Comentado y autodocumentado

### Comunidad
- GitHub Issues para bugs y features
- Wiki con tutoriales avanzados
- Foro de desarrolladores

---

**🔨 "El martillo que dejes hoy, estará exactamente ahí en 6 meses - GARANTIZADO."**

*Adventure Game con Memoria Perfecta - Donde nada se olvida jamás.*
"""
        
        # Escribir índice al ZIP
        zipf.writestr("INDEX.md", index_content)
        print(f"   ✅ {'📋 Índice del paquete':<30} ({len(index_content):,} bytes)")
        total_files += 1
        total_size += len(index_content)
    
    # Estadísticas finales
    zip_size = Path(zip_filename).stat().st_size
    compression_ratio = (1 - zip_size / total_size) * 100
    
    print(f"\n📊 ESTADÍSTICAS DEL PAQUETE:")
    print(f"   📁 Archivos incluidos: {total_files}")
    print(f"   📏 Tamaño original: {total_size:,} bytes")
    print(f"   🗜️ Tamaño comprimido: {zip_size:,} bytes")
    print(f"   📉 Compresión: {compression_ratio:.1f}%")
    
    print(f"\n✅ PAQUETE CREADO EXITOSAMENTE!")
    print(f"📦 Archivo: {zip_filename}")
    print(f"📍 Ubicación: {Path(zip_filename).absolute()}")
    
    print(f"\n🎯 CONTENIDO DEL PAQUETE:")
    print(f"   📊 Documentación completa del análisis MCP")
    print(f"   🔧 Código fuente completo y funcional")
    print(f"   🧪 Demos y scripts de prueba")
    print(f"   ⚙️ Herramientas de instalación")
    print(f"   📋 Índice y guías de inicio rápido")
    
    return zip_filename

def main():
    """Función principal"""
    print("🎉 GENERADOR DE PAQUETE COMPLETO")
    print("🎮 Adventure Game con Memoria Perfecta")
    print("🔗 Análisis MCP + Código + Documentación")
    print()
    
    try:
        zip_file = create_documentation_package()
        
        print(f"\n🚀 ¡PAQUETE LISTO PARA DESCARGAR!")
        print(f"📧 Puedes enviar {zip_file} por email")
        print(f"☁️ Subir a Google Drive, Dropbox, etc.")
        print(f"📱 Compartir por WhatsApp, Telegram, etc.")
        
        # Sugerir próximos pasos
        print(f"\n💡 PRÓXIMOS PASOS SUGERIDOS:")
        print(f"   1. Compartir {zip_file} con tu equipo")
        print(f"   2. Revisar INDEX.md para guía completa")
        print(f"   3. Ejecutar demos para ver el sistema en acción")
        print(f"   4. Leer ANALISIS_COMPLETO_MCP.md para detalles técnicos")
        
    except Exception as e:
        print(f"❌ Error creando paquete: {e}")

if __name__ == "__main__":
    main()
