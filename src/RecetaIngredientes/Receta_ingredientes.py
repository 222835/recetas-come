import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from src.database.connector import Base

class RecetaIngrediente(Base):
    __tablename__ = 'receta_ingrediente'
    
    id_receta = Column(Integer, ForeignKey('recetas.id_receta', ondelete='CASCADE'), primary_key=True)
    id_ingrediente = Column(Integer, ForeignKey('ingredientes.id_ingrediente', ondelete='CASCADE'), primary_key=True)
    cantidad = Column(Float, nullable=False)
    
    receta = relationship("Receta", back_populates="receta_ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="receta_ingredientes")
