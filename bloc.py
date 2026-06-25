import json
import os
import tkinter as tk
from tkinter import messagebox

class BlocCool:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Bloc Cool")
        self.root.geometry("600x520")
        
        # Archivo de persistencia real
        self.DB_FILE = "notas.json"
        self.notas = self.cargar_notas_desde_disco()
        self.active_note_idx = -1  # -1 significa que estamos creando una nota nueva

        # Paletas de colores dinámicas
        self.themes = {
            "Original (Blanco)": {"bg": "#ffffff", "fg": "#2c3e50", "accent": "#ecf0f1", "nav_bg": "#f8f9fa", "btn_add": "#2ecc71"},
            "Pastel Relajante": {"bg": "#fff5f5", "fg": "#4a4a4a", "accent": "#ffe3e3", "nav_bg": "#ffd1d1", "btn_add": "#ffb3b3"},
            "Modo Oscuro Cyberpunk": {"bg": "#0f0c1b", "fg": "#00ffcc", "accent": "#1a1530", "nav_bg": "#1f1a3a", "btn_add": "#ff007f"},
            "Ejecutivo (Azul/Gris)": {"bg": "#2b3e50", "fg": "#ffffff", "accent": "#1e2b37", "nav_bg": "#34495e", "btn_add": "#3498db"}
        }
        self.current_theme = "Original (Blanco)"

        # Contenedor Principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- EL ENGRANAJE INVISIBLE ---
        self.config_btn = tk.Button(
            self.root, text="⚙", font=("Arial", 18),
            bd=0, highlightthickness=0, cursor="hand2",
            command=self.toggle_menu_temas
        )
        self.config_btn.place(relx=0.97, rely=0.01, anchor="ne")

        self.menu_temas = tk.Frame(self.root, bd=1, relief=tk.SOLID)
        self.crear_menu_temas()

        # --- ESTRUCTURA DE LAS VISTAS ---
        self.frame_notas_raiz = tk.Frame(self.main_frame)
        self.frame_tareas = tk.Frame(self.main_frame)

        # Sub-vistas para el sistema de notas (Lista vs Editor)
        self.frame_lista_notas = tk.Frame(self.frame_notas_raiz)
        self.frame_editor_nota = tk.Frame(self.frame_notas_raiz)

        self.crear_arquitectura_notas()
        self.crear_vista_tareas()

        # Barra de navegación inferior
        self.nav_bar = tk.Frame(self.root, height=65)
        self.nav_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.crear_nav_bar()

        # Lanzamiento inicial
        self.mostrar_vista("notas")
        self.aplicar_tema()

    # --- PERSISTENCIA DE DATOS (GUARDADO REAL) ---
    def cargar_notas_desde_disco(self):
        if os.path.exists(self.DB_FILE):
            try:
                with open(self.DB_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def guardar_notas_en_disco(self):
        with open(self.DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.notas, f, ensure_ascii=False, indent=4)

    # --- ARQUITECTURA DEL SISTEMA DE NOTAS ---
    def crear_arquitectura_notas(self):
        self.frame_lista_notas.pack(fill=tk.BOTH, expand=True)
        
        # 1. Componentes de la VISTA LISTA
        self.lbl_no_notas = tk.Label(self.frame_lista_notas, text="No hay notas creadas.\n¡Presiona el botón + para empezar!", font=("Arial", 12, "italic"), pady=100)
        self.container_lista_botones = tk.Frame(self.frame_lista_notas, pady=20, padx=20)
        self.container_lista_botones.pack(fill=tk.BOTH, expand=True)

        # BOTÓN FLOTANTE CRUZ (+) - Ubicado matemáticamente abajo a la derecha
        self.btn_flotante_add = tk.Button(
            self.frame_lista_notas, text="+", font=("Arial", 22, "bold"),
            bd=0, highlightthickness=0, cursor="hand2", width=3, height=1,
            command=self.ir_a_crear_nota
        )
        self.btn_flotante_add.place(relx=0.93, rely=0.85, anchor="se")

        # 2. Componentes de la VISTA EDITOR
        self.top_editor_bar = tk.Frame(self.frame_editor_nota, pady=10, padx=15)
        self.top_editor_bar.pack(fill=tk.X)
        
        self.btn_volver = tk.Button(self.top_editor_bar, text="← Volver y Guardar", font=("Arial", 10, "bold"), bd=0, padx=10, pady=5, command=self.guardar_y_volver)
        self.btn_volver.pack(side=tk.LEFT)

        # Encabezado del título con tipografía grande de diseño
        self.entry_titulo = tk.Entry(self.frame_editor_nota, font=("Arial", 18, "bold"), bd=0, insertwidth=2)
        self.entry_titulo.pack(fill=tk.X, padx=20, pady=(15, 5))
        
        # Separador visual minimalista
        self.linea_divisoria = tk.Frame(self.frame_editor_nota, height=2)
        self.linea_divisoria.pack(fill=tk.X, padx=20, pady=5)

        # Campo inferior para el cuerpo de la nota
        self.text_contenido = tk.Text(self.frame_editor_nota, font=("Arial", 12), bd=0, padx=20, pady=10, wrap=tk.WORD)
        self.text_contenido.pack(fill=tk.BOTH, expand=True)

    def refrescar_render_lista_notas(self):
        # Limpiar botones anteriores
        for widget in self.container_lista_botones.winfo_children():
            widget.destroy()

        if not self.notas:
            self.lbl_no_notas.pack(fill=tk.BOTH, expand=True)
            return
        
        self.lbl_no_notas.pack_forget()
        
        # Renderizar cada nota como un botón estilizado
        t = self.themes[self.current_theme]
        for idx, nota in enumerate(self.notas):
            frame_item = tk.Frame(self.container_lista_botones, bg=t["bg"], pady=4)
            frame_item.pack(fill=tk.X)
            
            btn_nota = tk.Button(
                frame_item, text=f"📌  {nota['titulo']}", font=("Arial", 11, "bold"),
                anchor="w", bd=0, bg=t["accent"], fg=t["fg"],
                padx=15, pady=10, cursor="hand2",
                command=lambda i=idx: self.ir_a_editar_nota(i)
            )
            btn_nota.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            btn_eliminar = tk.Button(
                frame_item, text="🗑️", font=("Arial", 11), bd=0,
                bg=t["bg"], fg="#e74c3c", activebackground=t["bg"], cursor="hand2",
                command=lambda i=idx: self.eliminar_nota(i)
            )
            btn_eliminar.pack(side=tk.RIGHT, padx=5)

    def ir_a_crear_nota(self):
        self.active_note_idx = -1
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, "Nota nueva sin título")
        self.text_contenido.delete("1.0", tk.END)
        
        self.frame_lista_notas.pack_forget()
        self.frame_editor_nota.pack(fill=tk.BOTH, expand=True)
        self.entry_titulo.focus_set()

    def ir_a_editar_nota(self, index):
        self.active_note_idx = index
        nota = self.notas[index]
        
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, nota["titulo"])
        self.text_contenido.delete("1.0", tk.END)
        self.text_contenido.insert(tk.END, nota["contenido"])
        
        self.frame_lista_notas.pack_forget()
        self.frame_editor_nota.pack(fill=tk.BOTH, expand=True)

    def guardar_y_volver(self):
        titulo_texto = self.entry_titulo.get().strip()
        contenido_texto = self.text_contenido.get("1.0", tk.END).strip()
        
        if not titulo_texto:
            titulo_texto = "Nota vacía"

        struct_nota = {"titulo": titulo_texto, "contenido": contenido_texto}

        if self.active_note_idx == -1:
            self.notas.append(struct_nota)
        else:
            self.notas[self.active_note_idx] = struct_nota

        self.guardar_notas_en_disco()
        self.refrescar_render_lista_notas()
        
        # Regresar a la lista
        self.frame_editor_nota.pack_forget()
        self.frame_lista_notas.pack(fill=tk.BOTH, expand=True)
        self.aplicar_tema()

    def eliminar_nota(self, index):
        if messagebox.askyesno("Eliminar", "¿Seguro que quieres borrar esta nota?"):
            del self.notas[index]
            self.guardar_notas_en_disco()
            self.refrescar_render_lista_notas()

    # --- GESTOR DE TAREAS ---
    def crear_vista_tareas(self):
        self.lbl_tareas = tk.Label(self.frame_tareas, text="⚡ Lista de Tareas", font=("Arial", 14, "bold"), pady=40)
        self.lbl_tareas.pack()
        
        self.entry_tarea = tk.Entry(self.frame_tareas, font=("Arial", 12), width=30)
        self.entry_tarea.pack(pady=5)
        self.entry_tarea.insert(0, "Escribe una tarea y presiona Enter...")
        self.entry_tarea.bind("<FocusIn>", lambda e: self.entry_tarea.delete(0, tk.END) if self.entry_tarea.get() == "Escribe una tarea y presiona Enter..." else None)
        self.entry_tarea.bind("<Return>", self.agregar_tarea)
        
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
                bg=self.lista_frame["bg"], fg=self.lbl_tareas["fg"],
                selectcolor=self.frame_tareas["bg"], activebackground=self.lista_frame["bg"]
            )
            chk.pack(side=tk.LEFT)
            
            btn_borrar = tk.Button(frame_item, text="❌", bd=0, bg=self.lista_frame["bg"], fg="#e74c3c", activebackground=self.lista_frame["bg"], command=frame_item.destroy)
            btn_borrar.pack(side=tk.RIGHT)
            self.entry_tarea.delete(0, tk.END)

    # --- NAVEGACIÓN GENERAL ---
    def crear_nav_bar(self):
        self.btn_notas = tk.Button(self.nav_bar, text="📝\nNotas", font=("Arial", 10), bd=0, command=lambda: self.mostrar_vista("notas"))
        self.btn_notas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.btn_tareas = tk.Button(self.nav_bar, text="📋\nTareas", font=("Arial", 10), bd=0, command=lambda: self.mostrar_vista("tareas"))
        self.btn_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.btn_dic = tk.Button(self.nav_bar, text="📖\nDiccionario", font=("Arial", 10), bd=0, state=tk.DISABLED)
        self.btn_dic.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def mostrar_vista(self, vista):
        self.frame_notas_raiz.pack_forget()
        self.frame_tareas.pack_forget()
        
        if vista == "notas":
            self.frame_notas_raiz.pack(fill=tk.BOTH, expand=True)
            self.refrescar_render_lista_notas()
        elif vista == "tareas":
            self.frame_tareas.pack(fill=tk.BOTH, expand=True)
        self.aplicar_tema()

    # --- SISTEMA DE TEMAS DINÁMICOS ---
    def crear_menu_temas(self):
        tk.Label(self.menu_temas, text="Temas disponibles", font=("Arial", 9, "bold"), bg="#f8f9fa", pady=5).pack(fill=tk.X)
        for nombre_tema in self.themes.keys():
            btn = tk.Button(
                self.menu_temas, text=nombre_tema, font=("Arial", 9), bd=0, padx=10, pady=5,
                command=lambda t=nombre_tema: self.cambiar_tema(t)
            )
            btn.pack(fill=tk.X)

    def toggle_menu_temas(self):
        if self.menu_temas.winfo_viewable():
            self.menu_temas.place_forget()
        else:
            self.menu_temas.place(relx=0.97, rely=0.07, anchor="ne")

    def cambiar_tema(self, nombre_tema):
        self.current_theme = nombre_tema
        self.aplicar_tema()
        self.refrescar_render_lista_notas()
        self.menu_temas.place_forget()

    def aplicar_tema(self):
        t = self.themes[self.current_theme]
        
        self.root.config(bg=t["bg"])
        self.main_frame.config(bg=t["bg"])
        self.frame_notas_raiz.config(bg=t["bg"])
        self.frame_lista_notas.config(bg=t["bg"])
        self.frame_editor_nota.config(bg=t["bg"])
        self.frame_tareas.config(bg=t["bg"])
        self.lista_frame.config(bg=t["bg"])
        self.container_lista_botones.config(bg=t["bg"])
        
        # Estilos del editor
        self.top_editor_bar.config(bg=t["nav_bg"])
        self.btn_volver.config(bg=t["accent"], fg=t["fg"], activebackground=t["nav_bg"])
        self.entry_titulo.config(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])
        self.linea_divisoria.config(bg=t["accent"])
        self.text_contenido.config(bg=t["bg"], fg=t["fg"], insertbackground=t["fg"])
        
        self.lbl_no_notas.config(bg=t["bg"], fg=t["fg"])
        self.lbl_tareas.config(bg=t["bg"], fg=t["fg"])
        
        # Mimetizar engranaje
        self.config_btn.config(bg=t["bg"], fg=t["fg"], activebackground=t["bg"], activeforeground=t["fg"])
        
        # Estilar Botón Flotante de Cruz (+)
        self.btn_flotante_add.config(bg=t["btn_add"], fg="#ffffff", activebackground=t["accent"])

        # Menú desplegable flotante de temas
        self.menu_temas.config(bg=t["nav_bg"])
        for widget in self.menu_temas.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=t["accent"], fg=t["fg"])
            elif isinstance(widget, tk.Button):
                widget.config(bg=t["nav_bg"], fg=t["fg"], activebackground=t["accent"], activeforeground=t["fg"])

        # Barra inferior
        self.nav_bar.config(bg=t["nav_bg"])
        for btn in [self.btn_notas, self.btn_tareas, self.btn_dic]:
            if btn["state"] != tk.DISABLED:
                btn.config(bg=t["nav_bg"], fg=t["fg"], activebackground=t["accent"], activeforeground=t["fg"])

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocCool(root)
    root.mainloop()