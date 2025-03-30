from typing import Self
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

##@brief Base class for all models
class Ingrediente(Base):
    ##@brief Ingredient model class
    ##@details This class is used to represent an ingredient in the database
    
    __tablename__ = "Ingredientes"

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    clasificacion = Column(String(50))
    unidad_medida = Column(String(20))

    ## @brief Constructor for the ingredient class
    def __init__(self, nombre: str, clasificacion: str | None = None, unidad_medida: str | None = None) -> None:
        ##@param nombre The name of the ingredient
        ##@param clasificacion The classification of the ingredient (optional)
        ##@param unidad_medida The unit of measurement for the ingredient (optional)
    
        self.nombre = nombre
        self.clasificacion = clasificacion
        self.unidad_medida = unidad_medida

    ##@brief String representation of the ingredient class
    def __repr__(self) -> str:
        return f"Ingrediente({self.nombre}, {self.clasificacion}, {self.unidad_medida})"

    ##@brief String representation of the ingredient class for display
    def create(self, session) -> None:
        ##@brief Insert a new ingredient into the database
        ##@param session The SQLAlchemy session

        session.add(self)
        session.commit()

    ##@brief Fetch an ingredient from the database by its id
    def read(self, session) -> Self:
        ##@brief Fetch an ingredient from the database by its id
        ##@param session The SQLAlchemy session
        ##@return The ingredient object

        return session.query(Ingrediente).filter(Ingrediente.id_ingrediente == self.id_ingrediente).first()

    ##@brief Fetch all ingredients from the database
    def update(self, session, nombre: str | None = None, clasificacion: str | None = None, 
               unidad_medida: str | None = None) -> None:
        ##@brief Update an ingredient's information in the database
        ##@param session The SQLAlchemy session
        ##@param nombre The name of the ingredient (optional)
        ##@param clasificacion The classification of the ingredient (optional)
        ##@param unidad_medida The unit of measurement (optional)

        if nombre:
            self.nombre = nombre
        if clasificacion:
            self.clasificacion = clasificacion
        if unidad_medida:
            self.unidad_medida = unidad_medida
        session.commit()

    ##@brief Delete an ingredient from the database
    def delete(self, session) -> None:
        ##@brief Delete the ingredient from the database
        ##@param session The SQLAlchemy session
        session.delete(self)
        session.commit()
