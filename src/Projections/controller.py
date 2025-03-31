import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from Projections.model import Proyeccion, ProyeccionRecetas

## @brief projection controller, this class is responsible for managing the projections of recipes for users.     
class ProyeccionController:

    ## @brief Method to create a projection of recipes for a user.
    @staticmethod
    def create_projection(session: Session, numero_usuario: int, nombre: str, periodo: str, comensales: int, recetas: list[dict]):
        if len(recetas) < 2 or len(recetas) > 3:
            raise ValueError("Debes seleccionar entre 2 y 3 recetas.")

        total_porcentaje = sum(r['porcentaje'] for r in recetas)
        if total_porcentaje != 100:
            raise ValueError("La suma de los porcentajes debe ser 100%.")

        proyeccion = Proyeccion(numero_usuario, nombre, periodo, comensales)

        for receta in recetas:
            proy_rec = ProyeccionRecetas(
                id_proyeccion=proyeccion.id_proyeccion,
                id_receta=receta['id_receta'],
                porcentaje=receta['porcentaje']
            )
            proyeccion.recetas.append(proy_rec)

        session.add(proyeccion)
        session.commit()

        return proyeccion
    
    ## @brief Method to get all projections of a user.
    @staticmethod
    def get_projection(session: Session, id_proyeccion: int) -> Proyeccion:
        return session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

    ## @brief Method to get all projections of a user.
    @staticmethod
    def update_projection(session: Session, id_proyeccion: int, nombre: str = None, periodo: str = None, comensales: int = None):
        proyeccion = session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if not proyeccion:
            raise ValueError("La proyección no existe.")

        if nombre:
            proyeccion.nombre = nombre
        if periodo:
            proyeccion.periodo = periodo
        if comensales:
            proyeccion.comensales = comensales

        session.commit()

    ## @brief Method to delete a projection of recipes for a user.
    @staticmethod
    def delete_projection(session: Session, id_proyeccion: int):
        proyeccion = session.query(Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if not proyeccion:
            raise ValueError("La proyección no existe.")

        session.delete(proyeccion)
        session.commit()