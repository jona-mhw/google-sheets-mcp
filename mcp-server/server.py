#!/usr/bin/env python3
"""
Google Sheets MCP Server
Servidor MCP que conecta Claude con Google Sheets via Apps Script
"""

from fastmcp import FastMCP
import requests
import os
import json
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
APPS_SCRIPT_URL = os.getenv("APPS_SCRIPT_URL", "")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Crear instancia del servidor MCP
mcp = FastMCP("Google Sheets MCP Server")

@mcp.tool()
def read_cell(sheet_name: str = "demo", cell: str = "A1") -> str:
    """
    Lee el valor de una celda específica de Google Sheets
    
    Args:
        sheet_name: Nombre de la hoja (default: "demo")
        cell: Celda en notación A1 (default: "A1")
    
    Returns:
        El valor de la celda como string
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.get(
            APPS_SCRIPT_URL,
            params={
                "action": "read_cell",
                "sheet": sheet_name,
                "cell": cell
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            value = data.get("value", "")
            display_value = data.get("displayValue", "")
            cell_type = data.get("type", "unknown")
            
            return f"📊 Valor en {sheet_name}!{cell}: '{display_value}' (tipo: {cell_type})"
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Error: Timeout connecting to Google Sheets (>10s)"
    except requests.exceptions.ConnectionError:
        return "🔌 Error: No se pudo conectar con Google Apps Script"
    except json.JSONDecodeError:
        return f"📄 Error: Respuesta inválida del servidor - {response.text[:100]}"
    except Exception as e:
        return f"🚨 Error inesperado: {str(e)}"

@mcp.tool()
def list_sheets() -> str:
    """
    Lista todas las hojas disponibles en el spreadsheet
    
    Returns:
        Lista de hojas con información básica
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.get(
            APPS_SCRIPT_URL,
            params={"action": "list_sheets"},
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            sheets = data.get("sheets", [])
            spreadsheet_name = data.get("spreadsheetName", "Desconocido")
            total_sheets = data.get("totalSheets", len(sheets))
            
            if not sheets:
                return "📋 No se encontraron hojas en el spreadsheet"
            
            result = f"📚 Spreadsheet: {spreadsheet_name}\n"
            result += f"🔢 Total de hojas: {total_sheets}\n\n"
            
            for i, sheet in enumerate(sheets, 1):
                result += f"{i}. 📄 {sheet['name']}\n"
                result += f"   • Filas: {sheet['rows']}, Columnas: {sheet['columns']}\n"
                if sheet.get('hidden'):
                    result += f"   • Estado: Oculta\n"
                result += "\n"
            
            return result
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except Exception as e:
        return f"🚨 Error: {str(e)}"

@mcp.tool()
def get_spreadsheet_info() -> str:
    """
    Obtiene información general del spreadsheet
    
    Returns:
        Información detallada del spreadsheet
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.get(
            APPS_SCRIPT_URL,
            params={"action": "get_sheet_info"},
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            result = f"📊 INFORMACIÓN DEL SPREADSHEET\n"
            result += f"═══════════════════════════════\n"
            result += f"📝 Nombre: {data.get('spreadsheetName', 'Desconocido')}\n"
            result += f"🆔 ID: {data.get('spreadsheetId', 'Desconocido')}\n"
            result += f"🔗 URL: {data.get('url', 'No disponible')}\n"
            result += f"🌍 Locale: {data.get('locale', 'No disponible')}\n"
            result += f"⏰ Zona Horaria: {data.get('timeZone', 'No disponible')}\n"
            result += f"📄 Total de hojas: {data.get('totalSheets', 0)}\n"
            result += f"👤 Usuario: {data.get('owner', 'No disponible')}\n"
            result += f"📅 Consultado: {data.get('timestamp', 'No disponible')}\n"
            
            return result
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except Exception as e:
        return f"🚨 Error: {str(e)}"

@mcp.tool()
def test_connection() -> str:
    """
    Prueba la conexión con Google Apps Script
    
    Returns:
        Estado de la conexión y diagnósticos
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada.\n\n📝 Para configurar:\n1. Edita el archivo .env\n2. Agrega: APPS_SCRIPT_URL=tu_url_aqui"
    
    try:
        response = requests.get(
            APPS_SCRIPT_URL,
            params={"action": "info"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = f"✅ CONEXIÓN EXITOSA\n"
                result += f"═══════════════════\n"
                result += f"🔗 URL: {APPS_SCRIPT_URL}\n"
                result += f"⏱️ Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s\n"
                result += f"🎯 Servicio: {data.get('service', 'Google Sheets MCP Backend')}\n"
                result += f"📦 Versión: {data.get('version', '1.0.0')}\n"
                result += f"👤 Usuario: {data.get('user', 'No disponible')}\n"
                result += f"🛠️ Acciones disponibles: {len(data.get('availableActions', []))}\n"
                return result
            else:
                return f"⚠️ Conectado pero hay errores: {data.get('error', 'Error desconocido')}"
        else:
            return f"❌ Error HTTP {response.status_code}: {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return "⏱️ Error: Timeout (>10s) - verifique la URL de Apps Script"
    except requests.exceptions.ConnectionError:
        return "🔌 Error: No se pudo conectar - verifique la URL y acceso a internet"
    except Exception as e:
        return f"🚨 Error inesperado: {str(e)}"

@mcp.tool()
def write_cell(sheet_name: str = "demo", cell: str = "A1", value: str = "") -> str:
    """
    Escribe un valor en una celda específica de Google Sheets
    
    Args:
        sheet_name: Nombre de la hoja (default: "demo")
        cell: Celda en notación A1 (default: "A1")
        value: Valor a escribir (puede ser texto, número o fórmula que empiece con "=")
    
    Returns:
        Confirmación de la escritura
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.post(
            APPS_SCRIPT_URL,
            json={
                "action": "write_cell",
                "sheet_name": sheet_name,
                "cell": cell,
                "value": value
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            return f"✅ Valor escrito exitosamente en {sheet_name}!{cell}: '{value}'"
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except Exception as e:
        return f"🚨 Error: {str(e)}"

@mcp.tool()
def write_range(sheet_name: str = "demo", range_notation: str = "A1:B2", values: str = "") -> str:
    """
    Escribe datos en un rango de celdas de Google Sheets
    
    Args:
        sheet_name: Nombre de la hoja (default: "demo")
        range_notation: Rango en notación A1 (ej: "A1:B2")
        values: Datos en formato JSON array 2D (ej: '[["A1","B1"],["A2","B2"]]')
    
    Returns:
        Confirmación de la escritura
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        # Intentar parsear los valores JSON
        import json
        values_array = json.loads(values) if values else []
        
        response = requests.post(
            APPS_SCRIPT_URL,
            json={
                "action": "write_range",
                "sheet_name": sheet_name,
                "range_notation": range_notation,
                "values": values_array
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            rows_written = data.get("rows_written", 0)
            cols_written = data.get("columns_written", 0)
            return f"✅ Datos escritos exitosamente en {sheet_name}!{range_notation} ({rows_written}x{cols_written} celdas)"
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except json.JSONDecodeError:
        return "❌ Error: Los valores deben estar en formato JSON válido. Ejemplo: [[\"A1\",\"B1\"],[\"A2\",\"B2\"]]"
    except Exception as e:
        return f"🚨 Error: {str(e)}"

@mcp.tool()
def clear_range(sheet_name: str = "demo", range_notation: str = "A1:B2") -> str:
    """
    Limpia el contenido de un rango de celdas en Google Sheets
    
    Args:
        sheet_name: Nombre de la hoja (default: "demo")
        range_notation: Rango en notación A1 (ej: "A1:B2")
    
    Returns:
        Confirmación de la limpieza
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.post(
            APPS_SCRIPT_URL,
            json={
                "action": "clear_range",
                "sheet_name": sheet_name,
                "range_notation": range_notation
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            return f"✅ Rango {sheet_name}!{range_notation} limpiado exitosamente"
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except Exception as e:
        return f"🚨 Error: {str(e)}"

@mcp.tool()
def read_range(sheet_name: str = "demo", range_notation: str = "A1:B2") -> str:
    """
    Lee un rango de celdas de Google Sheets
    
    Args:
        sheet_name: Nombre de la hoja (default: "demo")
        range_notation: Rango en notación A1 (ej: "A1:B2")
    
    Returns:
        Los valores del rango como tabla formateada
    """
    if not APPS_SCRIPT_URL:
        return "❌ Error: APPS_SCRIPT_URL no está configurada"
    
    try:
        response = requests.get(
            APPS_SCRIPT_URL,
            params={
                "action": "read_range",
                "sheet": sheet_name,
                "range": range_notation
            },
            timeout=10
        )
        
        if response.status_code != 200:
            return f"❌ Error HTTP {response.status_code}: {response.text}"
        
        data = response.json()
        
        if data.get("success"):
            values = data.get("values", [])
            rows = data.get("rows", 0)
            cols = data.get("cols", 0)
            
            if not values or not any(row for row in values):
                return f"📋 El rango {sheet_name}!{range_notation} está vacío"
            
            result = f"📊 Rango {sheet_name}!{range_notation} ({rows}x{cols})\n"
            result += "═" * 40 + "\n\n"
            
            # Formatear como tabla
            for i, row in enumerate(values):
                result += f"Fila {i+1}: "
                for j, cell in enumerate(row):
                    result += f"[{chr(65+j)}{i+1}] {cell}  "
                result += "\n"
            
            return result
        else:
            return f"❌ Error: {data.get('error', 'Error desconocido')}"
            
    except Exception as e:
        return f"🚨 Error: {str(e)}"

def main():
    """Función principal para ejecutar el servidor MCP"""
    print("🚀 Iniciando Google Sheets MCP Server...")
    print("═" * 50)
    
    if not APPS_SCRIPT_URL:
        print("⚠️  ADVERTENCIA: APPS_SCRIPT_URL no está configurada")
        print("   📝 Edite el archivo .env y configure la URL de Apps Script")
        print("   📋 Ejemplo: APPS_SCRIPT_URL=https://script.google.com/.../exec")
        print()
    else:
        print(f"🔗 Apps Script URL configurada: ✅")
        if DEBUG:
            print(f"   URL: {APPS_SCRIPT_URL}")
    
    print("📋 Herramientas MCP disponibles:")
    print("   🔍 test_connection() - Probar conexión con Apps Script")
    print("   📖 read_cell(sheet, cell) - Leer valor de celda")
    print("   📄 list_sheets() - Listar hojas del spreadsheet")
    print("   📊 get_spreadsheet_info() - Información del spreadsheet")
    print("   📋 read_range(sheet, range) - Leer rango de celdas")
    print("   ✏️ write_cell(sheet, cell, value) - Escribir valor en celda")
    print("   📝 write_range(sheet, range, values) - Escribir datos en rango")
    print("   🧹 clear_range(sheet, range) - Limpiar contenido de rango")
    print()
    print("✅ Servidor MCP listo para conexiones...")
    print("🔗 Para conectar desde Claude Desktop, configure claude_desktop_config.json")
    print("═" * 50)
    
    # Ejecutar el servidor MCP
    mcp.run()

if __name__ == "__main__":
    main()
