import customtkinter as ctk
ctk.set_appearance_mode("light") 
import mysql.connector
import os
import ctypes
from pathlib import Path
from PIL import Image
import tkinter.messagebox as msgbox
from .agregar_proveedor import AgregarProveedorView
from src.Costs.controller import CostController
from src.database.connector import Connector

## Class CostosInvView
## This class creates a view for managing costs and ingredients.
class CostosAdminView(ctk.CTkFrame):
    ## Constructor
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)

        icono_bote_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
        self.img_bote = ctk.CTkImage(Image.open(icono_bote_path), size=(20, 20))

        icono_pen_path = BASE_DIR.parents[2] / "res" / "images" / "pen 1.png"
        self.img_pen = ctk.CTkImage(Image.open(icono_pen_path), size=(20, 20))

        icono_add_path = BASE_DIR.parents[2] / "res" / "images" / "add_circle.png"
        self.img_add = ctk.CTkImage(Image.open(icono_add_path), size=(20, 20))

        self.db_connector = Connector()
        self.session = self.db_connector.get_session()
        self.conn = self.db_connector.engine.raw_connection()
        self.cursor = self.conn.cursor()

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Costos", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        top_search_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_search_frame.pack(fill="x", padx=200, pady=(10, 10))

        self.search_entry = ctk.CTkEntry(top_search_frame, placeholder_text="Buscar ingrediente", width=500, height=30, fg_color="#dcd1cd", border_color="#b8191a", border_width=1, text_color="#3A3A3A", placeholder_text_color="#3A3A3A", font=self.fuente_small)
        self.search_entry.pack(side="left", padx=(0, 80))
        self.search_entry.bind("<KeyRelease>", lambda event: self.actualizar_cards())

        self.sort_option = ctk.CTkOptionMenu(top_search_frame, values=["Menor precio", "Mayor precio"], fg_color="#dcd1cd", button_color="#b8191a", button_hover_color="#991416", text_color="#3A3A3A", dropdown_fg_color="#dcd1cd", dropdown_text_color="#3A3A3A", font=self.fuente_small, dropdown_font=self.fuente_small)
        self.sort_option.set("Menor precio")
        self.sort_option.pack(side="left")
        self.sort_option.configure(command=self.actualizar_cards)

        btn_agregar = ctk.CTkButton(top_frame, image=self.img_add, text="Agregar nuevo proveedor", font=self.fuente_button, fg_color="#b8191a", hover_color="#991416", corner_radius=50, compound="left", command=self.mostrar_agregar_proveedor)
        btn_agregar.pack(side="right")

        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=25)

        ctk.CTkLabel(encabezado, text="Proveedor", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=1, padx=(40,0))
        ctk.CTkLabel(encabezado, text="Ingrediente", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=2, padx=(0,30))
        ctk.CTkLabel(encabezado, text="Unidad", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=3, padx=(0, 10), sticky="w")
        ctk.CTkLabel(encabezado, text="Precio", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=4, padx=(0, 10), sticky="w")

        encabezado.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)

        self.costos_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.costos_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_costos()
    ## Update method
    def actualizar_cards(self, *args):
        self.cargar_costos()

    ## Load costs
    def cargar_costos(self):
        for widget in self.costos_scroll_frame.winfo_children():
            widget.destroy()

        costos = CostController.get_all_costs(self.session)

        search_text = self.search_entry.get().strip().lower()
        if search_text:
            costos = CostController.search_costs(self.session, search_text)

        sort_option = self.sort_option.get()
        if sort_option == "Menor precio":
            costos = sorted(costos, key=lambda x: x.precio)
        else:
            costos = sorted(costos, key=lambda x: x.precio, reverse=True)

        for costo in costos:
            self.cursor.execute("SELECT nombre FROM Proveedores WHERE id_proveedor = %s", (costo.id_proveedor,))
            resultado = self.cursor.fetchone()
            nombre_proveedor = resultado[0] if resultado else "Desconocido"

            self.cursor.execute("SELECT unidad_medida FROM Ingredientes WHERE nombre = %s LIMIT 1", (costo.nombre_ingrediente,))
            unidad_result = self.cursor.fetchone()
            unidad = unidad_result[0] if unidad_result else "PZA"

            self.crear_card_costo(nombre_proveedor, costo.nombre_ingrediente, unidad, costo.precio)
    ## Function to create a cost card
    def crear_card_costo(self, proveedor, ingrediente, unidad, precio):
        card = ctk.CTkFrame(self.costos_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)
        
        ctk.CTkLabel(card, text=proveedor, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=1, padx=20)
        ctk.CTkLabel(card, text=ingrediente, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=2, padx=20)
        ctk.CTkLabel(card, text=unidad, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=3, padx=20)
        ctk.CTkLabel(card, text=f"${float(precio):.2f}", text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=4, padx=20)


        self.cursor.execute("SELECT id_proveedor FROM Proveedores WHERE nombre = %s", (proveedor,))
        proveedor_result = self.cursor.fetchone()
        proveedor_id = proveedor_result[0] if proveedor_result else None

        btn_editar = ctk.CTkButton(card, image=self.img_pen, text="", width=30, height=40, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda pid=proveedor_id, pname=proveedor: self.editar_proveedor(pid, pname))
        btn_editar.grid(row=0, column=6, padx=10)

        btn_eliminar = ctk.CTkButton(card, image=self.img_bote, text="", width=28, height=35, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda pid=proveedor_id, pname=proveedor, w=card: self.confirmar_eliminacion(pid, pname, w))
        btn_eliminar.grid(row=0, column=7, padx=(0, 10))

        card.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)

    ## Function to edit a provider
    def editar_proveedor(self, proveedor_id, nombre_proveedor):
        print(f"Editar proveedor: {nombre_proveedor} (ID: {proveedor_id})")
    ## Function to confirm deletion of a provider
    def confirmar_eliminacion(self, proveedor_id, proveedor_nombre, card_widget):
        ventana = ctk.CTkToplevel(self)
        ventana.title("Confirmar eliminación")
        ventana.geometry("400x200")
        ventana.configure(fg_color="#dcd1cd")
        ventana.grab_set()

        ventana.update_idletasks()
        ancho = 400
        alto = 200
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

        ctk.CTkLabel(ventana, text="¿Estás seguro?", font=self.fuente_titulo, text_color="#e03d3d").pack(pady=(20, 10))
        ctk.CTkLabel(ventana, text=f"¿Deseas eliminar el proveedor '{proveedor_nombre}'?", font=self.fuente_card, text_color="black").pack(pady=5)

        botones = ctk.CTkFrame(ventana, fg_color="transparent")
        botones.pack(pady=20)

        ctk.CTkButton(botones, text="Cancelar", font=self.fuente_button, fg_color="#a0a0a0", hover_color="#8c8c8c", width=100, command=ventana.destroy).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="Eliminar", font=self.fuente_button, fg_color="#d9534f", hover_color="#b52a25", width=100, command=lambda: self.eliminar_proveedor_confirmado(proveedor_id, proveedor_nombre, card_widget, ventana)).pack(side="left", padx=10)
    ## Function to confirm deletion of a provider
    def eliminar_proveedor_confirmado(self, proveedor_id, proveedor_nombre, card_widget, ventana):
        ventana.destroy()
        try:
            self.cursor.execute("DELETE FROM Costos WHERE id_proveedor = %s", (proveedor_id,))
            self.cursor.execute("DELETE FROM Proveedores WHERE id_proveedor = %s", (proveedor_id,))
            self.conn.commit()
            card_widget.destroy()
            self.mostrar_mensaje_personalizado("Eliminado", f"Proveedor '{proveedor_nombre}' eliminado correctamente.", "#b8191a")
        except Exception as e:
            self.mostrar_mensaje_personalizado("Error", f"No se pudo eliminar el proveedor.\n\n{e}", "#d9534f")
    ## Function to show a custom message
    def mostrar_mensaje_personalizado(self, titulo, mensaje, color):
        ventana_mensaje = ctk.CTkToplevel(self)
        ventana_mensaje.title(titulo)
        ventana_mensaje.geometry("420x200")
        ventana_mensaje.configure(fg_color="#dcd1cd")
        ventana_mensaje.grab_set()

        ventana_mensaje.update_idletasks()
        w = ventana_mensaje.winfo_width()
        h = ventana_mensaje.winfo_height()
        x = (ventana_mensaje.winfo_screenwidth() // 2) - (w // 2)
        y = (ventana_mensaje.winfo_screenheight() // 2) - (h // 2)
        ventana_mensaje.geometry(f"+{x}+{y}")

        ctk.CTkLabel(ventana_mensaje, text=titulo, font=self.fuente_titulo, text_color=color).pack(pady=(20, 10))
        ctk.CTkLabel(ventana_mensaje, text=mensaje, font=self.fuente_card, text_color="black", wraplength=380, justify="center").pack(pady=5)
        ctk.CTkButton(ventana_mensaje, text="Aceptar", font=self.fuente_button, width=120, fg_color=color, hover_color="#991416" if color == "#b8191a" else "#a12a28", command=ventana_mensaje.destroy).pack(pady=20)
    ## Function to create a new provider
    def mostrar_agregar_proveedor(self):
        for widget in self.winfo_children():
            widget.destroy()

        nueva_vista = AgregarProveedorView(
            parent=self,
            fuente_titulo=self.fuente_titulo,
            fuente_card=self.fuente_card,
            fuente_button=self.fuente_button
        )
        nueva_vista.pack(fill="both", expand=True)

    def on_close(self):
        if hasattr(self, 'session') and self.session:
            self.session.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        if hasattr(self, 'db_connector') and self.db_connector:
            self.db_connector.close_connection()
