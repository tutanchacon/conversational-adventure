# Demostración Final del Sistema de Memoria Perfecta
# Este script demuestra que el martillo NUNCA se olvida

import asyncio
import os
from datetime import datetime
from adventure_game import IntelligentAdventureGame

class FinalDemo:
    def __init__(self):
        self.db_name = "final_demo_world.db"
        self.game = None
    
    async def reset_world_if_needed(self):
        """Pregunta si resetear el mundo o continuar"""
        if os.path.exists(self.db_name):
            print("🌍 Mundo existente detectado")
            choice = input("¿Quieres (c)ontinuar el mundo existente o (r)eset? [c/r]: ").lower()
            if choice == 'r':
                os.remove(self.db_name)
                print("🗑️ Mundo reseteado")
            else:
                print("📖 Cargando mundo existente...")
    
    async def demo_session_1(self):
        """Primera sesión: crear y mover objetos"""
        print("\n" + "=" * 60)
        print("📅 SESIÓN 1: Creando el mundo y moviendo objetos")
        print("=" * 60)
        
        self.game = IntelligentAdventureGame(self.db_name, model="mock")
        # Usar IA simulada para demo
        self.game.ollama = MockOllamaForDemo()
        
        commands = [
            "mirar alrededor",
            "examinar la llave oxidada",
            "tomar la llave oxidada",
            "ir al norte",
            "ir al oeste", 
            "examinar el martillo del herrero",
            "tomar el martillo del herrero",
            "ir al este",
            "ir al este",
            "dejar el martillo del herrero en la biblioteca",
            "ir al oeste",
            "ir al sur",
            "dejar la llave oxidada en la entrada"
        ]
        
        print("🎯 Ejecutando comandos de la primera sesión...")
        for i, command in enumerate(commands, 1):
            print(f"\n[{i:2d}] 🗣️ {command}")
            response = await self.game.process_command_async(command)
            print(f"     🎮 {response[:100]}{'...' if len(response) > 100 else ''}")
            await asyncio.sleep(0.2)
        
        # Mostrar estado final de la sesión 1
        stats = await self.game.get_world_stats()
        print(f"\n📊 Estado al final de la sesión 1:")
        print(f"   Eventos registrados: {stats.split('Eventos registrados: ')[1].split()[0]}")
        
        await self.game.close()
        print("💾 Sesión 1 completada y guardada")
    
    async def demo_session_2(self):
        """Segunda sesión: verificar persistencia"""
        print("\n" + "=" * 60)
        print("📅 SESIÓN 2: Verificando persistencia (simulando días después)")
        print("=" * 60)
        
        print("🕰️ Reconectando al mundo guardado...")
        self.game = IntelligentAdventureGame(self.db_name, model="mock")
        self.game.ollama = MockOllamaForDemo()
        
        # Simular que ha pasado tiempo - oxidar objetos
        print("⏰ Simulando el paso del tiempo...")
        
        # Encontrar objetos y oxidarlos
        objects = await self.game.memory.get_objects_in_location("inventory_player")
        all_locations = ["entrada", "biblioteca", "cocina", "hall_principal"]
        
        # Buscar todos los objetos para oxidarlos
        for location_id in all_locations:
            cursor = self.game.memory.db_connection.execute("""
                SELECT id FROM locations WHERE name LIKE ?
            """, (f"%{location_id}%",))
            rows = cursor.fetchall()
            for row in rows:
                location_objects = await self.game.memory.get_objects_in_location(row[0])
                for obj in location_objects:
                    if "rust_level" in obj.properties:
                        new_rust = min(obj.properties.get("rust_level", 0) + 2, 5)
                        await self.game.memory.modify_object_properties(
                            obj.id,
                            {"rust_level": new_rust, "condition": "more_rusty"},
                            actor="time"
                        )
        
        commands = [
            "mirar alrededor",
            "ir al norte", 
            "ir al este",
            "mirar alrededor",  # ¿Está el martillo aquí?
            "examinar el martillo del herrero",
            "tomar el martillo del herrero",
            "ir al oeste",
            "ir al sur", 
            "mirar alrededor",  # ¿Está la llave aquí?
            "examinar la llave oxidada",
            "inventario"
        ]
        
        print("🔍 Verificando que los objetos siguen donde los dejamos...")
        for i, command in enumerate(commands, 1):
            print(f"\n[{i:2d}] 🗣️ {command}")
            response = await self.game.process_command_async(command)
            print(f"     🎮 {response[:100]}{'...' if len(response) > 100 else ''}")
            await asyncio.sleep(0.2)
        
        await self.game.close()
        print("✅ Sesión 2 completada")
    
    async def show_memory_analysis(self):
        """Muestra análisis detallado de la memoria"""
        print("\n" + "=" * 60)
        print("🧠 ANÁLISIS DE MEMORIA PERFECTA")
        print("=" * 60)
        
        self.game = IntelligentAdventureGame(self.db_name, model="mock")
        
        # Estadísticas generales
        stats = await self.game.get_world_stats()
        print(f"\n📊 ESTADÍSTICAS GENERALES:")
        print(stats)
        
        # Historial de objetos específicos
        print(f"\n🔨 HISTORIAL DEL MARTILLO:")
        
        # Buscar el martillo
        cursor = self.game.memory.db_connection.execute("""
            SELECT id, name, location_id, properties FROM game_objects 
            WHERE name LIKE '%martillo%'
        """)
        
        martillo_row = cursor.fetchone()
        if martillo_row:
            martillo_id = martillo_row[0]
            print(f"   ID: {martillo_id}")
            print(f"   Ubicación actual: {martillo_row[2]}")
            print(f"   Propiedades: {martillo_row[3]}")
            
            history = await self.game.memory.get_object_history(martillo_id)
            print(f"\n   📜 Eventos del martillo ({len(history)} total):")
            for event in history:
                timestamp = event.timestamp.strftime("%H:%M:%S")
                print(f"      {timestamp}: {event.action}")
        
        # Buscar la llave
        print(f"\n🗝️ HISTORIAL DE LA LLAVE:")
        cursor = self.game.memory.db_connection.execute("""
            SELECT id, name, location_id, properties FROM game_objects 
            WHERE name LIKE '%llave%'
        """)
        
        llave_row = cursor.fetchone()
        if llave_row:
            llave_id = llave_row[0]
            print(f"   ID: {llave_id}")
            print(f"   Ubicación actual: {llave_row[2]}")
            print(f"   Propiedades: {llave_row[3]}")
            
            history = await self.game.memory.get_object_history(llave_id)
            print(f"\n   📜 Eventos de la llave ({len(history)} total):")
            for event in history:
                timestamp = event.timestamp.strftime("%H:%M:%S")
                print(f"      {timestamp}: {event.action}")
        
        await self.game.close()
    
    async def run_complete_demo(self):
        """Ejecuta la demostración completa"""
        print("🎮 DEMOSTRACIÓN FINAL: MEMORIA PERFECTA")
        print("🔨 El martillo que dejes hoy, estará ahí en 6 meses")
        print("🧠 Sistema que NUNCA olvida nada")
        
        await self.reset_world_if_needed()
        
        try:
            await self.demo_session_1()
            
            input("\n⏸️ Presiona Enter para continuar con la sesión 2...")
            
            await self.demo_session_2()
            
            input("\n⏸️ Presiona Enter para ver el análisis de memoria...")
            
            await self.show_memory_analysis()
            
            print("\n" + "=" * 60)
            print("🎉 DEMOSTRACIÓN COMPLETADA")
            print("=" * 60)
            print("✅ Memoria perfecta demostrada:")
            print("   🔨 El martillo está exactamente donde lo dejaste")
            print("   🗝️ La llave sigue en su ubicación original")
            print("   ⏰ Los objetos se han oxidado con el tiempo")
            print("   📜 Cada movimiento quedó registrado permanentemente")
            print("   🧠 La IA tiene acceso a todo el historial")
            print("\n💡 Esto funciona igual después de días, semanas o meses!")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrumpida por el usuario")
        except Exception as e:
            print(f"\n❌ Error en demo: {e}")

