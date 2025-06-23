# 📊 Google Sheets MCP Server

🐍 **Python-based MCP Server** that enables Claude Desktop to interact seamlessly with Google Sheets through Google Apps Script.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🔬 Research Project**: This is an experimental development project demonstrating Model Context Protocol (MCP) capabilities and secure Google API integration. Developed as a proof of concept to explore new ways of connecting AI with productivity tools.

## ✨ Features

- 📖 **Read Operations**: Single cells, ranges, and sheet metadata  
- ✏️ **Write Operations**: Update cells and ranges with data
- 🧹 **Utility Operations**: Clear ranges and test connections
- 🔐 **Secure**: Uses Google Apps Script as secure proxy within your own account
- 🚀 **Easy Setup**: Works with Claude Desktop without complex configurations

## 🔒 Security & Privacy

### **🛡️ Multiple Security Layers**

1. **Google Apps Script (Your Account)**:
   - Runs in **YOUR Google infrastructure**
   - Only **YOU** have access to your data
   - Automatic authentication with your Google session
   - No exposed OAuth credentials

2. **Model Context Protocol (MCP)**:
   - Open standard protocol by Anthropic
   - Secure localhost-only communication
   - No data transmitted to third parties
   - Full control over exposed tools

3. **Local Architecture**:
   - MCP server runs on **YOUR machine**
   - No data leaves your control
   - No external servers involved

### **🎯 Why is it Secure?**

```
YOUR DATA → Google Sheets (YOUR account) → Apps Script (YOUR account) → MCP Server (YOUR machine) → Claude Desktop (YOUR machine)
```

**Result**: Your data NEVER leaves your personal ecosystem.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Claude Desktop installed  
- Google account with access to Google Sheets and Apps Script

### Installation

```bash
# 1. Clone this repository
git clone https://github.com/jona-mhw/google-sheets-mcp.git
cd google-sheets-mcp

# 2. Install Python dependencies
cd mcp-server
pip install -r requirements.txt

# 3. Configure environment variables
cp .env.example .env
# Edit .env and add your APPS_SCRIPT_URL
```

### Google Apps Script Setup

#### **Step 1: Create Apps Script Project**

1. Go to [script.google.com](https://script.google.com)
2. Click "New project"
3. **Important**: The file name can be anything (`Code.gs`, `main.gs`, `sheets.gs`, etc.)

#### **Step 2: Copy the Code**

1. Delete the default code
2. Copy **ALL** content from [`apps-script/Code.gs`](apps-script/Code.gs)
3. Paste it into your project
4. Save the project (Ctrl+S)

#### **Step 3: Deploy as Web App**

1. Click **"Deploy"** > **"New deployment"**
2. **Type**: Select **"Web app"**
3. **Configuration**:
   - **Execute as**: "Me" (your account)
   - **Who has access**: "Anyone" 
4. Click **"Deploy"**

> **⚠️ Costs**: Google Apps Script is **FREE** up to 6 hours of execution time per day. For normal spreadsheet usage, this is more than sufficient.

#### **Step 4: Get the URL**

1. Copy the **Web app URL** (ends with `/exec`)
2. This is your `APPS_SCRIPT_URL`

### Claude Desktop Configuration

1. **Find your configuration file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP configuration**:

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

**Path examples**:
- **macOS/Linux**: `/Users/your-username/google-sheets-mcp/mcp-server`
- **Windows**: `C:\\Users\\your-username\\google-sheets-mcp\\mcp-server`

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
- 🛡️ **Private**: Everything stays within your personal account

## ✅ Verification

After setup, ask Claude:

> "Test the Google Sheets connection"

Claude should be able to use the `test_connection()` tool and show you it's connected.

## 🔍 Troubleshooting

### Error: "No module named 'fastmcp'"
```bash
pip install -r requirements.txt
```

### Error: "APPS_SCRIPT_URL not configured"
- Verify that the `.env` file exists
- Verify that the URL is correct
- Ensure the Apps Script is deployed as Web App

### Claude doesn't see the MCP
- Verify that the `cwd` path is absolute and correct
- Restart Claude Desktop completely
- Check that the JSON configuration is valid

### Apps Script permission errors
- Ensure the Apps Script is deployed with "Anyone" permissions
- Verify that the Spreadsheet exists and you have access

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
**Type**: Research & Development Project - MCP Proof of Concept
