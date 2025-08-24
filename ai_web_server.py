#!/usr/bin/env python3
"""
🌐 AI ENHANCED WEB SERVER - Adventure Game v3.0
Servidor web con capacidades de IA avanzadas
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import os

# Imports del sistema AI
from ai_integration import AIAdventureGame, create_ai_game
from ai_engine import AIPersonality

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class CommandRequest(BaseModel):
    command: str
    player_id: str = "default_player"

class AIConfigRequest(BaseModel):
    personality: str
    enable_voice: bool = False
    enable_predictions: bool = True

class ContentGenerationRequest(BaseModel):
    content_type: str  # location, npc, object, quest
    context: Dict[str, Any] = {}

# App FastAPI
app = FastAPI(
    title="AI Adventure Game v3.0",
    description="Adventure Game con IA avanzada, RAG, y generación de contenido",
    version="3.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales
ai_game: Optional[AIAdventureGame] = None
active_connections: Dict[str, WebSocket] = {}
connection_stats = {
    "total_connections": 0,
    "active_connections": 0,
    "total_commands": 0,
    "avg_response_time": 0.0
}

# Eventos de aplicación
@app.on_event("startup")
async def startup_event():
    """Inicializar sistema AI al arrancar"""
    global ai_game
    
    logger.info("🚀 Starting AI Adventure Game v3.0...")
    
    try:
        ai_game = await create_ai_game("ai_adventure_web.db")
        logger.info("✅ AI Adventure Game initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI game: {e}")
        # Crear fallback simple
        ai_game = None

@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar sistemas al terminar"""
    global ai_game
    
    if ai_game:
        await ai_game.close()
        logger.info("🛑 AI Adventure Game closed")

# Dependency para verificar AI game
async def get_ai_game() -> AIAdventureGame:
    if ai_game is None:
        raise HTTPException(status_code=503, detail="AI Game not available")
    return ai_game

