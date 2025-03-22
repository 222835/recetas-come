import sys
import os

##Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Recipes.model import Receta
from src.Ingredients.model import Ingrediente
from sqlalchemy.orm import Session

class RecetaController:
    @staticmethod
    def create_receta(session: Session, nombre_receta: str, clasificacion: str, periodo: str,comensales_base: int, ingredientes: list) -> Receta:
        ##Create a new recipe in the database.
        print(f"Creating recipe: {nombre_receta}, {clasificacion}, {periodo}, {comensales_base}, {ingredientes}")
        
        nueva_receta = Receta(
            nombre_receta=nombre_receta,
            clasificacion=clasificacion,
            periodo=periodo,
            comensales_base=comensales_base,
            ingredientes=",".join(ingredientes)
        )
        
        session.add(nueva_receta)
        session.commit()
        print(f"Recipe created with ID: {nueva_receta.id_receta}")
        
        return nueva_receta

    @staticmethod
    def get_receta_by_id(session: Session, id_receta: int) -> Receta:
        ##Get a recipe by its ID.
        print(f"Getting recipe by ID: {id_receta}")
        receta = session.query(Receta).filter(Receta.id_receta == id_receta).first()
        
        if receta:
            print(f"Found recipe: {receta.nombre_receta}, {receta.clasificacion}, {receta.periodo}, {receta.comensales_base}")
        else:
            print("Recipe not found.")
        
        return receta

    @staticmethod
    def update_receta(session: Session, id_receta: int, nombre_receta: str = None, clasificacion: str = None,
                      periodo: str = None, comensales_base: int = None, ingredientes: list = None) -> Receta:
        ##Update an existing recipe.
        print(f"Updating recipe with ID: {id_receta}")
        
        receta = RecetaController.get_receta_by_id(session, id_receta)
        if receta is None:
            return None

        if nombre_receta:
            receta.nombre_receta = nombre_receta
        if clasificacion:
            receta.clasificacion = clasificacion
        if periodo:
            receta.periodo = periodo
        if comensales_base:
            receta.comensales_base = comensales_base
        if ingredientes:
            receta.ingredientes = ",".join(ingredientes)
        
        session.commit()
        print(f"Recipe updated: {receta.nombre_receta}")
        return receta

    @staticmethod
    def delete_receta(session: Session, id_receta: int) -> bool:
        ##Delete a recipe from the database.
        print(f"Deleting recipe with ID: {id_receta}")
        
        receta = RecetaController.get_receta_by_id(session, id_receta)
        if receta is None:
            return False
        
        session.delete(receta)
        session.commit()
        print(f"Recipe with ID {id_receta} deleted.")
        return True