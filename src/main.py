import tkinter as tk
from tkinter import messagebox
from database import cargar_datos, guardar_datos
from gui_notas import PanelNotas
from gui_tareas import PanelTareas
# CONFIGURACIÓN INTEGRADA: Importación del nuevo módulo de diccionario para la arquitectura
from gui_diccionario import PanelDiccionario 

class BlocApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Bloc Cool 🚀")
        self.root.geometry("850x600")
        self.root.configure(bg="#202225")

        # Cargar base de datos compartida
        self.datos = cargar_datos()

        # Asegurar estructuras base correctas
        if "notas" not in self.datos or not isinstance(self.datos["notas"], list):
            self.datos["notas"] = []
        if "tareas" not in self.datos:
            self.datos["tareas"] = []
        # CONFIGURACIÓN INTEGRADA: Estructura base para los datos del diccionario
        if "diccionario" not in self.datos:
            self.datos["diccionario"] = []

        # Contenedor central de pantallas
        self.contenedor_pantallas = tk.Frame(self.root, bg="#36393f")
        self.contenedor_pantallas.pack(fill="both", expand=True)

        # Inicializar los paneles modulares
        self.panel_notas = PanelNotas(self.contenedor_pantallas, self.datos, self.guardar_cambios)
        self.panel_tareas = PanelTareas(self.contenedor_pantallas, self.datos, self.guardar_cambios)
        # CONFIGURACIÓN INTEGRADA: Panel modular del Diccionario
        self.panel_diccionario = PanelDiccionario(self.contenedor_pantallas, self.datos, self.guardar_cambios)

        # Iniciar mostrando el panel de notas por defecto
        self.pantalla_actual = self.panel_notas
        self.pantalla_actual.pack(fill="both", expand=True)

        # Construir los elementos visuales de navegación
        self.crear_barra_navegacion()

        # CONFIGURACIÓN INTEGRADA: Inicializar el tema de forma defensiva y automática al arrancar
        tema_inicio = {"bg": "#36393f", "panel": "#2f3136", "fg": "#ffffff", "accent": "#7289da"}
        self.aplicar_tema_global(tema_inicio)

    def crear_barra_navegacion(self):
        # CONFIGURACIÓN CORREGIDA: Se guarda en 'self' para que sea accesible desde el gestor de temas
        self.barra_nav = tk.Frame(self.root, bg="#2f3136", height=65)
        self.barra_nav.pack(side="bottom", fill="x")
        self.barra_nav.pack_propagate(False)

        # Estilo común para botones limpios (solo icono)
        estilo_btn = {
            "bg": "#2f3136", "fg": "#b9bbbe", "activebackground": "#36393f",
            "activeforeground": "#ffffff", "bd": 0, "font": ("Segoe UI", 18),
            "cursor": "hand2", "padx": 20
        }

        # Botón Notas (Icono Grande)
        self.btn_notas = tk.Button(self.barra_nav, text="📝", command=lambda: self.cambiar_pantalla(self.panel_notas), **estilo_btn)
        self.btn_notas.pack(side="left", expand=True, fill="both")

        # Botón Tareas (Icono Grande)
        self.btn_tareas = tk.Button(self.barra_nav, text="🖊️", command=lambda: self.cambiar_pantalla(self.panel_tareas), **estilo_btn)
        self.btn_tareas.pack(side="left", expand=True, fill="both")

        # CONFIGURACIÓN INTEGRADA: Botón del módulo de Diccionario (Libro) para la barra inferior
        self.btn_diccionario = tk.Button(self.barra_nav, text="📖", command=lambda: self.cambiar_pantalla(self.panel_diccionario), **estilo_btn)
        self.btn_diccionario.pack(side="left", expand=True, fill="both")

        # Botón de Configuración Rápida de Tema (Engranaje)
        self.btn_config = tk.Button(self.barra_nav, text="⚙️", command=self.abrir_menu_temas, **estilo_btn)
        self.btn_config.pack(side="left", expand=True, fill="both")

    def cambiar_pantalla(self, nueva_pantalla):
        self.pantalla_actual.pack_forget()
        self.pantalla_actual = nueva_pantalla
        self.pantalla_actual.pack(fill="both", expand=True)

    def abrir_menu_temas(self):
        # Una pequeña ventana emergente minimalista
        ventana_temas = tk.Toplevel(self.root)
        ventana_temas.title("Temas")
        ventana_temas.geometry("250x200")
        ventana_temas.configure(bg="#2f3136")
        ventana_temas.resizable(False, False)

        tk.Label(ventana_temas, text="Selecciona un Estilo", bg="#2f3136", fg="#ffffff", font=("Arial", 12, "bold")).pack(pady=10)

        # Diccionario directo de temas centrales
        temas = {
            "Oscuro Cyberpunk": {"bg": "#121212", "panel": "#1e1e1e", "fg": "#00ff66", "accent": "#ff007f"},
            "Modo Discord": {"bg": "#36393f", "panel": "#2f3136", "fg": "#ffffff", "accent": "#7289da"},
            "Sepia Vintage": {"bg": "#f4ecd8", "panel": "#e4dcbc", "fg": "#5b4636", "accent": "#8c6d53"}
        }

        for nombre, colores in temas.items():
            btn = tk.Button(
                ventana_temas, text=nombre, bg=colores["panel"], fg=colores["fg"],
                font=("Arial", 10), bd=0, pady=5, cursor="hand2",
                command=lambda c=colores: self.aplicar_tema_global(c)
            )
            btn.pack(fill="x", padx=20, pady=5)

    def aplicar_tema_global(self, colores):
        # CONFIGURACIÓN CORREGIDA: Cambia los contenedores del archivo principal armónicamente
        self.root.configure(bg=colores["bg"])
        self.contenedor_pantallas.configure(bg=colores["bg"])
        self.barra_nav.configure(bg=colores["panel"])
        
        # CONFIGURACIÓN CORREGIDA: Bucle dinámico para rediseñar todos los botones inferiores a la vez
        botones_navegacion = [self.btn_notas, self.btn_tareas, self.btn_diccionario, self.btn_config]
        for btn in botones_navegacion:
            btn.configure(
                bg=colores["panel"],
                fg=colores["fg"],
                activebackground=colores["bg"],
                activeforeground=colores["fg"]
            )
        
        # Propagar la paleta de colores hacia las clases y paneles hijos
        self.panel_notas.aplicar_tema(colores)
        self.panel_tareas.aplicar_tema(colores)
        self.panel_diccionario.aplicar_tema(colores)

    def guardar_cambios(self):
        guardar_datos(self.datos)

def main():
    root = tk.Tk()
    app = BlocApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()