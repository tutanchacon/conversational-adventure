"""
🚀 CONFIGURACIÓN RÁPIDA DEL SISTEMA DE BACKUP
Script para configurar e inicializar el sistema de backup profesional
"""

import os
import sys
import asyncio
from pathlib import Path
from backup_system import BackupConfig, setup_backup_system, logger

def print_banner():
    """Muestra el banner del sistema"""
    print("""
🏢═══════════════════════════════════════════════════════════
   ADVENTURE GAME - BACKUP SYSTEM v1.0.0
   Sistema Profesional de Backup y Restauración
═══════════════════════════════════════════════════════════🏢
""")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    required_packages = ['schedule', 'cryptography']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Faltan dependencias: {', '.join(missing)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def create_backup_config():
    """Configura el sistema de backup interactivamente"""
    print("\n🔧 CONFIGURACIÓN DEL SISTEMA DE BACKUP")
    print("=" * 50)
    
    # Configuración básica
    backup_dir = input("📁 Directorio de backups [./backups]: ").strip() or "./backups"
    
    try:
        interval = int(input("⏰ Intervalo de backup automático en horas [6]: ").strip() or "6")
    except ValueError:
        interval = 6
    
    try:
        max_backups = int(input("📦 Máximo de backups a mantener [168]: ").strip() or "168")
    except ValueError:
        max_backups = 168
    
    compression = input("🗜️ ¿Habilitar compresión? [s/N]: ").strip().lower() in ['s', 'si', 'y', 'yes']
    encryption = input("🔐 ¿Habilitar encriptación? [s/N]: ").strip().lower() in ['s', 'si', 'y', 'yes']
    
    config = BackupConfig(
        backup_directory=backup_dir,
        auto_backup_interval_hours=interval,
        max_backups_to_keep=max_backups,
        enable_compression=compression,
        enable_encryption=encryption
    )
    
    print(f"\n✅ Configuración creada:")
    print(f"   📁 Directorio: {config.backup_directory}")
    print(f"   ⏰ Intervalo: {config.auto_backup_interval_hours}h")
    print(f"   📦 Máximo backups: {config.max_backups_to_keep}")
    print(f"   🗜️ Compresión: {'Sí' if config.enable_compression else 'No'}")
    print(f"   🔐 Encriptación: {'Sí' if config.enable_encryption else 'No'}")
    
    return config

def test_backup_system(backup_mgr, restore_mgr):
    """Prueba el sistema de backup"""
    print("\n🧪 PROBANDO SISTEMA DE BACKUP")
    print("=" * 40)
    
    # Crear backup de prueba
    print("1️⃣ Creando backup de prueba...")
    backup_id = backup_mgr.create_backup("test")
    
    if not backup_id:
        print("❌ Fallo creando backup de prueba")
        return False
    
    print(f"✅ Backup de prueba creado: {backup_id}")
    
    # Verificar backup
    print("2️⃣ Verificando backup...")
    backup_info = backup_mgr.get_backup_info(backup_id)
    if backup_info:
        print(f"   📄 Archivos: {backup_info.files_count}")
        print(f"   📦 Tamaño: {backup_info.size_bytes:,} bytes")
        print(f"   🕐 Fecha: {backup_info.timestamp}")
        print(f"   🔐 Hash: {backup_info.integrity_hash[:16]}...")
    
    # Probar restauración en directorio temporal
    print("3️⃣ Probando restauración...")
    test_restore_dir = "./test_restore"
    if restore_mgr.restore_backup(backup_id, test_restore_dir):
        print(f"✅ Restauración exitosa en {test_restore_dir}")
        
        # Limpiar directorio de prueba
        import shutil
        if os.path.exists(test_restore_dir):
            shutil.rmtree(test_restore_dir)
            print("🧹 Directorio de prueba limpiado")
    else:
        print("❌ Fallo en restauración de prueba")
        return False
    
    print("✅ Todas las pruebas pasaron exitosamente!")
    return True

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("""
📚 EJEMPLOS DE USO:

# Crear backup manual
backup_id = backup_mgr.create_backup("manual")

# Listar todos los backups
backups = backup_mgr.list_backups()
for backup in backups:
    print(f"{backup.backup_id} - {backup.timestamp}")

# Restaurar backup específico
restore_mgr.restore_backup("backup_20250823_140530", "./restored")

# Restaurar en ubicación actual (¡CUIDADO!)
restore_mgr.restore_to_current_location("backup_20250823_140530")

# Iniciar backups automáticos
scheduler.start()

# Detener backups automáticos
scheduler.stop()
""")

def main():
    """Función principal"""
    print_banner()
    
    # Verificar dependencias
    if not check_dependencies():
        return
    
    # Crear configuración
    config = create_backup_config()
    
    # Inicializar sistema
    print("\n🚀 INICIALIZANDO SISTEMA...")
    try:
        backup_mgr, restore_mgr, scheduler = setup_backup_system(config)
        print("✅ Sistema inicializado correctamente")
    except Exception as e:
        print(f"❌ Error inicializando sistema: {e}")
        return
    
    # Probar sistema
    if test_backup_system(backup_mgr, restore_mgr):
        print("\n🎉 SISTEMA DE BACKUP LISTO!")
        
        # Preguntar si iniciar scheduler automático
        start_auto = input("\n🤖 ¿Iniciar backups automáticos ahora? [S/n]: ").strip().lower()
        if start_auto not in ['n', 'no']:
            scheduler.start()
            print(f"✅ Backups automáticos iniciados (cada {config.auto_backup_interval_hours}h)")
        
        # Mostrar ejemplos
        show_examples = input("\n📚 ¿Mostrar ejemplos de uso? [S/n]: ").strip().lower()
        if show_examples not in ['n', 'no']:
            show_usage_examples()
        
        print("\n🏆 CONFIGURACIÓN COMPLETADA")
        print("   El sistema de backup está listo para usar.")
        print("   Consulta la documentación en RUTA_PROFESIONAL_PLAN.md")
        
        # Retornar objetos para uso inmediato
        return backup_mgr, restore_mgr, scheduler
    
    else:
        print("\n❌ Falló la configuración del sistema")
        return None

if __name__ == "__main__":
    result = main()
    
    if result:
        backup_mgr, restore_mgr, scheduler = result
        print(f"\n💡 Los objetos están disponibles:")
        print(f"   - backup_mgr: {type(backup_mgr).__name__}")
        print(f"   - restore_mgr: {type(restore_mgr).__name__}")
        print(f"   - scheduler: {type(scheduler).__name__}")
        
        # Mantener el programa corriendo si hay scheduler activo
        if hasattr(scheduler, 'is_running') and scheduler.is_running:
            print(f"\n🔄 Manteniendo programa activo para backups automáticos...")
            print(f"   Presiona Ctrl+C para detener")
            try:
                while True:
                    import time
                    time.sleep(60)
            except KeyboardInterrupt:
                print(f"\n🛑 Deteniendo sistema...")
                scheduler.stop()
                print(f"✅ Sistema detenido correctamente")
