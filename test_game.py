# Test rápido del juego sin Ollama (modo simulado)
import asyncio
from adventure_game import IntelligentAdventureGame

class MockOllamaClient:
    """Cliente simulado para pruebas sin Ollama"""
    
    async def generate(self, model, prompt, system=None):
        # Respuestas predefinidas basadas en palabras clave
        prompt_lower = prompt.lower()
        
        if "mirar" in prompt_lower or "examinar" in prompt_lower:
            return "Observas cuidadosamente tu entorno. Puedes ver los objetos claramente descritos en el contexto actual."
        elif "tomar" in prompt_lower or "coger" in prompt_lower:
            return "Extiendes tu mano y tomas el objeto. Sientes su peso y textura. Ahora forma parte de tu inventario."
        elif "ir" in prompt_lower or "mover" in prompt_lower:
            return "Te mueves hacia la dirección indicada. El entorno cambia a tu alrededor mientras exploras."
        elif "dejar" in prompt_lower or "soltar" in prompt_lower:
            return "Colocas cuidadosamente el objeto en el suelo. Queda perfectamente posicionado en esta ubicación."
        elif "inventario" in prompt_lower:
            return "Revisas tu inventario cuidadosamente, examinando cada objeto que llevas contigo."
        else:
            return "Comprendes el comando y respondes de acuerdo al contexto actual del mundo."
    
    async def close(self):
        print("🔒 Cliente simulado cerrado")

async def test_game_without_ollama():
    """Prueba el juego sin requerir Ollama"""
    print("🎮 PRUEBA DEL JUEGO (MODO SIMULADO)")
    print("=" * 50)
    print("⚠️ Usando IA simulada - instalar Ollama para experiencia completa")
    print()
    
    # Crear juego
    game = IntelligentAdventureGame("test_game_world.db", model="mock")
    
    # Reemplazar cliente real con simulado
    game.ollama = MockOllamaClient()
    
    # Comandos de prueba
    commands = [
        "mirar alrededor",
        "examinar la llave oxidada",
        "tomar la llave oxidada", 
        "ir al norte",
        "mirar alrededor",
        "inventario"
    ]
    
    for i, command in enumerate(commands, 1):
        print(f"\n--- COMANDO {i}/{len(commands)} ---")
        print(f"🗣️ Jugador: {command}")
        
        try:
            response = await game.process_command_async(command)
            print(f"🎮 IA: {response}")
            
            # Mostrar algunos detalles del estado
            if "inventario" in command.lower():
                inventory = await game.get_inventory()
                print(f"📦 {inventory}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        await asyncio.sleep(0.3)
    
    # Estadísticas finales
    print(f"\n📊 ESTADÍSTICAS DEL MUNDO:")
    stats = await game.get_world_stats()
    print(stats)
    
    await game.close()
    print("\n✅ Prueba completada exitosamente!")
    print("💡 Para experiencia completa: instalar y ejecutar Ollama")

if __name__ == "__main__":
    asyncio.run(test_game_without_ollama())
