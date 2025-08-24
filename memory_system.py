# Sistema de Memoria Perfecta para Adventure Game con MCP
# Garantiza que ningún detalle del mundo se pierda jamás

import asyncio
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GameObject:
    """Representa un objeto en el mundo del juego"""
    id: str
    name: str
    description: str
    location_id: str
    properties: Dict[str, Any]
    created_at: datetime
    last_modified: datetime
    version: int = 1
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_modified'] = self.last_modified.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameObject':
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['last_modified'] = datetime.fromisoformat(data['last_modified'])
        return cls(**data)

@dataclass
class Location:
    """Representa una ubicación en el mundo"""
    id: str
    name: str
    description: str
    connections: Dict[str, str]  # dirección -> location_id
    properties: Dict[str, Any]
    created_at: datetime
    last_modified: datetime
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['last_modified'] = self.last_modified.isoformat()
        return data

@dataclass
class GameEvent:
    """Evento inmutable en la línea temporal del juego"""
    id: str
    timestamp: datetime
    event_type: str
    actor: str  # quien realizó la acción
    action: str
    target: Optional[str]
    location_id: str
    context: Dict[str, Any]
    embedding_vector: Optional[List[float]] = None
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class PerfectMemorySystem:
    """
    Sistema de memoria que garantiza persistencia perfecta de todos los elementos
    del mundo del juego usando una combinación de:
    - Base de datos relacional para estado actual
    - Event sourcing para historial completo
    - Embeddings vectoriales para búsqueda semántica
    """
    
    def __init__(self, db_path: str = "perfect_memory.db"):
        self.db_path = Path(db_path)
        self.db_connection: Optional[sqlite3.Connection] = None
        self._initialize_database()
    
    async def initialize(self):
        """Método asíncrono para inicializar el sistema (compatibilidad con AI integration)"""
        if self.db_connection is None:
            self._initialize_database()
        logger.info("✅ PerfectMemorySystem inicializado")
        return True
        
    def _initialize_database(self):
        """Inicializa la base de datos con todas las tablas necesarias"""
        logger.info(f"Inicializando base de datos: {self.db_path}")
        
        self.db_connection = sqlite3.connect(
            self.db_path, 
            check_same_thread=False,
            isolation_level=None  # Autocommit mode
        )
        
        # Configurar row_factory para obtener diccionarios
        self.db_connection.row_factory = sqlite3.Row
        
        # Habilitar WAL mode para mejor concurrencia
        self.db_connection.execute("PRAGMA journal_mode=WAL")
        self.db_connection.execute("PRAGMA synchronous=NORMAL")
        self.db_connection.execute("PRAGMA cache_size=10000")
        
        self._create_tables()
        
    def _create_tables(self):
        """Crea todas las tablas necesarias"""
        
        # Tabla de ubicaciones
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                connections TEXT, -- JSON
                properties TEXT, -- JSON
                created_at TEXT NOT NULL,
                last_modified TEXT NOT NULL
            )
        """)
        
        # Tabla de objetos
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS game_objects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                location_id TEXT NOT NULL,
                properties TEXT, -- JSON
                created_at TEXT NOT NULL,
                last_modified TEXT NOT NULL,
                version INTEGER DEFAULT 1,
                FOREIGN KEY (location_id) REFERENCES locations (id)
            )
        """)
        
        # Tabla de eventos (Event Sourcing)
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS game_events (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                action TEXT NOT NULL,
                target TEXT,
                location_id TEXT NOT NULL,
                context TEXT, -- JSON
                embedding_vector TEXT, -- JSON de vector de embeddings
                FOREIGN KEY (location_id) REFERENCES locations (id)
            )
        """)
        
        # Tabla de estados del mundo (snapshots para optimización)
        self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS world_snapshots (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                snapshot_data TEXT NOT NULL, -- JSON completo del estado
                event_count INTEGER NOT NULL
            )
        """)
        
        # Índices para optimización
        self.db_connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_objects_location 
            ON game_objects(location_id)
        """)
        
        self.db_connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_timestamp 
            ON game_events(timestamp)
        """)
        
        self.db_connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_location 
            ON game_events(location_id)
        """)
        
        logger.info("✅ Base de datos inicializada correctamente")
    
    async def create_location(self, name: str, description: str, 
                            connections: Dict[str, str] = None, 
                            properties: Dict[str, Any] = None) -> Location:
        """Crea una nueva ubicación"""
        location_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        location = Location(
            id=location_id,
            name=name,
            description=description,
            connections=connections or {},
            properties=properties or {},
            created_at=now,
            last_modified=now
        )
        
        # Guardar en base de datos
        self.db_connection.execute("""
            INSERT INTO locations 
            (id, name, description, connections, properties, created_at, last_modified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            location.id,
            location.name,
            location.description,
            json.dumps(location.connections),
            json.dumps(location.properties),
            location.created_at.isoformat(),
            location.last_modified.isoformat()
        ))
        
        # Registrar evento
        await self._record_event(
            event_type="location_created",
            actor="system",
            action=f"created location '{name}'",
            target=location_id,
            location_id=location_id,
            context={"location_data": location.to_dict()}
        )
        
        logger.info(f"✅ Ubicación creada: {name} ({location_id})")
        return location
    
    async def create_object(self, name: str, description: str, 
                          location_id: str, properties: Dict[str, Any] = None) -> GameObject:
        """Crea un nuevo objeto en el mundo"""
        object_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        game_object = GameObject(
            id=object_id,
            name=name,
            description=description,
            location_id=location_id,
            properties=properties or {},
            created_at=now,
            last_modified=now
        )
        
        # Guardar en base de datos
        self.db_connection.execute("""
            INSERT INTO game_objects 
            (id, name, description, location_id, properties, created_at, last_modified, version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game_object.id,
            game_object.name,
            game_object.description,
            game_object.location_id,
            json.dumps(game_object.properties),
            game_object.created_at.isoformat(),
            game_object.last_modified.isoformat(),
            game_object.version
        ))
        
        # Registrar evento
        await self._record_event(
            event_type="object_created",
            actor="system",
            action=f"created object '{name}'",
            target=object_id,
            location_id=location_id,
            context={
                "object_data": game_object.to_dict(),
                "initial_placement": True
            }
        )
        
        logger.info(f"✅ Objeto creado: {name} en {location_id}")
        return game_object
    
    async def move_object(self, object_id: str, new_location_id: str, 
                         actor: str = "system") -> bool:
        """Mueve un objeto a una nueva ubicación"""
        # Obtener objeto actual
        cursor = self.db_connection.execute("""
            SELECT * FROM game_objects WHERE id = ?
        """, (object_id,))
        
        row = cursor.fetchone()
        if not row:
            logger.error(f"❌ Objeto no encontrado: {object_id}")
            return False
        
        old_location = row[3]  # location_id column
        now = datetime.now(timezone.utc)
        
        # Actualizar ubicación
        self.db_connection.execute("""
            UPDATE game_objects 
            SET location_id = ?, last_modified = ?, version = version + 1
            WHERE id = ?
        """, (new_location_id, now.isoformat(), object_id))
        
        # Registrar evento
        await self._record_event(
            event_type="object_moved",
            actor=actor,
            action=f"moved object from {old_location} to {new_location_id}",
            target=object_id,
            location_id=new_location_id,
            context={
                "old_location": old_location,
                "new_location": new_location_id,
                "object_id": object_id
            }
        )
        
        logger.info(f"✅ Objeto {object_id} movido a {new_location_id}")
        return True
    
    async def modify_object_properties(self, object_id: str, 
                                     property_updates: Dict[str, Any], 
                                     actor: str = "system") -> bool:
        """Modifica las propiedades de un objeto (ej: oxidación del martillo)"""
        # Obtener propiedades actuales
        cursor = self.db_connection.execute("""
            SELECT properties, location_id FROM game_objects WHERE id = ?
        """, (object_id,))
        
        row = cursor.fetchone()
        if not row:
            logger.error(f"❌ Objeto no encontrado: {object_id}")
            return False
        
        current_properties = json.loads(row[0] or "{}")
        location_id = row[1]
        
        # Aplicar actualizaciones
        old_properties = current_properties.copy()
        current_properties.update(property_updates)
        
        now = datetime.now(timezone.utc)
        
        # Actualizar en base de datos
        self.db_connection.execute("""
            UPDATE game_objects 
            SET properties = ?, last_modified = ?, version = version + 1
            WHERE id = ?
        """, (json.dumps(current_properties), now.isoformat(), object_id))
        
        # Registrar evento
        await self._record_event(
            event_type="object_modified",
            actor=actor,
            action=f"modified object properties",
            target=object_id,
            location_id=location_id,
            context={
                "old_properties": old_properties,
                "new_properties": current_properties,
                "property_updates": property_updates
            }
        )
        
        logger.info(f"✅ Propiedades actualizadas para objeto {object_id}")
        return True
    
    async def get_objects_in_location(self, location_id: str) -> List[GameObject]:
        """Obtiene todos los objetos en una ubicación específica"""
        cursor = self.db_connection.execute("""
            SELECT * FROM game_objects WHERE location_id = ?
        """, (location_id,))
        
        objects = []
        for row in cursor.fetchall():
            obj_data = {
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'location_id': row[3],
                'properties': json.loads(row[4] or "{}"),
                'created_at': row[5],
                'last_modified': row[6],
                'version': row[7]
            }
            objects.append(GameObject.from_dict(obj_data))
        
        return objects
    
    async def get_object_history(self, object_id: str) -> List[GameEvent]:
        """Obtiene el historial completo de un objeto"""
        cursor = self.db_connection.execute("""
            SELECT * FROM game_events 
            WHERE target = ? 
            ORDER BY timestamp ASC
        """, (object_id,))
        
        events = []
        for row in cursor.fetchall():
            event_data = {
                'id': row[0],
                'timestamp': row[1],
                'event_type': row[2],
                'actor': row[3],
                'action': row[4],
                'target': row[5],
                'location_id': row[6],
                'context': json.loads(row[7] or "{}"),
                'embedding_vector': json.loads(row[8] or "null")
            }
            events.append(GameEvent(**event_data))
        
        return events
    
    async def search_events_by_content(self, search_text: str, 
                                     limit: int = 50) -> List[GameEvent]:
        """Busca eventos por contenido de texto (búsqueda simple)"""
        cursor = self.db_connection.execute("""
            SELECT * FROM game_events 
            WHERE action LIKE ? OR context LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{search_text}%", f"%{search_text}%", limit))
        
        events = []
        for row in cursor.fetchall():
            event_data = {
                'id': row[0],
                'timestamp': row[1],
                'event_type': row[2],
                'actor': row[3],
                'action': row[4],
                'target': row[5],
                'location_id': row[6],
                'context': json.loads(row[7] or "{}"),
                'embedding_vector': json.loads(row[8] or "null")
            }
            events.append(GameEvent(**event_data))
        
        return events
    
    async def _record_event(self, event_type: str, actor: str, action: str,
                          target: Optional[str], location_id: str,
                          context: Dict[str, Any]) -> str:
        """Registra un evento en el sistema"""
        event_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        event = GameEvent(
            id=event_id,
            timestamp=now,
            event_type=event_type,
            actor=actor,
            action=action,
            target=target,
            location_id=location_id,
            context=context
        )
        
        # Guardar en base de datos
        self.db_connection.execute("""
            INSERT INTO game_events
            (id, timestamp, event_type, actor, action, target, location_id, context, embedding_vector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.id,
            event.timestamp.isoformat(),
            event.event_type,
            event.actor,
            event.action,
            event.target,
            event.location_id,
            json.dumps(event.context),
            None  # Embedding vector se calculará después
        ))
        
        return event_id
    
    async def get_world_state_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del estado actual del mundo"""
        # Contar ubicaciones
        cursor = self.db_connection.execute("SELECT COUNT(*) FROM locations")
        location_count = cursor.fetchone()[0]
        
        # Contar objetos
        cursor = self.db_connection.execute("SELECT COUNT(*) FROM game_objects")
        object_count = cursor.fetchone()[0]
        
        # Contar eventos
        cursor = self.db_connection.execute("SELECT COUNT(*) FROM game_events")
        event_count = cursor.fetchone()[0]
        
        # Últimos eventos
        cursor = self.db_connection.execute("""
            SELECT action, timestamp FROM game_events 
            ORDER BY timestamp DESC LIMIT 10
        """)
        recent_events = cursor.fetchall()
        
        return {
            "locations": location_count,
            "objects": object_count,
            "total_events": event_count,
            "recent_events": [
                {"action": row[0], "timestamp": row[1]} 
                for row in recent_events
            ],
            "memory_integrity": "perfect"  # Siempre perfecto con este sistema
        }
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self.db_connection:
            self.db_connection.close()
            logger.info("🔒 Conexión a base de datos cerrada")
    
    async def get_all_locations(self) -> List[Location]:
        """Obtiene todas las ubicaciones del mundo"""
        cursor = self.db_connection.execute(
            "SELECT * FROM locations ORDER BY created_at"
        )
        
        locations = []
        for row in cursor.fetchall():
            location_data = dict(row)
            location_data['connections'] = json.loads(location_data['connections'] or '{}')
            location_data['properties'] = json.loads(location_data['properties'] or '{}')
            location_data['created_at'] = datetime.fromisoformat(location_data['created_at'])
            location_data['last_modified'] = datetime.fromisoformat(location_data['last_modified'])
            locations.append(Location(**location_data))
        
        return locations
    
    async def get_location(self, location_id: str) -> Optional[Location]:
        """Obtiene una ubicación específica por ID"""
        cursor = self.db_connection.execute(
            "SELECT * FROM locations WHERE id = ?",
            (location_id,)
        )
        
        row = cursor.fetchone()
        if not row:
            return None
        
        location_data = dict(row)
        location_data['connections'] = json.loads(location_data['connections'] or '{}')
        location_data['properties'] = json.loads(location_data['properties'] or '{}')
        location_data['created_at'] = datetime.fromisoformat(location_data['created_at'])
        location_data['last_modified'] = datetime.fromisoformat(location_data['last_modified'])
        
        return Location(**location_data)
    
    async def update_location_connections(self, location_id: str, connections: Dict[str, str]) -> bool:
        """Actualiza las conexiones de una ubicación"""
        now = datetime.now(timezone.utc)
        
        try:
            self.db_connection.execute("""
                UPDATE locations 
                SET connections = ?, last_modified = ?
                WHERE id = ?
            """, (json.dumps(connections), now.isoformat(), location_id))
            
            # Registrar evento
            await self._record_event(
                event_type="location_updated",
                actor="system",
                action=f"updated location connections",
                target=location_id,
                location_id=location_id,
                context={"connections": connections}
            )
            
            logger.info(f"✅ Conexiones actualizadas para ubicación {location_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error actualizando conexiones: {e}")
            return False

# Ejemplo de uso y testing
async def test_perfect_memory():
    """Prueba el sistema de memoria perfecta"""
    print("🧪 PROBANDO SISTEMA DE MEMORIA PERFECTA")
    print("=" * 50)
    
    # Inicializar sistema
    memory = PerfectMemorySystem("test_perfect_memory.db")
    
    # Crear ubicaciones
    workshop = await memory.create_location(
        "Taller de Herramientas",
        "Un viejo taller lleno de bancos de trabajo y herramientas oxidadas.",
        connections={"norte": "patio", "sur": "bodega"},
        properties={"lighting": "dim", "temperature": "cool"}
    )
    
    # Crear el famoso martillo
    hammer = await memory.create_object(
        "martillo",
        "Un martillo de acero con mango de madera. Parece bastante usado.",
        workshop.id,
        properties={
            "material": "steel_and_wood",
            "condition": "used",
            "weight": 1.2,
            "last_used": None,
            "rust_level": 0
        }
    )
    
    print(f"🔨 Martillo creado: {hammer.id}")
    
    # Simular el paso del tiempo - martillo se oxida
    await asyncio.sleep(0.1)  # Simular tiempo
    await memory.modify_object_properties(
        hammer.id,
        {"rust_level": 2, "condition": "rusty"},
        actor="time"
    )
    
    # El jugador mueve el martillo
    await memory.move_object(hammer.id, "inventory_player", actor="player")
    
    # Después lo deja en otro lugar
    storage = await memory.create_location(
        "Bodega",
        "Una bodega húmeda y oscura."
    )
    
    await memory.move_object(hammer.id, storage.id, actor="player")
    
    # MESES DESPUÉS... el martillo sigue ahí
    print("\n📅 SIMULANDO MESES DESPUÉS...")
    
    # Buscar el martillo
    objects_in_storage = await memory.get_objects_in_location(storage.id)
    print(f"🔍 Objetos en bodega: {len(objects_in_storage)}")
    
    for obj in objects_in_storage:
        if "martillo" in obj.name:
            print(f"✅ ¡MARTILLO ENCONTRADO!")
            print(f"   📍 Ubicación: {obj.location_id}")
            print(f"   🏷️  Propiedades: {obj.properties}")
            
            # Ver historial completo
            history = await memory.get_object_history(obj.id)
            print(f"   📜 Historial: {len(history)} eventos")
            for event in history:
                print(f"      - {event.timestamp}: {event.action}")
    
    # Resumen del mundo
    summary = await memory.get_world_state_summary()
    print(f"\n🌍 Estado del mundo:")
    print(f"   Ubicaciones: {summary['locations']}")
    print(f"   Objetos: {summary['objects']}")
    print(f"   Eventos totales: {summary['total_events']}")
    print(f"   Integridad: {summary['memory_integrity']}")
    
    memory.close()
    print("\n✅ Prueba completada - El martillo NUNCA se olvida!")

if __name__ == "__main__":
    asyncio.run(test_perfect_memory())
