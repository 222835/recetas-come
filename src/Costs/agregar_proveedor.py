## @file agregar_proveedor.py
## @brief Provides the view for adding a new provider and its products.

import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk

## @class AgregarProveedorView
## @brief Displays the interface to add a new provider and their products.
class AgregarProveedorView(ctk.CTkFrame):
    ## @brief Initializes the provider addition view.
    def __init__(self, parent, conn, cursor, fuente_titulo, fuente_card, fuente_button):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.conn = conn
        self.cursor = cursor
        self.fuente_titulo = fuente_titulo
        self.fuente_card = fuente_card
        self.fuente_button = fuente_button

        self.build_interface()

    ## @brief Builds the UI components.
    def build_interface(self):
        contenedor = ctk.CTkFrame(self, fg_color="#E8E3E3", corner_radius=25, width=880, height=580)
        contenedor.pack(padx=40, pady=40, fill="both", expand=True)
        contenedor.pack_propagate(False)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 5))

        titulo = ctk.CTkLabel(top_frame, text="Nuevo proveedor", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        btn_volver = ctk.CTkButton(
            top_frame,
            text="← Volver",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=50,
            width=130,
            command=self.volver_a_costos
        )
        btn_volver.pack(side="right")

        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(contenedor, fg_color="white", corner_radius=25)
        scroll.pack(padx=30, pady=10, fill="both", expand=True)

        entradas_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        entradas_frame.pack(padx=20, pady=20, fill="x")

        nombre_frame = ctk.CTkFrame(entradas_frame, fg_color="transparent")
        nombre_frame.pack(side="left", padx=(0, 40))

        ctk.CTkLabel(nombre_frame, text="Nombre", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w", padx=(80, 0))
        ctk.CTkLabel(nombre_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w", padx=(80, 0))
        self.entry_nombre = ctk.CTkEntry(nombre_frame, width=400, fg_color="#F4F4F4", text_color="black", border_color="#E1222A", border_width=1)
        self.entry_nombre.pack(pady=(5, 0), padx=(80, 0), anchor="w")

        contacto_frame = ctk.CTkFrame(entradas_frame, fg_color="transparent")
        contacto_frame.pack(side="left")

        ctk.CTkLabel(contacto_frame, text="Contacto", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w", padx=(30, 0))
        ctk.CTkLabel(contacto_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w", padx=(30, 0))
        self.entry_contacto = ctk.CTkEntry(contacto_frame, width=300, fg_color="#F4F4F4", text_color="black", border_color="#E1222A", border_width=1)
        self.entry_contacto.pack(pady=(5, 0), padx=(30, 0), anchor="w")

        fechas_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        fechas_frame.pack(padx=20, pady=(10, 0), fill="x")

        expedicion_frame = ctk.CTkFrame(fechas_frame, fg_color="transparent")
        expedicion_frame.pack(side="left", padx=(0, 40))

        ctk.CTkLabel(expedicion_frame, text="Fecha de expedición", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w", padx=(80, 0))
        ctk.CTkLabel(expedicion_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w", padx=(80, 0))
        self.fecha_expedicion = DateEntry(expedicion_frame, width=18, background='#b8191a', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_expedicion.pack(pady=(5, 0), padx=(30, 0), anchor="w")

        vigencia_frame = ctk.CTkFrame(fechas_frame, fg_color="transparent")
        vigencia_frame.pack(side="left")

        ctk.CTkLabel(vigencia_frame, text="Fecha de vigencia", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        ctk.CTkLabel(vigencia_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w")
        self.fecha_vigencia = DateEntry(vigencia_frame, width=18, background='#b8191a', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_vigencia.pack(pady=(5, 0), padx=(30, 0), anchor="w")

        self.tabla_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=25)
        self.tabla_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree = ttk.Treeview(self.tabla_frame, columns=("Descripcion", "Unidad", "Precio", "Moneda"), show="headings", height=8)
        self.tree.heading("Descripcion", text="Descripción del producto")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Moneda", text="Moneda")

        self.tree.column("Descripcion", anchor="w", width=250)
        self.tree.column("Unidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Moneda", anchor="center", width=100)

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        btn_guardar = ctk.CTkButton(scroll, text="Guardar proveedor", font=self.fuente_button, width=500, corner_radius=50, fg_color="#b8191a", hover_color="#991416", command=self.guardar_proveedor)
        btn_guardar.pack(pady=(10, 20))

    ## @brief Saves the new provider to the database.
    def guardar_proveedor(self):
        nombre = self.entry_nombre.get().strip()
        contacto = self.entry_contacto.get().strip()
        fecha_expedicion = self.fecha_expedicion.get_date()
        fecha_vigencia = self.fecha_vigencia.get_date()

        if not nombre or not contacto or not fecha_expedicion or not fecha_vigencia:
            from tkinter import messagebox
            messagebox.showerror("Campos incompletos", "Por favor llena todos los campos obligatorios.")
            return

        try:
            self.cursor.execute("INSERT INTO Proveedores (nombre, categoria) VALUES (%s, %s)", (nombre, "General"))
            self.conn.commit()
            self.master.mostrar_mensaje_personalizado("Agregado", f"Proveedor '{nombre}' agregado correctamente.", "#b8191a")
            self.volver_a_costos()
        except Exception as e:
            self.master.mostrar_mensaje_personalizado("Error", f"No se pudo agregar el proveedor.\n\n{e}", "#d9534f")

    ## @brief Returns to the cost management view.
    def volver_a_costos(self):
        from .costos import CostosAdminView
        for widget in self.master.winfo_children():
            widget.destroy()
        vista_costos = CostosAdminView(self.master)
        vista_costos.pack(fill="both", expand=True)
