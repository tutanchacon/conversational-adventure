#!/usr/bin/env python3
"""
Test rápido de las nuevas capacidades vectoriales
"""

import asyncio
from adventure_game import IntelligentAdventureGame

async def test_fase2():
    print("🎮 PROBANDO FASE 2 - BÚSQUEDAS INTELIGENTES")
    print("=" * 50)
    
    game = IntelligentAdventureGame()
    
    try:
        # Inicializar juego
        print("📦 Iniciando juego...")
        await game.initialize_world()
        
        # Crear algunos objetos de prueba
        print("🏗️ Creando mundo de prueba...")
        
        # Crear ubicación
        await game.process_command_async("crear ubicación taller 'Un taller de carpintería'")
        await game.process_command_async("ir taller")
        
        # Crear objetos con propiedades
        await game.process_command_async("crear martillo 'Un martillo de carpintero robusto' material:acero tipo:herramienta uso:carpinteria")
        await game.process_command_async("crear sierra 'Una sierra de mano afilada' material:acero tipo:herramienta uso:cortar")
        await game.process_command_async("crear clavos 'Clavos de acero para construcción' material:acero tipo:suministro uso:construccion")
        
        print("\n🔍 PROBANDO BÚSQUEDAS INTELIGENTES:")
        print("-" * 40)
        
        # Test 1: Búsqueda por concepto
        print("\n1️⃣ Buscar 'herramientas de carpintería':")
        result = await game.process_command_async("buscar herramientas de carpintería")
        print(f"   Resultado: {result}")
        
        # Test 2: Búsqueda por material
        print("\n2️⃣ Buscar 'objetos de acero':")
        result = await game.process_command_async("buscar objetos de acero")
        print(f"   Resultado: {result}")
        
        # Test 3: Búsqueda por función
        print("\n3️⃣ Buscar 'cosas para construir':")
        result = await game.process_command_async("buscar cosas para construir")
        print(f"   Resultado: {result}")
        
        print("\n✅ ¡Fase 2 funcionando correctamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await game.close()

if __name__ == "__main__":
    asyncio.run(test_fase2())
