import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
from PIL import Image
from src.Recipes.controller import RecetasController
from src.database.connector import Connector
from src.Recipes.nueva_receta_admin import NuevaRecetaView
from src.Recipes.editar_receta_admin import EditarRecetaView
import os
import ctypes

## @class RecetasAdminView
## @brief Admin interface for managing recipes
class RecetasAdminView(ctk.CTkFrame):
    ## @brief Initializes the admin recipe view
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
        self.input_busqueda.bind("<KeyRelease>", lambda e: self.cargar_recetas())

        self.filtro_tiempo = ctk.CTkComboBox(busqueda_frame, values=["Todos", "Desayuno", "Comida"],
                                     height=35, width=180,fg_color="#dcd1cd", text_color="black", 
                                     border_color="#C82333", border_width=1, command=lambda choice: self.cargar_recetas())
        self.filtro_tiempo.set("Tiempo") 
        self.filtro_tiempo.pack(side="left", padx=(0, 10))

        self.filtro_categoria = ctk.CTkComboBox(busqueda_frame, values=["Todos", "Guarnicion", "Guisado", "Antojos"],
                                                height=35, width=180,fg_color="#dcd1cd", text_color="black", 
                                                border_color="#C82333", border_width=1, command=lambda choice: self.cargar_recetas())
        self.filtro_categoria.set("Categoría")
        self.filtro_categoria.pack(side="left", padx=(0, 10))

        col_widths = [30, 320, 250, 120, 120, 120, 150, 150, 80]
        
        encabezado = ctk.CTkFrame(self.contenedor, fg_color="#dcd1cd")
        encabezado.pack(fill="x", padx=30)

        headers = ["", "Nombre", "Ingredientes", "Cantidad", "Unidad", "Comensales", "Tiempo", "Categoría", ""]
        
        for i, header in enumerate(headers):
            col_frame = ctk.CTkFrame(encabezado, width=col_widths[i], fg_color="transparent")
            col_frame.grid(row=0, column=i, sticky="ew")
            col_frame.grid_propagate(False)  # Evita que el frame cambie de tamaño
            
            lbl = ctk.CTkLabel(col_frame, text=header, text_color="#3A3A3A", 
                            font=self.fuente_small, anchor="w")
            lbl.pack(side="left", fill="both", expand=True, padx=5)
            
            encabezado.grid_columnconfigure(i, weight=0, minsize=col_widths[i])
                    
        self.recetas_scroll_frame = ctk.CTkScrollableFrame(self.contenedor, fg_color="#dcd1cd", corner_radius=0)
        self.recetas_scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_recetas()

    ## @brief Opens the add new recipe view
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
                receta["id_receta"],
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
    def crear_card_receta(self, id_receta, nombre, ingredientes, cantidades, unidades, comensales, tiempo, categoria):
        card = ctk.CTkFrame(self.recetas_scroll_frame, fg_color="white", corner_radius=12)
        card.pack(fill="x", pady=8, padx=25)
        
        col_widths = [30, 250, 250, 120, 120, 120, 150, 150, 80]

        for i, width in enumerate(col_widths):
            card.grid_columnconfigure(i, weight=0, minsize=width)
        
        nombre_frame = ctk.CTkFrame(card, width=col_widths[1], height=25, fg_color="white")
        nombre_frame.grid(row=0, column=1, sticky="w")
        nombre_frame.grid_propagate(False)  # Evita que el frame cambie de tamaño
        
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
        
        acciones_frame = ctk.CTkFrame(card, fg_color="white", width=col_widths[8], height=25)
        acciones_frame.grid(row=0, column=8, sticky="e")
        
        btn_editar = ctk.CTkButton(
            acciones_frame, image=self.img_pen, text="", width=30, height=30,
            fg_color="white", hover_color="#E8E8E8", corner_radius=5,
            command=lambda: self.abrir_editar_receta(id_receta)
        )
        btn_editar.pack(side="left", padx=(5, 2))

        btn_eliminar = ctk.CTkButton(
            acciones_frame,
            image=self.img_bote,
            text="", width=30, height=30,
            fg_color="white", hover_color="#E8E8E8", corner_radius=5,
            command=lambda rid=id_receta, card=card: self.confirmar_eliminacion(rid, card)
        )
        btn_eliminar.pack(side="left", padx=2)

    ## @brief Handles recipe edit action
    def abrir_editar_receta(self, id_receta):
        self.session.close()
        for widget in self.winfo_children():
            widget.destroy()
        editar_view = EditarRecetaView(self, id_receta, self.fuente_titulo, self.fuente_button, self.fuente_card)
        editar_view.pack(fill="both", expand=True)

    ## @brief Confirms and deletes a recipe
    ## @param id_receta Recipe ID
    ## @param card_widget Widget to destroy
    def confirmar_eliminacion(self, id_receta, card_widget):
        if RecetasController.recipe_in_projection(self.session, id_receta):
            self.mostrar_error("No se puede eliminar \nLa receta está siendo utilizada en una proyección activa.")
            return
        
        ventana_confirmacion = ctk.CTkToplevel(self)
        ventana_confirmacion.title("Confirmar eliminación")
        ventana_confirmacion.geometry("400x180")
        ventana_confirmacion.configure(fg_color="#dcd1cd")
        ventana_confirmacion.resizable(False, False)
        ventana_confirmacion.grab_set()  

        label = ctk.CTkLabel(
            ventana_confirmacion,
            text="¿Deseas eliminar esta receta?",
            font=self.fuente_card,
            text_color="#1a1a22"
        )
        label.pack(pady=(30, 10))

        frame_botones = ctk.CTkFrame(ventana_confirmacion, fg_color="transparent")
        frame_botones.pack(pady=10)

        def confirmar():
            try:
                success = RecetasController.deactivate_recipe(self.session, id_receta)
                if success:
                    card_widget.destroy()
                    print(f"Receta eliminada con ID: {id_receta}")
                else:
                    self.mostrar_error("No se encontró la receta para eliminar.")
            except Exception as e:
                self.mostrar_error(f"No se pudo eliminar la receta.\n{e}")
            ventana_confirmacion.destroy()

        def cancelar():
            ventana_confirmacion.destroy()

        btn_si = ctk.CTkButton(
            frame_botones, text="Sí", width=80,
            font=self.fuente_button,
            fg_color="#b8191a", hover_color="#991416",
            corner_radius=10, command=confirmar
        )
        btn_si.pack(side="left", padx=10)

        btn_no = ctk.CTkButton(
            frame_botones, text="No", width=80,
            font=self.fuente_button,
            fg_color="#6c757d", hover_color="#5a6268",
            corner_radius=10, command=cancelar
        )
        btn_no.pack(side="left", padx=10)
        
    ## @brief Shows an error message
    ## @param mensaje Error message to display
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)