## @file actualizar_proveedores.py
## @brief View to display and update existing providers' product information.

import customtkinter as ctk
from datetime import date
import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv


class ActualizarProveedoresView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"

        if os.name == "nt":
            import ctypes
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=13)

        load_dotenv()
        self.conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_DATABASE"),
            port=int(os.getenv("DB_PORT"))
        )
        self.cursor = self.conn.cursor()

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        titulo = ctk.CTkLabel(self.contenedor, text="Actualizar proveedores", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(anchor="w", padx=30, pady=(10, 5))

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        self.scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.mostrar_proveedores()

    def mostrar_proveedores(self):
        self.cursor.execute("SELECT nombre, fecha_expedicion, fecha_vigencia FROM Proveedores")
        proveedores = self.cursor.fetchall()

        for nombre, fecha_exp, fecha_vig in proveedores:
            self.crear_card(nombre, fecha_exp, fecha_vig)

    def crear_card(self, nombre, fecha_exp, fecha_vig):
        hoy = date.today()

        expirada = False
        if fecha_vig is not None:
            expirada = fecha_vig < hoy

        texto_fecha = "Fecha expirada" if expirada else f"{fecha_exp} - {fecha_vig}" if fecha_exp and fecha_vig else "Fechas no registradas"
        color_texto = "#e03d3d" if expirada else "#3A3A3A"

        card = ctk.CTkButton(self.scroll_frame, fg_color="white", hover_color="#f1f1f1", corner_radius=12, text="", height=80, command=lambda: self.abrir_proveedor(nombre))
        card.pack(fill="x", pady=10, padx=30)
        card.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(card, text=nombre, font=self.fuente_card, text_color="black").grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        ctk.CTkLabel(card, text="Seleccionar si deseas cambiar la información de los productos", font=self.fuente_card, text_color="#a0a0a0").grid(row=1, column=0, sticky="w", padx=10)

        ctk.CTkLabel(card, text=texto_fecha, font=self.fuente_card, text_color=color_texto).grid(row=0, column=1, rowspan=2, sticky="e", padx=10)
    
    def abrir_proveedor(self, nombre_proveedor):
        for widget in self.master.winfo_children():
            widget.destroy()

        nueva_vista = ProveedorDatosView(self.master, nombre_proveedor, self.fuente_card, self.fuente_small)
        nueva_vista.pack(fill="both", expand=True)

