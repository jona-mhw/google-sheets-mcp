# Google Sheets MCP Server

Servidor MCP en Python que permite a Claude (Desktop o cualquier cliente MCP) leer y
escribir Google Sheets a través de un Google Apps Script desplegado como Web App.

## Qué hace

- Lectura: celdas, rangos y metadatos de hoja.
- Escritura: celdas y rangos.
- Utilidad: limpiar rangos, listar hojas, probar la conexión.

## Cómo funciona

```
Cliente MCP  →  servidor MCP (Python, local)  →  Apps Script Web App  →  Google Sheets
```

El Apps Script corre en tu propia cuenta de Google con tu sesión, así que no expones
credenciales OAuth ni tokens. El servidor MCP corre en tu máquina.

## Seguridad — léelo antes de desplegar

El Web App se publica con "Ejecutar como: yo" y acceso "Cualquiera". Eso significa que
**la URL `/exec` es un endpoint sin autenticación**: quien la conozca puede leer y
escribir tu hoja. En consecuencia:

- Trata la URL del Web App como un secreto. No la publiques ni la commitees.
- Para algo más que pruebas, añade un token compartido: que el Apps Script exija un
  parámetro secreto y rechace las peticiones que no lo traigan.

La protección real es que la URL sea privada (e, idealmente, un token); no hay "varias
capas de seguridad" más allá de eso.

## Requisitos

- Python 3.8+
- Un cliente MCP (por ejemplo, Claude Desktop)
- Cuenta de Google con acceso a Sheets y Apps Script

## Instalación

```bash
git clone https://github.com/jona-mhw/google-sheets-mcp.git
cd google-sheets-mcp/mcp-server
pip install -r requirements.txt
cp .env.example .env
# edita .env y pon tu APPS_SCRIPT_URL
```

## Apps Script

1. En [script.google.com](https://script.google.com) crea un proyecto nuevo.
2. Pega el contenido de [`apps-script/Code.gs`](apps-script/Code.gs).
3. Desplegar → Nueva implementación → Aplicación web. Ejecutar como: yo. Acceso: cualquiera.
4. Copia la URL que termina en `/exec`: esa es tu `APPS_SCRIPT_URL`.

Apps Script es gratis hasta 6 horas de ejecución por día, de sobra para uso normal.

## Configuración del cliente MCP

Archivo de configuración de Claude Desktop:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

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

Reinicia el cliente.

## Herramientas

| Tool | Descripción |
|------|-------------|
| `read_cell` | lee una celda |
| `write_cell` | escribe una celda |
| `read_range` | lee un rango |
| `write_range` | escribe un rango |
| `clear_range` | limpia un rango |
| `list_sheets` | lista las hojas |
| `test_connection` | prueba la conexión |

## Problemas frecuentes

- `No module named 'fastmcp'`: `pip install -r requirements.txt`.
- `APPS_SCRIPT_URL not configured`: revisa que `.env` exista y que la URL sea correcta.
- Claude no ve el MCP: `cwd` debe ser ruta absoluta; reinicia el cliente.

## Licencia

MIT. Ver [LICENSE](LICENSE). Construido sobre [FastMCP](https://github.com/jlowin/fastmcp).
