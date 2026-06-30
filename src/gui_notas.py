import tkinter as tk
from tkinter import ttk

class PanelNotas(tk.Frame):
    def __init__(self, parent, datos, callback_guardar):
        """
        Componente modular para el editor de notas y selección de temas.
        parent: Contenedor principal de Tkinter.
        datos: Diccionario de datos centralizado (compartido con la BD).
        callback_guardar: Función encargada de escribir en el JSON.
        """
        super().__init__(parent, bg="#36393f")  # Color de fondo base (estilo Discord)
        self.datos = datos
        self.callback_guardar = callback_guardar
        
        # Diccionario de configuraciones visuales profesionales
        self.temas = {
            "Oscuro Discord": {"bg": "#36393f", "fg": "#ffffff", "font": ("Consolas", 12)},
            "Cyberpunk Neon": {"bg": "#000000", "fg": "#00ff66", "font": ("Courier New", 12, "bold")},
            "Classic Light": {"bg": "#ffffff", "fg": "#000000", "font": ("Arial", 11)},
            "Sepia Vintage": {"bg": "#f4ecd8", "fg": "#5b4636", "font": ("Georgia", 12)}
        }
        
        self.crear_componentes()
        self.cargar_nota_inicial()

    def crear_componentes(self):
        # Barra superior interna exclusiva para herramientas del editor (Guardada en self)
        self.frame_herramientas = tk.Frame(self, bg="#2f3136", height=40)
        self.frame_herramientas.pack(fill="x", side="top")
        self.frame_herramientas.pack_propagate(False)

        self.lbl_tema = tk.Label(
            self.frame_herramientas, text="🎨 Tema Visual:", 
            bg="#2f3136", fg="#b9bbbe", font=("Segoe UI", 10)
        )
        self.lbl_tema.pack(side="left", padx=10, pady=5)

        # Menú desplegable de temas
        self.combo_temas = ttk.Combobox(
            self.frame_herramientas, values=list(self.temas.keys()), 
            state="readonly", width=15
        )
        self.combo_temas.set("Oscuro Discord")
        self.combo_temas.pack(side="left", padx=5, pady=5)
        self.combo_temas.bind("<<ComboboxSelected>>", self.cambiar_tema)

        # El lienzo de texto (Editor)
        self.txt_editor = tk.Text(
            self, wrap="word", undo=True, bd=0, padx=15, pady=15,
            bg=self.temas["Oscuro Discord"]["bg"],
            fg=self.temas["Oscuro Discord"]["fg"],
            font=self.temas["Oscuro Discord"]["font"],
            insertbackground="white"  # Color de la barra parpadeante
        )
        self.txt_editor.pack(fill="both", expand=True)

        # Captura en tiempo real cada vez que el usuario suelta una tecla
        self.txt_editor.bind("<KeyRelease>", self.actualizar_y_guardar)

    def cargar_nota_inicial(self):
        """Rellena el editor con el último texto guardado en el JSON."""
        texto_previo = self.datos.get("notas", "")
        self.txt_editor.insert("1.0", texto_previo)

    def cambiar_tema(self, event=None):
        """Modifica dinámicamente el estilo visual de la caja de texto (Local)."""
        tema_elegido = self.combo_temas.get()
        estilo = self.temas.get(tema_elegido, self.temas["Oscuro Discord"])
        
        self.txt_editor.configure(
            bg=estilo["bg"],
            fg=estilo["fg"],
            font=estilo["font"]
        )
        
        # Ajustamos el cursor para que no se pierda en fondos claros
        if estilo["bg"] == "#ffffff":
            self.txt_editor.configure(insertbackground="black")
        else:
            self.txt_editor.configure(insertbackground="white")

    def aplicar_tema(self, colores):
        """MÉTODO NUEVO: Escucha los cambios del engranaje global en main.py"""
        bg = colores.get("bg", "#36393f")
        fg = colores.get("fg", "#ffffff")
        input_bg = colores.get("input_bg", "#2f3136")
        text_muted = colores.get("text_muted", "#b9bbbe")

        # Actualizamos todos los componentes del panel
        self.configure(bg=bg)
        self.frame_herramientas.configure(bg=input_bg)
        self.lbl_tema.configure(bg=input_bg, fg=text_muted)
        self.txt_editor.configure(bg=bg, fg=fg)
        
        # Cambiar el color del cursor adaptativamente
        if bg == "#ffffff":
            self.txt_editor.configure(insertbackground="black")
        else:
            self.txt_editor.configure(insertbackground="white")

    def actualizar_y_guardar(self, event=None):
        """Extrae el contenido plano del editor y actualiza la persistencia."""
        self.datos["notas"] = self.txt_editor.get("1.0", "end-1c")
        self.callback_guardar()