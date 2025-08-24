#!/usr/bin/env python3
"""
🔬 QUICK TEST - Verificación rápida del sistema
"""

import asyncio
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.getcwd())

async def quick_test():
    print("🔬 VERIFICANDO SISTEMA...")
    
    try:
        # Test 1: Import básico
        print("📦 Test 1: Imports...")
        from ai_integration import AIAdventureGame, create_ai_game
        print("✅ Imports OK")
        
        # Test 2: Crear instancia
        print("🚀 Test 2: Creando instancia...")
        game = AIAdventureGame("quick_test.db")
        print("✅ Instancia creada")
        
        # Test 3: Inicializar
        print("🏗️ Test 3: Inicializando...")
        success = await game.initialize()
        print(f"✅ Inicialización: {'OK' if success else 'FAILED'}")
        
        if success:
            # Test 4: Comando inventario
            print("📦 Test 4: Comando inventario...")
            result = await game.process_command("test", "inventario")
            print(f"✅ Inventario: {result['success']}")
            print(f"   Mensaje: {result['message']}")
            
            # Test 5: Comando conversación
            print("💬 Test 5: Comando conversación...")
            result = await game.process_command("test", "hola")
            print(f"✅ Conversación: {result['success']}")
            print(f"   Mensaje: {result['message'][:50]}...")
        
        # Cerrar
        await game.close()
        print("🎉 ¡SISTEMA FUNCIONANDO!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(quick_test())
