#!/usr/bin/env python3
"""
🔧 TEST AI COMMUNICATION - Adventure Game v3.0
Script de diagnóstico para probar la comunicación con la IA
"""

import asyncio
import json
import urllib.request
import urllib.parse
import logging
import os
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AICommDiagnostic:
    """Diagnóstico de comunicación AI"""
    
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
        logger.info(f"🔧 Diagnóstico AI - Host: {self.ollama_host}, Model: {self.ollama_model}")
    
    async def test_ollama_connection(self) -> bool:
        """Test 1: Verificar conexión básica con Ollama"""
        logger.info("📡 Test 1: Verificando conexión con Ollama...")
        
        try:
            # Test endpoint de salud
            req = urllib.request.Request(f"{self.ollama_host}/api/version")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                logger.info(f"✅ Ollama conectado - Versión: {result.get('version', 'unknown')}")
                return True
                
        except Exception as e:
            logger.error(f"❌ Error conectando con Ollama: {e}")
            return False
    
    async def test_model_availability(self) -> bool:
        """Test 2: Verificar que el modelo está disponible"""
        logger.info("🤖 Test 2: Verificando disponibilidad del modelo...")
        
        try:
            req = urllib.request.Request(f"{self.ollama_host}/api/tags")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                models = [model['name'] for model in result.get('models', [])]
                
                logger.info(f"📋 Modelos disponibles: {models}")
                
                if self.ollama_model in models:
                    logger.info(f"✅ Modelo {self.ollama_model} disponible")
                    return True
                else:
                    logger.error(f"❌ Modelo {self.ollama_model} no encontrado")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error verificando modelos: {e}")
            return False
    
    async def test_simple_generation(self) -> bool:
        """Test 3: Probar generación simple de texto"""
        logger.info("✨ Test 3: Probando generación simple de texto...")
        
        try:
            # Preparar datos para Ollama
            data = {
                "model": self.ollama_model,
                "prompt": "Responde brevemente: ¿Cómo estás?",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 50
                }
            }
            
            # Convertir datos a JSON
            json_data = json.dumps(data).encode('utf-8')
            
            # Crear petición HTTP
            req = urllib.request.Request(
                f"{self.ollama_host}/api/generate",
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Realizar petición
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result.get("response", "").strip()
                
                if content:
                    logger.info(f"✅ Respuesta generada: '{content}'")
                    return True
                else:
                    logger.error("❌ Respuesta vacía del modelo")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error en generación: {e}")
            return False
    
    async def test_adventure_prompt(self) -> bool:
        """Test 4: Probar prompt específico de aventura"""
        logger.info("🎮 Test 4: Probando prompt de aventura...")
        
        adventure_prompt = """
        Eres un narrador de aventuras medieval. El jugador acaba de entrar en una habitación misteriosa.
        Describe brevemente lo que ve (máximo 3 líneas).
        """
        
        try:
            # Preparar datos para Ollama
            data = {
                "model": self.ollama_model,
                "prompt": adventure_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 100
                }
            }
            
            # Convertir datos a JSON
            json_data = json.dumps(data).encode('utf-8')
            
            # Crear petición HTTP
            req = urllib.request.Request(
                f"{self.ollama_host}/api/generate",
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            # Realizar petición
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                content = result.get("response", "").strip()
                
                if content:
                    logger.info(f"✅ Narrativa generada:")
                    logger.info(f"   {content}")
                    return True
                else:
                    logger.error("❌ No se generó narrativa")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Error en narrativa: {e}")
            return False
    
    async def test_ai_engine_integration(self) -> bool:
        """Test 5: Probar integración con AI Engine"""
        logger.info("🧠 Test 5: Probando integración con AI Engine...")
        
        try:
            from ai_integration import create_ai_game
            
            # Crear instancia del juego AI
            logger.info("Inicializando AI Adventure Game...")
            game = await create_ai_game("test_ai_comm.db")
            
            # Probar comando simple
            logger.info("Enviando comando de prueba...")
            result = await game.process_command("test_player", "mirar alrededor")
            
            if result and result.get("success"):
                logger.info(f"✅ AI Engine funcionando:")
                logger.info(f"   Narrativa: {result.get('narrative', 'Sin narrativa')[:100]}...")
                return True
            else:
                logger.error(f"❌ AI Engine falló: {result}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en AI Engine: {e}")
            return False
    
    async def run_full_diagnostic(self):
        """Ejecutar diagnóstico completo"""
        logger.info("🔧 INICIANDO DIAGNÓSTICO COMPLETO DE IA")
        logger.info("=" * 50)
        
        tests = [
            ("Conexión Ollama", self.test_ollama_connection),
            ("Disponibilidad Modelo", self.test_model_availability),
            ("Generación Simple", self.test_simple_generation),
            ("Prompt Aventura", self.test_adventure_prompt),
            ("Integración AI Engine", self.test_ai_engine_integration)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            logger.info(f"\n🧪 Ejecutando: {test_name}")
            try:
                success = await test_func()
                results[test_name] = success
                if success:
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    logger.info(f"❌ {test_name}: FAILED")
            except Exception as e:
                logger.error(f"💥 {test_name}: ERROR - {e}")
                results[test_name] = False
        
        # Resumen final
        logger.info("\n" + "=" * 50)
        logger.info("📊 RESUMEN DEL DIAGNÓSTICO")
        logger.info("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
        
        logger.info(f"\nResultado: {passed}/{total} tests pasados")
        
        if passed == total:
            logger.info("🎉 ¡TODOS LOS TESTS PASARON! El sistema AI está funcionando correctamente.")
        else:
            logger.info("⚠️  Algunos tests fallaron. Revisa los errores arriba.")
        
        return results

async def main():
    """Función principal"""
    diagnostic = AICommDiagnostic()
    await diagnostic.run_full_diagnostic()

if __name__ == "__main__":
    asyncio.run(main())
