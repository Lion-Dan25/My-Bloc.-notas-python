import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import json
import os

# --- CONFIGURACIÓN DE TEMAS FRESCOS ---
TEMAS = {
    "Minimalista Mint (Relajante)": {
        "bg_editor": "#F4F9F4", "fg_editor": "#2C4A3E",
        "bg_panel": "#E1EFE0", "bg_btn": "#A2D2A8", "fg_btn": "#1C3328",
        "fuente": ("Segoe UI", 12)
    },
    "Cyberpunk Night (Oscuro)": {
        "bg_editor": "#1E1E2F", "fg_editor": "#00FFFF",
        "bg_panel": "#27293D", "bg_btn": "#FF007F", "fg_btn": "#FFFFFF",
        "fuente": ("Consolas", 12)
    },
    "Atardecer Caliente (Productivo)": {
        "bg_editor": "#FFF5EE", "fg_editor": "#4A2E2B",
        "bg_panel": "#FFE4E1", "bg_btn": "#FFA07A", "fg_btn": "#4A2E2B",
        "fuente": ("Helvetica", 12)
    }
}

class BlocPremium:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Mi Bloc Personal Premium")
        self.root.geometry("850x550")
        self.root.configure(bg="#F0F2F5")

        self.archivo_actual = None
        self.tareas = []  # Lista para guardar los textos de las tareas

        # --- ESTILOS MODERNOS (TTK) ---
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # --- CONTENEDOR PRINCIPAL ---
        self.paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#DCDCDC", sashwidth=4)
        self.paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- COLUMNA IZQUIERDA: EDITOR DE TEXTO ---
        self.frame_editor = tk.Frame(self.paned, bg="#FFFFFF")
        self.paned.add(self.frame_editor, minsize=500)

        # Barra de Herramientas Superior del Editor
        self.barratools = tk.Frame(self.frame_editor, bg="#F0F2F5", height=40)
        self.barratools.pack(fill=tk.X, side=tk.TOP)

        # Botones del Editor con estilo plano
        self.btn_guardar = tk.Button(self.barratools, text="💾 Guardar", command=self.guardar_archivo, relief=tk.FLAT, bg="#E4E6EB")
        self.btn_guardar.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_cargar = tk.Button(self.barratools, text="📂 Abrir", command=self.cargar_archivo, relief=tk.FLAT, bg="#E4E6EB")
        self.btn_cargar.pack(side=tk.LEFT, padx=5, pady=5)

        # Selector de Temas Combinados
        tk.Label(self.barratools, text="🎨 Tema:", bg="#F0F2F5", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(15, 2))
        self.combo_temas = ttk.Combobox(self.barratools, values=list(TEMAS.keys()), state="readonly", width=25)
        self.combo_temas.set("Minimalista Mint (Relajante)")
        self.combo_temas.pack(side=tk.LEFT, padx=5, pady=5)
        self.combo_temas.bind("<<ComboboxSelected>>", self.aplicar_tema)

        # Campo de Texto Principal
        self.text_area = tk.Text(self.frame_editor, wrap=tk.WORD, bd=0, padx=15, pady=15)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # --- COLUMNA DERECHA: PANEL DE TAREAS (CHECKBOXES) ---
        self.frame_tareas = tk.Frame(self.paned, width=300, bg="#E1EFE0", padx=10, pady=10)
        self.paned.add(self.frame_tareas, minsize=250)

        tk.Label(self.frame_tareas, text="📋 Mis Tareas de Hoy", font=("Segoe UI", 13, "bold"), bg="#E1EFE0").pack(anchor=tk.W, pady=(0, 10))

        # Input para nueva tarea
        self.entry_tarea = ttk.Entry(self.frame_tareas, font=("Segoe UI", 11))
        self.entry_tarea.pack(fill=tk.X, pady=5)
        self.entry_tarea.bind("<Return>", lambda event: self.agregar_tarea())

        self.btn_add_tarea = tk.Button(self.frame_tareas, text="➕ Añadir Tarea", command=self.agregar_tarea, relief=tk.FLAT, font=("Segoe UI", 9, "bold"))
        self.btn_add_tarea.pack(fill=tk.X, pady=2)

        # Contenedor para la lista de checkboxes scrolleable
        self.canvas_tareas = tk.Canvas(self.frame_tareas, bg="#E1EFE0", bd=0, highlightthickness=0)
        self.scroll_tareas = ttk.Scrollbar(self.frame_tareas, orient="vertical", command=self.canvas_tareas.yview)
        self.scroll_frame_tareas = tk.Frame(self.canvas_tareas, bg="#E1EFE0")

        self.scroll_frame_tareas.bind(
            "<Configure>",
            lambda e: self.canvas_tareas.configure(scrollregion=self.canvas_tareas.bbox("all"))
        )
        self.canvas_tareas.create_window((0, 0), window=self.scroll_frame_tareas, anchor="nw")
        self.canvas_tareas.configure(yscrollcommand=self.scroll_tareas.set)

        self.canvas_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        self.scroll_tareas.pack(side=tk.RIGHT, fill=tk.Y)

        # Aplicar el tema por defecto al iniciar
        self.aplicar_tema()

    def aplicar_tema(self, event=None):
        nombre_tema = self.combo_temas.get()
        t = TEMAS[nombre_tema]

        # Configurar Editor
        self.text_area.configure(bg=t["bg_editor"], fg=t["fg_editor"], font=t["fuente"])
        
        # Configurar Paneles y Botones
        self.frame_tareas.configure(bg=t["bg_panel"])
        self.canvas_tareas.configure(bg=t["bg_panel"])
        self.scroll_frame_tareas.configure(bg=t["bg_panel"])
        
        self.btn_add_tarea.configure(bg=t["bg_btn"], fg=t["fg_btn"])
        self.btn_guardar.configure(bg=t["bg_btn"], fg=t["fg_btn"])
        self.btn_cargar.configure(bg=t["bg_btn"], fg=t["fg_btn"])

    def agregar_tarea(self):
        texto = self.entry_tarea.get().strip()
        if texto:
            var_check = tk.BooleanVar()
            
            # Contenedor para el checkbox y botón de borrar
            item_frame = tk.Frame(self.scroll_frame_tareas, bg=self.frame_tareas.cget("bg"))
            item_frame.pack(fill=tk.X, anchor=tk.W, pady=2)

            # Checkbox moderno usando ttk
            chk = ttk.Checkbutton(item_frame, text=texto, variable=var_check, command=lambda: self.marcar_tarea(chk, var_check))
            chk.pack(side=tk.LEFT, anchor=tk.W, padx=5)

            # Botón discreto para eliminar tarea de la lista
            btn_del = tk.Button(item_frame, text="❌", bd=0, bg=self.frame_tareas.cget("bg"), fg="red", 
                                command=lambda: item_frame.destroy(), cursor="hand2")
            btn_del.pack(side=tk.RIGHT, padx=5)

            self.entry_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Atención", "No puedes añadir una tarea vacía.")

    def marcar_tarea(self, checkbox, variable):
        # Efecto visual cool: Si se marca, podríamos hacer algo, o simplemente dejar que guarde estado
        pass

    def guardar_archivo(self):
        contenido = self.text_area.get("1.0", tk.END)
        if not self.archivo_actual:
            self.archivo_actual = filedialog.asksaveasfilename(defaultextension=".txt",
                                                                 filetypes=[("Archivos de texto", "*.txt")])
        if self.archivo_actual:
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(contenido)
            self.root.title(f"🚀 Mi Bloc Personal Premium - {os.path.basename(self.archivo_actual)}")

    def cargar_archivo(self):
        self.archivo_actual = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if self.archivo_actual:
            with open(self.archivo_actual, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", contenido)
            self.root.title(f"🚀 Mi Bloc Personal Premium - {os.path.basename(self.archivo_actual)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocPremium(root)
    root.mainloop()