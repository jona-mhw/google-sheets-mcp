# 📊 Google Sheets MCP Server

🐍 **Servidor MCP basado en Python** que permite a Claude Desktop interactuar de manera fluida con Google Sheets a través de Google Apps Script.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🔬 Proyecto de Investigación**: Este es un proyecto de desarrollo experimental que demuestra las capacidades del Model Context Protocol (MCP) y la integración segura con APIs de Google. Desarrollado como prueba de concepto para explorar nuevas formas de conectar IA con herramientas de productividad.

## ✨ Características

- 📖 **Operaciones de Lectura**: Celdas individuales, rangos y metadatos de hojas  
- ✏️ **Operaciones de Escritura**: Actualizar celdas y rangos con datos
- 🧹 **Operaciones de Utilidad**: Limpiar rangos y probar conexiones
- 🔐 **Seguro**: Usa Google Apps Script como proxy seguro en tu propia cuenta
- 🚀 **Configuración Fácil**: Funciona con Claude Desktop sin configuraciones complejas

## 🔒 Seguridad y Privacidad

### **🛡️ Múltiples Capas de Seguridad**

1. **Google Apps Script (Tu Cuenta)**:
   - Se ejecuta en **TU infraestructura de Google**
   - Solo **TÚ** tienes acceso a tus datos
   - Autenticación automática con tu sesión de Google
   - Sin credenciales OAuth expuestas

2. **Model Context Protocol (MCP)**:
   - Protocolo estándar abierto de Anthropic
   - Comunicación segura localhost-only
   - Sin datos transmitidos a terceros
   - Control total sobre qué herramientas exponer

3. **Arquitectura Local**:
   - El servidor MCP se ejecuta en **TU máquina**
   - Ningún dato sale de tu control
   - Sin servidores externos involucrados

### **🎯 ¿Por qué es Seguro?**

```
TUS DATOS → Google Sheets (TU cuenta) → Apps Script (TU cuenta) → MCP Server (TU máquina) → Claude Desktop (TU máquina)
```

**Resultado**: Tus datos NUNCA salen de tu ecosistema personal.

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8+ instalado
- Claude Desktop instalado  
- Cuenta de Google con acceso a Google Sheets y Apps Script

### Instalación

```bash
# 1. Clonar este repositorio
git clone https://github.com/jona-mhw/google-sheets-mcp.git
cd google-sheets-mcp

# 2. Instalar dependencias de Python
cd mcp-server
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar tu APPS_SCRIPT_URL
```

### Configuración de Google Apps Script

#### **Paso 1: Crear el Proyecto Apps Script**

1. Ve a [script.google.com](https://script.google.com)
2. Click "Nuevo proyecto"
3. **Importante**: El nombre del archivo puede ser cualquier cosa (`Code.gs`, `codigo.gs`, `main.gs`, etc.)

#### **Paso 2: Copiar el Código**

1. Borra el código por defecto
2. Copia **TODO** el contenido de [`apps-script/Code.gs`](apps-script/Code.gs)
3. Pégalo en tu proyecto
4. Guarda el proyecto (Ctrl+S)

#### **Paso 3: Desplegar como Web App**

1. Click **"Implementar"** > **"Nueva implementación"**
2. **Tipo**: Selecciona **"Aplicación web"**
3. **Configuración**:
   - **Ejecutar como**: "Yo" (tu cuenta)
   - **Quién tiene acceso**: "Cualquier persona" 
4. Click **"Implementar"**

> **⚠️ Costos**: Google Apps Script es **GRATUITO** hasta 6 horas de tiempo de ejecución por día. Para uso normal de hojas de cálculo, esto es más que suficiente.

#### **Paso 4: Obtener la URL**

1. Copia la **URL de la aplicación web** (termina en `/exec`)
2. Esta es tu `APPS_SCRIPT_URL`

### Configuración de Claude Desktop

1. **Encuentra tu archivo de configuración**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Agrega la configuración del MCP**:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/ruta/absoluta/a/google-sheets-mcp/mcp-server",
      "env": {
        "APPS_SCRIPT_URL": "https://script.google.com/macros/s/TU_SCRIPT_ID/exec",
        "DEBUG": "false"
      }
    }
  }
}
```

**⚠️ Importante**: Reemplaza `/ruta/absoluta/a/` con la ruta completa donde clonaste este repositorio.

**Ejemplos de rutas**:
- **macOS/Linux**: `/Users/tu-usuario/google-sheets-mcp/mcp-server`
- **Windows**: `C:\\Users\\tu-usuario\\google-sheets-mcp\\mcp-server`

3. **Reiniciar Claude Desktop**

## 🛠️ Herramientas Disponibles

| Herramienta | Descripción | Ejemplo de Uso |
|-------------|-------------|----------------|
| `read_cell` | Leer una celda individual | `read_cell("Hoja1", "A1")` |
| `write_cell` | Escribir en una celda | `write_cell("Hoja1", "A1", "Hola")` |
| `read_range` | Leer rango de celdas | `read_range("Hoja1", "A1:B5")` |
| `write_range` | Escribir en rango | `write_range("Hoja1", "A1:B2", datos)` |
| `clear_range` | Limpiar rango de celdas | `clear_range("Hoja1", "A1:B5")` |
| `list_sheets` | Listar todas las hojas | `list_sheets()` |
| `test_connection` | Probar configuración | `test_connection()` |

## 🏗️ Arquitectura

```
Claude Desktop → Servidor MCP Python → Google Apps Script → Google Sheets
     ↑                                                            ↓
     ←←←←←←←←←← Respuesta JSON ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

**¿Por qué este enfoque?**
- 🔐 **Sin OAuth complejo**: Apps Script usa tu sesión existente de Google
- 🎯 **Enfocado**: Diseñado específicamente para operaciones de Google Sheets  
- 🚀 **Escalable**: Fácil agregar nueva funcionalidad
- 💰 **Gratuito**: Usa la infraestructura gratuita de Google Apps Script
- 🛡️ **Privado**: Todo permanece en tu cuenta personal

## ✅ Verificación

Después de la configuración, pregunta a Claude:

> "Prueba la conexión con Google Sheets"

Claude debería poder usar la herramienta `test_connection()` y mostrarte que está conectado.

## 🔍 Troubleshooting

### Error: "No module named 'fastmcp'"
```bash
pip install -r requirements.txt
```

### Error: "APPS_SCRIPT_URL no está configurada"
- Verifica que el archivo `.env` existe
- Verifica que la URL es correcta
- Asegúrate de que el Apps Script está desplegado como Web App

### Claude no ve el MCP
- Verifica que la ruta en `cwd` es absoluta y correcta
- Reinicia Claude Desktop completamente
- Revisa que el JSON de configuración es válido

### Error de permisos en Apps Script
- Asegúrate de que el Apps Script está desplegado con permisos "Cualquier persona"
- Verifica que el Spreadsheet existe y tienes acceso

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama de feature (`git checkout -b feature/increible-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar increíble característica'`)
4. Push a la rama (`git push origin feature/increible-caracteristica`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Reconocimientos

- Construido con [FastMCP](https://github.com/jlowin/fastmcp)
- Se integra con [Google Apps Script](https://script.google.com/)
- Parte del ecosistema [Model Context Protocol](https://modelcontextprotocol.io/)

---

**Creado por**: Jona  
**Propósito**: Conectar Claude con Google Sheets de manera eficiente y segura  
**Tipo**: Proyecto de investigación y desarrollo - Prueba de concepto MCP
