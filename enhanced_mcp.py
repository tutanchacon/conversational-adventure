"""
Integración MCP Extendida con Búsqueda Vectorial
Extiende el sistema MCP original con capacidades de búsqueda semántica
Versión 1.1.0 - Vector Search Integration
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from mcp_integration import MCPContextProvider
from vector_search import VectorSearchEngine, SearchResult


class EnhancedMCPProvider(MCPContextProvider):
    """
    Proveedor MCP mejorado con búsqueda vectorial
    
    Extiende las capacidades originales con:
    - Búsqueda semántica de objetos, ubicaciones y eventos
    - Análisis de patrones y relaciones
    - Contexto enriquecido para IA basado en similitud
    - Recomendaciones inteligentes
    """
    
    def __init__(self, memory_system, db_path: str = "adventure_game.db"):
        super().__init__(memory_system, db_path)
        
        # Inicializar motor de búsqueda vectorial
        self.vector_engine = VectorSearchEngine(db_path)
        self.vector_initialized = False
        
        self.logger = logging.getLogger(__name__)
    
    async def initialize_vector_search(self):
        """Inicializar sistema de búsqueda vectorial"""
        if not self.vector_initialized:
            try:
                self.logger.info("🔄 Inicializando búsqueda vectorial...")
                await self.vector_engine.initialize_from_existing_data()
                self.vector_initialized = True
                self.logger.info("✅ Búsqueda vectorial inicializada")
            except Exception as e:
                self.logger.error(f"❌ Error inicializando búsqueda vectorial: {e}")
                self.vector_initialized = False
    
    async def generate_enhanced_world_context_for_ai(self, current_location: str, 
                                                   player_inventory: List[str],
                                                   recent_actions: List[str] = None) -> str:
        """
        Genera contexto enriquecido para IA con búsqueda vectorial
        
        Incluye:
        - Contexto básico original
        - Objetos semánticamente relacionados
        - Patrones de ubicación
        - Sugerencias basadas en similitud
        """
        
        # Asegurar que vector search esté inicializado
        await self.initialize_vector_search()
        
        # Obtener contexto base original
        base_context = await self.generate_world_context_for_ai(
            current_location, player_inventory, recent_actions
        )
        
        if not self.vector_initialized:
            return base_context + "\n\n[Búsqueda vectorial no disponible]"
        
        try:
            # Contexto vectorial enriquecido
            vector_context = await self._generate_vector_context(
                current_location, player_inventory, recent_actions or []
            )
            
            return f"""{base_context}

=== ANÁLISIS SEMÁNTICO AVANZADO ===
{vector_context}

=== INSTRUCCIONES PARA IA ===
Tienes acceso a búsqueda semántica avanzada. Puedes:
- Encontrar objetos similares: "objetos parecidos al martillo"
- Buscar por función: "herramientas de carpintería"
- Analizar patrones: "qué objetos aparecen juntos frecuentemente"
- Búsqueda contextual: "objetos relacionados con construcción"

