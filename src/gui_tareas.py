import tkinter as tk
from tkinter import ttk

class PanelTareas(tk.Frame):
    def __init__(self, parent, datos, callback_guardar):
        """
        Componente modular para la gestión de tareas.
        parent: El contenedor de Tkinter donde se va a dibujar.
        datos: El diccionario central de datos de la app.
        callback_guardar: La función que guarda los cambios en el JSON.
        """
        super().__init__(parent, bg="#2f3136")  # Fondo gris oscuro moderno
        self.datos = datos
        self.callback_guardar = callback_guardar
        
        # Guardamos un estado interno de colores para usar al redibujar elementos
        self.colores_actuales = {
            "bg": "#2f3136",
            "fg": "#ffffff",
            "input_bg": "#40444b",
            "text_muted": "#b9bbbe"
        }
        
        self.crear_componentes()
        self.actualizar_lista()

    def crear_componentes(self):
        # Título de la sección (Guardado en self para poder cambiarle el color)
        self.lbl_titulo = tk.Label(
            self, text="⚡ Mis Tareas", 
            font=("Segoe UI", 13, "bold"), fg=self.colores_actuales["fg"], bg=self.colores_actuales["bg"]
        )
        self.lbl_titulo.pack(pady=10)

        # Entrada de texto para añadir tareas
        self.txt_nueva_tarea = tk.Entry(
            self, font=("Segoe UI", 11), bg=self.colores_actuales["input_bg"], fg=self.colores_actuales["fg"], 
            insertbackground="white", bd=0, relief="flat"
        )
        self.txt_nueva_tarea.pack(fill="x", padx=15, pady=5, ipady=6)
        
        # Al pulsar Enter, se ejecuta automáticamente 'agregar_tarea'
        self.txt_nueva_tarea.bind("<Return>", self.agregar_tarea)

        # Contenedor interno con Scrollbar para las tareas acumuladas
        self.canvas = tk.Canvas(self, bg=self.colores_actuales["bg"], bd=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.frame_lista = tk.Frame(self.canvas, bg=self.colores_actuales["bg"])

        self.frame_lista.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.frame_lista, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        self.scrollbar.pack(side="right", fill="y", pady=10)

    def actualizar_lista(self):
        """Limpia el contenedor visual y vuelve a dibujar las tareas vigentes usando los colores actuales."""
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        bg_actual = self.colores_actuales["bg"]
        fg_muted = self.colores_actuales["text_muted"]

        for index, tarea in enumerate(self.datos.get("tareas", [])):
            item_frame = tk.Frame(self.frame_lista, bg=bg_actual)
            item_frame.pack(fill="x", pady=4)

            # Texto de la tarea
            lbl_item = tk.Label(
                item_frame, text=f"• {tarea}", 
                font=("Segoe UI", 11), fg=fg_muted, bg=bg_actual, anchor="w"
            )
            lbl_item.pack(side="left", fill="x", expand=True)

            # Botón de eliminar con una "❌"
            btn_borrar = tk.Button(
                item_frame, text="❌", bg=bg_actual, fg="#ff4757", bd=0, 
                activebackground=bg_actual, cursor="hand2",
                command=lambda i=index: self.eliminar_tarea(i)
            )
            btn_borrar.pack(side="right", padx=5)

    def aplicar_tema(self, colores):
        """MÉTODO NUEVO: Sincroniza los colores de las tareas con el tema seleccionado en main.py"""
        self.colores_actuales.update(colores)
        
        bg = self.colores_actuales.get("bg")
        fg = self.colores_actuales.get("fg")
        input_bg = self.colores_actuales.get("input_bg")
        
        # Configurar elementos estáticos
        self.configure(bg=bg)
        self.lbl_titulo.configure(bg=bg, fg=fg)
        self.txt_nueva_tarea.configure(bg=input_bg, fg=fg)
        self.canvas.configure(bg=bg)
        self.frame_lista.configure(bg=bg)
        
        # Cambiar color del cursor de la entrada de texto
        if bg == "#ffffff":
            self.txt_nueva_tarea.configure(insertbackground="black")
        else:
            self.txt_nueva_tarea.configure(insertbackground="white")
            
        # Forzar el redibujado de la lista para que las filas cambien de color
        self.actualizar_lista()

    def agregar_tarea(self, event=None):
        texto = self.txt_nueva_tarea.get().strip()
        if texto:
            if "tareas" not in self.datos:
                self.datos["tareas"] = []
            
            self.datos["tareas"].append(texto)
            self.txt_nueva_tarea.delete(0, tk.END)
            
            # Guardamos el cambio y refrescamos la vista
            self.callback_guardar()
            self.actualizar_lista()

    def eliminar_tarea(self, index):
        if 0 <= index < len(self.datos.get("tareas", [])):
            self.datos["tareas"].pop(index)
            self.callback_guardar()
            self.actualizar_lista()