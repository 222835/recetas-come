## @file agregar_proveedor.py
## @brief Provides the view for adding a new provider and their products.

import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk
import random

## @class AgregarProveedorView
## @brief Displays the interface to add a new provider and their products.
class AgregarProveedorView(ctk.CTkFrame):
    ## @brief Constructor.
    ## @param parent The parent container.
    ## @param conn Database connection object.
    ## @param cursor Database cursor.
    ## @param fuente_titulo Title font.
    ## @param fuente_card Font for labels and entries.
    ## @param fuente_button Font for buttons.
    def __init__(self, parent, conn, cursor, fuente_titulo, fuente_card, fuente_button):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.conn = conn
        self.cursor = cursor
        self.fuente_titulo = fuente_titulo
        self.fuente_card = fuente_card
        self.fuente_button = fuente_button

        self.build_interface()

    ## @brief Validates the contact field to allow only numbers up to 10 digits.
    ## @param proposed Proposed text input.
    ## @return True if valid, False otherwise.
    def _validate_contacto(self, proposed: str) -> bool:
        return proposed.isdigit() and len(proposed) <= 10 or proposed == ""

    ## @brief Builds the user interface.
    def build_interface(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure('TCombobox',
                        fieldbackground='white',
                        background='white',
                        bordercolor='white',
                        lightcolor='white',
                        darkcolor='white',
                        arrowcolor='black',
                        borderwidth=0,
                        relief='flat')

        container = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25, width=880, height=580)
        container.pack(padx=40, pady=40, fill="both", expand=True)
        container.pack_propagate(False)

        top_frame = ctk.CTkFrame(container, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 5))

        title = ctk.CTkLabel(top_frame, text="Nuevo proveedor", font=self.fuente_titulo, text_color="#b8191a")
        title.pack(side="left")

        btn_back = ctk.CTkButton(top_frame, text="← Volver", font=self.fuente_button, fg_color="#b8191a",
                                 hover_color="#991416", corner_radius=50, width=130, command=self.volver_a_costos)
        btn_back.pack(side="right")

        line = ctk.CTkLabel(container, text="─" * 200, text_color="#b8191a")
        line.pack(fill="x", padx=60, pady=(0, 10))

        scroll = ctk.CTkScrollableFrame(container, fg_color="white", corner_radius=25)
        scroll.pack(padx=30, pady=10, fill="both", expand=True)

        entries_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        entries_frame.pack(padx=(110, 0), pady=(0, 30), anchor="w", fill="x")
        entries_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="a")
        entries_frame.grid_columnconfigure((3, 4), weight=1, uniform="b")

        name_frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
        name_frame.grid(row=0, column=0, padx=(0, 5), pady=(0, 10), sticky="nw")
        ctk.CTkLabel(name_frame, text="Nombre", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        ctk.CTkLabel(name_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w")
        self.entry_nombre = ctk.CTkEntry(name_frame, width=300, fg_color="#F4F4F4", text_color="black",
                                         border_color="#E1222A", border_width=1)
        self.entry_nombre.pack(anchor="w", pady=(5, 0))

        contact_frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
        contact_frame.grid(row=0, column=1, padx=(5, 5), pady=(0, 10), sticky="nw")
        ctk.CTkLabel(contact_frame, text="Contacto", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        ctk.CTkLabel(contact_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w")
        self.entry_contacto = ctk.CTkEntry(contact_frame, width=250, fg_color="#F4F4F4", text_color="black",
                                           border_color="#E1222A", border_width=1,
                                           validate='key',
                                           validatecommand=(self.register(self._validate_contacto), '%P'))
        self.entry_contacto.pack(anchor="w", pady=(5, 0))

        category_frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
        category_frame.grid(row=0, column=2, padx=(5, 0), pady=(0, 10), sticky="nw")
        ctk.CTkLabel(category_frame, text="Categoría", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        ctk.CTkLabel(category_frame, text="* campo obligatorio", font=ctk.CTkFont(size=10), text_color="#E1222A").pack(anchor="w")
        self.combo_categoria = ctk.CTkOptionMenu(category_frame,
                                                 values=["Carnes", "Frutas y verduras", "Lácteos",
                                                         "Panadería y tortillería", "Bebidas", "Abarrotes",
                                                         "Desechables y químicos"],
                                                 font=self.fuente_card, fg_color="#F4F4F4", button_color="#E1222A",
                                                 button_hover_color="#b8191a", text_color="black",
                                                 dropdown_font=self.fuente_card, dropdown_fg_color="#F4F4F4",
                                                 dropdown_text_color="black", width=180)
        self.combo_categoria.set("Selecciona una categoría")
        self.combo_categoria.pack(anchor="w", pady=(5, 0))

        family = self.fuente_card.cget("family")
        size = self.fuente_card.cget("size")

        issue_frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
        issue_frame.grid(row=1, column=0, padx=(0, 5), pady=(0, 10), sticky="nw")
        ctk.CTkLabel(issue_frame, text="Fecha de expedición", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        self.fecha_expedicion = DateEntry(issue_frame, font=(family, size), background="#F4F4F4",
                                          foreground="black", borderwidth=0, relief="flat", state="readonly",
                                          date_pattern="yyyy-mm-dd")
        self.fecha_expedicion.configure(width=220)
        self.fecha_expedicion.pack(anchor="w", pady=(5, 0))

        valid_frame = ctk.CTkFrame(entries_frame, fg_color="transparent")
        valid_frame.grid(row=1, column=1, padx=(5, 0), pady=(0, 10), sticky="nw")
        ctk.CTkLabel(valid_frame, text="Fecha de vigencia", font=self.fuente_card, text_color="#3A3A3A").pack(anchor="w")
        self.fecha_vigencia = DateEntry(valid_frame, font=(family, size), background="#F4F4F4", foreground="black",
                                        borderwidth=0, relief="flat", state="readonly", date_pattern="yyyy-mm-dd")
        self.fecha_vigencia.configure(width=220)
        self.fecha_vigencia.pack(anchor="w", pady=(5, 0))

        self.tabla_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=25)
        self.tabla_frame.pack(padx=(110, 0), pady=(10, 30), anchor="nw")

        tabla_con_scroll = ctk.CTkFrame(self.tabla_frame, fg_color="white")  
        tabla_con_scroll.pack()

        self.tree = ttk.Treeview(tabla_con_scroll, columns=("Descripcion", "Unidad", "Precio", "Moneda"),
                         show="headings", height=10)
        self.tree.heading("Descripcion", text="Descripción del producto")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Moneda", text="Moneda")

        self.tree.column("Descripcion", width=300, anchor="w")
        self.tree.column("Unidad", width=180, anchor="center")
        self.tree.column("Precio", width=160, anchor="center")
        self.tree.column("Moneda", width=160, anchor="center")
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(tabla_con_scroll, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        ## @brief Enables pasting Excel data into the table
        def paste_from_clipboard(event=None):
            try:
                pasted_data = self.clipboard_get()
                rows = pasted_data.strip().split("\n")
                for row in rows:
                    values = row.strip().split("\t")
                    if len(values) == 4:
                        self.tree.insert("", "end", values=values)
                    else:
                        print("Formato no válido:", row)
            except Exception as e:
                print("Error al pegar datos:", e)

        self.tree.bind("<Control-v>", paste_from_clipboard)
        self.tree.bind("<Control-V>", paste_from_clipboard)

        btn_save = ctk.CTkButton(scroll, text="Guardar proveedor", font=self.fuente_button, width=500,
                                 corner_radius=50, fg_color="#b8191a", hover_color="#991416",
                                 command=self.guardar_proveedor)
        btn_save.pack(pady=(30, 80))


    ## @brief Saves the new provider to the database.
    def guardar_proveedor(self):
        nombre = self.entry_nombre.get().strip()
        contacto = self.entry_contacto.get().strip()
        fecha_expedicion = self.fecha_expedicion.get_date()
        fecha_vigencia = self.fecha_vigencia.get_date()
        categoria = self.combo_categoria.get()
        if categoria == "Selecciona una categoría":
            self.master.mostrar_mensaje_personalizado("Error", "Selecciona una categoría válida.", "#e03d3d")
            return

        if not nombre or not contacto or not categoria or not fecha_expedicion or not fecha_vigencia:
            self.master.mostrar_mensaje_personalizado("Error", "Por favor llena todos los campos obligatorios.",
                                                      "#e03d3d")
            return

        try:
            while True:
                id_prov = random.randint(1, 999999)
                self.cursor.execute("SELECT 1 FROM Proveedores WHERE id_proveedor = %s", (id_prov,))
                if not self.cursor.fetchone():
                    break

            self.cursor.execute("INSERT INTO Proveedores (id_proveedor, nombre, categoria) VALUES (%s, %s, %s)",
                                (id_prov, nombre, categoria))
            self.conn.commit()
            self.master.mostrar_mensaje_personalizado("Agregado",
                                                      f"Proveedor '{nombre}' agregado correctamente.",
                                                      "#b8191a")
            self.volver_a_costos()
        except Exception as e:
            self.master.mostrar_mensaje_personalizado("Error", f"No se pudo agregar el proveedor.\n\n{e}",
                                                      "#d9534f")

    ## @brief Returns to the cost management view.
    def volver_a_costos(self):
        from .costos import CostosAdminView
        for widget in self.master.winfo_children():
            widget.destroy()
        vista_costos = CostosAdminView(self.master)
        vista_costos.pack(fill="both", expand=True)
