import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Bloc de Notas Élite")
ventana.geometry("400x400")

# Crear el área de texto donde se escribe la nota
area_texto = tk.Text(ventana, font=("Arial", 12))
area_texto.pack(fill="both", expand=True)

# Ejecutar la aplicación
ventana.mainloop()