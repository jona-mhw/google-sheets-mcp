/**
 * Google Sheets MCP Backend - Apps Script
 * Proporciona endpoints HTTP para el servidor MCP
 * Usa autenticación automática con Session.getActiveUser()
 */

function doGet(e) {
  try {
    // Log para debugging
    const action = e.parameter.action || "info";
    const sheetName = e.parameter.sheet || "demo";
    const cell = e.parameter.cell || "A1";
    const range = e.parameter.range;
    
    console.log(`MCP Request: action=${action}, sheet=${sheetName}, cell=${cell}`);
    
    // Rutear según la acción
    switch(action) {
      case "read_cell":
        return handleReadCell(sheetName, cell);
        
      case "read_range":
        return handleReadRange(sheetName, range || cell);
        
      case "list_sheets":
        return handleListSheets();
        
      case "get_sheet_info":
        return handleGetSheetInfo();
        
      case "info":
        return handleInfo();
        
      default:
        return createErrorResponse(`Acción no válida: ${action}`);
    }
    
  } catch (error) {
    console.error("Error en doGet:", error);
    return createErrorResponse(`Error del servidor: ${error.toString()}`);
  }
}

function doPost(e) {
  try {
    // Para operaciones de escritura
    const data = JSON.parse(e.postData.contents);
    const action = data.action;
    
    console.log(`MCP POST Request: action=${action}`);
    
    switch(action) {
      case "write_cell":
        return handleWriteCell(data.sheet_name, data.cell, data.value);
        
      case "write_range":
        return handleWriteRange(data.sheet_name, data.range_notation, data.values);
        
      case "clear_range":
        return handleClearRange(data.sheet_name, data.range_notation);
        
      case "create_sheet":
        return handleCreateSheet(data.name);
        
      default:
        return createErrorResponse(`Acción POST no válida: ${action}`);
    }
    
  } catch (error) {
    console.error("Error en doPost:", error);
    return createErrorResponse(`Error del servidor: ${error.toString()}`);
  }
}

/**
 * Lee el valor de una celda específica
 */
function handleReadCell(sheetName, cell) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const worksheet = ss.getSheetByName(sheetName);
    
    if (!worksheet) {
      return createErrorResponse(`Hoja "${sheetName}" no encontrada`);
    }
    
    const value = worksheet.getRange(cell).getValue();
    const displayValue = worksheet.getRange(cell).getDisplayValue();
    
    return createSuccessResponse({
      action: "read_cell",
      sheet: sheetName,
      cell: cell,
      value: value,
      displayValue: displayValue,
      type: typeof value
    });
    
  } catch (error) {
    return createErrorResponse(`Error leyendo celda ${cell}: ${error.toString()}`);
  }
}

/**
 * Lee un rango de celdas
 */
function handleReadRange(sheetName, range) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const worksheet = ss.getSheetByName(sheetName);
    
    if (!worksheet) {
      return createErrorResponse(`Hoja "${sheetName}" no encontrada`);
    }
    
    const values = worksheet.getRange(range).getValues();
    const displayValues = worksheet.getRange(range).getDisplayValues();
    
    return createSuccessResponse({
      action: "read_range",
      sheet: sheetName,
      range: range,
      values: values,
      displayValues: displayValues,
      rows: values.length,
      cols: values[0] ? values[0].length : 0
    });
    
  } catch (error) {
    return createErrorResponse(`Error leyendo rango ${range}: ${error.toString()}`);
  }
}

/**
 * Lista todas las hojas del spreadsheet
 */
function handleListSheets() {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheets = ss.getSheets();
    
    const sheetList = sheets.map(sheet => ({
      name: sheet.getName(),
      id: sheet.getSheetId(),
      rows: sheet.getLastRow(),
      columns: sheet.getLastColumn(),
      hidden: sheet.isSheetHidden()
    }));
    
    return createSuccessResponse({
      action: "list_sheets",
      spreadsheetId: ss.getId(),
      spreadsheetName: ss.getName(),
      sheets: sheetList,
      totalSheets: sheetList.length
    });
    
  } catch (error) {
    return createErrorResponse(`Error listando hojas: ${error.toString()}`);
  }
}

/**
 * Obtiene información general del spreadsheet
 */
