import customtkinter as ctk
from tkinter import ttk, messagebox
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Costs.controller import CostController
from src.Providers.controller import ProveedorController
from src.database.connector import Connector

class AgregarProveedorView(ctk.CTkFrame):
    def __init__(self, parent, fuente_titulo, fuente_card, fuente_button):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        
        self.connector = Connector()
        self.session = self.connector.get_session()
        
        self.fuente_titulo = fuente_titulo
        self.fuente_card = fuente_card
        self.fuente_button = fuente_button
        
        self.cost_controller = CostController()
        self.productos = []

        self.build_interface()

    def build_interface(self):
        contenedor = ctk.CTkFrame(self, fg_color="#E8E3E3", corner_radius=25, width=880, height=580)
        contenedor.pack(padx=40, pady=40, fill="both", expand=True)
        contenedor.pack_propagate(False)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 5))

        ctk.CTkLabel(top_frame, text="Nuevo proveedor", font=self.fuente_titulo, text_color="#b8191a").pack(side="left")

        ctk.CTkButton(
            top_frame,
            text="← Volver",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=50,
            width=130,
            command=self.volver_a_costos
        ).pack(side="right")

        ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a").pack(fill="x", padx=30, pady=(0, 10))

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

        info_label = ctk.CTkLabel(
            scroll, 
            text="Para pegar datos desde Excel: Selecciona la tabla y presiona Ctrl+V",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#b8191a"
        )
        info_label.pack(pady=(10, 0))

        self.tabla_frame = ctk.CTkFrame(scroll, fg_color="white", corner_radius=25)
        self.tabla_frame.pack(padx=20, pady=20, fill="both", expand=True)

        tabla_con_scroll = ctk.CTkFrame(self.tabla_frame, fg_color="white")
        tabla_con_scroll.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tabla_con_scroll, columns=("Descripcion", "Unidad", "Precio"), show="headings", height=8)
        self.tree.heading("Descripcion", text="Descripción del producto")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.column("Descripcion", anchor="w", width=250)
        self.tree.column("Unidad", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabla_con_scroll, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Control-v>", self.pegar_desde_excel)
        self.tree.bind("<Control-V>", self.pegar_desde_excel)
        
        self.tree.bind("<Button-1>", lambda event: self.tree.focus_set())
        
        self.bind("<Control-v>", self.pegar_desde_excel)
        self.bind("<Control-V>", self.pegar_desde_excel)
        self.tabla_frame.bind("<Control-v>", self.pegar_desde_excel)
        self.tabla_frame.bind("<Control-V>", self.pegar_desde_excel)


        btn_guardar = ctk.CTkButton(scroll, text="Guardar proveedor", font=self.fuente_button, width=500, corner_radius=50, fg_color="#b8191a", hover_color="#991416", command=self.guardar_proveedor)
        btn_guardar.pack(pady=(10, 20))

    def pegar_desde_excel(self, event=None):
        import tkinter as tk
        import re

        try:
            root = tk.Tk()
            root.withdraw()
            raw = root.clipboard_get()
            root.destroy()

            if not raw.strip():
                messagebox.showwarning("Portapapeles vacío", "No hay datos para pegar.")
                return

            rows = raw.strip().split("\n")
            self.tree.delete(*self.tree.get_children())
            self.productos.clear()
            count = 0

            for row in rows:
                parts = [p.strip() for p in row.split("\t")]
                if len(parts) < 3:
                    continue

                descripcion = parts[0]
                unidad = parts[1]
                precio_str = re.sub(r"[^\d.,]", "", parts[2]).replace(",", ".")

                try:
                    precio = float(precio_str)
                except ValueError:
                    continue

                self.tree.insert("", "end", values=(descripcion, unidad, f"{precio:.2f}"))
                self.productos.append({
                    "descripcion": descripcion,
                    "unidad": unidad,
                    "precio": precio
                })
                count += 1

            if count == 0:
                messagebox.showwarning("Sin datos", "No se encontraron datos válidos para pegar.")
            else:
                messagebox.showinfo("Pegado exitoso", f"Se pegaron {count} productos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo pegar: {str(e)}")
    
    def guardar_proveedor(self):
        nombre = self.entry_nombre.get().strip()
        contacto = self.entry_contacto.get().strip()

        if not nombre or not contacto:
            messagebox.showerror("Campos incompletos", "Por favor llena todos los campos obligatorios.")
            return
            
        if not self.productos:
            respuesta = messagebox.askyesno("Advertencia", "No hay productos en la lista. ¿Desea continuar sin productos?")
            if not respuesta:
                return

        try:
            proveedor_existente = ProveedorController.get_provider_by_name(self.session, nombre)
            if proveedor_existente:
                messagebox.showerror("Error", f"Ya existe un proveedor con el nombre '{nombre}'.")
                return
            
            nuevo = ProveedorController.create_proveedor(self.session, nombre, "General")
            self.session.refresh(nuevo)
            
            for producto in self.productos:
                self.cost_controller.create_cost(
                    self.session,
                    nombre=producto["descripcion"],
                    precio=producto["precio"],
                    id_proveedor=nuevo.id_proveedor
                )
            
            self.session.commit()
            self.mostrar_mensaje_personalizado("Agregado", f"Proveedor '{nombre}' agregado correctamente.", "#b8191a")
            self.volver_a_costos()
        except Exception as e:
            self.session.rollback()
            self.mostrar_mensaje_personalizado("Error", f"No se pudo agregar el proveedor.\n\n{str(e)}", "#d9534f")

    def mostrar_mensaje_personalizado(self, titulo, mensaje, color):
        messagebox.showinfo(titulo, mensaje)

    def volver_a_costos(self):
        self.session.close()
        self.connector.close_connection()
        from .costos import CostosAdminView
        for widget in self.master.winfo_children():
            widget.destroy()
        vista_costos = CostosAdminView(self.master)
        vista_costos.pack(fill="both", expand=True)