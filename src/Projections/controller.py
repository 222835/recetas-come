import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from typing import List, Dict
from src.Projections.model import Proyeccion
from src.Recipes.model import Receta
## @brief Validate the list of recipes and their percentages.
def validate_recipes(recetas: List[Dict]):
    if not recetas:
        raise ValueError("Debe haber al menos 1 receta.")
    
    ##Add validation to match test case: at least 2 recipes required
    if len(recetas) < 2:
        raise ValueError("La proyeccion debe incluir al menos 2 recetas")
    
    if len(recetas) > 3:
        raise ValueError("Maximo 3 recetas permitidas.")

    total = sum(r.get('porcentaje', 0) for r in recetas)
    if total != 100:
        raise ValueError(f"La suma de porcentajes debe ser 100% (actual: {total}%)")
## @brief Class to manage projections in the database.This class provides methods to create, update, delete, and retrieve projections.
class ProyeccionController:
    @staticmethod
    def create_projection(
        session: Session,
        nombre: str,
        periodo: str,
        comensales: int,
        recetas: List[Dict]
    ) -> Proyeccion:
        validate_recipes(recetas)
        
        ids = ",".join(str(r['id_receta']) for r in recetas)
        porcentajes = ",".join(str(r['porcentaje']) for r in recetas)
        
        proyeccion = Proyeccion(
            nombre=nombre,
            periodo=periodo,
            comensales=comensales,
            recetas_ids=ids,
            porcentajes=porcentajes
        )
        
        session.add(proyeccion)
        session.commit()
        return proyeccion
    ## @brief Get a projection by its ID.
    @staticmethod
    def get_projection(session: Session, id_proyeccion: int) -> Proyeccion:
        return session.get(Proyeccion, id_proyeccion)

    ## @brief Update a projection in the database.
    @staticmethod
    def update_projection(
        session: Session,
        id_proyeccion: int,
        nombre: str = None,
        periodo: str = None,
        comensales: int = None,
        recetas: List[Dict] = None
    ):
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"Proyeccion {id_proyeccion} no encontrada")

        if nombre:
            proyeccion.nombre = nombre
        if periodo:
            proyeccion.periodo = periodo
        if comensales:
            proyeccion.comensales = comensales
        if recetas:
            validate_recipes(recetas)
            proyeccion.recetas_ids = ",".join(str(r['id_receta']) for r in recetas)
            proyeccion.porcentajes = ",".join(str(r['porcentaje']) for r in recetas)

        session.commit()
        return proyeccion 

    ## @brief Delete a projection from the database.
    @staticmethod
    def delete_projection(session: Session, id_proyeccion: int):
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if proyeccion:
            session.delete(proyeccion)
            session.commit()

    ## @brief Get all projections from the database.
    @staticmethod
    def get_all_projections(session: Session) -> List[Proyeccion]:
        return session.query(Proyeccion).all()
    
    ## @brief Calculate the total ingredients needed for a projection.
    @staticmethod
    def calculate_total_ingredients(session: Session, id_proyeccion: int) -> Dict:
        
        proyeccion = session.get(Proyeccion, id_proyeccion)
        if not proyeccion:
            raise ValueError(f"Proyeccion {id_proyeccion} no encontrada")
        
        receta_ids = [int(id) for id in proyeccion.recetas_ids.split(',')]
        porcentajes = [int(p) for p in proyeccion.porcentajes.split(',')]
        
        ingredientes_totales = {}
        
        for i, receta_id in enumerate(receta_ids):
            receta = session.get(Receta, receta_id)
            if not receta:
                continue
            
            ingredientes_lista = receta.ingredientes.split(',')
            factor = (porcentajes[i]/100) * (proyeccion.comensales / receta.comensales_base)
            
            for ingrediente in ingredientes_lista:
                ingrediente = ingrediente.strip()
                if ingrediente in ingredientes_totales:
                    ingredientes_totales[ingrediente] += factor
                else:
                    ingredientes_totales[ingrediente] = factor
        
        return ingredientes_totales