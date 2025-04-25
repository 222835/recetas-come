import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Costs.model import Costos

class CostController:
    @staticmethod
    def create_cost(session: Session, nombre: str, precio: int, id_proveedor: int) -> Costos:
        """Create a new cost in the database."""
        nuevo_cost = Costos(
            nombre=nombre,
            precio=precio,
            id_proveedor=id_proveedor
        )
        nuevo_cost.create(session)  # Use the model's create method
        return nuevo_cost
    
    @staticmethod
    def get_cost_by_name(session: Session, nombre_cost: str) -> Costos:
        """Get a cost by its name from the database."""
        cost = Costos()
        cost.nombre = nombre_cost
        return cost.read(session)
    
    @staticmethod
    def get_cost_by_id(session: Session, id_cost: int) -> Costos:
        """Get a cost by its ID from the database."""
        cost = Costos()
        cost.id_costo = id_cost
        return cost.read(session)  # Use the model's read method
    
    @staticmethod
    def update_cost(session: Session, id_cost: int, nombre: str = None,
                     precio: int = None) -> Costos | tuple[None, str]:
        """Update a cost in the database."""
        cost = CostController.get_cost_by_id(session, id_cost)
        if cost is None:
            return None, "Cost not found"
        
        if nombre:
            cost.nombre = nombre
        if precio:
            cost.precio = precio
        cost.update(session)  # Use the model's update method
        return cost

    @staticmethod
    def delete_cost(session: Session, id_cost: int) -> bool:
        """Delete a cost from the database."""
        cost = CostController.get_cost_by_id(session, id_cost)
        if cost is None:
            return False

        cost.delete(session)  # Use the model's delete method
        return True
    
    @staticmethod
    def create_costs(session: Session, costs: list[Costos]) -> None:
        """Insert multiple costs into the database."""
        Costos().bulk_create(session, costs)

    @staticmethod
    def get_all_costs(session: Session) -> list[Costos]:
        """Fetch all costs from the database."""
        cost = Costos()
        return cost.get_all_costs(session)  # Use the model's get_all_costs method
    
    @staticmethod
    def fetch_costs_by_provider(session: Session, id_proveedor: int) -> list[Costos]:
        """Fetch all costs for a specific provider."""
        return session.query(Costos).filter(Costos.id_proveedor == id_proveedor).all()
    
    @staticmethod
    def fetch_costs_by_name(session: Session, nombre: str) -> list[Costos]:
        """Fetch all costs by name."""
        return session.query(Costos).filter(Costos.nombre == nombre).all()
    
    @staticmethod
    def search_costs(session: Session, nombre: str) -> list[Costos]:
        """Search for costs by name."""
        return session.query(Costos).filter(Costos.nombre.ilike(f"%{nombre}%")).all()