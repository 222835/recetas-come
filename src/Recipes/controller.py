import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Recipes.model import Receta
from typing import List

class RecetasController:
    
    ## @brief This method creates a new recipe in the database.
    @staticmethod
    def create_recipe(session: Session, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, ingredientes: List[dict], user_role: str) -> Receta:
        ## Create a new recipe in the database.
        ## Only admin users are allowed to create recipes. 
        ## All fields are required, and the recipe must have at least one ingredient.
        
        if user_role != 'admin':
            raise PermissionError("Only administrators can create recipes.")
        
        ## Validate required fields
        if not nombre_receta or not clasificacion or not periodo or comensales_base <= 0:
            raise ValueError("Recipe name, classification, period, and base number of servings are required.")
        
        ## Validate ingredients
        if not ingredientes or len(ingredientes) == 0:
            raise ValueError("Recipe must contain at least one ingredient.")
        
        ## Ensure all ingredients have required fields
        for ingrediente in ingredientes:
            if not ingrediente.get('nombre') or not ingrediente.get('cantidad') or not ingrediente.get('unidad_medida'):
                raise ValueError("Each ingredient must have a name, quantity, and unit of measure.")
        
        receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            ingredientes=ingredientes
        )
        receta.create(session)  ## Call the create method from the Receta model
        return receta

    ## @brief This method retrieves a recipe by its ID.
    @staticmethod
    def get_recipe_by_id(session: Session, numero_receta: int) -> Receta:
        ## Retrieve a recipe by its ID.
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        return receta

    ## @brief This method retrieves all recipes from the database.
    @staticmethod
    def update_recipe(session: Session, numero_receta: int, nombre_receta: str = None, clasificacion: str = None, periodo: str = None, comensales_base: int = None, ingredientes: List[dict] = None, user_role: str = None) -> Receta:
        ## Update an existing recipe. 
        ## Only admin users are allowed to update recipes.
        
        if user_role != 'admin':
            raise PermissionError("Only administrators can update recipes.")
        
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
                    raise ValueError("Recipe must contain at least one ingredient.")
                for ingrediente in ingredientes:
                    if not ingrediente.get('nombre') or not ingrediente.get('cantidad') or not ingrediente.get('unidad_medida'):
                        raise ValueError("Each ingredient must have a name, quantity, and unit of measure.")
                receta.ingredientes = ingredientes
            receta.update(session)
        return receta

    ## @brief This method retrieves all recipes from the database.
    @staticmethod
    def delete_recipe(session: Session, numero_receta: int, user_role: str) -> bool:
        ## Delete a recipe from the database. 
        ## Only admin users are allowed to delete recipes.
        
        if user_role != 'admin':
            raise PermissionError("Only administrators can delete recipes.")
        
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        if receta:
            receta.delete(session)
            return True
        return False
