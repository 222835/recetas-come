import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Recipes.model import Receta
from typing import List

class RecetasController:
    
    ## @brief Create a new recipe in the database.
    @staticmethod
    def create_recipe(session: Session, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, ingredientes: List[dict], user_role: str) -> Receta:

        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden crear recetas.")
        ## Validate input parameters
        if not nombre_receta or not clasificacion or not periodo or comensales_base <= 0:
            raise ValueError("Los campos nombre_receta, clasificacion, periodo y comensales_base son obligatorios y deben ser válidos.")
        ## Validate ingredients
        if not ingredientes or len(ingredientes) == 0:
            raise ValueError("La receta debe contener al menos un ingrediente.")
        ## Validate each ingredient
        for ingrediente in ingredientes:
            if not ingrediente.get('nombre') or not ingrediente.get('cantidad') or not ingrediente.get('unidad_medida'):
                raise ValueError("Cada ingrediente debe tener un nombre, cantidad y unidad de medida.")
        
        receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            ingredientes=ingredientes
        )
        receta.create(session)  
        return receta

    ## @brief Retrieve a recipe by its ID.
    def get_recipe_by_id(session: Session, numero_receta: int) -> Receta:
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        return receta

    ## @brief Update a recipe in the database.
    def update_recipe(session: Session, numero_receta: int, nombre_receta: str = None, clasificacion: str = None, periodo: str = None, comensales_base: int = None, ingredientes: List[dict] = None, user_role: str = None) -> Receta:
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden actualizar recetas.")
        ## Validate input parameters
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        if receta:
            if nombre_receta:
                receta.nombre_receta = nombre_receta
            if clasificacion:
                receta.clasificacion = clasificacion
            if periodo:
                receta.periodo = periodo
            if comensales_base:
                receta.comensales_base = comensales_base
            if ingredientes:
                ## Validate ingredients
                if not ingredientes or len(ingredientes) == 0:
                    raise ValueError("La receta debe contener al menos un ingrediente.")
                for ingrediente in ingredientes:
                    if not ingrediente.get('nombre') or not ingrediente.get('cantidad') or not ingrediente.get('unidad_medida'):
                        raise ValueError("Cada ingrediente debe tener un nombre, cantidad y unidad de medida.")
                receta.ingredientes = ingredientes
            receta.update(session)
        return receta

    ## @brief Delete a recipe from the database.
    @staticmethod
    def delete_recipe(session: Session, numero_receta: int, user_role: str) -> bool:  
        ## Validate input parameters
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden eliminar recetas.")
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        if receta:
            receta.delete(session)
            return True
        return False
