import customtkinter as ctk
from PIL import Image
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Recipes.controller import RecetasController
from src.database.connector import Connector
from src.Projections.porcentajes_proyecciones import PorcentajesProyeccionesView

## @class ProyeccionesSeleccionView
## @brief Interface for selecting 2-3 recipes for projections with DB connection.
class ProyeccionesSeleccionView(ctk.CTkFrame):
    ## @brief Initializes the selection interface.
    ## @param parent The parent container for the frame.
    def __init__(self, parent, tipo_comida):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.tipo_comida = tipo_comida
        self.parent = parent
        
        self.db_connector = Connector()
        self.session = self.db_connector.get_session()

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=38, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=16, weight="bold")

        self.seleccionadas = 0 
        self.min_seleccionadas = 2
        self.max_seleccionadas = 3
        self.recetas_seleccionadas = []
        
        self.crear_ui()
        self.cargar_recetas()

    def crear_ui(self):
        contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(30, 5))

        titulo = ctk.CTkLabel(top_frame, text="Proyecciones - Selección de recetas", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")
        
        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        subtitulo = ctk.CTkLabel(contenedor, text="Seleccione 2 o 3 recetas para crear una proyección", font=self.fuente_subtitulo, text_color="black")
        subtitulo.pack(pady=(10, 20))

        filtros_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(filtros_frame, text="Tiempo:", font=self.fuente_card, text_color="black").pack(side="left", padx=(0, 5))
        ctk.CTkLabel(filtros_frame, text=self.tipo_comida, font=self.fuente_card, text_color="gray").pack(side="left", padx=(0, 20))

        self.buscador = ctk.CTkEntry(filtros_frame, placeholder_text="Buscar receta", width=240, fg_color="#dcd1cd", text_color="black", border_color="#b8191a", border_width=1)
        self.buscador.pack(side="right", padx=10)
        self.buscador.bind("<KeyRelease>", self.buscar_recetas_auto)

        self.scrollable_frame = ctk.CTkScrollableFrame(contenedor, fg_color="transparent")
        self.scrollable_frame.pack(padx=30, fill="both", expand=True)

        self.recetas_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.recetas_frame.pack(fill="both", expand=True)

        self.columnas_por_fila = 5
        for col in range(self.columnas_por_fila):
            self.recetas_frame.grid_columnconfigure(col, weight=1)


        bottom_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(10, 10), padx=30)

        self.contador = ctk.CTkLabel(
            bottom_frame, 
            text=f"Recetas seleccionadas: {self.seleccionadas}/{self.max_seleccionadas}", 
            font=self.fuente_card, 
            text_color="white", 
            fg_color="#3A3A3A", 
            corner_radius=8, 
            padx=10
        )
        self.contador.pack(side="left", padx=(0, 10))

        self.boton_siguiente = ctk.CTkButton(
            bottom_frame, 
            text="Siguiente", 
            font=self.fuente_button, 
            fg_color="#b8191a", 
            hover_color="#991416", 
            corner_radius=8, 
            state="disabled",
            command=self.siguiente
        )
        self.boton_siguiente.pack(side="right")
        
        boton_volver = ctk.CTkButton(
            bottom_frame, 
            text="Volver", 
            font=self.fuente_button, 
            fg_color="#3A3A3A", 
            hover_color="#2A2A2A", 
            corner_radius=8, 
            command=self.volver
        )
        boton_volver.pack(side="right", padx=(0, 10))



    def cargar_recetas(self):
        for widget in self.recetas_frame.winfo_children():
            widget.destroy()
        
        recetas = RecetasController.search_recipes(
            self.session, 
            periodo=self.tipo_comida
        )
        
        for index, receta in enumerate(recetas):
            self.crear_card_receta(index, receta)
            
    def crear_card_receta(self, index, receta):
        card = ctk.CTkFrame(self.recetas_frame, fg_color="white", width=150, height=160, corner_radius=12)
        card.grid(
            row=index // self.columnas_por_fila,
            column=index % self.columnas_por_fila,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        receta["seleccionada"] = False
        checkbox_var = ctk.StringVar(value="0")
        receta["checkbox_var"] = checkbox_var

        interior = ctk.CTkFrame(card, fg_color="transparent")
        interior.pack(fill="both", expand=True, padx=8, pady=8)

        checkbox_frame = ctk.CTkFrame(interior, fg_color="transparent")
        checkbox_frame.pack(fill="x")
        
        checkbox = ctk.CTkCheckBox(
            checkbox_frame,
            text="",
            font=self.fuente_card,
            fg_color="#b8191a",
            hover_color="#991416",
            variable=checkbox_var,
            onvalue="1",
            offvalue="0",
            command=lambda r=receta: self.seleccionar_receta(r)
        )
        checkbox.pack(pady=(5, 5), anchor="center", padx=(75, 0)) 
        
        ctk.CTkLabel(
            interior,
            text=receta["nombre_receta"],
            font=self.fuente_card,
            text_color="black",
            wraplength=120,
            justify="center"
        ).pack(pady=(0, 10))

        ctk.CTkLabel(interior, text="").pack(expand=True)

        ctk.CTkLabel(
            interior,
            text=f"Comensales ≈ {receta['comensales_base']}",
            font=self.fuente_card,
            text_color="gray"
        ).pack(pady=(0, 5))


    def seleccionar_receta(self, receta):
        checkbox_value = receta["checkbox_var"].get()
        
        if checkbox_value == "1":
            if len(self.recetas_seleccionadas) >= self.max_seleccionadas:
                receta["checkbox_var"].set("0")
                return
                
            self.recetas_seleccionadas.append(receta)
            self.seleccionadas += 1
        else:
            self.recetas_seleccionadas = [r for r in self.recetas_seleccionadas if r["id_receta"] != receta["id_receta"]]
            self.seleccionadas -= 1
        
        self.contador.configure(text=f"Recetas seleccionadas: {self.seleccionadas}/{self.max_seleccionadas}")
        
        if self.seleccionadas >= self.min_seleccionadas:
            self.boton_siguiente.configure(state="normal")
        else:
            self.boton_siguiente.configure(state="disabled")

    def buscar_recetas_auto(self, event=None):
        texto_busqueda = self.buscador.get()
        recetas = RecetasController.search_recipes(
            self.session, 
            nombre=texto_busqueda, 
            periodo=self.tipo_comida
        )
        
        for widget in self.recetas_frame.winfo_children():
            widget.destroy()
        
        for index, receta in enumerate(recetas):
            self.crear_card_receta(index, receta)

    def siguiente(self):
        if self.seleccionadas < self.min_seleccionadas:
            return
        
        recetas_ids = [receta["id_receta"] for receta in self.recetas_seleccionadas]

        self.destroy()
        
        nueva_vista = PorcentajesProyeccionesView(self.parent, recetas_ids=recetas_ids, tipo_comida=self.tipo_comida)
        nueva_vista.pack(fill="both", expand=True)

        
    def volver(self):
        self.destroy()  
        from src.Projections.proyecciones_admin import ProyeccionesAdminView
        nueva_vista = ProyeccionesAdminView(self.parent)
        nueva_vista.pack(fill="both", expand=True)

    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()