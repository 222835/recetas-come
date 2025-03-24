from typing import Self
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Proyeccion(Base):
    ## @brief Projections model class
    ## @details This class is used to represent a projection in the database

    __tablename__ = "Proyecciones" 

    id_proyeccion = Column(Integer, primary_key=True, autoincrement=True)
    numero_usuario = Column(Integer, ForeignKey('Usuarios.numero_usuario'), nullable=False)
    nombre = Column(String(100), nullable=False)
    periodo = Column(String(50), nullable=False)
    comensales = Column(Integer, nullable=False)

    usuario = relationship("Usuario", back_populates="proyecciones")

    recetas= relationship("Receta", secondary="Proyeccion_Recetas")

    def __init__(self, numero_usuario: int, nombre: str, periodo: str, comensales: int) -> None:
        ##@brief Constructor
        ##@param numero_usuario The user's ID
        ##@param nombre_proyeccion The name of the projection
        ##@param periodo The period when the projection is scheduled
        ##@param comensales The number of people the projection is for
        
        self.numero_usuario = numero_usuario
        self.nombre = nombre
        self.periodo = periodo
        self.comensales = comensales

    def __repr__(self) -> str:
        return f"Proyeccion: {self.nombre}, {self.periodo}, {self.comensales} comensales"
    
    def create(self, session) -> None:
        ##@brief Create a new projection in the database
        session.add(self)
        session.commit()
    
    def read(self, session) -> "Proyeccion":
        ##@brief Read a projection from the database
        return session.query(Proyeccion).filter(Proyeccion.id_proyeccion == self.id_proyeccion).first()
    
    def update(self, session, nombre: str | None = None, periodo: str | None = None, comensales: int | None = None) -> None:
        ##@brief Update the projection details
        if nombre:
            self.nombre = nombre
        if periodo:
            self.periodo = periodo
        if comensales:
            self.comensales = comensales
    
    def delete(self, session) -> None:
        ##@brief Delete the projection from the database
        session.delete(self)
        session.commit()
    
class ProyeccionRecetas (Base):
    ##@brief Projections-Recipes model class
    ##@details This class is used to represent the relationship between projections and recipes in the database

    __tablename__ = "Proyeccion_Recetas"

    id_proyeccion = Column(Integer, ForeignKey('Proyecciones.id_proyeccion'), primary_key=True)
    id_receta = Column(Integer, ForeignKey('Recetas.id_receta'), primary_key=True)
    porcentaje = Column(DECIMAL, nullable=False)

    proyeccion = relationship("Proyeccion", back_populates="recetas")
    receta = relationship("Receta", back_populates="proyecciones")

    def __init__(self, id_proyeccion: int, id_receta: int, porcentaje: float) -> None:
        ##@brief Constructor
        ##@param id_proyeccion The ID of the projection
        ##@param id_receta The ID of the recipe
        ##@param porcentaje The percentage of the recipe to be used in the projection

        self.id_proyeccion = id_proyeccion
        self.id_receta = id_receta
        self.porcentaje = porcentaje

    def __repr__(self) -> str:
        return f"ProyeccionRecetas: {self.id_proyeccion}, {self.id_receta}, {self.porcentaje}"
    