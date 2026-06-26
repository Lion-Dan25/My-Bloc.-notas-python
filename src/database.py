import json
import os

# Nombre del archivo donde centralizaremos la información
ARCHIVO_DB = "notas.json"

def cargar_datos():
    """Lee el archivo JSON y devuelve los datos. 
    Si el archivo no existe o está corrupto, devuelve una estructura base limpia."""
    if not os.path.exists(ARCHIVO_DB):
        # Añadimos de una vez el espacio para el futuro 'diccionario'
        return {"notas": "", "tareas": [], "diccionario": {}}
    
    try:
        with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"notas": "", "tareas": [], "diccionario": {}}

def guardar_datos(datos):
    """Recibe un diccionario con los datos de la app y los escribe en el JSON."""
    try:
        with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error crítico al guardar los datos: {e}")
        return False