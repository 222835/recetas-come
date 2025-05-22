
import customtkinter as ctk
from datetime import date
import os, sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.database.connector import Connector
from src.Recipes.model import Receta, Receta_Ingredientes
from src.Ingredients.model import Ingrediente
from src.Projections.controller import ProyeccionController
from src.Projections.proyecciones_resultados import ProyeccionesResultadosView

## @class PorcentajesProyeccionesView
#  @brief A view class for managing recipe percentages for projections
#
##This class creates a GUI interface that allows users to set percentage distributions
##for different recipes and generate ingredient projections based on those percentages.
##It displays recipe cards with their ingredients and allows adjusting percentage values.
class PorcentajesProyeccionesView(ctk.CTkFrame):
    ## @brief Constructor for the PorcentajesProyeccionesView class
    ##@param parent The parent widget for this frame
    ##@param recetas_ids List of recipe IDs to display (defaults to [1, 2, 3] if None)
    ##@param tipo_comida Type of meal ("Desayuno" by default)
    def __init__(self, parent, recetas_ids=None, tipo_comida="Desayuno"):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.parent = parent
        self.tipo_comida = tipo_comida
        self.recetas_ids = recetas_ids if recetas_ids else [1, 2, 3]
        self.connector = Connector()
        self.session = self.connector.get_session()
        self.recetas = []
        for receta_id in self.recetas_ids:
            receta = self.session.query(Receta).filter(Receta.id_receta == receta_id).first()
            if receta:
                self.recetas.append(receta)
        if not self.recetas:
            self.usar_datos_dummy()
        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=38, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=16, weight="bold")
        num_recetas = len(self.recetas)
        porcentaje_base = 100 // num_recetas
        self.porcentajes = {receta.id_receta: porcentaje_base for receta in self.recetas}
        if num_recetas > 0 and 100 % num_recetas != 0:
            self.porcentajes[self.recetas[0].id_receta] += 100 % num_recetas
        self.comensales = 100
        self._crear_interfaz()

    ## @brief Creates dummy recipe data when no recipes are found in the database
    #
    ##This method creates placeholder recipe objects with default values
    ##to ensure the interface can still display properly when database data
    ##is unavailable.
    def usar_datos_dummy(self):
        dummy_recetas = [
            {"id": 1, "nombre": "ARROZ BLANCO", "comensales": 100, "clasificacion": "Comida", "periodo": self.tipo_comida},
            {"id": 2, "nombre": "ARROZ BLANCO", "comensales": 100, "clasificacion": "Comida", "periodo": self.tipo_comida},
            {"id": 3, "nombre": "ARROZ BLANCO", "comensales": 100, "clasificacion": "Comida", "periodo": self.tipo_comida}
        ]
        self.recetas = []
        for i, data in enumerate(dummy_recetas[:len(self.recetas_ids)]):
            receta = Receta(
                nombre_receta=data["nombre"],
                clasificacion=data["clasificacion"],
                periodo=data["periodo"],
                comensales_base=data["comensales"],
                estatus=True
            )
            receta.id_receta = self.recetas_ids[i]
            self.recetas.append(receta)

    ## @brief Creates the main interface elements
    #
    ##This private method builds the UI layout including the scrollable container,
    ##title elements, recipe cards, and control elements for generating projections.
    def _crear_interfaz(self):
        contenedor = ctk.CTkScrollableFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)

        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 0))

        titulo = ctk.CTkLabel(
            top_frame,
            text="Proyecciones - Porcentajes",
            font=self.fuente_titulo,
            text_color="#b8191a"
        )
        titulo.pack(side="left")

        self.btn_volver = ctk.CTkButton(
            top_frame,
            text="← Volver",
            font=self.fuente_button,
            fg_color="transparent",
            text_color="#C82333",
            hover_color="#e6e6e6",
            command=self.volver_a_proyecciones
        )
        self.btn_volver.pack(side="right")



        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))

        cards_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        cards_frame.pack(pady=10)

        self.entries_porcentajes = {}

        for i, receta in enumerate(self.recetas):
            self._crear_tarjeta_receta(cards_frame, receta, i, column=i)


        bottom_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        bottom_frame.pack(pady=30)

        ctk.CTkLabel(bottom_frame, text="Comensales:", font=self.fuente_card, text_color="black").pack(side="left", padx=(0, 10))

        self.comensales_entry = ctk.CTkEntry(bottom_frame, width=100, fg_color="white", text_color="black")
        self.comensales_entry.pack(side="left")
        self.comensales_entry.insert(0, str(self.comensales))

        ctk.CTkButton(
            bottom_frame,
            text="Generar",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=8,
            command=self.actualizar_ingredientes
        ).pack(side="right", padx=10)

    ## @brief Creates a recipe card with ingredient information
    ##@param parent The parent widget for this card
    ##@param receta Recipe object containing recipe information
    ##@param index Index of the recipe in the list (used for display numbering)
    ##@param column Grid column position for layout
    #
    ##This method creates a card displaying recipe information, including
    ##its ingredients table and percentage input field.
    def _crear_tarjeta_receta(self, parent, receta, index, column):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=0, column=column, padx=20, pady=10, sticky="n")

        ctk.CTkLabel(
            wrapper,
            text=f"Receta {index + 1}",
            font=self.fuente_subtitulo,
            text_color="#b8191a"
        ).pack()

        card = ctk.CTkFrame(wrapper, fg_color="white", corner_radius=12, width=280)
        card.pack(pady=(5, 0))

        ctk.CTkLabel(
            card,
            text=receta.nombre_receta,
            font=self.fuente_card,
            text_color="black",
            wraplength=250, 
            justify="center"
        ).pack(pady=(10, 5))

        encabezado = ctk.CTkFrame(card, fg_color="transparent")
        encabezado.pack()
        ctk.CTkLabel(encabezado, text="Ingrediente", font=self.fuente_card, width=100, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Cantidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Unidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")

        tabla = ctk.CTkFrame(card, fg_color="#f5f0ed", corner_radius=5)
        tabla.pack(padx=10, pady=5)

        ingredientes = self.session.query(Receta_Ingredientes).filter_by(id_receta=receta.id_receta).all()
        for ing in ingredientes:
            ingrediente = self.session.get(Ingrediente, ing.id_ingrediente)
            if ingrediente:
                fila = ctk.CTkFrame(tabla, fg_color="transparent")
                fila.pack()
                ctk.CTkLabel(fila, text=ingrediente.nombre, font=self.fuente_card, width=100, anchor="w", text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=str(ing.cantidad), font=self.fuente_card, width=80, text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=ingrediente.unidad_medida, font=self.fuente_card, width=80, text_color="black").pack(side="left")

        vcmd = self.register(lambda P: P.isdigit() or P == "")

        entry = ctk.CTkEntry(
            card,
            width=60,
            fg_color="#f0f0f0",
            text_color="black",
            validate="key",
            validatecommand=(vcmd, '%P')
        )
        entry.pack(pady=(10, 5))
        entry.insert(0, str(self.porcentajes[receta.id_receta]))
        self.entries_porcentajes[receta.id_receta] = entry

        ctk.CTkLabel(card, text="%", font=self.fuente_card, text_color="black").pack()

    ##@brief Updates ingredient quantities based on percentages and diners count
    #
    ##This method is called when the "Generate" button is clicked.
    ##It calculates updated ingredient quantities based on the 
    ##percentage distribution and number of diners entered.
    #
    #  @note This method is currently a placeholder and needs implementation
    def actualizar_ingredientes(self):
        try:
            comensales = int(self.comensales_entry.get())
            porcentajes = {}

            for receta_id, entry in self.entries_porcentajes.items():
                valor = entry.get()
                if not valor.isdigit():
                    raise ValueError("Todos los porcentajes deben ser números enteros.")
                porcentajes[receta_id] = int(valor)

            if sum(porcentajes.values()) != 100:
                raise ValueError("La suma de los porcentajes debe ser exactamente 100.")

            self.destroy()
            resultados_view = ProyeccionesResultadosView(
                self.master,
                recetas_ids=self.recetas_ids,
                porcentajes=porcentajes,
                comensales=comensales,
                tipo_comida=self.tipo_comida
            )
            resultados_view.pack(fill="both", expand=True)

        except ValueError as e:
            error_label = ctk.CTkLabel(
                self,
                text=f"Error: {str(e)}",
                text_color="red",
                fg_color="#fff3f3",
                corner_radius=5
            )
            error_label.place(relx=0.5, rely=0.9, anchor="center")
            self.after(3000, error_label.destroy)


    def volver_a_proyecciones(self):
        from src.Projections.proyecciones_seleccion import ProyeccionesSeleccionView
        self.destroy()
        nueva_vista = ProyeccionesSeleccionView(self.master, tipo_comida=self.tipo_comida)
        nueva_vista.pack(fill="both", expand=True)



    ## @brief Saves the current projection to the database
    #
    ##This method should save the current projection configuration
    ##including percentages and diners count to the database.
    #
    ##@note This method is currently a placeholder and needs implementation
    def guardar_proyeccion(self):
        pass
