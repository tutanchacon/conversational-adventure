#!/usr/bin/env python3
"""
🧠 AI ENGINE CORE - Adventure Game v3.0
Sistema de IA avanzado con RAG enhancement, predicción y generación de contenido
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from memory_system import PerfectMemorySystem
import chromadb
from chromadb.config import Settings
import numpy as np
import spacy
from transformers import pipeline

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIPersonality(Enum):
    """Personalidades del AI Narrator"""
    MYSTERIOUS = "mysterious"
    FRIENDLY = "friendly"
    DRAMATIC = "dramatic"
    HUMOROUS = "humorous"
    SCHOLARLY = "scholarly"
    ADVENTUROUS = "adventurous"

@dataclass
class AIContext:
    """Contexto completo para la IA"""
    current_location: str
    recent_events: List[Dict]
    relevant_memories: List[Dict]
    player_mood: str
    narrative_state: str
    conversation_history: List[Dict]
    world_state: Dict[str, Any]
    player_preferences: Dict[str, Any]

@dataclass
class AIResponse:
    """Respuesta completa del sistema de IA"""
    content: str
    confidence: float
    suggestions: List[str]
    context_used: List[str]
    generated_content: Dict[str, Any]
    personality_applied: AIPersonality
    processing_time: float

class EnhancedRAGSystem:
    """Sistema RAG mejorado para búsqueda semántica avanzada"""
    
    def __init__(self, memory_system: PerfectMemorySystem):
        self.memory = memory_system
        self.chroma_client = chromadb.PersistentClient(
            path="./ai_enhanced_memory",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Crear colecciones especializadas
        self.collections = {
            "locations": self._get_or_create_collection("locations"),
            "objects": self._get_or_create_collection("objects"),
            "events": self._get_or_create_collection("events"),
            "conversations": self._get_or_create_collection("conversations"),
            "narratives": self._get_or_create_collection("narratives")
        }
        
        logger.info("🧠 Enhanced RAG System initialized")
    
    def _get_or_create_collection(self, name: str):
        """Obtener o crear colección con configuración optimizada"""
        try:
            return self.chroma_client.get_collection(name)
        except:
            return self.chroma_client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine", "hnsw:M": 16}
            )
    
    async def add_memory_embedding(self, content: str, category: str, metadata: Dict[str, Any]):
        """Agregar embedding de memoria con categorización"""
        try:
            collection = self.collections.get(category, self.collections["events"])
            
            # Generar ID único
            memory_id = f"{category}_{datetime.now().isoformat()}_{hash(content)}"
            
            # Agregar a ChromaDB
            collection.add(
                documents=[content],
                metadatas=[{
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "category": category
                }],
                ids=[memory_id]
            )
            
            logger.info(f"✅ Memory embedding added: {category} - {content[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Error adding memory embedding: {e}")
    
    async def semantic_search(self, query: str, category: Optional[str] = None, 
                            limit: int = 10, relevance_threshold: float = 0.7) -> List[Dict]:
        """Búsqueda semántica avanzada con filtrado inteligente"""
        results = []
        
        try:
            # Buscar en categorías específicas o todas
            collections_to_search = [self.collections[category]] if category else self.collections.values()
            
            for collection in collections_to_search:
                search_results = collection.query(
                    query_texts=[query],
                    n_results=limit,
                    include=["documents", "metadatas", "distances"]
                )
                
                # Filtrar por relevancia
                for i, distance in enumerate(search_results['distances'][0]):
                    relevance = 1.0 - distance  # Convertir distancia a relevancia
                    
                    if relevance >= relevance_threshold:
                        results.append({
                            "content": search_results['documents'][0][i],
                            "metadata": search_results['metadatas'][0][i],
                            "relevance": relevance,
                            "category": search_results['metadatas'][0][i].get('category', 'unknown')
                        })
            
            # Ordenar por relevancia
            results.sort(key=lambda x: x['relevance'], reverse=True)
            
            logger.info(f"🔍 Semantic search: '{query}' - {len(results)} results")
            return results[:limit]
            
        except Exception as e:
            logger.error(f"❌ Error in semantic search: {e}")
            return []

class NLPProcessor:
    """Procesador de lenguaje natural avanzado"""
    
    def __init__(self):
        # Cargar modelo de spaCy
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("⚠️ spaCy model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Clasificador de intenciones
        self.intent_classifier = self._setup_intent_classifier()
        
        # Patrones de comando
        self.command_patterns = {
            "movement": ["go", "move", "walk", "run", "travel", "head"],
            "interaction": ["take", "get", "pick", "grab", "use", "activate"],
            "observation": ["look", "examine", "inspect", "see", "check"],
            "inventory": ["inventory", "items", "carrying", "have"],
            "creation": ["create", "make", "craft", "build", "generate"],
            "search": ["find", "search", "locate", "where", "look for"],
            "social": ["talk", "speak", "say", "tell", "ask", "greet"],
            "help": ["help", "what", "how", "explain", "guide"]
        }
        
        logger.info("🧠 NLP Processor initialized")
    
    def _setup_intent_classifier(self):
        """Configurar clasificador de intenciones"""
        try:
            return pipeline("text-classification", 
                          model="microsoft/DialoGPT-medium",
                          return_all_scores=True)
        except:
            logger.warning("⚠️ Intent classifier not available")
            return None
    
    async def parse_command(self, text: str) -> Dict[str, Any]:
        """Analizar comando con NLP avanzado"""
        analysis = {
            "original": text,
            "cleaned": text.lower().strip(),
            "intent": "unknown",
            "entities": [],
            "confidence": 0.0,
            "suggestions": [],
            "emotion": "neutral"
        }
        
        try:
            if self.nlp:
                doc = self.nlp(text)
                
                # Extraer entidades
                analysis["entities"] = [
                    {"text": ent.text, "label": ent.label_, "description": spacy.explain(ent.label_)}
                    for ent in doc.ents
                ]
                
                # Clasificar intención
                intent, confidence = self._classify_intent(text)
                analysis["intent"] = intent
                analysis["confidence"] = confidence
                
                # Detectar emoción básica
                analysis["emotion"] = self._detect_emotion(text)
                
                # Generar sugerencias
                analysis["suggestions"] = self._generate_suggestions(intent, analysis["entities"])
            
            logger.info(f"🧠 Command parsed: '{text}' -> {analysis['intent']} ({analysis['confidence']:.2f})")
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error parsing command: {e}")
            return analysis
    
    def _classify_intent(self, text: str) -> Tuple[str, float]:
        """Clasificar intención del comando"""
        text_lower = text.lower()
        
        # Búsqueda por patrones
        for intent, patterns in self.command_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    return intent, 0.8
        
        return "unknown", 0.3
    
    def _detect_emotion(self, text: str) -> str:
        """Detectar emoción básica del texto"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["!", "amazing", "wow", "great", "awesome"]):
            return "excited"
        elif any(word in text_lower for word in ["?", "help", "confused", "don't understand"]):
            return "confused"
        elif any(word in text_lower for word in ["tired", "bored", "sad", "frustrated"]):
            return "negative"
        else:
            return "neutral"
    
    def _generate_suggestions(self, intent: str, entities: List[Dict]) -> List[str]:
        """Generar sugerencias basadas en intención"""
        suggestions = []
        
        if intent == "movement":
            suggestions = ["go north", "go south", "go east", "go west", "explore area"]
        elif intent == "observation":
            suggestions = ["look around", "examine object", "check inventory"]
        elif intent == "interaction":
            suggestions = ["take item", "use object", "interact with NPC"]
        elif intent == "unknown":
            suggestions = ["try 'help' for commands", "describe what you want to do"]
        
        return suggestions[:3]

