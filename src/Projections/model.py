import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.Recipes.model import Receta, Base


class Proyeccion(Base):
    __tablename__ = "Proyecciones"
    __table_args__ = {'extend_existing': True}

    id_proyeccion = Column(Integer, primary_key=True)
    numero_usuario = Column(Integer, ForeignKey('Usuarios.numero_usuario'), nullable=False)
    nombre = Column(String(100), nullable=False)
    periodo = Column(String(50), nullable=False)
    comensales = Column(Integer, nullable=False)

    def __init__(self, numero_usuario: int, nombre: str, periodo: str, comensales: int) -> None:
        self.numero_usuario = numero_usuario
        self.nombre = nombre
        self.periodo = periodo
        self.comensales = comensales

    def __repr__(self) -> str:
        return f"Proyeccion: {self.nombre}, {self.periodo}, {self.comensales} comensales"

    def calcular_ingredientes_totales(self, session) -> dict:
        ingredientes_totales = {}

        for proy_rec in session.query(Proyeccion).filter_by(id_proyeccion=self.id_proyeccion).all():
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
