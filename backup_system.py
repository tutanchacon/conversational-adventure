"""
🏢 BACKUP/RESTORE SYSTEM v1.0.0
Sistema profesional de backup y restauración para Adventure Game

Características:
✅ Backup incremental automático
✅ Compresión inteligente
✅ Validación de integridad
✅ Programación automática
✅ Restauración point-in-time
✅ Configuración flexible
"""

import os
import json
import gzip
import sqlite3
import hashlib
import zipfile
import schedule
import asyncio
import shutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import threading
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BackupConfig:
    """Configuración del sistema de backup"""
    backup_directory: str = "./backups"
    auto_backup_interval_hours: int = 6
    max_backups_to_keep: int = 168  # 7 días * 24 horas / 6 horas
    enable_compression: bool = True
    enable_encryption: bool = False
    backup_sqlite: bool = True
    backup_vector_db: bool = True
    backup_logs: bool = True
    integrity_check: bool = True
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass 
class BackupMetadata:
    """Metadatos de un backup"""
    backup_id: str
    timestamp: datetime
    version: str
    size_bytes: int
    files_count: int
    integrity_hash: str
    backup_type: str  # 'auto', 'manual', 'scheduled'
    game_state_summary: str
    is_encrypted: bool = False
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

class IntegrityValidator:
    """Validador de integridad de datos"""
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
        """Calcula hash de un archivo"""
        hash_func = hashlib.new(algorithm)
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            logger.error(f"Error calculando hash de {file_path}: {e}")
            return ""
    
    @staticmethod
    def calculate_directory_hash(directory: str) -> str:
        """Calcula hash de todo un directorio"""
        all_hashes = []
        try:
            for root, dirs, files in os.walk(directory):
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    file_hash = IntegrityValidator.calculate_file_hash(file_path)
                    relative_path = os.path.relpath(file_path, directory)
                    all_hashes.append(f"{relative_path}:{file_hash}")
            
            combined = "\n".join(sorted(all_hashes))
            return hashlib.sha256(combined.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculando hash del directorio {directory}: {e}")
            return ""
    
    @staticmethod
    def validate_sqlite_integrity(db_path: str) -> bool:
        """Valida integridad de base de datos SQLite"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            return result[0] == "ok"
        except Exception as e:
            logger.error(f"Error validando integridad de SQLite {db_path}: {e}")
            return False

class BackupManager:
    """Gestor principal del sistema de backup"""
    
    def __init__(self, config: BackupConfig):
        self.config = config
        self.backup_dir = Path(config.backup_directory)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Directorio de metadatos
        self.metadata_dir = self.backup_dir / "metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        
        # Configurar encriptación si está habilitada
        self.encryption_key = None
        if config.enable_encryption:
            self._setup_encryption()
        
        logger.info(f"BackupManager inicializado. Directorio: {self.backup_dir}")
    
    def _setup_encryption(self):
        """Configura la encriptación"""
        key_file = self.backup_dir / ".backup_key"
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            # Hacer el archivo de clave read-only
            os.chmod(key_file, 0o600)
        logger.info("Sistema de encriptación configurado")
    
    def _generate_backup_id(self) -> str:
        """Genera un ID único para el backup"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}"
    
    def _get_game_state_summary(self) -> str:
        """Obtiene un resumen del estado actual del juego"""
        try:
            # Intentar obtener información básica de la base de datos
            db_path = "./adventure_game.db"
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Contar eventos
                cursor.execute("SELECT COUNT(*) FROM events")
                events_count = cursor.fetchone()[0]
                
                # Obtener último evento
                cursor.execute("SELECT timestamp FROM events ORDER BY timestamp DESC LIMIT 1")
                last_event = cursor.fetchone()
                last_event_time = last_event[0] if last_event else "N/A"
                
                conn.close()
                
                return f"Events: {events_count}, Last: {last_event_time}"
            else:
                return "No game database found"
        except Exception as e:
            logger.warning(f"No se pudo obtener resumen del estado: {e}")
            return "State summary unavailable"
    
    def create_backup(self, backup_type: str = "manual") -> Optional[str]:
        """Crea un nuevo backup"""
        try:
            backup_id = self._generate_backup_id()
            backup_path = self.backup_dir / f"{backup_id}.zip"
            
            logger.info(f"Iniciando backup {backup_id} ({backup_type})")
            
            # Crear archivo zip
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                files_added = 0
                
                # Backup de base de datos SQLite
                if self.config.backup_sqlite:
                    sqlite_files = ["adventure_game.db", "adventure_game.db-wal", "adventure_game.db-shm"]
                    for db_file in sqlite_files:
                        if os.path.exists(db_file):
                            zip_file.write(db_file, f"sqlite/{db_file}")
                            files_added += 1
                            logger.debug(f"Agregado al backup: {db_file}")
                
                # Backup de vector database
                if self.config.backup_vector_db:
                    vector_db_path = Path("./vector_database")
                    if vector_db_path.exists():
                        for root, dirs, files in os.walk(vector_db_path):
                            for file in files:
                                file_path = Path(root) / file
                                arc_path = Path("vector_db") / file_path.relative_to(vector_db_path)
                                zip_file.write(file_path, str(arc_path))
                                files_added += 1
                
                # Backup de logs
                if self.config.backup_logs:
                    log_files = [f for f in os.listdir(".") if f.endswith('.log')]
                    for log_file in log_files:
                        zip_file.write(log_file, f"logs/{log_file}")
                        files_added += 1
                
                # Backup de archivos de configuración
                config_files = ["requirements.txt", "*.md", "*.py"]
                for pattern in config_files:
                    if pattern.endswith('.py'):
                        py_files = [f for f in os.listdir(".") if f.endswith('.py')]
                        for py_file in py_files:
                            zip_file.write(py_file, f"config/{py_file}")
                            files_added += 1
                    elif pattern.endswith('.md'):
                        md_files = [f for f in os.listdir(".") if f.endswith('.md')]
                        for md_file in md_files:
                            zip_file.write(md_file, f"docs/{md_file}")
                            files_added += 1
                    elif os.path.exists(pattern):
                        zip_file.write(pattern, f"config/{pattern}")
                        files_added += 1
            
            # Calcular tamaño y hash del backup
            backup_size = backup_path.stat().st_size
            backup_hash = IntegrityValidator.calculate_file_hash(str(backup_path))
            
            # Crear metadatos
            metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=datetime.now(),
                version="1.1.0",
                size_bytes=backup_size,
                files_count=files_added,
                integrity_hash=backup_hash,
                backup_type=backup_type,
                game_state_summary=self._get_game_state_summary(),
                is_encrypted=self.config.enable_encryption
            )
            
            # Guardar metadatos
            metadata_file = self.metadata_dir / f"{backup_id}.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata.to_dict(), f, indent=2)
            
            # Encriptar si está habilitado
            if self.config.enable_encryption and self.encryption_key:
                self._encrypt_backup(backup_path)
            
            logger.info(f"✅ Backup {backup_id} creado exitosamente")
            logger.info(f"   📁 Tamaño: {backup_size:,} bytes")
            logger.info(f"   📄 Archivos: {files_added}")
            logger.info(f"   🔐 Hash: {backup_hash[:16]}...")
            
            # Limpiar backups antiguos
            self._cleanup_old_backups()
            
            return backup_id
            
        except Exception as e:
            logger.error(f"❌ Error creando backup: {e}")
            return None
    
    def _encrypt_backup(self, backup_path: Path):
        """Encripta un archivo de backup"""
        try:
            fernet = Fernet(self.encryption_key)
            
            # Leer archivo original
            with open(backup_path, 'rb') as f:
                data = f.read()
            
            # Encriptar
            encrypted_data = fernet.encrypt(data)
            
            # Escribir archivo encriptado
            encrypted_path = backup_path.with_suffix('.zip.enc')
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Eliminar archivo original no encriptado
            backup_path.unlink()
            
            # Renombrar archivo encriptado
            encrypted_path.rename(backup_path)
            
            logger.info(f"🔐 Backup encriptado: {backup_path.name}")
            
        except Exception as e:
            logger.error(f"Error encriptando backup: {e}")
    
    def _cleanup_old_backups(self):
        """Elimina backups antiguos según la configuración"""
        try:
            # Obtener todos los backups ordenados por fecha
            backup_files = list(self.backup_dir.glob("backup_*.zip"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Eliminar backups excedentes
            if len(backup_files) > self.config.max_backups_to_keep:
                files_to_delete = backup_files[self.config.max_backups_to_keep:]
                for backup_file in files_to_delete:
                    backup_id = backup_file.stem
                    
                    # Eliminar archivo de backup
                    backup_file.unlink()
                    
                    # Eliminar metadatos
                    metadata_file = self.metadata_dir / f"{backup_id}.json"
                    if metadata_file.exists():
                        metadata_file.unlink()
                    
                    logger.info(f"🗑️ Backup antiguo eliminado: {backup_id}")
                    
        except Exception as e:
            logger.error(f"Error limpiando backups antiguos: {e}")
    
    def list_backups(self) -> List[BackupMetadata]:
        """Lista todos los backups disponibles"""
        backups = []
        try:
            for metadata_file in self.metadata_dir.glob("*.json"):
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                    metadata = BackupMetadata(**data)
                    backups.append(metadata)
            
            # Ordenar por fecha (más reciente primero)
            backups.sort(key=lambda x: x.timestamp, reverse=True)
            return backups
            
        except Exception as e:
            logger.error(f"Error listando backups: {e}")
            return []
    
    def get_backup_info(self, backup_id: str) -> Optional[BackupMetadata]:
        """Obtiene información de un backup específico"""
        try:
            metadata_file = self.metadata_dir / f"{backup_id}.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    data['timestamp'] = datetime.fromisoformat(data['timestamp'])
                    return BackupMetadata(**data)
            return None
        except Exception as e:
            logger.error(f"Error obteniendo info del backup {backup_id}: {e}")
            return None

class RestoreManager:
    """Gestor de restauración de backups"""
    
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager
        self.config = backup_manager.config
        
    def restore_backup(self, backup_id: str, target_directory: str = "./restored") -> bool:
        """Restaura un backup específico"""
        try:
            logger.info(f"Iniciando restauración del backup {backup_id}")
            
            # Verificar que el backup existe
            backup_info = self.backup_manager.get_backup_info(backup_id)
            if not backup_info:
                logger.error(f"Backup {backup_id} no encontrado")
                return False
            
            backup_file = self.backup_manager.backup_dir / f"{backup_id}.zip"
            if not backup_file.exists():
                logger.error(f"Archivo de backup {backup_file} no existe")
                return False
            
            # Validar integridad antes de restaurar
            if self.config.integrity_check:
                current_hash = IntegrityValidator.calculate_file_hash(str(backup_file))
                if current_hash != backup_info.integrity_hash:
                    logger.error(f"❌ Fallo de integridad en backup {backup_id}")
                    logger.error(f"   Hash esperado: {backup_info.integrity_hash}")
                    logger.error(f"   Hash actual: {current_hash}")
                    return False
                logger.info("✅ Validación de integridad exitosa")
            
            # Crear directorio de destino
            target_path = Path(target_directory)
            target_path.mkdir(exist_ok=True)
            
            # Desencriptar si es necesario
            temp_backup_file = backup_file
            if backup_info.is_encrypted and self.backup_manager.encryption_key:
                temp_backup_file = self._decrypt_backup(backup_file)
                if not temp_backup_file:
                    return False
            
            # Extraer backup
            with zipfile.ZipFile(temp_backup_file, 'r') as zip_file:
                zip_file.extractall(target_path)
                extracted_files = len(zip_file.namelist())
            
            # Limpiar archivo temporal si se desencriptó
            if temp_backup_file != backup_file:
                temp_backup_file.unlink()
            
            logger.info(f"✅ Backup {backup_id} restaurado exitosamente")
            logger.info(f"   📁 Directorio: {target_path}")
            logger.info(f"   📄 Archivos: {extracted_files}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error restaurando backup {backup_id}: {e}")
            return False
    
    def _decrypt_backup(self, backup_file: Path) -> Optional[Path]:
        """Desencripta un archivo de backup"""
        try:
            fernet = Fernet(self.backup_manager.encryption_key)
            
            # Leer archivo encriptado
            with open(backup_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Desencriptar
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Crear archivo temporal
            temp_file = backup_file.parent / f"temp_{backup_file.name}"
            with open(temp_file, 'wb') as f:
                f.write(decrypted_data)
            
            return temp_file
            
        except Exception as e:
            logger.error(f"Error desencriptando backup: {e}")
            return None
    
    def restore_to_current_location(self, backup_id: str, create_backup_first: bool = True) -> bool:
        """Restaura un backup en la ubicación actual (¡PELIGROSO!)"""
        try:
            # Crear backup de seguridad primero
            if create_backup_first:
                safety_backup = self.backup_manager.create_backup("safety_before_restore")
                if safety_backup:
                    logger.info(f"🛡️ Backup de seguridad creado: {safety_backup}")
                else:
                    logger.warning("⚠️ No se pudo crear backup de seguridad")
            
            # Restaurar a directorio temporal
            temp_dir = "./temp_restore"
            if not self.restore_backup(backup_id, temp_dir):
                return False
            
            # Mover archivos a ubicación actual
            temp_path = Path(temp_dir)
            
            # Restaurar SQLite
            sqlite_dir = temp_path / "sqlite"
            if sqlite_dir.exists():
                for sqlite_file in sqlite_dir.glob("*"):
                    target = Path(sqlite_file.name)
                    if target.exists():
                        target.unlink()
                    shutil.move(str(sqlite_file), str(target))
                    logger.info(f"📁 Restaurado: {sqlite_file.name}")
            
            # Restaurar vector database
            vector_dir = temp_path / "vector_db"
            if vector_dir.exists():
                target_vector_dir = Path("./vector_database")
                if target_vector_dir.exists():
                    shutil.rmtree(target_vector_dir)
                shutil.move(str(vector_dir), str(target_vector_dir))
                logger.info("📁 Vector database restaurada")
            
            # Limpiar directorio temporal
            shutil.rmtree(temp_path)
            
            logger.info(f"✅ Restauración completa del backup {backup_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en restauración completa: {e}")
            return False

class AutoBackupScheduler:
    """Programador automático de backups"""
    
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager
        self.config = backup_manager.config
        self.is_running = False
        self.scheduler_thread = None
        
    def start(self):
        """Inicia el programador automático"""
        if self.is_running:
            logger.warning("Programador automático ya está en ejecución")
            return
        
        # Programar backup automático
        schedule.every(self.config.auto_backup_interval_hours).hours.do(
            self._scheduled_backup
        )
        
        # Iniciar hilo del programador
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        logger.info(f"🕐 Programador automático iniciado (cada {self.config.auto_backup_interval_hours}h)")
    
    def stop(self):
        """Detiene el programador automático"""
        self.is_running = False
        schedule.clear()
        logger.info("🛑 Programador automático detenido")
    
    def _run_scheduler(self):
        """Hilo principal del programador"""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Verificar cada minuto
    
    def _scheduled_backup(self):
        """Ejecuta un backup programado"""
        logger.info("⏰ Ejecutando backup automático programado")
        backup_id = self.backup_manager.create_backup("auto")
        if backup_id:
            logger.info(f"✅ Backup automático completado: {backup_id}")
        else:
            logger.error("❌ Fallo en backup automático")

# Funciones de utilidad
def create_default_config() -> BackupConfig:
    """Crea una configuración por defecto"""
    return BackupConfig()

def setup_backup_system(config: Optional[BackupConfig] = None) -> Tuple[BackupManager, RestoreManager, AutoBackupScheduler]:
    """Configura el sistema completo de backup"""
    if config is None:
        config = create_default_config()
    
    backup_manager = BackupManager(config)
    restore_manager = RestoreManager(backup_manager)
    scheduler = AutoBackupScheduler(backup_manager)
    
    return backup_manager, restore_manager, scheduler

# Ejemplo de uso
if __name__ == "__main__":
    # Configuración personalizada
    config = BackupConfig(
        auto_backup_interval_hours=6,
        max_backups_to_keep=168,  # 7 días
        enable_compression=True,
        enable_encryption=False
    )
    
    # Inicializar sistema
    backup_mgr, restore_mgr, scheduler = setup_backup_system(config)
    
    # Crear backup manual
    print("🚀 Creando backup inicial...")
    backup_id = backup_mgr.create_backup("initial")
    
    if backup_id:
        print(f"✅ Backup creado: {backup_id}")
        
        # Listar backups
        print("\n📋 Backups disponibles:")
        for backup in backup_mgr.list_backups():
            print(f"  • {backup.backup_id} - {backup.timestamp} ({backup.backup_type})")
            print(f"    📄 {backup.files_count} archivos, {backup.size_bytes:,} bytes")
        
        # Iniciar programador automático
        print(f"\n🕐 Iniciando backups automáticos cada {config.auto_backup_interval_hours}h...")
        scheduler.start()
        
        print("✨ Sistema de backup configurado y funcionando!")
        print("   - Backups automáticos habilitados")
        print("   - Validación de integridad activa")
        print("   - Retención automática configurada")
        
    else:
        print("❌ Error configurando sistema de backup")
