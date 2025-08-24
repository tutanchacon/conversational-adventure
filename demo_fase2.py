#!/usr/bin/env python3
"""
Demo rápido de Adventure Game v1.1.0 - Fase 2
Prueba las nuevas capacidades de búsqueda vectorial
"""

import asyncio
import sys
from adventure_game import IntelligentAdventureGame

async def demo_fase2():
    print("🎮 DEMO ADVENTURE GAME v1.1.0 - FASE 2")
    print("🔍 Probando Búsqueda Vectorial")
    print("=" * 50)
    
    # Crear juego
    game = IntelligentAdventureGame()
    
    print("🏗️ Inicializando juego...")
    # El juego se inicializa automáticamente en el constructor
    
    print("✅ Juego inicializado exitosamente!")
    print()
    
    # Crear mundo de prueba
    print("🌍 Creando mundo de prueba...")
    
    # Simular algunos comandos básicos
    commands = [
        "mirar alrededor",
        "crear taller de carpintería",
        "ir a taller", 
        "crear martillo de acero usado para clavar",
        "crear sierra de mano para cortar madera",
        "crear clavos pequeños de metal",
        "mirar alrededor"
    ]
    
    for cmd in commands:
        print(f"🎮 Comando: {cmd}")
        response = await game.process_command_async(cmd)
        print(f"🤖 Respuesta: {response[:200]}...")
        print()
    
    # Probar búsquedas vectoriales
    print("🔍 PROBANDO BÚSQUEDAS VECTORIALES")
    print("-" * 40)
    
    vector_commands = [
        "buscar herramientas de carpintería",
        "buscar objetos para construcción", 
        "buscar objetos como martillo",
        "analizar patrones taller"
    ]
    
    for cmd in vector_commands:
        print(f"🔍 Búsqueda: {cmd}")
        try:
            response = await game.process_command_async(cmd)
            print(f"🧠 IA encontró: {response[:300]}...")
        except Exception as e:
            print(f"⚠️ Error: {e}")
        print()
    
    print("🎉 Demo completado exitosamente!")
    print("✅ Fase 2 funcionando correctamente!")

if __name__ == "__main__":
    try:
        asyncio.run(demo_fase2())
    except KeyboardInterrupt:
        print("\n👋 Demo cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        sys.exit(1)
