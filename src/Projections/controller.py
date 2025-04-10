import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Projections.model import Proyeccion
from src.Recipes.model import Receta

## @brief Class to handle projection-related operations.
class ProyeccionController:
    
    ## @brief Create a new projection in the database.
    @staticmethod
    def create_projection(session, nombre, periodo, comensales, recetas):
        
        ## Validate minimum number of recipes
        if len(recetas) < 2:
            raise ValueError("La proyeccion debe incluir al menos 2 recetas")
        
        ## Validate percentage sum
        total_porcentaje = sum(r["porcentaje"] for r in recetas)
        if total_porcentaje != 100:
            raise ValueError(f"La suma de porcentajes debe ser 100% (actual: {total_porcentaje}%)")
        
        ##Extract recipe IDs and percentages
        recetas_ids = ",".join(str(r["id_receta"]) for r in recetas)
        porcentajes = ",".join(str(r["porcentaje"]) for r in recetas)
        
        ##Create the projection
        proyeccion = Proyeccion(
            nombre=nombre,
            periodo=periodo,
            comensales=comensales,
            recetas_ids=recetas_ids,
            porcentajes=porcentajes
        )
        
        session.add(proyeccion)
        session.commit()
        
        return proyeccion
    
    ## @brief Update a projection by its ID.
    @staticmethod
    def update_projection(session, id_proyeccion, nombre, comensales, recetas):
       
        ## Validate minimum number of recipes
        if len(recetas) < 2:
            raise ValueError("La proyeccion debe incluir al menos 2 recetas")
        
        ## Validate percentage sum
        total_porcentaje = sum(r["porcentaje"] for r in recetas)
        if total_porcentaje != 100:
            raise ValueError(f"La suma de porcentajes debe ser 100% (actual: {total_porcentaje}%)")
        
        ##Extract recipe IDs and percentages
        recetas_ids = ",".join(str(r["id_receta"]) for r in recetas)
        porcentajes = ",".join(str(r["porcentaje"]) for r in recetas)
        
        ##Update the projection
        proyeccion = session.get(Proyeccion, id_proyeccion)
        proyeccion.nombre = nombre
        proyeccion.comensales = comensales
        proyeccion.recetas_ids = recetas_ids
        proyeccion.porcentajes = porcentajes
        
        session.commit()
        
        return proyeccion
    
    ## @brief Calculate the total ingredients needed per recipe acording to projection percentages.
    @staticmethod
    def calculate_total_ingredients(session, id_proyeccion):

        ## Get the projection
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"No se encontró la proyección con ID {id_proyeccion}")
            
        ## Get the recipes and percentages
        recetas_ids = proyeccion.recetas_ids.split(',')
        porcentajes = proyeccion.porcentajes.split(',')
        
        ##Initialize the ingredients dictionary
        total_ingredientes = {}
        
        ##Calculate the ingredients for each recipe
        for i in range(len(recetas_ids)):
            receta_id = int(recetas_ids[i])
            porcentaje = float(porcentajes[i]) / 100
            
            ## Get the recipe
            receta = session.get(Receta, receta_id)
            if not receta:
                continue
                
            ## Calculate the factor based on the percentage and number of people
            factor = (proyeccion.comensales / receta.comensales_base) * porcentaje
            
            ##Process ingredients
            ##Check if ingredientes is a list (new format) or stored as comma-separated strings (old format)
            if isinstance(receta.ingredientes, list):
                ## New format: list of dictionaries
                for ing_data in receta.get_ingredientes():
                    nombre = ing_data["nombre"]
                    cantidad = float(ing_data["cantidad"]) * factor
                    unidad = ing_data["unidad"]
                    
                    if nombre in total_ingredientes:
                        ## Extract the existing quantity
                        existing_qty_str = total_ingredientes[nombre].split()[0]
                        existing_qty = float(existing_qty_str)
                        total_ingredientes[nombre] = f"{existing_qty + cantidad} {unidad}"
                    else:
                        total_ingredientes[nombre] = f"{cantidad} {unidad}"
            else:
                ## Old format with comma-separated strings
                ingredientes_lista = receta.nombre_ingrediente.split(',')
                cantidades_lista = receta.cantidad.split(',')
                unidades_lista = receta.unidad_medida.split(',')
                
                for j in range(len(ingredientes_lista)):
                    nombre = ingredientes_lista[j].strip()
                    cantidad = float(cantidades_lista[j].strip()) * factor
                    unidad = unidades_lista[j].strip()
                    
                    if nombre in total_ingredientes:
                        ## Extract the existing quantity
                        existing_qty_str = total_ingredientes[nombre].split()[0]
                        existing_qty = float(existing_qty_str)
                        total_ingredientes[nombre] = f"{existing_qty + cantidad} {unidad}"
                    else:
                        total_ingredientes[nombre] = f"{cantidad} {unidad}"
        
        return total_ingredientes