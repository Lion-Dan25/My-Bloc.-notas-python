import tkinter as tk
from tkinter import Toplevel, ttk
import database
from gui_notas import PanelNotas
from gui_tareas import PanelTareas

# Diccionario central de temas profesionales
TEMAS = {
    "Oscuro Nórdico": {"bg": "#2F343F", "fg": "#FFFFFF", "accent": "#4B5162", "btn_nav": "#5294E2", "text_bg": "#383C4A"},
    "Cyberpunk": {"bg": "#001219", "fg": "#00F5D4", "accent": "#7B2CBF", "btn_nav": "#9B5DE5", "text_bg": "#240046"},
    "Pastel Relajante": {"bg": "#F7EDE2", "fg": "#F28482", "accent": "#F5CAC3", "btn_nav": "#84A59D", "text_bg": "#FFFFFF"},
    "Monocromo": {"bg": "#FFFFFF", "fg": "#000000", "accent": "#E0E0E0", "btn_nav": "#333333", "text_bg": "#F5F5F5"}
}

class AppPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloc Cool 🚀")
        self.root.geometry("450x650")
        
        # Cargar datos e inicializar tema por defecto
        self.datos = database.cargar_datos()
        self.tema_actual = "Oscuro Nórdico"
        
        # Contenedor principal superior (Barra de herramientas)
        self.header_frame = tk.Frame(root, bd=0, height=50)
        self.header_frame.pack(fill="x", side="top")
        
        # Botón de Engranaje (Configuración) en la esquina superior derecha
        self.btn_config = tk.Button(
            self.header_frame, text="⚙️", font=("Segoe UI", 16),
            bd=0, cursor="hand2", command=self.abrir_configuracion
        )
        self.btn_config.pack(side="right", padx=15, pady=5)
        
        # Contenedor central donde se alternarán los paneles
        self.contenedor_central = tk.Frame(root, bd=0)
        self.contenedor_central.pack(fill="both", expand=True)
        
        # Inicializar los paneles hijos dentro del contenedor central
        self.panel_notas = PanelNotas(self.contenedor_central, self.datos, self.guardar_cambios)
        self.panel_tareas = PanelTareas(self.contenedor_central, self.datos, self.guardar_cambios)
        
        # Barra de navegación inferior
        self.nav_bar = tk.Frame(root, bd=0, height=60)
        self.nav_bar.pack(fill="x", side="bottom")
        
        # Botón de Notas (Icono de Nota)
        self.btn_nav_notas = tk.Button(
            self.nav_bar, text="📝 Notas", font=("Segoe UI", 12, "bold"),
            bd=0, cursor="hand2", command=lambda: self.mostrar_pantalla("notas")
        )
        self.btn_nav_notas.pack(side="left", fill="both", expand=True)
        
        # Botón de Tareas (Icono de Lápiz/Check)
        self.btn_nav_tareas = tk.Button(
            self.nav_bar, text="✏️ Tareas", font=("Segoe UI", 12, "bold"),
            bd=0, cursor="hand2", command=lambda: self.mostrar_pantalla("tareas")
        )
        self.btn_nav_tareas.pack(side="right", fill="both", expand=True)
        
        # Mostrar la pantalla de notas al arrancar y aplicar colores iniciales
        self.mostrar_pantalla("notas")
        self.actualizar_diseno_global()

    def guardar_cambios(self):
        database.guardar_datos(self.datos)

    def mostrar_pantalla(self, pantalla):
        """Oculta un panel y muestra el otro simulando navegación por pestañas"""
        if pantalla == "notas":
            self.panel_tareas.pack_forget()
            self.panel_notas.pack(fill="both", expand=True)
        elif pantalla == "tareas":
            self.panel_notas.pack_forget()
            self.panel_tareas.pack(fill="both", expand=True)

    def abrir_configuracion(self):
        """Abre una ventana flotante y estilizada para elegir el tema"""
        ventana_config = Toplevel(self.root)
        ventana_config.title("Temas")
        ventana_config.geometry("280x250")
        ventana_config.grab_set() # Bloquea la ventana principal hasta cerrar esta
        
        colores = TEMAS[self.tema_actual]
        ventana_config.configure(bg=colores["bg"])
        
        lbl = tk.Label(ventana_config, text="Selecciona un Tema", font=("Segoe UI", 12, "bold"), bg=colores["bg"], fg=colores["fg"])
        lbl.pack(pady=15)
        
        for nombre_tema in TEMAS.keys():
            btn = tk.Button(
                ventana_config, text=nombre_tema, font=("Segoe UI", 10),
                bg=colores["accent"], fg=colores["fg"], bd=0, pady=5, width=20, cursor="hand2",
                command=lambda t=nombre_tema: [self.cambiar_tema_global(t), ventana_config.destroy()]
            )
            btn.pack(pady=5)

    def cambiar_tema_global(self, nombre_tema):
        self.tema_actual = nombre_tema
        self.actualizar_diseno_global()

    def actualizar_diseno_global(self):
        """Aplica el esquema de colores seleccionado a todos los componentes raíz y secundarios"""
        colores = TEMAS[self.tema_actual]
        
        # Colores de la app principal
        self.root.configure(bg=colores["bg"])
        self.header_frame.configure(bg=colores["bg"])
        self.contenedor_central.configure(bg=colores["bg"])
        self.nav_bar.configure(bg=colores["bg"])
        
        # Botón engranaje
        self.btn_config.configure(bg=colores["bg"], fg=colores["fg"], activebackground=colores["accent"])
        
        # Botones de navegación inferior
        self.btn_nav_notas.configure(bg=colores["accent"], fg=colores["fg"], activebackground=colores["btn_nav"])
        self.btn_nav_tareas.configure(bg=colores["accent"], fg=colores["fg"], activebackground=colores["btn_nav"])
        
        # Propagar el tema a los paneles internos (asumiendo que tienen el método aplicar_tema)
        if hasattr(self.panel_notas, "aplicar_tema"):
            self.panel_notas.aplicar_tema(colores)
        if hasattr(self.panel_tareas, "aplicar_tema"):
            self.panel_tareas.aplicar_tema(colores)

def main():
    root = tk.Tk()
    app = AppPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()