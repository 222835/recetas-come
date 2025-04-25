from typing import Self
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

##@brief Provider model class
##@details This class is used to represent a provider in the database
class Proveedor(Base):

    __tablename__ = "Proveedores"

    id_proveedor = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50))

    ##@brief Constructor for the provider class
    ##@param nombre The name of the provider
    ##@param categoria The category of the provider (optional)
    def __init__(self, nombre: str, categoria: str | None = None) -> None:
        self.nombre = nombre
        self.categoria = categoria

    def __repr__(self) -> str:
        return f"Proveedor({self.nombre}, {self.categoria})"

    ##@brief Insert a new provider into the database
    ##@param session The SQLAlchemy session
    def create(self, session) -> None:
        session.add(self)
        session.commit()

    ##@brief Fetch a provider from the database by its id
    ##@param session The SQLAlchemy session
    ##@return The provider object
    def read(self, session) -> Self:
        return session.query(Proveedor).filter(Proveedor.id_proveedor == self.id_proveedor).first()

    ##@brief Update a provider's information in the database
    ##@param session The SQLAlchemy session
    ##@param nombre The name of the provider (optional)
    ##@param categoria The category of the provider (optional)
    def update(self, session, nombre: str | None = None, categoria: str | None = None) -> None:
        if nombre:
            self.nombre = nombre
        if categoria:
            self.categoria = categoria
        session.commit()

    ##@brief Delete the provider from the database
    ##@param session The SQLAlchemy session
    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

    ##@brief Fetch all providers from the database
    ##@param session The SQLAlchemy session
    ##@return A list of all provider objects
    def get_all_providers(self, session) -> list[Self]:
        return session.query(Proveedor).all()
    
    ##@brief Fetch all providers by name from the database
    ##@param session The SQLAlchemy session
    ##@param nombre The name of the provider
    ##@return A list of provider objects that match the name
    def get_providers_by_name(self, session, nombre: str) -> list[Self]:
        return session.query(Proveedor).filter(Proveedor.nombre == nombre).all()
    
    ##@brief Fetch all providers by category from the database
    ##@param session The SQLAlchemy session
    ##@param categoria The category of the provider
    ##@return A list of provider objects that match the category
    def get_providers_by_category(self, session, categoria: str) -> list[Self]:
        return session.query(Proveedor).filter(Proveedor.categoria == categoria).all()
    
    