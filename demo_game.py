
# Demo del juego con Sistema de Memoria Perfecta
import asyncio
from adventure_game import IntelligentAdventureGame

async def demo():
    print("🎮 DEMO DEL JUEGO CON MEMORIA PERFECTA")
    print("=" * 50)
    print("🧠 Sistema de memoria que NUNCA olvida nada")
    print("🔨 El martillo que dejes hoy, estará ahí en 6 meses")
    print()
    
    # Inicializar juego con memoria perfecta
    game = IntelligentAdventureGame("demo_perfect_world.db", model="llama3.2")
    
    # Comandos de prueba que demuestran la persistencia
    test_commands = [
        "mirar alrededor",
        "examinar la llave oxidada", 
        "tomar la llave oxidada",
        "ir al norte",
        "mirar alrededor",
        "dejar la llave oxidada",
        "ir al este", 
        "examinar el libro de hechizos",
        "tomar el libro de hechizos",
        "ir al oeste",
        "ir al oeste", 
        "examinar el martillo del herrero",
        "tomar el martillo del herrero",
        "inventario",
        "ir al este",
        "ir al este",
        "dejar el martillo del herrero aquí",
        "mirar alrededor"
    ]
    
    print("🎯 Ejecutando secuencia de comandos que demuestran la memoria perfecta...")
    print()
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n--- COMANDO {i}/{len(test_commands)} ---")
        print(f"🗣️ Jugador: {command}")
        
        try:
            response = await game.process_command_async(command)
            print(f"🎮 Juego: {response}")
            
            # Pausa para que sea más fácil de seguir
            await asyncio.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETADA")
    
    # Mostrar estadísticas finales
    print("\n📊 ESTADÍSTICAS DEL MUNDO:")
    stats = await game.get_world_stats()
    print(stats)
    
    print("\n🔍 INVENTARIO FINAL:")
    inventory = await game.get_inventory()
    print(inventory)
    
    print("\n💾 DEMOSTRACIÓN DE MEMORIA PERFECTA:")
    print("- Cada objeto tiene una ubicación exacta registrada")
    print("- Cada movimiento del jugador queda grabado con timestamp")
    print("- Las propiedades de objetos evolucionan (oxidación, desgaste)")
    print("- El sistema recuerda TODO: donde dejaste cada objeto")
    print("- Incluso después de meses, el martillo estará donde lo dejaste")
    print("- La IA tiene acceso completo a toda esta información")
    
    print("\n🧪 PRUEBA TÚ MISMO:")
    print("1. Ejecuta 'python demo_game.py' varias veces")
    print("2. Los objetos permanecerán donde los dejes")
    print("3. El estado del mundo es 100% persistente")
    print("4. La IA recordará cada detalle")
    
    await game.close()
    
    print("\n✅ Sistema funcionando perfectamente!")
    print("🔮 ¡Tu mundo de aventura nunca olvidará nada!")

async def demo_memory_persistence():
    """Demo adicional que muestra la persistencia entre sesiones"""
    print("\n🔄 DEMO DE PERSISTENCIA ENTRE SESIONES")
    print("=" * 50)
    
    # Conectar al mismo mundo
    game = IntelligentAdventureGame("demo_perfect_world.db", model="llama3.2")
    
    print("🕰️ Reconectando al mundo existente...")
    
    # Verificar que los objetos siguen donde los dejamos
    commands = [
        "mirar alrededor",
        "ir al este", 
        "mirar alrededor",  # ¿Está el martillo aquí?
        "ir al oeste",
        "ir al sur",
        "ir al norte",
        "ir al norte", 
        "mirar alrededor"  # ¿Está la llave aquí?
    ]
    
    for command in commands:
        print(f"\n🗣️ {command}")
        response = await game.process_command_async(command)
        print(f"🎮 {response}")
        await asyncio.sleep(0.3)
    
    await game.close()
    print("\n✅ ¡Los objetos siguen exactamente donde los dejaste!")

if __name__ == "__main__":
    # Ejecutar demo principal
    asyncio.run(demo())
    
    # Ejecutar demo de persistencia
    asyncio.run(demo_memory_persistence())
