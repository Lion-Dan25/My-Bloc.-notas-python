import tkinter as tk

# --- LÓGICA DEL PROGRAMA ---

# Función para guardar el texto en un archivo local .txt
def guardar_nota():
    texto = area_texto.get("1.0", tk.END) # "1.0" significa: desde la línea 1, carácter 0 hasta el final
    with open("nota_guardada.txt", "w") as archivo: # "w" es modo Escritura (Write)
        archivo.write(texto)

# Función para leer el archivo .txt y mostrarlo en pantalla
def cargar_nota():
    try:
        with open("nota_guardada.txt", "r") as archivo: # "r" es modo Lectura (Read)
            texto = archivo.read()
            area_texto.delete("1.0", tk.END) # Limpiamos el bloc para no encimar texto
            area_texto.insert("1.0", texto)  # Insertamos la nota recuperada
    except FileNotFoundError:
        # Si el archivo no existe aún (primera vez que se usa), no hacemos nada para que no explote el programa
        pass 

# --- INTERFAZ GRÁFICA (GUI) ---

ventana = tk.Tk()
ventana.title("Mi Bloc de Notas Élite")
ventana.geometry("400x450") # Le damos 50 píxeles más de alto para acomodar los botones

# Creamos un contenedor (Frame) superior exclusivo para los botones
panel_botones = tk.Frame(ventana)
panel_botones.pack(fill="x") # Se extiende horizontalmente

# Botón Guardar (lo pegamos a la izquierda 'left')
btn_guardar = tk.Button(panel_botones, text="Guardar", command=guardar_nota)
btn_guardar.pack(side="left", padx=5, pady=5)

# Botón Cargar (lo pegamos al lado del botón guardar)
btn_cargar = tk.Button(panel_botones, text="Cargar", command=cargar_nota)
btn_cargar.pack(side="left", padx=5, pady=5)

# Área de texto principal (abajo del panel de botones)
area_texto = tk.Text(ventana, font=("Arial", 12))
area_texto.pack(fill="both", expand=True)

ventana.mainloop()