Usa esta información para proporcionar respuestas más ricas y contextualmente relevantes."""
            
        except Exception as e:
            self.logger.error(f"Error generando contexto vectorial: {e}")
            return base_context + f"\n\n[Error en análisis semántico: {e}]"
    
    async def _generate_vector_context(self, current_location: str,
                                     player_inventory: List[str],
                                     recent_actions: List[str]) -> str:
        """Genera contexto específico basado en búsqueda vectorial"""
        
        context_parts = []
        
        # 1. Análisis de objetos en inventario
        if player_inventory:
            inventory_context = await self._analyze_inventory_context(player_inventory)
            if inventory_context:
                context_parts.append(f"🎒 ANÁLISIS DE INVENTARIO:\n{inventory_context}")
        
        # 2. Análisis de patrones de ubicación actual
        location_patterns = await self._analyze_current_location_patterns(current_location)
        if location_patterns:
            context_parts.append(f"🏠 PATRONES DE UBICACIÓN:\n{location_patterns}")
        
        # 3. Análisis de acciones recientes
        if recent_actions:
            action_context = await self._analyze_recent_actions_context(recent_actions)
            if action_context:
                context_parts.append(f"⚡ CONTEXTO DE ACCIONES:\n{action_context}")
        
        # 4. Sugerencias semánticas
        suggestions = await self._generate_semantic_suggestions(
            current_location, player_inventory, recent_actions
        )
        if suggestions:
            context_parts.append(f"💡 SUGERENCIAS SEMÁNTICAS:\n{suggestions}")
        
        return "\n\n".join(context_parts) if context_parts else "Sin contexto vectorial adicional disponible."
    
    async def _analyze_inventory_context(self, inventory: List[str]) -> str:
        """Analiza el inventario usando búsqueda vectorial"""
        analysis_parts = []
        
        for object_id in inventory[:5]:  # Limitar a 5 objetos principales
            try:
                # Encontrar objetos similares
                similar_objects = await self.vector_engine.find_similar_objects(object_id, limit=3)
                
                if similar_objects:
                    object_info = await self.get_object_context(object_id)
                    object_name = object_info.split(':')[0] if ':' in object_info else object_id
                    
                    similar_names = [
                        result.document.metadata.get('name', 'Sin nombre')
                        for result in similar_objects
                    ]
                    
                    analysis_parts.append(
                        f"  • {object_name}: Similar a {', '.join(similar_names[:2])}"
                    )
                    
            except Exception as e:
                self.logger.debug(f"Error analizando objeto {object_id}: {e}")
        
        return "\n".join(analysis_parts) if analysis_parts else "Sin análisis de similitud disponible."
    
    async def _analyze_current_location_patterns(self, location_id: str) -> str:
        """Analiza patrones de la ubicación actual"""
        try:
            patterns = await self.vector_engine.analyze_location_patterns(location_id)
            
            if not patterns['patterns']:
                return "Sin patrones detectados en esta ubicación."
            
            pattern_descriptions = []
            for pattern in patterns['patterns'][:3]:  # Top 3 patrones
                pattern_descriptions.append(
                    f"  • {pattern['object1']} ↔ {pattern['object2']} "
                    f"(similitud: {pattern['similarity']:.2f})"
                )
            
            return f"Patrones detectados:\n" + "\n".join(pattern_descriptions)
            
        except Exception as e:
            self.logger.debug(f"Error analizando patrones de ubicación: {e}")
            return "Error analizando patrones de ubicación."
    
    async def _analyze_recent_actions_context(self, actions: List[str]) -> str:
        """Analiza el contexto de acciones recientes"""
        if not actions:
            return ""
        
        # Construir consulta semántica basada en acciones
        action_query = " ".join(actions[-3:])  # Últimas 3 acciones
        
        try:
            # Buscar eventos similares en el historial
            similar_events = await self.vector_engine.search_events(action_query, limit=3)
            
            if not similar_events:
                return "Sin eventos similares encontrados en el historial."
            
            event_descriptions = []
            for result in similar_events:
                event_type = result.document.metadata.get('event_type', 'Evento')
                timestamp = result.document.metadata.get('timestamp', 'Fecha desconocida')
                
                event_descriptions.append(
                    f"  • {event_type} en {timestamp[:10]} "
                    f"(similitud: {result.similarity_score:.2f})"
                )
            
            return f"Eventos similares en historial:\n" + "\n".join(event_descriptions)
            
        except Exception as e:
            self.logger.debug(f"Error analizando contexto de acciones: {e}")
            return "Error analizando contexto de acciones."
    
    async def _generate_semantic_suggestions(self, location_id: str,
                                           inventory: List[str],
                                           actions: List[str]) -> str:
        """Genera sugerencias semánticas inteligentes"""
        suggestions = []
        
        try:
            # Sugerencia 1: Objetos relacionados en ubicación actual
            location_objects = await self.vector_engine.search_objects(
                f"objetos ubicación {location_id}", limit=3
            )
            
            if location_objects:
                object_names = [
                    result.document.metadata.get('name', 'objeto')
                    for result in location_objects
                ]
                suggestions.append(f"  • Objetos relevantes aquí: {', '.join(object_names)}")
            
            # Sugerencia 2: Basada en último objeto del inventario
            if inventory:
                last_object = inventory[-1]
                similar_tools = await self.vector_engine.find_similar_objects(last_object, limit=2)
                
                if similar_tools:
                    tool_names = [
                        result.document.metadata.get('name', 'herramienta')
                        for result in similar_tools
                    ]
                    suggestions.append(f"  • Herramientas complementarias: {', '.join(tool_names)}")
            
            # Sugerencia 3: Basada en acciones recientes
            if actions:
                last_action = actions[-1]
                related_locations = await self.vector_engine.search_locations(
                    f"lugares para {last_action}", limit=2
                )
                
                if related_locations:
                    location_names = [
                        result.document.metadata.get('name', 'lugar')
                        for result in related_locations
                    ]
                    suggestions.append(f"  • Lugares relevantes: {', '.join(location_names)}")
            
        except Exception as e:
            self.logger.debug(f"Error generando sugerencias: {e}")
        
        return "\n".join(suggestions) if suggestions else "Sin sugerencias disponibles."
    
    async def search_objects_by_description(self, description: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Busca objetos por descripción en lenguaje natural
        
        Ejemplos:
        - "herramientas de metal oxidadas"
        - "objetos para construir"
        - "cosas similares a un martillo"
        """
        await self.initialize_vector_search()
        
        if not self.vector_initialized:
            return []
        
        try:
            results = await self.vector_engine.search_objects(description, limit)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    'object_id': result.document.metadata.get('object_id'),
                    'name': result.document.metadata.get('name'),
                    'location_id': result.document.metadata.get('location_id'),
                    'similarity_score': result.similarity_score,
                    'description': result.document.content,
                    'properties': result.document.metadata.get('properties', {})
                })
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda por descripción: {e}")
            return []
    
    async def find_objects_by_pattern(self, pattern_description: str) -> List[Dict[str, Any]]:
        """
        Encuentra objetos basado en patrones de uso
        
        Ejemplos:
        - "objetos que se usan para carpintería"
        - "herramientas que se oxidan"
        - "cosas que se guardan en talleres"
        """
        # Usar búsqueda global para encontrar patrones
        await self.initialize_vector_search()
        
        if not self.vector_initialized:
            return []
        
        try:
            # Buscar en objetos y eventos relacionados
            all_results = await self.vector_engine.search_all(pattern_description, limit=20)
            
            # Consolidar resultados de objetos
            object_results = all_results.get('objects', [])
            
            # Agregar objetos relacionados encontrados en eventos
            event_results = all_results.get('events', [])
            related_object_ids = set()
            
            for event_result in event_results:
                object_id = event_result.document.metadata.get('object_id')
                if object_id:
                    related_object_ids.add(object_id)
            
            # Buscar información de objetos relacionados
            for object_id in related_object_ids:
                try:
                    object_search = await self.vector_engine.search_objects(f"object_id:{object_id}", limit=1)
                    if object_search:
                        object_results.extend(object_search)
                except:
                    continue
            
            # Formatear y deduplicar resultados
            seen_objects = set()
            formatted_results = []
            
            for result in object_results:
                object_id = result.document.metadata.get('object_id')
                if object_id not in seen_objects:
                    seen_objects.add(object_id)
                    formatted_results.append({
                        'object_id': object_id,
                        'name': result.document.metadata.get('name'),
                        'location_id': result.document.metadata.get('location_id'),
                        'similarity_score': result.similarity_score,
                        'match_reason': 'pattern_analysis',
                        'properties': result.document.metadata.get('properties', {})
                    })
            
            # Ordenar por relevancia
            formatted_results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return formatted_results[:10]  # Top 10 resultados
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda por patrones: {e}")
            return []
    
    async def get_vector_search_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de búsqueda vectorial"""
        await self.initialize_vector_search()
        
        if not self.vector_initialized:
            return {'status': 'not_initialized', 'error': 'Vector search not available'}
        
        try:
            stats = self.vector_engine.get_stats()
            stats['status'] = 'active'
            stats['initialized'] = True
            return stats
        except Exception as e:
            return {'status': 'error', 'error': str(e)}


# Funciones de utilidad para integración
async def search_objects_naturally(enhanced_mcp: EnhancedMCPProvider, 
                                 query: str) -> List[Dict[str, Any]]:
    """
    Función helper para búsqueda natural de objetos
    Simplifica el uso desde el motor de juego principal
    """
    return await enhanced_mcp.search_objects_by_description(query)


async def find_related_objects(enhanced_mcp: EnhancedMCPProvider,
                             object_id: str) -> List[Dict[str, Any]]:
    """
    Función helper para encontrar objetos relacionados
    """
    await enhanced_mcp.initialize_vector_search()
    
    if not enhanced_mcp.vector_initialized:
        return []
    
    try:
        similar_results = await enhanced_mcp.vector_engine.find_similar_objects(object_id)
        
        return [
            {
                'object_id': result.document.metadata.get('object_id'),
                'name': result.document.metadata.get('name'),
                'similarity_score': result.similarity_score,
                'reason': 'semantic_similarity'
            }
            for result in similar_results
        ]
        
    except Exception as e:
        logging.error(f"Error finding related objects: {e}")
        return []


# Función de testing
async def test_enhanced_mcp():
    """Prueba la funcionalidad extendida del MCP"""
    from memory_system import PerfectMemorySystem
    
    print("🧪 Testing Enhanced MCP with Vector Search...")
    
    # Inicializar sistemas
    memory = PerfectMemorySystem()
    enhanced_mcp = EnhancedMCPProvider(memory)
    
    # Inicializar búsqueda vectorial
    await enhanced_mcp.initialize_vector_search()
    
    # Obtener estadísticas
    stats = await enhanced_mcp.get_vector_search_stats()
    print(f"📊 Vector search stats: {stats}")
    
    # Probar búsqueda de objetos
    print("\n🔍 Testing object search:")
    results = await enhanced_mcp.search_objects_by_description("herramientas metálicas")
    for result in results[:3]:
        print(f"  - {result['name']} (score: {result['similarity_score']:.3f})")
    
    # Probar búsqueda por patrones
    print("\n🎯 Testing pattern search:")
    pattern_results = await enhanced_mcp.find_objects_by_pattern("objetos de carpintería")
    for result in pattern_results[:3]:
        print(f"  - {result['name']} (score: {result['similarity_score']:.3f})")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    asyncio.run(test_enhanced_mcp())
