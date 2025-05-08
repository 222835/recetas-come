import customtkinter as ctk
from PIL import Image
from pathlib import Path

## @class ProyeccionesSeleccionView
## @brief Interface for selecting 2-3 recipes for projections (design only, no DB connection).
class ProyeccionesSeleccionView(ctk.CTkFrame):
    ## @brief Initializes the selection interface.
    ## @param parent The parent container for the frame.
    def __init__(self, parent, tipo_comida):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.tipo_comida = tipo_comida

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=38, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=16, weight="bold")

        self.seleccionadas = 0 
        self.max_seleccionadas = 3 

        contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(30, 5))

        titulo = ctk.CTkLabel(top_frame, text="Proyecciones - Selección de recetas", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")
        
        linea_horizontal = ctk.CTkFrame(contenedor, height=1, width=300, fg_color="#b8191a")
        linea_horizontal.pack(fill="x", padx=30, pady=(0, 10))

        subtitulo = ctk.CTkLabel(contenedor, text="Seleccione 2 o 3 recetas para crear una proyección", font=self.fuente_subtitulo, text_color="black")
        subtitulo.pack(pady=(10, 20))

        filtros_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(filtros_frame, text="Tiempo:", font=self.fuente_card, text_color="black").pack(side="left", padx=(0, 5))
        ctk.CTkLabel(filtros_frame, text=self.tipo_comida, font=self.fuente_card, text_color="gray").pack(side="left", padx=(0, 20))

        buscador = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar receta", width=240, fg_color="white", text_color="black", border_color="#b8191a")
        buscador.pack(side="right", padx=10)

        self.recetas_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        self.recetas_frame.pack(padx=30, fill="both", expand=True)

        self.crear_cards_dummy()

        bottom_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(10, 10), padx=30)

        self.contador = ctk.CTkLabel(bottom_frame, text=f"Recetas seleccionadas: {self.seleccionadas}/{self.max_seleccionadas}", font=self.fuente_card, text_color="white", fg_color="#3A3A3A", corner_radius=8, padx=10)
        self.contador.pack(side="left", padx=(0, 10))

        boton_siguiente = ctk.CTkButton(bottom_frame, text="Siguiente", font=self.fuente_button, fg_color="#b8191a", hover_color="#991416", corner_radius=8, command=self.siguiente)
        boton_siguiente.pack(side="right")

    ## @brief Generates placeholder recipe cards (for design only).
    def crear_cards_dummy(self):
        nombres = [
            "GUISADO CON RAJAS", "GUISADO EN VERDE", "GUISADO POBLANO", "GUISADO ENTOMATADO",
            "GUISADO BBQ", "GUISADO ESTOFADO", "100", "100", "", ""
        ]
        for index, nombre in enumerate(nombres):
            card = ctk.CTkFrame(self.recetas_frame, fg_color="white", width=140, height=100, corner_radius=12)
            card.grid(row=index // 5, column=index % 5, padx=10, pady=10)
            icono = "✔️" if index in [1, 2, 5] else "⬜"
            ctk.CTkLabel(card, text=icono, font=self.fuente_card, text_color="#b8191a").pack(pady=(10, 0))
            ctk.CTkLabel(card, text=nombre if nombre else "GUISADO", font=self.fuente_card, text_color="black").pack()
            ctk.CTkLabel(card, text="Comensales ≈ 100", font=self.fuente_card, text_color="gray").pack()

            
            ctk.CTkButton(
                card,
                text="Seleccionar",
                font=self.fuente_button,
                fg_color="#b8191a",
                hover_color="#991416",
                corner_radius=8,
                command=lambda receta=nombre: self.seleccionar_receta(receta)
            ).pack(pady=(5, 10))

    ## @brief Handles recipe selection.
    def seleccionar_receta(self, receta):
        if self.seleccionadas < self.max_seleccionadas:
            self.seleccionadas += 1
            self.contador.configure(text=f"Recetas seleccionadas: {self.seleccionadas}/{self.max_seleccionadas}")
        else:
            print("No puedes seleccionar más de 3 recetas.")

    ## @brief Handles the "Siguiente" button click.
    def siguiente(self):
        print("Avanzando a la siguiente etapa...")
        # SIG vista
