import tkinter as tk

# --- LÓGICA DEL PROGRAMA ---

def guardar_nota():
    texto = area_texto.get("1.0", tk.END)
    with open("nota_guardada.txt", "w") as archivo:
        archivo.write(texto)

def cargar_nota():
    try:
        with open("nota_guardada.txt", "r") as archivo:
            texto = archivo.read()
            area_texto.delete("1.0", tk.END)
            area_texto.insert("1.0", texto)
    except FileNotFoundError:
        pass 

# NUEVAS FUNCIONES: Cambiar color de fondo del área de texto
def fondo_amarillo():
    area_texto.config(bg="#FFF9A6") # Amarillo pastel

def fondo_verde():
    area_texto.config(bg="#C2FFD9") # Verde pastel

def fondo_blanco():
    area_texto.config(bg="white") # Restaurar a blanco de fábrica


# --- INTERFAZ GRÁFICA (GUI) ---

ventana = tk.Tk()
ventana.title("Mi Bloc de Notas Élite")
ventana.geometry("450x450") # Lo hacemos un poquito más ancho para que quepan todos los botones

panel_botones = tk.Frame(ventana)
panel_botones.pack(fill="x")

# Botones de Funcionalidad (Pegados a la izquierda)
btn_guardar = tk.Button(panel_botones, text="Guardar", command=guardar_nota)
btn_guardar.pack(side="left", padx=5, pady=5)

btn_cargar = tk.Button(panel_botones, text="Cargar", command=cargar_nota)
btn_cargar.pack(side="left", padx=5, pady=5)


# NUEVOS BOTONES: Estilos Visuales (Pegados a la derecha 'right')
btn_blanco = tk.Button(panel_botones, text="Blanco", command=fondo_blanco)
btn_blanco.pack(side="right", padx=5, pady=5)

btn_verde = tk.Button(panel_botones, text="Verde", command=fondo_verde)
btn_verde.pack(side="right", padx=5, pady=5)

btn_amarillo = tk.Button(panel_botones, text="Amarillo", command=fondo_amarillo)
btn_amarillo.pack(side="right", padx=5, pady=5)


# Área de texto principal
area_texto = tk.Text(ventana, font=("Arial", 12))
area_texto.pack(fill="both", expand=True)

ventana.mainloop()