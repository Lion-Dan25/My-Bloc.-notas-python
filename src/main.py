import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk  # 🚀 Inyectamos la nueva librería moderna

# Importaciones de tu arquitectura modular existente
from database import cargar_datos, guardar_datos
from gui_notas import PanelNotas
from gui_tareas import PanelTareas
from gui_diccionario import PanelDiccionario

# 🎨 CONFIGURACIÓN GLOBAL DEL TEMA (Estilo App Moderna)
ctk.set_appearance_mode("Dark")        # Fuerza el Modo Oscuro nativo
ctk.set_default_color_theme("blue")     # Tema de color para los controles

class BlocApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Bloc Cool 🚀")
        self.root.geometry("850x600")
        
        # Cargar base de datos compartida
        self.datos = cargar_datos()

        # Asegurar estructuras base correctas
        if "notas" not in self.datos or not isinstance(self.datos["notas"], list):
            self.datos["notas"] = []
        if "tareas" not in self.datos:
            self.datos["tareas"] = []
        if "diccionario" not in self.datos:
            self.datos["diccionario"] = {}

        # 📱 CONTENEDOR CENTRAL DE PANTALLAS (Ocupará todo el espacio superior)
        self.contenedor_pantallas = ctk.CTkFrame(self.root, fg_color="#36393f")
        # Al usar pack, le decimos que se expanda pero dejamos espacio abajo side="top"
        self.contenedor_pantallas.pack(side="top", fill="both", expand=True)

        # 🗺️ BARRA DE NAVEGACIÓN INFERIOR (Contenedor fijo abajo)
        self.barra_navegacion = ctk.CTkFrame(self.root, fg_color="#202225", height=60, corner_radius=0)
        self.barra_navegacion.pack(side="bottom", fill="x")
        self.barra_navegacion.pack_propagate(False) # Evita que colapse al meter botones

        # Inicializar tus paneles modulares existentes dentro del contenedor superior
        self.pantallas = {
            "notas": PanelNotas(self.contenedor_pantallas, self.datos, self.guardar_cambios),
            "tareas": PanelTareas(self.contenedor_pantallas, self.datos, self.guardar_cambios),
            "diccionario": PanelDiccionario(self.contenedor_pantallas, self.datos, self.guardar_cambios)
        }

        # Construir botones de navegación en la barra inferior
        self.crear_botones_navegacion()

        # Mostrar la pantalla de notas por defecto al iniciar
        self.mostrar_pantalla("notas")

    def crear_botones_navegacion(self):
        """Crea los botones de cambio de pantalla de forma limpia y alineada"""
        # Contenedor interno para centrar los botones principales
        frame_central_botones = ctk.CTkFrame(self.barra_navegacion, fg_color="transparent")
        frame_central_botones.pack(expand=True)

        # Botón Notas
        btn_notas = ctk.CTkButton(frame_central_botones, text="📝 Notas", width=120, height=40,
                                  command=lambda: self.mostrar_pantalla("notas"))
        btn_notas.pack(side="left", padx=10)

        # Botón Tareas
        btn_tareas = ctk.CTkButton(frame_central_botones, text="✅ Tareas", width=120, height=40,
                                   command=lambda: self.mostrar_pantalla("tareas"))
        btn_tareas.pack(side="left", padx=10)

        # Botón Diccionario
        btn_dicc = ctk.CTkButton(frame_central_botones, text="📖 Diccionario", width=120, height=40,
                                 command=lambda: self.mostrar_pantalla("diccionario"))
        btn_dicc.pack(side="left", padx=10)

        # ⚙️ BOTÓN DE ENGRANAJE (Configuración / Temas) - Esquina inferior izquierda
        btn_config = ctk.CTkButton(self.barra_navegacion, text="⚙️", width=40, height=40,
                                   fg_color="transparent", hover_color="#2f3136",
                                   command=self.abrir_configuracion)
        btn_config.place(x=15, y=10)

    def mostrar_pantalla(self, nombre_pantalla):
        """Oculta todos los paneles y despliega únicamente el seleccionado"""
        for pantalla in self.pantallas.values():
            pantalla.pack_forget()
        self.pantallas[nombre_pantalla].pack(fill="both", expand=True)

    def abrir_configuracion(self):
        """Ventana provisional de configuración de temas"""
        messagebox.showinfo("Configuración", "¡Aquí controlaremos las paletas de colores pronto!")

    def guardar_cambios(self):
        """Callback encargado de escribir de forma segura en el JSON"""
        guardar_datos(self.datos)


# 🏁 PUNTO DE ENTRADA DEL PROGRAMA
def main():
    root = ctk.CTk()  # 🌟 ¡Ventana nativa moderna!
    app = BlocApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()