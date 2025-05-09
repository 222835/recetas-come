import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import date

class HistorialAdminView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=16)

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Historial", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        top_search_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_search_frame.pack(padx=60, pady=(10, 10), anchor="center")

        self.search_entry = ctk.CTkEntry(
            top_search_frame,
            placeholder_text="Buscar",
            width=400,
            height=30,
            fg_color="#dcd1cd",
            border_color="#b8191a",
            border_width=1,
            text_color="#3A3A3A",
            placeholder_text_color="#3A3A3A",
            font=self.fuente_small
        )
        self.search_entry.pack(side="left", padx=(0, 20))

        self.sort_option = ctk.CTkOptionMenu(
            top_search_frame,
            values=["Reporte", "Proyección"],
            fg_color="#dcd1cd",
            button_color="#b8191a",
            button_hover_color="#991416",
            text_color="#3A3A3A",
            dropdown_fg_color="#dcd1cd",
            dropdown_text_color="#3A3A3A",
            font=self.fuente_small,
            dropdown_font=self.fuente_small
        )
        self.sort_option.set("Reporte/Proyección")
        self.sort_option.pack(side="left", padx=(0, 20))

        self.fecha_frame = ctk.CTkFrame(top_search_frame, fg_color="transparent")
        self.fecha_frame.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            self.fecha_frame,
            text="Fecha: ",
            font=self.fuente_small,
            text_color="#3A3A3A"
        ).pack(side="left", padx=(0, 8))  

        self.date_picker = DateEntry(
            self.fecha_frame,
            font=("Port Lligat Slab", 11),
            background="#F4F4F4",
            foreground="black",
            readonlybackground="#F4F4F4",  
            borderwidth=0,
            relief="flat",
            highlightthickness=0,
            state="readonly",
            date_pattern="yyyy-mm-dd",
            width=12
        )
        self.date_picker.set_date(date.today())
        self.date_picker.pack(side="left")

        self.historial_scroll = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd")
        self.historial_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        self.mostrar_proyecciones()

    def mostrar_proyecciones(self):
        pass

    def crear_card_historial(self, titulo, datos, fecha_str):
        card = ctk.CTkFrame(self.historial_scroll, fg_color="white", corner_radius=10)
        card.pack(fill="x", pady=10, padx=30)

        ctk.CTkLabel(card, text=titulo, font=self.fuente_card, text_color="#b8191a", anchor="w").pack(anchor="w", padx=20, pady=(10, 0))
        ctk.CTkLabel(card, text=f"📅 Fecha: {fecha_str}", font=self.fuente_small, text_color="gray", anchor="w").pack(anchor="w", padx=20, pady=(0, 5))

        for nombre, porcentaje in datos.items():
            ctk.CTkLabel(card, text=f"{nombre} {porcentaje}", font=self.fuente_card, text_color="black", anchor="w").pack(anchor="w", padx=40, pady=(0, 2))
