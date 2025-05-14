import customtkinter as ctk
from datetime import date
import os, sys
from typing import Dict, List

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.database.connector import Connector
from src.Recipes.model import Receta
from src.Ingredients.model import Ingrediente
from src.Projections.controller import ProyeccionController
from src.Projections.model import Proyeccion, ProyeccionReceta
from src.Projections.historial import HistorialAdminView

## @class ProyeccionesResultadosView
#  @brief A view class for displaying projection results
#
#  This class displays the results of ingredient projections for selected recipes
#  with their percentages and allows saving the projection to history or generating a report.
class ProyeccionesResultadosView(ctk.CTkFrame):
    ## @brief Constructor for the ProyeccionesResultadosView class
    #  @param parent The parent widget for this frame
    #  @param recetas_ids List of recipe IDs included in the projection
    #  @param porcentajes Dictionary of percentages for each recipe (id_receta: percentage)
    #  @param comensales Number of diners for the projection
    #  @param tipo_comida Type of meal ("Desayuno" or "Comida")
    def __init__(self, parent, recetas_ids=None, porcentajes=None, comensales=100, tipo_comida="Desayuno"):
        super().__init__(parent)
        self.configure(fg_color="#1a1a22")
        self.parent = parent
        self.tipo_comida = tipo_comida
        self.recetas_ids = recetas_ids if recetas_ids else []
        self.porcentajes = porcentajes if porcentajes else {}
        self.comensales = comensales
        
        self.connector = Connector()
        self.session = self.connector.get_session()
        
        self.recetas = []
        for receta_id in self.recetas_ids:
            receta = self.session.query(Receta).filter(Receta.id_receta == receta_id).first()
            if receta:
                self.recetas.append(receta)
                
        # Configuración de fuentes
        self.fuente_titulo = ctk.CTkFont(family="Port Lligat Slab", size=38, weight="bold")
        self.fuente_subtitulo = ctk.CTkFont(family="Port Lligat Slab", size=22)
        self.fuente_card = ctk.CTkFont(family="Port Lligat Slab", size=15)
        self.fuente_button = ctk.CTkFont(family="Port Lligat Slab", size=16, weight="bold")
        
        # Calcular ingredientes totales
        self.total_ingredientes = self._calcular_total_ingredientes()
        
        # Crear la interfaz
        self._crear_interfaz()
    
    ## @brief Calculates the total ingredients needed for the projection
    #
    #  This method calculates the total quantity of each ingredient needed
    #  based on recipe percentages and the number of diners.
    #  @return A dictionary with ingredient names as keys and their total quantities as values
    def _calcular_total_ingredientes(self) -> Dict[str, str]:
        total_ingredientes = {}
        
        for receta in self.recetas:
            if receta.id_receta not in self.porcentajes:
                continue
                
            porcentaje = self.porcentajes[receta.id_receta]
            factor = (self.comensales / receta.comensales_base) * (porcentaje / 100)
            
            # Obtener ingredientes de la receta
            receta_ingredientes = self.session.query(Receta.receta_ingredientes).filter_by(id_receta=receta.id_receta).all()
            
            for ri in receta_ingredientes:
                ingrediente = self.session.get(Ingrediente, ri.id_ingrediente)
                if not ingrediente:
                    continue
                
                nombre = ingrediente.nombre
                cantidad = ri.cantidad * factor
                unidad = ingrediente.unidad_medida
                
                if nombre in total_ingredientes:
                    partes = total_ingredientes[nombre].split()
                    existing_qty = float(partes[0])
                    total_ingredientes[nombre] = f"{existing_qty + cantidad} {unidad}"
                else:
                    total_ingredientes[nombre] = f"{cantidad} {unidad}"
        
        return total_ingredientes
    
    ## @brief Creates the main interface
    #
    #  This method builds the scrollable UI that displays recipe cards with their ingredients
    #  and the total ingredients required for the projection.
    def _crear_interfaz(self):
        # Contenedor principal
        contenedor = ctk.CTkScrollableFrame(self, fg_color="#dcd1cd", corner_radius=20)
        contenedor.pack(padx=60, pady=40, fill="both", expand=True)
        
        # Cabecera
        top_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        top_frame.pack(fill="x", padx=30, pady=(10, 0))
        
        titulo = ctk.CTkLabel(
            top_frame,
            text="Proyecciones - Resultados",
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
            command=self.volver_a_porcentajes
        )
        self.btn_volver.pack(side="right")
        
        linea = ctk.CTkLabel(contenedor, text="─" * 200, text_color="#b8191a")
        linea.pack(fill="x", padx=30, pady=(0, 10))
        
        # Contenedor de tarjetas
        cards_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        cards_frame.pack(pady=10)
        
        # Crear tarjetas para cada receta
        for i, receta in enumerate(self.recetas):
            self._crear_tarjeta_receta(cards_frame, receta, i, column=i)
        
        # Botones de acción
        bottom_frame = ctk.CTkFrame(contenedor, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(20, 10))
        
        self.btn_generar_reporte = ctk.CTkButton(
            bottom_frame,
            text="Generar reporte",
            font=self.fuente_button,
            fg_color="#3A3A3A",
            hover_color="#2A2A2A",
            corner_radius=8,
            command=self.generar_reporte
        )
        self.btn_generar_reporte.pack(side="right", padx=10)
        
        self.btn_guardar = ctk.CTkButton(
            bottom_frame,
            text="Guardar",
            font=self.fuente_button,
            fg_color="#b8191a",
            hover_color="#991416",
            corner_radius=8,
            command=self.guardar_proyeccion
        )
        self.btn_guardar.pack(side="right")
    
    ## @brief Creates a recipe card with ingredient information
    #  @param parent The parent widget for this card
    #  @param receta Recipe object containing recipe information
    #  @param index Index of the recipe in the list (used for display numbering)
    #  @param column Grid column position for layout
    def _crear_tarjeta_receta(self, parent, receta, index, column):
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.grid(row=0, column=column, padx=20, pady=10, sticky="n")
        
        ctk.CTkLabel(
            wrapper,
            text=f"Receta {index + 1}",
            font=self.fuente_subtitulo,
            text_color="#b8191a"
        ).pack()
        
        # Tarjeta
        card = ctk.CTkFrame(wrapper, fg_color="white", corner_radius=12, width=280)
        card.pack(pady=(5, 0))
        
        # Nombre de la receta
        ctk.CTkLabel(
            card,
            text=receta.nombre_receta,
            font=self.fuente_card,
            text_color="black",
            wraplength=250,
            justify="center"
        ).pack(pady=(10, 5))
        
        # Encabezados de la tabla
        encabezado = ctk.CTkFrame(card, fg_color="transparent")
        encabezado.pack()
        ctk.CTkLabel(encabezado, text="Ingrediente", font=self.fuente_card, width=100, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Cantidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")
        ctk.CTkLabel(encabezado, text="Unidad", font=self.fuente_card, width=80, text_color="#555555").pack(side="left")
        
        # Tabla de ingredientes
        tabla = ctk.CTkFrame(card, fg_color="#f5f0ed", corner_radius=5)
        tabla.pack(padx=10, pady=5)
        
        # Mostrar ingredientes
        for ri in receta.receta_ingredientes:
            ingrediente = self.session.get(Ingrediente, ri.id_ingrediente)
            if ingrediente:
                porcentaje = self.porcentajes.get(receta.id_receta, 0)
                factor = (self.comensales / receta.comensales_base) * (porcentaje / 100)
                cantidad_ajustada = ri.cantidad * factor
                
                fila = ctk.CTkFrame(tabla, fg_color="transparent")
                fila.pack()
                ctk.CTkLabel(fila, text=ingrediente.nombre, font=self.fuente_card, width=100, anchor="w", text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=f"{cantidad_ajustada:.2f}", font=self.fuente_card, width=80, text_color="black").pack(side="left")
                ctk.CTkLabel(fila, text=ingrediente.unidad_medida, font=self.fuente_card, width=80, text_color="black").pack(side="left")
        
        # Mostrar porcentaje
        ctk.CTkLabel(
            card, 
            text=f"{self.porcentajes.get(receta.id_receta, 0)}%", 
            font=self.fuente_card, 
            text_color="black"
        ).pack(pady=5)
    
    ## @brief Saves the current projection to the database
    #
    #  This method creates a new projection in the database with the current configuration
    #  and navigates to the history view to show the saved projection.
    def guardar_proyeccion(self):
        try:
            # Preparar datos para crear la proyección
            nombre = f"Proyección {self.tipo_comida} - {date.today().strftime('%d/%m/%Y')}"
            
            # Preparar formato de recetas para el controller
            recetas_data = []
            for receta_id in self.recetas_ids:
                if receta_id in self.porcentajes:
                    recetas_data.append({
                        "id_receta": receta_id,
                        "porcentaje": self.porcentajes[receta_id]
                    })
            
            # Crear la proyección
            ProyeccionController.create_projection(
                self.session,
                nombre=nombre,
                periodo=self.tipo_comida,
                comensales=self.comensales,
                recetas=recetas_data
            )
            
            # Navegar al historial
            self.ir_a_historial()
            
        except Exception as e:
            # Mostrar error
            error_label = ctk.CTkLabel(
                self,
                text=f"Error al guardar: {str(e)}",
                text_color="red",
                fg_color="#fff3f3",
                corner_radius=5
            )
            error_label.place(relx=0.5, rely=0.9, anchor="center")
            self.after(3000, error_label.destroy)
    
    ## @brief Generates a report based on the current projection
    #
    #  This method will redirect to the report view (to be implemented later)
    def generar_reporte(self):
        # Placeholder para la implementación futura
        # Esta función se conectará con la vista de informes que agregarás después
        print("Generando reporte - Esta función se implementará después")
        
        # Ejemplo de cómo se puede guardar temporalmente y generar reporte
        # Primero guardar la proyección para tener un ID
        nombre_temp = f"Proyección Temporal {self.tipo_comida} - {date.today().strftime('%d/%m/%Y')}"
        recetas_data = []
        for receta_id in self.recetas_ids:
            if receta_id in self.porcentajes:
                recetas_data.append({
                    "id_receta": receta_id,
                    "porcentaje": self.porcentajes[receta_id]
                })
        
        proyeccion = ProyeccionController.create_projection(
            self.session,
            nombre=nombre_temp,
            periodo=self.tipo_comida,
            comensales=self.comensales,
            recetas=recetas_data
        )
        
        # Generar informe para esa proyección
        ProyeccionController.generate_projection_report(self.session, proyeccion.id_proyeccion)
        
        # Mostrar mensaje de confirmación
        mensaje = ctk.CTkLabel(
            self,
            text="Reporte generado correctamente",
            text_color="green",
            fg_color="#f0fff0",
            corner_radius=5
        )
        mensaje.place(relx=0.5, rely=0.9, anchor="center")
        self.after(3000, mensaje.destroy)
    
    ## @brief Navigate back to percentages view
    def volver_a_porcentajes(self):
        from src.Projections.porcentajes_proyecciones import PorcentajesProyeccionesView
        self.destroy()
        nueva_vista = PorcentajesProyeccionesView(self.parent, recetas_ids=self.recetas_ids, tipo_comida=self.tipo_comida)
        nueva_vista.pack(fill="both", expand=True)
    
    ## @brief Navigate to projection history view
    def ir_a_historial(self):
        self.destroy()
        historial_view = HistorialAdminView(self.parent)
        historial_view.pack(fill="both", expand=True)
    
    ## @brief Destructor to ensure database session is closed
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()