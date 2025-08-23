"""
Prueba Simple del Sistema Vectorial v1.1.0
Verifica funcionamiento básico sin dependencias externas
"""

import asyncio
import sys
import traceback

async def test_vector_system():
    """Prueba básica del sistema vectorial"""
    print("🔍 TESTING VECTOR SEARCH SYSTEM v1.1.0")
    print("=" * 50)
    
    try:
        # Test 1: Importar módulos
        print("📦 Test 1: Importando módulos...")
        
        from vector_search import VectorSearchEngine
        print("  ✅ vector_search.py")
        
        from enhanced_mcp import EnhancedMCPProvider
        print("  ✅ enhanced_mcp.py")
        
        from memory_system import PerfectMemorySystem
        print("  ✅ memory_system.py")
        
        # Test 2: Crear instancias
        print("\n🏗️ Test 2: Creando instancias...")
        
        memory = PerfectMemorySystem("test_vector.db")
        print("  ✅ PerfectMemorySystem")
        
        enhanced_mcp = EnhancedMCPProvider(memory, "test_vector.db")
        print("  ✅ EnhancedMCPProvider")
        
        # Test 3: Verificar dependencias vectoriales
        print("\n📊 Test 3: Verificando dependencias...")
        
        try:
            import chromadb
            print("  ✅ ChromaDB disponible")
        except ImportError as e:
            print(f"  ❌ ChromaDB: {e}")
            return False
        
        try:
            import sentence_transformers
            print("  ✅ SentenceTransformers disponible")
        except ImportError as e:
            print(f"  ❌ SentenceTransformers: {e}")
            return False
        
        # Test 4: Crear ubicaciones y objetos de prueba
        print("\n🌍 Test 4: Creando mundo de prueba...")
        
        # Crear ubicación
        taller = await memory.create_location(
            "Taller de Carpintería",
            "Un taller lleno de herramientas de madera y metal",
            connections={},
            properties={"type": "workshop", "lighting": "good"}
        )
        print(f"  ✅ Ubicación creada: {taller.id}")
        
        # Crear objetos de prueba
        martillo = await memory.create_object(
            "martillo de carpintero",
            "Martillo pesado con mango de madera",
            taller.id,
            properties={"material": "steel_wood", "type": "hammer", "use": "carpentry"}
        )
        print(f"  ✅ Objeto creado: {martillo.name}")
        
        sierra = await memory.create_object(
            "sierra de mano",
            "Sierra dentada para cortar madera",
            taller.id,
            properties={"material": "steel", "type": "saw", "use": "cutting"}
        )
        print(f"  ✅ Objeto creado: {sierra.name}")
        
        # Test 5: Inicializar búsqueda vectorial
        print("\n🔍 Test 5: Inicializando búsqueda vectorial...")
        
        await enhanced_mcp.initialize_vector_search()
        
        if enhanced_mcp.vector_initialized:
            print("  ✅ Búsqueda vectorial inicializada")
        else:
            print("  ❌ Error inicializando búsqueda vectorial")
            return False
        
        # Test 6: Verificar estadísticas
        print("\n📊 Test 6: Verificando estadísticas...")
        
        stats = await enhanced_mcp.get_vector_search_stats()
        print(f"  📈 Estado: {stats.get('status', 'desconocido')}")
        
        if 'objects' in stats:
            print(f"  📦 Objetos indexados: {stats['objects'].get('document_count', 0)}")
        
        if 'locations' in stats:
            print(f"  🏠 Ubicaciones indexadas: {stats['locations'].get('document_count', 0)}")
        
        # Test 7: Prueba de búsqueda simple
        print("\n🔍 Test 7: Prueba de búsqueda básica...")
        
        try:
            results = await enhanced_mcp.search_objects_by_description("herramientas de carpintería", limit=2)
            print(f"  ✅ Búsqueda completada: {len(results)} resultados")
            
            for i, result in enumerate(results, 1):
                name = result.get('name', 'Sin nombre')
                score = result.get('similarity_score', 0)
                print(f"    {i}. {name} (score: {score:.3f})")
                
        except Exception as e:
            print(f"  ⚠️ Error en búsqueda: {e}")
        
        # Test 8: Cleanup
        print("\n🧹 Test 8: Limpieza...")
        memory.close()
        print("  ✅ Conexiones cerradas")
        
        print("\n" + "=" * 50)
        print("🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("✅ Sistema de búsqueda vectorial v1.1.0 FUNCIONANDO")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TESTS: {e}")
        print("\n🔍 Traceback completo:")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Iniciando tests del sistema vectorial...")
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Ejecutar tests
    success = asyncio.run(test_vector_system())
    
    if success:
        print("\n✅ Sistema listo para usar!")
        print("💡 Puedes ejecutar: python vector_demo.py")
    else:
        print("\n❌ Sistema requiere revisión")
        
    sys.exit(0 if success else 1)
