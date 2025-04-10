import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Recipes.model import Receta
from RecetaIngredientes.Receta_ingredientes import RecetaIngrediente
from src.Ingredients.model import Ingrediente
from src.database.connector import Base

class RecetasController:
    
    ## @brief This method creates a new recipe in the database, this method is static and does not require an instance of the class to be called.
    @staticmethod
    def create_recipe(session: Session, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, user_role: str) -> Receta:
        
        ## Create a new recipe in the database.
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden crear recetas.")
        ## Validate input parameters
        if not nombre_receta or not clasificacion or not periodo or comensales_base <= 0:
            raise ValueError("Los campos nombre_receta, clasificacion, periodo y comensales_base son obligatorios y deben ser válidos.")
        ## Validate ingredients.
        if not Ingrediente or len(Ingrediente) == 0:
            raise ValueError("La receta debe contener al menos un ingrediente.")
        
        receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            ingrediente=Ingrediente
        )
        session.add(receta)
        session.flush() ## the id of the recipe before commit

        for ing in Ingrediente:
            if not ing.get('id') or not ing.get('cantidad') or not ing.get('unidad'):
                raise ValueError("Cada ingrediente debe tener id, cantidad y unidad.")

            ingrediente_db = session.query(Ingrediente).filter_by(id_ingrediente=ing['id']).first()
            if not ingrediente_db:
                raise ValueError(f"Ingrediente con id {ing['id']} no encontrado.")

            receta_ingrediente = RecetaIngrediente(
                id_receta=receta.id_receta,
                id_ingrediente= ingrediente_db.id_ingrediente,
                cantidad=ing['cantidad'],
                unidad=ing['unidad']
            )
            session.add(receta_ingrediente)

        session.commit()
        return receta
    
    ## @brief This method retrieves a recipe by its ID. This method is static and does not require an instance of the class to be called.
    @staticmethod
    def get_recipe_by_id(session: Session, numero_receta: int) -> Receta:
        receta = session.query(Receta).filter(Receta.id_receta == numero_receta).first()
        return receta

    ## @brief This method retrieves all recipes from the database. This method is static and does not require an instance of the class to be called.
    @staticmethod
    def update_recipe(session: Session, numero_receta: int, nombre_receta: str = None, clasificacion: str = None, periodo: str = None, comensales_base: int = None, user_role: str = None) -> Receta:
        ## Update a recipe in the database.
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden actualizar recetas.")
        ## Validate input parameters
        receta = session.query(Receta).filter(Receta.id_receta == numero_receta).first()
        if receta:
            if nombre_receta:
                receta.nombre_receta = nombre_receta
            if clasificacion:
                receta.clasificacion = clasificacion
            if periodo:
                receta.periodo = periodo
            if comensales_base:
                receta.comensales_base = comensales_base
            if Ingrediente:
                ## Validate ingredients
                if not Ingrediente or len(Ingrediente) == 0:
                    raise ValueError("La receta debe contener al menos un ingrediente.")
                for ingrediente in Ingrediente:
                    if not ingrediente.get('nombre') or not ingrediente.get('cantidad') or not ingrediente.get('unidad_medida'):
                        raise ValueError("Cada ingrediente debe tener un nombre, cantidad y unidad de medida.")
            
            receta_ingrediente = RecetaIngrediente(
                id_receta=numero_receta,
                id_ingrediente=Base.id_ingrediente,
                cantidad=['cantidad'],
                unidad=['unidad']
            )
            session.add(receta_ingrediente)

        session.commit()
        return receta

    ## @brief This method retrieves all recipes from the database. This method is static and does not require an instance of the class to be called.
    @staticmethod
    def delete_recipe(session: Session, numero_receta: int, user_role: str) -> bool:
        ## Delete a recipe from the database.        
        if user_role != 'admin':
            raise PermissionError("Solo los administradores pueden eliminar recetas.")
        ## Validate input parameters
        receta = session.query(Receta).filter(Receta.id_receta == numero_receta).first()
        if receta:
            receta.delete(session)
            return True
        return False
