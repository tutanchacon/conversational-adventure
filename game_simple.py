#!/usr/bin/env python3
"""
🎮 ADVENTURE GAME v2.0.0 - SERVIDOR SIMPLE SIN DEPENDENCIAS EXTERNAS
Servidor básico que funciona sin las importaciones complejas
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import json
import asyncio
from datetime import datetime
import uuid

# Crear aplicación FastAPI
app = FastAPI(
    title="Adventure Game v2.0.0 - Simple",
    description="Juego de aventura básico en browser",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado del juego simple en memoria
game_state = {
    "current_location": "inicio",
    "locations": {
        "inicio": {
            "name": "Punto de Inicio",
            "description": "Te encuentras en un claro en el bosque. El aire es fresco y puedes ver senderos en varias direcciones.",
            "objects": [],
            "exits": {"norte": "bosque", "sur": "aldea", "este": "rio"}
        },
        "bosque": {
            "name": "Bosque Misterioso", 
            "description": "Un denso bosque lleno de árboles antiguos. Se escuchan sonidos extraños entre las hojas.",
            "objects": ["rama caída", "setas brillantes"],
            "exits": {"sur": "inicio", "oeste": "cueva"}
        },
        "aldea": {
            "name": "Aldea Tranquila",
            "description": "Una pequeña aldea con casas de piedra. Los aldeanos te saludan amigablemente.",
            "objects": ["pozo", "herramientas"],
            "exits": {"norte": "inicio", "este": "taller"}
        },
        "taller": {
            "name": "Taller de Carpintería",
            "description": "Un taller lleno de herramientas de madera. El olor a madera fresca llena el aire.",
            "objects": ["martillo", "sierra", "clavos"],
            "exits": {"oeste": "aldea"}
        },
        "rio": {
            "name": "Río Cristalino",
            "description": "Un río de aguas cristalinas que fluye suavemente. Puedes ver peces nadando.",
            "objects": ["piedras", "caña de pescar"],
            "exits": {"oeste": "inicio"}
        },
        "cueva": {
            "name": "Cueva Oscura",
            "description": "Una cueva profunda y misteriosa. Necesitas una antorcha para explorar.",
            "objects": ["cristales", "antorcha"],
            "exits": {"este": "bosque"}
        }
    },
    "inventory": [],
    "events": []
}

def process_command(command: str) -> str:
    """Procesa un comando del juego"""
    command = command.lower().strip()
    current_loc = game_state["locations"][game_state["current_location"]]
    
    # Comando: mirar
    if "mirar" in command or "look" in command:
        response = f"📍 **{current_loc['name']}**\n\n"
        response += f"{current_loc['description']}\n\n"
        
        if current_loc["objects"]:
            response += "🔍 **Objetos aquí:** " + ", ".join(current_loc["objects"]) + "\n\n"
        
        if current_loc["exits"]:
            response += "🚪 **Salidas:** " + ", ".join(current_loc["exits"].keys())
        
        return response
    
    # Comando: ir/move
    if any(word in command for word in ["ir", "move", "go"]):
        direction = None
        for exit_dir in current_loc["exits"]:
            if exit_dir in command:
                direction = exit_dir
                break
        
        if direction and direction in current_loc["exits"]:
            game_state["current_location"] = current_loc["exits"][direction]
            new_loc = game_state["locations"][game_state["current_location"]]
            
            # Log del evento
            game_state["events"].append({
                "time": datetime.now().isoformat(),
                "action": f"Movimiento: {current_loc['name']} → {new_loc['name']}"
            })
            
            return f"🚶 Te mueves hacia el {direction}...\n\n" + process_command("mirar")
        else:
            return f"❌ No puedes ir en esa dirección. Salidas disponibles: {', '.join(current_loc['exits'].keys())}"
    
    # Comando: tomar
    if any(word in command for word in ["tomar", "take", "get", "coger"]):
        for obj in current_loc["objects"]:
            if obj in command:
                current_loc["objects"].remove(obj)
                game_state["inventory"].append(obj)
                
                # Log del evento
                game_state["events"].append({
                    "time": datetime.now().isoformat(),
                    "action": f"Objeto tomado: {obj} en {current_loc['name']}"
                })
                
                return f"✅ Has tomado: {obj}"
        
        return "❌ No veo ese objeto aquí."
    
    # Comando: inventario
    if "inventario" in command or "inventory" in command:
        if game_state["inventory"]:
            return "🎒 **Tu inventario:**\n" + "\n".join(f"• {item}" for item in game_state["inventory"])
        else:
            return "🎒 Tu inventario está vacío."
    
    # Comando: crear
    if "crear" in command or "create" in command:
        # Extraer lo que quiere crear
        parts = command.split()
        if len(parts) > 1:
            obj_name = " ".join(parts[1:])
            current_loc["objects"].append(obj_name)
            
            # Log del evento
            game_state["events"].append({
                "time": datetime.now().isoformat(),
                "action": f"Objeto creado: {obj_name} en {current_loc['name']}"
            })
            
            return f"✨ Has creado: {obj_name}"
        else:
            return "❌ ¿Qué quieres crear? Ejemplo: 'crear espada mágica'"
    
    # Comando: buscar (simulación de vector search)
    if "buscar" in command:
        search_term = command.replace("buscar", "").strip()
        found_objects = []
        
        # Buscar en todas las ubicaciones
        for loc_name, loc_data in game_state["locations"].items():
            for obj in loc_data["objects"]:
                if any(word in obj.lower() for word in search_term.split()):
                    found_objects.append(f"{obj} (en {loc_data['name']})")
        
        # Buscar en inventario
        for obj in game_state["inventory"]:
            if any(word in obj.lower() for word in search_term.split()):
                found_objects.append(f"{obj} (en tu inventario)")
        
        if found_objects:
            return f"🔍 **Búsqueda '{search_term}':**\n" + "\n".join(f"• {obj}" for obj in found_objects)
        else:
            return f"🔍 No se encontraron objetos relacionados con '{search_term}'"
    
    # Comando: historial
    if "historial" in command or "history" in command:
        if game_state["events"]:
            recent_events = game_state["events"][-5:]  # Últimos 5 eventos
            response = "📜 **Historial reciente:**\n"
            for event in recent_events:
                time_str = event["time"].split("T")[1][:8]  # Solo la hora
                response += f"• {time_str}: {event['action']}\n"
            return response
        else:
            return "📜 No hay eventos en el historial."
    
    # Comando: ayuda
    if "ayuda" in command or "help" in command:
        return """🆘 **Comandos disponibles:**

