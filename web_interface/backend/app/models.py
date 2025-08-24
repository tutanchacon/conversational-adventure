"""
📊 MODELOS DE DATOS - Adventure Game Web Interface
Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

# ============================================================================
# ENUMS
# ============================================================================

class SystemStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"
    STARTING = "starting"
    STOPPING = "stopping"

class BackupType(str, Enum):
    MANUAL = "manual"
    AUTO = "auto" 
    SCHEDULED = "scheduled"
    EMERGENCY = "emergency"

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

# ============================================================================
# MODELOS BASE
# ============================================================================

class BaseResponse(BaseModel):
    """Respuesta base para todas las APIs"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None

class ErrorResponse(BaseResponse):
    """Respuesta de error"""
    success: bool = False
    error_code: str
    error_detail: str

# ============================================================================
# MODELOS DE SISTEMA
# ============================================================================

class SystemMetrics(BaseModel):
    """Métricas del sistema en tiempo real"""
    uptime_seconds: int
    uptime_formatted: str
    requests_count: int
    active_websockets: int
    system_health: str
    timestamp: datetime
    events_count: Optional[int] = None
    total_backups: Optional[int] = None
    last_backup: Optional[datetime] = None

class SystemStatusDetail(BaseModel):
    """Estado detallado del sistema"""
    adventure_game: Dict[str, Any]
    backup_system: Dict[str, Any]
    websockets: Dict[str, Any]

class ComponentStatus(BaseModel):
    """Estado de un componente del sistema"""
    name: str
    status: SystemStatus
    uptime: Optional[str] = None
    last_error: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

# ============================================================================
# MODELOS DE BACKUP
# ============================================================================

class BackupInfo(BaseModel):
    """Información de un backup"""
    backup_id: str
    timestamp: datetime
    size_bytes: int
    files_count: int
    backup_type: BackupType
    integrity_hash: str
    game_state_summary: str
    is_encrypted: bool = False

class BackupListResponse(BaseResponse):
    """Lista de backups"""
    backups: List[BackupInfo]
    total_count: int

class CreateBackupRequest(BaseModel):
    """Request para crear backup"""
    backup_type: BackupType = BackupType.MANUAL
    description: Optional[str] = None

class CreateBackupResponse(BaseResponse):
    """Respuesta de creación de backup"""
    backup_id: str
    started_at: datetime

class RestoreBackupRequest(BaseModel):
    """Request para restaurar backup"""
    backup_id: str
    target_directory: Optional[str] = None
    create_safety_backup: bool = True

class RestoreBackupResponse(BaseResponse):
    """Respuesta de restauración"""
    backup_id: str
    restored_files: int
    safety_backup_id: Optional[str] = None

# ============================================================================
# MODELOS DE EVENTOS
# ============================================================================

class GameEvent(BaseModel):
    """Evento del juego"""
    event_id: str
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class EventsListResponse(BaseResponse):
    """Lista de eventos"""
    events: List[GameEvent]
    total_count: int
    limit: int
    offset: int

class CreateEventRequest(BaseModel):
    """Request para crear evento"""
    event_type: str
    data: Dict[str, Any]
    user_id: Optional[str] = None

# ============================================================================
# MODELOS DE LOGS
# ============================================================================

class LogEntry(BaseModel):
    """Entrada de log"""
    timestamp: datetime
    level: LogLevel
    logger: str
    message: str
    module: Optional[str] = None
    function: Optional[str] = None
    line_number: Optional[int] = None

class LogsResponse(BaseResponse):
    """Respuesta de logs"""
    logs: List[LogEntry]
    total_count: int
    filters: Dict[str, Any]

class LogsFilter(BaseModel):
    """Filtros para logs"""
    level: Optional[LogLevel] = None
    logger: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    search_text: Optional[str] = None
    limit: int = 100
    offset: int = 0

# ============================================================================
# MODELOS DE CONFIGURACIÓN
# ============================================================================

class BackupConfig(BaseModel):
    """Configuración de backup"""
    backup_directory: str = "./backups"
    auto_backup_interval_hours: int = 6
    max_backups_to_keep: int = 48
    enable_compression: bool = True
    enable_encryption: bool = False
    backup_sqlite: bool = True
    backup_vector_db: bool = True
    backup_logs: bool = True
    integrity_check: bool = True

class GameConfig(BaseModel):
    """Configuración del juego"""
    max_events_in_memory: int = 10000
    enable_vector_search: bool = True
    vector_search_similarity_threshold: float = 0.7
    auto_save_interval_minutes: int = 5
    debug_mode: bool = False

