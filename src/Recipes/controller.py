import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Recipes.model import Receta
class RecetasController:
    
    @staticmethod
    def create_recipe(session: Session, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, ingredientes: str) -> Receta:
        ##Create a new recipe in the database.
        receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            ingredientes=ingredientes
        )
        receta.create(session)  ##Call the create method from the Receta model
        return receta

    @staticmethod
    def get_recipe_by_id(session: Session, numero_receta: int) -> Receta:
        ##Retrieve a recipe by its ID.
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        return receta

    @staticmethod
    def update_recipe(session: Session, numero_receta: int, nombre_receta: str = None, clasificacion: str = None, periodo: str = None, comensales_base: int = None, ingredientes: str = None) -> Receta:
        ##Update an existing recipe.
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        if receta:
            receta.update(session, nombre_receta, clasificacion, periodo, comensales_base, ingredientes)
        return receta

    @staticmethod
    def delete_recipe(session: Session, numero_receta: int) -> bool:
        ##Delete a recipe from the database.
        receta = session.query(Receta).filter(Receta.numero_receta == numero_receta).first()
        if receta:
            receta.delete(session)
            return True
        return False