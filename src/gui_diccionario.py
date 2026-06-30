import tkinter as tk
from tkinter import ttk

class PanelDiccionario(tk.Frame):
    def __init__(self, parent, datos, callback_guardar):
        """
        Componente modular para el Diccionario de Palabras.
        parent: Contenedor principal (contenedor_pantallas en main.py).
        datos: Diccionario centralizado compartido.
        callback_guardar: Función para escribir los cambios en el JSON.
        """
        super().__init__(parent, bg="#36393f")  # Fondo base por defecto (Oscuro Discord)
        self.datos = datos
        self.callback_guardar = callback_guardar
        
        # Asegurar que exista la estructura del diccionario dentro de nuestros datos
        if "diccionario" not in self.datos:
            self.datos["diccionario"] = []
            
        self.crear_componentes()

    def crear_componentes(self):
        """Construye la interfaz visual base para el laboratorio del diccionario"""
        # Etiqueta de título provisional
        self.label_titulo = tk.Label(
            self, 
            text="📖 Módulo Diccionario (Próxima Fase)", 
            fg="#ffffff", 
            bg="#36393f",
            font=("Segoe UI", 16, "bold")
        )
        self.label_titulo.pack(pady=20)

        # Mensaje de estado en el laboratorio
        self.label_info = tk.Label(
            self, 
            text="¡Cascarón conectado con éxito!\nEl import en main.py ya no causará fallos.\nPronto añadiremos la lógica de términos aquí.", 
            fg="#b9bbbe", 
            bg="#36393f",
            font=("Consolas", 11)
        )
        self.label_info.pack(pady=10)

    def aplicar_tema(self, colores):
        """
        Recibe el diccionario de colores del tema global 
        y rediseña los componentes al vuelo.
        """
        self.configure(bg=colores["bg"])
        self.label_titulo.configure(bg=colores["bg"], fg=colores["fg"])
        self.label_info.configure(bg=colores["bg"])