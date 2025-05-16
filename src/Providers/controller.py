import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Providers.model import Proveedor

class ProveedorController:
    ## @brief Create a new provider in the database.
    @staticmethod
    def create_proveedor(session: Session, name: str, category: str) -> Proveedor:
        """Create a new provider in the database."""
        new_provider = Proveedor(
            nombre=name,
            categoria=category
        )
        new_provider.create(session)
        return new_provider
    
    ## @brief Get a provider by its name from the database.
    @staticmethod
    def get_provider_by_name(session: Session, name: str) -> Proveedor:
        """Get a provider by its name from the database."""
        provider = Proveedor()
        provider.nombre = name
        return provider.read(session)
    
    ## @brief Get a provider by its ID from the database.
    @staticmethod
    def get_provider_by_id(session: Session, provider_id: int) -> Proveedor:
        """Get a provider by its ID from the database."""
        provider = Proveedor()
        provider.id_proveedor = provider_id
        return provider.read(session)
    
    ## @brief Update a provider in the database.
    @staticmethod
    def update_proveedor(session: Session, provider_id: int, name: str = None,
                           category: str = None) -> Proveedor | None:
        """Update a provider in the database."""
        provider = ProveedorController.get_provider_by_id(session, provider_id)
        if provider is None:
            return None

        if name:
            provider.nombre = name
        if category:
            provider.categoria = category
        
        provider.update(session, name, category)
        return provider

    ## @brief Delete a provider from the database.
    @staticmethod
    def delete_proveedor(session: Session, provider_id: int) -> bool:
        """Delete a provider from the database."""
        provider = ProveedorController.get_provider_by_id(session, provider_id)
        if provider is None:
            return False
        
        provider.delete(session)
        return True
    
    ## @brief Get all providers from the database.
    @staticmethod
    def get_all_providers(session: Session) -> list[Proveedor]:
        """Get all providers from the database."""
        provider = Proveedor()
        return provider.get_all_providers(session)
    
    ## @brief Get providers by name from the database.
    @staticmethod
    def get_providers_by_name(session: Session, name: str) -> list[Proveedor]:
        """Get providers by name from the database."""
        provider = Proveedor()
        return provider.get_providers_by_name(session, name)
    
    ## @brief Get providers by category from the database.
    @staticmethod
    def get_providers_by_category(session: Session, category: str) -> list[Proveedor]:
        """Get providers by category from the database."""
        provider = Proveedor()
        return provider.get_providers_by_category(session, category)