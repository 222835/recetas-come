import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Ingredients.model import Ingrediente

class IngredienteController:
    @staticmethod
    def create_ingrediente(session: Session, nombre: str, clasificacion: str, unidad_medida: str) -> Ingrediente:
        ##Create a new ingredient in the database.
        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            clasificacion=clasificacion,
            unidad_medida=unidad_medida
        )
        session.add(nuevo_ingrediente)
        session.commit()
        return nuevo_ingrediente
    
    @staticmethod
    def get_ingrediente_by_name(session: Session, nombre_ingrediente: str) -> Ingrediente:
        ##Get an ingredient by its name from the database.
        return session.query(Ingrediente).filter(Ingrediente.nombre == nombre_ingrediente).first()
    
    @staticmethod
    def get_ingrediente_by_id(session: Session, id_ingrediente: int) -> Ingrediente:
        ##Get an ingredient by its ID from the database.
        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()
    
    @staticmethod
    def update_ingrediente(session: Session, id_ingrediente: int, nombre: str = None,
                           clasificacion: str = None, unidad_medida: str = None) -> Ingrediente:
        ##Update an ingredient in the database.
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

    @staticmethod
    def delete_ingrediente(session: Session, id_ingrediente: int) -> bool:
        ##Delete an ingredient from the database.
        ingrediente = IngredienteController.get_ingrediente_by_id(session, id_ingrediente)
        if ingrediente is None:
            return False
        
        session.delete(ingrediente)
        session.commit()
        return True
