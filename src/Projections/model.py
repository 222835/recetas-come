import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.Recipes.model import Receta
from src.Users.model import Usuario

Base = declarative_base()

## @brief Proyecciones model class, which represents the Proyecciones table in the database.
class Proyeccion(Base):
    __tablename__ = "Proyecciones"
    __table_args__ = {'extend_existing': True}

    id_proyeccion = Column(Integer, primary_key=True)
    numero_usuario = Column(Integer, ForeignKey(Usuario.numero_usuario), nullable=False)
    nombre = Column(String(100), nullable=False)
    periodo = Column(String(50), nullable=False)
    comensales = Column(Integer, nullable=False)

    recetas = relationship("ProyeccionRecetas", back_populates="proyeccion", cascade="all, delete-orphan")  

    def __init__(self, numero_usuario: int, nombre: str, periodo: str, comensales: int) -> None:
        self.numero_usuario = numero_usuario
        self.nombre = nombre
        self.periodo = periodo
        self.comensales = comensales

    def __repr__(self) -> str:
        return f"Proyeccion: {self.nombre}, {self.periodo}, {self.comensales} comensales"

    ## @brief Calculate total ingredients needed for the projection
    def calcular_ingredientes_totales(self, session) -> dict:
        ingredientes_totales = {}

        for proy_rec in self.recetas:
            receta = session.query(Receta).filter_by(numero_receta=proy_rec.id_receta).first()

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


## @brief ProyeccionRecetas model class (intermediate table for many-to-many relationship)
class ProyeccionRecetas(Base):
    __tablename__ = "ProyeccionesRecetas"
    __table_args__ = {'extend_existing': True}

    id_proyeccion_receta = Column(Integer, primary_key=True)
    id_proyeccion = Column(Integer, ForeignKey('Proyecciones.id_proyeccion'), nullable=False)
    id_receta = Column(Integer, ForeignKey('Recetas.numero_receta'), nullable=False)
    porcentaje = Column(Integer, nullable=False)

    ## Relationship with Proyeccion and Receta
    proyeccion = relationship("Proyeccion", back_populates="recetas")
    receta = relationship("Receta", back_populates="proyecciones")

    def __init__(self, id_receta: int, porcentaje: int) -> None:
        self.id_receta = id_receta
        self.porcentaje = porcentaje
