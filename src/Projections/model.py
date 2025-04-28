import os
import sys

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.connector import Base

## Data model for Proyecciones. This model is used to store the projections of the recipes.
class Proyeccion(Base):
    __tablename__ = "proyecciones"

    id_proyeccion = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100))
    periodo = Column(String(50))
    comensales = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    estatus = Column(Boolean, default=True)
    fecha_eliminado = Column(Date, nullable=True)

    ## Relationship with Recetas and ProyeccionRecetas.
    proyeccion_recetas = relationship("ProyeccionReceta", back_populates="proyeccion")

    ## Constructor of the class.
    def __init__(self, numero_usuario: int, nombre: str, periodo: str, comensales: int, fecha, estatus: bool = True, fecha_eliminado: Date | None = None) -> None:
        self.numero_usuario = numero_usuario
        self.nombre = nombre
        self.periodo = periodo
        self.comensales = comensales
        self.fecha = fecha
        self.estatus = estatus
        self.fecha_eliminado = fecha_eliminado

    ## Method to create a new projection in the database.
    def create(self, session):
        session.add(self)
        session.commit()

    ## Method to read a projection from the database.
    def read(self, session, id_proyeccion: int = None):
        if id_proyeccion:
            return session.query(Proyeccion).filter(Proyeccion.id_proyeccion == id_proyeccion).first()
        else:
            return session.query(Proyeccion).all()

    ## Method to update projections in the database.
    def update(self, session, nombre: str = None, periodo: str = None, comensales: int = None, fecha = None, estatus: bool = None, fecha_eliminado: Date | None = None):
        if nombre:
            self.nombre = nombre
        if periodo:
            self.periodo = periodo
        if comensales is not None:
            self.comensales = comensales
        if fecha:
            self.fecha = fecha
        if estatus is not None:
            self.estatus = estatus
        if fecha_eliminado is not None:
            self.fecha_eliminado = fecha_eliminado
        session.commit()

    ## Method to delete a projection from the database.
    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"Proyeccion: {self.nombre}, Periodo: {self.periodo}, Comensales: {self.comensales}, Fecha: {self.fecha}, Estatus: {self.estatus}, Fecha eliminada: {self.fecha_eliminado}"

### Data model for ProyeccionRecetas. This model is used to store the recipes of the projections.
class ProyeccionReceta(Base):
    __tablename__ = "Proyeccion_Recetas"
        
    id_proyeccion = Column(Integer, ForeignKey("proyecciones.id_proyeccion", ondelete="CASCADE"), primary_key=True)
    id_receta = Column(Integer, ForeignKey("recetas.id_receta", ondelete="CASCADE"), primary_key=True)
    porcentaje = Column(Integer, nullable=False)
    proyeccion = relationship("Proyeccion", back_populates="proyeccion_recetas")
    receta = relationship("Receta")  

    def __init__(self, id_proyeccion: int, id_receta: int, porcentaje: int) -> None:
        self.id_proyeccion = id_proyeccion
        self.id_receta = id_receta
        self.porcentaje = porcentaje

    def __repr__(self):
        return f"ProyeccionReceta: Proyeccion_ID={self.id_proyeccion}, Receta_ID={self.id_receta}"
