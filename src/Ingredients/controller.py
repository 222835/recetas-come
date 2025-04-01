import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Ingredients.model import Ingrediente

## @brief This class is responsible for managing the ingredients in the database
class IngredienteController:
    ##Create a new ingredient in the database.
    @staticmethod
    def create_ingrediente(session: Session, nombre: str, clasificacion: str, unidad_medida: str) -> Ingrediente:
       
        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            clasificacion=clasificacion,
            unidad_medida=unidad_medida
        )
        session.add(nuevo_ingrediente)
        session.commit()
        return nuevo_ingrediente
    
    ##Get an ingredient by its name from the database.
    @staticmethod
    def get_ingrediente_by_name(session: Session, nombre_ingrediente: str) -> Ingrediente:
        return session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()
    
    ##Get an ingredient by its ID from the database.
    @staticmethod
    def get_ingrediente_by_id(session: Session, id_ingrediente: int) -> Ingrediente:
        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
    
    ##Update an ingredient in the database.
    @staticmethod
    def update_ingrediente(session: Session, id_ingrediente: int, nombre: str = None, clasificacion: str = None, unidad_medida: str = None) -> Ingrediente:
        
        ingrediente = IngredienteController.get_ingrediente_by_id(session, id_ingrediente)
        if ingrediente is None:
            return None

        if nombre:
            ingrediente.nombre = nombre
        if clasificacion:
            ingrediente.clasificacion = clasificacion
        if unidad_medida:
            ingrediente.unidad_medida = unidad_medida
        
        session.commit()
        return ingrediente

    ##Delete an ingredient from the database.
    @staticmethod
    def delete_ingrediente(session: Session, id_ingrediente: int) -> bool:
        ingrediente = IngredienteController.get_ingrediente_by_id(session, id_ingrediente)
        if ingrediente is None:
            return False
        
        session.delete(ingrediente)
        session.commit()
        return True