function handleGetSheetInfo() {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const user = Session.getActiveUser();
    
    return createSuccessResponse({
      action: "get_sheet_info",
      spreadsheetId: ss.getId(),
      spreadsheetName: ss.getName(),
      url: ss.getUrl(),
      owner: user.getEmail(),
      locale: ss.getSpreadsheetLocale(),
      timeZone: ss.getSpreadsheetTimeZone(),
      totalSheets: ss.getSheets().length,
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    return createErrorResponse(`Error obteniendo info: ${error.toString()}`);
  }
}

/**
 * Información básica del endpoint
 */
function handleInfo() {
  try {
    const user = Session.getActiveUser();
    
    return createSuccessResponse({
      action: "info",
      service: "Google Sheets MCP Backend",
      version: "1.0.0",
      user: user.getEmail(),
      timestamp: new Date().toISOString(),
      availableActions: [
        "read_cell",
        "read_range", 
        "list_sheets",
        "get_sheet_info",
        "write_cell",
        "write_range",
        "clear_range",
        "create_sheet"
      ]
    });
    
  } catch (error) {
    return createErrorResponse(`Error obteniendo info: ${error.toString()}`);
  }
}

/**
 * Escribe un valor en una celda específica
 */
function handleWriteCell(sheetName, cell, value) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const worksheet = ss.getSheetByName(sheetName);
    
    if (!worksheet) {
      return createErrorResponse(`Hoja "${sheetName}" no encontrada`);
    }
    
    const oldValue = worksheet.getRange(cell).getValue();
    worksheet.getRange(cell).setValue(value);
    
    // Verificar que se escribió correctamente
    const newValue = worksheet.getRange(cell).getValue();
    
    return createSuccessResponse({
      action: "write_cell",
      sheet: sheetName,
      cell: cell,
      oldValue: oldValue,
      newValue: newValue,
      success: true
    });
    
  } catch (error) {
    return createErrorResponse(`Error escribiendo en celda ${cell}: ${error.toString()}`);
  }
}

/**
 * Escribe datos en un rango de celdas
 */
function handleWriteRange(sheetName, rangeNotation, values) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const worksheet = ss.getSheetByName(sheetName);
    
    if (!worksheet) {
      return createErrorResponse(`Hoja "${sheetName}" no encontrada`);
    }
    
    if (!values || !Array.isArray(values)) {
      return createErrorResponse("Los valores deben ser un array 2D");
    }
    
    const range = worksheet.getRange(rangeNotation);
    range.setValues(values);
    
    return createSuccessResponse({
      action: "write_range",
      sheet: sheetName,
      range: rangeNotation,
      rows_written: values.length,
      columns_written: values[0] ? values[0].length : 0,
      success: true
    });
    
  } catch (error) {
    return createErrorResponse(`Error escribiendo rango ${rangeNotation}: ${error.toString()}`);
  }
}

/**
 * Limpia el contenido de un rango de celdas
 */
function handleClearRange(sheetName, rangeNotation) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const worksheet = ss.getSheetByName(sheetName);
    
    if (!worksheet) {
      return createErrorResponse(`Hoja "${sheetName}" no encontrada`);
    }
    
    const range = worksheet.getRange(rangeNotation);
    range.clearContent();
    
    return createSuccessResponse({
      action: "clear_range",
      sheet: sheetName,
      range: rangeNotation,
      success: true
    });
    
  } catch (error) {
    return createErrorResponse(`Error limpiando rango ${rangeNotation}: ${error.toString()}`);
  }
}

/**
 * Crea una nueva hoja
 */
function handleCreateSheet(name) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    
    // Verificar si ya existe
    if (ss.getSheetByName(name)) {
      return createErrorResponse(`La hoja "${name}" ya existe`);
    }
    
    const newSheet = ss.insertSheet(name);
    
    return createSuccessResponse({
      action: "create_sheet",
      name: name,
      id: newSheet.getSheetId(),
      success: true
    });
    
  } catch (error) {
    return createErrorResponse(`Error creando hoja "${name}": ${error.toString()}`);
  }
}

/**
 * Crea respuesta de éxito
 */
function createSuccessResponse(data) {
  const response = {
    success: true,
    timestamp: new Date().toISOString(),
    ...data
  };
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Crea respuesta de error
 */
function createErrorResponse(message) {
  const response = {
    success: false,
    error: message,
    timestamp: new Date().toISOString()
  };
  
  return ContentService
    .createTextOutput(JSON.stringify(response))
    .setMimeType(ContentService.MimeType.JSON);
}
