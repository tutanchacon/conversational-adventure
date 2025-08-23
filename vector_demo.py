"""
Demo Interactivo - Adventure Game v1.1.0 con Búsqueda Vectorial
Demuestra las nuevas capacidades de búsqueda semántica y análisis de patrones
"""

import asyncio
import logging
from pathlib import Path
from adventure_game import IntelligentAdventureGame


class VectorSearchDemo:
    """Demo especializado para mostrar búsqueda vectorial"""
    
    def __init__(self):
        self.game = IntelligentAdventureGame(
            memory_db_path="vector_demo.db",
            model="llama3.2:3b"
        )
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    async def run_demo(self):
        """Ejecuta demo completo de búsqueda vectorial"""
        
        print("=" * 70)
        print("🔍 DEMO: ADVENTURE GAME v1.1.0 - BÚSQUEDA VECTORIAL")
        print("=" * 70)
        print()
        
        # Inicializar mundo
        await self.game.initialize_world()
        
        # Inicializar sistema vectorial
        print("🔄 Inicializando búsqueda vectorial...")
        await self.game.mcp.initialize_vector_search()
        
        if self.game.mcp.vector_initialized:
            print("✅ Búsqueda vectorial ACTIVA")
        else:
            print("❌ Error: Búsqueda vectorial no disponible")
            return
        
        print()
        
        # Poblar con más objetos para mejores demos
        await self._populate_demo_world()
        
        # Mostrar estadísticas
        stats = await self.game.get_world_stats()
        print(stats)
        print()
        
        # Demo 1: Búsqueda de objetos similares
        await self._demo_similar_objects()
        
        # Demo 2: Búsqueda por función/categoría
        await self._demo_functional_search()
        
        # Demo 3: Análisis de patrones
        await self._demo_pattern_analysis()
        
        # Demo 4: Recomendaciones inteligentes
        await self._demo_smart_recommendations()
        
        # Demo 5: Comparación con sistema anterior
        await self._demo_comparison()
        
        print("\n" + "=" * 70)
        print("🎉 DEMO COMPLETADO - ¡Explora las nuevas capacidades!")
        print("=" * 70)
        
        # Modo interactivo
        await self._interactive_mode()
    
    async def _populate_demo_world(self):
        """Puebla el mundo con objetos adicionales para mejores demos"""
        print("🏗️ Poblando mundo con objetos adicionales...")
        
        # Obtener ubicaciones existentes
        cursor = self.game.memory.db_connection.execute("SELECT id FROM locations")
        locations = [row[0] for row in cursor.fetchall()]
        
        if len(locations) < 3:
            print("⚠️ Necesitamos más ubicaciones, creando mundo base...")
            return
        
        # Objetos de carpintería y construcción
        carpentry_objects = [
            ("sierra de mano", "Una sierra dentada para cortar madera fina", 
             {"material": "steel_wood", "type": "cutting_tool", "condition": "sharp", "use": "carpentry"}),
            ("martillo de carpintero", "Martillo específico para trabajos de carpintería", 
             {"material": "steel_wood", "type": "hammer", "condition": "good", "use": "carpentry"}),
            ("cincel de madera", "Herramienta para tallar y dar forma a la madera", 
             {"material": "steel_wood", "type": "carving_tool", "condition": "sharp", "use": "woodworking"}),
            ("clavos de hierro", "Un puñado de clavos de hierro forjado", 
             {"material": "iron", "type": "fastener", "condition": "new", "use": "construction"}),
            ("banco de trabajo", "Mesa sólida de roble para trabajos de carpintería", 
             {"material": "oak", "type": "furniture", "condition": "worn", "use": "workspace"})
        ]
        
        # Objetos de cocina y utilitarios
        kitchen_objects = [
            ("cuchillo de cocina", "Cuchillo afilado para preparar alimentos", 
             {"material": "steel_wood", "type": "cutting_tool", "condition": "sharp", "use": "cooking"}),
            ("olla de hierro", "Gran olla de hierro fundido para cocinar", 
             {"material": "cast_iron", "type": "cookware", "condition": "seasoned", "use": "cooking"}),
            ("cucharón de madera", "Cucharón tallado en madera de haya", 
             {"material": "wood", "type": "utensil", "condition": "smooth", "use": "cooking"}),
            ("mortero de piedra", "Mortero de granito para moler especias", 
             {"material": "granite", "type": "grinding_tool", "condition": "polished", "use": "food_prep"})
        ]
        
        # Objetos mágicos y antiguos
        magical_objects = [
            ("varita de roble", "Varita mágica tallada en roble ancestral", 
             {"material": "enchanted_oak", "type": "magic_tool", "condition": "powerful", "use": "spellcasting"}),
            ("cristal de cuarzo", "Cristal transparente que brilla con luz interior", 
             {"material": "quartz", "type": "magic_focus", "condition": "pure", "use": "energy_channeling"}),
            ("pergamino antiguo", "Pergamino amarillento con runas desconocidas", 
             {"material": "parchment", "type": "knowledge", "condition": "fragile", "use": "spell_research"}),
            ("amuleto de protección", "Medallón de plata con símbolos protectores", 
             {"material": "silver", "type": "protection", "condition": "blessed", "use": "defense"})
        ]
        
        # Distribuir objetos en ubicaciones
        all_objects = carpentry_objects + kitchen_objects + magical_objects
        
        for i, (name, desc, props) in enumerate(all_objects):
            location = locations[i % len(locations)]
            try:
                await self.game.memory.create_object(name, desc, location, properties=props)
                print(f"  ✅ {name} creado en {location}")
            except Exception as e:
                print(f"  ⚠️ Error creando {name}: {e}")
        
        # Re-inicializar índice vectorial con nuevos objetos
        await self.game.mcp.vector_engine.initialize_from_existing_data()
        print("✅ Mundo poblado e índice vectorial actualizado")
    
    async def _demo_similar_objects(self):
        """Demo: Búsqueda de objetos similares"""
        print("\n" + "🔍 DEMO 1: BÚSQUEDA DE OBJETOS SIMILARES")
        print("-" * 50)
        
        test_queries = [
            "buscar objetos como martillo",
            "objetos parecidos a herramientas de metal",
            "buscar objetos como cuchillo"
        ]
        
        for query in test_queries:
            print(f"\n🎯 Consulta: '{query}'")
            print("-" * 30)
            
            response = await self.game.process_command_async(query)
            print(response)
            
            await asyncio.sleep(1)  # Pausa para mejor visualización
    
    async def _demo_functional_search(self):
        """Demo: Búsqueda por función/categoría"""
        print("\n" + "🛠️ DEMO 2: BÚSQUEDA POR FUNCIÓN/CATEGORÍA")
        print("-" * 50)
        
        test_queries = [
            "buscar herramientas de carpintería",
            "buscar herramientas para cocinar",
            "buscar objetos mágicos"
        ]
        
        for query in test_queries:
            print(f"\n🎯 Consulta: '{query}'")
            print("-" * 30)
            
            response = await self.game.process_command_async(query)
            print(response)
            
            await asyncio.sleep(1)
    
    async def _demo_pattern_analysis(self):
        """Demo: Análisis de patrones de ubicación"""
        print("\n" + "📊 DEMO 3: ANÁLISIS DE PATRONES")
        print("-" * 50)
        
        # Mover algunos objetos para crear patrones
        print("🔄 Preparando escenario de patrones...")
        
        # Simular que el jugador mueve objetos relacionados
        await self.game.process_command_async("tomar martillo")
        await self.game.process_command_async("ir norte")
        await self.game.process_command_async("dejar martillo")
        await self.game.process_command_async("tomar sierra")
        await self.game.process_command_async("dejar sierra")
        
        print("\n🎯 Analizando patrones en ubicación actual...")
        response = await self.game.process_command_async("analizar patrones aquí")
        print(response)
    
    async def _demo_smart_recommendations(self):
        """Demo: Recomendaciones inteligentes"""
        print("\n" + "💡 DEMO 4: RECOMENDACIONES INTELIGENTES")
        print("-" * 50)
        
        # Tomar algunos objetos para generar contexto
        await self.game.process_command_async("tomar martillo de carpintero")
        
        print("🎯 Solicitando recomendaciones basadas en inventario...")
        response = await self.game.process_command_async("recomendar objetos")
        print(response)
    
    async def _demo_comparison(self):
        """Demo: Comparación con sistema anterior"""
        print("\n" + "⚖️ DEMO 5: COMPARACIÓN ANTES vs DESPUÉS")
        print("-" * 50)
        
        print("🔍 ANTES (v1.0.0): Búsqueda básica por nombre exacto")
        print("   ❌ Solo encuentra objetos con nombres exactos")
        print("   ❌ No comprende sinónimos o similitudes")
        print("   ❌ No puede buscar por función o categoría")
        
        print("\n🔍 DESPUÉS (v1.1.0): Búsqueda semántica avanzada")
        print("   ✅ Comprende similitudes conceptuales")
        print("   ✅ Busca por función: 'herramientas de carpintería'")
        print("   ✅ Encuentra objetos relacionados automáticamente")
        print("   ✅ Analiza patrones de uso y ubicación")
        
        print("\n🎯 Ejemplo práctico:")
        print("   Búsqueda: 'herramientas para cortar'")
        
        response = await self.game.process_command_async("buscar herramientas para cortar")
        print("\n📊 Resultado con IA semántica:")
        print(response)
    
    async def _interactive_mode(self):
        """Modo interactivo para probar búsquedas"""
        print("\n" + "🎮 MODO INTERACTIVO - PRUEBA LAS NUEVAS CAPACIDADES")
        print("-" * 60)
        print("Comandos especiales disponibles:")
        print("  • 'buscar objetos como X' - Encuentra objetos similares")
        print("  • 'buscar herramientas de Y' - Busca por función")
        print("  • 'analizar patrones aquí' - Analiza ubicación actual")
        print("  • 'recomendar objetos' - Sugerencias inteligentes")
        print("  • 'stats' - Ver estadísticas del sistema")
        print("  • 'salir' - Terminar demo")
        print()
        
        while True:
            try:
                command = input("🎮 Comando: ").strip()
                
                if command.lower() in ['salir', 'exit', 'quit']:
                    break
                
                if command.lower() == 'stats':
                    stats = await self.game.get_world_stats()
                    print(stats)
                    continue
                
                if not command:
                    continue
                
                print("\n🤖 Procesando...")
                response = await self.game.process_command_async(command)
                print(f"\n📖 Respuesta:\n{response}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo terminado por el usuario")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                continue
    
    async def close(self):
        """Cierra el demo"""
        await self.game.close()


async def main():
    """Función principal del demo"""
    demo = VectorSearchDemo()
    
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrumpido")
    except Exception as e:
        print(f"\n❌ Error en demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await demo.close()


if __name__ == "__main__":
    print("🚀 Iniciando Demo de Búsqueda Vectorial...")
    
    # Verificar dependencias
    try:
        import chromadb
        import sentence_transformers
        print("✅ Dependencias vectoriales disponibles")
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("📦 Instala con: pip install chromadb sentence-transformers")
        exit(1)
    
    asyncio.run(main())