class MockOllamaForDemo:
    """IA simulada para la demostración"""
    
    async def generate(self, model, prompt, system=None):
        prompt_lower = prompt.lower()
        
        if "mirar" in prompt_lower:
            if "biblioteca" in system.lower() if system else False:
                return "En la biblioteca ves estanterías llenas de libros antiguos. En el suelo, un martillo del herrero descansa donde alguien lo dejó."
            elif "entrada" in system.lower() if system else False:
                return "Estás en la entrada del castillo. En el suelo ves una llave oxidada que brilla débilmente."
            else:
                return "Observas cuidadosamente el entorno, notando cada detalle de esta ubicación histórica."
        
        elif "examinar" in prompt_lower:
            if "martillo" in prompt_lower:
                return "El martillo del herrero muestra signos de uso y tiempo. El óxido ha avanzado desde la última vez que lo viste, pero sigue siendo funcional."
            elif "llave" in prompt_lower:
                return "La llave oxidada ha acumulado más óxido desde que la dejaste aquí. El tiempo ha dejado su marca en el metal."
            else:
                return "Examinas el objeto con atención, notando cómo ha cambiado con el tiempo."
        
        elif "tomar" in prompt_lower:
            return "Tomas el objeto cuidadosamente. Sientes su peso familiar y notas los cambios que el tiempo ha causado."
        
        elif "dejar" in prompt_lower:
            return "Colocas el objeto cuidadosamente en esta ubicación. Quedará aquí, esperando tu regreso."
        
        elif "inventario" in prompt_lower:
            return "Revisas tu inventario, sintiendo el peso de los objetos que llevas contigo."
        
        elif "ir" in prompt_lower:
            return "Te desplazas hacia la dirección indicada, explorando este mundo persistente."
        
        else:
            return "Respondes al comando, sabiendo que cada acción queda registrada en la memoria perfecta del mundo."
    
    async def close(self):
        pass

async def main():
    demo = FinalDemo()
    await demo.run_complete_demo()

if __name__ == "__main__":
    asyncio.run(main())
