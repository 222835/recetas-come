import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from typing import List, Dict
from Projections.model import Proyeccion, ProyeccionRecetas
from Recipes.model import Receta

## @brief Validates the list of recipes for a projection.
def validate_recipes(recetas: List[Dict]):
    if len(recetas) < 2 or len(recetas) > 3:
        raise ValueError("Debes seleccionar entre 2 y 3 recetas.")

    total_porcentaje = sum(r['porcentaje'] for r in recetas)
    if total_porcentaje != 100:
        raise ValueError("La suma de los porcentajes debe ser 100%.")

## @brief Validates the list of recipes for a projection.
class ProyeccionController:
    @staticmethod
    def create_projection(session: Session, numero_usuario: int, nombre: str, periodo: str, comensales: int, recetas: List[Dict]) -> Proyeccion:
        validate_recipes(recetas)

        proyeccion = Proyeccion(numero_usuario, nombre, periodo, comensales)

        proyeccion.recetas = [ProyeccionRecetas(
                               id_receta=receta['id_receta'],
                               porcentaje=receta['porcentaje']
                           ) for receta in recetas]

        session.add(proyeccion)
        session.commit()

        return proyeccion
    
    @staticmethod
    def get_projection(session: Session, id_proyeccion: int) -> Proyeccion:
        return session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

    @staticmethod
    def update_projection(session: Session, id_proyeccion: int, nombre: str = None, periodo: str = None, comensales: int = None, recetas: List[Dict] = None):
        proyeccion = session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if not proyeccion:
            raise ValueError(f"La proyección con id {id_proyeccion} no existe.")

        if nombre:
            proyeccion.nombre = nombre
        if periodo:
            proyeccion.periodo = periodo
        if comensales:
            proyeccion.comensales = comensales
        
        if recetas:
            validate_recipes(recetas)
            proyeccion.recetas = [ProyeccionRecetas(
                                   id_receta=receta['id_receta'],
                                   porcentaje=receta['porcentaje']
                               ) for receta in recetas]

        session.commit()

    @staticmethod
    def delete_projection(session: Session, id_proyeccion: int):
        proyeccion = session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if not proyeccion:
            raise ValueError(f"La proyección con id {id_proyeccion} no existe.")

        session.delete(proyeccion)
        session.commit()

    @staticmethod
    def get_all_projections(session: Session, numero_usuario: int) -> List[Proyeccion]:
        return session.query(Proyeccion).filter_by(numero_usuario=numero_usuario).all()

    @staticmethod
    def calculate_total_ingredients(session: Session, id_proyeccion: int) -> Dict:
        proyeccion = session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if not proyeccion:
            raise ValueError(f"La proyección con id {id_proyeccion} no existe.")

        return proyeccion.calcular_ingredientes_totales(session)
