## @file basurero_admin.py
## @class AdminTrashcanView
## @brief Admin view for managing deleted recipes and projections
import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
import os, ctypes
from pathlib import Path

class AdminTrashcanView(ctk.CTkFrame):
    ## @brief Initializes the admin trashcan view
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=13)

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=25)
        self.contenedor.pack(padx=40, pady=40, fill="both", expand=True)

        top = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(10, 5))
        titulo = ctk.CTkLabel(top, text="Basurero", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        filtros = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        filtros.pack(fill="x", padx=30)
        filtros.grid_columnconfigure(0, weight=3)
        filtros.grid_columnconfigure(1, weight=1)

        self.entry_buscar = ctk.CTkEntry(
            filtros,
            placeholder_text="Buscar...",
            font=self.fuente_card,
            fg_color="#dcd1cd",
            border_color="#b8191a",
            border_width=1
        )
        self.entry_buscar.grid(row=0, column=0, sticky="ew", padx=(0, 15), pady=5)

        calendar_frame = ctk.CTkFrame(
            filtros,
            fg_color="#dcd1cd",
            corner_radius=10,
            border_color="#b8191a",
            border_width=1
        )
        calendar_frame.grid(row=0, column=1, sticky="ew", pady=5)

        self.date_entry = DateEntry(
            calendar_frame,
            width=12,
            background="#dcd1cd",
            foreground="black",
            borderwidth=0,
            font=self.fuente_card,
            date_pattern='dd/MM/yyyy'
        )
        self.date_entry.pack(fill="x", padx=5, pady=4)

        botones = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        botones.pack(fill="x", padx=30, pady=(10, 5))

        self.btn_recetas = ctk.CTkButton(
            botones, text="Recetas", font=self.fuente_button,
            fg_color="#b8191a", text_color="white", hover_color="#cccccc",
            corner_radius=50, height=40, width=200,
            command=self.seleccionar_recetas
        )
        self.btn_recetas.pack(side="left", expand=True, padx=(0, 10), fill="x")

        self.btn_proyecciones = ctk.CTkButton(
            botones, text="Proyecciones", font=self.fuente_button,
            fg_color="transparent", border_color="#b8191a", border_width=2,
            text_color="#b8191a", hover_color="#cccccc",
            corner_radius=50, height=40, width=200,
            command=self.seleccionar_proyecciones
        )
        self.btn_proyecciones.pack(side="left", expand=True, padx=(10, 0), fill="x")

        self.cards_scroll = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.cards_scroll.pack(fill="both", expand=True, padx=20, pady=10)

    ## @brief Handles "Recetas" button selection style
    def seleccionar_recetas(self):
        self.btn_recetas.configure(fg_color="#b8191a", text_color="white", border_width=0)
        self.btn_proyecciones.configure(fg_color="transparent", text_color="#b8191a", border_color="#b8191a", border_width=2)

    ## @brief Handles "Proyecciones" button selection style
    def seleccionar_proyecciones(self):
        self.btn_proyecciones.configure(fg_color="#b8191a", text_color="white", border_width=0)
        self.btn_recetas.configure(fg_color="transparent", text_color="#b8191a", border_color="#b8191a", border_width=2)

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Basurero")
    root.geometry("1280x800")
    app = AdminTrashcanView(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
