#!/usr/bin/env python3
"""
🔍 QUICK PROJECT STATUS CHECK
Verificación rápida del estado del proyecto para evitar confusiones

Este script debe ejecutarse SIEMPRE al inicio de cualquier sesión de trabajo
para confirmar qué funciona y qué no en el proyecto.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_file_exists(file_path, description):
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NO ENCONTRADO")
        return False

def check_database(db_path, description):
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            conn.close()
            print(f"✅ {description}: {db_path} ({table_count} tablas)")
            return True
        except Exception as e:
            print(f"⚠️ {description}: {db_path} - Error: {e}")
            return False
    else:
        print(f"❌ {description}: {db_path} - NO ENCONTRADO")
        return False

def check_port(port, description):
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True, shell=True)
        if f":{port}" in result.stdout:
            print(f"✅ {description}: Puerto {port} - ACTIVO")
            return True
        else:
            print(f"❌ {description}: Puerto {port} - NO ACTIVO")
            return False
    except:
        print(f"⚠️ {description}: Puerto {port} - NO SE PUEDE VERIFICAR")
        return False

def check_ollama():
    try:
        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama: FUNCIONANDO")
            if "llama3.2" in result.stdout:
                print(f"✅ Modelo Llama 3.2: DISPONIBLE")
            else:
                print(f"⚠️ Modelo Llama 3.2: NO ENCONTRADO")
            return True
        else:
            print(f"❌ Ollama: NO RESPONDE")
            return False
    except FileNotFoundError:
        print(f"❌ Ollama: NO INSTALADO")
        return False
    except Exception as e:
        print(f"⚠️ Ollama: Error - {e}")
        return False

def main():
    print_header("QUICK PROJECT STATUS CHECK")
    print("📅 Fecha:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Verificar archivos principales
    print_header("ARCHIVOS PRINCIPALES")
    core_files = [
        ("adventure_game.py", "Motor principal del juego"),
        ("ai_engine.py", "Motor de IA"),
        ("ai_integration.py", "Integración IA-Juego"),
        ("ai_web_server.py", "Servidor web IA"),
        ("start_ai_game.py", "Script inicio IA"),
        ("memory_system.py", "Sistema de memoria"),
        ("vector_search.py", "Búsqueda vectorial"),
        ("PROJECT_STATUS_CONTROL.md", "Archivo de control maestro")
    ]
    
    core_status = []
    for file_path, description in core_files:
        status = check_file_exists(file_path, description)
        core_status.append(status)
    
    # Verificar bases de datos
    print_header("BASES DE DATOS")
    db_files = [
        ("adventure_world.db", "BD principal del juego"),
        ("ai_adventure_web.db", "BD del sistema IA"),
        ("vector_db/chroma.sqlite3", "BD búsqueda vectorial")
    ]
    
    db_status = []
    for db_path, description in db_files:
        status = check_database(db_path, description)
        db_status.append(status)
    
    # Verificar servicios
    print_header("SERVICIOS Y PUERTOS")
    
    # Verificar Ollama
    ollama_status = check_ollama()
    
    # Verificar puertos
    ai_port_status = check_port(8091, "Servidor IA")
    web_port_status = check_port(3000, "Frontend React")
    api_port_status = check_port(8001, "Backend FastAPI")
    
    # Resumen final
    print_header("RESUMEN DEL ESTADO")
    
    core_ok = sum(core_status)
    db_ok = sum(db_status)
    
    print(f"📁 Archivos principales: {core_ok}/{len(core_files)} ({'✅' if core_ok == len(core_files) else '⚠️'})")
    print(f"💾 Bases de datos: {db_ok}/{len(db_files)} ({'✅' if db_ok >= 2 else '⚠️'})")
    print(f"🦙 Ollama: {'✅' if ollama_status else '❌'}")
    print(f"🌐 Servidor IA (8091): {'✅' if ai_port_status else '❌'}")
    
    # Recomendaciones
    print_header("RECOMENDACIONES")
    
    if core_ok == len(core_files) and db_ok >= 2 and ollama_status:
        print("✅ SISTEMA LISTO PARA USAR")
        print("🚀 Puedes ejecutar: python start_ai_game.py")
        if not ai_port_status:
            print("💡 El servidor IA no está ejecutándose, pero puede iniciarse")
    else:
        print("⚠️ SISTEMA INCOMPLETO")
        if not ollama_status:
            print("❗ Instalar/iniciar Ollama primero")
        if core_ok < len(core_files):
            print("❗ Faltan archivos principales del proyecto")
        if db_ok < 2:
            print("❗ Faltan bases de datos esenciales")
    
    print("\n📋 Consultar PROJECT_STATUS_CONTROL.md para detalles completos")
    print("🔄 Ejecutar este script regularmente para verificar estado")

if __name__ == "__main__":
    main()
