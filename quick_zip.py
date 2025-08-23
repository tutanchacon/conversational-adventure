import zipfile
from pathlib import Path
from datetime import datetime

zip_name = f'Adventure_Game_MCP_Documentation_{datetime.now().strftime("%Y%m%d_%H%M")}.zip'
files = ['ANALISIS_COMPLETO_MCP.md', 'RESUMEN_EJECUTIVO_MCP.md', 'README.md', 'memory_system.py', 'mcp_integration.py', 'adventure_game.py', 'demo_game.py', 'requirements.txt']

with zipfile.ZipFile(zip_name, 'w') as zipf:
    for f in files:
        if Path(f).exists():
            zipf.write(f)
            print(f'✅ {f}')

print(f'📦 Paquete creado: {zip_name}')
print(f'📏 Tamaño: {Path(zip_name).stat().st_size:,} bytes')
