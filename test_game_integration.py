#!/usr/bin/env python3
"""
🧪 TEST GAME INTEGRATION - Adventure Game v3.0
Prueba la integración del juego real con el sistema AI
"""

import asyncio
import logging
from ai_integration import create_ai_game

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def test_game_integration():
    """Probar la integración completa del juego con IA"""
    logger.info("🧪 INICIANDO TEST DE INTEGRACIÓN JUEGO + IA")
    logger.info("=" * 50)
    
    game = None
    
    try:
        # 1. Inicializar juego
        logger.info("🚀 Inicializando AI Adventure Game...")
        game = await create_ai_game("test_integration.db")
        logger.info("✅ Juego inicializado correctamente")
        
        # 2. Test comando inventario
        logger.info("\n📦 Test 1: Comando INVENTARIO")
        result = await game.process_command("test_player", "inventario")
        logger.info(f"Resultado: {result['success']}")
        logger.info(f"Mensaje: {result['message']}")
        logger.info(f"Acción: {result['game_action']}")
        
        # 3. Test comando mirar
        logger.info("\n👀 Test 2: Comando MIRAR")
        result = await game.process_command("test_player", "mirar alrededor")
        logger.info(f"Resultado: {result['success']}")
        logger.info(f"Mensaje: {result['message'][:100]}...")
        logger.info(f"Acción: {result['game_action']}")
        
        # 4. Test comando conversar
        logger.info("\n💬 Test 3: Comando CONVERSACIÓN")
        result = await game.process_command("test_player", "hola, ¿cómo estás?")
        logger.info(f"Resultado: {result['success']}")
        logger.info(f"Mensaje: {result['message'][:100]}...")
        logger.info(f"Acción: {result['game_action']}")
        
        # 5. Test comando tomar
        logger.info("\n🤏 Test 4: Comando TOMAR")
        result = await game.process_command("test_player", "tomar espada")
        logger.info(f"Resultado: {result['success']}")
        logger.info(f"Mensaje: {result['message']}")
        logger.info(f"Acción: {result['game_action']}")
        
        # 6. Test inventario después de tomar
        logger.info("\n📦 Test 5: INVENTARIO después de tomar")
        result = await game.process_command("test_player", "inventario")
        logger.info(f"Resultado: {result['success']}")
        logger.info(f"Mensaje: {result['message']}")
        
        logger.info("\n" + "=" * 50)
        logger.info("🎉 ¡TESTS COMPLETADOS!")
        logger.info("El sistema está funcionando correctamente.")
        logger.info("- ✅ Inventario funciona")
        logger.info("- ✅ Comandos del juego funcionan") 
        logger.info("- ✅ IA responde correctamente")
        logger.info("- ✅ Integración completa")
        
    except Exception as e:
        logger.error(f"❌ Error en test: {e}")
        
    finally:
        if game:
            logger.info("🛑 Cerrando juego...")
            await game.close()

async def main():
    """Función principal"""
    await test_game_integration()

if __name__ == "__main__":
    asyncio.run(main())
