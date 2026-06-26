import tkinter as tk
import database
from gui_notas import PanelNotas
from gui_tareas import PanelTareas

def main():
    # 1. Inicializar y cargar los datos centralizados desde el JSON
    datos = database.cargar_datos()

    # 2. Configurar la ventana principal de la aplicación (Root)
    root = tk.Tk()
    root.title("Proyecto Bloc Cool ⚡ Architecture Edition")
    root.geometry("950x600")
    root.configure(bg="#202225")  # Fondo ultra oscuro para los bordes de la app

    # Función puente (Callback)
    # Permite que los paneles visuales ordenen guardar en el JSON sin conocer la lógica interna de la BD
    def guardar_cambios():
        database.guardar_datos(datos)

    # 3. Crear el contenedor dividido responsivo (PanedWindow)
    # Esto te permite arrastrar la barra del medio con el ratón para expandir o encoger los paneles
    panel_dividido = tk.PanedWindow(root, orient="horizontal", bd=0, handleSize=8, bg="#202225")
    panel_dividido.pack(fill="both", expand=True)

    # 4. Instanciar nuestros componentes modulares pasándoles el diccionario compartido
    panel_izquierdo_notas = PanelNotas(panel_dividido, datos, guardar_cambios)
    panel_derecho_tareas = PanelTareas(panel_dividido, datos, guardar_cambios)

    # 5. Acoplar los componentes al panel dividido estableciendo límites de tamaño
    panel_dividido.add(panel_izquierdo_notas, stretch="always", minsize=500)
    panel_dividido.add(panel_derecho_tareas, stretch="never", minsize=350)

    # 6. Encender los motores del programa
    root.mainloop()

if __name__ == "__main__":
    main()