class WebInterfaceConfig(BaseModel):
    """Configuración de la interfaz web"""
    refresh_interval_seconds: int = 5
    max_websocket_connections: int = 100
    enable_real_time_logs: bool = True
    logs_buffer_size: int = 1000
    theme: str = "dark"

class SystemConfig(BaseModel):
    """Configuración completa del sistema"""
    backup: BackupConfig
    game: GameConfig
    web_interface: WebInterfaceConfig

# ============================================================================
# MODELOS DE WEBSOCKET
# ============================================================================

class WebSocketMessage(BaseModel):
    """Mensaje de WebSocket"""
    type: str
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Optional[Dict[str, Any]] = None

class MetricsUpdateMessage(WebSocketMessage):
    """Actualización de métricas por WebSocket"""
    type: str = "metrics_update"
    data: SystemMetrics

class BackupCreatedMessage(WebSocketMessage):
    """Notificación de backup creado"""
    type: str = "backup_created"
    backup_id: str

class SystemStatusMessage(WebSocketMessage):
    """Estado del sistema por WebSocket"""
    type: str = "system_status"
    status: SystemStatus
    message: str

class LogMessage(WebSocketMessage):
    """Mensaje de log en tiempo real"""
    type: str = "log_message"
    log_entry: LogEntry

# ============================================================================
# MODELOS DE AUTENTICACIÓN
# ============================================================================

class LoginRequest(BaseModel):
    """Request de login"""
    username: str
    password: str

class LoginResponse(BaseResponse):
    """Respuesta de login"""
    token: str
    user_info: Dict[str, Any]
    expires_at: datetime

class UserInfo(BaseModel):
    """Información de usuario"""
    username: str
    role: str
    permissions: List[str]
    last_login: Optional[datetime] = None

# ============================================================================
# MODELOS DE ESTADÍSTICAS
# ============================================================================

class StatisticsRequest(BaseModel):
    """Request para estadísticas"""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    granularity: str = "hour"  # minute, hour, day, week, month

class StatisticsResponse(BaseResponse):
    """Respuesta de estadísticas"""
    data_points: List[Dict[str, Any]]
    summary: Dict[str, Any]
    period: Dict[str, Any]

class GameStatistics(BaseModel):
    """Estadísticas del juego"""
    total_events: int
    events_by_type: Dict[str, int]
    active_sessions: int
    total_sessions_today: int
    average_session_duration: float
    most_active_hours: List[int]

# ============================================================================
# MODELOS DE BÚSQUEDA
# ============================================================================

class SearchRequest(BaseModel):
    """Request de búsqueda"""
    query: str
    search_type: str = "semantic"  # semantic, text, sql
    limit: int = 50
    filters: Optional[Dict[str, Any]] = None

class SearchResult(BaseModel):
    """Resultado de búsqueda"""
    item_id: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any]
    timestamp: datetime

class SearchResponse(BaseResponse):
    """Respuesta de búsqueda"""
    results: List[SearchResult]
    total_found: int
    query_time_ms: float
    search_type: str

# ============================================================================
# MODELOS DE CONTROL DE JUEGO
# ============================================================================

class GameControlRequest(BaseModel):
    """Request de control del juego"""
    action: str  # start, stop, restart, pause, resume
    parameters: Optional[Dict[str, Any]] = None

class GameControlResponse(BaseResponse):
    """Respuesta de control del juego"""
    action: str
    previous_status: SystemStatus
    new_status: SystemStatus
    details: Optional[str] = None

# ============================================================================
# MODELOS DE MONITOREO
# ============================================================================

class HealthCheck(BaseModel):
    """Health check del sistema"""
    status: str
    timestamp: datetime
    uptime: str
    components: List[ComponentStatus]
    version: str = "2.0.0"

class AlertRule(BaseModel):
    """Regla de alerta"""
    name: str
    condition: str
    threshold: float
    enabled: bool = True
    notification_channels: List[str] = []

class Alert(BaseModel):
    """Alerta del sistema"""
    alert_id: str
    rule_name: str
    severity: str  # low, medium, high, critical
    message: str
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None

# ============================================================================
# VALIDACIONES Y UTILIDADES
# ============================================================================

class ValidationError(BaseModel):
    """Error de validación"""
    field: str
    message: str
    invalid_value: Any

class BulkOperationResponse(BaseResponse):
    """Respuesta de operación en lote"""
    processed_count: int
    success_count: int
    error_count: int
    errors: List[ValidationError] = []
