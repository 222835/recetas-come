import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Costs.model import Costos

## @brief CostController class
## @details This class is used to manage costs in the database.
## It provides methods to create, read, update, and delete costs.
## @note: This class uses the Costos model to interact with the database.
## @note: This class uses SQLAlchemy for database operations.
## @note: This class is designed to be used with a SQLAlchemy session.
class CostController:

    ## Create a new cost in the database.
    ## @param session: The database session.
    ## @param nombre: The name of the cost.
    ## @param precio: The price of the cost.
    ## @param id_proveedor: The ID of the provider.
    ## @return: The created Costos object.
    ## @details This method creates a new cost in the database and returns the created Costos object.
    ## @note: This method uses the create method of the Costos model to insert the cost into the database.
    @staticmethod
    def create_cost(session: Session, nombre: str, precio: int, id_proveedor: int) -> Costos:
        nuevo_cost = Costos(
            nombre=nombre,
            precio=precio,
            id_proveedor=id_proveedor
        )
        nuevo_cost.create(session)  # Use the model's create method
        return nuevo_cost
    
    ## @brief Get a cost by its name from the database.
    ## @param session: The database session.
    ## @param nombre_cost: The name of the cost.
    ## @return: The Costos object if found, None otherwise.
    ## @details This method retrieves a cost from the database based on its name.
    ## @note: This method uses the read method of the Costos model to fetch the cost.
    @staticmethod
    def get_cost_by_name(session: Session, nombre_cost: str) -> Costos:
        cost = Costos()
        cost.nombre = nombre_cost
        return cost.read(session)
    
    ## @brief Get a cost by its ID from the database.
    ## @param session: The database session.
    ## @param id_cost: The ID of the cost.
    ## @return: The Costos object if found, None otherwise.
    ## @details This method retrieves a cost from the database based on its ID.
    ## @note: This method uses the read method of the Costos model to fetch the cost.
    @staticmethod
    def get_cost_by_id(session: Session, id_cost: int) -> Costos:
        cost = Costos()
        cost.id_costo = id_cost
        return cost.read(session)  # Use the model's read method
    
    ## @brief Update a cost in the database.
    ## @param session: The database session.
    ## @param id_cost: The ID of the cost to update.
    ## @param nombre: The new name of the cost (optional).
    ## @param precio: The new price of the cost (optional).
    ## @return: The updated Costos object if successful, None otherwise.
    ## @details This method updates a cost in the database based on its ID.
    ## @note: This method uses the update method of the Costos model to modify the cost.
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

    ## @brief Delete a cost from the database.
    ## @param session: The database session.
    ## @param id_cost: The ID of the cost to delete.
    ## @return: True if the cost was deleted successfully, False otherwise.
    ## @details This method deletes a cost from the database based on its ID.
    ## @note: This method uses the delete method of the Costos model to remove the cost.
    @staticmethod
    def delete_cost(session: Session, id_cost: int) -> bool:
        """Delete a cost from the database."""
        cost = CostController.get_cost_by_id(session, id_cost)
        if cost is None:
            return False

        cost.delete(session)  # Use the model's delete method
        return True
    
    ## @brief Create multiple costs in the database.
    ## @param session: The database session.
    ## @param costs: A list of Costos objects to insert.
    ## @return: None
    ## @details This method inserts multiple costs into the database.
    ## @note: This method uses the bulk_create method of the Costos model to insert multiple costs.
    @staticmethod
    def create_costs(session: Session, costs: list[Costos]) -> None:
        """Insert multiple costs into the database."""
        Costos().bulk_create(session, costs)

    ## @brief Fetch all costs from the database.
    ## @param session: The database session.
    ## @return: A list of Costos objects.
    ## @details This method retrieves all costs from the database.
    ## @note: This method uses the get_all_costs method of the Costos model to fetch all costs.
    @staticmethod
    def get_all_costs(session: Session) -> list[Costos]:
        """Fetch all costs from the database."""
        cost = Costos()
        return cost.get_all_costs(session)  # Use the model's get_all_costs method
    
    ## @brief Fetch all costs by provider from the database.
    ## @param session: The database session.
    ## @param id_proveedor: The ID of the provider.
    ## @return: A list of Costos objects that belong to the provider.
    ## @details This method retrieves costs from the database based on the provided provider ID.
    ## @note: This method uses the filter method to fetch costs by provider ID.
    @staticmethod
    def fetch_costs_by_provider(session: Session, id_proveedor: int) -> list[Costos]:
        """Fetch all costs for a specific provider."""
        return session.query(Costos).filter(Costos.id_proveedor == id_proveedor).all()
    
    ## @brief Fetch all costs by name from the database.
    ## @param session: The database session.
    ## @param nombre: The name of the cost to fetch.
    ## @return: A list of Costos objects that match the name.
    ## @details This method retrieves costs from the database based on the provided name.
    ## @note: This method uses the filter method to fetch costs by name.
    @staticmethod
    def fetch_costs_by_name(session: Session, nombre: str) -> list[Costos]:
        """Fetch all costs by name."""
        return session.query(Costos).filter(Costos.nombre == nombre).all()
    
    ## @brief Search for costs by name in the database.
    ## @param session: The database session.
    ## @param nombre: The name of the cost to search for.
    ## @return: A list of Costos objects that match the search criteria.
    ## @details This method retrieves costs from the database based on the provided name.
    ## @note: This method uses the ilike method for case-insensitive search.
    @staticmethod
    def search_costs(session: Session, nombre: str) -> list[Costos]:
        """Search for costs by name."""
        return session.query(Costos).filter(Costos.nombre.ilike(f"%{nombre}%")).all()
    
    ## @brief Compare multiple costs by their IDs and return them in order.
    ## @param session: The database session.
    ## @param ids: A list of cost IDs to compare.
    ## @return: A list of Costos objects in the order of the price.
    ## @details This method retrieves costs from the database based on the provided IDs.
    @staticmethod
    def compare_multiple_costs(session: Session, ids: list[int]) -> list[Costos]:
        if not ids:
            return []
        
        costs = session.query(Costos).filter(Costos.id_costo.in_(ids)).all()
        # Sort by precio
        sorted_costs = sorted(costs, key=lambda x: x.precio)
        return sorted_costs
    
    
    @staticmethod
    def add_costs_for_provider_from_excel(session: Session, id_proveedor: int, file_location:str) -> list[Costos]:
        """Add costs for a provider from an Excel file."""
        
        # Read the Excel file
        df = pd.read_excel(file_location)
        
        costos = [Costos(nombre=row['nombre'], precio=row['precio'], id_proveedor=id_proveedor) for index, row in df.iterrows()]
        
        # Insert the costs into the database
        CostController.create_costs(session, costos)

        
        
        return costos
        