import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from typing import Self
from src.Recipes.model import Receta
from src.Users.model import Usuario


Base = declarative_base()


## @brief Projection model, this class represents a projection of recipes for a user.
class Proyeccion(Base):
    __tablename__ = "Proyecciones" 

    id_proyeccion = Column(Integer, primary_key=True, autoincrement=True)
    numero_usuario = Column(Integer, ForeignKey('Usuarios.numero_usuario'), nullable=False)
    nombre = Column(String(100), nullable=False)
    periodo = Column(String(50), nullable=False)
    comensales = Column(Integer, nullable=False)

    ## Relationships
    usuario = relationship("Usuario", back_populates="proyecciones")
    recetas = relationship("Receta", secondary="Proyeccion_Recetas", back_populates="proyecciones")

    ## @brief Constructor of the Proyeccion class
    def __init__(self, numero_usuario: int, nombre: str, periodo: str, comensales: int) -> None:
        self.numero_usuario = numero_usuario
        self.nombre = nombre
        self.periodo = periodo
        self.comensales = comensales

    ## @brief Method to get the user associated with the projection
    def __repr__(self) -> str:
        return f"Proyeccion: {self.nombre}, {self.periodo}, {self.comensales} comensales"

    ## @brief Method to get the recipes associated with the projection
    def calcular_ingredientes_totales(self, session) -> dict:
        ingredientes_totales = {}

        for proy_rec in session.query(ProyeccionRecetas).filter_by(id_proyeccion=self.id_proyeccion).all():
            receta = session.query(Receta).filter_by(id_receta=proy_rec.id_receta).first()
            
            if receta:
                porcentaje = proy_rec.porcentaje / 100

                for ri in receta.ingredientes:
                    cantidad_total = ri.cantidad * porcentaje * self.comensales

                    if ri.id_ingrediente in ingredientes_totales:
                        ingredientes_totales[ri.id_ingrediente]['cantidad'] += cantidad_total
                    else:
                        ingredientes_totales[ri.id_ingrediente] = {
                            'nombre': ri.ingrediente.nombre,
                            'cantidad': cantidad_total,
                            'unidad': ri.unidad_medida
                        }

        return ingredientes_totales


## @brief Projection-Recipe association model, represents the relationship between projections and recipes with a percentage.
class ProyeccionRecetas(Base):
    __tablename__ = "Proyeccion_Recetas"

    id_proyeccion = Column(Integer, ForeignKey('Proyecciones.id_proyeccion'), primary_key=True)
    id_receta = Column(Integer, ForeignKey('Recetas.id_receta'), primary_key=True)
    porcentaje = Column(Integer, nullable=False) 

    ## Relationship
    proyeccion = relationship("Proyeccion", back_populates="recetas")
    receta = relationship("Receta", back_populates="proyecciones")

    ## @brief Constructor of the ProyeccionRecetas class
    def __init__(self, id_proyeccion: int, id_receta: int, porcentaje: int) -> None:
        self.id_proyeccion = id_proyeccion
        self.id_receta = id_receta
        self.porcentaje = porcentaje

    ## @brief Method to get the recipe associated with the projection-recipe association
    def __repr__(self) -> str:
        return f"ProyeccionRecetas: Proyeccion {self.id_proyeccion}, Receta {self.id_receta}, {self.porcentaje}%"