class SmartNarrator:
    """Narrador inteligente con personalidad adaptativa"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.personality = AIPersonality.FRIENDLY
        self.narrative_memory = []
        self.coherence_context = {}
        
        logger.info("🎭 Smart Narrator initialized")
    
    async def generate_response(self, context: AIContext, user_input: str) -> AIResponse:
        """Generar respuesta narrativa inteligente"""
        start_time = datetime.now()
        
        try:
            # Construir prompt contextual
            prompt = self._build_contextual_prompt(context, user_input)
            
            # Generar respuesta con OpenAI
            response = await self._call_openai(prompt)
            
            # Procesar y mejorar respuesta
            enhanced_response = self._enhance_response(response, context)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Construir respuesta completa
            ai_response = AIResponse(
                content=enhanced_response["content"],
                confidence=enhanced_response["confidence"],
                suggestions=enhanced_response["suggestions"],
                context_used=enhanced_response["context_used"],
                generated_content=enhanced_response["generated_content"],
                personality_applied=self.personality,
                processing_time=processing_time
            )
            
            # Actualizar memoria narrativa
            self._update_narrative_memory(user_input, ai_response.content)
            
            logger.info(f"🎭 Response generated in {processing_time:.2f}s")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {e}")
            return self._fallback_response(user_input)
    
    def _build_contextual_prompt(self, context: AIContext, user_input: str) -> str:
        """Construir prompt con contexto completo"""
        
        personality_traits = {
            AIPersonality.MYSTERIOUS: "mysterious, enigmatic, speaks in riddles",
            AIPersonality.FRIENDLY: "warm, helpful, encouraging",
            AIPersonality.DRAMATIC: "theatrical, passionate, emotionally intense", 
            AIPersonality.HUMOROUS: "witty, playful, finds humor in situations",
            AIPersonality.SCHOLARLY: "knowledgeable, precise, educational",
            AIPersonality.ADVENTUROUS: "bold, exciting, action-oriented"
        }
        
        prompt = f"""You are an AI narrator for an adventure game with perfect memory. 

