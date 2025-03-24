import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy.orm import Session
from src.Providers.model import Proveedor

class ProveedorController:
    @staticmethod
    def create_proveedor(session: Session, nombre: str, categoria: str) -> Proveedor:
        """Create a new provider in the database."""
        nuevo_proveedor = Proveedor(
            nombre=nombre,
            categoria=categoria
        )
        session.add(nuevo_proveedor)
        session.commit()
        return nuevo_proveedor
    
    @staticmethod
    def get_proveedor_by_name(session: Session, nombre_proveedor: str) -> Proveedor:
        """Get a provider by its name from the database."""
        return session.query(Proveedor).filter(Proveedor.nombre == nombre_proveedor).first()
    
    @staticmethod
    def get_proveedor_by_id(session: Session, id_proveedor: int) -> Proveedor:
        """Get a provider by its ID from the database."""
        return session.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
    
    @staticmethod
    def update_proveedor(session: Session, id_proveedor: int, nombre: str = None,
                           categoria: str = None) -> Proveedor:
        """Update a provider in the database."""
        proveedor = ProveedorController.get_proveedor_by_id(session, id_proveedor)
        if proveedor is None:
            return None

        if nombre:
            proveedor.nombre = nombre
        if categoria:
            proveedor.categoria = categoria
        
        session.commit()
        return proveedor

    @staticmethod
    def delete_proveedor(session: Session, id_proveedor: int) -> bool:
        """Delete a provider from the database."""
        proveedor = ProveedorController.get_proveedor_by_id(session, id_proveedor)
        if proveedor is None:
            return False
        
        session.delete(proveedor)
        session.commit()
        return True