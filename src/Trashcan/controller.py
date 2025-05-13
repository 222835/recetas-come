import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime import date, timedelta
from sqlalchemy.orm import Session
from src.Recipes.model import Receta
from src.Recipes.controller import RecetasController
from src.Projections.model import Proyeccion
from src.Projections.controller import ProyeccionController

## Class used to manage the trashcan in the database
class TrashcanController:
    ## Return all deleted recipes.
    def get_deleted_recipes(session: Session):
        return session.query(Receta).filter(
            Receta.estatus == False
        ).all()

    ## Return all deleted projections.
    def get_deleted_projections(session: Session):
        return session.query(Proyeccion).filter(
            Proyeccion.estatus == False
        ).all()

    ## Restore a recepie (remove from trashcan)
    def restore_recipe(session: Session, id_receta: int) -> bool:
        receta = session.query(Receta).filter(
            Receta.id_receta == id_receta,
            Receta.estatus == False
        ).first()

        if receta:
            receta.estatus = True
            receta.fecha_eliminado = None
            session.commit()
            return True
        return False

    ## Restore a projection (remove from trashcan)
    def restore_projection(session: Session, id_proyeccion: int) -> bool:
        proyeccion = session.query(Proyeccion).filter(
            Proyeccion.id_proyeccion == id_proyeccion,
            Proyeccion.estatus == False
        ).first()

        if proyeccion:
            proyeccion.estatus = True
            proyeccion.fecha_eliminado = None
            session.commit()
            return True
        return False

    ## Delete recipe from trashcan (permanently).
    def delete_recipe_from_trashcan(session, id_receta: int, user_role: str) -> bool:
        receta = session.query(RecetasController.Receta).filter_by(id_receta=id_receta).first()
        
        if receta and not receta.estatus:
            return RecetasController.delete_recipe(session, id_receta, user_role)
        return False

    ## Delete projection from trashcan (permanently).
    def delete_projection_from_trashcan(session, id_proyeccion: int) -> bool:
        proyeccion = session.query(ProyeccionController.Proyeccion).filter_by(id_proyeccion=id_proyeccion).first()

        if proyeccion and not proyeccion.estatus:
            return ProyeccionController.delete_projection(session, id_proyeccion)
        return False # note for later: deletions in recipes and projections work diferently so this might be wrong bc it doesnt return anything

    ## Clear trash can every session (if needed)
    def clear_trashcan(session: Session):
        today = date.today()
        limit = today - timedelta(weeks=12)

        deleted_recipes = session.query(Receta).filter(
            Receta.estatus == False,
            Receta.fecha_eliminado != None,
            Receta.fecha_eliminado <= limit
        ).all()

        deleted_projections = session.query(Proyeccion).filter(
            Proyeccion.estatus == False,
            Proyeccion.fecha_eliminado != None,
            Proyeccion.fecha_eliminado <= limit
        ).all()

        for recipe in deleted_recipes:
            session.delete(recipe)

        for projection in deleted_projections:
            session.delete(projection)
        
        session.commit()