PERSONALITY: {personality_traits[self.personality]}

CURRENT CONTEXT:
- Location: {context.current_location}
- Player mood: {context.player_mood}
- Narrative state: {context.narrative_state}

RECENT EVENTS:
{self._format_events(context.recent_events)}

RELEVANT MEMORIES:
{self._format_memories(context.relevant_memories)}

WORLD STATE:
{json.dumps(context.world_state, indent=2)}

PLAYER INPUT: "{user_input}"

INSTRUCTIONS:
1. Respond in character as the narrator
2. Use relevant memories to maintain continuity
3. Be contextually aware of the player's situation
4. Generate vivid, immersive descriptions
5. Maintain narrative coherence
6. Suggest 2-3 possible actions

RESPONSE FORMAT:
{
  "narrative": "Your narrative response here",
  "suggestions": ["action 1", "action 2", "action 3"],
  "generated_elements": {
    "new_objects": [],
    "environmental_changes": [],
    "mood_shift": ""
  }
}
"""
        
        return prompt
    
    def _format_events(self, events: List[Dict]) -> str:
        """Formatear eventos para el prompt"""
        if not events:
            return "No recent events"
        
        formatted = []
        for event in events[-5:]:  # Últimos 5 eventos
            formatted.append(f"- {event.get('timestamp', 'unknown')}: {event.get('description', '')}")
        
        return "\n".join(formatted)
    
    def _format_memories(self, memories: List[Dict]) -> str:
        """Formatear memorias relevantes para el prompt"""
        if not memories:
            return "No relevant memories"
        
        formatted = []
        for memory in memories[:3]:  # Top 3 memorias más relevantes
            relevance = memory.get('relevance', 0.0)
            content = memory.get('content', '')
            formatted.append(f"- (Relevance: {relevance:.2f}) {content}")
        
        return "\n".join(formatted)
    
    async def _call_openai(self, prompt: str) -> Dict[str, Any]:
        """Llamar a OpenAI con manejo de errores"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative, intelligent adventure game narrator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Intentar parsear como JSON
            try:
                return json.loads(content)
            except:
                # Si no es JSON válido, crear estructura
                return {
                    "narrative": content,
                    "suggestions": ["continue", "explore", "examine surroundings"],
                    "generated_elements": {}
                }
                
        except Exception as e:
            logger.error(f"❌ OpenAI API error: {e}")
            raise
    
    def _enhance_response(self, response: Dict[str, Any], context: AIContext) -> Dict[str, Any]:
        """Mejorar respuesta con análisis adicional"""
        
        enhanced = {
            "content": response.get("narrative", ""),
            "confidence": 0.85,  # Calcular basado en contexto
            "suggestions": response.get("suggestions", []),
            "context_used": [
                f"Location: {context.current_location}",
                f"Recent events: {len(context.recent_events)}",
                f"Memories: {len(context.relevant_memories)}"
            ],
            "generated_content": response.get("generated_elements", {})
        }
        
        return enhanced
    
    def _update_narrative_memory(self, input_text: str, response_text: str):
        """Actualizar memoria narrativa para coherencia"""
        self.narrative_memory.append({
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "response": response_text
        })
        
        # Mantener solo últimas 20 interacciones
        if len(self.narrative_memory) > 20:
            self.narrative_memory = self.narrative_memory[-20:]
    
    def _fallback_response(self, user_input: str) -> AIResponse:
        """Respuesta de fallback en caso de error"""
        return AIResponse(
            content=f"I notice you said '{user_input}'. Let me think about that for a moment...",
            confidence=0.3,
            suggestions=["try again", "be more specific", "use help command"],
            context_used=["fallback mode"],
            generated_content={},
            personality_applied=self.personality,
            processing_time=0.1
        )

