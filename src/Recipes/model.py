import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Date
from sqlalchemy.orm import relationship
from src.database.connector import Base


## @brief Recipes model class, this class is used to represent a recipe in the database
class Receta(Base): 
    __tablename__ = "recetas" 

    id_receta = Column(Integer, primary_key=True, autoincrement=True)
    nombre_receta = Column(String(100), nullable=False)
    clasificacion = Column(String(50))
    periodo = Column(String(50), nullable=False) 
    comensales_base = Column(Integer, nullable=False)
    receta_ingredientes = relationship("Receta_Ingredientes", back_populates="receta", cascade="all, delete-orphan")
    ##proyeccion_recetas = relationship("Proyeccion_Recetas", back_populates="receta", cascade="all, delete-orphan")
    estatus = Column(Boolean, default=True)  
    fecha_eliminado = Column(Date, nullable=True)

    ##@brief Constructor for the Receta class, this class is used to represent a recipe in the database
    def __init__(self, nombre_receta: str, clasificacion: str, periodo: str, comensales_base: int, estatus:bool, fecha_eliminado: Date | None = None) -> None:
        self.nombre_receta = nombre_receta
        self.clasificacion = clasificacion
        self.periodo = periodo
        self.comensales_base = comensales_base
        self.estatus = estatus
        self.fecha_eliminado = fecha_eliminado

    ## @brief Method to create a new recipe in the database
    def create(self, session) -> None:
        session.add(self)
        session.commit()
   
    ##@brief Method to update the recipe, this method is used to update the recipe in the database
    def update(self, session, nombre_receta: str | None = None, clasificacion: str | None = None, periodo: str | None = None, comensales_base: int | None = None, estatus: bool | None = None, fecha_eliminado: Date | None = None) -> None:
        if nombre_receta:
            self.nombre_receta = nombre_receta
        if clasificacion:
            self.clasificacion = clasificacion
        if periodo:
            self.periodo = periodo
        if comensales_base is not None:
            self.comensales_base = comensales_base
        if estatus is not None:
            self.estatus = estatus
        if fecha_eliminado is not None:
            self.fecha_eliminado = fecha_eliminado
        session.commit()
   
    ## @brief Method to read a recipe from the database
    def read(self, session) -> "Receta":
        return session.query(Receta).filter(Receta.id_receta == self.id_receta).first()
    
    ## @brief Method to delete a recipe from the database
    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

    ## @brief String representation of the Receta class
    def __repr__(self) -> str:
        return f"Receta: {self.nombre_receta}, Clasificacion: {self.clasificacion}, Periodo: {self.periodo}, Comensales: {self.comensales_base}, Estatus (activo): {self.estatus}, Fecha eliminada: {self.fecha_eliminado}"


class Receta_Ingredientes(Base):
    __tablename__ = 'receta_ingredientes'
    __table_args__ = {'extend_existing': True}  # Permite redefinir la tabla si ya existe
    
    id_receta = Column(Integer, ForeignKey('recetas.id_receta', ondelete='CASCADE'), primary_key=True)
    id_ingrediente = Column(Integer, ForeignKey('ingredientes.id_ingrediente', ondelete='CASCADE'), primary_key=True)
    cantidad = Column(Float, nullable=False)
    
    receta = relationship("Receta", back_populates="receta_ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="receta_ingredientes")
    
    ## @brief Constructor for the RecetaIngrediente class
    def __init__(self, id_receta: int, id_ingrediente: int, cantidad: float) -> None:
        self.id_receta = id_receta
        self.id_ingrediente = id_ingrediente
        self.cantidad = cantidad
        
    ## @brief String representation of the RecetaIngrediente class
    def __repr__(self) -> str:
        return f"RecetaIngrediente: receta_id={self.id_receta}, ingrediente_id={self.id_ingrediente}, cantidad={self.cantidad}"