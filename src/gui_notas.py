import customtkinter as ctk

class PanelNotas(ctk.CTkFrame):
    def __init__(self, parent, datos, callback_guardar):
        """
        Componente modular avanzado con flujo dinámico de pantallas (Lista -> Editor)
        completamente migrado a CustomTkinter.
        parent: Contenedor principal.
        datos: Diccionario de datos centralizado (fuente única de verdad).
        callback_guardar: Función encargada de persistir los cambios en el JSON.
        """
        # Inicializamos el contenedor base como un CTkFrame
        super().__init__(parent)
        self.datos = datos
        self.callback_guardar = callback_guardar
        self.nota_actual = None
        
        # Diccionario interno de control de colores para renderizado dinámico
        self.colores_actuales = {"bg": "#36393f", "fg": "#ffffff"}
        
        # Red de seguridad: Asegurar que la estructura de notas exista en los datos centralizados
        if "notas" not in self.datos or not isinstance(self.datos["notas"], list):
            self.datos["notas"] = []
            
        # Creación de los dos contenedores virtuales de pantalla (ahora CTkFrames modernos)
        self.frame_lista = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_editor = ctk.CTkFrame(self, fg_color="transparent")
        
        # Inicializar los componentes de software de cada interfaz
        self.crear_componentes_lista()
        self.crear_componentes_editor()
        
        # Flujo inicial: Mostrar la lista de notas al arrancar el programa
        self.mostrar_vista_lista()

    def crear_componentes_lista(self):
        """Construye la interfaz de la lista externa de notas."""
        # Barra de herramientas superior de la lista
        self.header_lista = ctk.CTkFrame(self.frame_lista, height=50)
        self.header_lista.pack(fill="x", padx=10, pady=10)
        
        self.lbl_titulo_lista = ctk.CTkLabel(self.header_lista, text="📝 Mis Notas", font=("Segoe UI", 16, "bold"))
        self.lbl_titulo_lista.pack(side="left", padx=15, pady=10)
        
        # Botón con la Cruz (➕) estilizado de forma limpia y moderna
        self.btn_nueva_nota = ctk.CTkButton(
            self.header_lista, 
            text="➕", 
            font=("Segoe UI", 14, "bold"),
            width=40,
            height=35,
            fg_color="transparent",
            hover_color="#40444b",
            command=self.crear_nueva_nota
        )
        self.btn_nueva_nota.pack(side="right", padx=15, pady=10)
        
        # 🔥 CRACK DE ARQUITECTURA: Reemplazamos más de 15 líneas de Canvas/Scrollbar 
        # por un solo CTkScrollableFrame nativo, ultra responsivo y limpio.
        self.contenedor_tarjetas = ctk.CTkScrollableFrame(self.frame_lista, fg_color="transparent")
        self.contenedor_tarjetas.pack(fill="both", expand=True, padx=10, pady=5)

    def crear_componentes_editor(self):
        """Construye la interfaz del editor interno de la nota seleccionada."""
        # Header del editor
        self.header_editor = ctk.CTkFrame(self.frame_editor, height=45)
        self.header_editor.pack(fill="x", padx=10, pady=5)
        
        # Botón Volver con estilo moderno transparente
        self.btn_volver = ctk.CTkButton(
            self.header_editor, 
            text="↩️ Volver a la lista", 
            font=("Segoe UI", 11, "bold"),
            fg_color="transparent",
            hover_color="#40444b",
            command=self.regresar_y_guardar
        )
        self.btn_volver.pack(side="left", padx=10, pady=5)
        
        # Campo de Entrada para el Título de la Nota
        self.lbl_tit = ctk.CTkLabel(self.frame_editor, text="Título de la Nota:", font=("Segoe UI", 11, "bold"))
        self.lbl_tit.pack(anchor="w", padx=12, pady=(10, 2))
        
        self.entry_titulo = ctk.CTkEntry(self.frame_editor, font=("Segoe UI", 13, "bold"), border_width=1)
        self.entry_titulo.pack(fill="x", padx=10, pady=5)
        
        # Campo de Texto para el cuerpo/contenido (Usamos CTkTextbox)
        self.lbl_cont = ctk.CTkLabel(self.frame_editor, text="Contenido:", font=("Segoe UI", 11, "bold"))
        self.lbl_cont.pack(anchor="w", padx=12, pady=(10, 2))
        
        self.text_contenido = ctk.CTkTextbox(self.frame_editor, font=("Consolas", 12), wrap="word", border_width=1)
        self.text_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    def mostrar_vista_lista(self):
        """Oculta el editor y despliega la lista externa actualizada."""
        self.frame_editor.pack_forget()
        self.frame_lista.pack(fill="both", expand=True)
        self.dibujar_lista_notas()

    def dibujar_lista_notas(self):
        """Mapea dinámicamente las notas del diccionario centralizado a tarjetas visuales."""
        # Limpiar tarjetas de notas anteriores para evitar duplicaciones
        for widget in self.contenedor_tarjetas.winfo_children():
            widget.destroy()
            
        notas = self.datos.get("notas", [])
        
        if not notas:
            lbl_vacio = ctk.CTkLabel(
                self.contenedor_tarjetas, 
                text="No hay notas guardadas.\n¡Presiona ➕ arriba para crear una!", 
                font=("Segoe UI", 12, "italic"),
                text_color=self.colores_actuales.get("fg")
            )
            lbl_vacio.pack(pady=50)
            return
            
        # Iterar el arreglo de notas para fabricar la interfaz de tarjetas
        for nota in notas:
            # Tarjeta contenedora modular con bordes redondeados nativos (corner_radius)
            tarjeta = ctk.CTkFrame(
                self.contenedor_tarjetas, 
                fg_color=self.colores_actuales.get("bg"),
                corner_radius=8,
                border_width=1,
                border_color="#202225" if self.colores_actuales.get("bg") != "#ffffff" else "#cccccc"
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
            lbl_tarjeta_titulo = ctk.CTkLabel(
                tarjeta, 
                text=titulo_texto, 
                font=("Segoe UI", 12, "bold"),
                text_color=self.colores_actuales.get("fg"),
                anchor="w"
            )
            lbl_tarjeta_titulo.pack(fill="x", padx=15, pady=(8, 2))
            
            # Etiqueta de vista previa atenuada/más clarita (faded look)
            fg_faded = "#a3a6aa" if self.colores_actuales.get("bg") != "#ffffff" else "#686868"
            lbl_tarjeta_preview = ctk.CTkLabel(
                tarjeta, 
                text=vista_previa, 
                font=("Segoe UI", 10, "italic"),
                text_color=fg_faded,
                anchor="w"
            )
            lbl_tarjeta_preview.pack(fill="x", padx=15, pady=(0, 8))
            
            # Vincular el evento de clic en toda la tarjeta usando CustomTkinter
            for widget in (tarjeta, lbl_tarjeta_titulo, lbl_tarjeta_preview):
                widget.bind("<Button-1>", lambda event, n=nota: self.abrir_editor_nota(n))

    def abrir_editor_nota(self, nota):
        """Cambia el contexto de la pantalla hacia el editor de la nota seleccionada."""
        self.nota_actual = nota
        self.frame_lista.pack_forget()
        self.frame_editor.pack(fill="both", expand=True)
        
        # Limpiar e inyectar los datos usando cadenas seguras ("end" en lugar de tk.END)
        self.entry_titulo.delete(0, "end")
        self.entry_titulo.insert(0, nota.get("titulo", ""))
        
        self.text_contenido.delete("1.0", "end")
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
            
            # Persistencia automática defensiva
            self.callback_guardar()
            
        self.mostrar_vista_lista()

    def aplicar_tema(self, colores):
        """Método exigido por el orquestador central (main.py) para inyectar paletas dinámicas."""
        self.colores_actuales = colores
        bg = colores.get("bg", "#36393f")
        fg = colores.get("fg", "#ffffff")
        
        # Cálculo de paletas secundarias según el tema inyectado
        bg_header = "#2f3136" if bg != "#ffffff" else "#e0e0e0"
        bg_cajas = "#40444b" if bg != "#ffffff" else "#ffffff"
        bd_color = "#202225" if bg != "#ffffff" else "#cccccc"
        bg_hover = "#4a4d52" if bg != "#ffffff" else "#d0d0d0"
        
        # Sincronizar contenedores raíces mediante fg_color de CustomTkinter
        self.configure(fg_color=bg)
        self.frame_lista.configure(fg_color=bg)
        self.frame_editor.configure(fg_color=bg)
        
        # Elementos de la pantalla Lista
        self.header_lista.configure(fg_color=bg_header)
        self.lbl_titulo_lista.configure(text_color=fg)
        self.btn_nueva_nota.configure(text_color=fg, hover_color=bg_hover)
        self.contenedor_tarjetas.configure(fg_color=bg)
        
        # Elementos de la pantalla Editor
        self.header_editor.configure(fg_color=bg_header)
        self.btn_volver.configure(text_color=fg, hover_color=bg_hover)
        self.lbl_tit.configure(text_color=fg)
        self.lbl_cont.configure(text_color=fg)
        
        # Sincronizar inputs (Entry y Textbox), modificando bordes y texto de inserción
        self.entry_titulo.configure(fg_color=bg_cajas, text_color=fg, border_color=bd_color)
        self.text_contenido.configure(fg_color=bg_cajas, text_color=fg, border_color=bd_color)
        
        # Forzar redibujado de la lista externa si está activa para repintar las tarjetas internas
        if self.frame_lista.winfo_manager():
            self.dibujar_lista_notas()