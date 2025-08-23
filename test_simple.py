#!/usr/bin/env python3
"""
Test rápido y simplificado para diagnosticar problemas del sistema vectorial
"""

import sys
import asyncio
from memory_system import PerfectMemorySystem
from enhanced_mcp import EnhancedMCPProvider

async def test_simple():
    print("🔍 TEST SIMPLIFICADO v1.1.0")
    print("=" * 40)
    
    # Test 1: Memory System
    print("📦 Test 1: Memory System...")
    try:
        memory = PerfectMemorySystem("test_simple.db")
        print("  ✅ PerfectMemorySystem OK")
    except Exception as e:
        print(f"  ❌ Error en PerfectMemorySystem: {e}")
        return False
    
    # Test 2: Enhanced MCP
    print("🔧 Test 2: Enhanced MCP...")
    try:
        enhanced_mcp = EnhancedMCPProvider(memory, "test_simple.db")
        print("  ✅ EnhancedMCPProvider OK")
    except Exception as e:
        print(f"  ❌ Error en EnhancedMCPProvider: {e}")
        return False
    
    # Test 3: Crear datos de prueba
    print("🌍 Test 3: Crear datos...")
    try:
        # Crear ubicación
        location = await memory.create_location(
            "Taller Simple", 
            "Un taller básico para pruebas"
        )
        location_id = location.id
        print(f"  ✅ Ubicación creada: {location_id}")
        
        # Crear objeto
        obj = await memory.create_object(
            "martillo simple",
            "Un martillo básico de prueba",
            location_id,
            {"tipo": "herramienta", "material": "acero"}
        )
        print(f"  ✅ Objeto creado: {obj.id}")
        
    except Exception as e:
        print(f"  ❌ Error creando datos: {e}")
        return False
    
    # Test 4: Inicializar vector search (sin ChromaDB por ahora)
    print("🔍 Test 4: Vector Search...")
    try:
        # Intentar inicializar vector search
        await enhanced_mcp.initialize_vector_search()
        print("  ✅ Vector Search inicializado")
        
    except Exception as e:
        print(f"  ❌ Error en Vector Search: {e}")
        print(f"  ℹ️  Error detallado: {type(e).__name__}: {str(e)}")
        return False
    
    print("\n🎉 ¡Todos los tests pasaron!")
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_simple())
        if result:
            print("\n✅ Sistema funcionando correctamente")
            sys.exit(0)
        else:
            print("\n❌ Sistema requiere revisión")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error crítico: {e}")
        sys.exit(1)
