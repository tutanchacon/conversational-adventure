#!/usr/bin/env python3
"""
Test ultra rápido - solo verificar que funciona básicamente
"""

import asyncio
from adventure_game import IntelligentAdventureGame

async def test_basico():
    print("🎮 TEST BÁSICO FASE 2")
    print("=" * 30)
    
    game = IntelligentAdventureGame()
    
    try:
        # Solo probar que responda a comandos básicos
        print("🗣️ Comando: 'mirar'")
        result = await game.process_command_async("mirar")
        print(f"   ✅ Respuesta: {result[:100]}...")
        
        print("\n🗣️ Comando: 'inventario'")
        result = await game.process_command_async("inventario")
        print(f"   ✅ Respuesta: {result[:100]}...")
        
        print("\n✅ ¡Sistema básico funcionando!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        await game.close()

if __name__ == "__main__":
    asyncio.run(test_basico())
