import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime import date, timedelta
from sqlalchemy.orm import Session
from src.Recipes.model import Receta
from src.Projections.model import Proyeccion

## @brief Clear trash can every session (if needed)
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