# ===== ENDPOINTS API =====

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    """Interface web principal con IA"""
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🧠 AI Adventure Game v3.0</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f0f23, #1a1a3a, #2d1b69);
                color: #e0e0ff;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                display: grid;
                grid-template-columns: 1fr 300px;
                grid-gap: 20px;
                min-height: 100vh;
            }
            
            .main-area {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            
            .header {
                text-align: center;
                background: rgba(0, 0, 0, 0.5);
                padding: 20px;
                border-radius: 15px;
                border: 2px solid #4a9eff;
                box-shadow: 0 0 30px rgba(74, 158, 255, 0.3);
            }
            
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                background: linear-gradient(45deg, #4a9eff, #00ffff, #9d4edd);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 30px rgba(74, 158, 255, 0.5);
            }
            
            .game-area {
                display: grid;
                grid-template-rows: 1fr auto;
                gap: 15px;
                height: 600px;
            }
            
            .output {
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid #4a9eff;
                border-radius: 10px;
                padding: 20px;
                overflow-y: auto;
                font-family: 'Courier New', monospace;
                line-height: 1.6;
                box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
            }
            
            .input-area {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .input-container {
                flex: 1;
                position: relative;
            }
            
            #commandInput {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #4a9eff;
                border-radius: 10px;
                background: rgba(0, 0, 0, 0.8);
                color: #e0e0ff;
                font-family: 'Courier New', monospace;
                font-size: 16px;
                box-shadow: 0 0 15px rgba(74, 158, 255, 0.2);
                transition: all 0.3s ease;
            }
            
            #commandInput:focus {
                outline: none;
                border-color: #00ffff;
                box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
            }
            
            .send-btn {
                padding: 15px 25px;
                background: linear-gradient(45deg, #4a9eff, #00ffff);
                border: none;
                border-radius: 10px;
                color: #000;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 16px;
            }
            
            .send-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(74, 158, 255, 0.4);
            }
            
            .sidebar {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .panel {
                background: rgba(0, 0, 0, 0.6);
                border: 1px solid #4a9eff;
                border-radius: 10px;
                padding: 15px;
            }
            
            .panel h3 {
                margin: 0 0 10px 0;
                color: #00ffff;
                font-size: 1.1em;
            }
            
            .ai-status {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                font-size: 0.9em;
            }
            
            .status-item {
                padding: 8px;
                background: rgba(74, 158, 255, 0.1);
                border-radius: 5px;
                text-align: center;
            }
            
            .personality-selector select {
                width: 100%;
                padding: 8px;
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #4a9eff;
                border-radius: 5px;
                color: #e0e0ff;
            }
            
            .quick-actions {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 8px;
            }
            
            .quick-btn {
                padding: 8px 12px;
                background: rgba(74, 158, 255, 0.2);
                border: 1px solid #4a9eff;
                border-radius: 5px;
                color: #e0e0ff;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 0.9em;
                text-align: center;
            }
            
            .quick-btn:hover {
                background: rgba(74, 158, 255, 0.4);
            }
            
            .suggestions {
                background: rgba(157, 78, 221, 0.1);
                border-left: 3px solid #9d4edd;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            
            .ai-response {
                background: rgba(0, 255, 255, 0.05);
                border-left: 3px solid #00ffff;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
            }
            
            .ai-meta {
                font-size: 0.8em;
                color: #888;
                margin-top: 5px;
            }
            
            .loading {
                display: inline-block;
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            @media (max-width: 768px) {
                .container {
                    grid-template-columns: 1fr;
                    padding: 10px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .quick-actions {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-area">
                <div class="header">
                    <h1>🧠 AI Adventure Game v3.0</h1>
                    <p>Aventura con Inteligencia Artificial Avanzada, RAG y Generación de Contenido</p>
                </div>
                
                <div class="game-area">
                    <div class="output" id="gameOutput">
                        <div class="ai-response">
                            🧠 <strong>AI Narrator:</strong> Welcome to the most advanced adventure game ever created! 
                            I am your AI-powered narrator, equipped with perfect memory, semantic understanding, 
                            and the ability to generate dynamic content just for you.
                            <br><br>
                            ✨ <strong>New AI Features:</strong>
                            <br>• 🔍 Semantic memory search
                            <br>• 🎭 Adaptive personality 
                            <br>• 🔮 Predictive suggestions
                            <br>• 🎨 Dynamic content generation
                            <br><br>
                            <strong>Type a command to begin your intelligent adventure...</strong>
                            <div class="ai-meta">AI Confidence: 100% | Personality: Friendly | Response: 0.1s</div>
                        </div>
                    </div>
                    
                    <div class="input-area">
                        <div class="input-container">
                            <input type="text" id="commandInput" 
                                   placeholder="Enter your command... (e.g., 'explore the mystical forest')"
                                   onkeypress="if(event.key==='Enter') sendCommand()">
                        </div>
                        <button class="send-btn" onclick="sendCommand()">🚀 Send</button>
                    </div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="panel">
                    <h3>🧠 AI Status</h3>
                    <div class="ai-status">
                        <div class="status-item">
                            <strong>Confidence</strong><br>
                            <span id="aiConfidence">95%</span>
                        </div>
                        <div class="status-item">
                            <strong>Response Time</strong><br>
                            <span id="responseTime">0.2s</span>
                        </div>
                        <div class="status-item">
                            <strong>Memory Recall</strong><br>
                            <span id="memoryRecall">Active</span>
                        </div>
                        <div class="status-item">
                            <strong>Predictions</strong><br>
                            <span id="predictions">Enabled</span>
                        </div>
                    </div>
                </div>
                
                <div class="panel">
                    <h3>🎭 AI Personality</h3>
                    <div class="personality-selector">
                        <select id="personalitySelect" onchange="changePersonality()">
                            <option value="friendly">😊 Friendly</option>
                            <option value="mysterious">🔮 Mysterious</option>
                            <option value="dramatic">🎭 Dramatic</option>
                            <option value="humorous">😄 Humorous</option>
                            <option value="scholarly">🎓 Scholarly</option>
                            <option value="adventurous">⚡ Adventurous</option>
                        </select>
                    </div>
                </div>
                
                <div class="panel">
                    <h3>⚡ Quick Actions</h3>
                    <div class="quick-actions">
                        <div class="quick-btn" onclick="quickCommand('look around')">👁️ Look</div>
                        <div class="quick-btn" onclick="quickCommand('check inventory')">🎒 Inventory</div>
                        <div class="quick-btn" onclick="quickCommand('explore area')">🗺️ Explore</div>
                        <div class="quick-btn" onclick="quickCommand('help')">❓ Help</div>
                        <div class="quick-btn" onclick="quickCommand('create something magical')">✨ Create</div>
                        <div class="quick-btn" onclick="getAIInsights()">📊 AI Stats</div>
                    </div>
                </div>
                
                <div class="panel">
                    <h3>🎯 AI Suggestions</h3>
                    <div id="aiSuggestions">
                        <div class="suggestions">
                            • Try asking for creative challenges<br>
                            • Use natural language descriptions<br>
                            • Ask the AI to generate new content
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let isProcessing = false;
            
            async function sendCommand(cmd = null) {
                if (isProcessing) return;
                
                const input = document.getElementById('commandInput');
                const output = document.getElementById('gameOutput');
                const command = cmd || input.value.trim();
                
                if (!command) return;
                
                isProcessing = true;
                
                // Mostrar comando del usuario
                output.innerHTML += `
                    <div style="margin: 10px 0; padding: 10px; background: rgba(74, 158, 255, 0.1); border-radius: 5px;">
                        <strong>You:</strong> ${command}
                    </div>
                `;
                
                // Mostrar loading
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'loading';
                loadingDiv.innerHTML = '🧠 <strong>AI thinking...</strong> <span style="animation: pulse 1s infinite;">●●●</span>';
                output.appendChild(loadingDiv);
                output.scrollTop = output.scrollHeight;
                
                if (!cmd) input.value = '';
                
                try {
                    const startTime = Date.now();
                    
                    const response = await fetch('/api/command', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            command: command,
                            player_id: 'web_player'
                        })
                    });
                    
                    const result = await response.json();
                    const responseTime = ((Date.now() - startTime) / 1000).toFixed(2);
                    
                    // Remover loading
                    output.removeChild(loadingDiv);
                    
                    if (result.success) {
                        // Mostrar respuesta AI
                        output.innerHTML += `
                            <div class="ai-response">
                                🧠 <strong>AI Narrator:</strong> ${result.message}
                                <div class="ai-meta">
                                    AI Confidence: ${(result.ai_confidence * 100).toFixed(1)}% | 
                                    Personality: ${result.ai_personality} | 
                                    Response: ${responseTime}s
                                </div>
                            </div>
                        `;
                        
                        // Actualizar sugerencias
                        if (result.suggestions && result.suggestions.length > 0) {
                            const suggestionsDiv = document.getElementById('aiSuggestions');
                            suggestionsDiv.innerHTML = `
                                <div class="suggestions">
                                    ${result.suggestions.map(s => `• ${s}`).join('<br>')}
                                </div>
                            `;
                        }
                        
                        // Actualizar status
                        document.getElementById('aiConfidence').textContent = 
                            `${(result.ai_confidence * 100).toFixed(0)}%`;
                        document.getElementById('responseTime').textContent = `${responseTime}s`;
                        
                    } else {
                        output.innerHTML += `
                            <div style="background: rgba(255, 0, 0, 0.1); border-left: 3px solid #ff4444; padding: 15px; margin: 10px 0; border-radius: 5px;">
                                ❌ <strong>Error:</strong> ${result.error || 'Unknown error'}
                            </div>
                        `;
                    }
                    
                } catch (error) {
                    // Remover loading
                    if (output.contains(loadingDiv)) {
                        output.removeChild(loadingDiv);
                    }
                    
                    output.innerHTML += `
                        <div style="background: rgba(255, 0, 0, 0.1); border-left: 3px solid #ff4444; padding: 15px; margin: 10px 0; border-radius: 5px;">
                            ❌ <strong>Connection Error:</strong> ${error.message}
                        </div>
                    `;
                }
                
                output.scrollTop = output.scrollHeight;
                isProcessing = false;
                input.focus();
            }
            
            function quickCommand(cmd) {
                sendCommand(cmd);
            }
            
            async function changePersonality() {
                const select = document.getElementById('personalitySelect');
                const personality = select.value;
                
                try {
                    const response = await fetch('/api/ai/config', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ 
                            personality: personality,
                            enable_predictions: true
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        const output = document.getElementById('gameOutput');
                        output.innerHTML += `
                            <div style="background: rgba(157, 78, 221, 0.1); border-left: 3px solid #9d4edd; padding: 10px; margin: 10px 0; border-radius: 5px;">
                                🎭 <strong>AI Personality changed to:</strong> ${personality}
                            </div>
                        `;
                        output.scrollTop = output.scrollHeight;
                    }
                } catch (error) {
                    console.error('Error changing personality:', error);
                }
            }
            
            async function getAIInsights() {
                try {
                    const response = await fetch('/api/ai/insights?player_id=web_player');
                    const insights = await response.json();
                    
                    const output = document.getElementById('gameOutput');
                    output.innerHTML += `
                        <div style="background: rgba(0, 255, 0, 0.1); border-left: 3px solid #00ff00; padding: 15px; margin: 10px 0; border-radius: 5px;">
                            📊 <strong>AI Insights:</strong><br>
                            • Play Style: ${insights.player_behavior?.play_style || 'unknown'}<br>
                            • Total AI Responses: ${insights.system_stats?.total_ai_responses || 0}<br>
                            • Avg Response Time: ${(insights.system_stats?.avg_response_time || 0).toFixed(2)}s<br>
                            • Player Satisfaction: ${((insights.system_stats?.player_satisfaction || 0) * 100).toFixed(1)}%
                        </div>
                    `;
                    output.scrollTop = output.scrollHeight;
                    
                } catch (error) {
                    console.error('Error getting AI insights:', error);
                }
            }
            
            // Focus en input al cargar
            document.getElementById('commandInput').focus();
            
            // Auto-completar básico
            document.getElementById('commandInput').addEventListener('input', function(e) {
                // TODO: Implementar autocompletado con IA
            });
        </script>
    </body>
    </html>
    """

@app.post("/api/command")
async def process_command(request: CommandRequest, game: AIAdventureGame = Depends(get_ai_game)):
    """Procesar comando con IA"""
    try:
        result = await game.process_command(request.player_id, request.command)
        connection_stats["total_commands"] += 1
        return result
        
    except Exception as e:
        logger.error(f"❌ Error processing command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/config")
async def configure_ai(request: AIConfigRequest, game: AIAdventureGame = Depends(get_ai_game)):
    """Configurar sistema de IA"""
    try:
        # Cambiar personalidad
        personality_map = {
            "friendly": AIPersonality.FRIENDLY,
            "mysterious": AIPersonality.MYSTERIOUS,
            "dramatic": AIPersonality.DRAMATIC,
            "humorous": AIPersonality.HUMOROUS,
            "scholarly": AIPersonality.SCHOLARLY,
            "adventurous": AIPersonality.ADVENTUROUS
        }
        
        personality = personality_map.get(request.personality, AIPersonality.FRIENDLY)
        success = await game.change_ai_personality(personality)
        
        return {
            "success": success,
            "personality": request.personality,
            "message": f"AI personality changed to {request.personality}"
        }
        
    except Exception as e:
        logger.error(f"❌ Error configuring AI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/insights")
async def get_ai_insights(player_id: str = "default_player", 
                         game: AIAdventureGame = Depends(get_ai_game)):
    """Obtener insights de IA sobre el jugador"""
    try:
        insights = await game.get_ai_insights(player_id)
        return insights
        
    except Exception as e:
        logger.error(f"❌ Error getting AI insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/generate")
async def generate_content(request: ContentGenerationRequest, 
                          game: AIAdventureGame = Depends(get_ai_game)):
    """Generar contenido del mundo con IA"""
    try:
        content = await game.generate_world_content(request.content_type, request.context)
        
        if content:
            return {
                "success": True,
                "content": content,
                "content_type": request.content_type
            }
        else:
            return {
                "success": False,
                "error": f"Could not generate {request.content_type}"
            }
            
    except Exception as e:
        logger.error(f"❌ Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    """Estado del sistema"""
    try:
        ai_stats = {}
        if ai_game:
            ai_stats = await ai_game.get_ai_insights("system")
        
        return {
            "ai_game_available": ai_game is not None,
            "connection_stats": connection_stats,
            "ai_stats": ai_stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"❌ Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/languages")
async def get_languages():
    """Obtener idiomas soportados"""
    try:
        from translations import translation_system
        from ai_engine import AILanguage
        
        languages = []
        for lang in AILanguage:
            languages.append({
                "code": lang.value,
                "name": translation_system.get_text(f"language_{lang.name.lower()}", lang),
                "native_name": translation_system.get_text(f"language_{lang.name.lower()}", lang)
            })
        
        return {
            "languages": languages,
            "current": ai_game.ai_engine.get_language().value if ai_game else "es"
        }
    except Exception as e:
        logger.error(f"❌ Error getting languages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/language")
async def set_language(request: dict):
    """Cambiar idioma del sistema"""
    try:
        from ai_engine import AILanguage
        
        language_code = request.get("language", "es")
        
        # Convertir código a enum
        language = None
        for lang in AILanguage:
            if lang.value == language_code:
                language = lang
                break
        
        if not language:
            raise HTTPException(status_code=400, detail="Idioma no soportado")
        
        if ai_game:
            ai_game.ai_engine.set_language(language)
        
        return {
            "success": True,
            "language": language.value,
            "message": f"Idioma cambiado a {language.value}"
        }
    except Exception as e:
        logger.error(f"❌ Error setting language: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/personalities")
async def get_personalities():
    """Obtener personalidades disponibles"""
    try:
        from translations import translation_system
        from ai_engine import AIPersonality, AILanguage
        
        current_language = ai_game.ai_engine.get_language() if ai_game else AILanguage.SPANISH
        
        personalities = []
        for personality in AIPersonality:
            personalities.append({
                "id": personality.value,
                "name": translation_system.get_text(f"personality_{personality.value}", current_language),
                "description": translation_system.get_personality_traits(current_language)[personality.value]
            })
        
        return {
            "personalities": personalities,
            "current": ai_game.ai_engine.narrator.personality.value if ai_game else "friendly"
        }
    except Exception as e:
        logger.error(f"❌ Error getting personalities: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    except Exception as e:
        logger.error(f"❌ Error getting status: {e}")
        return {
            "ai_game_available": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# WebSocket para tiempo real
@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """WebSocket para comunicación en tiempo real"""
    await websocket.accept()
    active_connections[player_id] = websocket
    connection_stats["total_connections"] += 1
    connection_stats["active_connections"] += 1
    
    try:
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": f"Connected to AI Adventure Game v3.0",
            "player_id": player_id
        }))
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "command" and ai_game:
                result = await ai_game.process_command(player_id, message.get("command", ""))
                await websocket.send_text(json.dumps({
                    "type": "response",
                    "result": result
                }))
            
    except WebSocketDisconnect:
        if player_id in active_connections:
            del active_connections[player_id]
        connection_stats["active_connections"] -= 1
        logger.info(f"🔌 Player {player_id} disconnected")

# Script de inicio
def start_ai_server(host: str = "127.0.0.1", port: int = 8091):
    """Iniciar servidor AI"""
    print("🧠 AI ADVENTURE GAME v3.0 - ENHANCED SERVER")
    print("=" * 50)
    print("🚀 Starting AI-enhanced server...")
    print(f"🌐 URL: http://{host}:{port}")
    print("📱 Open browser and navigate to the URL above")
    print("⚡ Features: AI Narrator, RAG Search, Content Generation")
    print("⏹️  To stop: Ctrl+C")
    print("-" * 50)
    
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    start_ai_server()
