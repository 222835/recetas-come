import customtkinter as ctk
from tkinter import ttk, messagebox
from src.Recipes.controller import RecetasController
from src.database.connector import Connector
from src.Recipes.nueva_receta_admin import NuevaRecetaView
from PIL import Image, ImageTk

class RecetasAdminView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        self.connector = Connector()
        self.session = self.connector.get_session()
        super().__init__(master, **kwargs)
        self.configure(fg_color="#ECEFF4")

        self.title = ctk.CTkLabel(self, text="Recetas", font=("Arial", 28, "bold"), text_color="#B81919")
        self.title.pack(anchor="nw", padx=30, pady=(30, 10))

        self.agregar_btn = ctk.CTkButton(self, text="🧾 Agregar nueva receta", fg_color="#B81919", hover_color="#a01515", width=180, command=self.abrir_vista_nueva_receta)
        self.agregar_btn.pack(anchor="ne", padx=30, pady=(0, 10))

        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=30, pady=(5, 10))

        self.buscar_entry = ctk.CTkEntry(self.search_frame, placeholder_text="🔍 Buscar receta", width=300)
        self.buscar_entry.grid(row=0, column=0, padx=5, pady=5)

        self.filtro_tiempo = ctk.CTkComboBox(self.search_frame, values=["Todos", "Desayuno", "Comida"], width=150, command=lambda choice: self.cargar_recetas())
        self.filtro_tiempo.grid(row=0, column=1, padx=5)

        self.filtro_categoria = ctk.CTkComboBox(self.search_frame, values=["Todos", "Guarnicion", "Guisado", "Antojo"], width=150, command=lambda choice: self.cargar_recetas())
        self.filtro_categoria.grid(row=0, column=2, padx=5)

        self.buscar_entry.bind("<KeyRelease>", lambda e: self.cargar_recetas())
        self.filtro_tiempo.set("Todos")
        self.filtro_categoria.set("Todos")

        # Tabla con columna de acciones
        columnas = ("Nombre", "Ingredientes", "Cantidad", "Unidad", "Comensales", "Tiempo", "Categoría", "Acciones")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")

        for col in columnas:
            self.tree.heading(col, text=col)
            ancho = 80 if col == "Acciones" else 120
            self.tree.column(col, anchor="center", width=ancho)

        self.tree.pack(fill="both", expand=True, padx=30, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.manejar_accion)

        self.cargar_recetas()

    def cargar_recetas(self):
        nombre = self.buscar_entry.get().strip()
        periodo = self.filtro_tiempo.get()
        clasificacion = self.filtro_categoria.get()

        recetas = RecetasController.search_recipes(
            self.session,
            nombre=nombre if nombre else None,
            periodo=periodo if periodo != "Todos" else None,
            clasificacion=clasificacion if clasificacion != "Todos" else None
        )

        for row in self.tree.get_children():
            self.tree.delete(row)

        if not recetas:
            self.tree.insert("", "end", values=("No hay recetas coincidentes", "", "", "", "", "", "", ""))
            return

        for receta in recetas:
            for ingrediente in receta["ingredientes"]:
                self.tree.insert("", "end", values=(
                    receta["nombre_receta"],
                    ingrediente["nombre_ingrediente"],
                    ingrediente["Cantidad"],
                    ingrediente["Unidad"],
                    receta["comensales_base"],
                    receta["periodo"],
                    receta["clasificacion_receta"],
                    "✏️ 🗑️"
                ))

    def manejar_accion(self, event):
        item = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        if not item or self.tree.item(item, "values")[0] == "No hay recetas guardadas":
            return

        if col == '#8':  # Columna de acciones
            respuesta = messagebox.askquestion("Acción", "¿Qué deseas hacer con esta receta?\n\nSí = Editar\nNo = Eliminar", icon="question")
            if respuesta == 'yes':
                self.editar_receta()
            else:
                self.eliminar_receta()

    def abrir_vista_nueva_receta(self):
        nueva_ventana = ctk.CTkToplevel(self)
        nueva_ventana.geometry("1000x700")
        nueva_ventana.title("Nueva Receta")
        #Cuando se cambie esto a redirigir y no crear una nueva ventana, cerrar session antes de destruir el widget
        NuevaRecetaView(nueva_ventana).pack(fill="both", expand=True)

    def editar_receta(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una receta para editar.")
            return
        print("Editar receta:", self.tree.item(selected)["values"])

    def eliminar_receta(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Aviso", "Selecciona una receta para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta receta?")
        if confirm:
            self.tree.delete(selected)
