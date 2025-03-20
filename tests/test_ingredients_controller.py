from sqlalchemy.orm import Session
import sys
import os

## Add the project root to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Ingredients.model import Ingrediente
class IngredienteController:
    
    @staticmethod
    def create_ingrediente(session: Session, nombre: str, clasificacion: str, unidad_medida: str) -> Ingrediente:
        ##@brief Create a new Ingrediente in the database
        ##@details This method adds a new ingredient to the database with the provided information
        ##@param session The SQLAlchemy session
        ##@param nombre The name of the ingredient
        ##@param clasificacion The classification of the ingredient (e.g., vegetable, fruit)
        ##@param unidad_medida The unit of measurement for the ingredient (e.g., kg, g)
        ##@return The created Ingrediente object
        
        new_ingrediente = Ingrediente(nombre=nombre, clasificacion=clasificacion, unidad_medida=unidad_medida)
        session.add(new_ingrediente)
        session.commit()
        return new_ingrediente

    @staticmethod
    def get_ingrediente_by_name(session: Session, nombre: str) -> Ingrediente:
        ##@brief Retrieve an Ingrediente by its name from the database
        ##@details This method retrieves an ingredient from the database by searching for its name
        ##@param session The SQLAlchemy session
        ##@param nombre The name of the ingredient to search for
        ##@return The Ingrediente object if found, otherwise None
        
        return session.query(Ingrediente).filter_by(nombre=nombre).first()

    @staticmethod
    def update_ingrediente(session: Session, ingrediente_id: int, nombre: str, clasificacion: str, unidad_medida: str) -> Ingrediente:
        ##@brief Update an existing Ingrediente's information
        ##@details This method updates the details of an existing ingredient in the database
        ##@param session The SQLAlchemy session
        ##@param ingrediente_id The ID of the ingrediente to update
        ##@param nombre The new name for the ingredient
        ##@param clasificacion The new classification for the ingredient
        ##@param unidad_medida The new unit of measurement for the ingredient
        ##@return The updated Ingrediente object
        
        ingrediente = session.query(Ingrediente).filter_by(id_ingrediente=ingrediente_id).first()
        if ingrediente:
            ingrediente.nombre = nombre
            ingrediente.clasificacion = clasificacion
            ingrediente.unidad_medida = unidad_medida
            session.commit()
        return ingrediente

    @staticmethod
    def delete_ingrediente(session: Session, ingrediente_id: int) -> None:
        ##@brief Delete an Ingrediente from the database
        ##@details This method removes an ingredient from the database by its ID
        ##@param session The SQLAlchemy session
        ##@param ingrediente_id The ID of the ingredient to delete
        ##@return None
    
        ingrediente = session.query(Ingrediente).filter_by(id_ingrediente=ingrediente_id).first()
        if ingrediente:
            session.delete(ingrediente)
            session.commit()
