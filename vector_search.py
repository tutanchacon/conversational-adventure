"""
Sistema de Búsqueda Vectorial para Adventure Game
Implementa búsqueda semántica usando ChromaDB y embeddings
Parte de la v1.1.0 - Vector Search
"""

import asyncio
import json
import logging
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path


@dataclass
class VectorDocument:
    """Documento vectorizado para búsqueda semántica"""
    id: str
    content: str
    metadata: Dict[str, Any]
    object_id: Optional[str] = None
    location_id: Optional[str] = None
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    document_type: str = "general"  # object, location, event, action


@dataclass 
class SearchResult:
    """Resultado de búsqueda vectorial"""
    document: VectorDocument
    similarity_score: float
    context: Dict[str, Any]


class VectorSearchEngine:
    """
    Motor de búsqueda vectorial para el adventure game
    
    Características:
    - Embeddings automáticos de objetos, ubicaciones y eventos
    - Búsqueda semántica natural
    - Análisis de patrones y relaciones
    - Integración con sistema de memoria perfecta
    """
    
    def __init__(self, db_path: str = "adventure_game.db", 
                 vector_db_path: str = "./vector_db"):
        self.db_path = db_path
        self.vector_db_path = Path(vector_db_path)
        self.vector_db_path.mkdir(exist_ok=True)
        
        # Configurar ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.vector_db_path),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Modelo de embeddings - optimizado para español e inglés
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Colecciones separadas por tipo
        self.collections = {
            'objects': self._get_or_create_collection('game_objects'),
            'locations': self._get_or_create_collection('game_locations'),
            'events': self._get_or_create_collection('game_events'),
            'actions': self._get_or_create_collection('game_actions')
        }
        
        self.logger = logging.getLogger(__name__)
        
    def _get_or_create_collection(self, name: str):
        """Obtiene o crea una colección en ChromaDB"""
        try:
            return self.chroma_client.get_collection(name)
        except Exception:
            return self.chroma_client.create_collection(
                name=name,
                metadata={"description": f"Vector embeddings for {name}"}
            )
    
    async def initialize_from_existing_data(self):
        """
        Inicializa el índice vectorial desde datos existentes en SQLite
        Convierte todo el historial en embeddings vectoriales
        """
        self.logger.info("🔄 Inicializando índice vectorial desde datos existentes...")
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # Procesar objetos existentes
            await self._process_existing_objects(conn)
            
            # Procesar ubicaciones existentes  
            await self._process_existing_locations(conn)
            
            # Procesar eventos históricos
            await self._process_existing_events(conn)
            
            self.logger.info("✅ Índice vectorial inicializado correctamente")
            
        except Exception as e:
            self.logger.error(f"❌ Error inicializando índice vectorial: {e}")
            raise
        finally:
            conn.close()
    
    async def _process_existing_objects(self, conn):
        """Procesa objetos existentes y los convierte en vectores"""
        cursor = conn.execute("""
            SELECT object_id, name, description, properties, location_id, 
                   created_at, version
            FROM game_objects 
            WHERE is_current = 1
        """)
        
        documents = []
        metadatas = []
        ids = []
        
        for row in cursor:
            # Crear contenido textual rico para embedding
            properties = json.loads(row['properties'] or '{}')
            content_parts = [
                f"Nombre: {row['name']}",
                f"Descripción: {row['description'] or 'Sin descripción'}"
            ]
            
            # Agregar propiedades importantes al texto
            for key, value in properties.items():
                if value and str(value).strip():
                    content_parts.append(f"{key}: {value}")
            
            content = " | ".join(content_parts)
            
            # Metadata para búsqueda y filtrado
            metadata = {
                'object_id': row['object_id'],
                'name': row['name'],
                'location_id': row['location_id'],
                'created_at': row['created_at'],
                'version': row['version'],
                'type': 'object',
                'properties': properties
            }
            
            documents.append(content)
            metadatas.append(metadata)
            ids.append(f"obj_{row['object_id']}_{row['version']}")
        
        if documents:
            # Generar embeddings y almacenar
            embeddings = self.embedding_model.encode(documents).tolist()
            
            self.collections['objects'].add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"📦 Procesados {len(documents)} objetos")
    
    async def _process_existing_locations(self, conn):
        """Procesa ubicaciones existentes"""
        cursor = conn.execute("""
            SELECT location_id, name, description, connections
            FROM locations
        """)
        
        documents = []
        metadatas = []
        ids = []
        
        for row in cursor:
            connections = json.loads(row['connections'] or '{}')
            
            content_parts = [
                f"Ubicación: {row['name']}",
                f"Descripción: {row['description'] or 'Sin descripción'}"
            ]
            
            if connections:
                connected_places = ", ".join(connections.keys())
                content_parts.append(f"Conectada con: {connected_places}")
            
            content = " | ".join(content_parts)
            
            metadata = {
                'location_id': row['location_id'],
                'name': row['name'],
                'type': 'location',
                'connections': connections
            }
            
            documents.append(content)
            metadatas.append(metadata)
            ids.append(f"loc_{row['location_id']}")
        
        if documents:
            embeddings = self.embedding_model.encode(documents).tolist()
            
            self.collections['locations'].add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"🏠 Procesadas {len(documents)} ubicaciones")
    
    async def _process_existing_events(self, conn):
        """Procesa eventos históricos"""
        cursor = conn.execute("""
            SELECT event_id, event_type, object_id, location_id, 
                   event_data, timestamp
            FROM game_events
            ORDER BY timestamp DESC
            LIMIT 10000  -- Limitamos para no sobrecargar
        """)
        
        documents = []
        metadatas = []
        ids = []
        
        for row in cursor:
            event_data = json.loads(row['event_data'] or '{}')
            
            content_parts = [
                f"Evento: {row['event_type']}",
                f"Timestamp: {row['timestamp']}"
            ]
            
            if row['object_id']:
                content_parts.append(f"Objeto: {row['object_id']}")
            
            if row['location_id']:
                content_parts.append(f"Ubicación: {row['location_id']}")
            
            # Agregar datos específicos del evento
            for key, value in event_data.items():
                if value and str(value).strip():
                    content_parts.append(f"{key}: {value}")
            
            content = " | ".join(content_parts)
            
            metadata = {
                'event_id': row['event_id'],
                'event_type': row['event_type'],
                'object_id': row['object_id'],
                'location_id': row['location_id'],
                'timestamp': row['timestamp'],
                'type': 'event',
                'event_data': event_data
            }
            
            documents.append(content)
            metadatas.append(metadata)
            ids.append(f"evt_{row['event_id']}")
        
        if documents:
            embeddings = self.embedding_model.encode(documents).tolist()
            
            self.collections['events'].add(
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"📅 Procesados {len(documents)} eventos")
    
    async def search_objects(self, query: str, limit: int = 10, 
                           filters: Optional[Dict] = None) -> List[SearchResult]:
        """
        Busca objetos usando búsqueda semántica
        
        Ejemplos:
        - "herramientas de carpintería"
        - "objetos metálicos oxidados"
        - "cosas similares a un martillo"
        """
        return await self._search_in_collection('objects', query, limit, filters)
    
    async def search_locations(self, query: str, limit: int = 10,
                             filters: Optional[Dict] = None) -> List[SearchResult]:
        """
        Busca ubicaciones usando descripción semántica
        
        Ejemplos:
        - "lugares para trabajar madera"
        - "espacios cerrados y húmedos"
        - "talleres o almacenes"
        """
        return await self._search_in_collection('locations', query, limit, filters)
    
    async def search_events(self, query: str, limit: int = 10,
                          filters: Optional[Dict] = None) -> List[SearchResult]:
        """
        Busca eventos históricos semánticamente
        
        Ejemplos:
        - "cuando se movió el martillo"
        - "eventos de oxidación"
        - "acciones de carpintería"
        """
        return await self._search_in_collection('events', query, limit, filters)
    
    async def search_all(self, query: str, limit: int = 20) -> Dict[str, List[SearchResult]]:
        """
        Búsqueda global en todas las colecciones
        Retorna resultados organizados por tipo
        """
        results = {}
        
        for collection_type in ['objects', 'locations', 'events']:
            try:
                results[collection_type] = await self._search_in_collection(
                    collection_type, query, limit//3
                )
            except Exception as e:
                self.logger.error(f"Error buscando en {collection_type}: {e}")
                results[collection_type] = []
        
        return results
    
    async def _search_in_collection(self, collection_type: str, query: str, 
                                  limit: int, filters: Optional[Dict] = None) -> List[SearchResult]:
        """Realiza búsqueda vectorial en una colección específica"""
        try:
            collection = self.collections[collection_type]
            
            # Generar embedding de la consulta
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Construir filtros de metadata
            where_clause = {}
            if filters:
                where_clause.update(filters)
            
            # Realizar búsqueda vectorial
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=limit,
                where=where_clause if where_clause else None,
                include=['metadatas', 'documents', 'distances']
            )
            
            # Convertir resultados
            search_results = []
            if results['ids'][0]:  # Si hay resultados
                for i, doc_id in enumerate(results['ids'][0]):
                    document = VectorDocument(
                        id=doc_id,
                        content=results['documents'][0][i],
                        metadata=results['metadatas'][0][i],
                        document_type=collection_type
                    )
                    
                    # ChromaDB retorna distancias (menor = más similar)
                    # Convertir a score de similitud (mayor = más similar)
                    distance = results['distances'][0][i]
                    similarity_score = max(0, 1.0 - distance)
                    
                    search_result = SearchResult(
                        document=document,
                        similarity_score=similarity_score,
                        context={'collection': collection_type, 'query': query}
                    )
                    
                    search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            self.logger.error(f"Error en búsqueda vectorial: {e}")
            return []
    
    async def find_similar_objects(self, object_id: str, limit: int = 5) -> List[SearchResult]:
        """
        Encuentra objetos similares a uno dado
        Útil para recomendaciones y análisis de patrones
        """
        # Obtener el objeto de referencia
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            cursor = conn.execute("""
                SELECT name, description, properties
                FROM game_objects 
                WHERE object_id = ? AND is_current = 1
            """, (object_id,))
            
            row = cursor.fetchone()
            if not row:
                return []
            
            # Crear consulta basada en el objeto
            properties = json.loads(row['properties'] or '{}')
            query_parts = [row['name']]
            
            if row['description']:
                query_parts.append(row['description'])
            
            # Agregar propiedades importantes
            important_props = ['material', 'tipo', 'color', 'estado', 'uso']
            for prop in important_props:
                if prop in properties and properties[prop]:
                    query_parts.append(str(properties[prop]))
            
            query = " ".join(query_parts)
            
            # Buscar objetos similares (excluyendo el mismo objeto)
            results = await self.search_objects(query, limit + 1)
            
            # Filtrar el objeto original
            similar_results = [
                r for r in results 
                if r.document.metadata.get('object_id') != object_id
            ]
            
            return similar_results[:limit]
            
        finally:
            conn.close()
    
    async def analyze_location_patterns(self, location_id: str) -> Dict[str, Any]:
        """
        Analiza patrones de objetos en una ubicación
        Identifica qué tipos de objetos aparecen frecuentemente juntos
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        
        try:
            # Obtener objetos que han estado en esta ubicación
            cursor = conn.execute("""
                SELECT DISTINCT o.name, o.description, o.properties
                FROM game_objects o
                JOIN game_events e ON o.object_id = e.object_id
                WHERE e.location_id = ? OR o.location_id = ?
            """, (location_id, location_id))
            
            objects_in_location = []
            for row in cursor:
                properties = json.loads(row['properties'] or '{}')
                objects_in_location.append({
                    'name': row['name'],
                    'description': row['description'],
                    'properties': properties
                })
            
            if not objects_in_location:
                return {'patterns': [], 'summary': 'No hay suficientes datos'}
            
            # Analizar patrones usando embeddings
            object_texts = []
            for obj in objects_in_location:
                text_parts = [obj['name']]
                if obj['description']:
                    text_parts.append(obj['description'])
                
                # Agregar propiedades importantes
                for key, value in obj['properties'].items():
                    if value and str(value).strip():
                        text_parts.append(f"{key}:{value}")
                
                object_texts.append(" ".join(text_parts))
            
            if len(object_texts) < 2:
                return {'patterns': [], 'summary': 'Necesarios más objetos para análisis'}
            
            # Generar embeddings para análisis de clusters
            embeddings = self.embedding_model.encode(object_texts)
            
            # Análisis simple de similitud
            from sklearn.metrics.pairwise import cosine_similarity
            similarity_matrix = cosine_similarity(embeddings)
            
            # Encontrar pares de objetos más similares
            patterns = []
            n_objects = len(object_texts)
            
            for i in range(n_objects):
                for j in range(i+1, n_objects):
                    similarity = similarity_matrix[i][j]
                    if similarity > 0.3:  # Umbral de similitud
                        patterns.append({
                            'object1': objects_in_location[i]['name'],
                            'object2': objects_in_location[j]['name'],
                            'similarity': float(similarity),
                            'pattern_type': 'semantic_similarity'
                        })
            
            # Ordenar por similitud
            patterns.sort(key=lambda x: x['similarity'], reverse=True)
            
            return {
                'patterns': patterns[:10],  # Top 10 patrones
                'total_objects': n_objects,
                'summary': f'Encontrados {len(patterns)} patrones de similitud en {n_objects} objetos'
            }
            
        except Exception as e:
            self.logger.error(f"Error analizando patrones: {e}")
            return {'patterns': [], 'summary': f'Error en análisis: {e}'}
        finally:
            conn.close()
    
    async def add_object_to_index(self, object_id: str, name: str, 
                                 description: str, properties: Dict[str, Any],
                                 location_id: str, version: int):
        """Agregar nuevo objeto al índice vectorial"""
        try:
            content_parts = [f"Nombre: {name}"]
            
            if description:
                content_parts.append(f"Descripción: {description}")
            
            for key, value in properties.items():
                if value and str(value).strip():
                    content_parts.append(f"{key}: {value}")
            
            content = " | ".join(content_parts)
            
            metadata = {
                'object_id': object_id,
                'name': name,
                'location_id': location_id,
                'version': version,
                'type': 'object',
                'properties': properties,
                'created_at': datetime.now().isoformat()
            }
            
            embedding = self.embedding_model.encode([content]).tolist()[0]
            doc_id = f"obj_{object_id}_{version}"
            
            self.collections['objects'].add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            self.logger.info(f"✅ Objeto {name} agregado al índice vectorial")
            
        except Exception as e:
            self.logger.error(f"Error agregando objeto al índice: {e}")
    
    async def add_event_to_index(self, event_id: str, event_type: str,
                               object_id: str, location_id: str,
                               event_data: Dict[str, Any], timestamp: str):
        """Agregar nuevo evento al índice vectorial"""
        try:
            content_parts = [
                f"Evento: {event_type}",
                f"Timestamp: {timestamp}"
            ]
            
            if object_id:
                content_parts.append(f"Objeto: {object_id}")
            
            if location_id:
                content_parts.append(f"Ubicación: {location_id}")
            
            for key, value in event_data.items():
                if value and str(value).strip():
                    content_parts.append(f"{key}: {value}")
            
            content = " | ".join(content_parts)
            
            metadata = {
                'event_id': event_id,
                'event_type': event_type,
                'object_id': object_id,
                'location_id': location_id,
                'timestamp': timestamp,
                'type': 'event',
                'event_data': event_data
            }
            
            embedding = self.embedding_model.encode([content]).tolist()[0]
            doc_id = f"evt_{event_id}"
            
            self.collections['events'].add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
        except Exception as e:
            self.logger.error(f"Error agregando evento al índice: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del índice vectorial"""
        stats = {}
        
        for name, collection in self.collections.items():
            try:
                count = collection.count()
                stats[name] = {
                    'document_count': count,
                    'status': 'active' if count > 0 else 'empty'
                }
            except Exception as e:
                stats[name] = {
                    'document_count': 0,
                    'status': f'error: {e}'
                }
        
        return stats


# Función de utilidad para testing
async def test_vector_search():
    """Función de prueba básica del sistema vectorial"""
    engine = VectorSearchEngine()
    
    print("🔄 Inicializando motor de búsqueda vectorial...")
    await engine.initialize_from_existing_data()
    
    print("\n📊 Estadísticas del índice:")
    stats = engine.get_stats()
    for collection, data in stats.items():
        print(f"  {collection}: {data['document_count']} documentos ({data['status']})")
    
    print("\n🔍 Probando búsqueda de objetos:")
    results = await engine.search_objects("herramientas metálicas", limit=3)
    for result in results:
        print(f"  - {result.document.metadata.get('name', 'Sin nombre')}")
        print(f"    Similitud: {result.similarity_score:.3f}")
        print(f"    Contenido: {result.document.content[:100]}...")
    
    print("\n🏠 Probando búsqueda de ubicaciones:")
    results = await engine.search_locations("taller trabajo", limit=2)
    for result in results:
        print(f"  - {result.document.metadata.get('name', 'Sin nombre')}")
        print(f"    Similitud: {result.similarity_score:.3f}")


if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Ejecutar prueba
    asyncio.run(test_vector_search())