🔍 **Exploración:**
• mirar - Ver tu ubicación actual
• ir [dirección] - Moverse (norte, sur, este, oeste)

🎒 **Objetos:**
• tomar [objeto] - Recoger un objeto
• inventario - Ver tus objetos
• crear [objeto] - Crear un nuevo objeto

🔍 **Búsqueda:**
• buscar [término] - Buscar objetos por palabra clave
• historial - Ver eventos recientes

💡 **Ejemplos:**
• mirar alrededor
• ir al norte
• tomar martillo
• crear espada mágica
• buscar herramientas"""
    
    # Comando no reconocido
    return f"❓ No entiendo el comando '{command}'. Escribe 'ayuda' para ver los comandos disponibles."

@app.get("/", response_class=HTMLResponse)
async def game_interface():
    """Interface web del juego"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adventure Game v2.0.0 - Simple</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #1a1a2e, #16213e);
                color: #00ff00;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
                min-height: 100vh;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: rgba(0, 0, 0, 0.8);
                padding: 30px;
                border-radius: 15px;
                border: 2px solid #00ff00;
                box-shadow: 0 0 30px rgba(0, 255, 0, 0.3);
            }
            h1 {
                text-align: center;
                color: #00ffff;
                text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .status-bar {
                display: flex;
                justify-content: space-between;
                background: #001a00;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
                border: 1px solid #004400;
            }
            .status-item {
                color: #88ff88;
            }
            .game-output {
                background: #0a0a0a;
                border: 2px solid #333;
                padding: 25px;
                min-height: 400px;
                max-height: 500px;
                overflow-y: auto;
                margin-bottom: 20px;
                border-radius: 10px;
                white-space: pre-wrap;
                box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
            }
            .input-container {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            #commandInput {
                flex: 1;
                background: #111;
                border: 2px solid #00ff00;
                color: #00ff00;
                padding: 15px;
                font-family: 'Courier New', monospace;
                border-radius: 5px;
                font-size: 16px;
            }
            #commandInput:focus {
                outline: none;
                border-color: #00ffff;
                box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            }
            #sendButton {
                background: linear-gradient(45deg, #004400, #006600);
                color: #00ff00;
                border: 2px solid #00ff00;
                padding: 15px 25px;
                cursor: pointer;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                transition: all 0.3s;
            }
            #sendButton:hover {
                background: linear-gradient(45deg, #006600, #008800);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.5);
            }
            .quick-commands {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin-bottom: 20px;
            }
            .quick-btn {
                background: #001a1a;
                border: 1px solid #00ffff;
                color: #00ffff;
                padding: 8px 12px;
                cursor: pointer;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                transition: all 0.3s;
            }
            .quick-btn:hover {
                background: #003333;
                box-shadow: 0 0 8px rgba(0, 255, 255, 0.3);
            }
            .examples {
                background: #001a1a;
                border-left: 4px solid #00ffff;
                padding: 15px;
                border-radius: 5px;
                margin-top: 10px;
            }
            .examples h3 {
                color: #00ffff;
                margin-top: 0;
            }
            .cmd-example {
                color: #ffff88;
                background: #222;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Adventure Game v2.0.0</h1>
            
            <div class="status-bar">
                <div class="status-item"><strong>🌟 Estado:</strong> ✅ Activo</div>
                <div class="status-item"><strong>🗺️ Ubicación:</strong> <span id="currentLocation">Cargando...</span></div>
                <div class="status-item"><strong>🎒 Objetos:</strong> <span id="inventoryCount">0</span></div>
            </div>
            
            <div class="game-output" id="gameOutput">🎮 Bienvenido a Adventure Game v2.0.0!
🌟 Sistema simplificado pero completamente funcional
🗺️ Mundo persistente con memoria de eventos
🔍 Búsqueda básica de objetos implementada

Escribe 'mirar' para comenzar tu aventura...
            </div>
            
            <div class="quick-commands">
                <button class="quick-btn" onclick="quickCommand('mirar')">👁️ Mirar</button>
                <button class="quick-btn" onclick="quickCommand('inventario')">🎒 Inventario</button>
                <button class="quick-btn" onclick="quickCommand('ayuda')">❓ Ayuda</button>
                <button class="quick-btn" onclick="quickCommand('historial')">📜 Historial</button>
            </div>
            
            <div class="input-container">
                <input type="text" id="commandInput" placeholder="Escribe tu comando aquí..." 
                       onkeypress="if(event.key==='Enter') sendCommand()">
                <button id="sendButton" onclick="sendCommand()">▶ Enviar</button>
            </div>
            
            <div class="examples">
                <h3>💡 Comandos de Ejemplo:</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>
                        <strong>🔍 Exploración:</strong><br>
                        <span class="cmd-example">mirar alrededor</span><br>
                        <span class="cmd-example">ir al norte</span><br>
                        <span class="cmd-example">ir al taller</span>
                    </div>
                    <div>
                        <strong>🎒 Objetos:</strong><br>
                        <span class="cmd-example">tomar martillo</span><br>
                        <span class="cmd-example">crear espada mágica</span><br>
                        <span class="cmd-example">buscar herramientas</span>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let gameState = { inventory: [], location: 'inicio' };

            async function sendCommand(cmd = null) {
                const input = document.getElementById('commandInput');
                const output = document.getElementById('gameOutput');
                const command = cmd || input.value.trim();
                
                if (!command) return;
                
                // Mostrar comando del usuario
                output.textContent += `\\n\\n> ${command}\\n`;
                if (!cmd) input.value = '';
                output.scrollTop = output.scrollHeight;
                
                try {
                    const response = await fetch('/command', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ command: command })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        output.textContent += result.response;
                        
                        // Actualizar estado de la UI
                        if (result.location) {
                            document.getElementById('currentLocation').textContent = result.location;
                        }
                        if (result.inventory_count !== undefined) {
                            document.getElementById('inventoryCount').textContent = result.inventory_count;
                        }
                    } else {
                        output.textContent += `❌ Error: ${result.error}`;
                    }
                } catch (error) {
                    output.textContent += `❌ Error de conexión: ${error.message}`;
                }
                
                output.scrollTop = output.scrollHeight;
            }
            
            function quickCommand(cmd) {
                sendCommand(cmd);
            }
            
            // Inicializar
            document.getElementById('commandInput').focus();
            sendCommand('mirar');
        </script>
    </body>
    </html>
    """

@app.post("/command")
async def handle_command(request: dict):
    """Procesar comando del juego"""
    command = request.get("command", "").strip()
    if not command:
        return {"success": False, "error": "Comando vacío"}
    
    try:
        response = process_command(command)
        current_loc = game_state["locations"][game_state["current_location"]]
        
        return {
            "success": True, 
            "response": response,
            "location": current_loc["name"],
            "inventory_count": len(game_state["inventory"])
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/status")
async def get_status():
    """Estado del juego"""
    current_loc = game_state["locations"][game_state["current_location"]]
    return {
        "success": True,
        "location": current_loc["name"],
        "inventory": game_state["inventory"],
        "events_count": len(game_state["events"])
    }

if __name__ == "__main__":
    print("🎮 ADVENTURE GAME v2.0.0 - SERVIDOR SIMPLE")
    print("=" * 50)
    print("🚀 Iniciando servidor sin dependencias externas...")
    print("🌐 URL: http://localhost:8090")
    print("📱 Abre Chrome y ve a: http://localhost:8090")
    print("⏹️  Para parar: Ctrl+C")
    print("-" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8090, log_level="info")
