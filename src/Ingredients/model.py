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

    receta_ingredientes = relationship("RecetaIngrediente", back_populates="ingrediente")

    ##@brief Constructor for the ingredient class, initializes the ingredient with a name, classification, and unit of measurement
    def __init__(self, nombre: str, clasificacion: str | None = None, unidad_medida: str | None = None) -> None:
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.unidad_medida = unidad_medida

    ##@brief Create an ingredient in database.
    def create(self, session) -> None:
        session.add(self)
        session.commit()

    ##@brief Update an ingredient in database.
    def update(self, session, nombre: str | None = None, clasificacion: str | None = None, 
               unidad_medida: str | None = None) -> None:

        if nombre:
            self.nombre = nombre
        if clasificacion:
            self.clasificacion = clasificacion
        if unidad_medida:
            self.unidad_medida = unidad_medida
        session.commit()

    ## @brief Method to read an ingredient from the database
    def read(self, session) -> "Ingrediente":
        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == self.id_ingrediente).first()
    
    ##@brief Delete an ingredient from the database.
    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

    def __repr__(self) -> str:
        return f"Ingrediente: {self.nombre}, {self.clasificacion}, {self.unidad_medida}"