import customtkinter as ctk
from src.components.navbar import Navbar
from src.components.sidebar import Sidebar

class RecetasAdminView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ECEFF4")  # Fondo claro

        # Navbar
        self.navbar = Navbar(self)
        self.navbar.pack(side="top", fill="x")

        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        # Contenido principal
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título de la vista
        self.title_label = ctk.CTkLabel(self.content_frame, text="Administración de Recetas", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        # Tabla de recetas (simulada con un Treeview)
        self.tree = ctk.CTkTreeview(self.content_frame, columns=("Nombre", "Ingredientes", "Cantidad", "Unidad", "Comensales", "Tiempo", "Categoría"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ingredientes", text="Ingredientes")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Comensales", text="Comensales")
        self.tree.heading("Tiempo", text="Tiempo")
        self.tree.heading("Categoría", text="Categoría")
        self.tree.pack(fill="both", expand=True, pady=10)

        # Agregar datos de ejemplo (simulados)
        self.tree.insert("", "end", values=("ARROZ BLANCO", "ARROZ, ACEITE", "3", "KG", "4", "30 min", "GUARNICION"))
        self.tree.insert("", "end", values=("PASTA", "PASTA, SALSA", "2", "KG", "6", "20 min", "PLATO PRINCIPAL"))

        # Formulario para agregar nueva receta
        self.form_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.form_frame.pack(fill="x", pady=20)

        self.nombre_label = ctk.CTkLabel(self.form_frame, text="Nombre:")
        self.nombre_label.grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        self.ingredientes_label = ctk.CTkLabel(self.form_frame, text="Ingredientes:")
        self.ingredientes_label.grid(row=1, column=0, padx=5, pady=5)
        self.ingredientes_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.ingredientes_entry.grid(row=1, column=1, padx=5, pady=5)

        self.cantidad_label = ctk.CTkLabel(self.form_frame, text="Cantidad:")
        self.cantidad_label.grid(row=2, column=0, padx=5, pady=5)
        self.cantidad_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.cantidad_entry.grid(row=2, column=1, padx=5, pady=5)

        self.unidad_label = ctk.CTkLabel(self.form_frame, text="Unidad:")
        self.unidad_label.grid(row=3, column=0, padx=5, pady=5)
        self.unidad_entry = ctk.CTkEntry(self.form_frame, width=200)
        self.unidad_entry.grid(row=3, column=1, padx=5, pady=5)

        self.agregar_button = ctk.CTkButton(self.form_frame, text="Agregar Receta", fg_color="#4C566A", hover_color="#434C5E", command=self.agregar_receta)
        self.agregar_button.grid(row=4, column=0, columnspan=2, pady=10)

    def agregar_receta(self):
        # Obtener los valores del formulario
        nombre = self.nombre_entry.get()
        ingredientes = self.ingredientes_entry.get()
        cantidad = self.cantidad_entry.get()
        unidad = self.unidad_entry.get()

        # Agregar la nueva receta a la tabla
        if nombre and ingredientes and cantidad and unidad:
            self.tree.insert("", "end", values=(nombre, ingredientes, cantidad, unidad, "", "", ""))
            self.nombre_entry.delete(0, "end")
            self.ingredientes_entry.delete(0, "end")
            self.cantidad_entry.delete(0, "end")
            self.unidad_entry.delete(0, "end")