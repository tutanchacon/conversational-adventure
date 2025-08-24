#!/usr/bin/env python3
"""
🎮 ADVENTURE GAME v2.0.0 - SERVIDOR DEMO RÁPIDO
Servidor simple para jugar en el browser
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
import sys
import os
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from adventure_game import IntelligentAdventureGame
    GAME_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ No se pudo importar adventure_game: {e}")
    GAME_AVAILABLE = False

# Crear aplicación FastAPI
app = FastAPI(
    title="Adventure Game v2.0.0 - Demo Browser",
    description="Juega Adventure Game desde tu browser",
    version="2.0.0"
)

# Configurar CORS para permitir cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable global para el juego
game_instance = None

@app.on_event("startup")
async def startup_event():
    """Inicializar el juego al arrancar el servidor"""
    global game_instance
    if GAME_AVAILABLE:
        try:
            print("🎮 Inicializando Adventure Game...")
            game_instance = IntelligentAdventureGame()
            print("✅ Adventure Game inicializado correctamente")
        except Exception as e:
            print(f"❌ Error inicializando juego: {e}")
            game_instance = None

@app.get("/", response_class=HTMLResponse)
async def game_interface():
    """Interface web simple para jugar"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Adventure Game v2.0.0</title>
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: #1a1a1a;
                color: #00ff00;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: #000;
                padding: 30px;
                border-radius: 10px;
                border: 2px solid #00ff00;
                box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
            }
            h1 {
                text-align: center;
                color: #00ffff;
                text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
                margin-bottom: 30px;
            }
            .game-output {
                background: #0a0a0a;
                border: 1px solid #333;
                padding: 20px;
                min-height: 300px;
                max-height: 400px;
                overflow-y: auto;
                margin-bottom: 20px;
                border-radius: 5px;
                white-space: pre-wrap;
            }
            .input-container {
                display: flex;
                gap: 10px;
            }
            #commandInput {
                flex: 1;
                background: #111;
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 10px;
                font-family: 'Courier New', monospace;
                border-radius: 3px;
            }
            #sendButton {
                background: #004400;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            #sendButton:hover {
                background: #006600;
            }
            .status {
                margin-bottom: 20px;
                padding: 10px;
                background: #001a00;
                border-left: 4px solid #00ff00;
                border-radius: 3px;
            }
            .examples {
                margin-top: 20px;
                padding: 15px;
                background: #001a1a;
                border-left: 4px solid #00ffff;
                border-radius: 3px;
            }
            .examples h3 {
                color: #00ffff;
                margin-top: 0;
            }
            .examples ul {
                margin: 0;
                padding-left: 20px;
            }
            .examples li {
                margin: 5px 0;
                color: #88ff88;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 Adventure Game v2.0.0</h1>
            
            <div class="status">
                <strong>🌟 Sistema:</strong> <span id="status">Conectando...</span><br>
                <strong>🔍 Vector Search:</strong> <span id="vectorStatus">Verificando...</span><br>
                <strong>🧠 Memory System:</strong> <span id="memoryStatus">Cargando...</span>
            </div>
            
            <div class="game-output" id="gameOutput">
🎮 Bienvenido a Adventure Game v2.0.0!
🧠 Sistema de memoria perfecta activo
🔍 Búsqueda vectorial inteligente lista
🌐 Ejecutándose en tu browser

Escribe tu comando abajo para comenzar...
            </div>
            
            <div class="input-container">
                <input type="text" id="commandInput" placeholder="Escribe tu comando aquí..." 
                       onkeypress="if(event.key==='Enter') sendCommand()">
                <button id="sendButton" onclick="sendCommand()">Enviar</button>
            </div>
            
            <div class="examples">
                <h3>💡 Comandos de Ejemplo:</h3>
                <ul>
                    <li><strong>Básicos:</strong> "mirar alrededor", "ir al norte", "crear martillo"</li>
                    <li><strong>Vector Search:</strong> "buscar herramientas de carpintería", "buscar objetos como martillo"</li>
                    <li><strong>Análisis:</strong> "analizar patrones aquí", "recomendar objetos"</li>
                    <li><strong>Estado:</strong> "inventario", "estado del juego", "historial"</li>
                </ul>
            </div>
        </div>

        <script>
            async function checkStatus() {
                try {
                    const response = await fetch('/status');
                    const status = await response.json();
                    
                    document.getElementById('status').textContent = status.game ? '✅ Activo' : '❌ Error';
                    document.getElementById('vectorStatus').textContent = status.vector_search ? '✅ Operativo' : '⚠️ Limitado';
                    document.getElementById('memoryStatus').textContent = status.memory ? '✅ Cargado' : '❌ Error';
                } catch (error) {
                    console.error('Error checking status:', error);
                }
            }

            async function sendCommand() {
                const input = document.getElementById('commandInput');
                const output = document.getElementById('gameOutput');
                const command = input.value.trim();
                
                if (!command) return;
                
                // Mostrar comando del usuario
                output.textContent += `\\n\\n> ${command}\\n`;
                input.value = '';
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
                    } else {
                        output.textContent += `❌ Error: ${result.error}`;
                    }
                } catch (error) {
                    output.textContent += `❌ Error de conexión: ${error.message}`;
                }
                
                output.scrollTop = output.scrollHeight;
            }
            
            // Verificar estado al cargar
            checkStatus();
            
            // Enfocar el input
            document.getElementById('commandInput').focus();
        </script>
    </body>
    </html>
    """

@app.get("/status")
async def game_status():
    """Estado del sistema de juego"""
    return {
        "game": game_instance is not None,
        "vector_search": GAME_AVAILABLE,
        "memory": GAME_AVAILABLE
    }

@app.post("/command")
async def process_command(request: dict):
    """Procesar comando del juego"""
    if not game_instance:
        return {"success": False, "error": "Juego no disponible"}
    
    command = request.get("command", "").strip()
    if not command:
        return {"success": False, "error": "Comando vacío"}
    
    try:
        response = await game_instance.process_command_async(command)
        return {"success": True, "response": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🎮 ADVENTURE GAME v2.0.0 - SERVIDOR DEMO")
    print("=" * 50)
    print("🚀 Iniciando servidor...")
    print("🌐 URL: http://localhost:8080")
    print("📱 Abre Chrome y ve a: http://localhost:8080")
    print("⏹️  Para parar: Ctrl+C")
    print("-" * 50)
    
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
