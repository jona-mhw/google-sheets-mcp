# 🔧 Google Apps Script Setup Guide

Esta guía te explica cómo configurar el backend de Google Apps Script para tu MCP Server.

## 📋 Paso a Paso Detallado

### **1. Crear el Proyecto**

1. Ve a [script.google.com](https://script.google.com)
2. Click **"Nuevo proyecto"**
3. Se creará un proyecto con un archivo por defecto

### **2. Configurar el Código**

1. **Nombre del archivo**: Puedes cambiar el nombre si quieres:
   - `Code.gs` (por defecto) ✅
   - `codigo.gs` ✅
   - `main.gs` ✅ 
   - `sheets.gs` ✅
   - **Cualquier nombre funciona** - es solo cosmético

2. **Reemplazar el código**:
   - Selecciona TODO el código por defecto
   - Bórralo
   - Copia **TODO** el contenido de [`Code.gs`](Code.gs)
   - Pégalo en el editor
   - Guarda (Ctrl+S)

### **3. Desplegar como Web App**

#### **Primer Deploy**

1. Click **"Implementar"** → **"Nueva implementación"**
2. **Configuración**:
   - **Tipo**: "Aplicación web"
   - **Ejecutar como**: "Yo (tu-email@gmail.com)"
   - **Quién tiene acceso**: "Cualquier persona"
3. Click **"Implementar"**
4. **Autorizar permisos** cuando se te pida
5. **Copiar la URL** que termina en `/exec`

#### **Actualizaciones Futuras**

Si haces cambios al código:
1. Click **"Implementar"** → **"Administrar implementaciones"**
2. Click el ícono de editar (✏️)
3. **Nueva versión**: "Nueva versión"
4. Click **"Implementar"**

### **4. Configurar Permisos**

Google Apps Script puede pedirte autorización para:
- ✅ **Ver y administrar hojas de cálculo**: Necesario para leer/escribir
- ✅ **Conectarse a servicios externos**: Para responder al MCP Server

**Estos permisos son seguros** porque:
- Solo se ejecutan en **TU cuenta**
- Solo **TÚ** puedes ver/modificar el código
- No hay acceso de terceros

## 💰 Costos y Límites

### **Gratuito**
- ✅ **6 horas de ejecución por día**
- ✅ **Triggers ilimitados**
- ✅ **Almacenamiento de script ilimitado**

### **Para Uso Normal de MCP**
- Una operación típica toma **< 1 segundo**
- Puedes hacer **miles de operaciones** por día
- **Más que suficiente** para uso personal

### **Si Excedes los Límites**
- Google Apps Script se pausa hasta el siguiente día
- **No hay cargos automáticos**
- Puedes actualizar a Google Workspace para más límites

## 🔒 Seguridad Explicada

### **¿Por qué "Cualquier persona"?**

Aunque seleccionas "Cualquier persona", esto **NO significa** que cualquiera puede acceder a tus datos:

1. **La URL es secreta**: Solo tú la conoces
2. **Se ejecuta en tu cuenta**: Solo accede a TUS hojas
3. **No hay UI pública**: Es solo una API
4. **Autenticación automática**: Usa tu sesión de Google

### **¿Qué puede hacer el script?**

```javascript
// ✅ PUEDE hacer:
SpreadsheetApp.getActiveSpreadsheet() // TUS hojas
Session.getActiveUser()               // TU información

// ❌ NO PUEDE hacer:
- Acceder a otras cuentas de Google
- Enviar emails sin tu permiso
- Acceder a archivos que no compartas
```

### **Comparación con OAuth**

| **Apps Script** | **OAuth Tradicional** |
|-----------------|----------------------|
| ✅ Sin credenciales expuestas | ❌ Client ID/Secret requeridos |
| ✅ Autenticación automática | ❌ Flujo de autorización manual |
| ✅ Ejecución en tu cuenta | ⚠️ Tokens pueden expirar |
| ✅ Control total del código | ❌ Dependes de librerías externas |

## 🧪 Pruebas

### **Probar Manualmente**

1. En Apps Script, click **"Ejecutar"** → selecciona `doGet`
2. Deberías ver en los logs: información del usuario
3. Si hay errores, revisa los permisos

### **Probar con URL**

Pega tu URL en el navegador seguida de `?action=info`:
```
https://script.google.com/macros/s/tu-script-id/exec?action=info
```

Deberías ver JSON con información del servicio.

## 🔄 Mantener Actualizado

### **Versionado**

Cada vez que hagas cambios:
1. Cambios menores: **Nueva versión**
2. Cambios mayores: **Nueva implementación**

### **Backup**

- **Git**: El código está en este repositorio
- **Apps Script**: Guarda automáticamente en Google Drive
- **Export**: Puedes descargar el proyecto como .zip

## ❓ Troubleshooting

### **Error: "Permisos insuficientes"**
- Re-autoriza el script desde la configuración
- Verifica que tienes acceso al Spreadsheet

### **Error: "Script not found"**
- Verifica que la URL es correcta
- Asegúrate de que el script está desplegado

### **Error: "Tiempo de ejecución excedido"**
- Optimiza las operaciones (usa rangos en lugar de celdas individuales)
- Verifica que no hay bucles infinitos

### **La URL cambió**
- Cada nueva implementación genera nueva URL
- Actualiza tu `.env` con la nueva URL

---

**💡 Tip**: Guarda la URL de tu Apps Script en un lugar seguro. Es la única conexión entre tu MCP y Google Sheets.