class PredictiveEngine:
    """Motor de predicción para gameplay inteligente"""
    
    def __init__(self, memory_system: PerfectMemorySystem):
        self.memory = memory_system
        self.player_patterns = {}
        self.world_trends = {}
        
        logger.info("🔮 Predictive Engine initialized")
    
    async def analyze_player_behavior(self, player_id: str) -> Dict[str, Any]:
        """Analizar patrones de comportamiento del jugador"""
        
        # Obtener historial del jugador
        events = await self.memory.get_events_by_actor(player_id, limit=100)
        
        analysis = {
            "preferred_actions": {},
            "location_preferences": {},
            "time_patterns": {},
            "engagement_level": 0.0,
            "play_style": "unknown",
            "predicted_next_actions": []
        }
        
        if not events:
            return analysis
        
        # Analizar acciones preferidas
        action_counts = {}
        location_counts = {}
        
        for event in events:
            action = event.get('action_type', 'unknown')
            location = event.get('location_id', 'unknown')
            
            action_counts[action] = action_counts.get(action, 0) + 1
            location_counts[location] = location_counts.get(location, 0) + 1
        
        # Calcular preferencias
        total_actions = len(events)
        analysis["preferred_actions"] = {
            action: count / total_actions 
            for action, count in action_counts.items()
        }
        
        analysis["location_preferences"] = {
            location: count / total_actions
            for location, count in location_counts.items()
        }
        
        # Determinar estilo de juego
        analysis["play_style"] = self._determine_play_style(analysis["preferred_actions"])
        
        # Predecir próximas acciones
        analysis["predicted_next_actions"] = self._predict_next_actions(
            analysis["preferred_actions"], 
            analysis["play_style"]
        )
        
        logger.info(f"🔮 Player behavior analyzed: {analysis['play_style']}")
        return analysis
    
    def _determine_play_style(self, preferred_actions: Dict[str, float]) -> str:
        """Determinar estilo de juego basado en acciones"""
        
        if preferred_actions.get('explore', 0) > 0.4:
            return "explorer"
        elif preferred_actions.get('interact', 0) > 0.3:
            return "social"
        elif preferred_actions.get('create', 0) > 0.2:
            return "creator"
        elif preferred_actions.get('observe', 0) > 0.3:
            return "observer"
        else:
            return "balanced"
    
    def _predict_next_actions(self, preferred_actions: Dict[str, float], play_style: str) -> List[str]:
        """Predecir próximas acciones basadas en patrones"""
        
        style_suggestions = {
            "explorer": ["explore new area", "go to unvisited location", "search for hidden paths"],
            "social": ["talk to NPCs", "interact with characters", "join conversations"],
            "creator": ["create new object", "build something", "craft items"],
            "observer": ["examine environment", "look around carefully", "analyze objects"],
            "balanced": ["continue current quest", "check inventory", "explore nearby"]
        }
        
        return style_suggestions.get(play_style, style_suggestions["balanced"])

