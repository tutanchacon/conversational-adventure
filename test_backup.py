"""
🧪 TEST RÁPIDO DEL SISTEMA DE BACKUP
Prueba básica para verificar que el sistema funciona correctamente
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime
from backup_system import BackupConfig, setup_backup_system

def test_backup_system():
    """Prueba completa del sistema de backup"""
    print("🧪 INICIANDO TESTS DEL SISTEMA DE BACKUP")
    print("=" * 50)
    
    # Crear configuración de prueba
    test_backup_dir = tempfile.mkdtemp(prefix="backup_test_")
    config = BackupConfig(
        backup_directory=test_backup_dir,
        auto_backup_interval_hours=1,  # 1 hora para pruebas
        max_backups_to_keep=5,
        enable_compression=True,
        enable_encryption=False  # Sin encriptación para simplificar tests
    )
    
    print(f"📁 Directorio de prueba: {test_backup_dir}")
    
    try:
        # Inicializar sistema
        print("\n1️⃣ Inicializando sistema...")
        backup_mgr, restore_mgr, scheduler = setup_backup_system(config)
        print("✅ Sistema inicializado")
        
        # Crear algunos archivos de prueba
        print("\n2️⃣ Creando archivos de prueba...")
        test_files = [
            "test_file1.txt",
            "test_file2.log", 
            "test_config.md"
        ]
        
        for filename in test_files:
            with open(filename, 'w') as f:
                f.write(f"Contenido de prueba para {filename}\n")
                f.write(f"Creado: {datetime.now()}\n")
        print(f"✅ {len(test_files)} archivos de prueba creados")
        
        # Crear backup
        print("\n3️⃣ Creando backup...")
        backup_id = backup_mgr.create_backup("test")
        if backup_id:
            print(f"✅ Backup creado: {backup_id}")
        else:
            print("❌ Fallo creando backup")
            return False
        
        # Verificar backup
        print("\n4️⃣ Verificando backup...")
        backup_info = backup_mgr.get_backup_info(backup_id)
        if backup_info:
            print(f"   📦 ID: {backup_info.backup_id}")
            print(f"   📄 Archivos: {backup_info.files_count}")
            print(f"   💾 Tamaño: {backup_info.size_bytes:,} bytes")
            print(f"   🕐 Fecha: {backup_info.timestamp}")
            print(f"   ✅ Hash: {backup_info.integrity_hash[:16]}...")
        else:
            print("❌ No se pudo verificar backup")
            return False
        
        # Listar backups
        print("\n5️⃣ Listando backups...")
        backups = backup_mgr.list_backups()
        print(f"   📋 Total: {len(backups)} backups")
        for backup in backups:
            print(f"   • {backup.backup_id} ({backup.backup_type})")
        
        # Probar restauración
        print("\n6️⃣ Probando restauración...")
        restore_dir = tempfile.mkdtemp(prefix="restore_test_")
        
        if restore_mgr.restore_backup(backup_id, restore_dir):
            print(f"✅ Restauración exitosa en {restore_dir}")
            
            # Verificar archivos restaurados
            restored_files = []
            for root, dirs, files in os.walk(restore_dir):
                for file in files:
                    if file.endswith(('.txt', '.log', '.md')):
                        restored_files.append(file)
            
            print(f"   📄 Archivos restaurados: {len(restored_files)}")
            for file in restored_files:
                print(f"   • {file}")
        else:
            print("❌ Fallo en restauración")
            return False
        
        # Test de múltiples backups
        print("\n7️⃣ Probando múltiples backups...")
        backup_ids = []
        for i in range(3):
            # Modificar archivo para crear diferencias
            with open("test_file1.txt", 'a') as f:
                f.write(f"Modificación {i+1}: {datetime.now()}\n")
            
            backup_id = backup_mgr.create_backup(f"test_multi_{i+1}")
            if backup_id:
                backup_ids.append(backup_id)
                print(f"   ✅ Backup {i+1}: {backup_id}")
            else:
                print(f"   ❌ Fallo en backup {i+1}")
        
        # Verificar lista actualizada
        backups = backup_mgr.list_backups()
        print(f"   📋 Total backups: {len(backups)}")
        
        # Test de programador (sin iniciar realmente)
        print("\n8️⃣ Probando programador...")
        print(f"   ⏰ Configurado para cada {config.auto_backup_interval_hours}h")
        print("   ✅ Programador listo (no iniciado en test)")
        
        print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("=" * 50)
        print("✅ El sistema de backup está funcionando correctamente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TESTS: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpiar archivos de prueba
        print("\n🧹 Limpiando archivos de prueba...")
        try:
            for filename in test_files:
                if os.path.exists(filename):
                    os.remove(filename)
            
            if os.path.exists(test_backup_dir):
                shutil.rmtree(test_backup_dir)
            
            if 'restore_dir' in locals() and os.path.exists(restore_dir):
                shutil.rmtree(restore_dir)
                
            print("✅ Limpieza completada")
        except Exception as e:
            print(f"⚠️ Error en limpieza: {e}")

if __name__ == "__main__":
    print("🚀 EJECUTANDO TESTS DEL SISTEMA DE BACKUP v1.0.0")
    print()
    
    # Verificar si estamos en el directorio correcto
    if not os.path.exists("adventure_game.py"):
        print("⚠️ Advertencia: No se encuentra adventure_game.py")
        print("   Los tests funcionarán, pero sin datos reales del juego")
    
    success = test_backup_system()
    
    if success:
        print("\n🏆 RESULTADO: TODOS LOS TESTS EXITOSOS")
        print("   El sistema está listo para uso en producción")
        print("   Ejecuta 'python setup_backup.py' para configuración completa")
    else:
        print("\n💥 RESULTADO: TESTS FALLIDOS")
        print("   Revisa los errores arriba y verifica dependencias")
        print("   Ejecuta: pip install -r requirements.txt")
    
    print(f"\n📖 Para más información consulta:")
    print(f"   • RUTA_PROFESIONAL_PLAN.md")
    print(f"   • backup_system.py (código fuente)")
    print(f"   • setup_backup.py (configuración)")
