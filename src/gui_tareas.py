import tkinter as tk
import customtkinter as ctk

class PanelTareas(ctk.CTkFrame):
    def __init__(self, parent, datos, callback_guardar):
        # Inicializamos como un contenedor moderno de CustomTkinter
        super().__init__(parent, fg_color="#36393f")
        self.datos = datos
        self.callback_guardar = callback_guardar

        # Diccionario interno de control de colores para renderizado dinámico y reactivo
        self.colores_actuales = {"bg": "#36393f", "fg": "#ffffff"}

        # Título de sección estilizado
        self.lbl_titulo = ctk.CTkLabel(self, text="LISTA DE TAREAS", font=("Arial", 16, "bold"), text_color="#ffffff")
        self.lbl_titulo.pack(pady=15)

        # Contenedor con scroll integrado de manera nativa (¡Mucho más limpio!)
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#36393f", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.crear_componentes()
        self.actualizar_lista()

    def crear_componentes(self):
        # --- BOTÓN FLOTANTE (FAB) '+' PARA TAREAS ---
        # Para lograr un círculo perfecto en CTkButton, el corner_radius debe ser exactamente la mitad del width/height
        self.btn_fab_tarea = ctk.CTkButton(
            self, text="+", fg_color="#ff007f", text_color="#ffffff", font=("Arial", 24, "bold"),
            width=56, height=56, corner_radius=28, hover_color="#cc0066",
            command=self.pedir_nueva_tarea
        )
        self.btn_fab_tarea.place(relx=0.94, rely=0.88, anchor="se")

    def pedir_nueva_tarea(self):
        # Ventana emergente moderna y estilizada nativa de CustomTkinter
        dialog = ctk.CTkInputDialog(text="Escribe tu tarea pendiente:", title="Nueva Tarea")
        tarea_texto = dialog.get_input()
        
        if tarea_texto and tarea_texto.strip():
            if "tareas" not in self.datos:
                self.datos["tareas"] = []
            
            # Guardamos respetando nuestra estructura centralizada (Única fuente de verdad)
            self.datos["tareas"].append({"texto": tarea_texto.strip(), "completada": False})
            self.callback_guardar()
            self.actualizar_lista()

    def actualizar_lista(self):
        # Limpiar elementos visuales previos del scroll
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for idx, tarea in enumerate(self.datos.get("tareas", [])):
            
            # 🛡️ CAPA DE MIGRACIÓN AUTOMÁTICA EN CALIENTE
            # Si el JSON contiene texto plano antiguo, lo transformamos a diccionario al vuelo sin romper nada
            if isinstance(tarea, str):
                tarea = {"texto": tarea, "completada": False}
                self.datos["tareas"][idx] = tarea  
                self.callback_guardar()            

            # Contenedor individual para cada fila de tarea
            frame_item = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            frame_item.pack(fill="x", expand=True, pady=4)

            # Checkbox interactivo moderno
            var_check = tk.BooleanVar(value=tarea.get("completada", False))
            cb = ctk.CTkCheckBox(
                frame_item, text=tarea.get("texto", ""), variable=var_check,
                text_color=self.colores_actuales.get("fg", "#ffffff"),
                font=("Arial", 12),
                command=lambda i=idx, v=var_check: self.conmutar_tarea(i, v)
            )
            cb.pack(side="left", anchor="w", padx=5)

            # Botón eliminar individual discreto moderno
            btn_del = ctk.CTkButton(
                frame_item, text="❌", fg_color="transparent", text_color="#ff4444",
                width=30, height=30, font=("Arial", 12), command=lambda i=idx: self.eliminar_tarea(i)
            )
            # Adaptamos sutilmente el color del hover según el fondo para que luzca limpio
            btn_del.configure(hover_color=("#e0e0e0" if self.colores_actuales.get("bg") == "#ffffff" else "#2f3136"))
            btn_del.pack(side="right", padx=10)

    def conmutar_tarea(self, index, var):
        self.datos["tareas"][index]["completada"] = var.get()
        self.callback_guardar()

    def eliminar_tarea(self, index):
        self.datos["tareas"].pop(index)
        self.callback_guardar()
        self.actualizar_lista()

    def aplicar_tema(self, colores):
        # Almacenamos los nuevos colores para que la lista dinámica los use al redibujarse
        self.colores_actuales = colores
        self.configure(fg_color=colores["bg"])
        self.lbl_titulo.configure(fg_color=colores["bg"], text_color=colores["fg"])
        self.scroll_frame.configure(fg_color=colores["bg"])
        self.btn_fab_tarea.configure(fg_color=colores.get("accent", "#ff007f"))
        self.actualizar_lista()