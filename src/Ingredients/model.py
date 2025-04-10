import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from typing import Self
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.connector import Base

##@brief Base class for all models, this class is used to represent an ingredient in the database
class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    clasificacion = Column(String(50))
    unidad_medida = Column(String(20), nullable=False)

    receta_ingredientes = relationship("RecetaIngrediente", back_populates="ingrediente", cascade="all, delete-orphan")

    ##@brief Constructor for the ingredient class, initializes the ingredient with a name, classification, and unit of measurement
    def __init__(self, nombre: str, clasificacion: str | None = None, unidad_medida: str | None = None) -> None:
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.unidad_medida = unidad_medida

    ##@brief String representation of the ingredient class, this is used for debugging and logging purposes
    def __repr__(self) -> str:
        return f"Ingrediente({self.nombre}, {self.clasificacion}, {self.unidad_medida})"

    ##@brief String representation of the ingredient class for display, this is used for debugging and logging purposes
    def create(self, session) -> None:
        session.add(self)
        session.commit()

    ##@brief Fetch an ingredient from the database by its id, this is used for debugging and logging purposes
    def read(self, session) -> Self:
        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == self.id_ingrediente).first()

    ##@brief Fetch all ingredients from the database, this is used for debugging and logging purposes
    def update(self, session, nombre: str | None = None, clasificacion: str | None = None, 
               unidad_medida: str | None = None) -> None:

        if nombre:
            self.nombre = nombre
        if clasificacion:
            self.clasificacion = clasificacion
        if unidad_medida:
            self.unidad_medida = unidad_medida
        session.commit()

    ##@brief Delete an ingredient from the database, this is used for debugging and logging purposes
    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

##@brief Import the RecetaIngrediente class for the relationship between ingredients and recipes
##Placed at the end to avoid circular import issues
from src.RecetaIngredientes.Receta_ingredientes import RecetaIngrediente
