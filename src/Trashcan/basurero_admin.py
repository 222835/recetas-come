## @class CuentasAdminView
## @brief Manages the administrator account interface and user control panel.
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from dotenv import load_dotenv
import mysql.connector
import os
import ctypes
from pathlib import Path
from PIL import Image 
import tkinter.messagebox as msgbox


class AdminTrashcanView(ctk.CTkFrame):
    ## @brief Initializes the account management view.
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

        BASE_DIR = Path(__file__).resolve()
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
        top_frame.pack(fill="x", padx=30, pady=(30, 0))

        middle_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        middle_frame.pack(fill="x", padx=30, pady=(5, 0))

        middle_frame.grid_rowconfigure(1, weight=1)
        middle_frame.grid_columnconfigure(0, weight=2)
        middle_frame.grid_columnconfigure(1, weight=1)

        bottom_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=30, pady=(10, 10))

        bottom_frame.grid_columnconfigure((0, 2), weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0, minsize=20)

        titulo = ctk.CTkLabel(top_frame, text="Basurero", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(middle_frame, text="─" * 200, text_color="#b8191a")
        linea.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(5, 5))

        self.entry_buscar = ctk.CTkEntry(middle_frame, placeholder_text="Buscar...")
        self.entry_buscar.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(5, 5))

        calendar_frame = tk.Frame(middle_frame)
        calendar_frame.grid(row=1, column=1, sticky="nsew", pady=(5, 5))
        date_entry = DateEntry(calendar_frame, width=12, background='darkred', foreground='white', borderwidth=1, date_pattern='yyyy-mm-dd')
        date_entry.pack(fill="x")

        self.btn_recetas = ctk.CTkButton(
            bottom_frame,
            width=250,
            text="Recetas",
            font=self.fuente_button,
            fg_color="#b8191a",
            text_color="white",
            hover_color="#991416",
            corner_radius=50,
            command=self.seleccionar_recetas
        )
        self.btn_recetas.pack(side="left", padx=(0, 10), fill="x", expand=True)

        self.btn_proyecciones = ctk.CTkButton(
            bottom_frame,
            width=250,
            text="Proyecciones",
            font=self.fuente_button,
            fg_color="transparent",
            text_color="#b8191a",
            border_color="#b8191a",
            border_width=2,
            hover_color="#991416",
            corner_radius=50,
            command=self.seleccionar_proyecciones
        )
        self.btn_proyecciones.pack(side="left", fill="x", expand=True)

        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=25)

        ctk.CTkLabel(encabezado, text="Usuario", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=1, padx=(50,0), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Nombre completo", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=2, padx=(0,25), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Contraseña", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=3, padx=(0,50), sticky="nsew")
        ctk.CTkLabel(encabezado, text="Rol de acceso", text_color="#3A3A3A", font=self.fuente_small, anchor="center", justify="center").grid(row=0, column=4, padx=(0,140), sticky="nsew")
        encabezado.grid_columnconfigure((1, 2, 3, 4), weight=1)

        self.usuarios_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.usuarios_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    def seleccionar_recetas(self):
            self.btn_recetas.configure(
                fg_color="#b8191a",
                text_color="white",
                border_width=0
            )
            self.btn_proyecciones.configure(
                fg_color="transparent",
                text_color="#b8191a",
                border_color="#b8191a",
                border_width=2
            )

    def seleccionar_proyecciones(self):
        self.btn_proyecciones.configure(
            fg_color="#b8191a",
            text_color="white",
            border_width=0
        )
        self.btn_recetas.configure(
            fg_color="transparent",
            text_color="#b8191a",
            border_color="#b8191a",
            border_width=2
        )

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Basurero de Recetas")
    root.geometry("1920x10800")
    app = AdminTrashcanView(root)
    app.pack(fill="both", expand=True)
    root.mainloop()