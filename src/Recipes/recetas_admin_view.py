import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from PIL import Image
from src.Recipes.controller import RecetasController
from src.database.connector import Connector
from src.Recipes.nueva_receta_admin import NuevaRecetaView
import os
import ctypes

class RecetasAdminView(ctk.CTkFrame):
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

        icono_pen_path = BASE_DIR.parents[2] / "res" / "images" / "pen 1.png"
        icono_bote_path = BASE_DIR.parents[2] / "res" / "images" / "bote.png"
        icono_add_path = BASE_DIR.parents[2] / "res" / "images" / "add_circle.png"

        self.img_pen = ctk.CTkImage(Image.open(icono_pen_path), size=(20, 20))
        self.img_bote = ctk.CTkImage(Image.open(icono_bote_path), size=(20, 20))
        self.img_add = ctk.CTkImage(Image.open(icono_add_path), size=(20, 20))

        self.contenedor = ctk.CTkFrame(self, fg_color="#dcd1cd", corner_radius=20)
        self.contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(self.contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(20, 0))

        titulo = ctk.CTkLabel(top_frame, text="Recetas", font=self.fuente_titulo, text_color="#b8191a")
        titulo.pack(side="left")

        btn_agregar = ctk.CTkButton(top_frame, image=self.img_add, text="Agregar nueva receta", font=self.fuente_button,
                                     fg_color="#b8191a", hover_color="#991416", corner_radius=50, compound="left", command=self.abrir_vista_nueva_receta)
        btn_agregar.pack(side="right")

        linea = ctk.CTkLabel(self.contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(10, 5))

        busqueda_frame = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        busqueda_frame.pack(fill="x", padx=25, pady=(10, 5))

        self.input_busqueda = ctk.CTkEntry(busqueda_frame, placeholder_text="Buscar receta...", 
                                        height=35, fg_color="#dcd1cd", text_color="black", 
                                        border_color="#C82333", border_width=1)
        self.input_busqueda.pack(side="left", padx=(0, 10), fill="x", expand=True)

        self.filtro_tiempo = ctk.CTkComboBox(busqueda_frame, values=["TODOS", "DESAYUNO", "COMIDA"],
                                     height=35, fg_color="#dcd1cd", text_color="black", 
                                     border_color="#C82333", border_width=1)
        self.filtro_tiempo.set("Tiempo") 
        self.filtro_tiempo.pack(side="left", padx=(0, 10))

        self.filtro_categoria = ctk.CTkComboBox(busqueda_frame, values=["TODOS", "GUARNICION", "GUISADO", "ANTOJOS"],
                                                height=35, fg_color="#dcd1cd", text_color="black", 
                                                border_color="#C82333", border_width=1)
        self.filtro_categoria.set("Categoría")
        self.filtro_categoria.pack(side="left", padx=(0, 10))

        btn_buscar = ctk.CTkButton(busqueda_frame, text="Buscar", font=self.fuente_card,
                                fg_color="#b8191a", hover_color="#991416", corner_radius=8,
                                command=self.filtrar_recetas)
        btn_buscar.pack(side="left")

        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=25)

        headers = ["Nombre", "Ingredientes", "Cantidad", "Unidad", "Comensales", "Tiempo", "Categoría"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(encabezado, text=h, text_color="#3A3A3A", font=self.fuente_small).grid(row=0, column=i, padx=10, sticky="w")
        encabezado.grid_columnconfigure(tuple(range(len(headers))), weight=1)

        self.recetas_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.recetas_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_recetas()

    def filtrar_recetas(self):
        texto = self.input_busqueda.get().lower()
        tiempo = self.filtro_tiempo.get().upper()
        categoria = self.filtro_categoria.get().upper()

        recetas = RecetasController.list_all_recipes_with_ingredients(self.session)

        if tiempo != "TODOS":
            recetas = [r for r in recetas if r["periodo"].upper() == tiempo]

        if categoria != "TODOS":
            recetas = [r for r in recetas if r["clasificacion_receta"].upper() == categoria]

        recetas_filtradas = [r for r in recetas if texto in r["nombre_receta"].lower()]

        for widget in self.recetas_scroll_frame.winfo_children():
            widget.destroy()

        if not recetas_filtradas:
            ctk.CTkLabel(self.recetas_scroll_frame, text="No se encontraron coincidencias.", font=self.fuente_card).pack(pady=20)
            return

        for receta in recetas_filtradas:
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

    def abrir_vista_nueva_receta(self):
        self.session.close()  
        for widget in self.winfo_children():
            widget.destroy()

        nueva_vista = NuevaRecetaView(
            master=self,
            fuente_titulo=self.fuente_titulo,
            fuente_button=self.fuente_button,
            fuente_card=self.fuente_card
        )
        nueva_vista.pack(fill="both", expand=True)

    def cargar_recetas(self):
        for widget in self.recetas_scroll_frame.winfo_children():
            widget.destroy()

        recetas = RecetasController.list_all_recipes_with_ingredients(self.session)

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


    def crear_card_receta(self, nombre, ingredientes, cantidades, unidades, comensales, tiempo, categoria):
        card = ctk.CTkFrame(self.recetas_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)

        ctk.CTkLabel(card, text=nombre, text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=0, padx=10, sticky="w")
        ctk.CTkLabel(card, text=str(comensales), text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=4, padx=10, sticky="w")
        ctk.CTkLabel(card, text=str(tiempo), text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=5, padx=10, sticky="w")
        ctk.CTkLabel(card, text=str(categoria), text_color="black", font=self.fuente_card, anchor="w").grid(row=0, column=6, padx=10, sticky="w")

        btn_editar = ctk.CTkButton(card, image=self.img_pen, text="", width=30, height=40,
                                fg_color="white", hover_color="#E8E8E8", corner_radius=5,
                                command=lambda: self.editar_receta(nombre))
        btn_editar.grid(row=0, column=7, padx=5)

        btn_eliminar = ctk.CTkButton(card, image=self.img_bote, text="", width=28, height=35,
                                    fg_color="white", hover_color="#E8E8E8", corner_radius=5,
                                    command=lambda: self.confirmar_eliminacion(nombre, card))
        btn_eliminar.grid(row=0, column=8, padx=5)

        for idx in range(len(ingredientes)):
            ctk.CTkLabel(card, text=ingredientes[idx], text_color="black", font=self.fuente_card, anchor="w").grid(row=idx + 1, column=1, padx=10, sticky="w")
            ctk.CTkLabel(card, text=cantidades[idx], text_color="black", font=self.fuente_card, anchor="w").grid(row=idx + 1, column=2, padx=10, sticky="w")
            ctk.CTkLabel(card, text=unidades[idx], text_color="black", font=self.fuente_card, anchor="w").grid(row=idx + 1, column=3, padx=10, sticky="w")

        card.grid_columnconfigure(tuple(range(9)), weight=1)


    def editar_receta(self, nombre_receta):
        print(f"Editar receta: {nombre_receta}")

    def confirmar_eliminacion(self, nombre_receta, card_widget):
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Deseas eliminar la receta '{nombre_receta}'?")
        if confirm:
            card_widget.destroy()
            print(f"Receta eliminada: {nombre_receta}")
