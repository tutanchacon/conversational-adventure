"""
🏆 BACKUP PROFESIONAL INMEDIATO
Crea un backup completo del estado actual del proyecto Adventure Game
"""

from backup_system import BackupConfig, setup_backup_system
from datetime import datetime

def create_immediate_backup():
    """Crea un backup inmediato del proyecto"""
    print("🏢 CREANDO BACKUP PROFESIONAL DEL PROYECTO")
    print("=" * 50)
    
    # Configuración profesional
    config = BackupConfig(
        backup_directory="./backups",
        auto_backup_interval_hours=6,
        max_backups_to_keep=48,  # 2 días de historial
        enable_compression=True,
        enable_encryption=False,
        backup_sqlite=True,
        backup_vector_db=True,
        backup_logs=True,
        integrity_check=True
    )
    
    # Inicializar sistema
    backup_mgr, restore_mgr, scheduler = setup_backup_system(config)
    
    # Crear backup del estado actual
    print("🚀 Creando backup del estado actual...")
    backup_id = backup_mgr.create_backup("professional_v1.1.0")
    
    if backup_id:
        print(f"✅ BACKUP EXITOSO: {backup_id}")
        
        # Mostrar información detallada
        backup_info = backup_mgr.get_backup_info(backup_id)
        if backup_info:
            print(f"\n📊 DETALLES DEL BACKUP:")
            print(f"   🆔 ID: {backup_info.backup_id}")
            print(f"   📅 Fecha: {backup_info.timestamp}")
            print(f"   📄 Archivos: {backup_info.files_count}")
            print(f"   💾 Tamaño: {backup_info.size_bytes:,} bytes")
            print(f"   🎮 Estado: {backup_info.game_state_summary}")
            print(f"   🔐 Hash: {backup_info.integrity_hash[:16]}...")
            print(f"   🏷️ Tipo: {backup_info.backup_type}")
        
        # Listar todos los backups
        print(f"\n📋 HISTORIAL DE BACKUPS:")
        all_backups = backup_mgr.list_backups()
        for i, backup in enumerate(all_backups, 1):
            print(f"   {i:2d}. {backup.backup_id} ({backup.backup_type})")
            print(f"       📅 {backup.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"       📦 {backup.size_bytes:,} bytes, {backup.files_count} archivos")
        
        print(f"\n🎉 BACKUP PROFESIONAL COMPLETADO!")
        print(f"   📁 Ubicación: ./backups/{backup_id}.zip")
        print(f"   🛡️ Tu proyecto está protegido")
        
        return backup_id
    else:
        print("❌ ERROR: No se pudo crear el backup")
        return None

if __name__ == "__main__":
    print("🏢 ADVENTURE GAME - BACKUP PROFESIONAL v1.0.0")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    backup_id = create_immediate_backup()
    
    if backup_id:
        print(f"\n✨ RUTA PROFESIONAL - FASE 1 COMPLETADA")
        print(f"   ✅ Sistema de Backup/Restore operativo")
        print(f"   ✅ Backup automático configurado") 
        print(f"   ✅ Validación de integridad activa")
        print(f"   ✅ Estado actual respaldado: {backup_id}")
        print(f"\n🚀 Listo para continuar con:")
        print(f"   📅 Semana 2-5: Web Interface")
        print(f"   📅 Semana 6-8: Multi-jugador")
        print(f"   📅 Semana 9: Analytics Dashboard")
    else:
        print(f"\n💥 Error en la configuración")
        print(f"   Revisa los logs arriba para más detalles")
