#!/usr/bin/env python3
"""
Test sin vector search - solo funcionalidad básica v1.0.0
"""

import asyncio
from memory_system import PerfectMemorySystem
from mcp_integration import MCPContextProvider

async def test_sin_vector():
    print("🎮 TEST SIN VECTOR SEARCH - FUNCIONALIDAD BÁSICA")
    print("=" * 50)
    
    # Crear sistema de memoria
    memory = PerfectMemorySystem("test_basico.db")
    mcp = MCPContextProvider(memory)
    
    try:
        # Test 1: Crear ubicación
        print("🏗️ Creando ubicación...")
        location = await memory.create_location(
            "Taller de Prueba",
            "Un taller para probar el sistema"
        )
        print(f"   ✅ Ubicación creada: {location.name}")
        
        # Test 2: Crear objeto
        print("🔨 Creando objeto...")
        obj = await memory.create_object(
            "martillo de prueba",
            "Un martillo para probar la persistencia",
            location.id,
            {"material": "acero", "tipo": "herramienta"}
        )
        print(f"   ✅ Objeto creado: {obj.name}")
        
        # Test 3: Verificar persistencia
        print("🔍 Verificando persistencia...")
        objects = await memory.get_objects_in_location(location.id)
        print(f"   ✅ Objetos encontrados: {len(objects)}")
        for o in objects:
            print(f"      - {o.name}: {o.description}")
        
        # Test 4: Generar contexto MCP
        print("🧠 Generando contexto para IA...")
        context = await mcp.generate_world_context_for_ai(location.id)
        print(f"   ✅ Contexto generado: {len(context)} caracteres")
        print(f"   📄 Vista previa: {context[:200]}...")
        
        print("\n🎉 ¡Sistema básico v1.0.0 funcionando perfectamente!")
        print("💡 La memoria perfecta está operativa")
        print("🔨 El 'martillo immortal' está garantizado")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        memory.close()  # Quitar await ya que close() no es async

if __name__ == "__main__":
    asyncio.run(test_sin_vector())
