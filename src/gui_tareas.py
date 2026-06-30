import tkinter as tk
from tkinter import simpledialog

class PanelTareas(tk.Frame):
    def __init__(self, parent, datos, callback_guardar):
        super().__init__(parent, bg="#36393f")
        self.datos = datos
        self.callback_guardar = callback_guardar

        # Título de sección
        self.lbl_titulo = tk.Label(self, text="LISTA DE TAREAS", bg="#36393f", fg="#ffffff", font=("Arial", 14, "bold"))
        self.lbl_titulo.pack(pady=15)

        # Contenedor para la lista de checkboxes
        self.canvas = tk.Canvas(self, bg="#36393f", bd=0, highlightthickness=0)
        self.scroll_frame = tk.Frame(self.canvas, bg="#36393f")
        
        self.canvas.pack(fill="both", expand=True, padx=20)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.crear_componentes()
        self.actualizar_lista()

    def crear_componentes(self):
        # --- BOTÓN FLOTANTE (FAB) '+' PARA TAREAS ---
        self.btn_fab_tarea = tk.Button(
            self, text="+", bg="#ff007f", fg="#ffffff", font=("Arial", 18, "bold"),
            bd=0, width=3, height=1, cursor="hand2", activebackground="#cc0066",
            command=self.pedir_nueva_tarea
        )
        self.btn_fab_tarea.place(relx=0.94, rely=0.88, anchor="se")

    def pedir_nueva_tarea(self):
        # Ventana emergente nativa y rápida para capturar la tarea
        tarea_texto = simpledialog.askstring("Nueva Tarea", "Escribe tu tarea pendiente:", parent=self)
        if tarea_texto and tarea_texto.strip():
            if "tareas" not in self.datos:
                self.datos["tareas"] = []
            
            # Guardamos como diccionario interno para soportar estados
            self.datos["tareas"].append({"texto": tarea_texto.strip(), "completada": False})
            self.callback_guardar()
            self.actualizar_lista()

    def actualizar_lista(self):
        # Limpiar elementos visuales previos
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for idx, tarea in enumerate(self.datos.get("tareas", [])):
            
            # 🛡️ CAPA DE MIGRACIÓN AUTOMÁTICA EN CALIENTE
            # Si la tarea guardada es un texto plano (versión antigua), la transformamos a diccionario al vuelo
            if isinstance(tarea, str):
                tarea = {"texto": tarea, "completada": False}
                self.datos["tareas"][idx] = tarea  # Actualizamos la memoria
                self.callback_guardar()            # Sincronizamos el archivo JSON

            frame_item = tk.Frame(self.scroll_frame, bg=self.cget("bg"), pady=5)
            frame_item.pack(fill="x", expand=True)

            # Checkbox interactivo
            var_check = tk.BooleanVar(value=tarea.get("completada", False))
            cb = tk.Checkbutton(
                frame_item, text=tarea.get("texto", ""), variable=var_check,
                bg=self.cget("bg"), fg="#ffffff", activebackground=self.cget("bg"),
                activeforeground="#ffffff", selectcolor="#202225", font=("Arial", 11),
                command=lambda i=idx, v=var_check: self.conmutar_tarea(i, v)
            )
            cb.pack(side="left", anchor="w")

            # Botón eliminar individual discreto
            btn_del = tk.Button(
                frame_item, text="❌", bg=self.cget("bg"), fg="#ff4444", bd=0,
                cursor="hand2", font=("Arial", 10), command=lambda i=idx: self.eliminar_tarea(i)
            )
            btn_del.pack(side="right", padx=10)

    def conmutar_tarea(self, index, var):
        self.datos["tareas"][index]["completada"] = var.get()
        self.callback_guardar()

    def eliminar_tarea(self, index):
        self.datos["tareas"].pop(index)
        self.callback_guardar()
        self.actualizar_lista()

    def aplicar_tema(self, colores):
        self.configure(bg=colores["bg"])
        self.lbl_titulo.configure(bg=colores["bg"], fg=colores["fg"])
        self.canvas.configure(bg=colores["bg"])
        self.scroll_frame.configure(bg=colores["bg"])
        self.btn_fab_tarea.configure(bg=colores.get("accent", "#ff007f"))
        self.actualizar_lista()