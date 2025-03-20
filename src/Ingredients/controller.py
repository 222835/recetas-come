import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Ingredients.model import Ingrediente

class IngredienteController:
    @staticmethod
    def create_ingrediente(session: Session, nombre: str, clasificacion: str, unidad_medida: str) -> Ingrediente:
        ##@brief Create a new ingredient in the database
        ##@details This method creates a new ingredient and adds it to the database
        ##@param session The SQLAlchemy session
        ##@param nombre The name of the ingredient
        ##@param clasificacion The classification of the ingredient
        ##@param unidad_medida The unit of measurement for the ingredient
        ##@return The created ingredient object
        nuevo_ingrediente = Ingrediente(
            nombre=nombre,
            clasificacion=clasificacion,
            unidad_medida=unidad_medida
        )
        session.add(nuevo_ingrediente)
        session.commit()
        return nuevo_ingrediente

    @staticmethod
    def get_ingrediente_by_id(session: Session, id_ingrediente: int) -> Ingrediente:
        ##@brief Get an ingredient by its ID from the database
        ##@details This method queries the database to retrieve the ingredient with the given ID
        ##@param session The SQLAlchemy session
        ##@param id_ingrediente The ID of the ingredient to retrieve
        ##@return The ingredient object or None if not found
        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == id_ingrediente).first()

    @staticmethod
    def update_ingrediente(session: Session, id_ingrediente: int, nombre: str = None,
                           clasificacion: str = None, unidad_medida: str = None) -> Ingrediente:
        ##@brief Update an ingredient in the database
        ##@details This method updates the ingredient details in the database
        ##@param session The SQLAlchemy session
        ##@param id_ingrediente The ID of the ingredient to update
        ##@param nombre The new name of the ingredient (optional)
        ##@param clasificacion The new classification of the ingredient (optional)
        ##@param unidad_medida The new unit of measurement for the ingredient (optional)
        ##@return The updated ingredient object or None if not found
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
        ##@brief Delete an ingredient from the database
        ##@details This method deletes an ingredient from the database using its ID
        ##@param session The SQLAlchemy session
        ##@param id_ingrediente The ID of the ingredient to delete
        ##@return True if the ingredient was deleted, False if not found
        ingrediente = IngredienteController.get_ingrediente_by_id(session, id_ingrediente)
        if ingrediente is None:
            return False
        
        session.delete(ingrediente)
        session.commit()
        return True
