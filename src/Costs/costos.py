## @file costos.py
## @brief Manages the cost management interface for providers in the Admin Dashboard.
import customtkinter as ctk
ctk.set_appearance_mode("light") 
import mysql.connector
import os
import ctypes
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
import tkinter.messagebox as msgbox
from .agregar_proveedor import AgregarProveedorView

## @class CostosAdminView
## @brief Displays the list of providers and costs.
class CostosAdminView(ctk.CTkFrame):
    ## @brief Initializes the CostosAdminView interface.
    ## @param parent Parent widget.
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

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Costos", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        top_search_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_search_frame.pack(fill="x", padx=200, pady=(10, 10))

        self.search_entry = ctk.CTkEntry(
            top_search_frame,
            placeholder_text="Buscar ingrediente",
            width=500,
            height=30,
            fg_color="#dcd1cd",
            border_color="#b8191a",
            border_width=1,
            text_color="#3A3A3A",
            placeholder_text_color="#3A3A3A",
            font=self.fuente_small
        )
        self.search_entry.pack(side="left", padx=(0, 80))
        self.search_entry.bind("<KeyRelease>", lambda event: self.actualizar_cards())

        self.sort_option = ctk.CTkOptionMenu(
            top_search_frame,
            values=["Menor precio", "Mayor precio"],
            fg_color="#dcd1cd",
            button_color="#b8191a",
            button_hover_color="#991416",
            text_color="#3A3A3A",
            dropdown_fg_color="#dcd1cd",
            dropdown_text_color="#3A3A3A",
            font=self.fuente_small,
            dropdown_font=self.fuente_small
        )
        self.sort_option.set("Menor precio")
        self.sort_option.pack(side="left")

        btn_agregar = ctk.CTkButton(top_frame, image=self.img_add, text="Agregar nuevo proveedor", font=self.fuente_button, fg_color="#b8191a", hover_color="#991416", corner_radius=50, compound="left", command=self.mostrar_agregar_proveedor)
        btn_agregar.pack(side="right")


        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=25)

        ctk.CTkLabel(encabezado, text="Proveedor", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=1, padx=(40,0))
        ctk.CTkLabel(encabezado, text="Ingrediente", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=2, padx=(0,30))
        ctk.CTkLabel(encabezado, text="Unidad", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=3, padx=(0,30))
        ctk.CTkLabel(encabezado, text="Precio", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=4, padx=(0,30))
        ctk.CTkLabel(encabezado, text="Moneda", text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=5, padx=(0,30))
        encabezado.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)

        self.costos_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.costos_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_costos()

    ## @brief Loads cost data from the database and creates cards.
    def cargar_costos(self):
        for widget in self.costos_scroll_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("""
            SELECT p.nombre, c.precio
            FROM Proveedores p
            JOIN Costos c ON p.id_proveedor = c.id_proveedor
        """)
        costos = self.cursor.fetchall()

        for proveedor, precio in costos:
            self.crear_card_costo(proveedor, "LECHUGA", "PZA", precio, "MX")

    ## @brief Creates a cost card with edit and delete buttons.
    def crear_card_costo(self, proveedor, ingrediente, unidad, precio, moneda):
        card = ctk.CTkFrame(self.costos_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)

        icono = ctk.CTkLabel(card, text="💲", font=self.fuente_card)
        icono.grid(row=0, column=0, padx=(10, 10), pady=10)

        ctk.CTkLabel(card, text=proveedor, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=1, padx=10)
        ctk.CTkLabel(card, text=ingrediente, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=2, padx=10)
        ctk.CTkLabel(card, text=unidad, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=3, padx=10)
        ctk.CTkLabel(card, text=f"${precio:.2f}", text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=4, padx=10)
        ctk.CTkLabel(card, text=moneda, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=5, padx=10)

        btn_editar = ctk.CTkButton(card, image=self.img_pen, text="", width=30, height=40, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda: print(f"Editar proveedor: {proveedor}"))
        btn_editar.grid(row=0, column=6, padx=10)

        btn_eliminar = ctk.CTkButton(card, image=self.img_bote, text="", width=28, height=35, fg_color="white", hover_color="#E8E8E8", corner_radius=5, command=lambda: self.confirmar_eliminacion(proveedor, card))
        btn_eliminar.grid(row=0, column=7, padx=(0, 10))

        card.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)

    ## @brief Shows confirmation dialog to delete a cost entry.
    def confirmar_eliminacion(self, proveedor, card_widget):
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
        ctk.CTkLabel(ventana, text=f"¿Deseas eliminar el proveedor '{proveedor}'?", font=self.fuente_card, text_color="black").pack(pady=5)

        botones = ctk.CTkFrame(ventana, fg_color="transparent")
        botones.pack(pady=20)

        ctk.CTkButton(botones, text="Cancelar", font=self.fuente_button, fg_color="#a0a0a0", hover_color="#8c8c8c", width=100, command=ventana.destroy).pack(side="left", padx=10)
        ctk.CTkButton(botones, text="Eliminar", font=self.fuente_button, fg_color="#d9534f", hover_color="#b52a25", width=100, command=lambda: self.eliminar_proveedor_confirmado(proveedor, card_widget, ventana)).pack(side="left", padx=10)

    ## @brief Deletes a provider and shows a feedback message.
    def eliminar_proveedor_confirmado(self, proveedor, card_widget, ventana):
        ventana.destroy()
        try:
            self.cursor.execute("DELETE FROM Proveedores WHERE nombre = %s", (proveedor,))
            self.conn.commit()
            card_widget.destroy()
            self.mostrar_mensaje_personalizado("Eliminado", f"Proveedor '{proveedor}' eliminado correctamente.", "#b8191a")
        except Exception as e:
            self.mostrar_mensaje_personalizado("Error", f"No se pudo eliminar el proveedor.\n\n{e}", "#d9534f")

    ## @brief Shows a modal message window.
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

    ## @brief Opens the AgregarProveedorView inside the current container.
    def mostrar_agregar_proveedor(self):
        for widget in self.winfo_children():
            widget.destroy()

        nueva_vista = AgregarProveedorView(
            parent=self,
            conn=self.conn,
            cursor=self.cursor,
            fuente_titulo=self.fuente_titulo,
            fuente_card=self.fuente_card,
            fuente_button=self.fuente_button
        )
        nueva_vista.pack(fill="both", expand=True)

    ## @brief Saves the new provider to the database.
    def guardar_nuevo_proveedor(self, nombre, precio, ventana):
        try:
            self.cursor.execute("INSERT INTO Proveedores (nombre, categoria) VALUES (%s, %s)", (nombre, "General"))
            self.conn.commit()
            ventana.destroy()
            self.cargar_costos()
            self.mostrar_mensaje_personalizado("Agregado", f"Proveedor '{nombre}' agregado correctamente.", "#b8191a")
        except Exception as e:
            self.mostrar_mensaje_personalizado("Error", f"No se pudo agregar el proveedor.\n\n{e}", "#d9534f")


