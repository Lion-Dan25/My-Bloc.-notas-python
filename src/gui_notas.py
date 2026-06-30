import tkinter as tk
from tkinter import ttk

class PanelNotas(tk.Frame):
    def __init__(self, parent, datos, callback_guardar):
        """
        Componente modular avanzado con flujo dinámico de pantallas (Lista -> Editor).
        parent: Contenedor principal de Tkinter.
        datos: Diccionario de datos centralizado (fuente única de verdad).
        callback_guardar: Función encargada de persistir los cambios en el JSON.
        """
        super().__init__(parent)
        self.datos = datos
        self.callback_guardar = callback_guardar
        self.nota_actual = None
        
        # Diccionario interno de control de colores para renderizado dinámico
        self.colores_actuales = {"bg": "#36393f", "fg": "#ffffff"}
        
        # Red de seguridad: Asegurar que la estructura de notas exista en los datos centralizados
        if "notas" not in self.datos or not isinstance(self.datos["notas"], list):
            self.datos["notas"] = []
            
        # Creación de los dos contenedores virtuales de pantalla
        self.frame_lista = tk.Frame(self)
        self.frame_editor = tk.Frame(self)
        
        # Inicializar los componentes de software de cada interfaz
        self.crear_componentes_lista()
        self.crear_componentes_editor()
        
        # Flujo inicial: Mostrar la lista de notas al arrancar el programa
        self.mostrar_vista_lista()

    def crear_componentes_lista(self):
        """Construye la interfaz de la lista externa de notas."""
        # Barra de herramientas superior de la lista
        self.header_lista = tk.Frame(self.frame_lista, height=50)
        self.header_lista.pack(fill="x", padx=10, pady=10)
        
        self.lbl_titulo_lista = tk.Label(self.header_lista, text="📝 Mis Notas", font=("Segoe UI", 14, "bold"))
        self.lbl_titulo_lista.pack(side="left")
        
        # Botón con la Cruz (➕) para inyectar nuevas notas
        self.btn_nueva_nota = tk.Button(
            self.header_lista, 
            text="➕", 
            font=("Segoe UI", 12, "bold"),
            bd=0, 
            cursor="hand2",
            command=self.crear_nueva_nota
        )
        self.btn_nueva_nota.pack(side="right")
        
        # Contenedor escroleable profesional mediante Canvas para soportar infinitas notas
        self.canvas_notas = tk.Canvas(self.frame_lista, bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.canvas_notas.yview)
        self.contenedor_tarjetas = tk.Frame(self.canvas_notas)
        
        # Configuración del scroll reactivo al tamaño del contenido
        self.contenedor_tarjetas.bind(
            "<Configure>",
            lambda e: self.canvas_notas.configure(scrollregion=self.canvas_notas.bbox("all"))
        )
        self.canvas_window = self.canvas_notas.create_window((0, 0), window=self.contenedor_tarjetas, anchor="nw")
        
        # Vincular el ancho del contenedor interno al ancho del Canvas de forma responsiva
        self.canvas_notas.bind(
            "<Configure>",
            lambda e: self.canvas_notas.itemconfig(self.canvas_window, width=e.width)
        )
        
        self.canvas_notas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas_notas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        self.scrollbar.pack(side="right", fill="y")

    def crear_componentes_editor(self):
        """Construye la interfaz del editor interno de la nota seleccionada."""
        # Header del editor
        self.header_editor = tk.Frame(self.frame_editor, height=40)
        self.header_editor.pack(fill="x", padx=10, pady=5)
        
        # Botón Volver que activará el guardado automático defensivo
        self.btn_volver = tk.Button(
            self.header_editor, 
            text="↩️ Volver a la lista", 
            font=("Segoe UI", 10, "bold"),
            bd=0, 
            cursor="hand2",
            command=self.regresar_y_guardar
        )
        self.btn_volver.pack(side="left")
        
        # Campo de Entrada para el Título de la Nota
        self.lbl_tit = tk.Label(self.frame_editor, text="Título de la Nota:", font=("Segoe UI", 10, "bold"))
        self.lbl_tit.pack(anchor="w", padx=10, pady=(10, 2))
        
        self.entry_titulo = tk.Entry(self.frame_editor, font=("Segoe UI", 12, "bold"), bd=1, relief="solid")
        self.entry_titulo.pack(fill="x", padx=10, pady=5)
        
        # Campo de Texto para el cuerpo/contenido
        self.lbl_cont = tk.Label(self.frame_editor, text="Contenido:", font=("Segoe UI", 10, "bold"))
        self.lbl_cont.pack(anchor="w", padx=10, pady=(10, 2))
        
        self.text_contenido = tk.Text(self.frame_editor, font=("Consolas", 11), wrap="word", bd=1, relief="solid")
        self.text_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_vista_lista(self):
        """Oculta el editor y despliega la lista externa actualizada."""
        self.frame_editor.pack_forget()
        self.frame_lista.pack(fill="both", expand=True)
        self.dibujar_lista_notas()

    def dibujar_lista_notas(self):
        """Mapea dinámicamente las notas del diccionario centralizado a tarjetas visuales."""
        # Limpiar tarjetas de notas anteriores para evitar duplicados en el render
        for widget in self.contenedor_tarjetas.winfo_children():
            widget.destroy()
            
        notas = self.datos.get("notas", [])
        
        if not notas:
            lbl_vacio = tk.Label(
                self.contenedor_tarjetas, 
                text="No hay notas guardadas.\n¡Presiona ➕ arriba para crear una!", 
                font=("Segoe UI", 11, "italic"),
                bg=self.colores_actuales.get("bg"),
                fg=self.colores_actuales.get("fg")
            )
            lbl_vacio.pack(pady=50)
            return
            
        # Iterar el arreglo de notas para fabricar la interfaz de tarjetas
        for nota in notas:
            # Tarjeta contenedora modular
            tarjeta = tk.Frame(
                self.contenedor_tarjetas, 
                bd=1, 
                relief="solid", 
                bg=self.colores_actuales.get("bg"),
                cursor="hand2"
            )
            tarjeta.pack(fill="x", padx=5, pady=6)
            
            # Obtener datos de forma segura
            titulo_texto = nota.get("titulo", "Sin título") or "Sin título"
            contenido_completo = nota.get("contenido", "")
            
            # Formatear la vista previa ("la etiqueta clarita de cómo empieza")
            vista_previa = contenido_completo.replace("\n", " ")[:40]
            if len(contenido_completo) > 40:
                vista_previa += "..."
            if not vista_previa.strip():
                vista_previa = "Nota vacía, escribe algo adentro..."
                
            # Etiqueta del Título de la tarjeta
            lbl_tarjeta_titulo = tk.Label(
                tarjeta, 
                text=titulo_texto, 
                font=("Segoe UI", 11, "bold"),
                bg=self.colores_actuales.get("bg"),
                fg=self.colores_actuales.get("fg"),
                anchor="w"
            )
            lbl_tarjeta_titulo.pack(fill="x", padx=12, pady=(6, 2))
            
            # Etiqueta de vista previa atenuada/más clarita (faded look)
            fg_faded = "#a3a6aa" if self.colores_actuales.get("bg") != "#ffffff" else "#686868"
            lbl_tarjeta_preview = tk.Label(
                tarjeta, 
                text=vista_previa, 
                font=("Segoe UI", 9, "italic"),
                bg=self.colores_actuales.get("bg"),
                fg=fg_faded,
                anchor="w"
            )
            lbl_tarjeta_preview.pack(fill="x", padx=12, pady=(0, 6))
            
            # Vincular el evento de clic en toda la tarjeta para abrir el editor de esa nota exacta
            for widget in (tarjeta, lbl_tarjeta_titulo, lbl_tarjeta_preview):
                widget.bind("<Button-1>", lambda event, n=nota: self.abrir_editor_nota(n))

    def abrir_editor_nota(self, nota):
        """Cambia el contexto de la pantalla hacia el editor de la nota seleccionada."""
        self.nota_actual = nota
        self.frame_lista.pack_forget()
        self.frame_editor.pack(fill="both", expand=True)
        
        # Limpiar e inyectar los datos en los controles gráficos
        self.entry_titulo.delete(0, tk.END)
        self.entry_titulo.insert(0, nota.get("titulo", ""))
        
        self.text_contenido.delete("1.0", tk.END)
        self.text_contenido.insert("1.0", nota.get("contenido", ""))
        self.entry_titulo.focus_set()

    def crear_nueva_nota(self):
        """Inyecta un nuevo objeto nota al diccionario y lo abre en caliente en el editor."""
        nueva_nota = {"titulo": "Nueva Nota 📝", "contenido": ""}
        self.datos["notas"].append(nueva_nota)
        self.abrir_editor_nota(nueva_nota)

    def regresar_y_guardar(self):
        """Sincroniza los textos con la BD central, auto-guarda el JSON y vuelve afuera."""
        if self.nota_actual is not None:
            # Absorber lo que escribió el usuario en caliente
            self.nota_actual["titulo"] = self.entry_titulo.get().strip() or "Sin título"
            self.nota_actual["contenido"] = self.text_contenido.get("1.0", "end-1c")
            
            # ¡Manejo defensivo y persistencia automática en tiempo real!
            self.callback_guardar()
            
        self.mostrar_vista_lista()

    def aplicar_tema(self, colores):
        """Método de control de calidad exigido por la arquitectura centralizada."""
        self.colores_actuales = colores
        bg = colores.get("bg", "#36393f")
        fg = colores.get("fg", "#ffffff")
        
        # Cálculo de paletas secundarias según el tema inyectado
        bg_header = "#2f3136" if bg != "#ffffff" else "#e0e0e0"
        bg_cajas = "#40444b" if bg != "#ffffff" else "#ffffff"
        bd_color = "#202225" if bg != "#ffffff" else "#cccccc"
        
        # Sincronizar contenedores raíces
        self.configure(bg=bg)
        self.frame_lista.configure(bg=bg)
        self.frame_editor.configure(bg=bg)
        
        # Elementos de la pantalla Lista
        self.header_lista.configure(bg=bg_header)
        self.lbl_titulo_lista.configure(bg=bg_header, fg=fg)
        self.btn_nueva_nota.configure(bg=bg_header, fg=fg, activebackground=bg_header, activeforeground=fg)
        self.canvas_notas.configure(bg=bg)
        self.contenedor_tarjetas.configure(bg=bg)
        
        # Elementos de la pantalla Editor
        self.header_editor.configure(bg=bg_header)
        self.btn_volver.configure(bg=bg_header, fg=fg, activebackground=bg_header, activeforeground=fg)
        self.lbl_tit.configure(bg=bg, fg=fg)
        self.lbl_cont.configure(bg=bg, fg=fg)
        
        # Sincronizar inputs y el color del cursor de texto (insertbackground)
        self.entry_titulo.configure(bg=bg_cajas, fg=fg, insertbackground=fg, highlightbackground=bd_color)
        self.text_contenido.configure(bg=bg_cajas, fg=fg, insertbackground=fg, highlightbackground=bd_color)
        
        # Forzar redibujado de la lista externa para aplicar colores a las tarjetas dinámicas
        if self.frame_lista.winfo_manager():
            self.dibujar_lista_notas()