class AIEngine:
    """Motor principal de IA que coordina todos los componentes"""
    
    def __init__(self, memory_system: PerfectMemorySystem, openai_api_key: str):
        self.memory = memory_system
        self.rag_system = EnhancedRAGSystem(memory_system)
        self.nlp_processor = NLPProcessor()
        self.narrator = SmartNarrator(openai_api_key)
        self.predictor = PredictiveEngine(memory_system)
        
        # Estado del motor
        self.active_contexts = {}
        self.processing_stats = {
            "total_requests": 0,
            "avg_response_time": 0.0,
            "successful_responses": 0
        }
        
        logger.info("🧠 AI Engine Core initialized successfully")
    
    async def process_player_input(self, player_id: str, input_text: str, 
                                 location_id: str) -> AIResponse:
        """Procesar entrada del jugador con IA completa"""
        
        start_time = datetime.now()
        self.processing_stats["total_requests"] += 1
        
        try:
            # 1. Analizar comando con NLP
            command_analysis = await self.nlp_processor.parse_command(input_text)
            
            # 2. Buscar memorias relevantes
            relevant_memories = await self.rag_system.semantic_search(
                input_text, limit=5, relevance_threshold=0.6
            )
            
            # 3. Obtener eventos recientes
            recent_events = await self.memory.get_recent_events(location_id, limit=10)
            
            # 4. Analizar comportamiento del jugador
            player_analysis = await self.predictor.analyze_player_behavior(player_id)
            
            # 5. Construir contexto completo
            context = AIContext(
                current_location=location_id,
                recent_events=recent_events,
                relevant_memories=relevant_memories,
                player_mood=command_analysis["emotion"],
                narrative_state="active",
                conversation_history=self.active_contexts.get(player_id, []),
                world_state=await self._get_world_state(location_id),
                player_preferences=player_analysis
            )
            
            # 6. Generar respuesta inteligente
            ai_response = await self.narrator.generate_response(context, input_text)
            
            # 7. Actualizar contexto activo
            self._update_active_context(player_id, input_text, ai_response.content)
            
            # 8. Agregar nueva memoria
            await self.rag_system.add_memory_embedding(
                f"Player {player_id}: {input_text} -> {ai_response.content}",
                "conversations",
                {
                    "player_id": player_id,
                    "location_id": location_id,
                    "intent": command_analysis["intent"],
                    "confidence": ai_response.confidence
                }
            )
            
            # 9. Actualizar estadísticas
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(processing_time, True)
            
            logger.info(f"🧠 AI processed input in {processing_time:.2f}s")
            return ai_response
            
        except Exception as e:
            logger.error(f"❌ Error processing player input: {e}")
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(processing_time, False)
            
            return AIResponse(
                content="I'm having trouble understanding that right now. Could you try rephrasing?",
                confidence=0.1,
                suggestions=["try again", "use simpler words", "type 'help'"],
                context_used=["error recovery"],
                generated_content={},
                personality_applied=AIPersonality.FRIENDLY,
                processing_time=processing_time
            )
    
    async def _get_world_state(self, location_id: str) -> Dict[str, Any]:
        """Obtener estado actual del mundo"""
        
        # Obtener objetos en la ubicación
        objects = await self.memory.get_objects_in_location(location_id)
        
        # Obtener información de la ubicación
        location_info = await self.memory.get_location_info(location_id)
        
        return {
            "location": location_info,
            "objects_present": [obj.to_dict() for obj in objects],
            "timestamp": datetime.now().isoformat(),
            "weather": "clear",  # TODO: Implementar sistema de clima
            "time_of_day": "day"  # TODO: Implementar ciclo día/noche
        }
    
    def _update_active_context(self, player_id: str, input_text: str, response: str):
        """Actualizar contexto activo del jugador"""
        if player_id not in self.active_contexts:
            self.active_contexts[player_id] = []
        
        self.active_contexts[player_id].append({
            "timestamp": datetime.now().isoformat(),
            "input": input_text,
            "response": response
        })
        
        # Mantener solo últimas 10 interacciones
        if len(self.active_contexts[player_id]) > 10:
            self.active_contexts[player_id] = self.active_contexts[player_id][-10:]
    
    def _update_stats(self, processing_time: float, success: bool):
        """Actualizar estadísticas de rendimiento"""
        if success:
            self.processing_stats["successful_responses"] += 1
        
        # Calcular tiempo promedio
        total_time = (self.processing_stats["avg_response_time"] * 
                     (self.processing_stats["total_requests"] - 1) + processing_time)
        self.processing_stats["avg_response_time"] = total_time / self.processing_stats["total_requests"]
    
    async def get_ai_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del motor de IA"""
        success_rate = (self.processing_stats["successful_responses"] / 
                       max(self.processing_stats["total_requests"], 1)) * 100
        
        return {
            **self.processing_stats,
            "success_rate": success_rate,
            "active_players": len(self.active_contexts),
            "memory_collections": len(self.rag_system.collections),
            "narrator_personality": self.narrator.personality.value
        }

# Función de inicialización para uso externo
async def initialize_ai_engine(memory_system: PerfectMemorySystem, 
                              openai_api_key: str) -> AIEngine:
    """Inicializar motor de IA completo"""
    
    logger.info("🚀 Initializing AI Engine...")
    
    try:
        engine = AIEngine(memory_system, openai_api_key)
        
        logger.info("✅ AI Engine initialized successfully!")
        logger.info("🧠 Features available:")
        logger.info("  - Enhanced RAG with semantic search")
        logger.info("  - Natural Language Processing")
        logger.info("  - Smart narrative generation")
        logger.info("  - Predictive gameplay analysis")
        logger.info("  - Multi-personality narrator")
        
        return engine
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize AI Engine: {e}")
        raise

if __name__ == "__main__":
    # Demo del AI Engine
    import os
    from memory_system import PerfectMemorySystem
    
    async def demo():
        # Configurar
        memory = PerfectMemorySystem("ai_demo.db")
        openai_key = os.getenv("OPENAI_API_KEY", "demo-key")
        
        # Inicializar
        ai_engine = await initialize_ai_engine(memory, openai_key)
        
        # Demo
        response = await ai_engine.process_player_input(
            "demo_player", 
            "I want to explore the mysterious forest", 
            "starting_location"
        )
        
        print(f"🧠 AI Response: {response.content}")
        print(f"🎯 Suggestions: {response.suggestions}")
        print(f"⚡ Processing time: {response.processing_time:.2f}s")
        
        # Estadísticas
        stats = await ai_engine.get_ai_stats()
        print(f"📊 AI Stats: {stats}")
    
    # Ejecutar demo
    asyncio.run(demo())
