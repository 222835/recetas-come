import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.Providers.controller import ProveedorController
from src.Providers.model import Proveedor, Base  # Importa el modelo y Base

class ProveedorScreen(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Configuración de la base de datos (reemplaza con tu configuración)
        self.engine = create_engine('sqlite:///:memory:')  # Para pruebas en memoria
        Base.metadata.create_all(self.engine)  # Crea las tablas
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Configuración del grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Widgets para la creación de proveedores
        self.nombre_label = ctk.CTkLabel(self, text="Nombre:")
        self.nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.nombre_entry = ctk.CTkEntry(self)
        self.nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.categoria_label = ctk.CTkLabel(self, text="Categoría:")
        self.categoria_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.categoria_entry = ctk.CTkEntry(self)
        self.categoria_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        self.crear_button = ctk.CTkButton(self, text="Crear Proveedor", command=self.crear_proveedor)
        self.crear_button.grid(row=0, column=4, padx=10, pady=5)

        # Treeview para listar los proveedores
        self.treeview = ttk.Treeview(self, column=("Nombre", "Categoría"), show="headings")
        self.treeview.heading("#1", text="Nombre")
        self.treeview.heading("#2", text="Categoría")
        self.treeview.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.actualizar_tabla()

    def crear_proveedor(self):
        nombre = self.nombre_entry.get()
        categoria = self.categoria_entry.get()
        ProveedorController.create_proveedor(self.session, nombre=nombre, categoria=categoria)
        self.actualizar_tabla()
        # Limpiar los campos de entrada
        self.nombre_entry.delete(0, ctk.END)
        self.categoria_entry.delete(0, ctk.END)

    def actualizar_tabla(self):
        # Limpiar la tabla
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        # Obtener los proveedores de la base de datos
        proveedores = self.session.query(Proveedor).all()

        # Insertar los proveedores en la tabla
        for proveedor in proveedores:
            self.treeview.insert("", ctk.END, values=(proveedor.nombre, proveedor.categoria))

if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    proveedor_screen = ProveedorScreen(master=app)
    proveedor_screen.pack(fill="both", expand=True)
    app.mainloop()