
# Generador de PDF para el Análisis MCP
# Requiere: pip install markdown pdfkit weasyprint

import markdown
import pdfkit
from pathlib import Path
import weasyprint
from datetime import datetime

def markdown_to_pdf(markdown_file: str, output_file: str, method: str = "weasyprint"):
    """Convierte Markdown a PDF usando diferentes métodos"""
    
    # Leer archivo Markdown
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convertir Markdown a HTML
    html = markdown.markdown(markdown_content, extensions=['tables', 'codehilite', 'toc'])
    
    # CSS para mejorar el formato
    css_style = """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        margin: 40px;
        color: #333;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #34495e;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    
    h3 {
        color: #7f8c8d;
        margin-top: 25px;
    }
    
    code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Consolas', 'Monaco', monospace;
    }
    
    pre {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        overflow-x: auto;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    .emoji {
        font-size: 1.2em;
    }
    
    @page {
        size: A4;
        margin: 2cm;
    }
    
    .page-break {
        page-break-before: always;
    }
    </style>
    """
    
    # HTML completo
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Análisis Completo MCP - Adventure Game</title>
        {css_style}
    </head>
    <body>
        <div class="header">
            <h1>🎮 ANÁLISIS COMPLETO DEL PROYECTO PARA MCP</h1>
            <p><strong>Adventure Game con Sistema de Memoria Perfecta</strong></p>
            <p>Generado el: {datetime.now().strftime("%d de %B, %Y")}</p>
            <hr>
        </div>
        {html}
        <div class="footer">
            <hr>
            <p><em>Documento generado automáticamente desde ANALISIS_COMPLETO_MCP.md</em></p>
        </div>
    </body>
    </html>
    """
    
    if method == "weasyprint":
        try:
            # Método preferido: WeasyPrint
            weasyprint.HTML(string=full_html).write_pdf(output_file)
            print(f"✅ PDF generado exitosamente: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error con WeasyPrint: {e}")
            return False
    
    elif method == "pdfkit":
        try:
            # Método alternativo: pdfkit + wkhtmltopdf
            options = {
                'page-size': 'A4',
                'margin-top': '2cm',
                'margin-right': '2cm',
                'margin-bottom': '2cm',
                'margin-left': '2cm',
                'encoding': "UTF-8",
                'no-outline': None,
                'enable-local-file-access': None
            }
            
            pdfkit.from_string(full_html, output_file, options=options)
            print(f"✅ PDF generado exitosamente: {output_file}")
            return True
        except Exception as e:
            print(f"❌ Error con pdfkit: {e}")
            return False
    
    return False

def main():
    """Función principal del generador"""
    markdown_file = "ANALISIS_COMPLETO_MCP.md"
    pdf_file = "ANALISIS_COMPLETO_MCP.pdf"
    
    print("📄 GENERADOR DE PDF - ANÁLISIS MCP")
    print("=" * 50)
    
    if not Path(markdown_file).exists():
        print(f"❌ Archivo no encontrado: {markdown_file}")
        return
    
    print(f"📖 Leyendo: {markdown_file}")
    print(f"📝 Generando: {pdf_file}")
    
    # Intentar con WeasyPrint primero
    success = markdown_to_pdf(markdown_file, pdf_file, "weasyprint")
    
    if not success:
        print("🔄 Intentando con método alternativo...")
        success = markdown_to_pdf(markdown_file, pdf_file, "pdfkit")
    
    if success:
        print(f"🎉 ¡PDF generado correctamente!")
        print(f"📍 Ubicación: {Path(pdf_file).absolute()}")
        
        # Mostrar información del archivo
        file_size = Path(pdf_file).stat().st_size / 1024  # KB
        print(f"📊 Tamaño: {file_size:.1f} KB")
    else:
        print("❌ No se pudo generar el PDF")
        print("💡 Intenta instalar las dependencias:")
        print("   pip install markdown weasyprint")
        print("   # o alternativamente:")
        print("   pip install markdown pdfkit")

if __name__ == "__main__":
    main()
