# 📊 Google Sheets MCP Server

🐍 **Python-based MCP Server** that enables Claude Desktop to interact seamlessly with Google Sheets through Google Apps Script.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 📖 **Read Operations**: Single cells, ranges, and sheet metadata  
- ✏️ **Write Operations**: Update cells and ranges with data
- 🧹 **Utility Operations**: Clear ranges and test connections
- 🔐 **Secure**: Uses Google Apps Script as secure proxy
- 🚀 **Easy Setup**: Works with Claude Desktop out of the box

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Claude Desktop installed  
- Google account with access to Google Sheets and Apps Script

### Installation

```bash
# 1. Clone this repository
git clone https://github.com/tu-usuario/google-sheets-mcp.git
cd google-sheets-mcp

# 2. Install Python dependencies
cd mcp-server
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and add your APPS_SCRIPT_URL
```

### Configuration

1. **Set up Google Apps Script** (see [detailed guide](SETUP.md))
2. **Configure Claude Desktop**:

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/absolute/path/to/google-sheets-mcp/mcp-server",
      "env": {
        "APPS_SCRIPT_URL": "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec",
        "DEBUG": "false"
      }
    }
  }
}
```

**⚠️ Important**: Replace `/absolute/path/to/` with the actual path where you cloned this repository.

3. **Restart Claude Desktop**

## 🛠️ Available Tools

| Tool | Description | Example Usage |
|------|-------------|---------------|
| `read_cell` | Read a single cell | `read_cell("Sheet1", "A1")` |
| `write_cell` | Write to a cell | `write_cell("Sheet1", "A1", "Hello")` |
| `read_range` | Read cell range | `read_range("Sheet1", "A1:B5")` |
| `write_range` | Write to range | `write_range("Sheet1", "A1:B2", data)` |
| `clear_range` | Clear cell range | `clear_range("Sheet1", "A1:B5")` |
| `list_sheets` | List all sheets | `list_sheets()` |
| `test_connection` | Test setup | `test_connection()` |

## 📚 Documentation

- [📋 Detailed Setup Guide](SETUP.md) - Step-by-step installation
- [🔧 Google Apps Script Configuration](apps-script/README.md)

## 🏗️ Architecture

```
Claude Desktop → Python MCP Server → Google Apps Script → Google Sheets
     ↑                                                          ↓
     ←←←←←←←←←← JSON Response ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

**Why this approach?**
- 🔐 **No complex OAuth**: Apps Script uses your existing Google session
- 🎯 **Focused**: Designed specifically for Google Sheets operations  
- 🚀 **Scalable**: Easy to add new functionality
- 💰 **Free**: Uses Google's free Apps Script infrastructure

## ✅ Verification

After setup, ask Claude:

> "Test the Google Sheets connection"

Claude should be able to use the `test_connection()` tool and show you it's connected.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Integrates with [Google Apps Script](https://script.google.com/)
- Part of the [Model Context Protocol](https://modelcontextprotocol.io/) ecosystem

---

**Created by**: Jona  
**Purpose**: Connect Claude with Google Sheets efficiently and securely
