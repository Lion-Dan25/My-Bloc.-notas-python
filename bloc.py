import tkinter as tk
from tkinter import messagebox, ttk

class BlocCool:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Bloc Cool")
        self.root.geometry("600x520")
        
        # Paleta de colores profesionales para cada tema
        self.themes = {
            "Original (Blanco)": {"bg": "#ffffff", "fg": "#2c3e50", "accent": "#ecf0f1", "nav_bg": "#f8f9fa"},
            "Pastel Relajante": {"bg": "#fff5f5", "fg": "#4a4a4a", "accent": "#ffe3e3", "nav_bg": "#ffd1d1"},
            "Modo Oscuro Cyberpunk": {"bg": "#0f0c1b", "fg": "#00ffcc", "accent": "#1a1530", "nav_bg": "#1f1a3a"},
            "Ejecutivo (Azul/Gris)": {"bg": "#2b3e50", "fg": "#ffffff", "accent": "#1e2b37", "nav_bg": "#34495e"}
        }
        self.current_theme = "Original (Blanco)"

        # Contenedor Principal (Donde se intercambian las pantallas)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- EL ENGRANAJE DE ÉLITE (Esquina Superior Derecha) ---
        # bd=0 y highlightthickness=0 eliminan por completo el borde para fusionarse con el fondo
        self.config_btn = tk.Button(
            self.root, text="⚙", font=("Arial", 18),
            bd=0, highlightthickness=0, cursor="hand2",
            command=self.toggle_menu_temas
        )
        # Lo posicionamos de forma absoluta arriba a la derecha
        self.config_btn.place(relx=0.97, rely=0.01, anchor="ne")

        # Menú desplegable oculto para cambiar de tema
        self.menu_temas = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.crear_menu_temas()

        # Inicialización de las dos vistas independientes
        self.frame_notas = tk.Frame(self.main_frame)
        self.frame_tareas = tk.Frame(self.main_frame)

        self.crear_vista_notas()
        self.crear_vista_tareas()

        # Barra de navegación inferior
        self.nav_bar = tk.Frame(self.root, height=65)
        self.nav_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.crear_nav_bar()

        # Lanzar la aplicación mostrando las Notas y aplicando el tema base
        self.mostrar_vista("notas")
        self.aplicar_tema()

    def crear_vista_notas(self):
        # Un editor de notas limpio que abarca toda la pantalla
        self.text_area = tk.Text(self.frame_notas, font=("Arial", 12), bd=0, padx=15, pady=40)
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def crear_vista_tareas(self):
        # Título del gestor de tareas
        self.lbl_tareas = tk.Label(self.frame_tareas, text="⚡ Lista de Tareas", font=("Arial", 14, "bold"), pady=40)
        self.lbl_tareas.pack()
        
        # Entrada de texto para añadir nuevas tareas
        self.entry_tarea = tk.Entry(self.frame_tareas, font=("Arial", 12), width=30)
        self.entry_tarea.pack(pady=5)
        self.entry_tarea.insert(0, "Escribe una tarea y presiona Enter...")
        self.entry_tarea.bind("<FocusIn>", lambda e: self.entry_tarea.delete(0, tk.END) if self.entry_tarea.get() == "Escribe una tarea y presiona Enter..." else None)
        self.entry_tarea.bind("<Return>", self.agregar_tarea)
        
        # Contenedor dinámico de tareas
        self.lista_frame = tk.Frame(self.frame_tareas)
        self.lista_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)

    def agregar_tarea(self, event):
        texto = self.entry_tarea.get().strip()
        if texto and texto != "":
            frame_item = tk.Frame(self.lista_frame, bg=self.lista_frame["bg"])
            frame_item.pack(fill=tk.X, pady=4)
            
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                frame_item, text=texto, variable=var, font=("Arial", 11),
                bg=self.lista_frame["bg"], fg=self.text_area["fg"],
                selectcolor=self.text_area["bg"], activebackground=self.lista_frame["bg"]
            )
            chk.pack(side=tk.LEFT)
            
            btn_borrar = tk.Button(frame_item, text="❌", bd=0, bg=self.lista_frame["bg"], fg="#e74c3c", activebackground=self.lista_frame["bg"], command=frame_item.destroy)
            btn_borrar.pack(side=tk.RIGHT)
            
            self.entry_tarea.delete(0, tk.END)

    def crear_nav_bar(self):
        # Estructura limpia de botones inferiores con iconos representativos
        self.btn_notas = tk.Button(self.nav_bar, text="📝\nNotas", font=("Arial", 10), bd=0, command=lambda: self.mostrar_vista("notas"))
        self.btn_notas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.btn_tareas = tk.Button(self.nav_bar, text="📋\nTareas", font=("Arial", 10), bd=0, command=lambda: self.mostrar_vista("tareas"))
        self.btn_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Botón borrador / Deshabilitado para el futuro
        self.btn_dic = tk.Button(self.nav_bar, text="📖\nDiccionario", font=("Arial", 10), bd=0, state=tk.DISABLED)
        self.btn_dic.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def mostrar_vista(self, vista):
        # Quitamos del medio la vista actual para renderizar la seleccionada
        self.frame_notas.pack_forget()
        self.frame_tareas.pack_forget()
        
        if vista == "notas":
            self.frame_notas.pack(fill=tk.BOTH, expand=True)
        elif vista == "tareas":
            self.frame_tareas.pack(fill=tk.BOTH, expand=True)

    def crear_menu_temas(self):
        # Ventana modal flotante simplificada
        tk.Label(self.menu_temas, text="Temas disponibles", font=("Arial", 9, "bold"), bg="#f8f9fa", pady=5).pack(fill=tk.X)
        for nombre_tema in self.themes.keys():
            btn = tk.Button(
                self.menu_temas, text=nombre_tema, font=("Arial", 9), bd=0, padx=10, pady=5,
                command=lambda t=nombre_tema: self.cambiar_tema(t)
            )
            btn.pack(fill=tk.X)

    def toggle_menu_temas(self):
        # Muestra u oculta el modal flotante justo debajo del icono
        if self.menu_temas.winfo_viewable():
            self.menu_temas.place_forget()
        else:
            self.menu_temas.place(relx=0.97, rely=0.07, anchor="ne")

    def cambiar_tema(self, nombre_tema):
        self.current_theme = nombre_tema
        self.aplicar_tema()
        self.menu_temas.place_forget()

    def aplicar_tema(self):
        t = self.themes[self.current_theme]
        
        # 1. Ajustes del contenedor principal y raíz
        self.root.config(bg=t["bg"])
        self.main_frame.config(bg=t["bg"])
        self.frame_notas.config(bg=t["bg"])
        self.frame_tareas.config(bg=t["bg"])
        self.lista_frame.config(bg=t["bg"])
        
        # 2. Ajustes específicos de las vistas
        self.text_area.config(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])
        self.lbl_tareas.config(bg=t["bg"], fg=t["fg"])
        
        # 3. MAGIC COUPLING: Mimetizar el engranaje con el fondo actual
        self.config_btn.config(
            bg=t["bg"], fg=t["fg"], 
            activebackground=t["bg"], activeforeground=t["fg"]
        )
        
        # 4. Paleta de colores para el pop-up de temas
        self.menu_temas.config(bg=t["nav_bg"])
        for widget in self.menu_temas.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=t["accent"], fg=t["fg"])
            elif isinstance(widget, tk.Button):
                widget.config(bg=t["nav_bg"], fg=t["fg"], activebackground=t["accent"], activeforeground=t["fg"])

        # 5. Colores de la barra de navegación inferior
        self.nav_bar.config(bg=t["nav_bg"])
        for btn in [self.btn_notas, self.btn_tareas, self.btn_dic]:
            if btn["state"] != tk.DISABLED:
                btn.config(bg=t["nav_bg"], fg=t["fg"], activebackground=t["accent"], activeforeground=t["fg"])

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocCool(root)
    root.mainloop()