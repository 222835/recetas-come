from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Proyecciones_Base = declarative_base()
##Data model for Proyecciones. This model is used to store the projections of the recipes.
class Proyeccion(Proyecciones_Base):
    __tablename__ = 'proyecciones'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    periodo = Column(String(50))
    comensales = Column(Integer)
    recetas_ids = Column(String(200)) 
    porcentajes = Column(String(200))

    def get_recetas(self):
        return [int(x) for x in self.recetas_ids.split(',') if x]

    def get_porcentajes(self):
        return [int(x) for x in self.porcentajes.split(',') if x]