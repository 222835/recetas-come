import customtkinter as ctk
from pathlib import Path
from PIL import Image
from src.Recipes.controller import RecetasController
from src.database.connector import Connector
import os
import ctypes

## @class RecetasInvView
## @brief Guest interface for viewing recipes (read-only)
class RecetasInvView(ctk.CTkFrame):
    ## @brief Initializes the guest recipe view
    ## @param parent Parent container
    def __init__(self, parent):
        self.connector = Connector()
        self.session = self.connector.get_session()
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")

        BASE_DIR = Path(__file__).resolve()
        font_path = BASE_DIR.parents[2] / "res" / "fonts" / "PortLligatSlab-Regular.ttf"
        if os.name == "nt":
            ctypes.windll.gdi32.AddFontResourceW(str(font_path))

        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=40, weight="bold")
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=18, weight="bold")
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_small = ctk.CTkFont(family="Port Lligat Slab", size=14)

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Recetas", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        busqueda_frame = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        busqueda_frame.pack(fill="x", padx=25, pady=(10, 5))

        self.input_busqueda = ctk.CTkEntry(busqueda_frame, placeholder_text="Buscar receta...", 
                                        height=35, fg_color="#dcd1cd", text_color="black", 
                                        border_color="#C82333", border_width=1)
        self.input_busqueda.pack(side="left", padx=(0, 10), fill="x", expand=True)
        self.input_busqueda.bind("<KeyRelease>", lambda e: self.cargar_recetas())

        self.filtro_tiempo = ctk.CTkComboBox(busqueda_frame, values=["Todos", "Desayuno", "Comida"],
                                     height=35, width=180, fg_color="#dcd1cd", text_color="black", 
                                     border_color="#C82333", border_width=1, command=lambda choice: self.cargar_recetas())
        self.filtro_tiempo.set("Tiempo") 
        self.filtro_tiempo.pack(side="left", padx=(0, 10))

        self.filtro_categoria = ctk.CTkComboBox(busqueda_frame, values=["Todos", "Guarnicion", "Guisado", "Antojos"],
                                                height=35, width=180, fg_color="#dcd1cd", text_color="black", 
                                                border_color="#C82333", border_width=1, command=lambda choice: self.cargar_recetas())
        self.filtro_categoria.set("Categoría")
        self.filtro_categoria.pack(side="left", padx=(0, 10))

        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=30, pady=4)

        headers = ["", "Nombre", "Ingredientes", "Cantidad", "Unidad", "Comensales", "Tiempo", "Categoría"]
        col_widths = [30, 390, 280, 120, 120, 120, 150, 150]

        for i, header in enumerate(headers):
            col_frame = ctk.CTkFrame(encabezado, width=col_widths[i], fg_color="transparent")
            col_frame.grid(row=0, column=i, sticky="ew")
            col_frame.grid_propagate(False)
            
            lbl = ctk.CTkLabel(col_frame, text=header, text_color="#3A3A3A", 
                            font=self.fuente_small, anchor="w")
            lbl.pack(side="left", fill="both", expand=True, padx=5)
            
            encabezado.grid_columnconfigure(i, weight=0, minsize=col_widths[i])

        self.recetas_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.recetas_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_recetas()

    ## @brief Loads all recipes into the scrollable frame
    def cargar_recetas(self):
        for widget in self.recetas_scroll_frame.winfo_children():
            widget.destroy()

        nombre = self.input_busqueda.get().strip()
        periodo = self.filtro_tiempo.get()
        clasificacion = self.filtro_categoria.get()

        recetas = RecetasController.search_recipes(
            self.session,
            nombre=nombre if nombre else None,
            periodo=periodo if periodo != "Todos" and periodo != "Tiempo" else None,
            clasificacion=clasificacion if clasificacion != "Todos" and clasificacion != "Categoría" else None
        )

        if not recetas:
            ctk.CTkLabel(self.recetas_scroll_frame, text="No hay recetas guardadas.", font=self.fuente_card).pack(pady=20)
            return

        for receta in recetas:
            nombres = [i["nombre_ingrediente"] for i in receta["ingredientes"]]
            cantidades = [i["Cantidad"] for i in receta["ingredientes"]]
            unidades = [i["Unidad"] for i in receta["ingredientes"]]

            self.crear_card_receta(
                receta["nombre_receta"],
                nombres,
                cantidades,
                unidades,
                receta["comensales_base"],
                receta["periodo"],
                receta["clasificacion_receta"]
            )

    ## @brief Creates a recipe card
    ## @param nombre Recipe name
    ## @param ingredientes List of ingredients
    ## @param cantidades List of quantities
    ## @param unidades List of units
    ## @param comensales Number of servings
    ## @param tiempo Meal time
    ## @param categoria Recipe category
    def crear_card_receta(self, nombre, ingredientes, cantidades, unidades, comensales, tiempo, categoria):
        card = ctk.CTkFrame(self.recetas_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)

        col_widths = [30, 300, 280, 120, 120, 120, 150, 150]

        for i, width in enumerate(col_widths):
            card.grid_columnconfigure(i, weight=0, minsize=width)
        
        nombre_frame = ctk.CTkFrame(card, width=col_widths[1], height=25, fg_color="white")
        nombre_frame.grid(row=0, column=1, sticky="w")
        nombre_frame.grid_propagate(False)
        
        nombre_label = ctk.CTkLabel(nombre_frame, text=nombre, text_color="black", 
                                    font=self.fuente_card, anchor="w", 
                                    wraplength=col_widths[1]-10)
        nombre_label.pack(side="left", fill="both", expand=True, padx=5)
        
        for idx in range(len(ingredientes)):
            if idx > 0:
                ctk.CTkFrame(card, width=col_widths[1], height=25, fg_color="white").grid(row=idx, column=1, sticky="w")
            
            
            ing_frame = ctk.CTkFrame(card, width=col_widths[2], height=25, fg_color="white")
            ing_frame.grid(row=idx, column=2, sticky="w")
            ing_frame.grid_propagate(False)
            
            ing_label = ctk.CTkLabel(ing_frame, text=ingredientes[idx], text_color="black", 
                                    font=self.fuente_card, anchor="w", 
                                    wraplength=col_widths[2]-10)
            ing_label.pack(side="left", fill="both", expand=True, padx=5)
            
            
            cant_frame = ctk.CTkFrame(card, width=col_widths[3], height=25, fg_color="white")
            cant_frame.grid(row=idx, column=3, sticky="w")
            cant_frame.grid_propagate(False)
            
            cant_label = ctk.CTkLabel(cant_frame, text=cantidades[idx], text_color="black", font=self.fuente_card, anchor="w")
            cant_label.pack(side="left", fill="both", expand=True, padx=5)
            
            unid_frame = ctk.CTkFrame(card, width=col_widths[4], height=25, fg_color="white")
            unid_frame.grid(row=idx, column=4, sticky="w")
            unid_frame.grid_propagate(False)
            
            unid_label = ctk.CTkLabel(unid_frame, text=unidades[idx], text_color="black", font=self.fuente_card, anchor="w")
            unid_label.pack(side="left", fill="both", expand=True, padx=5)
        

        com_frame = ctk.CTkFrame(card, width=col_widths[5], height=25, fg_color="white")
        com_frame.grid(row=0, column=5, sticky="w")
        com_frame.grid_propagate(False)
        
        com_label = ctk.CTkLabel(com_frame, text=str(comensales), text_color="black", font=self.fuente_card, anchor="w")
        com_label.pack(side="left", fill="both", expand=True, padx=5)
        
        tiempo_frame = ctk.CTkFrame(card, width=col_widths[6], height=25, fg_color="white")
        tiempo_frame.grid(row=0, column=6, sticky="w")
        tiempo_frame.grid_propagate(False)
        
        tiempo_label = ctk.CTkLabel(tiempo_frame, text=str(tiempo), text_color="black", font=self.fuente_card, anchor="w")
        tiempo_label.pack(side="left", fill="both", expand=True, padx=5)
        
        cat_frame = ctk.CTkFrame(card, width=col_widths[7], height=25, fg_color="white")
        cat_frame.grid(row=0, column=7, sticky="w")
        cat_frame.grid_propagate(False)
        
        cat_label = ctk.CTkLabel(cat_frame, text=str(categoria), text_color="black", font=self.fuente_card, anchor="w")
        cat_label.pack(side="left", fill="both", expand=True, padx=5)