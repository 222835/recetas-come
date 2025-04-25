from typing import Self
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

"""@brief Cost model class
@details This class is used to represent a cost in the database"""
class Costos(Base):

    __tablename__ = "Costos"

    id_costo = Column(Integer, primary_key=True, autoincrement=True)
    id_proveedor = Column(Integer, foreign_key="Proveedores.id_proveedor", nullable=False)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)

    """@brief Constructor for the cost class
    @param nombre The name of the cost
    @param categoria The category of the cost (optional)"""
    def __init__(self, nombre: str, categoria: str | None = None) -> None:
        self.nombre = nombre
        self.categoria = categoria

    def __repr__(self) -> str:
        return f"Costo({self.nombre}, {self.categoria})"
    
    def create(self, session) -> None:
        """Insert a new cost into the database"""
        session.add(self)
        session.commit()

    def bulk_create(self, session, costs: list[Self]) -> None:
        """Insert multiple costs into the database"""
        session.add_all(costs)
        session.commit()
    
    def read(self, session) -> Self:
        """Fetch a cost from the database by its id"""
        return session.query(Costos).filter(Costos.id_costo == self.id_costo).first()
    
    def update(self, session, nombre: str | None = None, precio:int|None = None) -> None:
        """Update a cost's information in the database"""
        if nombre:
            self.nombre = nombre
        if precio:
            self.precio = precio
        session.commit()

    def delete(self, session) -> None:
        """Delete the cost from the database"""
        session.delete(self)
        session.commit()

    def get_all_costs(self, session) -> list[Self]:
        """Fetch all costs from the database"""
        return session.query(Costos).all()
    
